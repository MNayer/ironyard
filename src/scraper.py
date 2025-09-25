import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def get_author(document):
    images = document.find_all("img")
    images = filter(lambda image: image.find_parent("li") is None, images)
    images = list(images)
    assert len(images) == 1, "Found multiple author images."

    image = images[0]
    author = image["alt"].strip()

    return author


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


def parse_table(table):
    rows = table.find_all("tr")
    table_entries = []

    for row in rows:
        entries = row.find_all("td")

        if len(entries) == 0:
            continue

        assert len(entries) == 3, "Invalid number of table entries for at least on row in the publication table."

        publication, cites, year = entries

        publication = publication.find("a").text.strip()
        cites = cites.find("a").text.strip()
        cites = int(cites) if len(cites) > 0 else 0
        year = year.text.strip()
        year = int(year) if len(year) > 0 else 0
        
        table_entries.append(
            {
                "publication": publication,
                "cites": cites,
                "year": year,
            }
        )

    return table_entries


def get_publications(document):
    # Check if there are any publications
    no_publications = document.find("td", string="There are no articles in this profile.")

    if no_publications:
        return []

    table = get_table(document)
    assert table is not None, "Could not find the publication table."

    publications = parse_table(table)

    return publications


def scrape_batch(user_id, start, page_size):
    language = "en"
    url = f"https://scholar.google.de/citations?hl={language}&user={user_id}&sortby=pubdate&cstart={start}&pagesize={page_size}"

    with sync_playwright() as p:
        browser_type = p.firefox
        browser = browser_type.launch()
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # Get author name
    author = get_author(soup)

    # Get publications
    publications = get_publications(soup)

    return {
        "author": author,
        "id": user_id,
        "publications": publications,
    }


def scrape_user(user_id):
    start = 0
    # Max batch size is 100 for Google Scholar
    batch_size = 100

    user_data = scrape_batch(user_id, start, batch_size)
    start += batch_size

    while True:
        batch = scrape_batch(user_id, start, batch_size)
        publications = batch["publications"]

        if len(publications) == 0:
            break

        user_data["publications"] += publications
        start += batch_size

    return user_data


def test():
    #user_data = scrape_user("PyPLDisAAAAJ") # Thorsten
    #user_data = scrape_user("9u16Fm4AAAAJ") # Felix
    user_data = scrape_user("MrYBOTEAAAAJ") # Konrad
    print(json.dumps(user_data, indent=2))


if __name__ == "__main__":
    test()
