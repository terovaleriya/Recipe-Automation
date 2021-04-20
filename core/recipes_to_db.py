import asyncio
import json
import os

from core import model
from core.domain import create_recipe_by_title, create_ingredient_by_raw_string, create_tag_by_tag, \
    create_instruction_by_instruction, create_image_by_image_url, \
    create_planning_by_planning, create_nutrition_by_nutrition, create_link
from core.model import db

from recipe_parser.recipe import Recipe


async def main():
    os.chdir("../recipe_parser/")
    await db.set_bind("postgresql://racine@localhost/stepa")
    json_folder = "recipes_json/"

    for f in os.listdir(json_folder):
        with open("recipes_json/" + f, "r") as file:
            json_str = file.readline()
            obj = json.loads(json_str)
            recipe = Recipe(**obj)
            recipe_id = await create_recipe_by_title(recipe.title)

            for ingredient in recipe.ingredients:
                ingredient_id = await create_ingredient_by_raw_string(ingredient.get("item"))
                await create_link(model.RecipesIngredients, recipe_id, ingredient_id)
            tags = recipe.tags
            if tags:
                for tag in tags:
                    tag_id = await create_tag_by_tag(tag.get("tag"))
                    await create_link(model.RecipesTags, recipe_id, tag_id)
            for instruction in recipe.instructions:
                instruction_id = await create_instruction_by_instruction(instruction.get("step"))
                await create_link(model.RecipesInstructions, recipe_id, instruction_id)
            image_id = await create_image_by_image_url(recipe.image_url)
            await create_link(model.RecipesImages, recipe_id, image_id)
            planning = recipe.planning
            planning_id = await create_planning_by_planning(planning.get("prep_time"), planning.get("cook_time"),
                                                            planning.get("total_time"), planning.get("serves"))
            await create_link(model.RecipesPlanning, recipe_id, planning_id)
            nutrition = recipe.nutrition
            if nutrition:
                nutrition_id = await create_nutrition_by_nutrition(nutrition.get("Energy"), nutrition.get("Fat"),
                                                                   nutrition.get("Saturated Fat"),
                                                                   nutrition.get("Carbohydrate"),
                                                                   nutrition.get("Sugars"), nutrition.get("Protein"),
                                                                   nutrition.get("Salt"), nutrition.get("Fibre"))

                await create_link(model.RecipesNutrition, recipe_id, nutrition_id)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
