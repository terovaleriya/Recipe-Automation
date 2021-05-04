import asyncio
import string
from random import shuffle, choice

from core.domain import get_matched_products_by_ingredient_id, get_unchecked_products_by_ingredient_id, \
    retrieve_product_by_id, create_link_matched_ingredients_products
from core.get_db_credentials import get_credentials
from core.model import db
from database_phantom.database import Database
from get_all_items.get_all_items import get_all_ingredients

SHUFFLE = True


def random_word(length):
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(length))


def instructions():
    print('Данные для проверки будут выводиться в следующем формате:')
    print('В первой строке будет отображаться ингредиент')
    print('В следующих строках будут находиться варианты продуктов')
    print('Введите номера продуктов (через пробел), который подходит под ингредиент')
    print('Если ничего не подходит, введите "no" (или просто "n")')
    print('Если хотите временно пропустить ингредиент, введите "skip" (или "s")')
    print('Если хотите посмотреть эти инструкции, введите "help" (или "h")')
    print('Если хотите закончить, введите "exit" (или "e")')
    input('Нажмите Enter чтобы продолжить ')
    print()


async def main():
    instructions()

    credentials = get_credentials()
    await db.set_bind(credentials)

    matching_filename = f'../database_phantom/backup/{random_word(8)}.txt'

    matching_db = Database()
    matching_db.create_table(['ingredientId', 'productId'])

    ingredients = await get_all_ingredients()
    if SHUFFLE:
        shuffle(ingredients)

    for ingred in ingredients:
        ingred_id = ingred.id
        if len(await get_matched_products_by_ingredient_id(ingred_id)) > 0:
            continue

        prod_ids = await get_unchecked_products_by_ingredient_id(ingred_id)
        products = [await retrieve_product_by_id(prod_id) for prod_id in prod_ids]

        print()
        print(ingred.raw_string)
        print()
        st = 1
        for num, prod in enumerate(products, start=st):
            print(f"{num}. {prod.name} {prod.size} {prod.image_url}")

        while True:
            command = input('> ').strip()
            if command == '':
                continue
            elif command.startswith('h'):
                instructions()
                continue
            elif command.startswith('e'):
                exit(0)
            elif command.startswith('s'):
                break
            elif command.startswith('n'):
                # await create_link_matched_ingredients_products(ingred_id, -1)
                matching_db.insert({
                    'ingredientId': ingred_id,
                    'productId': None,
                })
                matching_db.save_into_file(matching_filename)
                break
            else:
                items = command.split()
                if all(map(lambda x: x.isnumeric() and st <= int(x) < st + len(products), items)):
                    for x in items:
                        await create_link_matched_ingredients_products(ingred_id, products[int(x) - st].product_id)
                        matching_db.insert({
                            'ingredientId': ingred_id,
                            'productId': products[int(x) - st].product_id,
                        })
                    matching_db.save_into_file(matching_filename)
                    break
                else:
                    print('Введена неверная команда. Введите "help" или "h", чтобы узнать о доступных командах')
                    continue


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
