import re

from lxml.etree import _Element

from config import TAGS, TEMPLATE_NAMESPACE, ARTICLE_NAMESPACE


def is_article_title_ru(title: str) -> bool:
    pattern = re.compile(r"^[А-Яа-яЁё\-]+[^\-]$")
    return bool(re.match(pattern, title))


def is_template(page: _Element) -> bool:
    return page.find(TAGS["namespace"]).text == TEMPLATE_NAMESPACE


def is_template_title_ru(title: str) -> bool:
    pattern = re.compile(r"^Шаблон:.*ru.*$")
    return (bool(re.match(pattern, title))
            and "User" not in title)


def is_redirect(page: _Element) -> bool:
    if page.find(TAGS["redirect"]) is not None:
        return True
    else:
        return False


def is_article(page: _Element) -> bool:
    return page.find(TAGS["namespace"]).text == ARTICLE_NAMESPACE


def is_article_title_proper(title: str) -> bool:
    return title.istitle()


def is_element_page(elem: _Element) -> bool:
    return "page" in elem.tag


def get_page_id(page: _Element) -> int:
    return int(page.find(TAGS["id"]).text)


def get_raw_wiki(page: _Element) -> str:
    return page.find(TAGS["text"]).text


def get_page_title(page: _Element) -> str:
    return page.find(TAGS["title"]).text


def get_redirect_title(page: _Element) -> str:
    return page.find(TAGS["title"]).text
