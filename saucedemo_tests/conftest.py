import pytest
import json
import os
import logging
import time
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()  # 读取 .env 文件中的环境变量

def get_credentials():
    return {
        "standard_user": os.getenv("SD_STANDARD_USER", "standard_user"),
        "password": os.getenv("SD_PASSWORD", "secret_sauce"),
    }

# ========== 日志配置 ==========
def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/test.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()

# ========== 配置文件读取 ==========
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ========== Fixtures ==========

@pytest.fixture(scope="session")
def config():
    """延迟加载配置，避免导入时出错"""
    return load_config()

@pytest.fixture(scope="session")
def logger():
    """日志对象"""
    return setup_logging()

# ========== Session 级 Browser ==========

@pytest.fixture(scope="session")
def browser():
    """整个测试会话只启动一次浏览器"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    """每个用例新建 context 和 page，但复用 browser"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN"
    )
    page = context.new_page()
    page.set_default_timeout(30000)
    yield page
    context.close()

@pytest.fixture
def logged_in_page(page, config):
    """已登录标准用户的 page 对象"""
    from pages.login_page import LoginPage
    login_page = LoginPage(page)
    login_page.navigate().login("standard_user", get_credentials()["password"])
    return page

# ========== 失败自动截图 ==========

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(page, request):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs("images", exist_ok=True)
        screenshot_path = f"images/failed_{request.node.name}_{time.strftime('%H%M%S')}.png"
        try:
            page.screenshot(path=screenshot_path, full_page=True)
        except Exception:
            pass

# ========== Allure 环境信息写入（修复：放到 sessionfinish，避免被 --clean-alluredir 清空）==========

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """测试会话结束时写入环境信息（此时 --clean-alluredir 已执行完）"""
    allure_dir = "allure-results"
    os.makedirs(allure_dir, exist_ok=True)

    # 写入环境变量
    with open(os.path.join(allure_dir, "environment.properties"), "w", encoding="utf-8") as f:
        f.write("Project=SauceDemo Web自动化测试\n")
        f.write("Environment=Local\n")
        f.write("Framework=Playwright + Pytest\n")
        f.write("Python=3.11\n")
        f.write("Executor=Local-Dev\n")

    # 写入执行者信息
    executor = {
        "name": "Local-Dev",
        "type": "local",
        "buildName": "Local-Dev"
    }
    with open(os.path.join(allure_dir, "executor.json"), "w", encoding="utf-8") as f:
        json.dump(executor, f, ensure_ascii=False, indent=2)