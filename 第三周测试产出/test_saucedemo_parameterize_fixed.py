from playwright.sync_api import sync_playwright
import re

def login(page, username="standard_user", password="secret_sauce"):
    """封装登录函数"""
    page.goto("https://www.saucedemo.com",wait_until="domcontentloaded",timeout=90000)
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)
    page.locator("#login-button").click()
    page.wait_for_selector(".inventory_list")
    print(f"✅ 登录成功：{username}")

def add_items_to_cart(page, count=1):
    """封装加购函数"""
    add_buttons = page.locator(".btn_inventory")
    for i in range(count):
        add_buttons.nth(i).click()
    print(f"✅ 已添加 {count} 件商品")
    return count

def checkout(page, first_name="Test", last_name="User", postal_code="12345", expect_goods_num=1):
    """封装结算函数"""
    page.locator(".shopping_cart_link").click()
    page.wait_for_selector(".cart_list")
    cart_items = page.locator(".cart_item")
    actual_num = cart_items.count()
    assert actual_num == expect_goods_num, f"预期{expect_goods_num}件，实际{actual_num}件"
    print(f"✅ 购物车数量校验通过：{actual_num}件")

    page.locator("#checkout").click()
    page.wait_for_selector("#first-name")
    page.locator("#first-name").fill(first_name)
    page.locator("#last-name").fill(last_name)
    page.locator("#postal-code").fill(postal_code)
    page.locator("#continue").click()

    page.wait_for_selector(".summary_total_label")
    total_text = page.locator(".summary_total_label").text_content()
    price_match = re.search(r'\$([\d.]+)', total_text)
    if price_match:
        total_price = float(price_match.group(1))
        assert total_price > 0, "订单总价必须大于0"
        print(f"✅ 总价校验通过：${total_price:.2f}")
    else:
        print("⚠️ 未识别到订单价格")

    print("✅ 结算信息已填写")

def complete_order(page):
    """封装完成订单函数"""
    page.locator("#finish").click()
    page.wait_for_selector(".complete-header")
    success_msg = page.locator(".complete-header")
    assert success_msg.is_visible()
    print("✅ 订单完成")

def test_saucedemo_optimized():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(90000)

        login(page)
        expect_count = add_items_to_cart(page, count=2)
        checkout(page, expect_goods_num=expect_count)
        complete_order(page)

        page.screenshot(path="order_complete_optimized.png")
        print("截图已保存")

        browser.close()
        print("✅ 完整流程测试通过")

if __name__ == "__main__":
    test_saucedemo_optimized()