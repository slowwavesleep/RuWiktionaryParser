import json

from constants import WRITE_PATHS

# question marks at the end of templates are probably safe to remove in articles
# however, it is not clear what is their purpose exactly

# TODO generate word forms after processing all available templates
from src.utils.etc import determine_pos, basic_filter, read_redirects, replace_redirect, is_usable_template,\
    basic_json_read

redirects = read_redirects(WRITE_PATHS["template_redirect"])

full_noun_templates = []
broken_noun_templates = []

noun_templates = basic_json_read(WRITE_PATHS["template"])

for template in noun_templates:
    if determine_pos(template, page_type="template") == "noun":
        if is_usable_template(template):
            full_noun_templates.append(template["title"])
        else:
            broken_noun_templates.append(template["title"])


noun_article_templates = []
with open(WRITE_PATHS["article"]) as file:
    for line in file:
        article = json.loads(line)
        pos = determine_pos(article)
        if determine_pos(article) == "noun" and basic_filter(article):
            noun_article_templates.append(replace_redirect(article, redirects)["morpho"]["template"])

noun_article_templates = set(noun_article_templates)
full_noun_templates = set(full_noun_templates)
broken_noun_templates = set(broken_noun_templates)


missing = noun_article_templates - (broken_noun_templates | full_noun_templates)

print(len(missing))
print(len(full_noun_templates))
print(len(broken_noun_templates))
