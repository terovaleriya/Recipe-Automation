import json


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


all_products = json.load(open('../download_products/all_products.txt'))

while True:
    s = input()
    print(search_ingredient(s, all_products))
