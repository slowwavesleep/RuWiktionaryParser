from src.generation import segment_stem
from src.segmentation import clean_segments
from src.utils.etc import determine_pos, basic_json_read, read_redirects, replace_redirect, basic_filter
from constants import WRITE_PATHS, INVARIABLE_POS, IGNORE_POS, SEGMENT_SEPARATOR


def process_article(article, temps, *, sep: str = SEGMENT_SEPARATOR):
    title = article["title"]
    stems = article["morpho"]["stems"]
    pos = determine_pos(article)
    if pos in IGNORE_POS:
        return {}
    if pos in INVARIABLE_POS:
        segmented_forms = {"lemma": clean_segments(article["segments"])}
        return segmented_forms
    # nouns with one stem
    if pos == "noun" and len(stems) == 1:
        segments = clean_segments(article["segments"])
        stem = list(stems.values())[0]
        print(title)
        print(segment_stem(stem, segments))
    elif len(stems) > 1:
        pass


articles = basic_json_read(WRITE_PATHS["article"])
templates = basic_json_read(WRITE_PATHS["template"])
redirects = read_redirects(WRITE_PATHS["template_redirect"])

articles = [replace_redirect(article, redirects) for article in articles]

for article in articles:
    if basic_filter(article):
        # stems = article["morpho"]["stems"]
        # if all_stems_filled(stems) and len(stems) > 2:
        #     print(stems)
        process_article(article, templates)


