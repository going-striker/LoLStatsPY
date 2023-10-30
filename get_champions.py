from get_html import get_tbody
from bs4 import BeautifulSoup


def get_champions(lane, region = "global", tier = "emerald_plus"):
    url = "https://www.op.gg/champions?region={}&tier={}&position={}"
    final_url = url.format(region, tier, lane)
    tbody = get_tbody(final_url)
    soup = BeautifulSoup(tbody, "html.parser")

    result = list()

    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        result.append(cells[1].get_text())

    return result
