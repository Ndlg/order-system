# 订单整理系统

面单模式驱动的可配置报货 Excel 平台。

## 项目定位

本系统用于接收采集工具或用户上传的数据，识别面单模式，读取面单内容并生成标准化明细。后续由用户在 Web 界面定义面单字段、关键字段、图片匹配、档口匹配和导出方式，系统按这些配置生成报货 Excel。

系统要做的是平台框架，不是业务规则定制。

系统只负责：

```text
面单模式识别
原始采集内容留存
面单模板解析
标准化明细管理
面单字段定义
关键字段配置
关键字段匹配规则维护
图片信息管理
档口资料维护
报货汇总引擎
Excel 导出引擎
异常提示与人工修正入口
多用户工作空间隔离
```

系统不负责在代码里定义：

```text
哪个字段代表哪种业务含义
哪些字段必须存在
哪些字段参与图片匹配
哪些字段参与档口匹配
哪些字段用于汇总分组
哪个关键字段组合对应哪张图片
哪个关键字段组合对应哪个档口
最终 Excel 必须按哪一种业务固定格式输出
```

这些全部由用户在 Web 界面配置。

## 最高原则

```text
1. 系统不是任何具体业务类型的订单系统。
2. 系统不是按任何预设业务对象整理订单。
3. 系统只按面单信息、面单模式、用户定义字段和用户配置处理数据。
4. 任何面单字段名都只能作为用户定义字段存在，系统不得预设其业务含义。
5. 字段是否使用、如何使用、是否参与匹配，全部由用户在字段配置中定义。
6. 禁止把用户业务对象作为系统一级固定对象。
7. 禁止使用 shop_id 作为核心隔离字段。
8. 不同用户维护不同字段定义、关键字段组合、图片匹配、档口匹配和导出配置。
9. 这些配置必须按 workspace_id 隔离。
10. 具体业务关系全部由用户定义，不允许写死在代码中。
```

一句话：

```text
系统只读取和处理面单，业务字段和匹配规则都交给用户定义。
```

## 核心链路

```text
采集工具 / 用户上传 Excel
  ↓
原始采集记录留存
  ↓
面单模式识别
  ↓
面单模板解析
  ↓
标准化明细
  ↓
用户定义面单字段
  ↓
用户选择关键字段
  ↓
用户配置图片 / 档口匹配规则
  ↓
报货汇总
  ↓
三种方式导出 Excel
```

## 技术栈

- 前端：Vue 3 + TypeScript + Element Plus
- 后端：Python FastAPI
- 数据库：MySQL
- 缓存：Redis
- Excel：openpyxl
- 图片处理：Pillow
- 部署：Windows 优先，后续兼容 Docker

## 开发启动

准备环境：

```text
Python 3.12+
Node.js 20+
MySQL 8+
Redis 7+
```

初始化配置：

```powershell
copy .env.example .env
mysql -u root -p < scripts/init_db.sql
```

启动后端：

```powershell
scripts\start_backend.bat
```

后端 OpenAPI：

```text
http://127.0.0.1:8000/docs
```

启动前端：

```powershell
scripts\start_frontend_dev.bat
```

前端地址：

```text
http://127.0.0.1:5173
```

默认开发账号：

```text
用户名：admin
密码：admin123
```

文件存储目录：

```text
storage/workspaces/
```

当前第一版骨架使用内存数据服务，保证前后端和 OpenAPI 可以先启动；MySQL Repository 和持久化会在下一阶段接入。

## 文档

主任务书：

- [Codex 项目任务书](docs/CODEX_TASKBOOK.md)

辅助原则文档：

- [平台职责边界](docs/PLATFORM_SCOPE.md)
- [面单驱动设计原则](docs/WAYBILL_DRIVEN_DESIGN.md)
- [配置归属与隔离原则](docs/CONFIG_SCOPE.md)

如果文档之间出现冲突，以 `docs/CODEX_TASKBOOK.md` 为准。
