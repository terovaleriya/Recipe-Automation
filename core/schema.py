class Recipe:
    def __init__(self, recipe_id: int, title: str):
        self.recipe_id = recipe_id
        self.title = title

    def __str__(self) -> str:
        return str(self.recipe_id) + ", " + self.title
