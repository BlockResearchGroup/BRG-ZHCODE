from compas.colors import Color
from compas.datastructures import Graph
from compas.geometry import Cylinder
from compas.geometry import Line
from compas.geometry import Pointcloud
from compas.itertools import pairwise
from compas_viewer.viewer import Viewer

cloud = Pointcloud.from_bounds(10, 10, 0, 53)
graph = Graph.from_pointcloud(cloud, degree=3)

start, end = graph.node_sample(size=2)

path: list[int] = graph.shortest_path(start, end)  # type: ignore

points = [graph.node_point(node) for node in path]
segments = [Cylinder.from_line_and_radius(Line(a, b), 0.03) for a, b in pairwise(points)]

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()
viewer.scene.add(graph, show_points=True, pointsize=10)

group = viewer.scene.add_group(name="Shortest Path")
pathnodes = viewer.scene.add_group(name="Nodes", parent=group)
pathedges = viewer.scene.add_group(name="Edges", parent=group)

pathnodes.add_from_list(points, pointsize=20, pointcolor=Color.red())  # type: ignore
pathedges.add_from_list(segments, color=Color.blue())  # type: ignore

viewer.show()
