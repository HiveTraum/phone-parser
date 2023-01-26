import asyncio

from playwright.async_api import async_playwright

from domain.interactor import Interactor
from implementations.mock_organization_repository import MockOrganizationRepository
from implementations.playwright_page_parser import PlaywrightPageParser


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page_parser = PlaywrightPageParser(browser)
        organization_repository = MockOrganizationRepository()
        interactor = Interactor(
            page_parser=page_parser,
            organization_repository=organization_repository
        )

        await interactor.start_parsing()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
