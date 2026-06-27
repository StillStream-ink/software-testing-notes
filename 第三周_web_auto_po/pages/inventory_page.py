from playwright.sync_api import Page

class InventoryPage:
    def __init__(self,page:Page):
        self.page = page
        self.inventory_list = page.locator(".inventory_list")
        self.add_buttons = page.locator(".btn_inventory")
        self.cart_link = page.locator(".shopping_cart_link")
        self.item_names = page.locator(".inventory_item_name")

    def wait_for_load(self):
        """等待商品页加载完成"""
        self.inventory_list.wait_for(state="visible")
        return self
    
    def add_items_to_cart(self,count:int = 1):
        """添加指定数量的商品到购物车"""
        for i in range(count):
            self.add_buttons.nth(i).click()
        return self
    
    def go_to_cart(self):
         """进入购物车"""
         self.cart_link.click()
         return self
    
    def get_item_count(self) -> int:
        """获取商品数量"""
        return self.item_names.count()