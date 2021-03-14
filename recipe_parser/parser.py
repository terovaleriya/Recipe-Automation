import html
import json
import re

import requests
from bs4 import BeautifulSoup

from recipe_parser.recipe import *


def normalize(string: str):
    # Convert all named and numeric character references (e.g. &gt;, &#62;)
    unescaped_string = html.unescape(string)
    return re.sub(
        r"\s+",
        " ",
        unescaped_string.replace("\xa0", " ")
            .replace("\n", " ")  # &nbsp;
            .replace("\t", " ")
            .strip(),
    )


class Soup:
    def __init__(self, url, test: bool = False):
        if test:  # when testing, we load a file
            page_data = url.read()
            url = None
        else:
            page_data = requests.get(url).text
        self.url = url
        self.soup = BeautifulSoup(page_data, "html.parser")
        self.recipe_content = self.soup.find('body', {'class': "recipes content"})


class Parser(Soup):

    def title(self) -> str:
        title = self.recipe_content.find('h1', {'class': "title"}).text
        return normalize(title)

    def tags(self) -> List[Tag]:
        tags = self.recipe_content.find('ul', {'class': "tags"})
        if tags:
            all_tags: List[Tag] = []
            for tag in tags.findAll('li'):
                all_tags.append(Tag(normalize(tag.text)))
            return all_tags

    def planning(self) -> Planing:
        prep = self.recipe_content.find('span', {'itemprop': "prepTime"})
        prep_time = prep.text.strip() if prep else None
        cook = self.recipe_content.find('span', {'itemprop': "cookTime"})
        cook_time = cook.text if cook else None
        total = self.recipe_content.find('span', {'itemprop': "totalTime"})
        total_time = total.text if total else None
        serves = self.recipe_content.find('span', {'itemprop': "recipeYield"}).text

        return Planing(normalize(prep_time), normalize(cook_time), normalize(total_time), normalize(serves))

    def ingredients(self) -> List[Ingredient]:
        ingredients = self.recipe_content.find('div', {'itemprop': "ingredients"})
        all_ingredients: List[Ingredient] = []
        for ingredient in ingredients.text.split("\n"):
            all_ingredients.append(Ingredient(normalize(ingredient)))
        return all_ingredients

    def instructions(self) -> List[Step]:
        instructions = self.recipe_content.find('div', {'class': "method"})

        all_instructions: List[Step] = []

        for child in instructions.findAll('p'):
            all_instructions.append(Step(normalize(child.text)))
        return all_instructions

    def images(self) -> str:
        images = self.recipe_content.find('img')
        if images:
            image = images.parent.find("img", {"src": True})
            return image["src"] if image else ""

    def nutrition(self) -> dict:
        table = self.recipe_content.find('div', {'itemprop': "nutrition"})
        return {normalize(i.text): normalize(cell.text) for i, cell in zip(table.findAll("th"), table.findAll("td"))}

    def recipe(self):
        return Recipe(self.title(), self.tags(), self.planning(), self.ingredients(), self.instructions(),
                      self.nutrition(), self.images())

    # getting json out of parsed Recipe
    def get_json(self) -> json:
        recipe = self.recipe()
        with open('recipe_json.txt', 'w') as outfile:
            json.dump(recipe.__dict__, outfile, default=lambda o: o.__dict__, ensure_ascii=False, indent=4)
        return json.dumps(recipe.__dict__, default=lambda o: o.__dict__, ensure_ascii=False)
