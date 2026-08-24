# SauceDemo Web 自动化测试项目

> 基于 Python + Playwright + pytest + Allure 的 Web 自动化测试项目，使用 Page Object Model（PO）模式封装页面对象，对 SauceDemo 电商网站完成完整购物流程自动化测试。

## ✨ 项目特点

- **Page Object Model**：页面元素与业务逻辑分离，代码结构清晰，易于维护和扩展
- **BasePage 抽象层**：提取公共逻辑（导航、截图、URL 校验），减少重复代码
- **Playwright**：现代化的 Web 自动化测试框架，支持多浏览器、自动等待
- **pytest**：灵活的测试用例管理与执行，支持参数化和 fixture 注入
- **Allure 报告**：专业的测试报告，含 Environment 环境信息、步骤截图、趋势图、分类展示
- **数据驱动**：测试数据集中管理在 `config.json` 中，支持多环境快速切换
- **日志系统**：测试执行过程自动记录日志，便于问题追溯
- **失败自动截图**：测试失败时自动截取全屏，方便定位问题
- **视觉回归测试**：截图比对捕获 UI 偏移、图片错位等视觉差异
- **一键报告脚本**：`generate_report.bat` 自动生成含趋势图的 Allure 报告
- **持续集成**：GitHub Actions 自动运行测试，每次代码提交自动触发

## 🛠️ 技术栈

- Python 3.11
- Playwright 1.45.0
- pytest 7.4.4
- pytest-playwright 0.4.3
- pytest-xdist 3.6.1
- allure-pytest 2.16.0
- Allure 命令行工具
- Locust 2.31.3
- GitHub Actions

## 📁 项目结构

```
第三周_web_auto_po/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI 配置
├── config/
│   ├── categories.json          # Allure 失败分类配置
│   └── config.json              # 测试数据与运行配置
├── pages/
│   ├── __init__.py              # Page 统一导出
│   ├── base_page.py             # PO 抽象基类（导航、截图、URL 校验）
│   ├── cart_page.py             # 购物车及结算页面对象
│   ├── inventory_page.py        # 商品列表页面对象
│   └── login_page.py            # 登录页面对象
├── tests/
│   ├── test_saucedemo_po.py     # 功能测试用例（6 条）
│   └── test_visual_regression.py # 视觉回归测试（2 条）
├── performance/
│   └── locustfile.py            # Locust 性能测试脚本
├── allure-results/              # Allure 原始数据（自动生成）
├── allure-report/               # Allure HTML 报告（自动生成）
├── images/                      # 失败截图目录（自动生成）
├── logs/                        # 测试日志目录（自动生成）
├── conftest.py                  # pytest 全局配置（session browser、失败截图、环境信息）
├── pytest.ini                   # pytest 统一配置（markers、alluredir）
├── .gitignore                   # Git 忽略配置
├── generate_report.bat          # 一键生成 Allure 报告（含趋势图）
├── requirements.txt             # 项目依赖（版本锁定）
└── README.md
```

## 📋 测试流程

### 功能测试覆盖

| 测试场景 | 用例数 | 说明 |
|----------|--------|------|
| 完整购物流程 | 1 | standard_user 登录 → 加购 → 结算 → 完成订单 |
| 锁定用户登录 | 1 | locked_out_user 登录失败并提示错误 |
| 问题用户登录 | 1 | problem_user 登录后页面展示异常（图片错位） |
| 性能抖动用户 | 1 | performance_glitch_user 慢加载场景，验证超时容忍 |
| 错误用户结算 | 1 | error_user 结算时触发系统错误，验证异常捕获 |
| 空购物车结算 | 1 | 空购物车直接进入结算页面 |
| **功能小计** | **6** | |

### 视觉回归测试

| 测试场景 | 用例数 | 说明 |
|----------|--------|------|
| 标准用户基线 | 1 | standard_user 商品页截图作为视觉基线，严格比对 |
| 视觉差异用户 | 1 | visual_user 截图留档，人工审查与基线的差异 |
| **视觉小计** | **2** | |

| **总计** | **8** | 全部通过 ✅ |

## 🚀 运行方式

### 1. 安装依赖

```powershell
py -m pip install -r requirements.txt
py -m playwright install chromium
```

### 2. 运行功能测试

```powershell
# 运行全部测试（推荐）
py -m pytest

# 只跑功能测试
py -m pytest tests/test_saucedemo_po.py

# 只跑视觉回归
py -m pytest tests/test_visual_regression.py

# 只跑冒烟测试
py -m pytest -m smoke
```

### 3. 生成并查看 Allure 报告

```powershell
# 方式一：一键脚本（推荐，自动复制历史数据生成趋势图）
.\generate_report.bat

# 方式二：手动命令
# 复制分类配置
copy config\categories.json allure-results\categories.json
# 生成报告
allure generate allure-results -o allure-report --clean
# 打开报告
allure open allure-report
```

> **注意**：Allure 趋势图需要历史数据。首次运行 Trend 为空，第二次及以后运行 `generate_report.bat` 会自动累积历史数据并显示趋势折线图。

## ⚡ 性能测试

项目使用 Locust 进行简单的静态资源压测。

```powershell
py -m pip install locust
cd performance
py -m locust -f locustfile.py
```

然后访问 http://localhost:8089，设置并发用户数，点击 Start 开始压测。

> **说明**：SauceDemo 是前端渲染的 SPA，完整业务链路压测需要使用 `PlaywrightUser`（见 `locustfile.py` 内注释）。

## 🏗️ 架构亮点

### Session 级 Browser 复用

`conftest.py` 中 browser 提升到 session 级别，整个测试会话只启动一次 Chromium，每个用例复用 browser 但隔离 context，兼顾效率与稳定性。

### 配置与代码分离

所有可变参数（URL、用户凭证、超时时间、截图策略）集中在 `config.json`，支持多环境切换。

### 失败自动截图

通过 `pytest_runtest_makereport` hook，测试失败时自动截取全屏保存到 `images/` 目录，并附加到 Allure 报告。

## 📝 项目说明

该项目是 Web 自动化测试学习的产出，旨在展示：

- 从零搭建 Playwright 自动化测试环境
- PO 模式 + BasePage 抽象层的设计思路
- pytest fixture 注入与 session 级资源管理
- 结合 pytest + Allure 生成专业测试报告（含趋势图）
- 数据驱动 + 日志系统 + 失败截图的工程化实践
- 视觉回归测试的截图比对思路
- GitHub Actions 持续集成自动运行测试

该测试项目基于 SauceDemo 演示网站 (https://www.saucedemo.com) 构建，仅用于学习与作品展示。
