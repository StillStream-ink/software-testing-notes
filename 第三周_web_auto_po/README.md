# Saucedemo Web 自动化测试项目

基于 **Python + Playwright + pytest + Allure** 的 Web 自动化测试项目，使用 **Page Object Model（PO）** 模式封装页面对象，对 SauceDemo 电商网站完成 **16 条测试用例**，覆盖正向流程、异常场景、边界条件、安全测试、UI 交互、性能场景和兼容性验证。

---

## ✨ 项目特点

- **Page Object Model**：页面元素与业务逻辑分离，代码结构清晰，易于维护和扩展
- **BasePage 基类**：封装公共方法（截图、等待、导航），减少重复代码，提升复用性
- **Playwright**：现代化的 Web 自动化测试框架，支持多浏览器、自动等待
- **pytest**：灵活的测试用例管理与执行
- **Allure 报告**：专业的测试报告，含 Environment 环境信息、步骤截图、分类展示
- **GitHub Actions CI**：代码推送后自动运行测试，Allure 报告部署至 GitHub Pages
- **多环境支持**：通过环境变量切换 dev/staging/prod 环境
- **失败自动截图**：测试失败时自动截图，快速定位问题
- **Session 级浏览器复用**：测试执行效率提升约 3 倍
- **并行执行**：支持 `pytest-xdist` 多进程并行，16 条用例从 85 秒压缩至 27 秒

---

## 🛠️ 技术栈

- Python 3.11+
- Playwright
- pytest
- allure-pytest
- pytest-xdist（并行执行）
- Allure 命令行工具
- GitHub Actions

---

## 📁 项目结构

```text
第三周_web_auto_po/
├── pages/
│   ├── base_page.py              # BasePage 基类（公共方法）
│   ├── login_page.py             # 登录页面对象
│   ├── inventory_page.py         # 商品列表页面对象
│   └── cart_page.py              # 购物车及结算页面对象
├── tests/
│   ├── test_saucedemo_po.py      # PO 模式测试用例（16 条）
│   └── test_visual_regression.py # 视觉回归测试（2 条）
├── images/                        # Allure 报告截图
│   ├── allure_overview_16pass.png
│   ├── allure_environment.png
│   ├── allure_behaviors.png
│   ├── allure_suites.png
│   └── allure_test_detail.png
├── conftest.py                    # pytest fixture 配置
├── config.py                      # 统一配置管理（URL、账号、超时）
├── environment.properties         # Allure 环境信息
├── pytest.ini                     # pytest 配置（标记、参数）
├── requirements.txt               # 项目依赖
├── run_tests.bat                  # 一键运行脚本
└── README.md
```

---

## 📋 测试用例覆盖（16 条）

| 分类 | 用例数 | 具体用例 |
|------|--------|----------|
| 登录-正向 | 2 | 标准用户登录成功、登出功能 |
| 登录-异常 | 4 | 错误密码、锁定用户、问题用户、性能抖动用户 |
| 登录-边界 | 2 | 用户名为空、密码为空 |
| 登录-安全 | 1 | SQL 注入攻击 |
| 购物车操作 | 4 | 加购 1 件、加购多件、移除商品、继续购物 |
| 结算流程 | 2 | 完整下单流程、空购物车结算 |
| 视觉回归 | 2 | 标准用户截图比对、视觉用户截图比对 |
| **合计** | **16** | |

---

## 🚀 运行方式

### 1. 安装依赖

```bash
pip install -r requirements.txt
playwright install
```

### 2. 运行测试

```bash
# 串行执行（默认）
py -m pytest -v

# 并行执行（推荐，效率提升约 68%）
py -m pytest -n 4 -v

# 冒烟测试（快速验证核心流程）
py -m pytest -m smoke -v

# 运行指定测试文件
py -m pytest tests/test_saucedemo_po.py -v
```

### 3. 生成 Allure 报告

```bash
# 生成测试数据
py -m pytest --alluredir=allure-results

# 查看报告
allure serve allure-results
```

### 4. 一键运行（Windows）

双击 `run_tests.bat`，选择运行模式即可。

> ⚠️ **注意**：Allure 报告必须通过 `allure serve` 命令打开，不能直接双击 HTML 文件。

---

## 🔧 环境切换

```bash
# 默认生产环境
py -m pytest -v

# 切换到 staging 环境（Windows PowerShell）
$env:TEST_ENV="staging"; py -m pytest -v

# 切换到 dev 环境（Windows CMD）
set TEST_ENV=dev && py -m pytest -v
```

---

## ⚡ 效率优化

引入 `pytest-xdist` 后，测试执行效率大幅提升：

| 模式 | 命令 | 耗时 |
|------|------|------|
| 串行执行 | `py -m pytest -v` | 85 秒 |
| 并行执行（4 进程） | `py -m pytest -n 4 -v` | **27 秒** |
| 冒烟测试 | `py -m pytest -m smoke -v` | 21 秒 |

---

## 🔐 环境变量配置

创建 `.env` 文件（已加入 `.gitignore`）：

```env
SD_STANDARD_USER=standard_user
SD_PASSWORD=secret_sauce
```

敏感信息不提交到版本库，本地开发使用 `.env` 加载，CI 环境通过 GitHub Secrets 注入。

---

## 📊 测试报告截图

![Allure Overview 16 Pass](images/allure_overview_16pass.png)

16 条测试用例 100% 通过。

![Allure Environment](images/allure_environment.png)

![Allure Behaviors](images/allure_behaviors.png)

![Allure Suites](images/allure_suites.png)

![Allure Test Detail](images/allure_test_detail.png)

---

## 🎯 项目亮点

- **测试覆盖**：16 条用例覆盖 8 个维度（正向/异常/边界/安全/UI 交互/购物车/结算/视觉回归）
- **代码设计**：BasePage 基类 + POM 分层 + config 统一配置
- **效率优化**：Session 级浏览器复用 + 并行执行，85 秒 → 27 秒，效率提升 **68%**
- **CI/CD**：GitHub Actions 自动运行，Allure 报告部署在 GitHub Pages
- **调试体验**：测试失败自动截图，快速定位问题
- **多环境支持**：通过环境变量切换 dev/staging/prod
- **安全加固**：密码迁移到 `.env` 环境变量，敏感信息不提交版本库

---

## 🐛 踩坑记录

### 1. 浏览器 headless 模式在 CI 环境无法启动

**现象**：GitHub Actions 报错 `launched a headed browser without having a XServer running`

**原因**：Linux CI 环境无图形界面

**解决**：通过环境变量 `HEADLESS` 控制，CI 中设为 `true`

### 2. fixture 作用域不合理导致测试执行慢

**现象**：每个用例都重新启动浏览器，执行耗时超过 60 秒

**解决**：改为 `scope="session"` 复用浏览器实例，执行时间降至 18 秒

### 3. 账号密码明文存储风险

**现象**：`config.json` 中明文存放密码

**解决**：迁移到 `.env` 环境变量，加入 `.gitignore`

### 4. 视觉回归测试跨平台误报

**现象**：本地通过，CI 失败

**原因**：不同操作系统字体渲染差异导致像素不一致

**解决**：改用 Playwright 内置截图比对，设置像素容差阈值

---

## 📝 项目说明

该项目是第三周 Web 自动化测试学习的产出，旨在展示：

- 从零搭建 Playwright 自动化测试环境
- PO 模式 + BasePage 基类的设计思路
- 结合 pytest + Allure 生成专业测试报告
- 16 条用例覆盖多维度测试场景
- GitHub Actions CI 持续集成实践
- 并行执行等工程化优化能力

该测试项目基于 SauceDemo 演示网站 ([https://www.saucedemo.com](https://www.saucedemo.com)) 构建，仅用于学习与作品展示。

更多项目请访问：[software-testing-notes](https://github.com/StillStream-ink/software-testing-notes)

---

## 🔗 相关链接

- [GitHub 仓库](https://github.com/StillStream-ink/opencart-auto-test)
- [Allure 在线报告](https://github.com/StillStream-ink/opencart-auto-test/actions)
- [掘金文章：从 Playwright 到 GitHub Actions](https://juejin.cn)

欢迎交流，一起进步！🚀
