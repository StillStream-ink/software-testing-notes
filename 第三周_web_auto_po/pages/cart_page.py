from playwright.sync_api import Page
import re
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page, base_url: str = "https://www.saucedemo.com"):
        super().__init__(page, base_url)
        self.cart_items = page.locator(".cart_item")
        self.title = page.locator(".title")
        self.checkout_button = page.locator("#checkout")
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")
        self.finish_button = page.locator("#finish")
        self.complete_header = page.locator(".complete-header")
        self.total_label = page.locator(".summary_total_label")
        self.error_msg = page.locator("[data-test='error']")

    def navigate(self) -> "CartPage":
        """直接跳转到购物车页面"""
        super().navigate("cart.html")
        self.title.wait_for(state="visible")
        return self

    def get_cart_count(self) -> int:
        return self.cart_items.count()

    def click_checkout(self) -> "CartPage":
        """点击结算按钮"""
        self.checkout_button.click()
        return self

    def checkout(self, first_name: str, last_name: str, postal_code: str) -> "CartPage":
        self.checkout_button.click()
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()
        self.total_label.wait_for(state="visible", timeout=15000)
        return self

    def complete_order(self) -> "CartPage":
        self.finish_button.click()
        return self

    def wait_for_error(self) -> "CartPage":
        """等待错误提示出现"""
        self.error_msg.wait_for(state="visible")
        return self

    def get_error_text(self) -> str:
        """获取错误提示文本"""
        return self.error_msg.text_content() or ""

    def is_order_complete(self) -> bool:
        return self.complete_header.is_visible()

    def is_on_checkout_page(self) -> bool:
        """判断是否在结算信息填写页"""
        return self.page.url.endswith("/checkout-step-one.html")

    def get_total_price(self) -> float:
        total_text = self.total_label.text_content() or ""
        match = re.search(r'\$([\d.]+)', total_text)
        return float(match.group(1)) if match else 0.0