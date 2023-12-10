from dataclasses import dataclass


@dataclass
class SitemapItem:
    location: str


@dataclass
class LocationItem:
    link: str


@dataclass
class LocationItemInfo:
    name: str
    description: str
    id: str
