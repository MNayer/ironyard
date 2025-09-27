import json
from typing import List
from bs4 import BeautifulSoup
from dataclasses import asdict
from playwright.sync_api import sync_playwright

from db import Researcher, Publication


def get_name(document):
    images = document.find_all("img")
    images = filter(lambda image: image.find_parent("li") is None, images)
    images = list(images)
    assert len(images) == 1, "Found multiple images."

    image = images[0]
    name = image["alt"].strip()

    return name


def get_table(document):
    tables = document.find_all("table")

    for table in tables:
        table_heads = table.find_all("th")
        for table_head in table_heads:
            a_tags = table_head.find_all("a")
            a_tags = filter(lambda tag: tag.text == "Title", a_tags)
            a_tags = list(a_tags)
            if len(a_tags) > 0:
                return table

    return None


def parse_table(table) -> List[Publication]:
    rows = table.find_all("tr")
    publications = []

    for row in rows:
        entries = row.find_all("td")

        if len(entries) == 0:
            continue

        assert (
            len(entries) == 3
        ), "Invalid number of table entries for at least on row in the publication table."

        title, cites, year = entries

        title = title.find("a").text.strip()
        cites = cites.find("a").text.strip()
        cites = int(cites) if len(cites) > 0 else 0
        year = year.text.strip()
        year = int(year) if len(year) > 0 else 0

        publication = Publication(title, cites, year)
        publications.append(publication)

    return publications


def get_publications(document):
    # Check if there are any publications
    no_publications = document.find(
        "td", string="There are no articles in this profile."
    )

    if no_publications:
        return []

    table = get_table(document)
    assert table is not None, "Could not find the publication table."

    publications = parse_table(table)

    return publications


def scrape_batch(user_id, start, page_size) -> Researcher:
    language = "en"
    url = f"https://scholar.google.de/citations?hl={language}&user={user_id}&sortby=pubdate&cstart={start}&pagesize={page_size}"

    with sync_playwright() as p:
        browser_type = p.chromium
        browser = browser_type.launch()
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # Get author name
    name = get_name(soup)

    # Get publications
    publications = get_publications(soup)

    researcher = Researcher(name, user_id, publications)

    return researcher


def scrape_researcher(user_id: str) -> Researcher:
    start = 0
    # Max batch size is 100 for Google Scholar
    batch_size = 100

    researcher = scrape_batch(user_id, start, batch_size)
    start += batch_size

    while True:
        researcher_batch = scrape_batch(user_id, start, batch_size)
        publications = researcher_batch.publications

        if len(publications) == 0:
            break

        researcher.publications += publications
        start += batch_size

    return researcher


def test():
    # researcher = scrape_researcher("PyPLDisAAAAJ") # Thorsten
    # researcher = scrape_researcher("9u16Fm4AAAAJ") # Felix
    researcher = scrape_researcher("MrYBOTEAAAAJ")  # Konrad
    print(json.dumps(asdict(researcher), indent=2))


if __name__ == "__main__":
    test()
