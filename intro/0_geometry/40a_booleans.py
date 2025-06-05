from compas.geometry import Box
from compas.geometry import Sphere
from compas_viewer.viewer import Viewer

box = Box(1)
sphere = Sphere(point=box.points[6], radius=0.5)

# =============================================================================
# Conversions
# =============================================================================

A = box.to_polyhedron(triangulated=True)
B = sphere.to_polyhedron(triangulated=True)

# =============================================================================
# Booleans
# =============================================================================

C = A + B

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()
viewer.scene.add(C)
viewer.show()
