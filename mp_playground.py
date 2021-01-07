import multiprocessing as mp
from bz2 import BZ2File
from lxml.etree import iterparse, _Element
from itertools import islice
from typing import Union

from config import DUMP_PATH, PROCESS_TEMPLATES, PROCESS_ARTICLES
from src.data import Article, Template
from src.utils.xml import is_article_title_ru, is_template, is_template_title_ru, is_redirect, is_article, \
    is_article_title_proper, is_element_page, get_page_id, get_raw_wiki, get_page_title
from src.utils.wiki import find_ru_section, parse_ru_section


def process_element(element: _Element) -> Union[Article, Template, None]:

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
            wiki_page = None

        element.clear()

        for ancestor in element.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]

        return wiki_page


def parse_dump(dump_path, conn):

    with BZ2File(dump_path) as bz_file:

        for index, (_, elem) in enumerate(islice(iterparse(bz_file), 100000)):

            if index % 100000 == 0:
                print("\r" + f"Processed {index} XML elements...", end="")

            processed_page = process_element(elem)
            if processed_page:
                conn.put(processed_page)

        conn.put('STOP')


def parse_wiki(conn):
    while True:
        data = conn.get()
        if data == 'STOP':
            break


if __name__ == "__main__":

    queue = mp.Queue()

    wiki_process = mp.Process(target=parse_wiki, args=(queue, ))

    wiki_process.start()

    parse_dump(DUMP_PATH, queue)

    wiki_process.join()



