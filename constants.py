from typing import Dict, List

# TODO Move to config yaml
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

INVARIABLE_POS = [
    "adv",
    "деепр"
]

POS_MAP = {
    "сущ": "noun",
    "прил": "adj",
    "гл": "verb",
    "adv": "adv"
}

CASE_MAP = {
    "Им.": "nom",
    "Р.": "gen",
    "Д.": "dat",
    "В.": "acc",
    "Тв.": "gen",
    "Пр.": "prp"
}

NUMBER_MAP = {
    "ед. ч.": "sg",
    "мн. ч.": "pl"
}

GENDER_MAP = {
    "муж. р.": "m",
    "ср. р.": "n",
    "жен. р.": "f"
}


ARTICLE_NAMESPACE: str = "0"
TEMPLATE_NAMESPACE: str = "10"
USER_AGENT = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/74.0.3729.169 Safari/537.36'}