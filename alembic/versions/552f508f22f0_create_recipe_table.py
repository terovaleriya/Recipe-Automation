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
                    sa.Column('title', String))

    op.create_table('ingredients',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('name', String),
                    sa.Column('quantity', String),
                    sa.Column('comment', String),
                    sa.Column('raw_string', String))

    op.create_table('products',
                    sa.Column('id', INTEGER, autoincrement=True, primary_key=True),
                    sa.Column('name', String),
                    sa.Column('size', String),
                    sa.Column('image_url', String))

    op.create_table('recipes_ingredients',
                    sa.Column('recipe', INTEGER, ForeignKey('ingredients.id')),
                    sa.Column('ingredient', INTEGER, ForeignKey('recipes.id')))

    op.create_table('ingredients_products',
                    sa.Column('product', INTEGER, ForeignKey('ingredients.id')),
                    sa.Column('ingredient', INTEGER, ForeignKey('products.id')))



    


def downgrade():
    op.drop_table('recipe')
