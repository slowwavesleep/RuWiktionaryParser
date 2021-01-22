import json
from pprint import pprint

import wikitextparser as wtp

from constants import WRITE_PATHS

# question marks at the end of templates are probably safe to remove in articles
# however, it is not clear what is their purpose exactly

# TODO generate word forms after processing all available templates
from src.utils.etc import determine_pos

redirects = {}
with open(WRITE_PATHS["template_redirect"]) as file:
    for line in file:
        redirect = json.loads(line)
        redirects[redirect["title"]] = redirect["redirect_title"]

full_templates = []
broken_templates = []
with open(WRITE_PATHS["template"]) as file:
    for line in file:
        template = json.loads(line)
        if "сущ" in template["title"] and template["template"]:
            if "nom-sg" in template["template"]:
                full_templates.append(template["title"])
            else:
                broken_templates.append(template["title"])


temps = []
with open(WRITE_PATHS["article"]) as file:
    for line in file:
        article = json.loads(line)
        pos = determine_pos(article)
        if not pos:
            print(article)
        if "сущ" in article["morpho"]["template"] and not article["is_proper"] and not article["is_obscene"]:
            if article["morpho"]["template"] in redirects:
                temps.append(redirects[article["morpho"]["template"]])
            else:
                temps.append(article["morpho"]["template"])

temps = set(temps)
full_templates = set(full_templates)
broken_templates = set(broken_templates)


missing = temps - (broken_templates | full_templates)

print(len(missing))
print(len(full_templates))
print(len(broken_templates))