from compas.geometry import Box
from compas.geometry import Brep
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Sphere
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
# Conversions
# =============================================================================

# =============================================================================
# Booleans
# =============================================================================

# =============================================================================
# Meshing
# =============================================================================

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()


viewer.show()
