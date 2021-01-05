from typing import Dict
from yaml import safe_load


# DUMP_PATH: str = "data/ruwiktionary-20201201-pages-articles.xml.bz2"
# TMP_PATH: str = "tmp/"
# WIKI_NS: str = "{http://www.mediawiki.org/xml/export-0.10/}"


with open("config.yml") as file:
    config = safe_load(file)

DUMP_PATH = config["dump_path"]
TMP_PATH = config["tmp_path"]
WIKI_NS = config["wiki_ns"]

TAGS: Dict[str, str] = {
    "text": WIKI_NS + "revision//" + WIKI_NS + "text",
    "title": WIKI_NS + "title",
    "redirect": WIKI_NS + "redirect",
    "namespace": WIKI_NS + "ns",
    "id": WIKI_NS + "id"
}

ARTICLE_NAMESPACE: str = "0"
TEMPLATE_NAMESPACE: str = "10"

PROCESS_ARTICLES: bool = True
PROCESS_TEMPLATES: bool = True
