from compas.geometry import Box
from compas_viewer.viewer import Viewer

box = Box(1)

viewer = Viewer()
viewer.scene.add(box)
viewer.show()
