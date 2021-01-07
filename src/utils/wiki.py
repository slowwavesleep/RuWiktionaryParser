from typing import Union, Dict, List

from wikitextparser import Section, Template
from wikitextparser._wikitext import WikiText


def find_ru_section(wiki_text: WikiText) -> Union[Section, None]:
    sections = wiki_text.get_sections()
    sections = [sec for sec in sections if sec.level == 1 and '{{-ru-}}' in sec.title]
    if len(sections) == 1:
        return sections[0]
    else:
        return None


def find_ru_morpho_section(wiki_text: WikiText) -> Union[Section, None]:
    sections = wiki_text.get_sections()
    sections = [sec for sec in sections if 'Морфологические и синтаксические свойства' in str(sec.title)]
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


def parse_segments(temp: Template) -> Union[Dict[str, str], None]:
    assert "морфо-ru" in temp.name
    args = temp.arguments
    if not len(args) > 0:
        return None
    segments = {segment.name: segment.value for segment in args}
    return segments


def parse_ru_section(wiki_section: Section) -> Union[Dict[str, str], None]:
    wiki_section = find_ru_morpho_section(wiki_section)
    if not wiki_section or not wiki_section.templates:
        return None
    wiki_section = wiki_section.templates
    morpho = parse_morpho(wiki_section[0])
    segments = find_segments(wiki_section)
    if not segments:
        return None
    segments = parse_segments(segments)
    if not segments or len(segments) == 1 and segments["1"] == "":
        return None
    return {
        "morpho": morpho,
        "segments": segments
    }