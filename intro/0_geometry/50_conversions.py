from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import Polyhedron
from compas_viewer.viewer import Viewer

a = Box(1)
b = Box(1, frame=Frame(point=a.points[6]))

# =============================================================================
# Conversions
# =============================================================================

A = a.to_polyhedron(triangulated=True)

mesh: Mesh = b.to_mesh()
subd: Mesh = mesh.subdivided(k=3)
subd.quads_to_triangles()

V, F = subd.to_vertices_and_faces()

B = Polyhedron(V, F)

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
