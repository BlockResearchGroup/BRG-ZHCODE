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
from compas_libigl.mapping import map_pattern_to_mesh
from compas_viewer.viewer import Viewer

# =============================================================================
# Session data
# =============================================================================

HERE = pathlib.Path(__file__).parent
DATA = HERE.parent.parent / "data"
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

pattern = map_pattern_to_mesh(
    name="ZigZag",
    mesh=trimesh,
    tolerance=1e-3,
    clip_boundaries=True,
    pattern_u=16,
    pattern_v=16,
)

# =============================================================================
# Thickness
# =============================================================================

pattern.update_default_vertex_attributes(thickness=0)

zvalues: list[float] = pattern.vertices_attribute(name="z")  # type: ignore
zmin = min(zvalues)
zmax = max(zvalues)

tmin = 0.1
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

# viewer.scene.add(trimesh, name="TriMesh")
viewer.scene.add(pattern, name="Pattern", facecolor=Color.red(), opacity=0.5)

group = viewer.scene.add_group(name="Normals")
for face in pattern.faces():
    point = pattern.face_centroid(face)
    normal = pattern.face_normal(face)
    line = Line.from_point_direction_length(point, normal, 0.3)
    group.add(line, linecolor=Color.blue())  # type: ignore

group = viewer.scene.add_group(name="Blocks")
group.add_from_list(blocks, show_faces=True, opacity=0.5)  # type: ignore

viewer.show()
