from bz2 import BZ2File
import re
from dataclasses import dataclass
from enum import Enum, auto
from lxml.etree import iterparse, _Element
from itertools import islice
from constants import DUMP_PATH, TAGS, ARTICLE_NAMESPACE, TEMPLATE_NAMESPACE
import jsons


class PageType(Enum):
    template = auto()
    article = auto()
    other = auto()


@dataclass
class Page:
    page_id: int
    page_title: str
    page_type: PageType
    raw_wiki: str


def is_title_ru(title: str) -> bool:
    pattern = re.compile(r"^[А-Яа-яЁё\-]+[^\-]$")
    return bool(re.match(pattern, title))


def is_template_ru(title: str) -> bool:
    pattern = re.compile(r"^Шаблон:.+ru.+$")
    return bool(re.match(pattern, title))


def is_redirect(page: _Element) -> bool:
    if page.find(TAGS["redirect"]) is not None:
        return True
    else:
        return False


def is_article(page: _Element) -> bool:
    return page.find(TAGS["namespace"]).text == ARTICLE_NAMESPACE


def is_template(page: _Element) -> bool:
    return page.find(TAGS["namespace"]).text == TEMPLATE_NAMESPACE


def is_element_page(elem: _Element) -> bool:
    return "page" in elem.tag


def get_page_id(page: _Element) -> int:
    return int(page.find(TAGS["id"]).text)


def get_raw_wiki(page: _Element) -> str:
    return page.find(TAGS["text"]).text


def get_page_title(page: _Element) -> str:
    return page.find(TAGS["title"]).text


def process_article(page: _Element):
    pass


def process_template(page: _Element):
    pass


articles = []
templates = []
with BZ2File(DUMP_PATH) as bz_file:
    for _, element in islice(iterparse(bz_file), 1000):

        if is_element_page(element) and not is_redirect(element):

            page_id = get_page_id(element)
            page_title = get_page_title(element)
            raw_wiki = get_raw_wiki(element)

            if is_article(element):
                page_type = PageType.article

            elif is_template(element):
                page_type = PageType.template

            else:
                page_type = PageType.other

            cur_page = Page(page_id,
                            page_title,
                            page_type,
                            raw_wiki)

            if (cur_page.page_type == PageType.article
                    and is_title_ru(cur_page.page_title)):

                articles.append(cur_page)

            elif (cur_page.page_type == page_type.template
                  and is_template_ru(cur_page.page_title)):

                templates.append(cur_page)

print(jsons.dump(articles[-1]))

with open('tmp/templates.json', 'w') as file:
    for article in articles:
        file.write(jsons.dumps(article))
