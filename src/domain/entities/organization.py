from dataclasses import dataclass


@dataclass
class Organization:
    id: str
    name: str
    links: list[str]
    phones: list[str]
