from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator('[data-test="username"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error_msg = page.locator('[data-test="error"]')

    def navigate(self):
        """打开登录页"""
        self.page.goto("https://www.saucedemo.com", wait_until="domcontentloaded")
        return self

    def login(self, username: str, password: str, expect_success: bool = True):
        """执行登录操作"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

        if expect_success:
            # 登录成功，等待跳转到商品页
            self.page.wait_for_url("**/inventory.html", timeout=10000)
        else:
            # 登录失败，等待错误提示出现
            self.error_msg.wait_for(state="visible", timeout=5000)

        return self

    def get_error_text(self) -> str:
        return self.error_msg.text_content() or ""

    def wait_for_error(self):
        self.error_msg.wait_for(state="visible")
        return self