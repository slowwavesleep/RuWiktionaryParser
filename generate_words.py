from typing import List, Union

from src.segmentation import clean_segments
from src.utils.etc import clean_string, determine_pos, basic_json_read, read_redirects, replace_redirect
from constants import WRITE_PATHS, INVARIABLE_POS, IGNORE_POS


# def segment_stem(stem: str, segments: dict) -> Union[List[str], None]:
#     """
#     Attempts to divide given stem into individual morphemes using morpheme division of a lemma.
#     :param stem: candidate word stem as a string
#     :param segments: a segmented lemma without additional processing, i.e. {"1": "seg_1", "2": "seg_2", ... "n": "seg_n"
#     :return: a list of stem segments or None
#     """
#     stem = clean_string(stem)
#     segments = clean_segments(segments)
#     whole_word = "".join(segments)
#     if len(stem) == combined_len(segments):
#         return segments
#     if whole_word.startswith(stem):
#         stem_segments = []
#         for seg in segments:
#             stem_segments.append(seg)
#             combined_seg = "".join(stem_segments)
#             if (stem == combined_seg
#                     or stem + "ь" == combined_seg
#                     or stem + "й" == combined_seg):
#                 return stem_segments
#             elif combined_seg[-1] == "и" and stem == combined_seg[:-1]:
#                 stem_segments[-1] = stem_segments[-1][:-1]
#                 return stem_segments
#
#         print(f"Stem: `{stem}` did not match with segments in `{whole_word}`")
#     else:
#         print(f"Different stem: {stem} {whole_word}")


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


def process_article(article, temps):
    title = article["title"]
    stems = article["morpho"]["stems"]
    pos = determine_pos(article)
    if pos in IGNORE_POS:
        return None
    if pos in INVARIABLE_POS:
        cleaned_segments = {"invariable": clean_segments(article["segments"])}
        print(cleaned_segments)

    # nouns with one stem and no "-"
    if pos == "noun" and "-" not in article["title"] and len(stems) == 1:
        pass
    # nouns with multiple stems and no "-"
    # nouns with "-"
    pass


articles = basic_json_read(WRITE_PATHS["article"])
templates = basic_json_read(WRITE_PATHS["template"])
redirects = read_redirects(WRITE_PATHS["template_redirect"])

articles = [replace_redirect(article, redirects) for article in articles]

for article in articles:
    process_article(article, templates)