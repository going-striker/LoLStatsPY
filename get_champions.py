from get_html import get_tbody
from bs4 import BeautifulSoup


def get_champions(lane, region = "global", tier = "emerald_plus", patch = None):
    url = "https://www.op.gg/champions?region={}&tier={}&position={}"
    final_url = url.format(region, tier, lane)
    if patch is not None:
        final_url += f"&patch={patch}"
    tbody = get_tbody(final_url)
    soup = BeautifulSoup(tbody, "html.parser")

    result = list()

    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        champ = (cells[1].get_text(), cells[4].get_text(), cells[5].get_text(), cells[6].get_text())
        result.append(champ)

    return result

