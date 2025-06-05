import pathlib

import compas
from compas.datastructures import Mesh
from compas.scene import MeshObject
from compas.scene import Scene
from compas_session.lazyload import LazyLoadSession
from compas_viewer.viewer import Viewer

HERE = pathlib.Path(__file__).parent

session = LazyLoadSession(name="RV", basedir=HERE)

# =============================================================================
# RhinoVAULT data
# =============================================================================

HERE = pathlib.Path(__file__).parent
DATA = HERE.parent.parent / "data"
FILE = DATA / "RhinoVAULT.json"
rhinovault = compas.json_load(FILE)

scene: Scene = rhinovault["scene"]
sceneobj: MeshObject = scene.find_by_name("ThrustDiagram")  # type: ignore
mesh: Mesh = sceneobj.mesh

for face in list(mesh.faces_where(_is_loaded=False)):
    mesh.delete_face(face)

# =============================================================================
# Export
# =============================================================================

session["basemesh"] = mesh
session.dump()

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

viewer.scene.add(mesh, name="TriMesh")

viewer.show()
