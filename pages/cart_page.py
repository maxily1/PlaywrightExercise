from utils.price_utils import parse_price

class CartPage:
    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto("https://cart.ebay.com")
        self.page.wait_for_load_state("domcontentloaded")

    def get_total(self):
        total_text = self.page.locator(
            "//span[contains(@class,'total-price')]"
        ).inner_text()
        return parse_price(total_text)
