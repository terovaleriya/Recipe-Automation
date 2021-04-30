from parse_ingredient.grammar import Grammar


def preprocess(raw_ingredient):
    bad_symbols = ['\x07', '\xa0', '•', '\t', '\u2028']
    for b in bad_symbols:
        raw_ingredient = raw_ingredient.replace(b, ' ')
    raw_ingredient = raw_ingredient.strip()
    return raw_ingredient


def is_end_of_word(text, pos):
    res = True
    res &= not text[pos].isspace()
    res &= pos == len(text) - 1 or text[pos + 1].isspace()
    return res


def parse_ingredient(raw_ingredient, grammar):
    raw_ingredient = preprocess(raw_ingredient)

    quantity = None
    raw_quantity = None
    ingredient = raw_ingredient.strip()
    comment = None

    comma_pos = raw_ingredient.find(',')
    if comma_pos != -1:
        comment = raw_ingredient[comma_pos + 1:].strip()
        raw_ingredient = raw_ingredient[:comma_pos].strip()
        ingredient = raw_ingredient

    grammar.clear_cache()
    for i in range(1, len(raw_ingredient) + 1):
        if not is_end_of_word(raw_ingredient, i - 1):
            continue
        parsed_quantity = grammar.parse(raw_ingredient[:i])
        if parsed_quantity != []:
            raw_quantity = raw_ingredient[:i].strip()
            quantity = parsed_quantity
            ingredient = raw_ingredient[i:].strip()

    return {
        'quantity': quantity,
        'raw_quantity': raw_quantity,
        'ingredient': ingredient,
        'comment': comment,
    }


if __name__ == "__main__":
    grammar = Grammar('grammar.txt')

    while True:
        s = input()
        res = parse_ingredient(s, grammar)
        print()
        print(s)
        print(f"quantity: {res['quantity']}")
        print(f"raw_quantity: {res['raw_quantity']}")
        print(f"ingredient: {res['ingredient']}")
        print(f"comment: {res['comment']}")
        print()
