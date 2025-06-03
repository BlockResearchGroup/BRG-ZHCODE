from compas_viewer import Viewer
from compas_viewer.components import Treeform
from compas_occ.brep import Brep
from compas.datastructures import Mesh
# from compas.colors import Color
from compas.tolerance import TOL
from compas.geometry import Transformation
from compas.geometry import Frame
import json
from compas_ifc.model import Model



def add_elements(model: Model, name):

    index = json.load(open(f"temp/ZHA/{name}.json"))

    # file_group = scene.add_group(name=name)
    loaded_blocks = {}

    for guid, info in index.items():

        print(guid, info)
        obj = None

        if info["type"] == "Brep":
            brep = Brep.from_step(f"temp/ZHA/step_exports/{guid}.step")
            brep.scale(0.001) # OCC auto converts to mm, we want m
            # layer_group = create_hierarchy(scene, info["layer"], file_group)
            if brep.is_solid:
                obj = model.create(geometry=brep, name=info["name"], parent=model.building_storeys[0])
    
        if info["type"] == "Mesh":
            mesh = Mesh.from_obj(f"temp/ZHA/step_exports/{guid}.obj")
            # layer_group = create_hierarchy(scene, info["layer"], file_group)
            model.create(geometry=mesh, name=info["name"], parent=model.building_storeys[0])

        if info["type"] == "InstanceReferenceGeometry":
            block_id = info["block_id"]
            if block_id not in loaded_blocks:
                brep = Brep.from_step(f"temp/ZHA/step_exports/{block_id}.step")
                brep.scale(0.001) # OCC auto converts to mm, we want m
                transformation = Transformation(info["transform"])
                scale = transformation.scale # We apply the scale component of the transformation to the brep
                brep.transform(scale)
                loaded_blocks[block_id] = brep
            else:
                brep = loaded_blocks[block_id]

            frame = Frame.from_matrix(info["transform"]) # We apply the rotation and translation components of the transformation to the frame
            obj = model.create(geometry=brep, name=info["name"], parent=model.building_storeys[0], frame=frame)
        
        if obj:
            obj.attributes["info"] = info


model = Model.template(unit="m", use_occ=True)

TOL.lineardeflection = 1000


# add_elements(model, "blocks")
# add_elements(model, "supports")
add_elements(model, "waffle")
# add_elements(model, "foundations")

# model.print_spatial_hierarchy()
model.save("temp/ZHA/ifc_export_brep.ifc")
# model.show()
