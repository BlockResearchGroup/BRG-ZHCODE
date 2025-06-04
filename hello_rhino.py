#! python3
# venv: zha-intro-rhino

import compas
from compas.datastructures import Mesh
from compas.scene import Scene

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

scene = Scene()
scene.clear_context()
scene.add(mesh, disjoint=True, color="#00ff00")
scene.draw()
