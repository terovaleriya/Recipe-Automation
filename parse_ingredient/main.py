from grammar import *


def split_ingredient(ingredient, grammar):
    result = ([None], ingredient)
    for i in range(1, len(ingredient) + 1):
        if i < len(ingredient) and ingredient[i] != ' ':
            continue
        res = grammar.parse(ingredient[:i])
        if res != []:
            result = (res, ingredient[i:].strip())
    return result


grammar = Grammar('grammar.txt')

while True:
    s = input()
    res, rem = split_ingredient(s, grammar)
    comma_pos = rem.find(',')
    if comma_pos == -1:
        ingred_name = rem
        ingred_comment = ""
    else:
        ingred_name = rem[:comma_pos].strip()
        ingred_comment = rem[comma_pos+1:].strip()
    print()
    print(s)
    print(res)
    print(ingred_name)
    print(ingred_comment)
    print()
