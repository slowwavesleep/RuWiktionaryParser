import json
from pprint import pprint


PARSED_PATH = "tmp/parsed.json"

with open(PARSED_PATH) as file:
    test = json.load(file)

# pprint(test[1000:1200])
# print(len(test))

c = 0
for d in test:
    if d['morpho']['stems'] == dict():
        c += 1

print(c)