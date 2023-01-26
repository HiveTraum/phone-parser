from asyncio import sleep

import phonenumbers
from playwright.async_api import Browser, Page

from domain.page_parser import PageParser

PHONE_REGEXP = r"/(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}/i"
HIDDEN_PHONE_TEXT_BUTTON = {"показать телефон"}


class PlaywrightPageParser(PageParser):

    def __init__(self, browser: Browser):
        self.browser = browser

    async def parse(self, url: str) -> list[str]:
        page = await self.browser.new_page()
        phones: list[str] = []
        try:
            await page.goto(url, wait_until="networkidle")
            await self._reveal_hidden_phones(page)
            element = page.locator(f"text={PHONE_REGEXP}")

            for phone_element_candidate in await element.all():
                text_containing_potential_phones = await phone_element_candidate.inner_text()
                potential_phones = text_containing_potential_phones.split("\n")
                phones.extend(self._parse_phone(potential_phones))
        except Exception as exc:
            await page.close()
            raise exc

        return phones

    @staticmethod
    def _parse_phone(potential_phones: list[str]) -> list[str]:
        """
        Парсинг найденных телефонов
        """
        phones: list[str] = []
        for potential_phone in potential_phones:
            phone_obj = phonenumbers.parse(potential_phone, "RU")
            phone = phonenumbers.format_number(phone_obj, phonenumbers.PhoneNumberFormat.NATIONAL)
            phone = phone.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
            phones.append(phone)
        return phones

    @staticmethod
    async def _reveal_hidden_phones(page: Page):
        """
        Ищем возможные кнопки для раскрытия скрытых номеров
        """

        potential_hidden_phone_buttons = await page.get_by_role("button").all()
        for potential_hidden_phone_button in potential_hidden_phone_buttons:
            inner_text = await potential_hidden_phone_button.inner_text()
            texts = set(inner_text.lower().split("\n"))
            if not texts.intersection(HIDDEN_PHONE_TEXT_BUTTON):
                continue

            await potential_hidden_phone_button.click()

        await sleep(3)
