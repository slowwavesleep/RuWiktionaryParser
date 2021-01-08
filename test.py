import json
from pprint import pprint
from collections import Counter
import pathlib

PARSED_PATH = "tmp/articles.json"

templates = Counter()

with open("tmp/index2title.json") as file:
    index2title = json.load(file)

with open(PARSED_PATH) as file:
    for line in file:
        test = json.loads(line)
        if not test["is_proper"]:
            templates.update([test["morpho"]["template"]])

paths = list(pathlib.Path("tmp/templates").joinpath().glob("*"))

temps = []

for path in paths:
    temps.append(index2title[str(path.parts[-1])][7:])

found = set(temps).intersection(templates)
missing = []
for item in templates:
    if item not in found:
        missing.append(item)

# TODO
# Remove wiki comments, strip newline,
for item in missing:
    print(item)
# print(len(templates))
# pprint(templates.most_common())
