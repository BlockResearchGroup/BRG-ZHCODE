import compas
from compas.colors import Color
from compas.datastructures import CellNetwork
from compas_viewer.viewer import Viewer

network: CellNetwork = CellNetwork.from_json(compas.get("cellnetwork_example.json"))  # type: ignore

cells = []
for cell in network.cells():
    cellfaces = []
    for face in network.cell_faces(cell):
        polygon = network.face_polygon(face)
        cellfaces.append(polygon)
    cells.append(cellfaces)

faces = []
for face in network.faces_without_cell():
    polygon = network.face_polygon(face)
    faces.append(polygon)

edges = []
for edge in network.edges_without_face():
    line = network.edge_line(edge)
    edges.append(line)

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()

cellgroup = viewer.scene.add_group(name="Cells")
for polygons in cells:
    polygroup = viewer.scene.add_group(name="Faces", parent=cellgroup)
    polygroup.add_from_list(polygons, opacity=0.5)  # type: ignore

facegroup = viewer.scene.add_group(name="Faces w/o Cells")
facegroup.add_from_list(faces, opacity=0.5, surfacecolor=Color.cyan())  # type: ignore

edgegroup = viewer.scene.add_group(name="Edges w/o Faces")
edgegroup.add_from_list(edges)

viewer.show()
