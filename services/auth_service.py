import os
from pages.login_page import LoginPage

def authenticate_from_data(page, auth_data: dict):
    if not auth_data.get("enabled", False):
        return

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(
        auth_data["username"],
        auth_data["password"]
    )


def authenticate_from_env(page):
    username = os.getenv("EBAY_USERNAME")
    password = os.getenv("EBAY_PASSWORD")

    if not username or not password:
        raise EnvironmentError("Missing EBAY_USERNAME / EBAY_PASSWORD")

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(username, password)


def authenticate(page, auth_config: dict):
    mode = auth_config.get("mode", "guest")

    if mode == "data":
        authenticate_from_data(page, auth_config)
    elif mode == "env":
        authenticate_from_env(page)
    elif mode == "guest":
        return
    else:
        raise ValueError(f"Unsupported auth mode: {mode}")
