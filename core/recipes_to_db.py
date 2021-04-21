import asyncio
import json
import logging
import os

from core.loaders import recipe_to_db
from core.model import db

from recipe_parser.recipe import Recipe


async def main():
    
    await db.set_bind("postgresql://racine@localhost/stepa")
    os.chdir("../recipe_parser/")
    json_folder = "recipes_json/"
    for f in os.listdir(json_folder):
        f = "recipes_json/" + f
        with open(f, "r") as file:
            json_str = file.readline()
            obj = json.loads(json_str)
            recipe = Recipe(**obj)
            await recipe_to_db(recipe)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
