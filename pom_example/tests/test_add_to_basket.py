"""
This is an example of implementing a project object model.
"""

from playwright.sync_api import expect, Page
from pages.search import HuelSearch


def test_add_to_basket(page: Page) -> None:
    # Test data
    product = {
        "name": "Complete Nutrition Bar",
        "flavour": "Dark Chocolate Raspberry",
        "quantity": 2,
    }

    # Step 1: Navigate to Huel homepage
    main_page = HuelSearch(page)
    main_page.load()

    # Step 2: Accept cookies if present
    main_page.accept_cookies()

    # Step 3: Search for product name
    main_page.search(product["name"])
