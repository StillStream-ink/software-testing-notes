from playwright.sync_api import sync_playwright

def test_login_flow():
    print("开始测试")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        #1.打开登录页
        print("打开登录页")
        page.goto("https://www.saucedemo.com",timeout=60000)

        #2.输入用户名
        print("输入用户名")
        page.locator("#user-name").fill("standard_user")

        #3.输入密码
        print("输入密码")
        page.locator("#password").fill("secret_sauce")

        #4.点击登录按钮
        print("点击登录")
        page.locator("#login-button").click()

        #5.等待商品列表加载
        print("等待商品列表")
        page.wait_for_selector(".inventory_list")

        #新增：验证登录后的页面标签
        title = page.title()
        print("页面标题：",title)
        assert "Swag Labs" in title

        #6.获取商品数量并打印
        items = page.locator(".inventory_item")
        print("商品数量：",items.count())

        #新增：验证商品数量是否正确
        assert items.count() == 6
        print("✅ 商品数量验证通过，共6件商品")
        

        #7.打印第一个商品名称
        first_item = page.locator(".inventory_item_name").first
        print("第一个商品：",first_item.text_content())

        #8.截图保存
        page.screenshot(path="login_success.png")
        print("截图已保存")

        browser.close()
        print("测试完成")
        
if __name__=="__main__":
    test_login_flow()