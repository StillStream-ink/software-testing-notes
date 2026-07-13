import pytest
from playwright.sync_api import sync_playwright
import sys
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def page():
    """每个测试用例独立浏览器实例"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(60000)
        yield page
        context.close()
        browser.close( )
