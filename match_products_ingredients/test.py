from database_phantom.database import Database
from collections import Counter


def score(ingredient_name, product_name):
    ingredient_set = set(ingredient_name.lower().split())
    product_set = set(product_name.lower().split())
    return len(ingredient_set & product_set) / len(ingredient_set | product_set)


def search_ingredient(ingredient_name, all_products):
    best_products = []
    best_score = 1e-9
    for product in all_products:
        product_name = product['name']
        cur_score = score(ingredient_name, product_name)
        if cur_score > best_score:
            best_score = cur_score
            best_products = [product]
        elif cur_score == best_score:
            best_products.append(product)
    print(f"score: {best_score}")
    return best_products


def match_ingredient_and_products(ingredient_name, all_products):
    result = []
    for product in all_products:
        product_name = product['name']
        cur_score = score(ingredient_name, product_name)
        result.append((cur_score, product['id']))
    result.sort(key=lambda x: x[0], reverse=True)
    return list(map(lambda x: x[1], result[:5]))


# all_products = json.load(open('../download_products/all_products.txt'))
#
# while True:
#     s = input()
#     print(search_ingredient(s, all_products))

matching_db = Database()
matching_db.create_table(['ingredientId', 'productIds', 'checked', 'answer'])

ingredients_db = Database()
ingredients_db.load_from_file('../database_phantom/db_ingredients.txt')
ingredients = ingredients_db.select_all()

products_db = Database()
products_db.load_from_file('../database_phantom/db_products.txt')
products = products_db.select_all()

all_items = []

for ingred in products:
    # print(ingred['name'])
    ingredient_name = ingred['name']
    items = set(ingredient_name.lower().split())
    all_items.extend(items)

count = Counter(all_items)
print(*sorted(count.items(), key=lambda x: x[1], reverse=True)[:1000], sep='\n')
