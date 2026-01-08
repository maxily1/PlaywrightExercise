from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page
    
    def wait_for_page(self):
        self.page.wait_for_load_state("domcontentloaded")
    
    def click(self, locator: str):
        self.page.locator(locator).click()

    def fill(self, locator: str, value: str):
        self.page.locator(locator).fill(value)

    def get_text(self, locator: str) -> str:
        return self.page.locator(locator).inner_text()
    
    def screenshot(self, name: str):
        self.page.screenshot(path=f"/report/{name}.png")
