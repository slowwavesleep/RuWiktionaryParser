import wikitextparser as wtp
from wikitextparser._wikitext import WikiText
from wikitextparser._section import Section
from wikitextparser._template import Template
from typing import Union, Dict, List
import pathlib
from itertools import islice
from tqdm import tqdm
import json



paths = list(pathlib.Path("tmp/articles/other").joinpath().glob("*.tmp"))
total = len(paths)

PARSED_PATH = "tmp/parsed.json"


def find_ru_section(wiki_text: WikiText) -> Union[Section, None]:
    sections = wiki_text.get_sections()
    sections = [section for section in sections if section.level == 1 and '{{-ru-}}' in section.title]
    if len(sections) == 1:
        return sections[0]
    else:
        return None


def find_ru_morpho_section(wiki_text: WikiText) -> Union[Section, None]:
    sections = wiki_text.get_sections()
    sections = [section for section in sections if 'Морфологические и синтаксические свойства' in str(section.title)]
    if len(sections) == 1:
        return sections[0]
    else:
        return None


def parse_morpho(temp: Template) -> Dict[str, Union[str, dict]]:
    temp_name = temp.name.strip('\n')
    args = temp.arguments
    stems = {arg.name.strip('\n'): arg.value.strip('\n')
             for arg in args if "основа" in arg.name}
    return {
        "template": temp_name,
        "stems": stems
    }


def find_segments(templates: List[Template]) -> Union[Template, None]:
    segments = [temp for temp in templates if "морфо-ru" in temp.name]
    if len(segments) == 1:
        return segments[0]
    else:
        return None


def parse_segments(temp: Template) -> Dict[str, str]:
    assert "морфо-ru" in temp.name
    args = temp.arguments
    assert len(args) > 0
    segments = {segment.name: segment.value for segment in args}
    return segments


def parse_ru_section(section: Section):
    section = find_ru_morpho_section(section)
    if not section or not section.templates:
        return None
    section = section.templates
    morpho = parse_morpho(section[0])
    segments = find_segments(section)
    if not segments:
        return None
    segments = parse_segments(segments)
    if len(segments) == 1 and segments["1"] == "":
        return None
    return {
        "morpho": morpho,
        "segments": segments
    }


parsed = []
for path in tqdm(paths, total=total):
    with open(path) as file:
        data = file.read()
        data = wtp.parse(data)
        section = find_ru_section(data)

        if section:
            section = parse_ru_section(section)
            if section:
                parsed.append(section)
        else:
            pass


with open(PARSED_PATH, "w") as file:
    json.dump(parsed, file, indent=4)

# with open(PARSED_PATH) as file:
#     test = json.load(file)
#
# print(test)