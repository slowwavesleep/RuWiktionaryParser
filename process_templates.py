import json
import re
from typing import Tuple, Optional
import pathlib

from constants import WRITE_PATHS, SEGMENT_SEPARATOR, PROCESSED_DIR

# question marks at the end of templates are probably safe to remove in articles
# however, it is not clear what is their purpose exactly

# TODO generate word forms after processing all available templates
from src.utils.etc import determine_pos, basic_filter, read_redirects, replace_redirect, is_usable_template, \
    basic_json_read, clean_string


def separate_form_template(form_template: str) -> Optional[Tuple[str, str]]:
    ending = re.findall(r"[^\}]+$", form_template)
    if ending:
        ending = ending[0]
    else:
        ending = ""
    stem_name = re.findall(r"основа-?\d?", form_template)
    if not stem_name:
        return None
    else:
        return stem_name[0], clean_string(ending)


def process_template(template_page: dict):
    pos = determine_pos(template_page, page_type="template")
    result = {}
    for key, value in template_page["template"].items():
        if "основа" in value:
            if "<br>" in value:
                value = value.split("<br>")
            elif "<br />" in value:
                value = value.split("<br />")
            elif " " in value:
                value = value.split()
            else:
                value = [value]

            if "if" not in value and "основа" in value[0]:
                if pos == "noun":
                    result[key] = separate_form_template(value[0])
    return result


def remove_duplicate_seps(segmented_string: str, *, sep: str = SEGMENT_SEPARATOR):
    sep_flag = False
    filtered = []
    for c in segmented_string:
        if c != sep:
            filtered.append(c)
            if sep_flag:
                sep_flag = False
        else:
            if not sep_flag:
                sep_flag = True
                filtered.append(c)
    return "".join(filtered)


def process_ending_noun(ending, *, sep: str = SEGMENT_SEPARATOR):
    if ending == "еняток":
        return sep + "ен" + sep + "ят" + sep + "ок"
    if ending == "енят":
        return sep + "ен" + sep + "ят"
    if ending == "енятки":
        return sep + "ен" + sep + "ят" + sep + "к" + sep + "и"
    if ending == "еняткам":
        return sep + "ен" + sep + "ят" + sep + "к" + sep + "ам"
    if ending == "енятками":
        return sep + "ен" + sep + "ят" + sep + "к" + sep + "ам" + "и"
    if ending == "енятках":
        return sep + "ен" + sep + "ят" + sep + "к" + sep + "ах"
    if ending == "енята":
        return sep + "ен" + sep + "ят" + sep + "а"
    if ending == "енятам":
        return sep + "ен" + sep + "ят" + sep + "ам"
    if ending == "енятами":
        return sep + "ен" + sep + "ят" + sep + "ам" + sep + "и"
    if ending == "енятах":
        return sep + "ен" + sep + "ят" + sep + "ах"
    if ending == "яьми":
        return sep + "ями"
    if ending == "еви":
        return sep + "ев" + "и"

    if len(ending) > 2 and ending[:2] == "ён":
        return sep + ending[:2] + sep + ending[2:]
    if len(ending) == 1:
        if ending in "ьъ":
            return ending
        else:
            return sep + ending
    elif len(ending) > 2 and ending[:2] == "иц":
        return "и" + "ц" + sep + ending[2:]
    else:
        if ending[0] in "ьи":
            return ending[0] + sep + ending[1:]
        elif ending[0] in "кцн":
            return sep + ending[0] + sep + ending[1:]
        else:
            return sep + ending


def process_ending(ending: str, pos: str, *, sep: str = SEGMENT_SEPARATOR) -> str:
    if not ending:
        return ending
    if ending[-1] == '̈е':  # broken unicode
        ending[-1] = "ё"

    if pos == "noun":
        ending = process_ending_noun(ending, sep=sep)

    if len(ending) > 2 and ending[-2:] in ("ся", "сь"):
        ending = ending[:-2] + sep + ending[-2:]

    ending = remove_duplicate_seps(ending, sep=sep)

    return ending


redirects = read_redirects(WRITE_PATHS["template_redirect"])

full_noun_templates = []
broken_noun_templates = []

noun_templates = basic_json_read(WRITE_PATHS["template"])

destination = pathlib.Path(PROCESSED_DIR)
destination.mkdir(parents=True, exist_ok=True)

with open(destination / "templates.jsonl", "w") as file:
    for template in noun_templates:
        if determine_pos(template, page_type="template") == "noun":
            template_id = template["id"]
            template_title = template["title"]
            if is_usable_template(template):
                temp = process_template(template)
                final_temp = {}
                for key, value in temp.items():
                    final_temp[key] = {value[0]: process_ending(value[1], "noun")}
                if final_temp:
                    file.write(json.dumps({"id": template_id,
                                           "title": template_title,
                                           "template": final_temp}, ensure_ascii=False) + "\n")

