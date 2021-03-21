from JsonTemplate import *
from DownloadFromWaitrose import *
import json

reload = False

if reload:
    raw_all_products = get_all_products("10051")
    with open('raw_all_products.txt', 'w') as f:
        json.dump(raw_all_products, f)
else:
    with open('raw_all_products.txt') as f:
        raw_all_products = json.load(f)

template = JsonTemplate('product_template.txt')
all_products = list(map(template.filter_json, raw_all_products))
with open('all_products.txt', 'w') as f:
    json.dump(all_products, f)
