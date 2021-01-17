from string import digits
from typing import List, Union, Dict
from unicodedata import normalize
import re


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


def clean_segments(segments: dict) -> List[str]:
    """
    Transforms a raw segments dictionary into a list of cleaned segments.
    :param segments: a raw segments dictionary
    :return: a sorted list of segments
    """
    return [clean_string(value) for key, value in sorted(segments.items())
            if key in digits and value]


def combined_len(segments: List[str]) -> int:
    """
    Simple function to check the total length of combined segments.
    :param segments: a list of segments
    :return: total amount of symbols
    """
    return sum(len(seg) for seg in segments)


def segment_stem(stem: str, segments: dict) -> Union[List[str], None]:
    """
    Attempts to divide given stem into individual morphemes using morpheme division of a lemma.
    :param stem: candidate word stem as a string
    :param segments: a segmented lemma without additional processing, i.e. {"1": "seg_1", "2": "seg_2", ... "n": "seg_n"
    :return: a list of stem segments or None
    """
    stem = clean_string(stem)
    segments = clean_segments(segments)
    whole_word = "".join(segments)
    if len(stem) == combined_len(segments):
        return segments
    if whole_word.startswith(stem):
        stem_segments = []
        for seg in segments:
            stem_segments.append(seg)
            combined_seg = "".join(stem_segments)
            if (stem == combined_seg
                    or stem + "ь" == combined_seg
                    or stem + "й" == combined_seg):
                return stem_segments
            elif combined_seg[-1] == "и" and stem == combined_seg[:-1]:
                stem_segments[-1] = stem_segments[-1][:-1]
                return stem_segments

        print(f"Stem: `{stem}` did not match with segments in `{whole_word}`")
    else:
        print(f"Different stem: {stem} {whole_word}")


def all_stems_filled(stems: dict) -> bool:
    """
    Returns True if stems dictionary is not empty
    and all its values are not empty.
    :param stems: a dictionary containing word stem or stems
    :return: a boolean value
    """
    if stems and all(stems.values()):
        # assert "основа" in stems.keys()
        return True
    else:
        return False


def some_stems_filled(stems: dict) -> bool:
    """
    Returns True if stems dictionary is not empty,
    and some of its values are not empty.
    :param stems: a dictionary containing word stem or stems
    :return: a boolean value
    """
    if stems and any(stems.values()):
        return True
    else:
        return False


def replace_template_redirects(article: dict, template_redirects: Dict[str, str]) -> dict:
    template_name = article["morpho"]["template"]
    if template_name in template_redirects:
        article["morpho"]["template"] = template_redirects[template_name]
    return article


def process_articles():
    # nouns with one stem and no "-"
    # nouns with multiple stems and no "-"
    # nouns with "-"
    pass

