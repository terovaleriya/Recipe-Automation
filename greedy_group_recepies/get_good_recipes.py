import asyncio
import json
import string
from pprint import pprint
from random import shuffle, choice
from typing import List

from core import model
from core.domain import get_matched_products_by_ingredient_id, get_unchecked_products_by_ingredient_id, \
    retrieve_product_by_id, create_link_matched_ingredients_products, retrieve_recipe_by_id, retrieve_ingredient_by_id
from core.get_db_credentials import get_credentials
from core.model import db
from database_phantom.database import Database
from core.get_all_items import get_all_ingredients
from greedy_group_recepies.retrieve_price import retrieve_price
from greedy_group_recepies.retrieve_quantity import retrieve_quantity


async def get_recipe_ids() -> List[int]:
    link_list = await model.Recipes.query.where(True).gino.all()
    return [i.id for i in link_list]


async def get_ingredients_by_recipe_id(recipe_id: int) -> List[int]:
    link_list = await model.RecipesIngredients.query.where(
        model.RecipesIngredients.recipe == recipe_id).gino.all()
    return [i.ingredient for i in link_list]


async def get_best_product(ingredient_id):
    link_list = await model.MatchedIngredientsProducts.query.where(
        model.MatchedIngredientsProducts.ingredient == ingredient_id).gino.all()
    if len(link_list) > 0:
        link_list.sort(key=lambda x: x.id)
        return link_list[0].product

    link_list = await model.UncheckedIngredientsProducts.query.where(
        model.UncheckedIngredientsProducts.ingredient == ingredient_id).gino.all()
    if len(link_list) > 0:
        link_list.sort(key=lambda x: x.id)
        return link_list[0].product

    return None


async def main():
    credentials = get_credentials()
    await db.set_bind(credentials)

    good_recipes = []

    recipe_ids = await get_recipe_ids()
    print(len(recipe_ids))

    cnt = 0
    for recipe_id in recipe_ids:
        ingreds = await get_ingredients_by_recipe_id(recipe_id)
        res = []
        is_bad = False
        for ingred_id in ingreds:
            ingred = await retrieve_ingredient_by_id(ingred_id)
            if ingred.quantity is None:
                continue
            ingred_quantity = retrieve_quantity(ingred.quantity)
            # print(ingred_id)
            # print(ingred.name, ingred.quantity, quantity.quantity, quantity.uom)
            product_id = await get_best_product(ingred_id)
            product = await retrieve_product_by_id(product_id)
            prod_quantity = retrieve_quantity(product.size)
            # print(product.name, product.size, prod_quantity.quantity, prod_quantity.uom)
            prod_price = retrieve_price(product.price)
            # print(prod_price.price, prod_price.uom)
            # print()
            if ingred_quantity.uom == 'small':
                continue
            if ingred_quantity.quantity is None or ingred_quantity.uom is None or \
                prod_quantity.quantity is None or prod_quantity.uom is None or \
                prod_price.price is None or prod_price.uom is None or \
                not (ingred_quantity.uom == prod_quantity.uom == prod_price.uom):
                print(recipe_id)
                print('fail')
                print(ingred.name, ingred.quantity)
                print(ingred_quantity.quantity, ingred_quantity.uom)
                print(product.name, product.size)
                print(prod_quantity.quantity, prod_quantity.uom)
                print(prod_price.price, prod_price.uom)
                print()

                is_bad = True
                break
            res.append({
                'ingredient_id': ingred_id,
                'ingredient_name': ingred.name,
                'product_id': product_id,
                'product_name': product.name,
                'uom': ingred_quantity.uom,
                'ingredient_quantity': ingred_quantity.quantity,
                'product_quantity': prod_quantity.quantity,
                'product_price_per_uom': prod_price.price
            })
        if not is_bad:
            cnt += 1
            good_recipes.append({
                'recipe_id': recipe_id,
                'recipe': res,
            })
            print(recipe_id)
            for item in res:
                pprint(item)
            print()
    print(cnt)
    with open('good_recipes.txt', 'w') as f:
        json.dump(good_recipes, f)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
