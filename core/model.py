from gino import Gino
from sqlalchemy import String, ForeignKey, Column, Integer
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

from core import schema
from recipe_parser.recipe import Tag, Planning, Ingredient, Step


db: Gino = Gino()


# RecipesIngredients = Table('recipes_ingredients', Column('recipe' ,Integer, ForeignKey('ingredients.id')),
#                            Column('ingredient', Integer, ForeignKey('recipes.id')))
#
# IngredientsProducts = Table('ingredients_products', Column('product', Integer, ForeignKey('ingredients.id')),
#                             Column('ingredient', Integer, ForeignKey('products.id')))


class RecipesIngredients(db.Model):
    __tablename__ = 'recipes_ingredients'
    id = Column(Integer, primary_key=True)
    recipe = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    ingredient = Column(Integer, ForeignKey('recipes.id'), primary_key=True)


class RecipesTags(db.Model):
    __tablename__ = 'recipes_tags'
    id = Column(Integer, primary_key=True)
    recipe = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    tag = Column(Integer, ForeignKey('recipes.id'), primary_key=True)


class RecipesImages(db.Model):
    __tablename__ = 'recipes_images'
    id = Column(Integer, primary_key=True)
    recipe = Column(Integer, ForeignKey('images.id'), primary_key=True)
    image = Column(Integer, ForeignKey('recipes.id'), primary_key=True)


class RecipesPlanning(db.Model):
    __tablename__ = 'recipes_planning'
    id = Column(Integer, primary_key=True)
    recipe = Column(Integer, ForeignKey('planning.id'), primary_key=True)
    planning = Column(Integer, ForeignKey('recipes.id'), primary_key=True)


class RecipesNutrition(db.Model):
    __tablename__ = 'recipes_nutrition'
    id = Column(Integer, primary_key=True)
    recipe = Column(Integer, ForeignKey('nutrition.id'), primary_key=True)
    nutrition = Column(Integer, ForeignKey('recipes.id'), primary_key=True)


class IngredientsProducts(db.Model):
    __tablename__ = 'ingredients_products'
    id = Column(Integer, primary_key=True)
    product = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    ingredient = Column(Integer, ForeignKey('products.id'), primary_key=True)


class Recipes(db.Model):
    __tablename__ = 'recipes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, nullable=False, unique=True)

    ingredients = relationship("RecipesIngredients")
    tags = relationship("RecipesTags")
    images = relationship("RecipesImages")
    planing = relationship("RecipesPlanning")
    nutrition = relationship("RecipesNutrition")

    def as_schema(self) -> schema.Recipe:
        return schema.Recipe(recipe_id=self.id, title=self.title)


class Ingredients(db.Model):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(String)
    comment = Column(String)
    raw_string = Column(String)

    def as_schema(self) -> schema.Ingredient:
        return schema.Ingredient(ingredient_id=self.id, name=self.name, quantity=self.quantity, comment=self.comment,
                                 raw_string=self.raw_string)


class Tags(db.Model):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag = Column(String)

    def as_schema(self) -> schema.Tag:
        return schema.Tag(tag_id=self.id, tag=self.tag)


class Images(db.Model):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    image = Column(String)

    def as_schema(self) -> schema.Image:
        return schema.Image(image_id=self.id, image=self.image)


class Plan(db.Model):
    __tablename__ = "planning"
    id = Column(Integer, primary_key=True)
    prep_time = Column(String)
    cook_time = Column(String)
    total_time = Column(String)
    serves = Column(String)

    def as_schema(self) -> schema.Plan:
        return schema.Plan(planning_id=self.id, prep_time=self.prep_time, cook_time=self.cook_time,
                           total_time=self.total_time, serves=self.serves)


class Nutrition(db.Model):
    __tablename__ = "nutrition"
    id = Column(Integer, primary_key=True)
    energy = Column(String)
    fat = Column(String)
    saturated_fat = Column(String)
    carbohydrate = Column(String)
    sugars = Column(String)
    protein = Column(String)
    salt = Column(String)
    fibre = Column(String)

    def as_schema(self) -> schema.Nutrition:
        return schema.Nutrition(nutrition_id=self.id, energy=self.energy, fat=self.fat,
                                saturated_fat=self.saturated_fat, carbohydrate=self.carbohydrate, sugars=self.sugars,
                                protein=self.protein,
                                salt=self.salt, fibre=self.fibre)


class Products(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(String)
    image_url = Column(String)

    def as_schema(self) -> schema.Product:
        return schema.Product(product_id=self.id, name=self.name, size=self.size, image_url=self.image_url)


class Instructions(db.Model):
    __tablename__ = 'instructions'
    id = Column(Integer, primary_key=True)
    instruction = Column(String)

    def as_schema(self) -> schema.Instruction:
        return schema.Instruction(instruction_id=self.id, instruction=self.instruction)
