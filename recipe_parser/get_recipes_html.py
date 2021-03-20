import os
import re

from recipe_parser.parser import Soup

if not os.path.exists("recipe_parser/recipes_html"):
    os.makedirs("recipe_parser/recipes_html")

urls = open("recipe_parser/recipes_urls.txt", "r")
for url in urls.read().split("\n"):
    id = re.findall('[^/]+(?=/$|$)', url)[0]
    if not os.path.exists('recipe_parser/recipes_html/' + id):
        with open('recipe_parser/recipes_html/' + id, 'w') as f:
            f.write(str(Soup(url).soup))
        f.close()
