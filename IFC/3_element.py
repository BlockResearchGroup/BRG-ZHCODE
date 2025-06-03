from compas_ifc.model import Model

model = Model("IFC/data/Duplex_A_20110907.ifc")

window = model.get_entities_by_type("IfcWindow")[0]
print(window)

# print the attributes of the window
print(window.attributes)
window.print_attributes(max_depth=2)

# print the property sets of the window
print(window.property_sets)
window.print_properties(max_depth=2)

# visualize the window in the viewer
window.show()
