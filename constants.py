from typing import Dict, List

WRITE_PATHS: Dict[str, str] = {
    "template": "tmp/templates.json",
    "article": "tmp/articles.json",
    "template_redirect": "tmp/template_redirects.json"
}

SPECIAL_TEMPLATES: List[str] = [
    "сущ-ru"
]

BROKEN_ARTICLES: List[str] = [
    "ханьжа"
]
ARTICLE_NAMESPACE: str = "0"
TEMPLATE_NAMESPACE: str = "10"
