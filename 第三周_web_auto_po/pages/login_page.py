from playwright.sync_api import Page

class LoginPage:
    def __init__(self,page:Page):
        self.page = page
        #定位器集中管理
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_msg = page.locator("[data-test='error']")

    def navigate(self):
        """打开登录页"""
        self.page.goto("https://www.saucedemo.com", timeout=90000, wait_until="domcontentloaded")
        return self
    
    def login(self, username: str, password: str):
        """执行登录操作"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.wait_for(state="visible")
        self.login_button.click()
        return self
    
    def get_error_text(self) -> str:
        """获取错误提示文本"""
        return self.error_msg.text_content()
    
    def wait_for_error(self):
         """等待错误提示出现"""
         self.error_msg.wait_for(state="visible")
         return self
