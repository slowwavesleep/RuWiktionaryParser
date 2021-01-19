from typing import Union, Dict
from timeit import default_timer as timer
import requests

from bs4 import BeautifulSoup as Soup
from bs4.element import Tag
import pandas as pd

from constants import NUMBER_MAP, CASE_MAP
from src.utils.etc import clean_string


# TODO parse template pages and pages for words that don't provide stems explicitly
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


def request_text(title: str) -> str:
    url = get_url(title)
    html = requests.get(url, headers=USER_AGENT)
    return html.text


def prepare_html_table(table: Tag) -> str:
    for br in table.find_all("br"):
        br.replace_with("\n")
    table = str(table).replace(u"\xa0", " ")
    return table


def parse_noun_table(table: Tag) -> Dict[str, str]:
    table = prepare_html_table(table)
    table = pd.read_html(table, flavor="bs4")[0]
    table = table.rename(columns={**{"падеж": "case"}, **NUMBER_MAP}).set_index("case").rename(index=CASE_MAP)
    return table_to_dict(table)


def table_to_dict(df: pd.DataFrame) -> Dict[str, str]:
    result = {}
    for col in df.columns:
        for index, item in df[col].items():
            if " " in item:
                item = item.split(" ")
                item = [clean_string(option) for option in item]
            else:
                item = clean_string(item)
            result[f"{index}-{col}"] = item
    return result


def get_morpho_table(html: str) -> Union[pd.DataFrame, None]:
    # this is just the first meaning
    # homonymy is not considered at the moment
    table = pd.read_html(html, attrs={'class': 'morfotable ru'})[0]
    return table


def process_title(title: str) -> Union[Dict[str, str], None]:
    html = request_text(title)
    parsed = Soup(html, features="lxml").find_all(class_="morfotable ru")
    if len(parsed) > 0:
        table = parse_noun_table(parsed[0])
        return table


start = timer()
for word in TEST_WORDS:
    print(word)
    print(process_title(word))

end = timer()

print("\n" + f"Time elapsed: {end - start:.4f}")