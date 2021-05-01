# RuWiktionaryParser

## Data extraction
The first step of the process is the extraction of the data from the downloaded Wiktionary dump.
The most recent version can be found [here](https://dumps.wikimedia.org/backup-index.html). You'll want
the pages-articles version of the dump which hash the following name format: 
__ruwiktionary-{date}-pages-articles.xml.bz2__. You don't need to unpack it. Just put it in a desired
directory, then specify the path in the [config.yml](config.yml) file.

After running the following command (it should take approximately 10 minutes):
### Extract data from the dump
```
python extract_from_dump.py
```
Three files will be generated in the `tmp` folder: `articles.jsonl`, `templates.jsonl`,
and `template_redirects.jsonl`

### Some examples of the format

#### An article
```
{
  "morpho": {
    "template": "сущ ru m ina 1a",
    "stems": {
      "основа": "перево́д"
    },
    "alternate": {},
    "forms": {},
    "info": {
      "слоги": "{{по-слогам|пе|ре|во́д}}"
    }
  },
  "segments": {
    "1": "пере-",
    "2": "вод",
    "и": "т"
  },
  "id": 3941,
  "title": "перевод",
  "type": "article",
  "is_proper": false,
  "is_obscene": false,
  "has_homonyms": false
}
```

#### A template

```
{
  "template": {
    "case": "{{{case|}}}",
    "form": "{{{form|}}}",
    "nom-sg": "{{{основа}}}я",
    "nom-pl": "{{{основа}}}и",
    "gen-sg": "{{{основа}}}и",
    "gen-pl": "{{{основа1}}}ь",
    "dat-sg": "{{{основа}}}е",
    "dat-pl": "{{{основа}}}ям",
    "acc-sg": "{{{основа}}}ю",
    "acc-pl": "{{{основа}}}и",
    "ins-sg": "{{{основа}}}ей",
    "ins-sg2": "{{{основа}}}ею",
    "ins-pl": "{{{основа}}}ями",
    "prp-sg": "{{{основа}}}е",
    "prp-pl": "{{{основа}}}ях",
    "loc-sg": "{{{М|}}}",
    "voc-sg": "{{{З|}}}",
    "prt-sg": "{{{Р|}}}",
    "П": "{{{П|}}}",
    "hide-text": "{{{hide-text|}}}",
    "слоги": "{{{слоги|}}}",
    "дореф": "{{{дореф|}}}",
    "Сч": "{{{Сч|}}}",
    "st": "{{{st|}}}",
    "pt": "{{{pt|}}}",
    "затрудн": "{{{затрудн|}}}",
    "коммент": "{{{коммент|}}}",
    "зачин": "{{{зачин|}}}",
    "клитика": "{{{клитика|}}}",
    "кат": "неодуш",
    "род": "{{{род|жен}}}",
    "скл": "1",
    "зализняк": "2*a^",
    "чередование": "1"
  },
  "id": 15763,
  "title": "сущ ru f ina 2*a^",
  "type": "template"
}
```
#### A template redirect
```
{
  "id": 836905,
  "title": "сущ ru f ina 2*a-ня(2)",
  "redirect_title": "сущ ru f ina 2*a(2)-ня",
  "type": "template_redirect"
}
```

Suppose that the extracted data in this form may have its uses. Do note, however, that homonymous
lemmas _are currently not accounted for_. This means that if a certain page has articles for several
word senses, then only the first one will be saved.

## Generating Word Forms
The main purpose of this project is to generate word forms with morpheme boundaries marked using the provided
wiki-templates and segmented lemmas. To do this, some preliminary steps are required.

*Note:* only nouns are supported at the moment.

### Process the templates
This will filter and reformat `templates.jsonl`.
```
python process_templates.py
```

### Process the articles
This will clean up and enrich `articles.json`. 
```
python process_articles.py
```

The results of the last two steps will be saved in `tmp/processed/` folder by default.

#### Generate the segmented noun word forms
This will use the processed files to generate word forms (where possible).
```
python generate_nouns.py
```
The output is saved to `result/processed_articles.jsonl` by default. The file should
contain approximately 500 thousand noun word forms.
