from compas_viewer import Viewer
from compas_viewer.components import Treeform
from compas_occ.brep import Brep
from compas.datastructures import Mesh
# from compas.colors import Color
from compas.tolerance import TOL
from compas.geometry import Transformation
import json

TOL.lineardeflection = 100

hierarchy = {}

def create_hierarchy(scene, layer, file_group = None):
    # Split the layer path into individual layer names
    layers = layer.split("::")
    
    # Start from the root of the hierarchy
    current_group = scene
    if file_group:
        current_path = file_group.name + "::"
    else:
        current_path = ""
    
    # Traverse through each layer in the path
    for i, layer_name in enumerate(layers):
        # Build the current path
        current_path = f"{current_path}::{layer_name}" if current_path else layer_name
        
        # Check if this path already exists in the hierarchy
        if current_path not in hierarchy:
            # For top layer, parent should be None
            parent = file_group if i == 0 else current_group
            # Create new group and store it in hierarchy
            hierarchy[current_path] = scene.add_group(name=layer_name, parent=parent)
        
        # Move to the next level in the hierarchy
        current_group = hierarchy[current_path]
    
    return current_group



def add_file(scene, name):

    index = json.load(open(f"temp/ZHA/{name}.json"))

    file_group = scene.add_group(name=name)
    loaded_blocks = {}

    for guid, info in index.items():

        print(guid, info)
        obj = None

        if info["type"] == "Brep":
            brep = Brep.from_step(f"temp/ZHA/step_exports/{guid}.step")
            brep.scale(0.001) # OCC auto converts to mm, we want m
            layer_group = create_hierarchy(scene, info["layer"], file_group)
            if brep.is_solid:
                obj = scene.add(brep, name=info["name"], parent=layer_group)
    
        if info["type"] == "Mesh":
            mesh = Mesh.from_obj(f"temp/ZHA/step_exports/{guid}.obj")
            layer_group = create_hierarchy(scene, info["layer"], file_group)
            scene.add(mesh, name=info["name"], parent=layer_group)

        if info["type"] == "InstanceReferenceGeometry":
            layer_group = create_hierarchy(scene, info["layer"], file_group)
            block_id = info["block_id"]
            if block_id not in loaded_blocks:
                brep = Brep.from_step(f"temp/ZHA/step_exports/{block_id}.step")
                brep.scale(0.001) # OCC auto converts to mm, we want m
                loaded_blocks[block_id] = brep
            else:
                brep = loaded_blocks[block_id]
            

            obj = scene.add(brep, name=info["name"], parent=layer_group)
            obj.transformation = Transformation(matrix=info["transform"])
        
        if obj:
            obj.attributes["info"] = info


viewer = Viewer()

add_file(viewer.scene, "blocks")
add_file(viewer.scene, "supports")
add_file(viewer.scene, "waffle")
add_file(viewer.scene, "foundations")

treeform = Treeform()
viewer.ui.sidebar.widget.addWidget(treeform)

def update_treeform(form, obj):
    info = obj.attributes["info"]
    treeform.update_from_dict({"Info": info})

viewer.ui.sidebar.sceneform.callback = update_treeform

viewer.show()