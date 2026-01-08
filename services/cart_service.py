from pages.product_page import ProductPage
from pages.cart_page import CartPage

def addItemsToCart(page, urls: list[str]):
    product_page = ProductPage(page)

    for idx, url in enumerate(urls):
        page.goto(url)
        product_page.add_to_cart()
        page.screenshot(path=f"reports/item_{idx}.png")


def assertCartTotalNotExceeds(page, budget_per_item: int, items_count: int):
    cart_page = CartPage(page)
    cart_page.open()

    total = cart_page.get_total()
    max_allowed = budget_per_item * items_count

    page.screenshot(path="reports/cart.png")
    assert total <= max_allowed, f"Total {total} exceeds {max_allowed}"
