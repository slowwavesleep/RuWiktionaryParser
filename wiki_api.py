import requests
import pandas as pd
import json

USER_AGENT = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/74.0.3729.169 Safari/537.36'}

TEST_WORDS = [
    "дар",
    "друг",
    "заживо",
    "доха",
    "муж",
    "ребёнок",
    "младенец",
    "лужа",
    "крыша",
    "звезда"
]


def get_url(title):
    return f"https://ru.wiktionary.org/w/api.php?action=parse&page={title}&prop=text&formatversion=2&format=json"


def request_text(title):
    url = get_url(title)
    html = requests.get(url, headers=USER_AGENT)
    return html.text


def get_morpho_table(title):
    text = request_text(title)
    text = json.loads(text)["parse"]["text"]
    try:
        table = pd.read_html(text, attrs={'class': 'morfotable ru'})[0]
        return table
    except ValueError:
        pass


for word in TEST_WORDS:
    print(word)
    print(get_morpho_table(word))

