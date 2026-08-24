from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, base_url: str = "https://www.saucedemo.com"):
        super().__init__(page, base_url)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_msg = page.locator("[data-test='error']")

    def navigate(self) -> "LoginPage":
        """打开登录页"""
        super().navigate("")
        self.username_input.wait_for(state="visible")
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """执行登录操作"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return self

    def wait_for_error(self) -> "LoginPage":
        """等待错误提示出现"""
        self.error_msg.wait_for(state="visible")
        return self

    def get_error_text(self) -> str:
        """获取错误提示文本"""
        return self.error_msg.text_content() or ""