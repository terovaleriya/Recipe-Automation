import json
import os

from recipe_parser.parser import get_json

# битые по каким-то причинам html, потом разберусь


ingredients = set()
# ingredients = []

for file in os.listdir("recipes_json"):
    with open("recipes_json/" + file) as f:
        data = json.loads(f.readline())["ingredients"]
        for i in data:
            # ingredients.add(i["item"])
            ingredients.add(i["item"])

ingredients_txt = open("ingredients.txt", "w")

for i in ingredients:
    ingredients_txt.write(i + "\n")

