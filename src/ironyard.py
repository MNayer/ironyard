import json
import re
import yaml
import time
import logging
from typing import List
from pathlib import Path
from dataclasses import asdict
from collections import defaultdict

from db import Researcher, Publication
from scraper import scrape_researcher
from screen import Screen
from render import render_new_publications

log = logging.getLogger(__name__)


class Database:

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db = {}


    def load(self):
        if not self.db_path.exists():
            return

        db_data = self.db_path.read_text()
        self.db = json.loads(db_data)


    def get_publication_diff(self, researcher) -> List[Publication]:
        if researcher.id not in self.db:
            return []

        old_researcher = self.db[researcher.id]
        old_publications = old_researcher.publications
        publication_diff = set(researcher.publications) - set(old_publications)

        return list(publication_diff)


    def update(self, researcher: Researcher):
        if researcher.id not in self.db:
            self.db[researcher.id] = researcher
            return

        # Sanity check
        if len(researcher.publications) < len(self.db[researcher.id].publications) * 0.9:
            log.warning(f"The number of publications from '{researcher.name}' with id '{researcher.id}' would decrease significantly upon update. Skipping.")
            return

        self.db[researcher.id] = researcher


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


def test():
    # Setup Screen
    screen = Screen()

    # Load config
    config_path = Path("./config.yml")
    config = load_config(config_path)

    # Extract the researcher IDs
    researcher_ids = extract_researcher_ids(config["researchers"])

    # Load/create database file
    db_path = Path(config["dbpath"])
    db = Database(db_path)
    db.load()

    new_publications = defaultdict(set)

    # TODO: USE
    #for researcher_id in researcher_ids:
    #    researcher = scrape_researcher(researcher_id)
    #    researcher_new_publications = db.get_publication_diff(researcher)

    #    for publication in researcher_new_publications:
    #        new_publications[publication.title].add(researcher.name)

    #    db.update(researcher)

    # TODO: REMOVE
    new_publications["LLM-based Vulnerability Discovery through the Lens of Code Metrics"] = set(["Thorsten Eisenhofer"])
    new_publications["Adversarial Observations in Weather Forecasting"] = set(["Thorsten Eisenhofer", "Erik Imgrund"])

    if len(new_publications) > 0:
        images = render_new_publications(new_publications)

        for image in images:
            screen.update(image)
            time.sleep(config["show"])


if __name__ == "__main__":
    test()
