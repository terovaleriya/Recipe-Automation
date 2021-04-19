from typing import Optional

from core import schema, model


# RECIPE

async def retrieve_recipe_by_id(recipe_id: int) -> Optional[schema.Recipe]:
    obj = await model.Recipes.get(recipe_id)
    return obj.as_schema() if obj else None


async def delete_recipe_by_id(recipe_id: int) -> None:
    await model.Recipes.delete.where(model.Recipes.id == recipe_id).gino.status()


async def create_recipe_by_title(title: str) -> None:
    recipes = model.Recipes
    id = await get_recipe_id_by_title(title)
    if id is not None:
        print("Recipe with this title already exists")
        return
    obj_data = {
        "title": title
    }
    await recipes.create(**obj_data)


async def update_recipe_by_id(recipe_id: int, title: str) -> None:
    recipes = model.Recipes
    obj = await recipes.get(recipe_id)
    title = title if (title is not None) else obj.title
    obj_data = {
        "title": title
    }
    if not obj:
        print("Recipe with this ID doesn't exist")

    await obj.update(**obj_data).apply()


async def get_recipe_id_by_title(title: str) -> int:
    recipes = model.Recipes
    id = await recipes.query.where(recipes.title == title).gino.scalar()
    return id


# INGREDIENT
async def retrieve_ingredient_by_id(ingredient_id: int) -> Optional[schema.Ingredient]:
    obj = await model.Ingredients.get(ingredient_id)
    return obj.as_schema() if obj else None


async def delete_ingredient_by_id(ingredient_id: int) -> None:
    await model.Ingredients.delete.where(model.Ingredients.id == ingredient_id).gino.status()


async def create_ingredient_by_raw_string(raw_string: str, name: str = None, quantity: str = None,
                                          comment: str = None) -> None:
    ingredients = model.Ingredients

    id = await get_ingredient_id_by_raw_string(raw_string)

    if id is not None:
        print("Ingredient with this raw string already exists")
        return

    obj_data = {
        "name": name,
        "quantity": quantity,
        "comment": comment,
        "raw_string": raw_string
    }

    await ingredients.create(**obj_data)


async def update_ingredient_by_id(ingredient_id: int, raw_string: str, name: str = None, quantity: str = None,
                                  comment: str = None) -> None:
    ingredients = model.Ingredients
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
    if not obj:
        print("Ingredient with this id doesn't exist")
        return
    await obj.update(**obj_data).apply()


async def get_ingredient_id_by_raw_string(raw_string: str) -> int:
    ingredients = model.Ingredients
    id = await ingredients.query.where(ingredients.raw_string == raw_string).gino.scalar()
    return id


# PRODUCT
async def retrieve_product_by_id(product_id: int) -> Optional[schema.Product]:
    obj = await model.Products.get(product_id)
    return obj.as_schema() if obj else None


async def delete_product_by_id(product_id: int) -> None:
    await model.Products.delete.where(model.Products.id == product_id).gino.status()


async def create_product(name: str, size: str, image_url: str) -> None:
    products = model.Products
    id = await get_product_id_by_name(name)
    if id is not None:
        product = await products.get(id)
        if product.size == size and product.image_url == image_url:
            print("This product with this exact size and image url already exists")
            return
    obj_data = {
        "name": name,
        "size": size,
        "image_url": image_url
    }
    await products.create(**obj_data)


async def update_product_by_id(product_id: int, name: str = None, size: str = None, image_url: str = None) -> None:
    products = model.Products
    obj = await products.get(product_id)
    name = name if (name is not None) else obj.name
    size = size if (size is not None) else obj.size
    image_url = image_url if (image_url is not None) else obj.image_url
    obj_data = {
        "name": name,
        "size": size,
        "image_url": image_url
    }
    if not obj:
        print("Product with this ID doesn't exist")
    else:
        await obj.update(**obj_data).apply()


async def get_product_id_by_name(name: str):
    products = model.Products
    p_id = await products.select("id").where(products.name == name).gino.scalar()
    return p_id


# TAG

async def retrieve_tag_by_id(tag_id: int) -> Optional[schema.Tag]:
    obj = await model.Tags.get(tag_id)
    return obj.as_schema() if obj else None


async def delete_tag_by_id(tag_id: int) -> None:
    await model.Tags.delete.where(model.Tags.id == tag_id).gino.status()


async def create_tag_by_tag(tag: str) -> None:
    tags = model.Tags
    id = await get_tag_id_by_tag(tag)
    if id:
        print("Tag with this name already exists")
        return
    obj_data = {
        "tag": tag
    }
    await tags.create(**obj_data)


async def update_tag_by_id(tag_id: int, tag: str) -> None:
    tags = model.Tags
    obj = await tags.get(tag_id)
    tag = tag if (tag is not None) else obj.tag
    obj_data = {
        "tag": tag
    }
    if not obj:
        print("Tag with this ID doesn't exist")
        return
    await obj.update(**obj_data).apply()


async def get_tag_id_by_tag(tag: str) -> int:
    tags = model.Tags
    id = await tags.query.where(tags.tag == tag).gino.scalar()
    return id


# IMAGE URL


async def retrieve_image_by_id(image_id: int) -> Optional[schema.Image]:
    obj = await model.Images.get(image_id)
    return obj.as_schema() if obj else None


async def delete_image_by_id(image_id: int) -> None:
    await model.Images.delete.where(model.Images.id == image_id).gino.status()


async def create_image_by_image_url(image_url: str) -> None:
    images = model.Images
    id = await get_image_id_by_image_url(image_url)
    if id:
        print("Image with this image URL already exists")
        return
    obj_data = {
        "image": image_url
    }
    await images.create(**obj_data)


async def update_image_by_id(image_id: int, image_url: str) -> None:
    images = model.Images
    obj = await images.get(image_id)
    image_url = image_url if (image_url is not None) else obj.image_url
    obj_data = {
        "image": image_url
    }
    if not obj:
        print("Image with this ID doesn't exist")
        return
    await obj.update(**obj_data).apply()


async def get_image_id_by_image_url(image_url: str) -> int:
    images = model.Images
    id = await images.query.where(images.image == image_url).gino.scalar()
    return id


# INSTRUCTIONS


async def retrieve_instruction_by_id(instruction_id: int) -> Optional[schema.Instruction]:
    obj = await model.Instructions.get(instruction_id)
    return obj.as_schema() if obj else None


async def delete_instruction_by_id(instruction_id: int) -> None:
    await model.Instructions.delete.where(model.Instructions.id == instruction_id).gino.status()


async def create_instruction_by_instruction(instruction: str) -> None:
    instructions = model.Instructions
    id = await get_instruction_by_instruction(instruction)
    if id:
        print("Instruction with this content already exists")
        return
    obj_data = {
        "instruction": instruction
    }
    await instructions.create(**obj_data)


async def update_instruction_by_id(instruction_id: int, instructions: str) -> None:
    instructions = model.Instructions
    obj = await instructions.get(instruction_id)
    image_url = instructions if (instructions is not None) else obj.instructions
    obj_data = {
        "instruction": instructions
    }
    if not obj:
        print("Instruction with this ID doesn't exist")
        return
    await obj.update(**obj_data).apply()


async def get_instruction_by_instruction(instruction: str) -> int:
    instructions = model.Instructions
    id = await instructions.query.where(instructions.instruction == instruction).gino.scalar()
    return id


# PLANNING

async def retrieve_plannnig_by_id(planning_id: int) -> Optional[schema.Plan]:
    obj = await model.Plan.get(planning_id)
    return obj.as_schema() if obj else None


async def delete_planning_by_id(planning_id: int) -> None:
    await model.Plan.delete.where(model.Plan.id == planning_id).gino.status()


async def create_planning_by_planning(preptime: str, cooktime: str, totaltime: str, serves: str) -> None:
    planning = model.Plan
    obj_data = {
        "prep_time": preptime,
        "cook_time": cooktime,
        "total_time": totaltime,
        "serves": serves
    }
    id = await planning.query.where(planning.prep_time == preptime).where(planning.cook_time == cooktime).where(
        planning.total_time == totaltime).where(planning.serves == serves).gino.scalar()
    if id is not None:
        print("This planning with this exact time estimations already exists")
        return
    await planning.create(**obj_data)


async def update_planning_by_id(planning_id: int, prep_time: str, cook_time: str, total_time: str, serves: str) -> None:
    planning = model.Plan
    obj = await planning.get(planning_id)
    if not obj:
        print("Planning with this ID doesn't exist")
        return
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


# NUTRITION

async def retrieve_nutrition_by_id(nutrition_id: int) -> Optional[schema.Nutrition]:
    obj = await model.Nutrition.get(nutrition_id)
    return obj.as_schema() if obj else None


async def delete_nutrition_by_id(nutrition_id: int) -> None:
    await model.Nutrition.delete.where(model.Nutrition.id == nutrition_id).gino.status()


async def create_nutrition_by_nutrition(energy: str, fat: str, saturated_fat: str, carbohydrate: str, sugars: str,
                                        protein: str, salt: str, fibre: str) -> None:
    nutrition = model.Nutrition
    obj_data = {
        "energy": energy,
        "fat": fat,
        "saturated_fat": saturated_fat,
        "carbohydrate": carbohydrate,
        "sugars": sugars,
        "protein": protein,
        "salt": salt,
        "fibre": fibre,
    }
    id = await nutrition.query.where(nutrition.energy == energy).where(nutrition.fat == fat).where(
        nutrition.saturated_fat == saturated_fat).where(nutrition.carbohydrate == carbohydrate).where(
        nutrition.sugars == sugars).where(nutrition.protein == protein).where(
        nutrition.salt == salt).where(nutrition.fibre == fibre).gino.scalar()
    if id is not None:
        print("This nutrition with this exact time estimations already exists")
        return
    await nutrition.create(**obj_data)


async def update_nutrition_by_id(nutrition_id: int, energy: str, fat: str, saturated_fat: str, carbohydrate: str,
                                 sugars: str,
                                 protein: str, salt: str, fibre: str) -> None:
    nutrition = model.Nutrition
    obj = await nutrition.get(nutrition_id)
    if not obj:
        print("Planning with this ID doesn't exist")
        return
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

#
# async def main():
#     await db.set_bind("postgresql://racine@localhost/stepa")
#     with open("my_json.json", "r") as file:
#         await create_recipe_by_title("Печенная дыня")
#         await create_ingredient_by_raw_string("Винчик", "много (бутылок 5)", "Здесь был я", "So Raaaaw")
#         await create_product("Сыр к винчику", "упаковка", "LINKKK")
#         await create_product("Мороженное", "брикет", "linknknknk")
#         await create_product("Мороженное", "3 брикета", "linknknknk")
#         id = await get_recipe_id_by_title("Печенная дыня")
#         await update_product_by_id(1, size="")
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
