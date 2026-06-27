from playwright.sync_api import Page
import re

class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("#checkout")
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")
        self.finish_button = page.locator("#finish")
        self.complete_header = page.locator(".complete-header")   # ✅ 已修正
        self.total_label = page.locator(".summary_total_label")

    def get_cart_count(self) -> int:
        return self.cart_items.count()

    def checkout(self, first_name: str, last_name: str, postal_code: str):
        self.checkout_button.click()
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()
        # 等待概览页加载，确保总价元素出现
        self.total_label.wait_for(state="visible", timeout=90000)
        return self

    def complete_order(self):
        self.finish_button.click()
        self.complete_header.wait_for(state="visible", timeout=90000)
        return self

    def is_order_complete(self) -> bool:
        return self.complete_header.is_visible()

    def get_total_price(self) -> float:
        total_text = self.total_label.text_content()
        match = re.search(r'\$([\d.]+)', total_text)
        return float(match.group(1)) if match else 0.0