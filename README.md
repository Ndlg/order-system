# 订单整理系统

面单模式驱动的可配置报货 Excel 平台。

## 项目定位

本系统用于接收采集工具或用户上传的数据，识别面单模式，并用平台共用解析规则把杂乱采集内容整理成客户可读的面单信息。后续由用户在 Web 界面定义如何基于这些面单信息匹配商品、图片、档口和导出方式，系统按这些配置生成报货 Excel。

系统要做的是平台框架，不是业务规则定制。

## 前端入口定位与端口边界

前端需要拆成两个 UI 应用入口，并且端口必须区分：

```text
租户端 UI：面向客户公司，包含业务页面和管理页面。
平台后台 UI：面向平台开发者 / 服务端管理员，只能部署在私有端口、内网或本机，不暴露给租户。
```

租户端 UI 包含：

```text
业务页面：员工采集面单信息、上传、查看采集记录、处理异常和导出。
管理页面：客户公司管理员维护采集连接、字段定义、关键字段、图片、档口、匹配和导出配置。
```

平台后台 UI 只维护：

```text
客户 / 租户账户
工作空间映射
用户
平台共用面单解析模式
平台共用面单解析模板
```

采集器连接、采集任务、原始采集记录、字段定义、图片、档口和导出数据都属于租户工作空间数据，不进入平台后台 UI。

第一版数据库采用：

```text
单个平台数据库
多租户逻辑隔离
tenant_id + workspace_id 数据归属
```

系统只负责：

```text
面单模式识别
原始采集内容留存
平台共用面单解析模板
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

推荐新手优先使用 Docker 启动，本机只需要安装并打开 Docker Desktop：

```powershell
scripts\docker_console.bat
```

或直接一键启动：

```powershell
scripts\docker_start.bat
```

Docker 会在容器内安装 Python/Node 依赖并构建前端，本机不需要额外安装 Python、Node、npm。

Docker 常用地址：

```text
客户业务页：http://127.0.0.1:5173
客户管理页：http://127.0.0.1:5173/admin
平台后台：http://127.0.0.1:5174/admin
后端接口文档：http://127.0.0.1:8000/docs
```

默认账号：

```text
用户名：admin
密码：admin123
```

如需开发调试，也可以使用本地服务器控制台：

```powershell
scripts\server_console.bat
```

控制台支持：

```text
一键启动客户系统（后端 + 客户 UI）
启动全部（后端 + 客户 UI + 平台后台）
查看服务状态和日志
打开客户业务页、客户管理页、平台后台
安装/更新依赖
启动本机采集器
停止服务
```

常用地址：

```text
客户业务页：http://127.0.0.1:5173
客户管理页：http://127.0.0.1:5173/admin
平台后台：http://127.0.0.1:5174/admin
后端接口文档：http://127.0.0.1:8000/docs
```

下面是手动启动方式。

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

租户端 UI：

```text
业务页面：http://127.0.0.1:5173/
管理页面：http://127.0.0.1:5173/admin
```

平台后台 UI 开发入口：

```powershell
scripts\start_platform_admin_frontend_dev.bat
```

平台后台 UI 私有地址：

```text
http://127.0.0.1:5174/admin
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

当前第一版骨架已接入 SQLAlchemy Repository 和 workspace 隔离测试；本地开发默认可用 SQLite，生产目标仍为 MySQL。

## 文档

主任务书：

- [Codex 项目任务书](docs/CODEX_TASKBOOK.md)

辅助原则文档：

- [平台职责边界](docs/PLATFORM_SCOPE.md)
- [面单驱动设计原则](docs/WAYBILL_DRIVEN_DESIGN.md)
- [配置归属与隔离原则](docs/CONFIG_SCOPE.md)
- [前端入口与受众边界](docs/FRONTEND_ENTRYPOINTS.md)

阶段文档：

- [当前进度报告](docs/CURRENT_PROGRESS_REPORT.md)
- [阶段任务书索引](docs/TASKBOOK_INDEX.md)
- [当前阶段 45：业务现场验证准备与采集器下载入口](docs/taskbooks/2026-06-13-stage-45-business-site-validation-readiness-taskbook.md)

如果文档之间出现冲突，以 `docs/CODEX_TASKBOOK.md` 为准。

## 2026-06-11 数据库与租户归属补充

当前第一版数据库方案已明确为：

```text
单个平台数据库
多租户逻辑隔离
tenant_id + workspace_id 记录客户和工作区归属
```

新增文档：

- [数据库与租户归属设计](docs/DATABASE_DESIGN.md)
- [阶段 07：数据库租户归属与数据边界闭环任务书](docs/taskbooks/2026-06-11-stage-07-database-tenant-closure-taskbook.md)
