import requests
from time import sleep


def get_all_products(category):
    client = requests.session()
    all_products = []
    start = 0
    while True:
        url = 'https://www.waitrose.com/api/content-prod/v2/cms/publish/productcontent/browse/-1?clientType=WEB_APP'
        headers = {
            'authorization': 'Bearer unauthenticated',
            'cookie': 'wtr_cookie_consent=1; wtr_cookies_advertising=1; wtr_cookies_analytics=1; wtr_cookies_functional=1; _fbp=fb.1.1615198810734.1223567296; bm_sz=D4E5B5AAE85B8D8F480EBF69E7AA55CB~YAAQV1QXAn/tpBx4AQAAwhAnKAs4hnxDiN8xMzLlLQbagOt/5szqEjItfQ97Kva0o7QbKb4qDJ5ZTz/KuQRqqltRy8vVdBqJOb8U729eg7oN3mb5hVMz9zcBpHmg/hwesAAeTTz/i6V6mXNTzv3t3a0DbnqZSYemAWjwjEAeY6Xz1juI948IfR4nQVBwtR/Kx/Y=; ak_bmsc=DFA29313184973B53A8423ECCEA5032E02175457F4010000A8D04B60EC08997D~pl5sGM2nZsE4Ov1EgqOsWYhqvP8ZSF9kocElBUkQTl7z1P5NrprKugbsm6NT0qJuDBLo5TY0PwCDzrIDdldaNH2t6Te9bVzx8OXiBQXKN0kBlG0qT3Lpc5okEcy8aICXdnbv9ybW7Gw5RQkkbZ+bfOjNB1DfZ9/K4yvUsVoysfptKBOqJWRee30eNOT5ERC2fZzp1vEfa+rkCNJMjqwu+B9DU+ATtksNu2mEbVme6YPiLznGAqnpVU6Xc5Hz1c3HXD; bm_sv=7945D9CCAEFEA1D8FA0A98F6FBA190EE~wnb3QpNnclDuD50NYBEa/lCf36MYHGXdYLczxaU4Bg/RpFQf304v7RguRADR1ftdPCXrvYy7vFup4/mV903yJ0gWTxh6e57i8DaVtKt4PZ8+vbNxKg5lfrnuk+ABqs08Kd1q5jgSC37Npim1xi6E7XgZbkXGAI0uTO4WXmzt9bk=; _abck=05882B32CB19077F967C33B8C10493B5~-1~YAAQV1QXArbtpBx4AQAAjlAoKAUuUUKDNDdEoFI61k2za+pW4ca7PK5zMjZtsK2CBcHtjKd1k9tnFAAF1x9zyAnmf0JM0cfrxCU45RhJJEnNhEYx9teJJ7roy1vxXBOvSZpKAhuhyc8HKHm9ian6iM0xWMTwHiynicPs8KHzeWtFCYWuEx/QEA0mlMO0WMcD1SPq7NT4XUnQsEXSBeDHnzQPKNC5p/lrDeqwnpSZHHJZKetzGduPsk1LPGaDSfM51ochQj00zTOuaeQ/zIV2VOe/MLt/3Yq5xbWnAOvCeSbWjJa22/2jqMM73CyxttEWghyFcGTQBYZUJ8lQdTl+5+gUfIScPOJjHKvjF77ioGyJVP18bUV5LNPCMOVLt2IycknyB66WS3pmQutBjeQhKpdkjfIi3+dYNX3+~-1~-1~-1',
            'features': 'samosa,enAppleWallet',
            'origin': 'https://www.waitrose.com',
            'referer': 'https://www.waitrose.com/ecom/shop/browse/groceries',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
        }
        data = {
            "customerSearchRequest": {
                "queryParams": {
                    "size":128,
                    "category":category,
                    "filterTags":[],
                    "sortBy":"MOST_POPULAR",
                    "orderId":"0",
                    "start":start,
                }
            }
        }
        succ = False
        for it in range(5):
            sleep(0.5)
            try:
                r = client.post(url, headers=headers, json=data)
            except Exception:
                continue
            else:
                succ = True
                break
        if not succ:
            raise
        print(start, r.status_code)
        if r.status_code != 200:
            break
        if r.json()['productsInResultset'] == 0:
            break
        for new_product in r.json()['componentsAndProducts']:
            all_products.append(new_product['searchProduct'])
        print(r.json()['productsInResultset'])
        print()
        start += r.json()['productsInResultset']
    return all_products
