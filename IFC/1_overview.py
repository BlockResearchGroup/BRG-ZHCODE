from compas_ifc.model import Model

# Load an IFC file
model = Model("IFC/data/Duplex_A_20110907.ifc")

# Print a summary of the model
model.print_summary()

# Print the spatial hierarchy of the model
model.print_spatial_hierarchy()

# Visualize the model
model.show()
