from compas_viewer import Viewer
from compas_viewer.components import Treeform
from compas_occ.brep import Brep
from compas.datastructures import Mesh
from compas.tolerance import TOL
from compas.geometry import Transformation
import json

TOL.lineardeflection = 1000

created_groups = {}


def create_layer_group(scene, full_layer_path, file_group):
    """Create groups for each layer in a tree structure without duplicates."""

    # Split the layer path into individual layer names
    # Example: "Level1::Wall::Exterior" becomes ["Level1", "Wall", "Exterior"]
    layers = full_layer_path.split("::")

    # Start from the root of the hierarchy
    parent = file_group
    full_path = file_group.name

    # Traverse through each layer in the path
    for layer_name in layers:
        full_path += f"::{layer_name}"

        # Check if this layer has already been created as a group
        if full_path not in created_groups:
            # Create new group and store it
            created_groups[full_path] = scene.add_group(name=layer_name, parent=parent)

        # Move to the next level in the hierarchy
        parent = created_groups[full_path]

    # Return the last created group (the last layer in the path)
    return parent


def add_file(scene, name):

    metadata = json.load(open(f"IFC/data/{name}.json"))

    # Make a top level group for this file
    file_group = scene.add_group(name=name)

    # Store loaded blocks to avoid loading the same file multiple times
    loaded_blocks = {}

    for guid, info in metadata.items():

        print(f"Processing {guid} ({info['type']})")
        obj = None

        if info["type"] == "Brep":
            brep = Brep.from_step(f"IFC/data/exports/{guid}.step")
            brep.scale(0.001)  # OCC auto converts to mm, we want m
            layer_group = create_layer_group(scene, info["layer"], file_group)
            if brep.is_solid:
                obj = scene.add(brep, name=info["name"], parent=layer_group)

        if info["type"] == "Mesh":
            mesh = Mesh.from_obj(f"IFC/data/exports/{guid}.obj")
            layer_group = create_layer_group(scene, info["layer"], file_group)
            scene.add(mesh, name=info["name"], parent=layer_group)

        if info["type"] == "InstanceReferenceGeometry":
            layer_group = create_layer_group(scene, info["layer"], file_group)
            block_name = info["block_name"]
            if block_name not in loaded_blocks:
                brep = Brep.from_step(f"IFC/data/exports/{block_name}.step")
                brep.scale(0.001)  # OCC auto converts to mm, we want m
                loaded_blocks[block_name] = brep
            else:
                brep = loaded_blocks[block_name]

            obj = scene.add(brep, name=info["name"], parent=layer_group)
            obj.transformation = Transformation(matrix=info["transform"])

        if obj:
            obj.attributes["info"] = info


viewer = Viewer()

# Add the previously exported files to the viewer
add_file(viewer.scene, "blocks")
add_file(viewer.scene, "supports")
add_file(viewer.scene, "waffle")
add_file(viewer.scene, "foundations")

# Some UI tweaks
# Show the object info in the sidebar
treeform = Treeform()
viewer.ui.sidebar.widget.addWidget(treeform)


def update_treeform(form, obj):
    info = obj.attributes.get("info", {})
    treeform.update_from_dict({"Info": info})


viewer.ui.sidebar.sceneform.callback = update_treeform

viewer.show()
