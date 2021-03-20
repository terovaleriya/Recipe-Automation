import re

from recipe_parser.parser import Soup

url = "https://www.waitrose.com/content/waitrose/en/home/recipes.html"

# достаем список категорий
categories = Soup(url).soup.find('div', {'class': "l-content"}).findAll("a", href=re.compile("/home/recipes_html/.+$"))
categories = [category['href'] for category in categories]
categories = [category if category.startswith("https://www.waitrose.com") else 'https://www.waitrose.com' + category for
              category in categories]
categories = set(categories)

# из каждой категории достаем все рецепты
# recipes_per_category.txt – распределение рецептов по категориям, url могут повторяться
#

all_recipes = set()
distribution = open('recipes_per_category.txt', 'w')
for category in categories:
    category_soup = Soup(category).soup
    recipes = category_soup.findAll("a", href=re.compile("/home/recipes_html/recipe_directory.+$"))

    distribution.write("\nКатегория: " + category + "\n")
    distribution.write("Рецептов в категории: " + str(len(recipes)) + "\n")

    recipes = [recipe['href'] for recipe in recipes]
    recipes = [
        recipe if recipe.startswith("https://www.waitrose.com") else 'https://www.waitrose.com' + recipe + ".html"
        for recipe in recipes]
    recipes = [re.findall('.+?\.html', recipe)[0] for recipe in recipes]
    distribution.write("Url рецептов: " + "\n".join(recipes) + "\n")
    all_recipes |= set(recipes)
distribution.close()

# recipes_urls.txt – уникальный список всех url рецептов
with open('recipes_urls.txt', 'w') as f:
    for recipe_url in all_recipes:
        f.write(recipe_url + "\n")
f.close()
