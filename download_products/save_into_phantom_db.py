import json
from database_phantom.database import Database

with open('all_products.txt') as f:
    all_products = json.load(f)

products_db = Database()
products_db.create_table(['id', 'name', 'size', 'image'])

for item in all_products:
    products_db.insert({
        'id': item['id'],
        'name': item['name'],
        'size': item.get('size', None),
        'image': None,
    })

products_db.save_into_file('../database_phantom/db_products.txt')
