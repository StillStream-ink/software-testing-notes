import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

def test_saucedemo_full_flow_po(page: Page):
    # 使用 PO 模式完成测试
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    # 登录
    login_page.navigate().login("standard_user", "secret_sauce")
    inventory_page.wait_for_load()

    # 加购 2 件商品
    inventory_page.add_items_to_cart(2).go_to_cart()

    # 校验购物车数量
    assert cart_page.get_cart_count() == 2, "购物车数量应为 2 件"

    # 结算：填写信息 → 进入概览页
    cart_page.checkout("Test", "User", "12345")  # 进入概览页，等待总价
    # 在概览页获取订单总价并断言
    total_price = cart_page.get_total_price()
    assert total_price > 0, f"订单总价应大于 0，实际为 {total_price}"

    # 点击 Finish 完成订单
    cart_page.complete_order()

    # 验证订单完成
    assert cart_page.is_order_complete(), "订单完成页面未出现"          # 验证订单完成
  

    print("✅ PO 模式测试通过")

