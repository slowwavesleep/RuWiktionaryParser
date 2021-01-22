import json

import wikitextparser as wtp

from constants import WRITE_PATHS

# question marks at the end of templates are probably safe to remove in articles
# however th
from src.utils.wiki import remove_no_include

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


# with open(WRITE_PATHS["article"]) as file:
#     for line in file:
#         article = json.loads(line)
#         if article["morpho"]["template"] == "сущ ru f a 6a÷":
#             print(article)

# temps = []
# with open(WRITE_PATHS["article"]) as file:
#     for line in file:
#         article = json.loads(line)
#         if "сущ" in article["morpho"]["template"] and not article["is_proper"]:
#             if article["morpho"]["template"] in redirects:
#                 temps.append(redirects[article["morpho"]["template"]])
#             else:
#                 temps.append(article["morpho"]["template"])
#
#
# with open(WRITE_PATHS["template"]) as file:
#     for line in file:
#         article = json.loads(line)
#         if article["id"] == 10567:
#             print(article)

wiki_text = '{{inflection сущ ru<noinclude>|шаблон-кат=1</noinclude>\n|form={{{form|}}}\n|case={{{case|}}}\n|nom-sg={{{основа}}}а́\n|nom-pl={{{основа}}}и́\n|gen-sg={{{основа}}}и́\n|gen-pl={{{основа1}}}\n|dat-sg={{{основа}}}е́\n|dat-pl={{{основа}}}а́м\n|acc-sg={{{основа}}}у́\n|acc-pl={{{основа1}}}\n|ins-sg={{{основа}}}о́й\n|ins-sg2={{{основа}}}о́ю\n|ins-pl={{{основа}}}а́ми\n|prp-sg={{{основа}}}е́\n|prp-pl={{{основа}}}а́х\n|loc-sg={{{М|}}} \n|voc-sg={{{З|}}} \n|prt-sg={{{Р|}}}\n|hide-text={{{hide-text|}}}\n|слоги={{{слоги|}}}\n|дореф={{{дореф|}}}\n|Сч={{{Сч|}}}\n|st={{{st|}}}\n|pt={{{pt|}}}\n|затрудн={{{затрудн|}}}\n|коммент={{{коммент|}}}\n|зачин={{{зачин|}}}\n|клитика={{{клитика|}}}\n|кат=одуш\n|род={{{род|{{#switch:{{{можо}}}|мо=муж|можо=общ|жен}}}}}\n|скл=1\n|зализняк=3b\n}}'
# wiki_text ='{{inflection сущ ru<noinclude>|шаблон-кат=1</noinclude>\n|form={{{form|}}}\n|case={{{case|}}}\n|nom-sg={{{основа}}}а́\n|nom-pl={{{основа}}}и́\n|gen-sg={{{основа}}}и́\n|gen-pl={{{основа1}}}\n|dat-sg={{{основа}}}е́\n|dat-pl={{{основа}}}а́м\n|acc-sg={{{основа}}}у́\n|acc-pl={{{основа1}}}\n|ins-sg={{{основа}}}о́й\n|ins-sg2={{{основа}}}о́ю\n|ins-pl={{{основа}}}а́ми\n|prp-sg={{{основа}}}е́\n|prp-pl={{{основа}}}а́х\n|loc-sg={{{М|}}} \n|voc-sg={{{З|}}} \n|prt-sg={{{Р|}}}\n|hide-text={{{hide-text|}}}\n|слоги={{{слоги|}}}\n|дореф={{{дореф|}}}\n|Сч={{{Сч|}}}\n|st={{{st|}}}\n|pt={{{pt|}}}\n|затрудн={{{затрудн|}}}\n|коммент={{{коммент|}}}\n|зачин={{{зачин|}}}\n|клитика={{{клитика|}}}\n|кат=одуш\n|род={{{род|{{#switch:{{{можо}}}|мо=муж|можо=общ|жен}}}}}\n|скл=1\n|зализняк=3b\n}}'
# print(remove_no_include(wiki_text))

print(wtp.parse(remove_no_include(wiki_text)))
