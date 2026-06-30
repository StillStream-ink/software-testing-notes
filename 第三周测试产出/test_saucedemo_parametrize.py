import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.parametrize("username, password, expected", [
    ("standard_user", "secret_sauce", True),
    ("locked_out_user", "secret_sauce", False),
    ("problem_user", "secret_sauce", True),
])
def test_login_with_param(username, password, expected):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(90000)
        page.goto("https://www.saucedemo.com", wait_until="domcontentloaded")
        page.locator("#user-name").fill(username)
        page.locator("#password").fill(password)
        page.locator("#login-button").click()

        if expected is True:
            page.wait_for_selector(".inventory_list", timeout=90000)
            assert page.locator(".inventory_list").is_visible()
            print(f"✅ {username} 登录成功")
        else:
            error_msg = page.locator("[data-test='error']")
            assert error_msg.is_visible()
            print(f"❌ {username} 登录失败，符合预期")

        browser.close()