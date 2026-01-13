from pages.search_page import SearchPage
import allure
from allure_commons.types import AttachmentType
import json

@allure.step("Searching items by name under price")
def searchItemsByNameUnderPrice(page, query: str, max_price: int, limit: int = 5):
    """
    Search for items under a specific price including shipping costs
    
    :param query: Search query
    :param max_price: Maximum price per item (including shipping)
    :param limit: Number of items to collect
    :return: List of item URLs
    """
    
    # Attach search parameters
    allure.attach(
        json.dumps({
            "query": query,
            "max_price": max_price,
            "limit": limit
        }, indent=2),
        name="Search Parameters",
        attachment_type=AttachmentType.JSON
    )
    
    search_page = SearchPage(page)

    with allure.step(f"Searching for '{query}'"):
        search_page.search(query)
        
    with allure.step(f"Applying max price filter: {max_price} ILS"):
        search_page.apply_max_price_filter(max_price)
    
    with allure.step(f"Collecting up to {limit} items under {max_price} ILS"):
        urls = search_page.collect_item_urls_under_price(
            max_price=max_price,
            limit=limit
        )
    
    # Attach collected URLs
    allure.attach(
        json.dumps({
            "total_items_found": len(urls),
            "urls": urls
        }, indent=2),
        name="Collected Items",
        attachment_type=AttachmentType.JSON
    )
    
    # Take screenshot of search results
    allure.attach(
        page.screenshot(full_page=True),
        name="Search Results Page",
        attachment_type=AttachmentType.PNG
    )
    
    return urls