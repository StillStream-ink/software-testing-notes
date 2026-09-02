import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from conftest import get_credentials


@allure.feature("购物流程")
@allure.story("完整下单流程")
@allure.title("测试 saucedemo 完整购物流程")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_saucedemo_full_flow_po(page: Page):
    creds = get_credentials()
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    # 1. 登录
    login_page.navigate().login(creds["standard_user"], creds["password"])
    inventory_page.wait_for_load()
    inventory_page.screenshot("登录完成页面")

    # 2. 加购 2 件商品
    inventory_page.add_items_to_cart(2)
    inventory_page.go_to_cart()
    inventory_page.screenshot("购物车页面")

    # 3. 校验购物车数量
    assert cart_page.get_cart_count() == 2, "购物车数量应为 2 件"

    # 4. 结算
    cart_page.checkout("Test", "User", "12345")
    total_price = cart_page.get_total_price()
    assert total_price > 0, f"订单总价应大于 0，实际为 {total_price}"

    cart_page.complete_order()
    assert cart_page.is_order_complete(), "订单完成页面未出现"
    cart_page.screenshot("订单完成页面")

    print("✅ PO 模式测试通过")


@allure.feature("登录功能")
@allure.story("异常登录")
@allure.title("测试 locked_out_user 登录失败")
@allure.severity(allure.severity_level.NORMAL)
def test_locked_out_user_login(page: Page):
    login_page = LoginPage(page)
    login_page.navigate().login("locked_out_user", "secret_sauce", expect_success=False)
    login_page.wait_for_error()
    error_text = login_page.get_error_text()
    assert "locked out" in error_text.lower()


@allure.feature("登录功能")
@allure.story("问题用户登录")
@allure.title("测试 problem_user 登录后页面展示")
@allure.severity(allure.severity_level.NORMAL)
def test_problem_user_login(page: Page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.navigate().login("problem_user", "secret_sauce")
    inventory_page.wait_for_load()
    inventory_page.screenshot("问题用户登录后页面")


@allure.feature("登录功能")
@allure.story("性能抖动用户登录")
@allure.title("测试 performance_glitch_user 慢加载场景")
@allure.severity(allure.severity_level.NORMAL)
def test_performance_glitch_user(page: Page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.navigate().login("performance_glitch_user", "secret_sauce")
    inventory_page.wait_for_load()
    inventory_page.screenshot("性能抖动用户登录后页面")


@allure.feature("购物流程")
@allure.story("错误用户结算异常")
@allure.title("测试 error_user 结算时页面错乱")
@allure.severity(allure.severity_level.NORMAL)
def test_error_user_checkout_failure(page: Page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    login_page.navigate().login("error_user", "secret_sauce")
    inventory_page.wait_for_load()
    inventory_page.add_items_to_cart(1)
    inventory_page.go_to_cart()

    cart_page.click_checkout()
    cart_page.fill_shipping_info("Test", "User", "12345")
    cart_page.continue_button.click()

    # error_user 结算时页面会错乱，检查是否有异常元素
    # 例如：商品图片缺失、布局异常、文字重叠等
    # 这里简单检查页面是否有 img 标签的 src 属性为空
    broken_images = page.locator('img[src=""]')
    if broken_images.count() > 0:
        print("✅ error_user 页面错乱检测成功")
    else:
        # 如果没有明显错误，至少确保页面停留在结算页（而不是成功页）
        assert "checkout-step-two" in page.url or "error" in page.url, f"预期页面错乱，实际URL: {page.url}"


@allure.feature("结算功能")
@allure.story("异常结算")
@allure.title("测试空购物车结算")
def test_empty_cart_checkout(page: Page):
    creds = get_credentials()
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    login_page.navigate().login(creds["standard_user"], creds["password"])
    inventory_page.wait_for_load()
    inventory_page.go_to_cart()

    cart_page.click_checkout()
    cart_page.fill_shipping_info("Test", "User", "12345")
    cart_page.continue_to_overview()

    total = cart_page.get_total_price()
    assert total == 0.0, f"空购物车总价应为 0，实际为 {total}"

@allure.feature("登录功能")
@allure.story("正向登录")
@allure.title("测试标准用户登录成功")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_login_success(page: Page):
    creds = get_credentials()
    login_page = LoginPage(page)
    login_page.navigate().login(creds["standard_user"], creds["password"])
    assert "inventory.html" in page.url


@allure.feature("登录功能")
@allure.story("边界条件")
@allure.title("测试用户名为空")
def test_login_empty_username(page: Page):
    login_page = LoginPage(page)
    login_page.navigate().login("", "secret_sauce", expect_success=False)
    login_page.wait_for_error()
    error_text = login_page.get_error_text()
    assert "Username is required" in error_text


@allure.feature("登录功能")
@allure.story("边界条件")
@allure.title("测试密码为空")
def test_login_empty_password(page: Page):
    login_page = LoginPage(page)
    login_page.navigate().login("standard_user", "", expect_success=False)
    login_page.wait_for_error()
    error_text = login_page.get_error_text()
    assert "Password is required" in error_text


@allure.feature("登录功能")
@allure.story("安全测试")
@allure.title("测试 SQL 注入攻击")
def test_login_sql_injection(page: Page):
    login_page = LoginPage(page)
    login_page.navigate().login("' OR '1'='1", "anything", expect_success=False)
    login_page.wait_for_error()
    error_text = login_page.get_error_text()
    assert "Username and password do not match" in error_text or "Username is required" in error_text


@allure.feature("购物车功能")
@allure.story("正向操作")
@allure.title("测试加购1件商品")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_cart_add_one(page: Page):
    creds = get_credentials()
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    login_page.navigate().login(creds["standard_user"], creds["password"])
    inventory_page.wait_for_load()
    inventory_page.add_items_to_cart(1)
    inventory_page.go_to_cart()

    assert cart_page.get_cart_count() == 1


@allure.feature("购物车功能")
@allure.story("正向操作")
@allure.title("测试加购多件商品")
def test_cart_add_multiple(page: Page):
    creds = get_credentials()
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    login_page.navigate().login(creds["standard_user"], creds["password"])
    inventory_page.wait_for_load()
    inventory_page.add_items_to_cart(3)
    inventory_page.go_to_cart()

    assert cart_page.get_cart_count() == 3


@allure.feature("购物车功能")
@allure.story("正向操作")
@allure.title("测试移除购物车商品")
def test_cart_remove_item(page: Page):
    creds = get_credentials()
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    login_page.navigate().login(creds["standard_user"], creds["password"])
    inventory_page.wait_for_load()
    inventory_page.add_items_to_cart(2)
    inventory_page.go_to_cart()

    # 移除第一个商品
    remove_btn = page.locator('[data-test="remove-sauce-labs-backpack"]')
    remove_btn.click()
    assert cart_page.get_cart_count() == 1


@allure.feature("购物车功能")
@allure.story("交互操作")
@allure.title("测试继续购物按钮")
def test_cart_continue_shopping(page: Page):
    creds = get_credentials()
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.navigate().login(creds["standard_user"], creds["password"])
    inventory_page.wait_for_load()
    inventory_page.go_to_cart()

    continue_btn = page.locator('[data-test="continue-shopping"]')
    continue_btn.click()
    assert "inventory.html" in page.url