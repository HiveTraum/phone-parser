import asyncio

from domain.entities.organization import Organization
from domain.organization_repository import OrganizationRepository
from domain.page_parser import PageParser


class Interactor:

    def __init__(self, page_parser: PageParser, organization_repository: OrganizationRepository):
        self.page_parser = page_parser
        self.organization_repository = organization_repository

    async def start_parsing(self):
        organizations = await self.organization_repository.get_organizations()
        tasks = map(asyncio.create_task, map(self.parse_organization, organizations))
        await asyncio.gather(*tasks)

    async def parse_organization(self, organization: Organization):
        tasks = map(asyncio.create_task, map(self.page_parser.parse, organization.links))
        phones = await asyncio.gather(*tasks)
        phones = [phone for phones_ in phones for phone in phones_]
        if len(phones) == 0:
            # На случай если мы ничего не нашли на странице, есть вероятность, что страница была загружена некорректна.
            # В таком случае полагаемся на следующий запуск парсинга
            return

        organization.phones = phones
        await self.organization_repository.insert_organization(organization)
