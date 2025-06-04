from compas_ifc.model import Model


model = Model("IFC/data/striatus_built.ifc")

# Check the Pset of a block
block = model.get_entity_by_global_id("0ufU4VYEr7QA$Yt$0FZofy")
block.print_properties(max_depth=4)

# Validate the Pset of the block
block.validate_properties({"Pset_ConcreteRecipe": "IFC/data/recipe_schema.json"})
