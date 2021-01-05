from bz2 import BZ2File
from typing import NoReturn
from lxml.etree import iterparse, _Element
import pathlib
import json
from typing import Union
from config import DUMP_PATH, TMP_PATH, PROCESS_ARTICLES, PROCESS_TEMPLATES
from src.data import Article, Template
from src.xml_utils import is_article_title_ru, is_template, is_template_title_ru, is_redirect, is_article, \
    is_article_title_proper, is_element_page, get_page_id, get_raw_wiki, get_page_title


def store_raw_wiki(page: Union[Article, Template]) -> NoReturn:
    if isinstance(page, Article):
        sub_folder: str = "proper" if page.is_proper else "other"
        path: pathlib.Path = pathlib.Path(f"{TMP_PATH}articles/{sub_folder}/")
    elif isinstance(page, Template):
        path: pathlib.Path = pathlib.Path(f"{TMP_PATH}templates/")
    else:
        raise NotImplementedError

    path.mkdir(parents=True, exist_ok=True)

    path = path.joinpath(f"{page.id_}")
    with open(path, "w") as file:
        file.write(page.raw_wiki)


def store_index2title(i2t) -> NoReturn:
    path = pathlib.Path(TMP_PATH + "index2title.json")
    with open(path, "w") as file:
        json.dump(i2t, file, indent=4)


def process_element(element: _Element) -> Union[Article, Template, None]:

    wiki_page = None

    if is_element_page(element) and not is_redirect(element):

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

        element.clear()

        for ancestor in element.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]

        return wiki_page


with BZ2File(DUMP_PATH) as bz_file:

    index2title = dict()

    for index, (_, elem) in enumerate(iterparse(bz_file)):

        if index % 100000 == 0:
            print("\r" + f"Processed {index} XML elements...", end="")

        processed_page = process_element(elem)

        if processed_page:
            index2title[processed_page.id_] = processed_page.title
            store_raw_wiki(processed_page)

    store_index2title(index2title)

    print("\n" + f"Finished processing {index} elements!")

