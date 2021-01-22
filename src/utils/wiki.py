from typing import Union, Dict, List
import re

from wikitextparser import Section, Template
from wikitextparser import WikiText


# TODO Consider synonymy, i.e. multiple sections for one word
def find_ru_section(wiki_text: WikiText) -> Union[Section, None]:
    """
    Attempts to find Russian language section in a given
    parsed wiki text.
    :param wiki_text: parsed wiki text
    :return: None or found section
    """
    sections = wiki_text.get_sections()
    sections = [sec for sec in sections if sec.level == 1 and '{{-ru-}}' in sec.title]
    if len(sections) == 1:
        return sections[0]
    else:
        return None


def find_ru_morpho_section(wiki_text: WikiText) -> Union[Section, None]:
    """
    Attempts to find a section pertaining to Russian morphology within
    parsed wiki text.
    :param wiki_text: parsed wiki text
    :return: None or found section
    """
    sections = wiki_text.get_sections()
    sections = [sec for sec in sections if 'Морфологические и синтаксические свойства' in str(sec.title)]
    if len(sections) == 1:
        return sections[0]
    else:
        return None


def clean_template_name(template: str) -> str:
    """
    Removes unnecessary symbols from template name
    to achieve uniformity in naming.
    :param template: raw template name as a string
    :return: cleaned template name
    """
    template = template.replace("Шаблон:", "").strip("\n").strip()

    # comment = re.compile(r"<!--.*?-->")
    # template = comment.sub("", template)

    whitespace = re.compile(r"\s+")
    template = whitespace.sub(" ", template)
    return template.strip()


def parse_morpho(temp: Template) -> Dict[str, Union[str, dict]]:
    """
    Extracts template name and stems for a given word from a
    parsed wikitext morphology template.
    :param temp: an instance of wikitextparser Template class
    :return: a dictionary containing template name and stems
    """
    temp_name = clean_template_name(temp.name)
    # some templates use some arcane script
    # to generate actual word forms, thus it's not
    # worth the effort trying to implement that
    # functionality here
    # other templates generally have arguments with the
    # word `основа` in them, so if no such arguments were
    # found, then these words will be ignored further on
    args = temp.arguments
    stems = {arg.name.strip("\n").strip(): arg.value.strip("\n")
             for arg in args if "основа" in arg.name}
    return {
        "template": temp_name,
        "stems": stems
    }


def find_segments(templates: List[Template]) -> Union[Template, None]:
    """
    Attempts to find the morpheme division template in a list
    of parsed templates.
    :param templates: a list of templates extracted from parsed wiki text
    :return: either None or the relevant template
    """
    segments = [temp for temp in templates if "морфо-ru" in temp.name]
    if len(segments) == 1:
        return segments[0]
    else:
        return None


def parse_segments(temp: Template) -> Union[Dict[str, str], None]:
    """
    Transforms given morpheme division template into a dictionary.
    Return None if the template has no arguments.
    :param temp: morpheme division template
    :return: either None or a dictionary containing template argument
    names and their values
    """
    assert "морфо-ru" in temp.name
    args = temp.arguments
    # some templates are empty and have no arguments
    # these are useless
    if not len(args) > 0:
        return None
    segments = {segment.name: segment.value for segment in args}
    # some templates have arguments but no values for them
    # these are also useless
    if not any(segments.values()):
        return None
    return segments


def parse_ru_section(wiki_section: Section) -> Union[Dict[str, str], None]:
    """
    Processes the entire Russian language section of an article.
    Return a dictionary with morphological information and morpheme segmentation.
    :param wiki_section: a wiki text section in Russian language
    :return: a dictionary with relevant information or None
    """
    # try to find morphological section
    # generally, it should be present in all articles
    wiki_section = find_ru_morpho_section(wiki_section)
    # return None if no such section was found or if
    # it contains no templates
    if not wiki_section or not wiki_section.templates:
        return None
    # deal with templates found
    wiki_section = wiki_section.templates
    # the morphological template should be the first one
    # in the relevant section; it cannot be identified by name
    morpho = parse_morpho(wiki_section[0])
    # the template with morphemes can be found by name
    segments = find_segments(wiki_section)
    # return None if no such template is found
    # because that's what we're trying to extract from the dump
    if not segments:
        return None
    # convert template to Python dictionary
    segments = parse_segments(segments)
    # sometimes this template is completely empty
    # or filled with empty elements
    # naturally, that's not very useful
    if not segments or len(segments) == 1 and segments["1"] == "":
        return None
    return {
        "morpho": morpho,
        "segments": segments
    }


def parse_template_page(wiki_text: WikiText) -> Union[dict, None]:
    """
    Convert the entire template page to a single dictionary.
    :param wiki_text: parsed wiki text of a template page
    :return: a dict or None
    """
    templates = wiki_text.templates
    # in general, that shouldn't happen
    if not templates:
        return None
    # for our purposes we expect a template page
    # containing just one template
    # template pages not satisfying this condition
    # are likely irrelevant
    if len(templates) > 1:
        return None
    # templates attribute always return a list
    # so we need to take out the only element
    template = templates[0]
    return {"template": template_to_dict(template)}


def remove_no_include(raw_template_page: str) -> str:
    """
    wikitextparser can't parse templates with `<noinclude>`
    tags in them. This function removes these tags and their
    contents.
    :param raw_template_page: unprocessed text body of a template page
    :return: the same text body with tags removed
    """
    pattern = re.compile(r"<noinclude>.*?</noinclude>")
    lines = raw_template_page.split("\n")
    output = []
    for line in lines:
        line = re.sub(pattern, "", line)
        if line:
            output.append(line)
    return "\n".join(output)


def template_to_dict(template: Template) -> dict:
    """
    A simple function to convert a parsed template into a dictionary.
    :param template: parsed wiki template
    :return: a dictionary with the contents of the template
    """
    output = {}
    for arg in template.arguments:
        output[arg.name.strip("\n").strip()] = arg.value.strip("\n")
    return output
