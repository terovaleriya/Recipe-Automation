from typing import List


class Tag:
    def __init__(self, tag: str):
        self.tag = tag

    def __repr__(self):
        return self.tag


class Ingredient:
    def __init__(self, item: str,
                 # amount: float, units: str
                 ):
        self.item = item
        # self.amount = amount
        # self.measure = units

    def __repr__(self):
        return self.item \
            # + ": "+ str(self.amount) + self.measure


class Step:
    def __init__(self, step: str):
        self.step = step

    def __repr__(self):
        return self.step


# class Nutrition:
#     def __init__(self, ...):
#         self.energy = energy
#         self.fat = fat
#         self.saturated_fat = saturated_fat
#         self.carbohydrate = carbohydrate
#         self.sugars = sugars
#         self.protein = protein
#         self.salt = salt
#         self.fibre = fibre


class Planing:
    def __init__(self, prep_time: str, cook_time: str, total_time: str, serves: str):
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.total_time = total_time
        self.serves = serves

    def __str__(self):
        return "Preparation time: " + self.prep_time + "\n" + "Cooking time: " + self.cook_time + "\n" + "Total time: " + self.total_time + "\n" + "Serves: " + self.serves


class Recipe:
    def __init__(self, title: str, tags: List[Tag], planning: Planing, ingredients: List[Ingredient],
                 instructions: List[Step], nutrition: dict, images_url: List[str]):
        self.title = title
        self.tags = tags
        self.planning = planning
        self.nutrition = nutrition
        self.ingredients = ingredients
        self.instructions = instructions
        self.nutrition = nutrition
        self.images_url = images_url

    def __str__(self):
        recipe = "\n" + self.title + "\n\n"
        print(self.tags)
        if self.tags:
            recipe += '\n'.join([str(x) for i, x in enumerate(self.tags)]) + "\n\n"
        recipe += str(self.planning) + "\n\n"
        recipe += '\n'.join([str(i).strip() for i in self.ingredients]) + "\n\n"
        recipe += '\n'.join([str(x) for x in self.instructions]) + "\n\n"
        recipe += '\n'.join([El + ": " + x for El, x in zip(self.nutrition.keys(), self.nutrition.values())]) + "\n\n"
        recipe += '\n'.join([str(i) for i in self.images_url])
        return recipe
