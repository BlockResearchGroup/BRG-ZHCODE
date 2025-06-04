import compas
from compas.geometry import Box

box = Box(1)

print(box.__data__)
print(box.__dtype__)

print(compas.json_dumps(box, pretty=True))
