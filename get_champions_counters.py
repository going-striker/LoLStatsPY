from get_html import get_tbody
from bs4 import BeautifulSoup

def get_champion_counters(champion, lane, region = "global", tier="emerald_plus", patch = None):
    url = "https://www.op.gg/champions/{}/counters/{}?region={}&tier={}"
    if patch is not None:
        url += f"&patch={patch}"
    final_url = url.format(champion, lane, region, tier)
    tbody = get_tbody(final_url)
    soup = BeautifulSoup(tbody, "html.parser")

    result = dict()

    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        result[cells[1].get_text()] = (cells[2].get_text(), cells[3].get_text())

    return result

