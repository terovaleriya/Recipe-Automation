import re

# файл с url
url_file = "files/recipes_urls_A4.txt"
# куда пишем id
id_file = "files/matches_A4.txt"

# хотим достать уникальные идентефикаторы для рецептов из url (так называются файлы с html рецептов)
with open(url_file, 'r') as urls:
    matches = urls.read().split("\n")
    matches = set([re.findall('[^/]+(?=/$|$)', url)[0] for url in matches])

# запишем их в matches_*.txt
matches_file = open(id_file, 'w')
for match in matches:
    matches_file.write(match + "\n")
matches_file.close()
