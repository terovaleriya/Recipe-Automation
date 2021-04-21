import asyncio
import logging
from typing import Optional

import asyncpg

from core import schema, model

# Links
from core.model import db

logging.basicConfig(filename="db_load.log", level=logging.WARNING)


def get_field(table: model) -> str:
    field = ""
    if table == model.RecipesIngredients:
        field = "ingredient"
    elif table == model.RecipesInstructions:
        field = "instruction"
    elif table == model.RecipesNutrition:
        field = "nutrition"
    elif table == model.RecipesPlanning:
        field = "planning"
    elif table == model.RecipesImages:
        field = "image"
    elif table == model.RecipesTags:
        field = "tag"
    return field


async def create_link(table: model, recipe_id: int, id: int) -> int:
    field = get_field(table)
    obj_data = {
        "recipe": recipe_id,
        field: id
    }
    link = await table.create(**obj_data)
    return link.id


# PRODUCT

# OK
async def retrieve_product_by_id(product_id: int) -> Optional[schema.Product]:
    obj = await model.Products.get(product_id)
    return obj.as_schema() if obj else None


# OK
async def delete_product_by_id(product_id: int) -> None:
    await model.Products.delete.where(model.Products.id == product_id).gino.status()


# OK
async def create_product(name: str, size: str = None, image_url: str = None) -> int:
    products = model.Products
    try:
        obj_data = {
            "name": name,
            "size": size,
            "image_url": image_url
        }
        product = await products.create(**obj_data)
        return product.id

    except asyncpg.exceptions.UniqueViolationError:
        logging.info(
            "Product with [name '%s', size '%s', image_url '%s'] already exists", name, str(size), str(image_url))
        return await get_product_id_by_parameters(name, size, image_url)


# OK
async def update_product_by_id(product_id: int, name: str = None, size: str = None, image_url: str = None) -> None:
    products = model.Products

    try:
        obj = await products.get(product_id)
        name = name if (name is not None) else obj.name
        size = size if (size is not None) else obj.size
        image_url = image_url if (image_url is not None) else obj.image_url
        obj_data = {
            "name": name,
            "size": size,
            "image_url": image_url
        }
        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Product with id %s doesn't exist", str(product_id))


# OK
async def get_product_id_by_parameters(name: str, size: str = None, image_url: str = None) -> int:
    products = model.Products
    return await products.query.where(products.name == name).where(products.size == size).where(
        products.image_url == image_url).gino.scalar()


# RECIPE

# OK
async def retrieve_recipe_by_id(recipe_id: int) -> Optional[schema.Recipe]:
    obj = await model.Recipes.get(recipe_id)
    return obj.as_schema() if obj else None


# OK
async def delete_recipe_by_id(recipe_id: int) -> None:
    await model.Recipes.delete.where(model.Recipes.id == recipe_id).gino.status()


# OK
# (пытается создать, если удалось -- вернет новый id,
# а если такой уже есть, вернет id уже существующего)
async def create_recipe_by_title(title: str) -> int:
    recipes = model.Recipes
    try:
        obj_data = {
            "title": title
        }
        _recipe = await recipes.create(**obj_data)
        logging.info("RECIPE CREATED")
        return _recipe.id
    except asyncpg.exceptions.UniqueViolationError:
        logging.info("Recipe with title '%s' already exists", title)
        id = await get_recipe_id_by_title(title)
        return id


# OK
async def update_recipe_by_id(recipe_id: int, title: str = None) -> None:
    recipes = model.Recipes
    try:
        obj = await recipes.get(recipe_id)
        title = title if (title is not None) else obj.title
        obj_data = {
            "title": title
        }
        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Recipe with id %s doesn't exist", str(recipe_id))


# OK
async def get_recipe_id_by_title(title: str) -> int:
    recipes = model.Recipes
    id = await recipes.query.where(recipes.title == title).gino.scalar()
    return id


# INGREDIENT

# OK
async def retrieve_ingredient_by_id(ingredient_id: int) -> Optional[schema.Ingredient]:
    obj = await model.Ingredients.get(ingredient_id)
    return obj.as_schema() if obj else None


# OK
async def delete_ingredient_by_id(ingredient_id: int) -> None:
    await model.Ingredients.delete.where(model.Ingredients.id == ingredient_id).gino.status()


# OK
async def create_ingredient_by_raw_string(raw_string: str, name: str = None, quantity: str = None,
                                          comment: str = None) -> int:
    ingredients = model.Ingredients
    try:
        obj_data = {
            "name": name,
            "quantity": quantity,
            "comment": comment,
            "raw_string": raw_string
        }
        _ingredient = await ingredients.create(**obj_data)
        logging.info("INGREDIENT CREATED")
        return _ingredient.id
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_ingredient_id_by_raw_string(raw_string)
        logging.info("Ingredient with raw string '%s' already exists", raw_string)
        return id


# OK
async def update_ingredient_by_id(ingredient_id: int, raw_string: str = None, name: str = None, quantity: str = None,
                                  comment: str = None) -> None:
    ingredients = model.Ingredients

    try:
        obj = await ingredients.get(ingredient_id)
        raw_string = raw_string if (raw_string is not None) else obj.raw_string
        name = name if (name is not None) else obj.name
        quantity = quantity if (quantity is not None) else obj.quantity
        comment = comment if (comment is not None) else obj.comment
        obj_data = {
            "name": name,
            "quantity": quantity,
            "comment": comment,
            "raw_string": raw_string
        }
        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Ingredient with id %s doesn't exist", str(ingredient_id))


# OK
async def get_ingredient_id_by_raw_string(raw_string: str) -> int:
    ingredients = model.Ingredients
    id = await ingredients.query.where(ingredients.raw_string == raw_string).gino.scalar()
    return id


# TAG

# OK
async def retrieve_tag_by_id(tag_id: int) -> Optional[schema.Tag]:
    obj = await model.Tags.get(tag_id)
    return obj.as_schema() if obj else None


# OK
async def delete_tag_by_id(tag_id: int) -> None:
    await model.Tags.delete.where(model.Tags.id == tag_id).gino.status()


# OK
async def create_tag_by_tag(tag: str) -> int:
    tags = model.Tags
    id = await get_tag_id_by_tag(tag)
    try:
        obj_data = {
            "tag": tag
        }
        _tag = await tags.create(**obj_data)
        return _tag.id

    except asyncpg.exceptions.UniqueViolationError:
        logging.info("Tag with name '%s' already exists", tag)
        return id


# OK
async def update_tag_by_id(tag_id: int, tag: str = None) -> None:
    tags = model.Tags
    try:
        obj = await tags.get(tag_id)
        tag = tag if (tag is not None) else obj.tag
        obj_data = {
            "tag": tag
        }
        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Tag with id %s doesn't exist", str(tag_id))


# OK
async def get_tag_id_by_tag(tag: str) -> int:
    tags = model.Tags
    id = await tags.query.where(tags.tag == tag).gino.scalar()
    return id


# IMAGE URL

# OK
async def retrieve_image_by_id(image_id: int) -> Optional[schema.Image]:
    obj = await model.Images.get(image_id)
    return obj.as_schema() if obj else None


# OK
async def delete_image_by_id(image_id: int) -> None:
    await model.Images.delete.where(model.Images.id == image_id).gino.status()


# OK
async def create_image_by_image_url(image_url: str) -> int:
    images = model.Images
    try:
        obj_data = {
            "image": image_url
        }
        _image = await images.create(**obj_data)
        return _image.id
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_image_id_by_image_url(image_url)
        logging.info("Image with image URL '%s' already exists", image_url)
        return id


# OK
async def update_image_by_id(image_id: int, image_url: str = None) -> None:
    images = model.Images
    try:
        obj = await images.get(image_id)
        image_url = image_url if (image_url is not None) else obj.image
        obj_data = {
            "image": image_url
        }
        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Image with id %s doesn't exist", str(image_id))


# OK
async def get_image_id_by_image_url(image_url: str) -> int:
    images = model.Images
    id = await images.query.where(images.image == image_url).gino.scalar()
    return id


# INSTRUCTIONS

# OK
async def retrieve_instruction_by_id(instruction_id: int) -> Optional[schema.Instruction]:
    obj = await model.Instructions.get(instruction_id)
    return obj.as_schema() if obj else None


# OK
async def delete_instruction_by_id(instruction_id: int) -> None:
    await model.Instructions.delete.where(model.Instructions.id == instruction_id).gino.status()


# OK
async def create_instruction_by_instruction(instruction: str) -> int:
    instructions = model.Instructions

    try:
        obj_data = {
            "instruction": instruction
        }
        _instruction = await instructions.create(**obj_data)
        return _instruction.id
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_instruction_by_instruction(instruction)
        logging.info("Instruction with content '%s' already exists", instruction)
        return id


# OK
async def update_instruction_by_id(instruction_id: int, instruction: str = None) -> None:
    instructions = model.Instructions
    try:
        obj = await instructions.get(instruction_id)
        instruction = instruction if (instruction is not None) else obj.instruction
        obj_data = {
            "instruction": instruction
        }
        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Instruction with id %s doesn't exist", str(instruction_id))


# OK
async def get_instruction_by_instruction(instruction: str) -> int:
    instructions = model.Instructions
    id = await instructions.query.where(instructions.instruction == instruction).gino.scalar()
    return id


# PLANNING
# OK
async def retrieve_planning_by_id(planning_id: int) -> Optional[schema.Plan]:
    obj = await model.Plan.get(planning_id)
    return obj.as_schema() if obj else None


# OK
async def delete_planning_by_id(planning_id: int) -> None:
    await model.Plan.delete.where(model.Plan.id == planning_id).gino.status()


# OK
async def create_planning_by_planning(prep_time: str = None, cook_time: str = None, total_time: str = None,
                                      serves: str = None) -> int:
    planning = model.Plan
    try:
        obj_data = {
            "prep_time": prep_time,
            "cook_time": cook_time,
            "total_time": total_time,
            "serves": serves
        }
        _planning = await planning.create(**obj_data)
        return _planning.id
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_planning_id_by_parameters(prep_time, cook_time, total_time, serves)
        logging.info(
            "Planning with [prep_time = %s, cook_time = %s, total_time = %s, %s serves] already exists", str(prep_time),
            str(cook_time), str(total_time), str(serves))
        return id


# OK
async def update_planning_by_id(planning_id: int, prep_time: str = None, cook_time: str = None, total_time: str = None,
                                serves: str = None) -> None:
    planning = model.Plan
    try:
        obj = await planning.get(planning_id)
        prep_time = prep_time if (prep_time is not None) else obj.prep_time
        cook_time = cook_time if (cook_time is not None) else obj.cook_time
        total_time = total_time if (total_time is not None) else obj.total_time
        serves = serves if (serves is not None) else obj.serves

        obj_data = {
            "prep_time": prep_time,
            "cook_time": cook_time,
            "total_time": total_time,
            "serves": serves
        }

        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Planning with id %s doesn't exist", str(planning_id))


# OK
async def get_planning_id_by_parameters(prep_time: str = None, cook_time: str = None, total_time: str = None,
                                        serves: str = None) -> int:
    planning = model.Plan
    id = await planning.query.where(planning.prep_time == prep_time).where(planning.cook_time == cook_time).where(
        planning.total_time == total_time).where(planning.serves == serves).gino.scalar()
    return id


# NUTRITION

# OK
async def retrieve_nutrition_by_id(nutrition_id: int) -> Optional[schema.Nutrition]:
    obj = await model.Nutrition.get(nutrition_id)
    return obj.as_schema() if obj else None


# OK
async def delete_nutrition_by_id(nutrition_id: int) -> None:
    await model.Nutrition.delete.where(model.Nutrition.id == nutrition_id).gino.status()


# OK
async def create_nutrition_by_nutrition(energy: str = None, fat: str = None, saturated_fat: str = None,
                                        carbohydrate: str = None, sugars: str = None,
                                        protein: str = None, salt: str = None, fibre: str = None) -> int:
    nutrition = model.Nutrition
    try:
        obj_data = {
            "energy": energy,
            "fat": fat,
            "saturated_fat": saturated_fat,
            "carbohydrate": carbohydrate,
            "sugars": sugars,
            "protein": protein,
            "salt": salt,
            "fibre": fibre
        }
        _nutrition = await nutrition.create(**obj_data)
        return _nutrition.id
    except asyncpg.exceptions.UniqueViolationError:
        id = await get_nutrition_id_by_parameters(energy, fat, saturated_fat, carbohydrate,
                                                  sugars, protein, salt, fibre)
        logging.info("This nutrition with this exact nutrient information already exists")
        return id


# OK
async def update_nutrition_by_id(nutrition_id: int, energy: str = None, fat: str = None, saturated_fat: str = None,
                                 carbohydrate: str = None, sugars: str = None,
                                 protein: str = None, salt: str = None, fibre: str = None) -> None:
    nutrition = model.Nutrition
    try:
        obj = await nutrition.get(nutrition_id)

        energy = energy if (energy is not None) else obj.energy
        fat = fat if (fat is not None) else obj.fat
        saturated_fat = saturated_fat if (saturated_fat is not None) else obj.saturated_fat
        carbohydrate = carbohydrate if (carbohydrate is not None) else obj.carbohydrate
        sugars = sugars if (sugars is not None) else obj.sugars
        protein = protein if (protein is not None) else obj.protein
        salt = salt if (salt is not None) else obj.salt
        fibre = fibre if (fibre is not None) else obj.fibre

        obj_data = {
            "energy": energy,
            "fat": fat,
            "saturated_fat": saturated_fat,
            "carbohydrate": carbohydrate,
            "sugars": sugars,
            "protein": protein,
            "salt": salt,
            "fibre": fibre
        }

        await obj.update(**obj_data).apply()
    except AttributeError:
        logging.warning("Planning with id %s doesn't exist", str(nutrition_id))


# OK
async def get_nutrition_id_by_parameters(energy: str = None, fat: str = None, saturated_fat: str = None,
                                         carbohydrate: str = None, sugars: str = None,
                                         protein: str = None, salt: str = None, fibre: str = None) -> int:
    nutrition = model.Nutrition
    nutrition_id = await nutrition.query.where(nutrition.energy == energy).where(nutrition.fat == fat).where(
        nutrition.saturated_fat == saturated_fat).where(nutrition.carbohydrate == carbohydrate).where(
        nutrition.sugars == sugars).where(nutrition.protein == protein).where(
        nutrition.salt == salt).where(nutrition.fibre == fibre).gino.scalar()
    return nutrition_id


async def main():
    await db.set_bind("postgresql://racine@localhost/stepa")

    # print(await retrieve_recipe_by_id(67))
    # print(await delete_recipe_by_id(67))
    # print(await delete_recipe_by_id(1000000000))
    # print(await retrieve_recipe_by_id(67))
    # await create_recipe_by_title("LALALALALA_RECIPE")
    # await create_recipe_by_title("LALALALALA_RECIPE")
    #
    # await update_recipe_by_id(26543, "")

    # print(await create_product("ldld", "kld", "jfkd"))
    # print(await create_product("ldld", "kld", "r"))
    # print(await create_product("f", "kld", "r"))

    # await update_product_by_id(758434)
    #
    # print(await get_product_id_by_parameters("ldld", "kld", "r"))

    # print(await create_image_by_image_url("veggie"))
    # print(await create_image_by_image_url("veggie"))

    # print(await create_planning_by_planning("hfjdk", "gfd", "hgf", "gfd"))
    # print(await create_nutrition_by_nutrition("hfjdk", "gfd", "hgf", "jgds", "gjfkdlso", "hgbfvds"))
    # print(await create_nutrition_by_nutrition("hfjdk", "gfd", "hgf", "jgds", "gjfkdlso", "hgbfvds"))
    # print(await delete_nutrition_by_id(2))

    # await update_planning_by_id(11)
    # print(await retrieve_planning_by_id(1))
    # await delete_planning_by_id(1)
    # await delete_planning_by_id(7)
    # print(await retrieve_instruction_by_id(1))
    # await delete_instruction_by_id(1)

    # print(await delete_tag_by_id(1))
    # print(await get_image_id_by_image_url("hfjdk"))
    #
    # print(await retrieve_image_by_id(5))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
