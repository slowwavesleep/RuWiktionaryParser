from string import digits
from typing import List

from src.utils.etc import clean_string


def clean_segments(segments: dict) -> str:
    """
    Transforms a raw segments dictionary into a list of cleaned segments.
    :param segments: a raw segments dictionary
    :return: a string where morpheme boundaries are represented using `|` symbol
    """
    return "|".join(clean_string(value) for key, value in sorted(segments.items())
                    if key in digits and value)
