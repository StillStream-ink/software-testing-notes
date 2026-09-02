import os
import pytest
import allure
import io
from playwright.sync_api import Page
from pages import LoginPage, InventoryPage
from PIL import Image, ImageChops

SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), "__snapshots__")


def _attach_screenshot(page: Page, description: str):
    allure.attach(
        page.screenshot(),
        description,
        allure.attachment_type.PNG
    )


def _assert_snapshot_with_tolerance(
    screenshot_bytes: bytes,
    name: str,
    max_diff_pixels: int = 2000,
):
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    baseline_path = os.path.join(SNAPSHOT_DIR, name)

    # 如果基线不存在，保存当前截图作为基线
    if not os.path.exists(baseline_path):
        with open(baseline_path, "wb") as f:
            f.write(screenshot_bytes)
        return

    # 加载图片
    baseline_img = Image.open(baseline_path)
    current_img = Image.open(io.BytesIO(screenshot_bytes))

    # 检查尺寸
    if baseline_img.size != current_img.size:
        raise AssertionError(
            f"截图尺寸不一致: 基线 {baseline_img.size} vs 当前 {current_img.size}"
        )

    # 计算差异
    diff_img = ImageChops.difference(baseline_img, current_img)
    diff_pixels = sum(1 for p in diff_img.getdata() if p != (0, 0, 0))

    total_pixels = baseline_img.width * baseline_img.height
    diff_percent = (diff_pixels / total_pixels) * 100

    # 保存差异图（如果差异较大）
    if diff_pixels > max_diff_pixels:
        diff_path = baseline_path.replace(".png", "_diff.png")
        diff_img.save(diff_path)
        allure.attach.file(diff_path, "差异图", allure.attachment_type.PNG)

    # 断言
    assert diff_pixels <= max_diff_pixels, (
        f"视觉差异超出容差: 差异像素 {diff_pixels} (阈值 {max_diff_pixels}), "
        f"占比 {diff_percent:.2f}%"
    )


@allure.feature("视觉回归")
@allure.story("标准用户页面截图比对")
@allure.title("测试 standard_user 商品页视觉基线（仅截图，不断言）")
@allure.severity(allure.severity_level.NORMAL)
def test_standard_user_inventory_snapshot(page: Page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.navigate().login("standard_user", "secret_sauce")
    inventory_page.wait_for_load()

    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)

    screenshot = page.screenshot(full_page=True)
    _attach_screenshot(page, "standard_user 当前页面")

    # 只截图，不做比对
    # _assert_snapshot_with_tolerance(...) 注释掉或删除

@allure.feature("视觉回归")
@allure.story("visual_user 页面截图留档")
@allure.title("测试 visual_user 登录后页面视觉差异")
@allure.severity(allure.severity_level.NORMAL)
def test_visual_user_inventory_snapshot(page: Page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("1. 登录 visual_user"):
        login_page.navigate().login("visual_user", "secret_sauce")
        inventory_page.wait_for_load()

    with allure.step("2. 截图保存供人工审查"):
        screenshot = page.screenshot(full_page=True)

        os.makedirs(SNAPSHOT_DIR, exist_ok=True)
        visual_path = os.path.join(SNAPSHOT_DIR, "visual_user_inventory.png")
        with open(visual_path, "wb") as f:
            f.write(screenshot)

        allure.attach.file(
            visual_path,
            "visual_user 页面截图",
            allure.attachment_type.PNG
        )

        standard_path = os.path.join(SNAPSHOT_DIR, "standard_user_inventory.png")
        if os.path.exists(standard_path):
            standard_size = os.path.getsize(standard_path)
            visual_size = os.path.getsize(visual_path)
            size_diff = abs(visual_size - standard_size) / standard_size
            assert size_diff > 0.01, "visual_user 与标准用户过于相似，可能异常未生效"