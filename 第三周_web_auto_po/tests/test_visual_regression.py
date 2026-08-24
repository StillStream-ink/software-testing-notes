import os
import pytest
import allure
from playwright.sync_api import Page
from pages import LoginPage, InventoryPage


SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), "__snapshots__")


def _assert_snapshot(screenshot_bytes: bytes, name: str):
    """手写截图比对：首次保存基线，后续严格比对"""
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    baseline_path = os.path.join(SNAPSHOT_DIR, name)

    if not os.path.exists(baseline_path):
        with open(baseline_path, "wb") as f:
            f.write(screenshot_bytes)
        return

    with open(baseline_path, "rb") as f:
        baseline = f.read()

    if baseline == screenshot_bytes:
        return

    current_path = baseline_path.replace(".png", "_current.png")
    with open(current_path, "wb") as f:
        f.write(screenshot_bytes)

    raise AssertionError(
        f"视觉差异 detected: {name}\n"
        f"  基线: {baseline_path}\n"
        f"  当前: {current_path}"
    )


@allure.feature("视觉回归")
@allure.story("标准用户页面截图比对")
@allure.title("测试 standard_user 商品页视觉基线")
@allure.severity(allure.severity_level.NORMAL)
def test_standard_user_inventory_snapshot(page: Page):
    """标准用户作为视觉基线，严格比对确保页面稳定"""
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.navigate().login("standard_user", "secret_sauce")
    inventory_page.wait_for_load()

    screenshot = page.screenshot(full_page=True)
    _attach_screenshot(page, "standard_user 当前页面")
    _assert_snapshot(screenshot, "standard_user_inventory.png")


@allure.feature("视觉回归")
@allure.story("visual_user 页面截图留档")
@allure.title("测试 visual_user 登录后页面视觉差异")
@allure.severity(allure.severity_level.NORMAL)
def test_visual_user_inventory_snapshot(page: Page):
    """
    visual_user 的页面布局与标准用户存在视觉差异（图片错位、UI偏移）。
    本测试只截图保存到 Allure 和本地，供人工审查差异，不做严格比对。
    """
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("1. 登录 visual_user"):
        login_page.navigate().login("visual_user", "secret_sauce")
        inventory_page.wait_for_load()

    with allure.step("2. 截图保存供人工审查"):
        screenshot = page.screenshot(full_page=True)

        # 保存到本地供对比
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)
        visual_path = os.path.join(SNAPSHOT_DIR, "visual_user_inventory.png")
        with open(visual_path, "wb") as f:
            f.write(screenshot)

        # 附加到 Allure 报告
        allure.attach.file(
            visual_path,
            "visual_user 页面截图（预期与标准用户有差异）",
            allure.attachment_type.PNG
        )

        # 可选：与 standard_user 基线做简单大小对比（如果大小差异很大，说明异常明显）
        standard_path = os.path.join(SNAPSHOT_DIR, "standard_user_inventory.png")
        if os.path.exists(standard_path):
            standard_size = os.path.getsize(standard_path)
            visual_size = os.path.getsize(visual_path)
            size_diff = abs(visual_size - standard_size) / standard_size

            allure.attach(
                f"standard_user: {standard_size} bytes\n"
                f"visual_user: {visual_size} bytes\n"
                f"差异比例: {size_diff:.1%}",
                "截图文件大小对比",
                allure.attachment_type.TEXT
            )

            # visual_user 应该与标准用户有差异，差异太小反而说明异常未出现
            assert size_diff > 0.01, "visual_user 页面与标准用户过于相似，可能异常未生效"


def _attach_screenshot(page: Page, description: str):
    """内存截图附加到 Allure"""
    allure.attach(
        page.screenshot(),
        description,
        allure.attachment_type.PNG
    )