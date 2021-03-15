from recipe_parser.parser import Parser

# url = 'https://www.waitrose.com/content/waitrose/en/home/recipes/recipe_directory/l/lemon-chess-pie-withclottedcream.html'
# url = "https://www.waitrose.com/content/waitrose/en/home/recipes/recipe_directory/s/spinach-feta-filopie.html"
# url = 'https://www.waitrose.com/content/waitrose/en/home/recipes/recipe_directory/c/chocolate-brownieswithcaramelandhazelnuts.html'
url = 'https://www.waitrose.com/content/waitrose/en/home/recipes/recipe_directory/p/pulled-beef-saladwithmintavocado0.html'

# print(Parser(url).title())
# print(Parser(url).tags())
# print(Parser(url).planning())
# print(Parser(url).nutrition())
# print(Parser(url).ingredients())
# print(Parser(url).instructions())
# print(Parser(url).images())

print(Parser(url).get_json())




