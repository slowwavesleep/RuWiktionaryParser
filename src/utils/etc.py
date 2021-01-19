import re
from unicodedata import normalize


def clean_string(seg: str) -> str:
    # TODO Consider complex words with "-"
    """
    Removes all symbols not part of the Russian alphabet from a given string and
    converts all chars into their composed unicode form.
    :param seg: a string to remove unnecessary symbols from
    :return: a cleaned string
    """
    # remove optional elements
    seg = re.sub(r"\(.*?\)", "", seg)
    # decompose string to filter out stress marks
    seg = normalize("NFD", seg)
    ru_letters = ({chr(ind) for ind in range(ord("а"), ord("я") + 1)}
                  | {chr(ind) for ind in range(ord("А"), ord("Я") + 1)}
                  | {"\u0308", "\u0306"}) # this is diacritical marks for letters `й` and `ё`
    seg = "".join(c for c in seg if c in ru_letters)
    # convert back to composed form
    return normalize("NFC", seg)