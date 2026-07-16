# Saucedemo Web 自动化测试项目

> 基于 Python + Playwright + pytest + Allure 的 Web 自动化测试项目，使用 Page Object Model（PO）模式封装页面对象，对 SauceDemo 电商网站完成完整购物流程自动化测试。

## ✨ 项目特点

- **Page Object Model**：页面元素与业务逻辑分离，代码结构清晰，易于维护和扩展
- **Playwright**：现代化的 Web 自动化测试框架，支持多浏览器、自动等待
- **pytest**：灵活的测试用例管理与执行
- **Allure 报告**：专业的测试报告，含 Environment 环境信息、步骤截图、分类展示

## 🛠️ 技术栈

- Python 3.13
- Playwright
- pytest
- allure-pytest
- Allure 命令行工具

## 📁 项目结构
第三周_web_auto_po/
├── pages/
│ ├── cart_page.py # 购物车及结算页面对象
│ ├── inventory_page.py # 商品列表页面对象
│ └── login_page.py # 登录页面对象
├── tests/
│ └── test_sucedemo_po.py # PO 模式测试用例
├── images/ # Allure 报告截图
│ ├── allure_overview.png
│ ├── allure_environment.png
│ ├── allure_behaviors.png
│ ├── allure_suites.png
│ └── allure_test_detail.png
├── conftest.py # pytest fixture 配置
├── environment.properties # Allure 环境信息
├── requirements.txt # 项目依赖
└── README.md

## 📋 测试流程

测试用例覆盖了完整的购物流程：

1. 登录（standard_user）
2. 添加 2 件商品到购物车
3. 进入购物车并校验商品数量
4. 填写收货信息
5. 提取订单总价并校验
6. 完成订单并验证成功

## 🚀 运行方式

```bash
pip install -r requirements.txt
playwright install
pytest tests/test_sucedemo_po.py -v --alluredir=./allure-results --clean-alluredir
allure serve ./allure-results

Allure 报告必须通过 allure serve 命令打开，不能直接双击 HTML 文件。

📊 测试报告截图


📝 项目说明
该项目是第三周 Web 自动化测试学习的产出，旨在展示：

从零搭建 Playwright 自动化测试环境

PO 模式封装页面对象的设计思路

结合 pytest + Allure 生成专业测试报告

该测试项目基于 SauceDemo 演示网站 (https://www.saucedemo.com) 构建，仅用于学习与作品展示
