import 'dotenv/config';
import { chromium } from 'playwright';
import { PlaywrightAgent } from '@midscene/web/playwright';

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

(async () => {
  console.log('🚀 开始测试...');
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto('https://www.saucedemo.com');
  await sleep(3000);

  const agent = new PlaywrightAgent(page);

  // 1. 登录
  console.log('🔐 登录...');
  await agent.aiAct('输入用户名 standard_user，输入密码 secret_sauce，点击登录按钮');
  await sleep(5000);

  // 2. 直接加购指定商品（绕过“最低价”判断）
  console.log('🛒 加购 Sauce Labs Onesie...');
  await agent.aiAct('点击名称为 "Sauce Labs Onesie" 的商品下方的 "Add to cart" 按钮');
  await sleep(3000);

  // 3. 查看购物车
  console.log('🛍️ 查看购物车...');
  await agent.aiAct('点击右上角的购物车图标');
  await sleep(3000);

  console.log('✅ 脚本结束，请手动查看购物车是否有一个商品');
  // 不自动关闭浏览器，让你手动查看
  // await browser.close();
})();