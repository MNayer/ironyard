from typing import List, Dict, Set
import datetime as dt
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
    _authors: List[str] = field(repr=False)
    _date: str = field(repr=False)

    def __init__(self, title: str, authors: Set[str], date: dt.date):
        self.title = title
        self.authors = authors
        self.date = date

    @property
    def date(self) -> dt.date:
        return dt.date.fromisoformat(self._date)

    @date.setter
    def date(self, value: dt.date) -> None:
        self._date = value.isoformat()

    @property
    def authors(self) -> Set[str]:
        return set(self._authors)

    @authors.setter
    def authors(self, value: Set[str]) -> None:
        self._authors = list(value)


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
