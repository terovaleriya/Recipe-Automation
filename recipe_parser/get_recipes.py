import re

from recipe_parser.parser import Parser

url = "https://www.waitrose.com/content/waitrose/en/home/recipes..html?wtrint=1-Content-_-2-header-_-3-recipes-_-4-megamenu-_-5-recipes-_-6-allrecipes"

soup = Parser(url).soup
categories = soup.findAll("a", href=re.compile("/home/recipes/.+$"))

all_categories = []
for category in categories:
    category = category['href']
    if not category.startswith("https://www.waitrose.com"):
        category = 'https://www.waitrose.com' + category
    all_categories.append(category)

all_recipes = open('recipes_urls.txt', 'w')
for category in all_categories:
    print("Категория: " + category)
    category_soup = Parser(category).soup
    recipe_soup = category_soup.findAll("a", href=re.compile("/home/recipes/recipe_directory.+$"))
    print("Рецептов в категории: " + str(len(recipe_soup)))
    for recipe_url in recipe_soup:
        recipe_url = recipe_url['href']
        if not recipe_url.startswith("https://www.waitrose.com"):
            recipe_url = 'https://www.waitrose.com' + recipe_url
        print("Url рецепта: " + recipe_url)
        if not recipe_url.startswith("https://www.waitrose.com"):
            recipe_url = 'https://www.waitrose.com' + recipe_url + ".html"
        all_recipes.write(recipe_url + "\n")

all_recipes.close()
