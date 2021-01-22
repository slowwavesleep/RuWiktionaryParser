import re
from typing import NoReturn, Union
from unicodedata import normalize

from constants import POS_MAP


def clean_string(seg: str) -> str:
    # TODO Consider complex words with "-"
    """
    Removes all symbols not part of the Russian alphabet from a given string and
    converts all chars into their composed unicode form.
    :param seg: a string to remove unnecessary symbols from
    :return: a cleaned string
    """
    # remove optional elements
    seg = seg.strip("\n").strip()
    seg = re.sub(r"\(.*?\)", "", seg)
    # decompose string to filter out stress marks
    seg = normalize("NFD", seg)
    ru_letters = ({chr(ind) for ind in range(ord("а"), ord("я") + 1)}
                  | {chr(ind) for ind in range(ord("А"), ord("Я") + 1)}
                  | {"-"}
                  | {"\u0308", "\u0306"}) # this is diacritical marks for letters `й` and `ё`
    seg = "".join(c for c in seg if c in ru_letters)
    # convert back to composed form
    return normalize("NFC", seg).strip("-")


def empty_file(path: str) -> NoReturn:
    """
    Given a path creates an empty file
    :param path: file path
    """
    open(path, "w").close()


def basic_filter(article: dict) -> bool:
    return not article["is_proper"] and not article["is_obscene"]


def determine_pos(article: dict) -> Union[str, None]:
    template = article["morpho"].get("template")
    for key in POS_MAP.keys():
        if key in template:
            return POS_MAP[key]

