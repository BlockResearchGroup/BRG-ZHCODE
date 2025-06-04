import rhinoscriptsyntax as rs
import scriptcontext as sc
import os
import json


# Get all objects in the document
objects = rs.GetObjects("Select objects to export (press Enter for all objects)", preselect=True)

if not objects:
    # If no objects are selected, get all objects in the document
    objects = rs.AllObjects()


def export_object(obj, filepath):
    # Select given object
    rs.UnselectAllObjects()
    rs.SelectObject(obj)

    # Export using rs command
    command = f'_-Export "{filepath}" _Enter'
    rs.Command(command)

def export_block(block_name, filepath):
    rs.UnselectAllObjects()
    copied_objs = []

    for block_obj_id in rs.BlockObjects(block_name):
        block_obj = sc.doc.Objects.Find(block_obj_id)
        block_obj_type = block_obj.Geometry.GetType().Name

        if block_obj_type == "Brep" or block_obj_type == "Extrusion":
            copied_obj = rs.CopyObject(block_obj)
            copied_objs.append(copied_obj)
            rs.SelectObject(copied_obj)
        else:
            print(f"Skipping {block_obj_type}")

    filepath = os.path.join(EXPORT_DIR, f"{block_name}.step")
    command = f'_-Export "{filepath}" _Enter'
    rs.Command(command)
    rs.DeleteObjects(copied_objs)

# Create export directory in the same location as the script
HERE = os.path.dirname(os.path.abspath(__file__))
EXPORT_DIR = os.path.join(HERE, "data/exports")

# Create the export directory if it doesn't exist
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

# Dictionary to store object information
metadata = {}

# Set to track exported unique blocks
exported_blocks = set()

for obj_guid in objects:
    # Get the object
    obj = sc.doc.Objects.Find(obj_guid)

    # Get the object name
    name = rs.ObjectName(obj_guid)

    # Get object type
    type_name = obj.Geometry.GetType().Name

    # Get layer information
    layer = rs.ObjectLayer(obj_guid)


    # Determine file format based on object type
    if type_name == "Mesh":
        # Export Mesh as OBJ
        export_format = "obj"
        filename = f"{obj_guid}.{export_format}"
        filepath = os.path.join(EXPORT_DIR, filename)
        export_object(obj, filepath)

        metadata[str(obj_guid)] = {
            "layer": layer,
            "type": type_name,
            "name": name,
            "format": export_format
        }
        
    elif type_name == "Brep" or type_name == "Extrusion":
        # Export Brep or Extrusion as STEP
        export_format = "step"
        filename = f"{obj_guid}.{export_format}"
        filepath = os.path.join(EXPORT_DIR, filename)
        export_object(obj, filepath)

        metadata[str(obj_guid)] = {
            "layer": layer,
            "type": type_name,
            "name": name,
            "format": export_format
        }

    elif type_name == "InstanceReferenceGeometry":
        # Export InstanceReferenceGeometry as STEP but only the unique blocks

        # Get the transformation matrix of the instance
        transform = obj.Geometry.Xform

        # Convert transformation matrix to 2D array
        transform_array = [
            [transform.M00, transform.M01, transform.M02, transform.M03],
            [transform.M10, transform.M11, transform.M12, transform.M13],
            [transform.M20, transform.M21, transform.M22, transform.M23],
            [transform.M30, transform.M31, transform.M32, transform.M33]
        ]


        # Get the block name (unique)
        block_name = rs.BlockInstanceName(obj_guid)

        # Export the block if it hasn't been exported yet
        if block_name not in exported_blocks:
            export_block(block_name, EXPORT_DIR)
            exported_blocks.add(block_name)

        # Store instance reference information
        metadata[str(obj_guid)] = {
            "layer": layer,
            "type": type_name,
            "name": name,
            "transform": transform_array,
            "block_name": block_name,
            "format": "step"
        }

    else:
        print(f"Skipping {name} ({type_name})")
        continue


# Save the metadata to a JSON file
json_path = os.path.join(HERE, "data/waffle.json")
with open(json_path, "w") as f:
    json.dump(metadata, f, indent=4)

print(f"\nExport completed. Files saved in: {EXPORT_DIR}")
print(f"Metadata saved as: {json_path}")
