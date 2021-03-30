import json
import os

# where we take jsons from
json_folder = "recipes_json"

# where we want put ingredients
to_file = "ingredients.txt"

ingredients = set()

for file in os.listdir(json_folder):
    with open(json_folder + "/" + file) as f:
        data = json.loads(f.readline())["ingredients"]
        for i in data:
            ingredients.add(i["item"])

ingredients_txt = open(to_file, "w")
for i in ingredients:
    ingredients_txt.write(i + "\n")
