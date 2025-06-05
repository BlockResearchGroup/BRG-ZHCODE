from compas.colors import Color
from compas.geometry import Pointcloud
from compas.geometry import Polyline
from compas.geometry import SphericalSurface
from compas.itertools import linspace
from compas_viewer.viewer import Viewer

U = 48
V = 48

surface = SphericalSurface(radius=5)

patch = surface.to_polyhedron(nu=U, nv=V, du=[0, 1.0], dv=[0, 1.0])

points = []
polylines = []

for j in linspace(0, 1, U + 1):
    temp = [surface.point_at(u=i, v=j) for i in linspace(0, 1, V + 1)]
    points += temp

    polyline = Polyline(temp)
    polylines.append(polyline)

isocurve_u = surface.isocurve_u(u=0.3)
isocurve_v = surface.isocurve_v(v=0.3)

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

viewer.scene.add(
    patch,
    color=Color.cyan(),
    pointcolor=Color.blue(),
    linecolor=Color.blue(),
    show_points=True,
    show_lines=True,
    name="Patch",
)

viewer.scene.add(Pointcloud(points), color=Color.red(), pointsize=5, name="Cloud")

group = viewer.scene.add_group(name="Polylines")
group.add_from_list(polylines, linecolor=Color.green())  # type: ignore

viewer.scene.add(isocurve_u, u=128, name="Isocurve U")
viewer.scene.add(isocurve_v, u=128, name="Isocurve V")

viewer.show()
