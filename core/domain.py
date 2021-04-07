import asyncio
from typing import Optional

from core import schema, model
from core.model import db


async def retrieve_recipe(recipe_id: int) -> Optional[schema.Recipe]:
    obj = await model.Recipes.get(recipe_id)
    return obj.as_schema() if obj else None


async def retrieve_ingredient(ingredient_id: int) -> Optional[schema.Ingredient]:
    obj = await model.Ingredients.get(ingredient_id)
    return obj.as_schema() if obj else None


async def retrieve_product(product_id: int) -> Optional[schema.Product]:
    obj = await model.Products.get(product_id)
    return obj.as_schema() if obj else None


async def delete_recipe(recipe_id: int) -> None:
    await model.Recipes.delete.where(model.Recipes.id == recipe_id).gino.status()


async def delete_ingredient(ingredient_id: int) -> None:
    await model.Ingredients.delete.where(model.Ingredients.id == ingredient_id).gino.status()


async def delete_product(product_id: int) -> None:
    await model.Products.delete.where(model.Products.id == product_id).gino.status()


async def create_or_update_recipe(recipe_id: int, title: str) -> None:
    obj = await model.Recipes.get(recipe_id)
    obj_data = {
        "title": title
    }
    if not obj:
        await model.Recipes.create(id=recipe_id, **obj_data)
    else:
        await obj.update(**obj_data).apply()


async def create_or_update_ingredient(ingredient_id: int, name: str, quantity: str,
                                      comment: str, raw_string: str) -> None:
    obj = await model.Ingredients.get(ingredient_id)
    obj_data = {
        "name": name,
        "quantity": quantity,
        "comment": comment,
        "raw_string": raw_string
    }
    if not obj:
        await model.Ingredients.create(id=ingredient_id, **obj_data)
    else:
        await obj.update(**obj_data).apply()


async def create_or_update_product(product_id: int, name: str, size: str, image_url: str) -> None:
    obj = await model.Products.get(product_id)
    obj_data = {
        "name": name,
        "size": size,
        "image_url": image_url
    }
    if not obj:
        await model.Products.create(id=product_id, **obj_data)
    else:
        await obj.update(**obj_data).apply()


async def main():
    await db.set_bind("postgresql://racine@localhost/stepa")
    await create_or_update_recipe(6, "Печенная дыня")
    recipe = await retrieve_recipe(6)
    await create_or_update_ingredient(4, "Винчик", "много (бутылок 5)", "Здесь был я", "So Raaaaw")
    ingredient = await retrieve_ingredient(4)
    await create_or_update_product(7, "Сыр к винчику", "упаковка", "LINKKK")
    await create_or_update_product(8, "Мороженное", "брикет", "linknknknk")
    product = await retrieve_product(7)
    print(recipe)
    print(ingredient)
    print(product)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
