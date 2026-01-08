import random
from playwright.sync_api import Page

class ProductPage:
    def __init__(self, page: Page):
        self.page = page

    def select_random_variants(self):
        selects = self.page.locator("select")
        for i in range(selects.count()):
            options = selects.nth(i).locator("option")
            if options.count() > 1:
                selects.nth(i).select_option(
                    index=random.randint(1, options.count() - 1)
                )

    def add_to_cart(self):
        self.select_random_variants()
        self.page.click("text=Add to cart")
        self.page.wait_for_load_state("domcontentloaded")
