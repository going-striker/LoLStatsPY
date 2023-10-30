from urllib.request import urlopen

def get_tbody(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    start_tbody_index = html.find("<tbody>")
    end_tbody_index = html.find("</tbody>")
    tbody = html[start_tbody_index:end_tbody_index]
    return tbody