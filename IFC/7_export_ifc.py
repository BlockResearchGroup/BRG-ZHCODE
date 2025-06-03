from compas_occ.brep import Brep
from compas.datastructures import Mesh
from compas.geometry import Transformation
from compas.geometry import Frame
import json
from compas_ifc.model import Model


mapping = {

    # Blocks
    "Blocks": "IfcBuildingElementPart",

    # Waffle
    "waffle_addition": "IfcMember",
    "waffle_modules": "IfcMember",

    # Supports
    "tension_ties": "IfcPlate",
    "splice_plates": "IfcPlate",
    "Plates": "IfcPlate",
    "bolts": "IfcMechanicalFastener",
    "anchor_bolts": "IfcMechanicalFastener",

    # Foundations
    "Concrete_pad": "IfcFooting",
    "grout": "IfcBuildingElementPart",
    "_UPDATE_concrete_pads": "IfcElementAssembly",

}


def get_cls(info):
    """Get the the IFC class for a given layer name, using the mapping dictionary."""
    layers = info["layer"].split("::")
    for layer_name, cls in mapping.items():
        if layer_name in layers:
            return cls



def add_elements(model: Model, name, parent):

    metadata = json.load(open(f"IFC/data/{name}.json"))

    loaded_blocks = {}

    for guid, info in metadata.items():

        print(guid, info)

        if info["type"] == "Brep":
            brep = Brep.from_step(f"IFC/data/exports/{guid}.step")
            brep.scale(0.001) # OCC auto converts to mm, we want m
            if brep.is_solid:
                model.create(cls=get_cls(info), geometry=brep, name=info["name"], parent=parent)
    
        if info["type"] == "Mesh":
            mesh = Mesh.from_obj(f"IFC/data/exports/{guid}.obj")
            model.create(cls=get_cls(info), geometry=mesh, name=info["name"], parent=parent)

        if info["type"] == "InstanceReferenceGeometry":
            block_name = info["block_name"]
            if block_name not in loaded_blocks:
                brep = Brep.from_step(f"IFC/data/exports/{block_name}.step")
                brep.scale(0.001) # OCC auto converts to mm, we want m
                
                # We need to first apply the scale component of the transformation to the brep
                # Because of this we don't need to set a large linear deflection anymore, since the instance block is already scaled
                transformation = Transformation(info["transform"])
                scale = transformation.scale 
                brep.transform(scale)

                # store the loaded block brep for reuse
                loaded_blocks[block_name] = brep
            else:
                brep = loaded_blocks[block_name]

            # We then assign a frame for the IFC element (translation and rotation of the transformation)
            frame = Frame.from_matrix(info["transform"]) 
            model.create(cls=get_cls(info), geometry=brep, name=info["name"], parent=parent, frame=frame)

# Create the template model
model = Model.template(unit="m", use_occ=False)


# Create some parent elements
slab = model.create(cls="IfcSlab", name="Bridge", parent=model.building_storeys[0])
scaffold = model.create(cls="IfcElementAssembly", name="Scaffold", parent=model.building_storeys[0])
support = model.create(cls="IfcElementAssembly", name="Support", parent=model.building_storeys[0])

# Add the elements to the model
add_elements(model, "blocks", slab)
add_elements(model, "supports", support)
add_elements(model, "waffle", scaffold)
add_elements(model, "foundations", model.building_storeys[0])

# Save the model
model.save("IFC/data/striatus.ifc")

# Reload and view the model
# model = Model("IFC/data/striatus.ifc")
# model.show()