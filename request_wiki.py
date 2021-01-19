from typing import Union, Dict
from timeit import default_timer as timer
import requests

from bs4 import BeautifulSoup as bs
from bs4.element import Tag

USER_AGENT = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/74.0.3729.169 Safari/537.36'}

TEST_WORDS = [
    "дар",
    "друг",
    "заживо",
    "доха",
    "муж",
    "ребёнок",
    "младенец",
    "лужа",
    "крыша",
    "звезда",
    "молоко"
]


def get_url(title: str) -> str:
    """
    Generate an api url for a given title.
    :param title: a word to look up
    :return: an url
    """
    # using the api in this format is essentially equivalent to simply requesting a regular page
    # also, using the `parse` api is considerably slower
    # keeping it in case of discovering some useful application for it
    # return f"https://ru.wiktionary.org/w/api.php?action=parse&page={title}&prop=text&formatversion=2&format=json"

    # so, ultimately it's much easier to parse the regular article
    return f"https://ru.wiktionary.org/wiki/{title}"


def request_text(title):
    url = get_url(title)
    html = requests.get(url, headers=USER_AGENT)
    return html.text


def parse_noun_table(html: Tag) -> Dict[str, str]:
    pass

# def get_morpho_table(html: str) -> Union[pd.DataFrame, None]:
#     try:
#         # this is just the first meaning
#         # homonymy is not considered at the moment
#         table = pd.read_html(html, attrs={'class': 'morfotable ru'})[0]
#         return table
#     except ValueError:
#         return None


# def process_title(title: str) -> Union[pd.DataFrame, None]:
#     html = request_text(title)
#     table = get_morpho_table(html)
#     return table.to_json()


# start = timer()
# for word in TEST_WORDS[0]:
#     print(word)
#     print(process_title(word))
#
# end = timer()
#
# print("\n" + f"Time elapsed: {end - start:.4f}")