from dataclasses import dataclass


@dataclass
class WikiPage:
    id_: int
    title: str
    raw_wiki: str


@dataclass
class Article(WikiPage):
    is_proper: bool


@dataclass
class Template(WikiPage):
    pass
