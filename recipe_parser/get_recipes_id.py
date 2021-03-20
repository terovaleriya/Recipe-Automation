import re

# хотим достать уникальные идентефикаторы для рецептов из url (так называются файлы с html рецептов)
with open('files/recipes_urls_A4.txt', 'r') as urls:
    matches = urls.read().split("\n")
    matches = set([re.findall('[^/]+(?=/$|$)', url)[0] for url in matches])

# запишем их в matches_*.txt
matches_file = open('files/matches_A4.txt', 'w')
for match in matches:
    matches_file.write(match + "\n")
matches_file.close()
