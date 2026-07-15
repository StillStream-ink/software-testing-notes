from locust import HttpUser, task, between

class SaucedemoUser(HttpUser):
    """模拟用户对 saucedemo 网站进行性能测试"""
    wait_time = between(1, 3)

    def on_start(self):
        """用户启动时执行一次，模拟打开首页"""
        self.client.get("/")

    @task(3)
    def login(self):
        """模拟登录请求（权重3）"""
        self.client.post(
            "/login",
            json={
                "username": "standard_user",
                "password": "secret_sauce"
            }
        )

    @task(2)
    def browse_inventory(self):
        """模拟浏览商品列表（权重2）"""
        self.client.get("/inventory.html")

    @task(1)
    def view_cart(self):
        """模拟查看购物车（权重1）"""
        self.client.get("/cart.html")
