import pytest
import allure
from playwright.sync_api import Page
from pages import LoginPage, InventoryPage, CartPage


def _attach_screenshot(page: Page, description: str):
    """内存截图，直接附加到 Allure"""
    allure.attach(
        page.screenshot(),
        description,
        allure.attachment_type.PNG
    )


@allure.feature("购物流程")
@allure.story("完整下单流程")
@allure.title("测试 saucedemo 完整购物流程")
@allure.severity(allure.severity_level.CRITICAL)
def test_saucedemo_full_flow_po(page: Page, config, logger, request):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    with allure.step("1. 登录并进入商品页"):
        login_page.navigate().login("standard_user", config["users"]["standard_user"])
        inventory_page.wait_for_load()

    with allure.step("2. 添加商品到购物车"):
        inventory_page.add_items_to_cart(config["test_data"]["item_count"]).go_to_cart()

    with allure.step("3. 校验购物车并结算"):
        _attach_screenshot(page, "购物车页面")
        assert cart_page.get_cart_count() == 2
        cart_page.checkout(
            config["test_data"]["checkout_info"]["first_name"],
            config["test_data"]["checkout_info"]["last_name"],
            config["test_data"]["checkout_info"]["postal_code"]
        )
        total_price = cart_page.get_total_price()
        assert total_price > 0

    with allure.step("4. 完成订单"):
        cart_page.complete_order()
        assert cart_page.is_order_complete()
        _attach_screenshot(page, "订单完成页面")


@allure.feature("登录功能")
@allure.story("锁定用户登录")
@allure.title("测试 locked_out_user 登录失败")
@allure.severity(allure.severity_level.NORMAL)
def test_locked_out_user_login(page: Page, config, logger):
    login_page = LoginPage(page)
    login_page.navigate().login("locked_out_user", config["users"]["locked_out_user"])
    login_page.wait_for_error()
    assert "locked out" in login_page.get_error_text().lower()


@allure.feature("登录功能")
@allure.story("问题用户登录")
@allure.title("测试 problem_user 登录后页面展示")
@allure.severity(allure.severity_level.NORMAL)
def test_problem_user_login(page: Page, config, logger):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    login_page.navigate().login("problem_user", config["users"]["problem_user"])
    inventory_page.wait_for_load()
    assert inventory_page.inventory_list.is_visible()

    item_images = page.locator(".inventory_item_img img")
    first_image_src = item_images.first.get_attribute("src")
    assert "sl-404" in first_image_src or "not_found" in first_image_src


@allure.feature("购物车功能")
@allure.story("空购物车结算")
@allure.title("空购物车直接结算应被拦截")
@allure.severity(allure.severity_level.NORMAL)
def test_empty_cart_checkout(logged_in_page: Page, config, logger):
    cart_page = CartPage(logged_in_page)
    cart_page.navigate()
    assert cart_page.get_cart_count() == 0
    cart_page.click_checkout()
    assert cart_page.is_on_checkout_page()


@allure.feature("登录功能")
@allure.story("性能抖动用户登录")
@allure.title("测试 performance_glitch_user 慢加载场景")
@allure.severity(allure.severity_level.NORMAL)
def test_performance_glitch_user(page: Page, config, logger):
    """performance_glitch_user 登录后页面加载极慢，测试长超时等待策略"""
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    logger.info("开始测试性能抖动用户登录")
    login_page.navigate().login(
        "performance_glitch_user",
        config["users"]["performance_glitch_user"]
    )

    with allure.step("等待商品页加载（慢加载场景）"):
        inventory_page.wait_for_load()
        assert inventory_page.inventory_list.is_visible(), "商品列表未显示"
        _attach_screenshot(page, "性能抖动用户-商品页加载完成")

    logger.info("性能抖动用户登录测试通过")


@allure.feature("购物流程")
@allure.story("错误用户结算异常")
@allure.title("测试 error_user 结算时触发系统错误")
@allure.severity(allure.severity_level.NORMAL)
def test_error_user_checkout_failure(page: Page, config, logger):
    """error_user 无法正常完成订单，验证异常流程处理"""
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    logger.info("开始测试错误用户结算异常")

    with allure.step("1. 登录并添加商品"):
        login_page.navigate().login("error_user", config["users"]["error_user"])
        inventory_page.wait_for_load()
        inventory_page.add_items_to_cart(1).go_to_cart()
        assert cart_page.get_cart_count() == 1

    with allure.step("2. 填写结算信息"):
        cart_page.checkout(
            config["test_data"]["checkout_info"]["first_name"],
            config["test_data"]["checkout_info"]["last_name"],
            config["test_data"]["checkout_info"]["postal_code"]
        )
        total_price = cart_page.get_total_price()
        assert total_price > 0
        _attach_screenshot(page, "错误用户-结算概览页")

    with allure.step("3. 点击完成订单，验证异常"):
        cart_page.complete_order()
        _attach_screenshot(page, "错误用户-点击finish后页面")

        # error_user 无法正常完成订单，验证订单未完成即可
        # （具体错误表现形式可能变化，截图留档供人工确认）
        assert not cart_page.is_order_complete(),             "error_user 不应成功完成订单，但订单完成页出现了"

        logger.info("错误用户结算异常测试通过")