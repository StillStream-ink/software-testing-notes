import pytest
from playwright.sync_api import sync_playwright

def test_saucedemo_full_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        #登录
        page.goto("https://www.saucedemo.com",wait_until="domcontentloaded")
        page.locator("#user-name").fill("standard_user")
        page.locator("#password").fill("secret_sauce")
        page.locator("#login-button").click()
        page.wait_for_selector(".inventory_list")

        #加购
        page.locator(".btn_inventory").first.click()
        page.locator(".shopping_cart_link").click()
        page.wait_for_selector(".cart_list")

        #结算
        page.locator("#checkout").click()
        page.wait_for_selector("#first-name")
        page.locator("#first-name").fill("Test")
        page.locator("#last-name").fill("User")
        page.locator("#postal-code").fill("12345")
        page.locator("#continue").click()
        

        #完成
        page.locator("#finish").click()
        page.wait_for_selector(".complete-header")

        #断言
        success_msg = page.locator(".complete-header")
        assert success_msg.is_visible()

        browser.close()



