import compas
from compas.datastructures import Mesh
from compas.geometry import Box

box = Box(1)
mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

session = {
    "box": box,
    "mesh": mesh,
}

compas.json_dump(session, "session.json")
