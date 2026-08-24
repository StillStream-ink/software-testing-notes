from playwright.sync_api import Page
from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page: Page, base_url: str = "https://www.saucedemo.com"):
        super().__init__(page, base_url)
        self.inventory_list = page.locator(".inventory_list")
        self.add_buttons = page.locator(".btn_inventory")
        self.cart_link = page.locator(".shopping_cart_link")
        self.item_names = page.locator(".inventory_item_name")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def wait_for_load(self) -> "InventoryPage":
        """等待商品页加载完成"""
        self.inventory_list.wait_for(state="visible")
        return self

    def add_items_to_cart(self, count: int = 1) -> "InventoryPage":
        """添加指定数量的商品到购物车"""
        available = self.add_buttons.count()
        if count > available:
            raise ValueError(f"请求添加 {count} 件，但页面只有 {available} 件商品")
        for i in range(count):
            self.add_buttons.nth(i).click()
        return self

    def go_to_cart(self) -> "InventoryPage":
        """进入购物车"""
        self.cart_link.click()
        return self

    def get_inventory_item_count(self) -> int:
        """获取页面商品列表中的商品总数"""
        return self.item_names.count()

    def get_cart_badge_count(self) -> int:
        """获取购物车右上角的数字徽章"""
        if self.cart_badge.is_visible():
            text = self.cart_badge.text_content()
            return int(text) if text and text.isdigit() else 0
        return 0