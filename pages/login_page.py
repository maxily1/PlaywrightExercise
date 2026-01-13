from pages.base_page import BasePage

class LoginPage(BasePage):
    """This is the login page structure and functions."""
    def open(self):
        """Open the login page"""
        self.page.goto("https://www.ebay.com/signin")

    def login(self, username: str, password: str):
        """
        The login function to ebay platform.
        
        :param username: The mail to the platform.
        :type username: str
        :param password: The password to the platform.
        :type password: str
        """
        
        self.page.fill('#userid', username)
        self.page.click("#signin-continue-btn")

        self.page.fill('#pass', password)
        self.page.click('#sgnBt')

