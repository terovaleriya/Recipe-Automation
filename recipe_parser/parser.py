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
    ingredients = recipe.find("div", {'class', re.compile('parbase ingredients text.*')})
    all_ingredients: List[Ingredient] = []
    if not ingredients:
        print(ingredients)
    for ingredient in ingredients.text.split("\n"):
        if ingredient:
            all_ingredients.append(Ingredient(ingredient.strip()))
            # print(parse(normalize(ingredient)))
            # print(normalize(ingredient) + "\n\n")
    assert all_ingredients is not None
    return all_ingredients


def get_instructions(recipe: BeautifulSoup) -> List[Step]:
    instructions = recipe.find('div', {'class', re.compile("method parbase text.*")})

    all_instructions: List[Step] = []

    for step in instructions.findAll('p'):
        if step:
            all_instructions.append(Step(step.text.strip()))
    assert all_instructions is not None
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


def get_recipe(url, file: bool):
    recipe = recipe_content(url, file)
    return Recipe(get_title(recipe), get_tags(recipe), get_planning(recipe), get_ingredients(recipe),
                  get_instructions(recipe),
                  get_nutrition(recipe), get_image(recipe))


# getting json out of parsed Recipe
def get_json(url, file: bool):
    recipe = get_recipe(url, file)
    # with open('recipe_json.txt', 'w') as outfile:
    #     json.dump(recipe.__dict__, outfile, default=lambda o: o.__dict__, ensure_ascii=False, indent=2)
    return json.dumps(recipe.__dict__, default=lambda o: o.__dict__, ensure_ascii=False)
