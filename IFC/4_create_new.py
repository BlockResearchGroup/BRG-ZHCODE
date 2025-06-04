import compas
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Sphere
from compas.geometry import Frame
from compas_ifc.model import Model

# Create a new model using the template method
model = Model.template(storey_count=1, unit="m")

# Create some compas geometries
box = Box.from_width_height_depth(5, 5, 0.05)
sphere = Sphere(2)
mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

# The parent of the elements is the first storey
storey = model.building_storeys[0]

# Create the elements
element1 = model.create_wall(geometry=box, frame=Frame([0, 0, 0]), name="My Wall", parent=storey)
element2 = model.create_roof(geometry=mesh, frame=Frame([0, 0, 5]), name="My Roof", parent=storey)
element3 = model.create(geometry=sphere, frame=Frame([0, 5, 0]), name="Sphere", parent=storey, properties={"Custom_Pset": {"Custom_Property": "Custom Value"}})

# Print the spatial hierarchy of the model
model.print_spatial_hierarchy(max_depth=5)

# Show the model in the viewer
model.show()

# Save the model to a file
model.save("IFC/data/test.ifc")
