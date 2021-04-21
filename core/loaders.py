from typing import List

from core import model
from core.domain import create_recipe_by_title, create_ingredient_by_raw_string, create_tag_by_tag, \
    create_instruction_by_instruction, create_image_by_image_url, \
    create_planning_by_planning, create_nutrition_by_nutrition, create_link

from recipe_parser.recipe import Recipe


async def recipe_to_db(recipe: Recipe):
    recipe_id = await create_recipe_by_title(recipe.title)

    ingredients = recipe.ingredients
    if ingredients:
        for ingredient in ingredients:
            ingredient_id = await create_ingredient_by_raw_string(ingredient.get("item"))
            await create_link(model.RecipesIngredients, recipe_id, ingredient_id)

    tags = recipe.tags
    if tags:
        for tag in tags:
            tag_id = await create_tag_by_tag(tag.get("tag"))
            await create_link(model.RecipesTags, recipe_id, tag_id)

    instructions = recipe.instructions
    if instructions:
        for instruction in instructions:
            instruction_id = await create_instruction_by_instruction(instruction.get("step"))
            await create_link(model.RecipesInstructions, recipe_id, instruction_id)

    image_id = await create_image_by_image_url(recipe.image_url)
    await create_link(model.RecipesImages, recipe_id, image_id)

    planning = recipe.planning
    if planning:
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


async def load_unchecked_products(ingredient_id: int, id_list: List[int]):
    for id in id_list:
        await create_link(model.UncheckedIngredientsProducts, ingredient_id, id)


async def load_matched_product(ingredient_id: int, product_id: int):
    await create_link(model.MatchedIngredientsProducts, ingredient_id, product_id)
