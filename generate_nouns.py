from typing import List, Dict
import json

from src.generation import segment_stem
from src.segmentation import clean_segments
from src.utils.etc import determine_pos, basic_json_read, read_redirects, replace_redirect, basic_filter
from constants import WRITE_PATHS, INVARIABLE_POS, IGNORE_POS, SEGMENT_SEPARATOR


def process_article(article, temps, *, sep: str = SEGMENT_SEPARATOR):
    title = article["title"]
    stems = article["morpho"]["stems"]
    pos = determine_pos(article)
    if pos in IGNORE_POS:
        return {}
    if pos in INVARIABLE_POS:
        segmented_forms = {"lemma": clean_segments(article["segments"])}
        return segmented_forms
    # nouns with one stem
    if pos == "noun" and len(stems) == 1:
        segments = clean_segments(article["segments"])
        stem = list(stems.values())[0]
        print(title)
        print(segment_stem(stem, segments))
    elif len(stems) > 1:
        pass


def map_templates(temps: List[dict]) -> Dict[str, dict]:
    result = {}
    for t in temps:
        result[t["title"]] = t
    return result


# TODO refactor paths
articles = basic_json_read("tmp/processed/articles.jsonl")
templates = map_templates(basic_json_read("tmp/processed/templates.jsonl"))
redirects = read_redirects(WRITE_PATHS["template_redirect"])

articles = [replace_redirect(article, redirects) for article in articles]

# the process of attaching corresponding stems to their endings
with open("result/processed_articles.jsonl", "w") as file:
    for article in articles:
        if basic_filter(article) and determine_pos(article) == "noun":
            article_template = article["morpho"]["template"]
            if article_template in templates.keys():
                stems: dict = article["processed_stems"]
                if stems:
                    template: dict = templates[article_template]
                    form_templates = template["template"]
                    generated_forms: dict = dict()
                    for form, temp in form_templates.items():
                        for name, value in stems.items():
                            if name in temp.keys():
                                generated_forms[form] = f"{value}{temp[name]}"
                    article["generated_forms"] = generated_forms
                    file.write(json.dumps(article, ensure_ascii=False) + "\n")
