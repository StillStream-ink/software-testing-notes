from playwright.sync_api import Page
import os


class BasePage:
    """Page Object 基类，封装通用操作"""

    def __init__(self, page: Page, base_url: str = "https://www.saucedemo.com"):
        self.page = page
        self.base_url = base_url

    def navigate(self, path: str = "") -> "BasePage":
        """跳转到指定路径，超时 30s（兼容网站波动）"""
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
        return self

    def screenshot(self, name: str) -> str:
        """截图并返回文件路径"""
        os.makedirs("images", exist_ok=True)
        path = f"images/{name}.png"
        self.page.screenshot(path=path, full_page=True)
        return path

    def get_current_url(self) -> str:
        return self.page.url

    def wait_for_url_contains(self, text: str, timeout: int = 30000) -> bool:
        """等待 URL 包含指定文本"""
        try:
            self.page.wait_for_url(f"**/{text}", timeout=timeout)
            return True
        except Exception:
            return False