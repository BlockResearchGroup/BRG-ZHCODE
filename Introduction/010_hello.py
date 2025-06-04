# Just create and visualize a red box

from compas.colors import Color
from compas.geometry import Box
from compas_viewer.viewer import Viewer

box = Box(1)

viewer = Viewer()
viewer.scene.add(box, surfacecolor=Color.red())
viewer.show()
