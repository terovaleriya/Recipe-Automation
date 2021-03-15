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
        assert self.recipe_content is not None


class Parser(Soup):

    def title(self) -> str:
        title = self.recipe_content.find('h1', {'class': "title"}).text
        assert title is not None
        return normalize(title)

    def tags(self) -> List[Tag]:
        tags = self.recipe_content.find('ul', {'class': "tags"})
        if tags:
            all_tags: List[Tag] = []
            for tag in tags.findAll('li'):
                all_tags.append(Tag(normalize(tag.text)))
            return all_tags

    def planning(self) -> Planing:
        prep_time = self.recipe_content.find('span', {'itemprop': "prepTime"})
        prep_time = prep_time.text.strip() if prep_time else None
        cook_time = self.recipe_content.find('span', {'itemprop': "cookTime"})
        cook_time = cook_time.text if cook_time else None
        total_time = self.recipe_content.find('span', {'itemprop': "totalTime"})
        total_time = total_time.text if total_time else None
        serves = self.recipe_content.find('span', {'itemprop': "recipeYield"})
        serves = serves.text if serves else None

        return Planing(normalize(prep_time), normalize(cook_time), normalize(total_time), normalize(serves))

    def ingredients(self) -> List[Ingredient]:
        ingredients = self.recipe_content.find('div', {'itemprop': "ingredients"})
        all_ingredients: List[Ingredient] = []
        for ingredient in ingredients.text.split("\n"):
            if ingredient:
                all_ingredients.append(Ingredient(normalize(ingredient)))
        assert all_ingredients is not None
        return all_ingredients

    def instructions(self) -> List[Step]:
        instructions = self.recipe_content.find('div', {'class': "method"})

        all_instructions: List[Step] = []

        for step in instructions.findAll('p'):
            if step:
                all_instructions.append(Step(normalize(step.text)))
        assert all_instructions is not None
        return all_instructions

    def images(self) -> List[str]:
        images = self.recipe_content.findAll('img', {'title': self.title()})
        all_images: List[str] = []
        if images:
            for image in images:
                all_images.append(image["src"])
        return all_images

    def nutrition(self) -> dict:
        table = self.recipe_content.find('div', {'itemprop': "nutrition"})
        return {normalize(i.text): normalize(cell.text) for i, cell in zip(table.findAll("th"), table.findAll("td"))}

    def recipe(self):
        return Recipe(self.title(), self.tags(), self.planning(), self.ingredients(), self.instructions(),
                      self.nutrition(), self.images())

    # getting json out of parsed Recipe
    def get_json(self):
        recipe = self.recipe()
        with open('recipe_json.txt', 'w') as outfile:
            json.dump(recipe.__dict__, outfile, default=lambda o: o.__dict__, ensure_ascii=False, indent=4)
        return json.dumps(recipe.__dict__, default=lambda o: o.__dict__, ensure_ascii=False)
