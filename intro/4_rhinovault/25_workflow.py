import pathlib

from compas.datastructures import Mesh
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import bestfit_frame_numpy
from compas.itertools import pairwise
from compas_session.lazyload import LazyLoadSession
from compas_viewer.viewer import Viewer

HERE = pathlib.Path(__file__).parent

session = LazyLoadSession(name="RV", basedir=HERE)

# =============================================================================
# Session data
# =============================================================================

pattern: Mesh = session["pattern"]

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
# Export
# =============================================================================

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

group = viewer.scene.add_group(name="Blocks")
group.add_from_list(blocks, show_faces=True, opacity=0.5)  # type: ignore

viewer.show()
