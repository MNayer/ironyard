import json
import re
import yaml
import time
import logging
import functools as ft
from typing import List
from pathlib import Path
from dataclasses import asdict
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler

from db import Researcher, PublicationUpdate, Database
from scraper import scrape_researcher
from screen import Screen
from render import render_new_publications, render_default

log = logging.getLogger(__name__)

CONFIG_PATH = "./config.yml"

class DatabaseManager:

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db = Database()


    def load(self):
        if not self.db_path.exists():
            return

        db_data = self.db_path.read_text()
        self.db = json.loads(db_data)


    def update(self, researcher: Researcher):
        if researcher.id not in self.db.researchers:
            self.db.researchers[researcher.id] = researcher
            return

        # Sanity check
        if len(researcher.publications) < len(self.db.researchers[researcher.id].publications) * 0.9:
            log.warning(f"The number of publications from '{researcher.name}' with id '{researcher.id}' would decrease significantly upon update. Skipping.")
            return


        # Update the new publications
        old_researcher = self.db.researchers[researcher.id]
        old_publications = old_researcher.publications
        publication_diff = set(researcher.publications) - set(old_publications)

        for publication in publication_diff:
            if publication.title not in self.db.new:
                self.db.new[publication.title] = PublicationUpdate(
                    title=publication.title,
                    authors=set(researcher.name),
                    date=date.today(),
                )
                continue

            self.db.new[publication.title].authors.add(researcher.name)

        # Update the researcher
        self.db.researchers[researcher.id] = researcher


    def get_new_publications(self):
        return self.db.new


    def save(self):
        pass


    def to_dict(self) -> dict:
        db_dict = {
            id: asdict(researcher) for id, researcher in self.db.items()
        }
        return db_dict


    def show(self):
        print(json.dumps(self.to_dict(), indent=2))


def load_config(config_path: Path) -> dict:
    config_data = config_path.read_text()
    config = yaml.safe_load(config_data)
    return config


def extract_researcher_ids(researcher_urls: List[str]) -> List[str]:
    researcher_ids = map(lambda url: re.match(r".*user=([^&]+)", url), researcher_urls)
    researcher_ids = filter(lambda match: match is not None, researcher_ids)
    researcher_ids = map(lambda match: match.group(1), researcher_ids)
    researcher_ids = list(researcher_ids)
    assert len(researcher_urls) == len(researcher_ids), "Could not parse all researcher URLs."
    return researcher_ids


def update(screen):
    # Load config
    config_path = Path(CONFIG_PATH)
    config = load_config(config_path)

    if config["noscrape"]:
        log.warning("Scraping is disabled. With this setting, new publications are not retrieved. Only set this for debugging purposes.")

    # Extract the researcher IDs
    researcher_ids = extract_researcher_ids(config["researchers"])

    # Load/create database file
    db_path = Path(config["dbpath"])
    db = DatabaseManager(db_path)
    db.load()

    # Scrape for new publications
    if not config["noscrape"]:
        for researcher_id in researcher_ids:
            researcher = scrape_researcher(researcher_id)
            db.update(researcher)

    new_publications = db.get_new_publications()

    if config["test"]:
        new_publications["LLM-based Vulnerability Discovery through the Lens of Code Metrics"] = PublicationUpdate(
                    title="LLM-based Vulnerability Discovery through the Lens of Code Metrics",
                    authors=set(["Thorsten Eisenhofer"]),
                    date=date.today(),
                )
        new_publications["Adversarial Observations in Weather Forecasting"] = PublicationUpdate(
                    title="Adversarial Observations in Weather Forecasting",
                    authors=set(["Thorsten Eisenhofer", "Erik Imgrund"]),
                    date=date.today(),
                )
        new_publications["This should not appear"] = PublicationUpdate(
                    title="This should not appear",
                    authors=set(["Thorsten Eisenhofer", "Erik Imgrund"]),
                    date=date(1999, 1, 1),
                )

    # Filter new publications to only include the most recent ones
    current_date = date.today()
    max_delta = config["shownewfordays"]
    new_publications = filter(lambda publication: (current_date - publication.date).days < max_delta, new_publications.values())
    new_publications = list(new_publications)

    if len(new_publications) > 0:
        images = render_new_publications(new_publications)

        for image in images:
            screen.update(image)
            time.sleep(config["show"])
    else:
        image = render_default()
        screen.update(image)


def start():
    # Load config
    config_path = Path(CONFIG_PATH)
    config = load_config(config_path)

    # Setup screen
    screen = Screen()

    if config["runonce"]:
        update(screen)
        screen.shutdown()
        return

    scheduler = BlockingScheduler()
    scheduler.add_job(ft.partial(update, screen=screen), "cron", hour="9,15,18,21")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        screen.shutdown()


if __name__ == "__main__":
    start()
