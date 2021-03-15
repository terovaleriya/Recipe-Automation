import json
import unittest

from recipe_parser.parser import Parser
from recipe_parser.recipe import *

url_beef = 'https://www.waitrose.com/content/waitrose/en/home/recipes/recipe_directory/p/pulled-beef-saladwithmintavocado0.html'


class test_Parser_beef(unittest.TestCase):

    def test_parse_html(self):
        recipe = Parser(url_beef).recipe()
        my_recipe = Recipe("Pulled beef salad with mint & avocado", [Tag("Gluten Free")],
                           Planing("10 minutes", "30 minutes", "40 minutes", "2"),
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
                           [
                               "//d1v30bmd12dhid.cloudfront.net/static/version6/content/dam/waitrose/recipes/images/p/WW-Pulled-Beef-Mint-Avocado-Salad-Shroud.gif/_jcr_content/renditions/cq5dam.thumbnail.200.200.png"])
        if not self.assertEqual(str(my_recipe), str(recipe)):
            self.assertEqual(my_recipe.title, recipe.title)
            self.assertEqual(my_recipe.tags, recipe.tags)
            self.assertEqual(str(my_recipe.planning), str(recipe.planning))
            self.assertEqual(str(my_recipe.ingredients), str(recipe.ingredients))
            self.assertEqual(str(my_recipe.instructions), str(recipe.instructions))
            self.assertEqual(my_recipe.nutrition, recipe.nutrition)
            self.assertEqual(my_recipe.images_url, recipe.images_url)

    def test_get_json(self):
        jsonStr = Parser(url_beef).get_json()
        my_jsonStr = json.JSONEncoder(ensure_ascii=False).encode(
            {
                "title": "Pulled beef salad with mint & avocado",
                "tags": [
                    {
                        "tag": "Gluten Free"
                    }
                ],
                "planning": {
                    "prep_time": "10 minutes",
                    "cook_time": "30 minutes",
                    "total_time": "40 minutes",
                    "serves": "2"
                },
                "nutrition": {
                    "Energy": "3,226kJ 768kcals",
                    "Fat": "29g",
                    "Saturated Fat": "7.9g",
                    "Carbohydrate": "78g",
                    "Sugars": "17g",
                    "Protein": "44g",
                    "Salt": "1.3g",
                    "Fibre": "8g"
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
                        "item": "3 tbsp Cooks' Ingredients Thai Sweet Chilli Sauce"
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
                        "item": "1 Cooks' Ingredients Red Thai Chilli, thinly sliced"
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
                "images_url": [
                    "//d1v30bmd12dhid.cloudfront.net/static/version6/content/dam/waitrose/recipes/images/p/WW-Pulled-Beef-Mint-Avocado-Salad-Shroud.gif/_jcr_content/renditions/cq5dam.thumbnail.200.200.png"
                ]
            })
        self.assertEqual(my_jsonStr, jsonStr)


if __name__ == '__main__':
    unittest.main()
