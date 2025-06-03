from compas_occ.brep import Brep
from compas.datastructures import Mesh
from compas.tolerance import TOL
from compas.geometry import Transformation
from compas.geometry import Frame
import json
from compas_ifc.model import Model



def add_elements(model: Model, name, parent, get_cls=None):

    index = json.load(open(f"IFC/data/{name}.json"))

    loaded_blocks = {}

    for guid, info in index.items():

        print(guid, info)
        obj = None

        if info["type"] == "Brep":
            brep = Brep.from_step(f"IFC/data/exports/{guid}.step")
            brep.scale(0.001) # OCC auto converts to mm, we want m
            if brep.is_solid:
                obj = model.create(cls=get_cls(info), geometry=brep, name=info["name"], parent=parent)
    
        if info["type"] == "Mesh":
            mesh = Mesh.from_obj(f"IFC/data/exports/{guid}.obj")
            model.create(cls=get_cls(info), geometry=mesh, name=info["name"], parent=parent)

        if info["type"] == "InstanceReferenceGeometry":
            block_name = info["block_name"]
            if block_name not in loaded_blocks:
                brep = Brep.from_step(f"IFC/data/exports/{block_name}.step")
                brep.scale(0.001) # OCC auto converts to mm, we want m
                transformation = Transformation(info["transform"])
                scale = transformation.scale # We apply the scale component of the transformation to the brep
                brep.transform(scale)
                loaded_blocks[block_name] = brep
            else:
                brep = loaded_blocks[block_name]

            frame = Frame.from_matrix(info["transform"]) # We apply the rotation and translation components of the transformation to the frame
            obj = model.create(cls=get_cls(info), geometry=brep, name=info["name"], parent=parent, frame=frame)
        
        if obj:
            obj.attributes["info"] = info


model = Model.template(unit="m", use_occ=False)

TOL.lineardeflection = 1000

slab = model.create(cls="IfcSlab", name="Bridge", parent=model.building_storeys[0])
scaffold = model.create(cls="IfcElementAssembly", name="Scaffold", parent=model.building_storeys[0])
support = model.create(cls="IfcElementAssembly", name="Support", parent=model.building_storeys[0])


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

    layers = info["layer"].split("::")
    for layer_name, cls in mapping.items():
        if layer_name in layers:
            return cls

    return "IfcBuildingElementProxy"


add_elements(model, "blocks", slab, get_cls=get_cls)
add_elements(model, "supports", support, get_cls=get_cls)
add_elements(model, "waffle", scaffold, get_cls=get_cls)
add_elements(model, "foundations", model.building_storeys[0], get_cls=get_cls)


model.save("IFC/data/striatus.ifc")

# model = Model("IFC/data/striatus.ifc")
# model.show()