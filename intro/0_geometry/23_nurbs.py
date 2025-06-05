import random

from compas.colors import Color
from compas.geometry import NurbsSurface
from compas.geometry import Polyline
from compas.itertools import flatten
from compas.itertools import linspace
from compas_viewer import Viewer

U = 10
V = 20

surface = NurbsSurface.from_meshgrid(nu=U, nv=V)

# ==============================================================================
# Update
# ==============================================================================

for u in range(1, U):
    for v in range(1, V):
        point = surface.points[u, v]
        point.z = random.choice([+1, -1]) * random.random()
        surface.points[u, v] = point

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = Viewer()

viewer.scene.add(surface)

# control polygon

points = list(surface.points)

group = viewer.scene.add_group(name="Control")

rowgroup = viewer.scene.add_group(name="Rows", parent=group)
colgroup = viewer.scene.add_group(name="Cols", parent=group)
pntgroup = viewer.scene.add_group(name="Points", parent=group)

rowgroup.add_from_list([Polyline(row) for row in points], linecolor=Color(0.3, 0.3, 0.3))  # type: ignore
colgroup.add_from_list([Polyline(col) for col in zip(*points)], linecolor=Color(0.3, 0.3, 0.3))  # type: ignore
pntgroup.add_from_list(list(flatten(points)), pointsize=10)  # type: ignore

# isocurves

u_curves = viewer.scene.add_group(name="U Curves")
for u in linspace(*surface.domain_u, num=53):
    u_curves.add(surface.isocurve_u(u).to_polyline())

v_curves = viewer.scene.add_group(name="V Curves")
for v in linspace(*surface.domain_v, num=53):
    v_curves.add(surface.isocurve_v(v).to_polyline())

viewer.show()
