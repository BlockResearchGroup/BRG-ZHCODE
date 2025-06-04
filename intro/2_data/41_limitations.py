import compas
from compas.geometry import Box

box = Box(1).to_brep()

compas.json_dump(box, "box.json")
