import compas
from compas.datastructures import Mesh
from compas.utilities import print_profile
from compas_cgal.meshing import mesh_remesh
from compas_viewer.viewer import Viewer

mesh_from_ply = print_profile(Mesh.from_ply)

mesh = mesh_from_ply(compas.get("bunny.ply"))
mesh.scale(30)
mesh.rotate(0.5 * 3.14159, [1, 0, 0])

box = mesh.aabb()
vector = box.points[0] * -1

mesh.translate(vector)
box.translate(vector)


@print_profile
def remesh(mesh):
    average = (
        sum(mesh.edge_length(edge) for edge in mesh.edges()) / mesh.number_of_edges()
    )
    target = 3 * average
    V, F = mesh_remesh(mesh.to_vertices_and_faces(), target)
    return Mesh.from_vertices_and_faces(V, F)


mesh = remesh(mesh)

viewer = Viewer()
viewer.scene.add(mesh)
viewer.scene.add(box, show_faces=False, show_lines=True)
viewer.show()
