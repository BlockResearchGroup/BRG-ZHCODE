from compas.geometry import Box
from compas.geometry import Brep
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Sphere
from compas_gmsh.models import MeshModel
from compas_viewer.viewer import Viewer

R = 1.4
YZ = Frame.worldYZ()
ZX = Frame.worldZX()
XY = Frame.worldXY()

box = Box(2 * R).to_brep()
sphere = Sphere(radius=1.25 * R).to_brep()

cx = Cylinder(0.7 * R, 4 * R, frame=YZ).to_brep()
cy = Cylinder(0.7 * R, 4 * R, frame=ZX).to_brep()
cz = Cylinder(0.7 * R, 4 * R, frame=XY).to_brep()

result = Brep.from_boolean_difference(box & sphere, cz + cx + cy)

# =============================================================================
# Meshing
# =============================================================================

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()
viewer.scene.add(result)
viewer.show()
