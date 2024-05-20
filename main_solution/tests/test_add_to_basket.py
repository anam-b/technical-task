"""
This test adds specific items to a basket, then verifies items in basket.
"""

from playwright.sync_api import expect, Page


def test_add_to_basket(page: Page) -> None:
    # Test data
    products = [
        {
            "name": "Huel Instant Meal Cups",
            "flavour": "Chick'n Alfredo Pasta",
            "quantity": 1,
        },
        {
            "name": "Huel Complete Nutrition Bar",
            "flavour": "Dark Chocolate Raspberry",
            "quantity": 2,
        },
        {
            "name": "Huel Ready-to-drink",
            "flavour": "Iced Coffee Caramel",
            "quantity": 1,
        },
        {
            "name": "Huel Complete Protein",
            "flavour": "Banana Pudding",
            "quantity": 2,
        },
    ]

    # Step 1: Navigate to Huel homepage in a headless browser
    page.goto("https://huel.com/")

    # Accept cookies if present
    try:
        expect(page.get_by_test_id("acceptCookieButton")).to_be_visible()
        page.get_by_test_id("acceptCookieButton").click()
    except AssertionError as e:
        print("Accept cookies button not visible:", e)
    except TimeoutError as e:
        print("Accept cookies button timeout:", e)

    for product in products:
        # Step 2: Search for specific product
        search_bar = page.get_by_test_id("SearchBar__input")

        page.get_by_test_id("IconLink-Search").click()
        search_bar.click()
        search_bar.fill(product["name"])
        search_bar.press("Enter")

        # Check if product name is part of the search results
        try:
            expect(
                page.get_by_role("link", name=product["name"], exact=True)
            ).to_be_visible(timeout=8000)
        except AssertionError as e:
            print("Product name element not found:", e)
            raise
        except TimeoutError as e:
            print("Element failed to load:", e)
            raise

        # Step 3: Open product page
        page.get_by_role("link", name=product["name"], exact=True).click()

        # Check if product flavour exists
        flavour_title = page.locator(".FlavourPicker__title-qty:visible").filter(
            has_text=product["flavour"]
        )
        flavour_card = page.get_by_role("listitem").filter(has=flavour_title)

        try:
            expect(flavour_title).to_be_visible(timeout=8000)
        except AssertionError as e:
            print("Product flavour element not found:", e)
            raise
        except TimeoutError as e:
            print("Element failed to load:", e)
            raise

        # Check if flavour is out of stock
        try:
            expect(flavour_card).not_to_contain_text("out of stock", ignore_case=True)
        except AssertionError as e:
            print("Flavour out of stock:", e)
            raise

        # Step 4: Select flavour and quantity
        page.get_by_role("button", name=product["flavour"]).click(
            click_count=product["quantity"]
        )

        # Step 5: Add to basket with default purchase type (subscription)
        continue_btn = page.get_by_role("button", name="Continue")

        continue_btn.click()
        continue_btn.click()

        # Ensure confirmation page has finished loading, otherwise search can be interrupted
        page.wait_for_url("**/pages/cross-sell")

    # Step 5: Open basket
    page.get_by_test_id("IconLink-Cart").click()

    # Step 6: Verify number of products in basket
    try:
        expect(page.locator(".CartMixAndMatchBundle__items > li")).to_have_count(
            len(products)
        )
    except AssertionError as e:
        print("Number of items in basket does not match number of products:", e)
        raise
