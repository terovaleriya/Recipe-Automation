import os

from recipe_parser.parser import Parser

if not os.path.exists("recipes_json_A4"):
    os.makedirs("recipes_json_A4")

for file in os.listdir("recipes_html_A4"):
    print(file)
    with open("recipes_json_A4/" + file[:-5] + ".json", "w") as f:
        file = open("recipes_html_A4/" + file, "r")
        f.write(Parser(file, True).get_json())
        file.close()
