from playwright.sync_api import sync_playwright

def test_saucedemo_full_flow():
    print("开始完整购物流程测试")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        #1.登录
        print("1.登录")
        page.goto("https://saucedemo.com")
        page.locator("#user-name").fill("standard_user")
        page.locator("#password").fill("secret_sauce")
        page.locator("#login-button").click()
        page.wait_for_selector(".inventory_list")

        #加购多件商品
        add_buttons = page.locator(".btn_inventory")
        except_count=3

        print(f"准备添加{except_count}件商品")
        for i in range(except_count):
            add_buttons,nth(i).click()
            print(f"已添加第{i+1}件商品")
        
        #点击购物车
        page.locator(".shopping_cart_link").click()
        page.wait_for_selector(".cart_list")

        #检验购物车商品数量
        cart_items = page.locator(".cart_item")
        actual_count = cart_items.count()
        print(f"购物车中实际商品数量：{actual_count}")
        assert actual_count == except_count,f"预期{except_count}件，实际{actual_count}件"
        print(f"✅ 购物车数量校验通过：{actual_count}件")

        #2.添加第一个商品到购物车
        print("2.添加商品到购物车")
        page.locator(".btn_inventory").first.click()
        print("✅ 已添加第一个商品")

        #3.进入购物车
        print("3.进入购物车")
        page.locator(".shopping_cart_link").click()
        page.wait_for_selector(".cart_list")

        #4.点击结算
        print("4.点击结算")
        page.locator("#checkout").click()
        page.wait_for_selector("#first-name")

        #5.填写收货信息
        print("5.填写收获信息")
        page.locator("#first-name").fill("Test")
        page.locator("#last-name").fill("User")
        page.locator("#postal-code").fill("12345")
        page.locator("#continue").click()

        #提取订单总价
        page.wait_for_selector(".summary_total_label")
        total_label = page.locator("summary_total_label")
        total_text = total_label.text_content()
        print("订单总价文本",total_text)

        #提取数值（去掉 $ 符号，转为浮点数）
        import re
        price_match = re.search(r'\$([\d.]+)',total_text)
        if price_match:
            total_price = float(price_match.group(1))
            print(f"订单总价：${total_price:.2f}")
            #验证总价大于0
            assert total_price > 0,"订单总价应该大于0"
            print(f"✅ 订单总价校验通过：${total_price:.2f}")
        else:
            print("⚠️ 未找到价格信息")

        #6.点击完成订单
        print("6.点击完成订单")
        page.locator("#finish").click()

        #7.验证订单完成
        print("7.验证订单完成")
        success_msg = page.locator(".complete-header")
        assert success_msg.is_visible()
        print("✅ 订单完成，验证通过！")

        #截图
        page.screenshot(path="order_complete.png")
        print("截图以保存：order_complete.png")

        browser.close()
        print("完整购物流程测试结束")

if __name__=="__main__":
    test_saucedemo_full_flow()

