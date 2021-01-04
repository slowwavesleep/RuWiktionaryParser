from typing import Dict

DUMP_PATH: str = "data/ruwiktionary-20201201-pages-articles.xml.bz2"
WIKI_NS: str = "{http://www.mediawiki.org/xml/export-0.10/}"

TAGS: Dict[str, str] = {
    "text": WIKI_NS + "revision//" + WIKI_NS + "text",
    "title": WIKI_NS + "title",
    "redirect": WIKI_NS + "redirect",
    "namespace": WIKI_NS + "ns",
    "id": WIKI_NS + "id"
}

ARTICLE_NAMESPACE: str = "0"
TEMPLATE_NAMESPACE: str = "10"

