import pathlib

from compas.datastructures import Mesh
from compas.geometry import trimesh_remesh
from compas_session.lazyload import LazyLoadSession
from compas_viewer.viewer import Viewer

HERE = pathlib.Path(__file__).parent

session = LazyLoadSession(name="RV", basedir=HERE)

# =============================================================================
# Session data
# =============================================================================

basemesh: Mesh = session["basemesh"]

# =============================================================================
# Remeshed triangle mesh
# =============================================================================

trimesh: Mesh = basemesh.copy()
trimesh.quads_to_triangles()

average_length = sum(basemesh.edge_length(edge) for edge in basemesh.edges()) / basemesh.number_of_edges()
target_edge_length = 0.5 * average_length

VF = trimesh.to_vertices_and_faces()

V, F = trimesh_remesh(VF, target_edge_length=target_edge_length)  # type: ignore

trimesh = Mesh.from_vertices_and_faces(V, F)

# =============================================================================
# Export
# =============================================================================

session["trimesh"] = trimesh
session.dump()

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

viewer.scene.add(trimesh, name="TriMesh")

viewer.show()
