from multiprocessing import Queue, Process, cpu_count
from bz2 import BZ2File
from lxml.etree import iterparse, Element
from typing import Union, NoReturn
from timeit import default_timer as timer
import json

import wikitextparser as wtp

from config import DUMP_PATH, PROCESS_TEMPLATES, PROCESS_ARTICLES
from constants import WRITE_PATHS, BROKEN_ARTICLES
from src.data import Article, Template, TemplateRedirect
from src.utils.xml import is_article_title_ru, is_template, is_template_title_ru, is_redirect, is_article, \
    is_article_title_proper, is_element_page, get_page_id, get_raw_wiki, get_page_title, get_redirect_title
from src.utils.wiki import find_ru_section, parse_ru_section, clean_template_name, parse_template_page, \
    remove_no_include

assert cpu_count() > 4
NUM_PROCESSES = 4


def process_element(element: Element) -> Union[Article, Template, None]:
    """
    Parses an individual XML element. Returns an instance of a corresponding
    class if successful, None otherwise.
    Additionally, clears all parent elements of a given element to conserve memory.
    :param element: XML element
    :return: an instance of Article or Template class or None
    """
    # we're only interested in `page` elements in this dump
    if is_element_page(element):

        cur_id: int = get_page_id(element)
        cur_title: str = get_page_title(element)
        cur_wiki: str = get_raw_wiki(element)

        # filter out incorrectly formatted articles
        if cur_title in BROKEN_ARTICLES:
            wiki_page = None

        elif (is_article(element)
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
        # not interested in other cases
        else:
            wiki_page = None

        # remove data from current element
        element.clear()

        # clear all preceding elements
        for ancestor in element.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]

        return wiki_page


def parse_dump(dump_path: str, conn: Queue) -> NoReturn:
    """
    Iteratively goes through a compressed XML dump. Extracts information
    from page elements. If extraction is successful (i.e. not None), then
    the processed information is passed on to an output queue.
    :param dump_path: path leading to the compressed XML dump
    :param conn: output queue
    """
    with BZ2File(dump_path) as bz_file:
        for index, (_, elem) in enumerate(iterparse(bz_file)):
            if index % 100000 == 0:
                print("\r" + f"Processed {index} XML elements...", end="")

            processed_page = process_element(elem)

            if processed_page:
                conn.put(processed_page)

        # we need to stop each individual process down the line
        # after we're done parsing the dump
        for _ in range(NUM_PROCESSES):
            conn.put('STOP')

        # total number of elements processed for reference
        print("\n" + f"Total elements processed: {index}")


def parse_wiki(in_conn: Queue, out_conn: Queue) -> NoReturn:
    """
    Processes actual wiki text of a given page. Receives data from an input queue
    and puts results into an output queue.
    Meant to run in multiple parallel processes.
    :param in_conn: input queue
    :param out_conn: output queue
    """
    # runs in an infinite cycle until it receives a stop signal
    while True:
        data: Union[Article, Template, str] = in_conn.get()
        # upon receiving the stop signal
        # pass it further down the line and break the infinite cycle
        if data == "STOP":
            out_conn.put(data)
            break
        # parse the article type
        if isinstance(data, Article):
            wiki_data = wtp.parse(data.raw_wiki)
            wiki_data = find_ru_section(wiki_data)
            # proceed if Russian language section is found
            if wiki_data:
                # parse found section
                parsed_wiki_data = parse_ru_section(wiki_data)
                # proceed if morphological information and segmentation data were found
                if parsed_wiki_data:
                    parsed_wiki_data["id"] = data.id_
                    parsed_wiki_data["title"] = data.title
                    parsed_wiki_data["type"] = "article"
                    parsed_wiki_data["is_proper"] = data.is_proper

                    out_conn.put(parsed_wiki_data)
        # Template class contains data from a page dedicated to a particular template
        elif isinstance(data, Template):
            wiki_data = wtp.parse(remove_no_include(data.raw_wiki))

            if wiki_data:
                parsed_wiki_data = parse_template_page(wiki_data)
                if parsed_wiki_data:
                    parsed_wiki_data["id"] = data.id_
                    parsed_wiki_data["title"] = data.title
                    parsed_wiki_data["type"] = "template"

                    out_conn.put(parsed_wiki_data)
        # we're interested only in template redirects
        # those are essentially aliases for template names
        # although only one page contains data
        elif isinstance(data, TemplateRedirect):
            # here we don't actually need any wiki data from the page body
            parsed_wiki_data = {
                "id": data.id_,
                "title": data.title,
                "redirect_title": data.redirect_title,
                "type": "template_redirect"
            }

            out_conn.put(parsed_wiki_data)
        # not interested in any other cases
        else:
            pass


def empty_file(path: str) -> NoReturn:
    """
    Given a path creates an empty file
    :param path: file path
    """
    open(path, "w").close()


def write_result(paths: dict, conn: Queue) -> NoReturn:
    """
    Receives data from input queue and writes it to a single line
    in a file. The file path depends on specified data type.
    :param paths: dictionary containing data types as keys and corresponding
    paths as values.
    :param conn: input queue
    """
    for _, path in paths.items():
        empty_file(path)
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
    # to check total time elapsed
    start = timer()
    # create necessary queues
    task_queue = Queue()
    write_queue = Queue()

    # wiki pages are completely independent of each other (except morphological templates, but we'll deal
    # with them separately), so it makes sense to parallelize their parsing
    wiki_process = [Process(target=parse_wiki, args=(task_queue, write_queue)) for _ in range(NUM_PROCESSES)]
    # this can be also done independently of XML and wiki parsing
    write_process = Process(target=write_result, args=(WRITE_PATHS, write_queue))
    # start all the processes
    for process in wiki_process:
        process.start()

    write_process.start()
    # run the main function
    parse_dump(DUMP_PATH, task_queue)
    # close the processes
    for process in wiki_process:
        process.join()
    write_process.join()

    end = timer()

    print("\n" + f"Time elapsed: {end - start:.4f}")



