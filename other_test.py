from collections import Counter
import json

articles_path = "tmp/articles.json"
templates_path = "tmp/templates.json"
template_redirects_path = "tmp/template_redirects.json"

article_templates = Counter()

with open(articles_path) as file:
    for line in file:
        test = json.loads(line)
        if not test["is_proper"]:
            article_templates.update([test["morpho"]["template"]])

templates = []
with open(templates_path) as file:
    for line in file:
        test = json.loads(line)
        templates.append(test["title"])
templates = set(templates)

template_redirects = []
with open(template_redirects_path) as file:
    for line in file:
        test = json.loads(line)
        template_redirects.append(test["title"])

template_redirects = set(template_redirects)

all_templates = templates | template_redirects

for temp in article_templates:
    if temp not in all_templates:
        print(temp)