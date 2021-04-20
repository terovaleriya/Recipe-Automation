"""create recipe table

Revision ID: 552f508f22f0
Revises: 
Create Date: 2021-04-07 00:25:50.019385

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import INTEGER, String, ForeignKey

# revision identifiers, used by Alembic.
revision = '552f508f22f0'
down_revision = None
branch_labels = None
depends_on = None


# У нас есть четыре таблицы:
#   -- Рецепты
#   -- Ингридиенты
#   -- Продукты из магазина
#         id :: String
#         name :: String
#         size :: String
#         image_url :: String
#   -- Таблица матчинга ингридиенов с продуктами
#         id ингредиента (число, которое из таблицы с ингредиентами)
#         список длины <= 5 из id продуктов (строки, которые из таблицы с продуктами)
#         не знаю как правильно в базе хранить списки. Наверное попросить json перевести список в строку. Не знаешь способа получше?
#         булевское значение, которое означает, проверил ли человек этот matching :: Bool
#         id продукта (строка, из таблицы с продуктами), который выбрал человек (или None)


def upgrade():
    op.create_table('recipes',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('title', String, nullable=False, unique=True))

    op.create_table('ingredients',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('name', String),
                    sa.Column('quantity', String),
                    sa.Column('comment', String),
                    sa.Column('raw_string', String))

    op.create_table('instructions',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('instruction', String))

    op.create_table('products',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('name', String),
                    sa.Column('size', String),
                    sa.Column('image_url', String))

    op.create_table('tags',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('tag', String))

    op.create_table('images',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('image', String))

    op.create_table('planning',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('prep_time', String),
                    sa.Column('cook_time', String), sa.Column('total_time', String), sa.Column('serves', String))

    op.create_table('nutrition',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('energy', String),
                    sa.Column('fat', String), sa.Column('saturated_fat', String), sa.Column('carbohydrate', String),
                    sa.Column('sugars', String), sa.Column('protein', String), sa.Column('salt', String),
                    sa.Column('fibre', String))

    op.create_table('recipes_ingredients',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('recipe', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE")),
                    sa.Column('ingredient', INTEGER, ForeignKey('ingredients.id', ondelete="CASCADE")))

    op.create_table('ingredients_products',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('product', INTEGER, ForeignKey('products.id', ondelete="CASCADE")),
                    sa.Column('ingredient', INTEGER, ForeignKey('ingredients.id', ondelete="CASCADE")))

    op.create_table('recipes_instructions',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('recipe', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE")),
                    sa.Column('instruction', INTEGER, ForeignKey('instructions.id', ondelete="CASCADE")))

    op.create_table('recipes_tags',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('recipe', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE")),
                    sa.Column('tag', INTEGER, ForeignKey('tags.id', ondelete="CASCADE")))

    op.create_table('recipes_images',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('recipe', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE")),
                    sa.Column('image', INTEGER, ForeignKey('images.id', ondelete="CASCADE")))

    op.create_table('recipes_planning',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('recipe', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE")),
                    sa.Column('planning', INTEGER, ForeignKey('planning.id', ondelete="CASCADE")))

    op.create_table('recipes_nutrition',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('recipe', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE")),
                    sa.Column('nutrition', INTEGER, ForeignKey('nutrition.id', ondelete="CASCADE")))


def downgrade():
    op.drop_table('recipe')
