from abc import ABC, abstractmethod


class PageParser(ABC):

    @abstractmethod
    async def parse(self, url: str) -> list[str]:
        ...
