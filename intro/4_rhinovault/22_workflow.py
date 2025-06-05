import pathlib

from compas.datastructures import Mesh
from compas_session.lazyload import LazyLoadSession
from compas_viewer.viewer import Viewer

HERE = pathlib.Path(__file__).parent

session = LazyLoadSession(name="RV", basedir=HERE)

# =============================================================================
# Session data
# =============================================================================

basemesh: Mesh = session["basemesh"]

# =============================================================================
# Export
# =============================================================================

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

viewer.scene.add(basemesh, name="BaseMesh")

viewer.show()
