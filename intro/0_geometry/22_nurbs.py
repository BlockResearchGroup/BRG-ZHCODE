from compas.colors import Color
from compas.geometry import NurbsSurface
from compas.geometry import Point
from compas.itertools import linspace
from compas_viewer import Viewer

points = [
    [Point(0, 0, 0), Point(1, 0, 0), Point(2, 0, 0), Point(3, 0, 0), Point(4, 0, 0)],
    [Point(0, 1, 0), Point(1, 1, 2), Point(2, 1, 2), Point(3, 1, 0), Point(4, 1, 0)],
    [Point(0, 2, 0), Point(1, 2, 2), Point(2, 2, 2), Point(3, 2, 0), Point(4, 2, 0)],
    [Point(0, 3, 0), Point(1, 3, 0), Point(2, 3, 0), Point(3, 3, 0), Point(4, 3, 0)],
]

surface = NurbsSurface.from_points(points=points)

# ==============================================================================
# Viz
# ==============================================================================

viewer = Viewer()

viewer.scene.add(surface)

u_curves = viewer.scene.add_group(name="U Curves")
for u in linspace(*surface.domain_u, num=17):
    u_curves.add(surface.isocurve_u(u).to_polyline())

v_curves = viewer.scene.add_group(name="V Curves")
for v in linspace(*surface.domain_v, num=17):
    v_curves.add(surface.isocurve_v(v).to_polyline(), linecolor=Color.red())  # type: ignore

viewer.show()
