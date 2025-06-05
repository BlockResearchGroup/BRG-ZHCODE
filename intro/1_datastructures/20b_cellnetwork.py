import compas
from compas.colors import Color
from compas.datastructures import CellNetwork
from compas_viewer.viewer import Viewer

network: CellNetwork = CellNetwork.from_json(compas.get("cellnetwork_example.json"))  # type: ignore

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

viewer.show()
