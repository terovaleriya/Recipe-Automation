import os
import re

from recipe_parser.html_loader import get_html

if not os.path.exists("recipes_html"):
    os.makedirs("recipes_html_A4")

urls = open("files/recipes_urls.txt", "r")
for url in urls.read().split("\n"):
    id = re.findall('[^/]+(?=/$|$)', url)[0]
    if not os.path.exists('recipes_html/' + id):
        try:
            cur_soup = get_html(url)
            with open('recipes_html/' + id, 'w') as f:
                f.write(cur_soup)
        except ConnectionError:
            print("Can't get html from " + url)
