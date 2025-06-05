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

# =============================================================================
# Booleans
# =============================================================================

A = box.to_polyhedron(triangulated=True, u=64)
B = sphere.to_polyhedron(triangulated=True, u=64, v=64)

Cx = cx.to_polyhedron(triangulated=True, u=64)
Cy = cy.to_polyhedron(triangulated=True, u=64)
Cz = cz.to_polyhedron(triangulated=True, u=64)

result = A & B
result = result - Cx
result = result - Cy
# result = result - Cz

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()
viewer.scene.add(result)
viewer.show()
