import pathlib

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import bestfit_frame_numpy
from compas.geometry import trimesh_remesh
from compas.itertools import pairwise
from compas.scene import MeshObject
from compas.scene import Scene
from compas_libigl.mapping import map_mesh
from compas_viewer.viewer import Viewer
from tessagon.adaptors.list_adaptor import ListAdaptor
from tessagon.types.brick_tessagon import BrickTessagon
from tessagon.types.octo_tessagon import OctoTessagon
from tessagon.types.zig_zag_tessagon import ZigZagTessagon

# =============================================================================
# Session data
# =============================================================================

HERE = pathlib.Path(__file__).parent
DATA = HERE.parent / "data"
SESSION = DATA / "RhinoVAULT.json"
session = compas.json_load(SESSION)

# =============================================================================
# RV mesh
# =============================================================================

scene: Scene = session["scene"]
sceneobj: MeshObject = scene.find_by_name("ThrustDiagram")  # type: ignore
mesh: Mesh = sceneobj.mesh

for face in list(mesh.faces_where(_is_loaded=False)):
    mesh.delete_face(face)

# =============================================================================
# Remeshed triangle mesh
# =============================================================================

trimesh: Mesh = mesh.copy()
trimesh.quads_to_triangles()

average_length = sum(mesh.edge_length(edge) for edge in mesh.edges()) / mesh.number_of_edges()
target_edge_length = 1 * average_length

V, F = trimesh_remesh(
    trimesh.to_vertices_and_faces(),
    target_edge_length=target_edge_length,
    number_of_iterations=100,
)  # type: ignore

trimesh = Mesh.from_vertices_and_faces(V, F)

# =============================================================================
# Pattern mapping
# =============================================================================

options = {
    "function": lambda u, v: [u, v, 0],
    "u_range": [-0.25, 1.25],
    "v_range": [-0.25, 1.25],
    "u_num": 16,
    "v_num": 16,
    "u_cyclic": False,
    "v_cyclic": False,
    "adaptor_class": ListAdaptor,
}

tessagon = OctoTessagon(**options)
tessagon_mesh = tessagon.create_mesh()
pv = tessagon_mesh["vert_list"]
pf = tessagon_mesh["face_list"]

v, f = trimesh.to_vertices_and_faces()

mv, mf = map_mesh((v, f), (pv, pf), clip_boundaries=True, tolerance=1e-6)
pattern = Mesh.from_vertices_and_faces(mv, mf)

# =============================================================================
# Thickness
# =============================================================================

pattern.update_default_vertex_attributes(thickness=0)

zvalues: list[float] = pattern.vertices_attribute(name="z")  # type: ignore
zmin = min(zvalues)
zmax = max(zvalues)

tmin = 0.03
tmax = 0.3

for vertex in pattern.vertices():
    point = pattern.vertex_point(vertex)
    normal = pattern.vertex_normal(vertex)
    z = (point.z - zmin) / (zmax - zmin)
    thickness = (1 - z) * (tmax - tmin) + tmin
    pattern.vertex_attribute(vertex, name="thickness", value=thickness)

# =============================================================================
# Intrados
# =============================================================================

idos: Mesh = pattern.copy()

for vertex in idos.vertices():
    point = pattern.vertex_point(vertex)
    normal = pattern.vertex_normal(vertex)
    thickness = pattern.vertex_attribute(vertex, name="thickness")
    idos.vertex_attributes(vertex, names="xyz", values=point - normal * (0.5 * thickness))  # type: ignore

# =============================================================================
# blocks
# =============================================================================

blocks: list[Mesh] = []

for face in pattern.faces():
    vertices = pattern.face_vertices(face)
    normals = [pattern.vertex_normal(vertex) for vertex in vertices]
    thickness = pattern.vertices_attribute("thickness", keys=vertices)

    bottom = idos.vertices_points(vertices)
    top = [point + vector * t for point, vector, t in zip(bottom, normals, thickness)]  # type: ignore

    frame = Frame(*bestfit_frame_numpy(top))
    plane = Plane.from_frame(frame)

    flattop = []
    for a, b in zip(bottom, top):
        b = plane.intersection_with_line(Line(a, b))
        flattop.append(b)

    sides = []
    for (a, b), (aa, bb) in zip(pairwise(bottom + bottom[:1]), pairwise(flattop + flattop[:1])):
        sides.append([a, b, bb, aa])

    polygons = [bottom[::-1], flattop] + sides

    block: Mesh = Mesh.from_polygons(polygons)
    blocks.append(block)

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

viewer.scene.add(trimesh, name="TriMesh")
viewer.scene.add(pattern, name="Pattern", facecolor=Color.red())

group = viewer.scene.add_group(name="Blocks")
group.add_from_list(blocks)  # type: ignore

viewer.show()
