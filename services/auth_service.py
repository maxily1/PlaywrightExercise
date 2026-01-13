import os
import allure
from allure_commons.types import AttachmentType
from pages.login_page import LoginPage

@allure.step("Authenticating user from test data")
def authenticate_from_data(page, auth_data: dict):
    if not auth_data.get("enabled", False):
        allure.attach("Authentication skipped (disabled in config)", 
                     name="Auth Status", 
                     attachment_type=AttachmentType.TEXT)
        return

    login_page = LoginPage(page)
    
    with allure.step("Opening login page"):
        login_page.open()
    
    with allure.step(f"Logging in as {auth_data['username']}"):
        login_page.login(
            auth_data["username"],
            auth_data["password"]
        )
    
    allure.attach(
        page.screenshot(),
        name="After Login",
        attachment_type=AttachmentType.PNG
    )

@allure.step("Authenticating user from environment variables")
def authenticate_from_env(page):
    username = os.getenv("EBAY_USERNAME")
    password = os.getenv("EBAY_PASSWORD")

    if not username or not password:
        raise EnvironmentError("Missing EBAY_USERNAME / EBAY_PASSWORD")

    login_page = LoginPage(page)
    
    with allure.step("Opening login page"):
        login_page.open()
    
    with allure.step(f"Logging in as {username}"):
        login_page.login(username, password)

def authenticate(page, auth_config: dict):
    mode = auth_config.get("mode", "guest")
    
    allure.attach(f"Authentication mode: {mode}", 
                 name="Auth Mode", 
                 attachment_type=AttachmentType.TEXT)

    if mode == "data":
        authenticate_from_data(page, auth_config)
    elif mode == "env":
        authenticate_from_env(page)
    elif mode == "guest":
        allure.attach("Proceeding as guest user", 
                     name="Guest Mode", 
                     attachment_type=AttachmentType.TEXT)
        return
    else:
        raise ValueError(f"Unsupported auth mode: {mode}")