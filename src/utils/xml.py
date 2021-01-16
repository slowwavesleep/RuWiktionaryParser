import re

from lxml.etree import Element

from config import TAGS, TEMPLATE_NAMESPACE, ARTICLE_NAMESPACE


def is_article_title_ru(title: str) -> bool:
    pattern = re.compile(r"^[А-Яа-яЁё\-]+[^\-]$")
    return bool(re.match(pattern, title))


def is_template(page: Element) -> bool:
    return page.find(TAGS["namespace"]).text == TEMPLATE_NAMESPACE


def is_template_title_ru(title: str) -> bool:
    pattern = re.compile(r"^Шаблон:.*ru.*$")
    return (bool(re.match(pattern, title))
            and "User" not in title)


def is_redirect(page: Element) -> bool:
    if page.find(TAGS["redirect"]) is not None:
        return True
    else:
        return False


def is_article(page: Element) -> bool:
    return page.find(TAGS["namespace"]).text == ARTICLE_NAMESPACE


def is_article_title_proper(title: str) -> bool:
    return title.istitle()


def is_element_page(elem: Element) -> bool:
    return "page" in elem.tag


def get_page_id(page: Element) -> int:
    return int(page.find(TAGS["id"]).text)


def get_raw_wiki(page: Element) -> str:
    return page.find(TAGS["text"]).text


def get_page_title(page: Element) -> str:
    return page.find(TAGS["title"]).text


def get_redirect_title(page: Element) -> str:
    return page.find(TAGS["redirect"]).get("title")
