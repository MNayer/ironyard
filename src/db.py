from typing import List, Dict, Set
from datetime import date
from dataclasses import dataclass, field


@dataclass
class Publication:
    """Information about a specific publiciation."""
    title: str
    cites: int
    year: int

    def __hash__(self):
        return hash(self.title)


@dataclass
class PublicationUpdate:
    """Information about a new publiciation."""
    title: str
    authors: Set[str]
    date: date


@dataclass
class Researcher:
    """Keep track about a researcher's publication record."""
    name: str
    id: str
    publications: List[Publication]


@dataclass
class Database:
    new: Dict[str, PublicationUpdate] = field(default_factory=dict)
    researchers: Dict[str, Researcher] = field(default_factory=dict)
