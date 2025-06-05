from compas.colors import Color
from compas.datastructures import Graph
from compas.geometry import Cylinder
from compas.geometry import Line
from compas.geometry import Pointcloud
from compas.itertools import pairwise
from compas_viewer.viewer import Viewer

cloud = Pointcloud.from_bounds(10, 10, 0, 53)
graph = Graph.from_pointcloud(cloud, degree=3)

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

viewer.scene.add(graph, show_points=True, pointsize=10)

viewer.show()
