import asyncio

from core.domain import retrieve_product_by_id
from core.get_db_credentials import get_credentials
from core.model import db
from greedy_group_recepies.retrieve_quantity import retrieve_quantity


class Price:
    def __init__(self, price=None, uom=None):
        self.price = price
        self.uom = uom


def retrieve_price(price_str):
    if price_str is None:
        return Price(price=None, uom=None)
    price_str = price_str.removeprefix('(').removesuffix(')')
    if price_str.endswith('each'):
        quantity_str = 'each'
        price_str = price_str.removesuffix('each').strip()
    elif '/' in price_str:
        pos = price_str.find('/')
        price_str, quantity_str = price_str[:pos], price_str[pos + 1:]
    else:
        return Price(price=None, uom=None)
    quantity = retrieve_quantity(quantity_str)

    if quantity.quantity is None or quantity.uom is None:
        return Price(price=None, uom=None)

    if price_str.startswith('£'):
        price = float(price_str.removeprefix('£'))
    elif price_str.endswith('p'):
        price = float(price_str.removesuffix('p')) / 100
    else:
        return Price(price=None, uom=None)

    return Price(price=price / quantity.quantity, uom=quantity.uom)


# async def main():
#     credentials = get_credentials()
#     await db.set_bind(credentials)
#
#     for product_id in range(1, 20):
#         product = await retrieve_product_by_id(product_id)
#         prod_quantity = retrieve_quantity(product.size)
#         print(product.name, product.size, prod_quantity.quantity, prod_quantity.uom)
#         print()
#         prod_price = retrieve_price(product.price)
#         print(product.price, prod_price.price, prod_price.uom)
#         print()
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
