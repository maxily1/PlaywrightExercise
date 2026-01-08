from utils.price_utils import parse_price

class SearchPage:
    def __init__(self, page):
        self.page = page

    def search(self, query: str):
        self.page.fill("input[aria-label='Search for anything']", query)
        self.page.keyboard.press("Enter")
        self.page.wait_for_load_state("domcontentloaded")

    def apply_max_price_filter(self, max_price: int):
        self.page.fill("input[name='_udhi']", str(max_price))
        self.page.click("button[aria-label='Submit price range']")
        self.page.wait_for_load_state("domcontentloaded")

    def collect_item_urls_under_price(self, max_price: int, limit: int):
        urls = []

        while len(urls) < limit:
            items = self.page.locator("//li[contains(@class,'s-item')]")

            for i in range(items.count()):
                if len(urls) >= limit:
                    break

                price_text = items.nth(i).locator(".s-item__price").inner_text()
                price = parse_price(price_text)

                if price is not None and price <= max_price:
                    url = items.nth(i).locator("a.s-item__link").get_attribute("href")
                    urls.append(url)

            next_btn = self.page.locator("//a[contains(@aria-label,'Next')]")
            if next_btn.count() == 0:
                break

            next_btn.click()
            self.page.wait_for_load_state("domcontentloaded")

        return urls
