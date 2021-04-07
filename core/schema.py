class Recipe:
    def __init__(self, recipe_id: int, title: str):
        self.recipe_id = recipe_id
        self.title = title

    def __str__(self) -> str:
        return str(self.recipe_id) + ", " + self.title


class Ingredient:
    def __init__(self, ingredient_id: int, name: str, quantity: str, comment: str, raw_string: str):
        self.ingredient_id = ingredient_id
        self.name = name
        self.quantity = quantity
        self.comment = comment
        self.raw_string = raw_string

    def __str__(self) -> str:
        return str(self.ingredient_id) + ", " + self.name + ", " + \
               self.quantity + ", " + self.comment + ", " + self.raw_string


class Product:
    def __init__(self, product_id: int, name: str, size: str, image_url: str):
        self.product_id = product_id
        self.name = name
        self.size = size
        self.image_url = image_url

    def __str__(self) -> str:
        return str(self.product_id) + ", " + self.name + ", " + self.size + ", " + self.image_url
