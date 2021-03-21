import os
import re

from recipe_parser.get_recipe_soup import soup

if not os.path.exists("recipes_html_A4"):
    os.makedirs("recipes_html_A4")

urls = open("files/recipes_urls_A4.txt", "r")
for url in urls.read().split("\n"):
    id = re.findall('[^/]+(?=/$|$)', url)[0]
    if not os.path.exists('recipes_html_A4/' + id):
        cur_soup, page = soup(url)
        if page:
            with open('recipes_html_A4/' + id, 'w') as f:
                f.write(str(cur_soup))
            f.close()
