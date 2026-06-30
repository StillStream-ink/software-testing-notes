from playwright.sync_api import sync_playwright

def test_locator_practice():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        #打开saucedemo 登录页
        page.goto("http://www.saucedemo.com/", timeout=60000)

        #1.定位用户名输入框
        username_input = page.locator("#user-name")
        print("1.用户名输入框 - placeholder:",username_input.get_attribute("placeholder"))

        #2.定位密码输入框
        password_input = page.locator("#password")
        print("2.密码输入框 - placeholder:",password_input.get_attribute("placeholder"))

        #3.定位密码登录按钮
        login_btn = page.locator("#login-button")
        print("3.登录按钮 - value:",login_btn.get_attribute("value"))

        #先登录，才能看到商品和购物车
        username_input.fill("standard_user")
        password_input.fill("secret_sauce")
        login_btn.click()

        #等待页面跳转
        page.wait_for_url("**/inventory.html")

        #4.定位商品列表中的第一个商品名称
        first_product = page.locator(".inventory_item_name").first
        print("4.第一个商品名称：",first_product.text_content())

        #5.定位购物车图标
        cart_icon = page.locator(".shopping_cart_link")
        print("5.购物车图标 - class:",cart_icon.get_attribute("class"))

        #停留3秒看效果
        page.wait_for_timeout(3000)

        browser.close()
        print("\n所有元素定位完成！")

if __name__=="__main__":
    test_locator_practice()