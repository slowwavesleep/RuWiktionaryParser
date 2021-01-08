from dataclasses import dataclass


@dataclass
class BaseWikiPage:
    id_: int
    title: str


@dataclass
class WikiPage(BaseWikiPage):
    raw_wiki: str


@dataclass
class Article(WikiPage):
    is_proper: bool


@dataclass
class Template(WikiPage):
    pass


# @dataclass
# class ParsedArticleMorpho(BaseWikiPage):
#     template: str
#     stems: dict
#     segments: dict

