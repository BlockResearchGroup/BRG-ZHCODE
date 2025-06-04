from compas.geometry import Box
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Polyhedron
from compas.geometry import Sphere
from compas.geometry import boolean_difference_mesh_mesh
from compas.geometry import boolean_intersection_mesh_mesh
from compas_viewer.viewer import Viewer

R = 1.4
YZ = Frame.worldYZ()
ZX = Frame.worldZX()
XY = Frame.worldXY()

box = Box(2 * R)
sphere = Sphere(radius=1.25 * R)

cx = Cylinder(0.7 * R, 4 * R, frame=YZ)
cy = Cylinder(0.7 * R, 4 * R, frame=ZX)
cz = Cylinder(0.7 * R, 4 * R, frame=XY)

A = boolean_intersection_mesh_mesh(
    box.to_vertices_and_faces(triangulated=True),
    sphere.to_vertices_and_faces(triangulated=True),
)

for B in (cx, cy):
    A = boolean_difference_mesh_mesh(A, B.to_vertices_and_faces(triangulated=True))

result = Polyhedron(*A)  # type: ignore

# =============================================================================
# Viz
# =============================================================================

# TOL.lineardeflection = 0.1

viewer = Viewer()
viewer.scene.add(result)
viewer.show()
