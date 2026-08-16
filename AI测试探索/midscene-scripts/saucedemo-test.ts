import 'dotenv/config';
import { chromium } from 'playwright';

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

(async () => {
  console.log('🚀 脚本启动...');
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto('https://www.saucedemo.com');
  await sleep(2000);

  // 登录（Playwright 原生，稳定）
  console.log('🔐 登录...');
  await page.fill('#user-name', 'standard_user');
  await page.fill('#password', 'secret_sauce');
  await page.click('#login-button');
  await sleep(3000);

  // 获取商品列表
  console.log('📦 获取商品数据...');
  const itemNames = await page.locator('[data-test="inventory-item-name"]').allTextContents();
  const itemPrices = await page.locator('[data-test="inventory-item-price"]').allTextContents();
  const items = itemNames.map((name, i) => ({
    name,
    price: parseFloat(itemPrices[i]?.replace('$', '') || '0')
  }));
  console.log('商品列表:', items);

  // 找最便宜
  const cheapest = items.reduce((a, b) => a.price < b.price ? a : b);
  console.log(`最便宜的商品: ${cheapest.name} ($${cheapest.price})`);

  // 🛒 直接加购（最可靠的 CSS 选择器）
  console.log(`🛒 加购 ${cheapest.name}...`);
  await page.locator('.inventory_item:has-text("' + cheapest.name + '") .btn_primary').click();
  await sleep(2000);

  // 🛍️ 查看购物车
  console.log('🛍️ 查看购物车...');
  await page.locator('[data-test="shopping-cart-link"]').click();
  await sleep(2000);

  // 验证购物车
  const cartItems = await page.locator('[data-test="inventory-item-name"]').allTextContents();
  console.log('购物车中的商品:', cartItems);
  console.log(cartItems.length > 0 ? '✅ 测试通过！' : '❌ 测试失败。');

  await browser.close();
  console.log('🎉 测试完成！');
})();