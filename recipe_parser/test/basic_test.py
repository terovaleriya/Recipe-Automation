import json
import os
import re
import unittest
import pytest

from recipe_parser.html_loader import get_html
from recipe_parser.parser import get_recipe, get_json
from recipe_parser.recipe import *

unittest.TestLoader.sortTestMethodsUsing = None

os.chdir("recipe_parser/test/")


def pytest_namespace():
    return {'file_path': ''}


class TestParserBeef(unittest.TestCase):
    @pytest.fixture
    def TestLoadHtml(self):
        beef_url = "https://www.waitrose.com/content/waitrose/en/home/recipes/recipe_directory/p/pulled-beef-saladwithmintavocado0.A4.html"

        id = re.findall('[^/]+(?=/$|$)', beef_url)[0]
        try:
            cur_soup = get_html(beef_url)
            with open(id, 'w') as f:
                f.write(cur_soup)
        except ConnectionError:
            print("Can't get html from " + beef_url)
        pytest.file_path = id + ".html"
        

    def TestParseHtml(self):
        beef_file = open(pytest.file_path, "r")
        recipee = get_recipe(beef_file)
        my_recipe = Recipe("Pulled beef salad with mint & avocado", [Tag("Gluten Free")],
                           Planing("PT10M", "PT30M", "PT40M", "2"),
                           [Ingredient('380g pack slow cooked beef brisket'),
                            Ingredient('2 echalion shallots, thinly sliced into rings'),
                            Ingredient('2 essential Lemons, juice reserved'),
                            Ingredient('3 tbsp Cooks’ Ingredients Thai Sweet Chilli Sauce'),
                            Ingredient('1 x 350g tub Thai Sticky Rice'),
                            Ingredient('1 Waitrose 1 Perfectly Ripe Extra Large Avocado, stoned and sliced'),
                            Ingredient('½ x 25g pack mint, leaves picked'),
                            Ingredient('1 Cooks’ Ingredients Red Thai Chilli, thinly sliced')],
                           [Step(
                               "1. Preheat the oven to 200°C, gas mark 6. Cook the beef for 30 minutes, following pack instructions. Discard any large pieces of fat from the liquor before you cook."),
                               Step(
                                   "2. Toss the shallots with 5 tbsp lemon juice and the sweet chilli sauce to create a dressing, then set aside."),
                               Step(
                                   "3. When the meat is cooked, lift it from the juices and pull to shreds using two forks. Add 2 tbsp of the cooking juices to the shallots and sweet chilli sauce."),
                               Step("4. Meanwhile, heat the sticky rice according to the pack instructions."),
                               Step(
                                   "5. Toss the meat with the dressing, avocado, mint leaves and fresh Thai chilli, then serve straight away with the sticky rice.")],
                           {'Energy': '3,226kJ 768kcals', 'Fat': '29g', 'Saturated Fat': '7.9g', 'Carbohydrate': '78g',
                            'Sugars': '17g',
                            'Protein': '44g', 'Salt': '1.3g', 'Fibre': '8g'},
                           "//d1v30bmd12dhid.cloudfront.net/static/version6/content/dam/waitrose/recipes/images/p/WW-Pulled-Beef-Mint-Avocado-Salad-Shroud.gif/_jcr_content/renditions/cq5dam.thumbnail.400.400.png"
                           )
        # if not self.assertEqual(str(my_recipe), str(recipe)):
        self.assertEqual(my_recipe.title, recipee.title)
        self.assertEqual(str(my_recipe.tags), str(recipee.tags))
        self.assertEqual(str(my_recipe.planning), str(recipee.planning))
        self.assertEqual(str(my_recipe.ingredients), str(recipee.ingredients))
        self.assertEqual(str(my_recipe.instructions), str(recipee.instructions))
        self.assertEqual(my_recipe.nutrition, recipee.nutrition)
        self.assertEqual(my_recipe.image_url, recipee.image_url)
        beef_file.close()

    def TestGetJson(self):
        beef_file = open(pytest.file_path, "r")
        json_str = get_json(beef_file)
        my_json_str = json.JSONEncoder(ensure_ascii=False).encode(
            {
                "title": "Pulled beef salad with mint & avocado",
                "tags": [
                    {
                        "tag": "Gluten Free"
                    }
                ],
                "planning": {
                    "prep_time": "PT10M",
                    "cook_time": "PT30M",
                    "total_time": "PT40M",
                    "serves": "2"
                },
                "ingredients": [
                    {
                        "item": "380g pack slow cooked beef brisket"
                    },
                    {
                        "item": "2 echalion shallots, thinly sliced into rings"
                    },
                    {
                        "item": "2 essential Lemons, juice reserved"
                    },
                    {
                        "item": "3 tbsp Cooks’ Ingredients Thai Sweet Chilli Sauce"
                    },
                    {
                        "item": "1 x 350g tub Thai Sticky Rice"
                    },
                    {
                        "item": "1 Waitrose 1 Perfectly Ripe Extra Large Avocado, stoned and sliced"
                    },
                    {
                        "item": "½ x 25g pack mint, leaves picked"
                    },
                    {
                        "item": "1 Cooks’ Ingredients Red Thai Chilli, thinly sliced"
                    }
                ],
                "instructions": [
                    {
                        "step": "1. Preheat the oven to 200°C, gas mark 6. Cook the beef for 30 minutes, following pack instructions. Discard any large pieces of fat from the liquor before you cook."
                    },
                    {
                        "step": "2. Toss the shallots with 5 tbsp lemon juice and the sweet chilli sauce to create a dressing, then set aside."
                    },
                    {
                        "step": "3. When the meat is cooked, lift it from the juices and pull to shreds using two forks. Add 2 tbsp of the cooking juices to the shallots and sweet chilli sauce."
                    },
                    {
                        "step": "4. Meanwhile, heat the sticky rice according to the pack instructions."
                    },
                    {
                        "step": "5. Toss the meat with the dressing, avocado, mint leaves and fresh Thai chilli, then serve straight away with the sticky rice."
                    }
                ],
                "nutrition": {
                    "Energy": "3,226kJ 768kcals",
                    "Fat": "29g",
                    "Saturated Fat": "7.9g",
                    "Carbohydrate": "78g",
                    "Sugars": "17g",
                    "Protein": "44g",
                    "Salt": "1.3g",
                    "Fibre": "8g"
                }
                ,
                "image_url": "//d1v30bmd12dhid.cloudfront.net/static/version6/content/dam/waitrose/recipes/images/p/WW-Pulled-Beef-Mint-Avocado-Salad-Shroud.gif/_jcr_content/renditions/cq5dam.thumbnail.400.400.png"
            })
        self.assertEqual(my_json_str, json_str)
        beef_file.close()


if __name__ == '__main__':
    unittest.main()
