from pages.search_page import SearchPage

def searchItemsByNameUnderPrice(page, query: str, max_price: int, limit: int = 5):
    search_page = SearchPage(page)

    search_page.search(query)
    search_page.apply_max_price_filter(max_price)

    return search_page.collect_item_urls_under_price(
        max_price=max_price,
        limit=limit
    )
