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

templates: list[Geometry] = [
    Box(xsize=1, ysize=0.5, zsize=0.25),
    Cone(radius=0.3, height=1.0),
    Cylinder(radius=0.3, height=1.0),
    Sphere(radius=0.5),
    Torus(radius_axis=0.5, radius_pipe=0.2),
]

cloud = Pointcloud.from_bounds(x=10, y=10, z=10, n=256)

shapes = []

for point in cloud:
    shape: Geometry = random.choice(templates).copy()
    shape.rotate(angle=random.random(), axis=[1, 0, 0])
    shape.rotate(angle=random.random(), axis=[0, 1, 0])
    shape.rotate(angle=random.random(), axis=[0, 0, 1])
    shape.translate(point)
    shapes.append(shape)

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

viewer.scene.add(cloud)

group = viewer.scene.add_group(name="Shapes")
for shape in shapes:
    color = Color.from_number(random.random())
    group.add(shape, surfacecolor=color, linecolor=color.contrast)  # type: ignore

viewer.show()
