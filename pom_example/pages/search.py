from playwright.sync_api import Page


class HuelSearch:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.search_icon = page.get_by_test_id("IconLink-Search")
        self.search_input = page.get_by_test_id("SearchBar__input")

    def load(self) -> None:
        self.page.goto("https://huel.com/")

    def search(self, text: str) -> None:
        self.search_icon.click()
        self.search_input.click()
        self.search_input.fill(text)
        self.search_input.press("Enter")
