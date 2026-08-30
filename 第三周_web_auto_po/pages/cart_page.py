from playwright.sync_api import Page
from pages.base_page import BasePage
import re


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.first_name_input = page.locator('[data-test="firstName"]')
        self.last_name_input = page.locator('[data-test="lastName"]')
        self.postal_code_input = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.total_label = page.locator('[data-test="total-label"]')

    def get_cart_count(self) -> int:
        return self.cart_items.count()

    def click_checkout(self):
        self.checkout_button.click()
        return self

    def fill_shipping_info(self, first_name: str, last_name: str, postal_code: str):
        """填写收货信息"""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        return self

    def continue_to_overview(self):
        self.continue_button.click()
        self.total_label.wait_for(state="visible", timeout=10000)
        return self

    def complete_order(self):
        self.finish_button.click()
        self.complete_header.wait_for(state="visible", timeout=10000)
        return self

    def is_order_complete(self) -> bool:
        return self.complete_header.is_visible()

    def get_total_price(self) -> float:
        total_text = self.total_label.text_content() or ""
        match = re.search(r'\$([\d.]+)', total_text)
        return float(match.group(1)) if match else 0.0

    def checkout(self, first_name: str, last_name: str, postal_code: str):
        self.click_checkout()
        self.fill_shipping_info(first_name, last_name, postal_code)
        self.continue_to_overview()
        return self