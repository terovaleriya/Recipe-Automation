from sqlalchemy import String, ForeignKey, Column, Integer
from sqlalchemy.orm import relationship

from gino import Gino

from core import schema

db: Gino = Gino()


# RecipesIngredients = Table('recipes_ingredients', Column('recipe' ,Integer, ForeignKey('ingredients.id')),
#                            Column('ingredient', Integer, ForeignKey('recipes.id')))
#
# IngredientsProducts = Table('ingredients_products', Column('product', Integer, ForeignKey('ingredients.id')),
#                             Column('ingredient', Integer, ForeignKey('products.id')))


class RecipesIngredients(db.Model):
    __tablename__ = 'recipes_ingredients'

    recipe = Column(Integer, ForeignKey('ingredients.id'))
    ingredient = Column(Integer, ForeignKey('recipes.id'))


class IngredientsProducts(db.Model):
    __tablename__ = 'ingredients_products'
    product = Column(Integer, ForeignKey('ingredients.id'))
    ingredient = Column(Integer, ForeignKey('products.id'))


class Recipes(db.Model):
    __tablename__ = 'recipes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)

    def as_schema(self) -> schema.Recipe:
        return schema.Recipe(recipe_id=self.id, title=self.title)


class Ingredients(db.Model):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    products = relationship("Product", secondary=IngredientsProducts, backref="ingredients")
    recipes = relationship("Recipe", secondary=RecipesIngredients, backref="ingredients")
    name = Column(String)
    quantity = Column(String)
    comment = Column(String)
    raw_string = Column(String)

    def as_schema(self) -> schema.Ingredient:
        return schema.Ingredient(ingredient_id=self.id, name=self.name, quantity=self.quantity, comment=self.comment,
                                 raw_string=self.raw_string)


class Products(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(String)
    image_url = Column(String)

    def as_schema(self) -> schema.Product:
        return schema.Product(product_id=self.id, name=self.name, size=self.size, image_url=self.image_url)
