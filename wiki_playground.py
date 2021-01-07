import wikitextparser as wtp
import pathlib
from tqdm import tqdm
import json
from pprint import pprint

from src.utils.wiki import find_ru_section, parse_ru_section
from src.data import Article, Template

paths = list(pathlib.Path("tmp/articles/other").joinpath().glob("*"))
total = len(paths)


with open("tmp/index2title.json") as file:
    index2title = json.load(file)

PARSED_PATH = "tmp/parsed.json"

parsed = []
for path in tqdm(paths, total=total):
    with open(path) as file:
        article_id = path.parts[-1]
        article_title = index2title[article_id]
        data = file.read()
        data = wtp.parse(data)
        section = find_ru_section(data)

        if section:
            parsed_section = parse_ru_section(section)
            if parsed_section:
                parsed_section["title"] = article_title
                parsed_section["id"] = article_id
                parsed.append(parsed_section)
        else:
            pass


with open(PARSED_PATH, "w") as file:
    json.dump(parsed, file, indent=4)

with open(PARSED_PATH) as file:
    test = json.load(file)

print(test)

