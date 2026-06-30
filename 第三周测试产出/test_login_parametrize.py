import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.parametrize("username, password, should_success", [
    ("standard_user", "secret_sauce", True),
    ("locked_out_user", "secret_sauce", False),
    ("problem_user", "secret_sauce", True),
])
def test_login_with_param(username, password, should_success):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(60000)
        page.goto("https://www.saucedemo.com")
        page.locator("#user-name").fill(username)
        page.locator("#password").fill(password)
        page.locator("#login-button").click()

        if should_success:
            page.wait_for_selector(".inventory_list")
            assert page.locator(".inventory_list").is_visible()
            print(f"✅ {username} 登录成功")
        else:
            error_msg = page.locator("[data-test='error']")
            error_msg.wait_for(state="visible")
            assert error_msg.is_visible()
            error_text = error_msg.text_content()
            print(f"❌ {username} 登录失败，错误提示：{error_text}")

        browser.close()