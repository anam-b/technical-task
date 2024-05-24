## Approach
The main solution to the script is in the folder `main_solution`.

The requirement is a single test which follows straightforward steps, so a design pattern isn't necessary for organising and maintaining the test scripts. However, in `pom_example`, I've also included an example of implementing a page object model for the search functionality, encapsulating interactions related to searching products. While it improves readability and scalability, it also introduces too much abstraction for a single test case.

The script:
1. **Stores the test data in a list of dictionaries.**  
Only two products are needed for the test, and each product has a *name*, *flavour*, and *quantity*, so a list of dictionaries is a convenient way to store and/or modify the test data. If a larger data set is needed, an external file would be more suitable.
The focus of the test is the functionality to add products to the basket (as opposed to the search, for example), so specific product names and flavours are provided as part of the test data.
2. **Navigates to the Huel homepage.**  
Playwright runs tests in a headless browser within a unique browser context by default.
3. **Accepts cookies, if present.**  
	If a product quantity is selected, the cookies overlay obstructs the 'Complete' button required to proceed to checkout.
	The overlay is shown predictably, so it can be dismissed as part of the test flow, which is recommended in the [Playwright documentation](https://playwright.dev/python/docs/api/class-page#page-add-locator-handler).
	Cookies aren't essential to the test, so if the button element can't be located for whatever reason, the relevant errors (AssertionError, TimeoutError) are handled through exceptions.
4. **Finds and adds products to a basket.**  
	Since the same actions are completed for each product, this is achieved through a `for loop`. The loop doesn't complicate the code, and can be used to dynamically iterate over a list of test data.
	
	The steps are:
	1. Search for the product name.  
	2. Verify that the product name is part of the search result links. If it isn't, an exception is raised and the script terminates.  
	  Search results can at times take a bit longer to load, especially in headed mode, so the timeout has been increased to ensure errors don't occur pre-emptively. 
	  The name match needs to be exact. I considered a few alternatives to this, but decided that ensuring the test data is accurate and up-to-date is the most straightforward way to find the relevant link within the current results page layout. Other solutions I came up with add complexity in a part of the test where it isn't needed.
	1. Open the product page.  
	2. Verify that the expected flavour exists *and* is in stock. If it isn't, an exception is raised and the script terminates.  
	  Product pages can at times take a bit longer to load, especially in headed mode, so the timeout has been increased to ensure errors don't occur pre-emptively.  
	5. Select desired quantity of the flavour.  
	6. Add the search product to the basket.  
	7. Wait for the confirmation page to load. Otherwise, the navigation bar loads first, so the search steps for the next product are initiated, but at times the search is disrupted when the rest of the page finishes loading.  
5. **Open the basket.**  
6. **Verify that the number of *products* in the basket matches the number of products in the test data.** If it doesn't, an exception is raised and the script terminates.  

### Locators
Test IDs provide a reliable way to locate elements, so they have been prioritised. At times, user-facing attributes and explicit contracts are used as recommended in the [Playwright documentation](https://playwright.dev/docs/locators).

### Notes
The script doesn't work with the [Black Edition Ready-to-Drink](https://huel.com/products/huel-black-edition-ready-to-drink?_pos=1&_sid=fb33d8ec6&_ss=r) product page from the search result due to its layout.

## Improvements
- **Logging errors:** In the current script, when an exception is raised, a print statement is executed. For more complex projects or more flexible messages, the [logging module](https://docs.python.org/3/library/logging.html) can be used instead.  
- **Design pattern:** As mentioned in the approach.
