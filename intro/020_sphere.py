# Make a box in different ways
# and inspect its attributes

from compas.colors import Color
from compas.geometry import Sphere
from compas_viewer.viewer import Viewer

sphere = Sphere(radius=1)

print(sphere.frame)
print(sphere.radius)

sphere.resolution_u = 8
sphere.resolution_v = 8

print(len(sphere.vertices))
print(len(sphere.edges))
print(len(sphere.faces))

viewer = Viewer()
viewer.scene.add(sphere, u=8, v=8, surfacecolor=Color.pink(), linecolor=Color.pink().contrast)
viewer.show()
