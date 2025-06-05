from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import NurbsCurve
from compas.geometry import Point
from compas.geometry import Polyline
from compas.geometry import Transformation
from compas.itertools import linspace
from compas_viewer.viewer import Viewer

box = Box(xsize=1, ysize=0.5, zsize=0.3)

points = [
    Point(0, 0, 0),
    Point(3, 6, 0),
    Point(6, -6, 3),
    Point(9, 0, 0),
]

curve = NurbsCurve.from_points(points)

for u in linspace(*curve.domain, 53):
    pass

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

viewer.scene.add(curve, name="NurbsCurve")
viewer.scene.add(Polyline(points), show_points=True, name="ControlPoly")

viewer.show()
