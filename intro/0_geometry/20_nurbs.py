from compas.geometry import NurbsCurve
from compas.geometry import Point
from compas.geometry import Polyline
from compas_viewer.viewer import Viewer

points = [
    Point(0, 0, 0),
    Point(3, 6, 0),
    Point(6, -6, 3),
    Point(9, 0, 0),
]

curve = NurbsCurve.from_points(points)

viewer = Viewer()
viewer.scene.add(curve, name="NurbsCurve")
viewer.scene.add(Polyline(points), show_points=True, name="ControlPoly")
viewer.show()
