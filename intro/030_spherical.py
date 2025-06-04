# Get more familiar with the code using the spherical surface as an example.
# Explore link between parametric definition of the analytical geometry and discrete representations.

from compas.colors import Color
from compas.geometry import Pointcloud
from compas.geometry import Polyline
from compas.geometry import SphericalSurface
from compas.itertools import linspace
from compas_viewer.viewer import Viewer

surface = SphericalSurface(radius=10)

patch = surface.to_polyhedron(nu=64, nv=64, du=[0, 1], dv=[0, 1])

points = []
polylines = []
for j in linspace(0, 1, 65):
    temp = [surface.point_at(u=i, v=j) for i in linspace(0, 1, 65)]
    polyline = Polyline(temp)

    points += temp
    polylines.append(polyline)

isocurve_u = surface.isocurve_u(u=0.3)
isocurve_v = surface.isocurve_v(v=0.3)

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

viewer.scene.add(patch, name="Patch", color=Color.cyan(), pointcolor=Color.blue(), show_points=True)

# group = viewer.scene.add_group(name="Points")
# group.add_from_list(points, pointcolor=Color.red())

viewer.scene.add(Pointcloud(points), color=Color.red(), pointsize=5, name="Cloud")

group = viewer.scene.add_group(name="Polylines")
group.add_from_list(polylines, linecolor=Color.green())  # type: ignore

viewer.scene.add(isocurve_u, u=128, name="Isocurve U")
viewer.scene.add(isocurve_v, u=128, name="Isocurve V")

viewer.show()
