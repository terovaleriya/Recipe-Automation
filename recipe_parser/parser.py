import json
import re

from bs4 import BeautifulSoup

from recipe_parser.get_recipe_soup import recipe_content
from recipe_parser.recipe import *


def get_title(recipe: BeautifulSoup) -> str:
    title = recipe.find('h2').text
    assert title is not None
    return title.strip()


def get_tags(recipe: BeautifulSoup) -> List[Tag]:
    tags = recipe.find('ul', {'class': "tags"})
    if tags:
        all_tags: List[Tag] = []
        for tag in tags.findAll('li'):
            all_tags.append(Tag(tag.text.strip()))
        return all_tags


def get_planning(recipe: BeautifulSoup) -> Planing:
    prep_time = recipe.find('span', {'itemprop': "prepTime"})
    prep_time = prep_time["content"].strip() if prep_time else None
    cook_time = recipe.find('span', {'itemprop': "cookTime"})
    cook_time = cook_time["content"].strip() if cook_time else None
    total_time = recipe.find('span', {'itemprop': "totalTime"})
    total_time = total_time["content"].strip() if total_time else None
    serves = recipe.find('span', {'itemprop': "recipeYield"})
    serves = serves.text.strip() if serves else None

    return Planing(prep_time, cook_time, total_time, serves)


def get_ingredients(recipe: BeautifulSoup) -> List[Ingredient]:
    ingredients_list = recipe.find("div", {'class': re.compile('parbase ingredients text.*')})
    if ingredients_list.find('div', class_="text"):
        ingredients_list = ingredients_list.find('div', class_="text")
        ingredients_list = ingredients_list.text.split('\n')
    else:
        ingredients_list = ingredients_list.find_all("p")
        ingredients_list = [i.get_text().replace("\n", "") for i in ingredients_list]
    all_ingredients: List[Ingredient] = []
    for ingredient in ingredients_list:
        ingredient = ingredient.replace("• ", "").replace("• ;", "").replace("*", "").strip()
        comment = ingredient.startwith("(") and ingredient.endswith(")")
        if ingredient and not ingredient.isupper() and not ingredient.endswith(":") and not comment:
            all_ingredients.append(Ingredient(ingredient))
    assert all_ingredients is not None
    return all_ingredients


def get_instructions(recipe: BeautifulSoup) -> List[Step]:
    instructions_list = recipe.find('div', {'class', re.compile("method parbase text.*")})
    if instructions_list.find('div', class_="text"):
        instructions_list = instructions_list.find('div', class_="text")
        instructions_list = instructions_list.text.split('\n')
    else:
        instructions_list = instructions_list.find_all("p")
        instructions_list = [i.get_text().replace("\n", "") for i in instructions_list]

    all_instructions: List[Step] = []
    for instruction in instructions_list:
        ingredient = instruction.replace("• ", "").replace("• ;", "").strip()
        if ingredient and not ingredient.isupper() and not ingredient.endswith(":"):
            all_instructions.append(Step(ingredient))
    return all_instructions


def get_image(recipe: BeautifulSoup) -> str:
    image = recipe.find('img')["src"]

    # getting a larger picture (some of 200.200 don't exist)
    image = image.replace("200.200", "400.400")
    return image.strip()


def get_nutrition(recipe: BeautifulSoup) -> dict:
    table = recipe.find('div', {'itemprop': "nutrition"})
    if table:
        th = table.findAll("th")
        td = table.findAll("td")
        return {i.text.strip(): cell.text.strip() for i, cell in zip(th, td)}


def get_recipe(url):
    recipe = recipe_content(url)
    return Recipe(get_title(recipe), get_tags(recipe), get_planning(recipe), get_ingredients(recipe),
                  get_instructions(recipe),
                  get_nutrition(recipe), get_image(recipe))


# getting json out of parsed Recipe
def get_json(url):
    recipe = get_recipe(url)
    return json.dumps(recipe.__dict__, default=lambda o: o.__dict__, ensure_ascii=False)
