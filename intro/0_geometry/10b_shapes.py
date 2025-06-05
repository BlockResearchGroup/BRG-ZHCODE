import random

from compas.colors import Color
from compas.geometry import Box
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Geometry
from compas.geometry import Pointcloud
from compas.geometry import Sphere
from compas.geometry import Torus
from compas_viewer.viewer import Viewer

templates = [
    Box(xsize=1, ysize=0.5, zsize=0.25),
    Cone(radius=0.3, height=1.0),
    Cylinder(radius=0.3, height=1.0),
    Sphere(radius=0.5),
    Torus(radius_axis=0.5, radius_pipe=0.2),
]

cloud = Pointcloud.from_bounds(x=10, y=10, z=10, n=256)

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

viewer.scene.add(cloud)

viewer.show()
