from compas_ifc.model import Model

model = Model("IFC/data/Duplex_A_20110907.ifc")


# Print the total number of entities in the model
entities = list(model.entities)
print("Total number of entities: ", len(entities))

# Print the last 5 entities in the model
for entity in entities[-5:]:
    print(entity)

# Get entities by the IFC class name
ifc_windows = model.get_entities_by_type("IfcWindow")
print("\nTotal number of windows: ", len(ifc_windows))
for entity in ifc_windows:
    print(entity)

# Get entities by the element name
name = "M_Fixed:4835mm x 2420mm:4835mm x 2420mm:145788"
entities = model.get_entities_by_name(name)
print("\nFound entities with the name: {}".format(name))
print(entities)

# Get entity by the global id
global_id = "1hOSvn6df7F8_7GcBWlR72"
entity = model.get_entity_by_global_id(global_id)
print("\nFound entity with the global id: {}".format(global_id))
print(entity)

# Get entity by the id (index in the IFC file)
entity = model.get_entity_by_id(6426)
print("\nFound entity with the id: {}".format(id))
print(entity)
