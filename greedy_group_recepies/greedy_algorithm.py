import asyncio
import json
from math import ceil
from typing import Dict

from core import model
from core.get_db_credentials import get_credentials
from core.model import Recipes, db


async def get_recipes_dict() -> Dict[int, str]:
    recipes_list = await model.Recipes.query.where(True).gino.all()
    return {i.id: i.title for i in recipes_list}


def calc_cost(recipes):
    cart = {}
    is_good = True
    for recipe in recipes:
        is_good = False
        for ingredient in recipe['recipe']:
            product_id = ingredient['product_id']
            if product_id not in cart:
                cart[product_id] = {
                    'uom': ingredient['uom'],
                    'product_quantity': ingredient['product_quantity'],
                    'product_price_per_uom': ingredient['product_price_per_uom'],
                    'needed_amount': 0.0,
                }
            else:
                is_good = True
            cart[product_id]['needed_amount'] += ingredient['ingredient_quantity']

    if not is_good:
        return 10 ** 20, 10 ** 20

    total_money = 0.0
    extra_money = 0.0
    for product_id, product in cart.items():
        cnt_packs = ceil(product['needed_amount'] / product['product_quantity'])
        extra_amount = cnt_packs * product['product_quantity'] - product['needed_amount']
        total_money += cnt_packs * product['product_quantity'] * product['product_price_per_uom']
        extra_money += extra_amount * product['product_price_per_uom']
    return total_money, extra_money


def choose_recipes(recipes, first_recipe_id, cnt_recipes):
    chosen_recipe_ids = {first_recipe_id}
    chosen_recipes = []
    for recipe in recipes:
        if recipe['recipe_id'] == first_recipe_id:
            chosen_recipes.append(recipe)

    while len(chosen_recipes) < cnt_recipes:
        best_cost = 10 ** 20
        best_recipe = None

        for new_recipe in recipes:
            if new_recipe['recipe_id'] in chosen_recipe_ids:
                continue
            total_money, extra_money = calc_cost(chosen_recipes + [new_recipe])
            if extra_money < best_cost:
                best_cost = extra_money
                best_recipe = new_recipe

        # print(best_cost)
        # print(best_recipe)
        # print()
        chosen_recipe_ids.add(best_recipe['recipe_id'])
        chosen_recipes.append(best_recipe)

    return chosen_recipes


async def main():
    credentials = get_credentials()
    await db.set_bind(credentials)

    k = 4
    with open('good_recipes.txt') as f:
        recipes = json.load(f)

    recipes_dict = await get_recipes_dict()

    for first_recipe in recipes:
        chosen_recipes = choose_recipes(recipes, first_recipe['recipe_id'], k)
        total_money, extra_money = calc_cost(chosen_recipes)

        print(f'total money: {total_money}£, extra money: {extra_money}£')
        for recipe in chosen_recipes:
            print(recipes_dict[recipe['recipe_id']])
        print()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
