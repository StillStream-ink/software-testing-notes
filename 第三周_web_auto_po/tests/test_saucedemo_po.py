import pytest
import allure
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from conftest import CONFIG, LOGGER


@allure.feature("购物流程")
class TestShoppingFlow:

    @allure.story("完整下单流程")
    @allure.title("测试 saucedemo 完整购物流程")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_saucedemo_full_flow_po(self, page: Page):
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)

        # 从配置文件读取测试数据
        user = CONFIG["test_data"].get("user", "standard_user")
        password = CONFIG["users"].get(user, "secret_sauce")
        first_name = CONFIG["test_data"].get("first_name", "Test")
        last_name = CONFIG["test_data"].get("last_name", "User")
        postal_code = CONFIG["test_data"].get("postal_code", "12345")
        item_count = CONFIG["test_data"].get("item_count", 2)

        with allure.step("1. 登录 saucedemo 网站"):
            login_page.navigate().login(user, password)
            inventory_page.wait_for_load()
            allure.attach(page.screenshot(), "登录后商品页", allure.attachment_type.PNG)

        with allure.step("2. 添加商品到购物车"):
            inventory_page.add_items_to_cart(item_count).go_to_cart()
            allure.attach(page.screenshot(), "购物车页面", allure.attachment_type.PNG)

        with allure.step("3. 校验购物车商品数量"):
            assert cart_page.get_cart_count() == item_count, f"购物车数量应为 {item_count} 件"

        with allure.step("4. 填写结算信息并验证总价"):
            cart_page.checkout(first_name, last_name, postal_code)
            total_price = cart_page.get_total_price()
            assert total_price > 0, f"订单总价应大于0，实际为 {total_price}"

        with allure.step("5. 完成订单并验证成功"):
            cart_page.complete_order()
            assert cart_page.is_order_complete(), "订单完成页面未出现"
            allure.attach(page.screenshot(), "订单完成页面", allure.attachment_type.PNG)


@allure.feature("登录功能")
class TestLogin:

    @allure.story("锁定用户登录")
    @allure.title("测试 locked_out_user 登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    def test_locked_out_user_login(self, page: Page):
        login_page = LoginPage(page)
        LOGGER.info("开始测试锁定用户登录")
        login_page.navigate().login("locked_out_user", CONFIG["users"]["locked_out_user"])
        login_page.wait_for_error()
        error_text = login_page.get_error_text()
        LOGGER.info(f"错误提示: {error_text}")
        assert "locked out" in error_text.lower()
        allure.attach(page.screenshot(), "锁定用户登录错误提示", allure.attachment_type.PNG)
        LOGGER.info("锁定用户登录测试通过")

    @allure.story("问题用户登录")
    @allure.title("测试 problem_user 登录后页面展示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_problem_user_login(self, page: Page):
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        LOGGER.info("开始测试问题用户登录")
        login_page.navigate().login("problem_user", CONFIG["users"]["problem_user"])
        inventory_page.wait_for_load()
        assert inventory_page.inventory_list.is_visible()
        item_images = page.locator(".inventory_item_img img")
        first_image_src = item_images.first.get_attribute("src")
        LOGGER.info(f"第一个商品图片地址: {first_image_src}")
        allure.attach(page.screenshot(), "问题用户登录后页面", allure.attachment_type.PNG)
        LOGGER.info("问题用户登录测试通过")

    @pytest.mark.parametrize("user,expected_success", [
        ("standard_user", True),
        ("locked_out_user", False),
        ("problem_user", True),
    ])
    @allure.story("多用户登录测试")
    @allure.title("测试用户 {user} 登录")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_users(self, page: Page, user, expected_success):
        login_page = LoginPage(page)
        LOGGER.info(f"测试用户登录：{user}")
        login_page.navigate().login(user, CONFIG["users"].get(user, ""))

        if expected_success:
            inventory_page = InventoryPage(page)
            inventory_page.wait_for_load()
            assert inventory_page.inventory_list.is_visible()
            allure.attach(page.screenshot(), f"{user} 登录成功", allure.attachment_type.PNG)
            LOGGER.info(f"{user} 登录成功")
        else:
            login_page.wait_for_error()
            error_text = login_page.get_error_text()
            allure.attach(page.screenshot(), f"{user} 登录失败", allure.attachment_type.PNG)
            LOGGER.info(f"{user} 登录失败，错误提示：{error_text}")
            assert "locked out" in error_text.lower() or "username" in error_text.lower()


@allure.feature("购物车功能")
class TestCart:

    @allure.story("空购物车结算")
    @allure.title("空购物车直接结算")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_cart_checkout(self, page: Page):
        login_page = LoginPage(page)
        LOGGER.info("开始测试空购物车结算")
        login_page.navigate().login("standard_user", CONFIG["users"]["standard_user"])
        page.locator(".shopping_cart_link").click()
        page.wait_for_selector(".cart_list")
        cart_items = page.locator(".cart_item")
        assert cart_items.count() == 0, "购物车应为空"
        page.locator("#checkout").click()
        page.wait_for_selector("#first-name")
        allure.attach(page.screenshot(), "空购物车结算页面", allure.attachment_type.PNG)
        LOGGER.info("空购物车结算测试通过")
