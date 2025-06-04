from compas.geometry import Box
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Sphere
from compas_gmsh.models import MeshModel
from compas_viewer.viewer import Viewer

R = 1.4

box = Box(2 * R).to_brep()
sphere = Sphere(radius=1.25 * R).to_brep()  # type: ignore

cylx = Cylinder(radius=0.7 * R, height=3 * R, frame=Frame.worldYZ()).to_brep()
cyly = Cylinder(radius=0.7 * R, height=3 * R, frame=Frame.worldZX()).to_brep()
cylz = Cylinder(radius=0.7 * R, height=3 * R, frame=Frame.worldXY()).to_brep()

brep = box & sphere
brep = brep - cylz
brep = brep - cylx
brep = brep - cyly

brep.to_step("brep.stp")

model = MeshModel.from_step("brep.stp")
model.options.mesh.meshsize_max = 0.1
model.generate_mesh()

mesh = model.mesh_to_compas()

viewer = Viewer()
viewer.scene.add(mesh)
viewer.show()
