"""Page Object 统一导出"""

from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

__all__ = ["BasePage", "LoginPage", "InventoryPage", "CartPage"]