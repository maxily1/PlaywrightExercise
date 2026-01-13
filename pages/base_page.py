from playwright.sync_api import Page
import allure
from allure_commons.types import AttachmentType

class BasePage:
    def __init__(self, page: Page):
        self.page = page
    
    def wait_for_page(self):
        with allure.step("Waiting for page to load"):
            self.page.wait_for_load_state("domcontentloaded")
    
    def click(self, locator: str):
        with allure.step(f"Clicking element: {locator}"):
            self.page.locator(locator).click()

    def fill(self, locator: str, value: str):
        with allure.step(f"Filling '{locator}' with value"):
            # Don't log sensitive data like passwords
            if 'password' not in locator.lower() and 'pass' not in locator.lower():
                allure.attach(value, name="Input Value", attachment_type=AttachmentType.TEXT)
            self.page.locator(locator).fill(value)

    def get_text(self, locator: str) -> str:
        with allure.step(f"Getting text from: {locator}"):
            text = self.page.locator(locator).inner_text()
            allure.attach(text, name="Retrieved Text", attachment_type=AttachmentType.TEXT)
            return text
    
    def take_screenshot(self, name: str):
        """Take and attach screenshot to Allure report"""
        with allure.step(f"Taking screenshot: {name}"):
            screenshot = self.page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name=name,
                attachment_type=AttachmentType.PNG
            )