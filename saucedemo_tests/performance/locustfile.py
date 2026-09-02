from locust import HttpUser, task, between


class SauceDemoUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://www.saucedemo.com"

    def on_start(self):
        """每个虚拟用户启动时预热"""
        self.client.get("/")

    @task(3)
    def load_inventory(self):
        """模拟访问商品页"""
        with self.client.get("/inventory.html", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"状态码异常: {resp.status_code}")
            elif "Products" not in resp.text:
                resp.failure("页面内容异常：未找到 Products")

    @task(1)
    def load_cart(self):
        """访问购物车页面"""
        with self.client.get("/cart.html", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"状态码异常: {resp.status_code}")

    @task(1)
    def load_static_assets(self):
        """加载静态资源"""
        assets = [
            "/css/sample-app-web.css",
            "/js/sample-app-web.js",
        ]
        for asset in assets:
            self.client.get(asset)

# 注意：SauceDemo 是前端渲染的 SPA，真实登录需要 JavaScript 执行。
# 如需测试完整业务链路（登录→浏览→加购→结算），请使用 locust-plugins 的 PlaywrightUser：
#   pip install locust-plugins
# 参考文档：https://github.com/SvenskaSpel/locust-plugins/blob/master/examples/playwright_ex.py