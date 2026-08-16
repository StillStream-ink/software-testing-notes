# Midscene.js 自动化测试脚本

> 用自然语言驱动 UI 自动化的尝试，基于 Midscene.js v1.10.12

## 项目简介

本项目是基于 Midscene.js 的自然语言驱动 UI 自动化测试实践，使用 SauceDemo 网站作为测试目标，验证了"用中文描述操作意图，AI 自动执行"的可行性。

**技术栈**：Playwright + Midscene.js + TypeScript + tsx

## 文件结构

```text
midscene-scripts/
├── .env.example          # 环境变量模板
├── .env                  # 环境变量（含 API Key，不上传 GitHub）
├── package.json          # 依赖配置
├── package-lock.json     # 依赖锁定
├── saucedemo-test.ts     # 主要测试脚本
├── test-cart.ts          # 加购测试脚本
├── README.md             # 本说明文件
└── midscene_run/         # 测试报告文件夹（自动生成）
```

## 环境要求

- Node.js ≥ 18
- npm ≥ 9

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API Key：

```bash
MIDSCENE_MODEL_BASE_URL=https://your-base-url.com/v1
MIDSCENE_MODEL_API_KEY=sk-your-api-key
MIDSCENE_MODEL_NAME=qwen-plus
MIDSCENE_MODEL_FAMILY=qwen3
```

> ⚠️ **安全提醒**：`.env` 文件已加入 `.gitignore`，请勿将真实 API Key 提交到 GitHub。

### 3. 安装 Playwright 浏览器

```bash
npx playwright install
```

### 4. 运行脚本

```bash
# 完整购物流程（自然语言 + Playwright 混用）
npx tsx saucedemo-test.ts

# 纯 Playwright 定位加购测试
npx tsx test-cart.ts
```

## 脚本说明

| 脚本 | 功能 | 技术特点 |
|------|------|---------|
| `saucedemo-test.ts` | 完整购物流程：登录 → 提取商品 → 加购最低价商品 → 验证购物车 | Playwright 原生定位 + Midscene 自然语言描述 |
| `test-cart.ts` | 加购测试：登录 → 直接加购指定商品 → 查看购物车 | 纯 Playwright 定位，不依赖 AI |

## 运行示例

```text
🚀 脚本启动...
🔐 登录...
📦 获取商品数据...
商品列表: [
  { name: 'Sauce Labs Backpack', price: 29.99 },
  { name: 'Sauce Labs Bike Light', price: 9.99 },
  ...
]
最便宜的商品: Sauce Labs Onesie ($7.99)
🛒 加购 Sauce Labs Onesie...
🛍️ 查看购物车...
购物车中的商品: [ 'Sauce Labs Onesie' ]
✅ 测试通过！
🎉 测试完成！
```

## 相关链接

- [Midscene.js 官方文档](https://midscenejs.com/)
- [Midscene.js GitHub](https://github.com/web-infra-dev/midscene)
- [从 10 行定位代码到 1 句中文：Midscene.js 让 AI 帮我写测试](./Midscene.js%E4%BD%93%E9%AA%8C%E8%AE%B0%E5%BD%95.md)

## 许可证

MIT
