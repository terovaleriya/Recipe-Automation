import asyncio
import json
import os

from core.domain import create_recipe_by_title, create_ingredient_by_raw_string, create_product, get_recipe_id_by_title, \
    update_product_by_id, create_tag_by_tag, create_instruction_by_instruction, create_image_by_image_url, \
    create_planning_by_planning, create_nutrition_by_nutrition
from core.model import db
from recipe_parser.recipe import Recipe


async def main():
    os.chdir("../recipe_parser/")
    await db.set_bind("postgresql://racine@localhost/stepa")
    json_folder = "recipes_json/"
    for f in os.listdir(json_folder):
        with open("recipes_json/" + f, "r") as file:
            print(f)
            json_str = file.readline()
            obj = json.loads(json_str)
            recipe = Recipe(**obj)

            await create_recipe_by_title(recipe.title)
            for ingredient in recipe.ingredients:
                await create_ingredient_by_raw_string(ingredient.get("item"))
            tags = recipe.tags
            if tags:
                for tag in tags:
                    await create_tag_by_tag(tag.get("tag"))
            for instruction in recipe.instructions:
                await create_instruction_by_instruction(instruction.get("step"))
            await create_image_by_image_url(recipe.image_url)
            planning = recipe.planning
            await create_planning_by_planning(planning.get("prep_time"), planning.get("cook_time"),
                                              planning.get("total_time"), planning.get("serves"))
            nutrition = recipe.nutrition
            if nutrition:
                await create_nutrition_by_nutrition(nutrition.get("Energy"), nutrition.get("Fat"),
                                                    nutrition.get("Saturated Fat"), nutrition.get("Carbohydrate"),
                                                    nutrition.get("Sugars"), nutrition.get("Protein"),
                                                    nutrition.get("Salt"), nutrition.get("Fibre"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
