import compas
from compas.geometry import Box

box = Box(1)

compas.json_dump(box, "box.json")
