# 软件测试学习笔记 & 作品集

> 从零开始，到完成 Web 自动化 + 接口自动化 + CI/CD 持续集成的完整测试项目
>
<<<<<<< HEAD
=======
> 目标岗位：初级测试工程师 / 初级自动化测试工程师
>
>>>>>>> 8375006 (docs: 更新根目录README，补充SauceDemo项目16条用例说明)
> [![CI](https://github.com/StillStream-ink/software-testing-notes/actions/workflows/ci.yml/badge.svg)](https://github.com/StillStream-ink/software-testing-notes/actions/workflows/ci.yml)


## 关于我

- 计算机专业
- 目标城市：深圳
- 目标岗位：功能测试 / 初级自动化测试工程师


## 项目成果速览

| 项目 | 技术栈 | 状态 |
|------|--------|------|
| **SauceDemo Web自动化** | Playwright + POM + Allure + GitHub Actions CI | ✅ 16条用例全部通过，CI 自动运行 |
| **OpenCart 全流程测试** | 手工测试 + 接口测试 | ✅ 104 条用例，4 个有效 Bug |
| **ReqRes 接口自动化** | Python + requests + pytest + Allure | ✅ 31 条用例，100% 通过 |
| **Midscene AI 测试探索** | Midscene.js + Playwright + MCP | ✅ 已跑通，输出文章 |


## 学习路线

| 阶段 | 状态 | 内容 |
|------|------|------|
| 测试理论基础 | ✅ | 黑盒测试方法、测试流程、Bug 生命周期 |
| 测试用例设计 | ✅ | Testin 平台考核通过（小红书首页，52 条用例） |
| Bug 探索与报告 | ✅ | Testin 平台考核通过（永辉生活 App，3 个有效 Bug） |
| Linux + SQL | ✅ | 常用命令、多表查询 |
| 接口自动化 | ✅ | Python + requests + pytest |
| Web 自动化 | ✅ | Playwright + Page Object Model + Allure |
| **持续集成（CI）** | ✅ | **GitHub Actions 自动运行测试 + 生成 Allure 报告** |


## 📂 仓库内容

### 第一周：测试入门（SauceDemo 登录功能测试）

| 文件 | 说明 |
|------|------|
| [测试用例（33条，最终版）](第一周测试产出/SauceDemo_登录功能测试用例_33条_最终版.csv) | 含步骤、预期、实际结果、优先级 |
| [测试用例说明](第一周测试产出/测试用例说明.md) | 测试范围、设计方法、版本对比 |
| [核心用例执行记录](第一周测试产出/核心用例执行记录.md) | 6 条核心用例执行结果 + 截图路径 |
| [复盘记录](第一周测试产出/复盘记录.md) | 从 16 条到 33 条的完整迭代过程 |
| [Bug报告](第一周测试产出/第一周Bug报告.docx) | 原始 Bug 报告（含后续修正说明） |
| [第一周学习笔记](第一周测试产出/软件测试第一周学习笔记.docx) | 第一周学习笔记 |

> 💡 用例从第一版的 16 条扩展至 33 条，覆盖正常/异常/边界/安全/UI/兼容性/场景法 7 个维度。


### 第二周：接口自动化

| 文件 | 说明 |
|------|------|
| [接口自动化脚本](第二周测试产出/test_api_new.py) | Python + requests + pytest |
| [OpenCart 接口测试用例](第二周测试产出/OpenCart接口测试用例.xlsx) | 31 条接口用例 |
| [第二周学习笔记](第二周测试产出/第二周学习笔记：接口自动化入门.docx) | 接口自动化入门笔记 |


### 第三周：Web 自动化（Playwright + PO 模式）

| 文件 | 说明 |
|------|------|
| [SauceDemo Web 自动化项目](第三周_web_auto_po/README.md) | Playwright + POM + Allure + GitHub Actions CI，16条用例全部通过 |
| [Allure 在线报告](https://stillstream-ink.github.io/software-testing-notes/allure-report/) | 自动化测试报告（GitHub Pages 部署） |


### 第四周：持续集成（CI） + 掘金文章

| 文件 | 说明 |
|------|------|
| [CI 配置文件](.github/workflows/ci.yml) | GitHub Actions 工作流，代码推送自动触发测试 |
| [第四周学习笔记](第四周测试产出/软件测试第四周学习笔记.docx) | CI/CD 集成学习笔记 |
| [掘金文章：从 Playwright 到 GitHub Actions](https://juejin.cn/user/3154926176044170) | 第四周实战记录（待发布） |


### AI 测试探索（独立方向）

| 文件 | 说明 |
|------|------|
| [Midscene.js 体验记录](AI测试探索/Midscene.js体验记录.md) | 自然语言驱动 UI 自动化 |
| [Midscene SDK 实战记录](AI测试探索/从跑不通到跑通了_Midscene_SDK实战记录.md) | 从 Playground 到可复用脚本 |
| [OpenCart 结算自动化实战](AI测试探索/从Midscene到Playwright_OpenCart结算自动化实战记录.md) | Midscene → Playwright 混合模式 |


### 平台考核

| 项目 | 状态 |
|------|------|
| 小红书首页测试用例（52 条） | ✅ 一次性通过 Testin 考核 |
| 永辉生活 App Bug 探索（3 个有效 Bug） | ✅ 一次性通过 Testin 考核 |


## 🛠️ 技能清单

### 测试基础
- 黑盒测试方法：等价类划分、边界值分析、场景法、错误推测法
- 测试用例设计、评审、执行
- Bug 生命周期与缺陷报告撰写
- 探索性测试

### 自动化测试
- **接口自动化**：Python + requests + pytest + Allure
- **Web 自动化**：Python + Playwright + pytest + Page Object Model
- **AI 驱动测试**：Midscene.js + Playwright-MCP（探索中）

### 工具与环境
- Postman、禅道、Git、GitHub
- GitHub Actions（CI 流水线）
- Allure（可视化测试报告）
- Linux 常用命令、SQL 基础查询


## 📝 技术文章

- [掘金 - 第一周：从零开始的第一周](https://juejin.cn/user/3154926176044170)
- [掘金 - 第二周：接口自动化入门](https://juejin.cn/user/3154926176044170)
- [掘金 - 第三周：Playwright + PO 模式](https://juejin.cn/user/3154926176044170)
- [掘金 - 第四周：GitHub Actions CI/CD 集成](https://juejin.cn/user/3154926176044170)（待发布）


## 🔗 相关项目仓库

- [OpenCart 接口自动化测试](https://github.com/StillStream-ink/opencart-api-test)
- [ReqRes 接口自动化练习](https://github.com/StillStream-ink/api-test-demo)


---

**欢迎交流，一起进步！** 🚀