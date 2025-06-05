import compas
from compas_viewer.viewer import Viewer

box = compas.json_load("box.json")

viewer = Viewer()
viewer.scene.add(box)
viewer.show()
