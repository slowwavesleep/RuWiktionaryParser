from multiprocessing import Queue, Process, cpu_count
from bz2 import BZ2File
from lxml.etree import iterparse, Element
from typing import Union, NoReturn
from timeit import default_timer as timer
import json

import wikitextparser as wtp

from config import DUMP_PATH, PROCESS_TEMPLATES, PROCESS_ARTICLES
from constants import WRITE_PATHS
from src.data import Article, Template, TemplateRedirect
from src.utils.xml import is_article_title_ru, is_template, is_template_title_ru, is_redirect, is_article, \
    is_article_title_proper, is_element_page, get_page_id, get_raw_wiki, get_page_title, get_redirect_title
from src.utils.wiki import find_ru_section, parse_ru_section, clean_template_name, parse_template_page, \
    remove_no_include

assert cpu_count() > 4
NUM_PROCESSES = 4


def process_element(element: Element) -> Union[Article, Template, None]:

    if is_element_page(element):

        cur_id: int = get_page_id(element)
        cur_title: str = get_page_title(element)
        cur_wiki: str = get_raw_wiki(element)

        if (is_article(element)
                and is_article_title_ru(cur_title)
                and not is_redirect(element)
                and PROCESS_ARTICLES):

            is_proper: bool = is_article_title_proper(cur_title)

            wiki_page = Article(id_=cur_id,
                                title=cur_title,
                                raw_wiki=cur_wiki,
                                is_proper=is_proper)

        elif (is_template(element)
              and is_template_title_ru(cur_title)
              and not is_redirect(element)
              and PROCESS_TEMPLATES):

            cur_title: str = clean_template_name(cur_title)

            wiki_page = Template(id_=cur_id,
                                 title=cur_title,
                                 raw_wiki=cur_wiki)

        elif (is_template(element)
              and is_template_title_ru(cur_title)
              and is_redirect(element)
              and PROCESS_TEMPLATES):

            cur_title: str = clean_template_name(cur_title)

            redirect_title: str = get_redirect_title(element)
            redirect_title: str = clean_template_name(redirect_title)

            wiki_page = TemplateRedirect(id_=cur_id,
                                         title=cur_title,
                                         raw_wiki=cur_wiki,
                                         redirect_title=redirect_title)

        else:
            wiki_page = None

        element.clear()

        for ancestor in element.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]

        return wiki_page


def parse_dump(dump_path: str, conn: Queue) -> NoReturn:
    with BZ2File(dump_path) as bz_file:
        for index, (_, elem) in enumerate(iterparse(bz_file)):
            if index % 100000 == 0:
                print("\r" + f"Processed {index} XML elements...", end="")

            processed_page = process_element(elem)

            if processed_page:
                conn.put(processed_page)

        for _ in range(NUM_PROCESSES):
            conn.put('STOP')

        print("\n" + f"Total elements processed: {index}")


def parse_wiki(in_conn: Queue, out_conn: Queue) -> NoReturn:
    while True:
        data: Union[Article, Template, str] = in_conn.get()
        if data == "STOP":
            for _ in range(NUM_PROCESSES):
                out_conn.put(data)
            break

        if isinstance(data, Article):
            wiki_data = wtp.parse(data.raw_wiki)
            wiki_data = find_ru_section(wiki_data)

            if wiki_data:
                parsed_wiki_data = parse_ru_section(wiki_data)
                if parsed_wiki_data:
                    parsed_wiki_data["id"] = data.id_
                    parsed_wiki_data["title"] = data.title
                    parsed_wiki_data["type"] = "article"
                    parsed_wiki_data["is_proper"] = data.is_proper

                    out_conn.put(parsed_wiki_data)

        elif isinstance(data, Template):
            wiki_data = wtp.parse(remove_no_include(data.raw_wiki))
            if wiki_data:
                parsed_wiki_data = parse_template_page(wiki_data)
                if parsed_wiki_data:
                    parsed_wiki_data["id"] = data.id_
                    parsed_wiki_data["title"] = data.title
                    parsed_wiki_data["type"] = "template"

                    out_conn.put(parsed_wiki_data)

        elif isinstance(data, TemplateRedirect):
            parsed_wiki_data = {
                "id": data.id_,
                "title": data.title,
                "redirect_title": data.redirect_title,
                "type": "template_redirect"
            }

            out_conn.put(parsed_wiki_data)
        else:
            pass


def empty_file(path: str) -> NoReturn:
    open(path, "w").close()


def write_result(paths: dict, conn: Queue):
    for _, path in paths.items():
        empty_file(path)
    while True:
        data: Union[dict, str] = conn.get()
        if data == "STOP":
            break
        data_type = data["type"]
        path = paths.get(data_type, None)
        # why both files
        if path:
            with open(path, "a") as file:
                file.write(json.dumps(data) + "\n")


if __name__ == "__main__":

    start = timer()

    task_queue = Queue()
    write_queue = Queue()

    wiki_process = [Process(target=parse_wiki, args=(task_queue, write_queue)) for _ in range(NUM_PROCESSES)]
    write_process = Process(target=write_result, args=(WRITE_PATHS, write_queue))

    for process in wiki_process:
        process.start()

    write_process.start()

    parse_dump(DUMP_PATH, task_queue)

    for process in wiki_process:
        process.join()
    write_process.join()

    end = timer()

    print("\n" + f"Time elapsed: {end - start:.4f}")


