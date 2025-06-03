import rhinoscriptsyntax as rs
import os
import scriptcontext as sc
import json



def export_objects_to_step():
    # Get all objects in the document
    # objects = rs.GetObjects("Select objects to analyze (press Enter for all objects)", preselect=True)
    
    # if not objects:
    #     # If no objects are selected, get all objects in the document
    objects = rs.AllObjects()

    # Create export directory in the same location as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    export_dir = os.path.join(script_dir, "data/exports")
    
    # Create the export directory if it doesn't exist
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # Dictionary to store object information
    object_info = {}
    # Set to track exported parent objects
    exported_blocks = {}
    
    print("\nExporting objects:")
    print("-" * 50)

    for obj in objects:
        # Get object name first (in case we need it for error handling)
        name = rs.ObjectName(obj)
        if not name:
            name = "Unnamed"
        
        # Get object type
        obj_type = rs.ObjectType(obj)
        type_name = sc.doc.Objects.Find(obj).Geometry.GetType().Name
        
        # Get layer information
        layer = rs.ObjectLayer(obj)
        
        # Generate a unique filename using the object's ID
        guid = str(obj)  # The object's ID is already a unique identifier
        
        # Handle instance references
        if type_name == "InstanceReferenceGeometry":
            # Get the instance reference geometry
            instance_ref = sc.doc.Objects.Find(obj).Geometry
            
            # Get the transformation matrix
            transform = instance_ref.Xform

            block_name = rs.BlockInstanceName(obj)

            # Convert transformation matrix to 2D array
            transform_array = [
                [transform.M00, transform.M01, transform.M02, transform.M03],
                [transform.M10, transform.M11, transform.M12, transform.M13],
                [transform.M20, transform.M21, transform.M22, transform.M23],
                [transform.M30, transform.M31, transform.M32, transform.M33]
            ]

            block_id = exported_blocks.get(block_name, None)

            if not block_id:

                rs.UnselectAllObjects()

                copied_objs = []

                block_obj_ids = rs.BlockObjects(block_name)
                for block_obj_id in block_obj_ids:
                    block_obj = sc.doc.Objects.Find(block_obj_id)
                    block_obj_type = block_obj.Geometry.GetType().Name

                    if block_obj_type == "Brep" or block_obj_type == "Extrusion":
                        copied_obj = rs.CopyObject(block_obj)
                        copied_objs.append(copied_obj)
                        rs.SelectObject(copied_obj)


                

                block_id = str(copied_objs[0])
                filepath = os.path.join(export_dir, f"{block_id}.step")
                command = f'_-Export "{filepath}" _Enter'
                rs.Command(command)

                rs.DeleteObjects(copied_objs)
                exported_blocks[block_name] = block_id


            # Store instance reference information
            object_info[guid] = {
                "layer": layer,
                "type": type_name,
                "name": name,
                "transform": transform_array,
                "block_name": block_name,
                "block_id": block_id,
                "format": "step"
            }

            continue


        # Determine file format based on object type
        if type_name == "Mesh":
            filename = f"{guid}.obj"
            export_format = "obj"
        elif type_name == "Brep" or type_name == "Extrusion":
            filename = f"{guid}.step"
            export_format = "step"
        else:
            print(f"Skipping {name} ({type_name})")
            continue
            
        filepath = os.path.join(export_dir, filename)
        
        # Store object information in dictionary
        object_info[guid] = {
            "layer": layer,
            "type": type_name,
            "name": name,
            "format": export_format
        }
        
        # Select only the current object
        rs.UnselectAllObjects()
        rs.SelectObject(obj)
        
        # Export using command line
        command = f'_-Export "{filepath}" _Enter'
        rs.Command(command)
        
        print(f"Exported: {name}")
        print(f"Type: {type_name}")
        print(f"Format: {export_format}")
        print(f"Layer: {layer}")
        print(f"File: {filename}")
        print("-" * 50)
                
   
    
    # Save the object information to a JSON file
    json_path = os.path.join(script_dir, "data/waffle.json")
    with open(json_path, 'w') as f:
        json.dump(object_info, f, indent=4)
    
    print(f"\nExport completed. Files saved in: {export_dir}")
    print(f"Index file saved as: {json_path}")

if __name__ == "__main__":
    export_objects_to_step()
