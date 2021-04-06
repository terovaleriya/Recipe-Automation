from database_phantom.database import Database
import json


def instructions():
    print('Данные для проверки будут выводиться в следующем формате:')
    print('В первой строке будет отображаться ингредиент')
    print('В следующих строках будут находиться варианты продуктов')
    print('Введите номер продукта, который подходит под ингредиент')
    print('Если ничего не подходит, введите "no" (или просто "n")')
    print('Если хотите временно пропустить ингредиент, введите "skip" (или "s")')
    print('Если хотите посмотреть эти инструкции, введите "help" (или "h")')
    print('Если хотите закончить, введите "exit" (или "e")')
    input('Нажмите Enter чтобы продолжить ')
    print()


matching_db = Database()
matching_db.load_from_file('../database_phantom/db_matching.txt')

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

    ingred_name = ingred_name_list[0]['name']

    print(ingred_name)
    print()
    for num, prod_name in enumerate(prod_name_list):
        print(f"{num}. {prod_name}")

    while True:
        command = input('> ').strip()
        if command == '':
            continue
        elif command.startswith('h'):
            instructions()
            continue
        elif command.startswith('e'):
            break
        elif command.startswith('s'):
            break
        elif command.startswith('n'):
            matching_db.insert_where_col_equals({
                'checked': True,
            }, 'ingredientId', ingred_id)
            matching_db.save_into_file('../database_phantom/db_matching.txt')
            break
        else:
            if command.isnumeric():
                command = int(command)
                if 0 <= command < len(prod_name_list):
                    matching_db.insert_where_col_equals({
                        'checked': True,
                        'answer': prod_ids[command],
                    }, 'ingredientId', ingred_id)
                    matching_db.save_into_file('../database_phantom/db_matching.txt')
                    print()
                    break
                else:
                    print('Введена неверная команда. Введите "help" или "h", чтобы узнать о доступных командах')
                    continue
            else:
                print('Введена неверная команда. Введите "help" или "h", чтобы узнать о доступных командах')
                continue
