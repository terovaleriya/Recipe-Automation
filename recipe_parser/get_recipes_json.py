import os

from recipe_parser.parser import get_json

# битые по каким-то причинам html, потом разберусь
skip = ["perfect-roast-potatoes0.A4.html", "martha-s-pumpkinroastalmondsoup.A4.html",
        "hundreds-and-thousandscake.A4.html"]

if not os.path.exists("recipes_json_A4_plane"):
    os.makedirs("recipes_json_A4_plane")

for file in os.listdir("recipes_html_A4"):
    print(file)
    if file not in skip:
        with open("recipes_json_A4_plane/" + file[:-5] + ".json", "w") as f:
            file = open("recipes_html_A4/" + file, "r")
            f.write(get_json(file, True))
            file.close()
