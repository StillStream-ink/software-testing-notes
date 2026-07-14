import pytest
import sys
import json
import os
import logging
from playwright.sync_api import sync_playwright

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

LOGGER = setup_logging()

# ========== 配置文件读取 ==========
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

CONFIG = load_config()

# ========== Playwright fixture ==========
@pytest.fixture(scope="function")
def page():
    """每个测试用例独立浏览器实例"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(60000)
        yield page
        context.close()
        browser.close()
