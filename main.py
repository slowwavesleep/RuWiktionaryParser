from bz2 import BZ2File
import re
from typing import NoReturn
from lxml.etree import iterparse, _Element
from tqdm import tqdm
import pathlib
from itertools import islice
from typing import Union
from constants import DUMP_PATH, TAGS, ARTICLE_NAMESPACE, TEMPLATE_NAMESPACE,\
                      TMP_PATH, PROCESS_ARTICLES, PROCESS_TEMPLATES, TOTAL_LINES
from src.data import Article, Template


def store_raw_wiki(page: Union[Article, Template]) -> NoReturn:
    if isinstance(wiki_page, Article):
        sub_folder: str = "proper" if page.is_proper else "other"
        path: pathlib.Path = pathlib.Path(f"{TMP_PATH}articles/{sub_folder}/")
    elif isinstance(wiki_page, Template):
        path: pathlib.Path = pathlib.Path(f"{TMP_PATH}templates/")
    else:
        raise NotImplementedError

    path.mkdir(parents=True, exist_ok=True)

    path = path.joinpath(f"{page.id_}.tmp")
    with open(path, "w") as file:
        file.write(page.raw_wiki)


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


with BZ2File(DUMP_PATH) as bz_file:
    # for _, element in islice(iterparse(bz_file), 5000000):
    for _, element in tqdm(iterparse(bz_file),
                           total=TOTAL_LINES):  # inaccurate

        if is_element_page(element) and not is_redirect(element):

            wiki_page = None

            cur_id = get_page_id(element)
            cur_title = get_page_title(element)
            cur_wiki = get_raw_wiki(element)

            if is_article(element) and is_article_title_ru(cur_title) and PROCESS_ARTICLES:

                is_proper: bool = is_article_title_proper(cur_title)

                wiki_page = Article(id_=cur_id,
                                    title=cur_title,
                                    raw_wiki=cur_wiki,
                                    is_proper=is_proper)

            elif is_template(element) and is_template_title_ru(cur_title) and PROCESS_TEMPLATES:

                wiki_page = Template(id_=cur_id,
                                     title=cur_title,
                                     raw_wiki=cur_wiki)

            else:
                pass

            if wiki_page:
                store_raw_wiki(wiki_page)

            # Runs out of memory otherwise
            element.clear()

