import json
import pytest
import allure
from allure_commons.types import AttachmentType
from services.auth_service import authenticate
from services.search_service import searchItemsByNameUnderPrice
from services.cart_service import addItemsToCart, assertCartTotalNotExceeds

@allure.feature("E2E Shopping Flow")
@allure.story("Complete Purchase Flow")
@allure.title("End-to-End eBay Shopping Test")
@allure.description("""
This test validates the complete shopping flow on eBay:
1. Navigate to eBay homepage
2. Authenticate (if configured)
3. Search for products with price filtering
4. Add items to cart
5. Verify cart total is within budget
""")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
def test_full_e2e_flow(page):
    """
    Complete E2E test for eBay shopping flow
    
    Test Steps:
    - Load test configuration
    - Navigate to eBay
    - Authenticate user
    - Search for items under specified price
    - Add items to shopping cart
    - Verify total price is within budget
    """
    
    with allure.step("Loading test configuration"):
        with open("data/test_data.json") as f:
            data = json.load(f)
        
        # Attach test configuration
        allure.attach(
            json.dumps(data, indent=2),
            name="Test Configuration",
            attachment_type=AttachmentType.JSON
        )
        
        # Set dynamic parameters
        allure.dynamic.parameter("Search Query", data["search"]["query"])
        allure.dynamic.parameter("Max Price", f"{data['search']['max_price']} ILS")
        allure.dynamic.parameter("Items Limit", data["search"]["limit"])

    with allure.step("Navigating to eBay homepage"):
        page.goto("https://www.ebay.com")
        page.wait_for_load_state("domcontentloaded")
        
        allure.attach(
            page.screenshot(full_page=True),
            name="eBay Homepage",
            attachment_type=AttachmentType.PNG
        )

    with allure.step("User Authentication"):
        authenticate(page, data["auth"])

    with allure.step("Searching for products"):
        urls = searchItemsByNameUnderPrice(
            page,
            data["search"]["query"],
            data["search"]["max_price"],
            data["search"]["limit"]
        )
        
        allure.dynamic.parameter("Items Found", len(urls))
        
        if len(urls) == 0:
            allure.attach(
                "No items found matching the criteria",
                name="Search Result",
                attachment_type=AttachmentType.TEXT
            )
            pytest.skip("No items found under specified price")

    with allure.step(f"Adding {len(urls)} items to cart"):
        addItemsToCart(page, urls)

    with allure.step("Verifying cart total"):
        assertCartTotalNotExceeds(
            page,
            data["search"]["max_price"],
            len(urls)
        )
    
    with allure.step("Test completed successfully"):
        allure.attach(
            "✓ All assertions passed\n"
            "✓ Items added to cart successfully\n"
            "✓ Cart total is within budget",
            name="Test Summary",
            attachment_type=AttachmentType.TEXT
        )