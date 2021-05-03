import asyncio
from typing import Set, List

from core.domain import create_link_unchecked_ingredients_products
from core.get_db_credentials import get_credentials
from core.model import db, Products
from get_all_items.get_all_items import get_all_ingredients, get_all_products
from match_products_ingredients.nltk_preprocess import nltk_preprocess


def score(ingredient_set: Set[str], product_set: Set[str]) -> float:
    if len(ingredient_set | product_set) > 0:
        return len(ingredient_set & product_set) / len(ingredient_set | product_set)
    else:
        return -1


# all_products: List[(Products, Set[str])]
def match_ingredient_and_products(ingredient_name: str, all_products) -> List[Products]:
    result = []
    ingredient_set = nltk_preprocess(ingredient_name)
    for product, product_set in all_products:
        cur_score = score(ingredient_set, product_set)
        result.append((cur_score, product))
    result.sort(key=lambda x: x[0], reverse=True)
    return list(map(lambda x: x[1], result[:5]))


async def main():
    credentials = get_credentials()
    await db.set_bind(credentials)

    ingredients = await get_all_ingredients()
    products = await get_all_products()
    products = list((item, nltk_preprocess(item.name)) for item in products)
    for item in ingredients:
        print(item.name)
        print(item.raw_string)
        matching = match_ingredient_and_products(item.name, products)
        for match_product in matching:
            print(match_product.id, match_product.name)
        print()
        for match_product in matching:
            await create_link_unchecked_ingredients_products(match_product.id, item.id)
        # this works incorrectly
        # load_unchecked_products(item.id, [match_product.id for match_product in matching])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
