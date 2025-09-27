from typing import List
from dataclasses import dataclass


@dataclass
class Publication:
    """Information about a specific publiciation."""
    title: str
    cites: int
    year: int

    def __hash__(self):
        return hash(self.title)


@dataclass
class Researcher:
    """Keep track about a researcher's publication record."""
    name: str
    id: str
    publications: List[Publication]
