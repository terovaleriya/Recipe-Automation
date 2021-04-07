import asyncio
from typing import Optional

from core import schema, model
from core.model import db


async def retrieve_recipe(recipe_id: int) -> Optional[schema.Recipe]:
    obj = await model.Recipes.get(recipe_id)
    return obj.as_schema() if obj else None


async def create_or_update_recipe(recipe_id: int, title: str) -> None:
    obj = await model.Recipes.get(recipe_id)
    obj_data = {
        "title": title
    }
    if not obj:
        await model.Recipes.create(id=recipe_id, **obj_data)
    else:
        await obj.update(**obj_data).apply()


async def main():
    await db.set_bind("postgresql://racine@localhost/stepa")
    await create_or_update_recipe(6, "Печенная жопа1")
    recipe = await retrieve_recipe(6)
    print(recipe)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
