from database_phantom.database import Database
import json


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


matching_filename = '../database_phantom/db_matching_v2.txt'

matching_db = Database()
matching_db.load_from_file(matching_filename)

ingredients_db = Database()
ingredients_db.load_from_file('../database_phantom/db_ingredients.txt')

products_db = Database()
products_db.load_from_file('../database_phantom/db_products.txt')


instructions()

matching_to_check = matching_db.select_where_col_equals('checked', False)
for match in matching_to_check:
    ingred_id = match['ingredientId']
    prod_ids = json.loads(match['productIds'])

    ingred_name_list = ingredients_db.select_where_col_equals('id', ingred_id)
    prod_name_list = products_db.select_where_col_in_list('id', prod_ids)

    if len(prod_ids) != len(prod_name_list):
        continue
    if len(ingred_name_list) != 1:
        continue

    raw_ingred_name = ingred_name_list[0]['raw']

    print(raw_ingred_name)
    print()
    for num, prod_name in enumerate(prod_name_list, start=1):
        print(f"{num}. {prod_name}")

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
            matching_db.insert_where_col_equals({
                'checked': True,
            }, 'ingredientId', ingred_id)
            matching_db.save_into_file(matching_filename)
            break
        else:
            items = command.split()
            if all(map(lambda x: x.isnumeric() and 0 <= int(x) < len(prod_name_list), items)):
                pos = [int(x) for x in items]
                matching_db.insert_where_col_equals({
                    'checked': True,
                    'answer': json.dumps([prod_ids[p - 1] for p in pos]),
                }, 'ingredientId', ingred_id)
                matching_db.save_into_file(matching_filename)
                print()
                break
            else:
                print('Введена неверная команда. Введите "help" или "h", чтобы узнать о доступных командах')
                continue
