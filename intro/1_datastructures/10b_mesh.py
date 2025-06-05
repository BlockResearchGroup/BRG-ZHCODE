import compas
from compas.datastructures import Mesh
from compas.utilities import print_profile
from compas_cgal.meshing import mesh_remesh
from compas_viewer.viewer import Viewer

mesh = Mesh.from_ply(compas.get("bunny.ply"))

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()
viewer.scene.add(mesh)
viewer.show()
