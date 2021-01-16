from string import digits
from typing import List


def clean_string(seg: str) -> str:
    """
    Removes all symbols not part of the Russian alphabet
    from a given string.
    :param seg: a string to remove unnecessary symbols from
    :return: a cleaned string
    """
    ru_letters = ({chr(ind) for ind in range(ord("а"), ord("я") + 1)}
                  | {chr(ind) for ind in range(ord("А"), ord("Я") + 1)}
                  | {"Ё", "ё"})
    return "".join(c for c in seg if c in ru_letters)


def clean_segments(segments: dict):
    return [clean_string(value) for key, value in sorted(segments.items())if key in digits]


def combined_len(segments: List[str]) -> int:
    return sum(len(seg) for seg in segments)


def segment_stem(stem: str, segments: dict):
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

        print(f"Stem: `{stem}` didn't match with segments in `{whole_word}`")
    else:
        print("Different stem")


# segs = {'1': 'воскресеньj', '2': '+е', 'и': 'т'}
# stem = "воскресе́н"
#
# print(segment_stem(stem, segs))
