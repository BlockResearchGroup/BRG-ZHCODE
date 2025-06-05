import pathlib

from compas.datastructures import Mesh
from compas_libigl.mapping import map_pattern_to_mesh
from compas_session.lazyload import LazyLoadSession
from compas_viewer.viewer import Viewer

HERE = pathlib.Path(__file__).parent

session = LazyLoadSession(name="RV", basedir=HERE)

# =============================================================================
# Session data
# =============================================================================

trimesh: Mesh = session["trimesh"]

# =============================================================================
# Pattern mapping
# =============================================================================

pattern = map_pattern_to_mesh(
    name="ZigZag",
    mesh=trimesh,
    tolerance=1e-3,
    clip_boundaries=True,
    pattern_u=16,
    pattern_v=16,
)

# =============================================================================
# Export
# =============================================================================

session["pattern"] = pattern
session.dump()

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

viewer.scene.add(pattern, name="Pattern")

viewer.show()
