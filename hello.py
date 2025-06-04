import compas
from compas.datastructures import Mesh
from compas_viewer.viewer import Viewer

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

viewer = Viewer()
viewer.scene.add(mesh)
viewer.show()
