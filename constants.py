from typing import Dict, List

# TODO Move to config yaml
WRITE_PATHS: Dict[str, str] = {
    "template": "tmp/templates.jsonl",
    "article": "tmp/articles.jsonl",
    "template_redirect": "tmp/template_redirects.jsonl"
}

PROCESSED_DIR = "tmp/processed/"

SEGMENT_SEPARATOR: str = "|"

SPECIAL_TEMPLATES: List[str] = [
    "сущ-ru"
]

BROKEN_ARTICLES: List[str] = [
    "ханьжа"
]

INVARIABLE_POS: List[str] = [
    "adv",
    "ger"
]

IGNORE_POS: List[str] = [
    "intrj",
    "conj",
    "fam"
]

POS_MAP: Dict[str, str] = {
    "сущ": "noun",
    # "падежи": "noun",
    "прил": "adj",
    "гл": "verb",
    "прич": "participle",
    "деепр": "ger",
    "adv": "adv",
    "interj": "intrj",
    "part": "particle",
    "мест": "padj",  # possessive
    "predic": "pred",
    "conj": "conj",
    "числ": "num",
    "prep": "prep",
    # not really parts of speech, it's just for consistency's sake
    "Фам": "fam",
    "собств.": "prop",  # proper name
    "abbrev": "abbr",
    "onomatop": "ono",
    "intro": "par",  # parenthesis
    "не так": "broken",  # ungrammatical, ignore this
}

CASE_MAP: Dict[str, str] = {
    "Им.": "nom",
    "Р.": "gen",
    "Д.": "dat",
    "В.": "acc",
    "Тв.": "ins",
    "Пр.": "prp"
}

CASE_PRONOUN_MAP: Dict[str, str] = {
    "Кто/что? (ед)": "nom-sg",
    "Кто/что? (мн)": "nom-pl",
    "Нет кого/чего? (ед)": "gen-sg",
    "Нет кого/чего? (мн)": "gen-pl",
    "Кому/чему? (ед)": "dat-sg",
    "Кому/чему? (мн)": "gat-pl",
    "Кого/что? (ед)": "acc-sg",
    "Кого/что? (мн)": "acc-pl",
    "Кем/чем? (ед)": "ins-sg",
    "Кем/чем? (мн)": "ins-pl",
    "О ком/чём? (ед)": "prp-sg",
    "О ком/чём? (мн)": "prp-pl"
}

NUMBER_MAP: Dict[str, str] = {
    "ед. ч.": "sg",
    "мн. ч.": "pl"
}

GENDER_MAP: Dict[str, str] = {
    "муж. р.": "m",
    "ср. р.": "n",
    "жен. р.": "f"
}

VERB_FORM_MAP = {
    "Я": "sfp-present",
    "Я (прош.)": "sg-fp-past",
    "Мы": "pl-fp-present",
    "Мы (прош.)": "pl-fp-past",
    "Ты": "sg-sp-present",
    "Ты (прош.)": "sg-sp-past",
    "Ты (повел.)": "sg-sp-imperative",
    "Вы": "pl-sp-present",
    "Вы (прош.)": "pl-sp-past",
    "Вы (повел.)": "pl-sp-imperative",
    "Он/она/оно": "sg-tp-mfn-present",
    "Он/она/оно (прош.)": "sg-tp-mfn-past",
    "Они": "pl-tp-present",
    "Они (прош.)": "pl-tp-past",
    "ПричНаст": "participle-present",
    "ПричПрош": "participle-past",
    "ДеепрНаст": "ger-present",
    "ДеепрПрош": "ger-past",
    "ПричСтрад": "ger-present-passive",
    "ПричСтрадПрош": "get-past-passive",
    "Будущее": "future"

}

VERB_TP = [
    "sg-tp-m-past",
    "sg-tp-f-past",
    "sg-tp-n-past"
]

ARTICLE_NAMESPACE: str = "0"
TEMPLATE_NAMESPACE: str = "10"

USER_AGENT: Dict[str, str] = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.169 Safari/537.36'}
