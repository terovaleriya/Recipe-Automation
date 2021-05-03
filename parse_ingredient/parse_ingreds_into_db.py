import asyncio

from core.domain import update_ingredient_by_id
from core.get_db_credentials import get_credentials
from core.model import db
from get_all_items.get_all_items import get_all_ingredients
from parse_ingredient.grammar import Grammar
from parse_ingredient.ingredient_parser import parse_ingredient


async def main():
    credentials = get_credentials()
    await db.set_bind(credentials)

    grammar = Grammar('grammar.txt')

    ingredients = await get_all_ingredients()
    for item in ingredients:
        print(item['raw_string'])
        parsed_item = parse_ingredient(item['raw_string'], grammar)
        await update_ingredient_by_id(
            ingredient_id=item['id'],
            name=parsed_item['ingredient'],
            quantity=parsed_item['raw_quantity'],
            comment=parsed_item['comment']
        )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
