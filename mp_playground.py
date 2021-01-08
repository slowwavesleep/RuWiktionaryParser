import multiprocessing as mp
from bz2 import BZ2File
from lxml.etree import iterparse, _Element
from itertools import islice
from typing import Union
import wikitextparser as wtp
from timeit import default_timer as timer
import json

from config import DUMP_PATH, PROCESS_TEMPLATES, PROCESS_ARTICLES
from src.data import Article, Template
from src.utils.xml import is_article_title_ru, is_template, is_template_title_ru, is_redirect, is_article, \
    is_article_title_proper, is_element_page, get_page_id, get_raw_wiki, get_page_title
from src.utils.wiki import find_ru_section, parse_ru_section


WRITE_PATHS = {
    "template": "tmp/templates.json",
    "article": "tmp/articles.json"
}


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

        for index, (_, elem) in enumerate(islice(iterparse(bz_file), 1000000)):

            if index % 100000 == 0:
                print("\r" + f"Processed {index} XML elements...", end="")

            processed_page = process_element(elem)
            if processed_page:
                conn.put(processed_page)

        conn.put('STOP')
        print("\n" + f"Total elements processed: {index}")


def parse_wiki(in_conn, out_conn):

    while True:

        data: Union[Article, Template, str] = in_conn.get()

        if data == "STOP":
            out_conn.put(data)
            break

        wiki = wtp.parse(data.raw_wiki)
        ru_section = find_ru_section(wiki)

        if ru_section:
            parsed_ru_section = parse_ru_section(ru_section)
            if parsed_ru_section:
                parsed_ru_section["id"] = data.id_
                parsed_ru_section["title"] = data.title
                if isinstance(data, Article):
                    parsed_ru_section["type"] = "article"
                    parsed_ru_section["is_proper"] = data.is_proper
                elif isinstance(data, Template):
                    parsed_ru_section["type"] = "template"
                else:
                    parsed_ru_section["type"] = "other"

                out_conn.put(parsed_ru_section)


def write_result(paths, conn):
    while True:
        data: Union[dict, str] = conn.get()
        if data == "STOP":
            break
        data_type = data["type"]
        path = paths.get(data_type, None)
        if path:
            with open(path, "a") as file:
                file.write(json.dumps(data) + "\n")


if __name__ == "__main__":

    start = timer()

    task_queue = mp.Queue()
    write_queue = mp.Queue()

    wiki_process = mp.Process(target=parse_wiki, args=(task_queue, write_queue))
    write_process = mp.Process(target=write_result, args=(WRITE_PATHS, write_queue))

    wiki_process.start()
    write_process.start()

    parse_dump(DUMP_PATH, task_queue)

    wiki_process.join()
    write_process.join()

    end = timer()

    print("\n" + f"Time elapsed: {end - start:.4f}")



