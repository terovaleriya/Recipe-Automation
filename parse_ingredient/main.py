# TODO разобраться с large/medium/small
# TODO наверное разбираться в этом не тут

from grammar import Grammar
from ingredient_parser import parse_ingredient
from collections import Counter
from known_answers import Answers
from database_phantom.database import Database


def get_all_ingredients():
    with open("../recipe_parser/files/ingredients.txt") as f:
        for line in f:
            line = line.strip()
            if line != '':
                yield line


def get_bad_symbols(all_ingredients):
    bad_symbols = (c
                   for ingredient in all_ingredients
                   for c in ingredient
                   if not (32 <= ord(c) <= 126))

    c = Counter(bad_symbols)
    print(c)


def compare_answers(old_answer, new_answer):
    res = True
    res &= old_answer['raw_quantity'] == new_answer['raw_quantity']
    res &= old_answer['ingredient'] == new_answer['ingredient']
    res &= old_answer['comment'] == new_answer['comment']
    return res


def print_parsed_ingredient(res):
    print(ingredient)
    print(f"quantity: {res['quantity']}")
    print(f"raw_quantity: {res['raw_quantity']}")
    print(f"ingredient: {res['ingredient']}")
    print(f"comment: {res['comment']}")
    print()

grammar = Grammar('grammar.txt')

all_ingredients = get_all_ingredients()

known_answers = Answers("known_answers.txt")
skip_answers = Answers("skip_answers.txt")

db_ingredients = Database()
db_ingredients.create_table(['id', 'name', 'quantity', 'comment', 'raw'])

SKIP_ANSWERS = True

next_id = 0
for ingredient in all_ingredients:
    print(ingredient)
    new_answer = parse_ingredient(ingredient, grammar)
    db_ingredients.insert({
        'id': next_id,
        'name': new_answer['ingredient'],
        'quantity': new_answer['raw_quantity'],
        'comment': new_answer['comment'],
        'raw': ingredient,
    })
    next_id += 1
    continue

    if SKIP_ANSWERS and skip_answers.has_answer(ingredient):
        continue

    new_answer = parse_ingredient(ingredient, grammar)

    if known_answers.has_answer(ingredient):
        old_answer = known_answers.get_answer(ingredient)
        if compare_answers(old_answer, new_answer):
            pass
        else:
            print("FAILED")
            print("old answer")
            print_parsed_ingredient(old_answer)
            print("new answer")
            print_parsed_ingredient(new_answer)
            action = input("Select action: u - update, s - skip, other - skip ")
            if action.startswith('u'):
                known_answers.add_answer(ingredient, new_answer)
            print()
    else:
        print("new answer")
        print_parsed_ingredient(new_answer)
        action = input("Select action: a - add answer, d - skip always, s - skip, other - skip ")
        if action.startswith('a'):
            known_answers.add_answer(ingredient, new_answer)
        elif action.startswith('d'):
            skip_answers.add_answer(ingredient, None)
        print()

db_ingredients.save_into_file('../database_phantom/db_ingredients.txt')
