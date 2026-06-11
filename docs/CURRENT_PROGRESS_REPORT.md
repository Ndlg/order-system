# 当前进度报告

> 报告日期：2026-06-11  
> 当前阶段：平台骨架阶段完成  
> 报告基线：`b188639 chore: scaffold platform application`

## 总体结论

当前项目已经从纯文档仓库进入可运行平台骨架阶段。后端、前端、采集端预留目录、Windows 脚本、环境示例、数据库初始化 SQL 和存储目录已经建立。

当前成果还不是完整业务闭环。它是后续开发登录、数据库持久化、字段配置、关键字段匹配、图片 / 档口匹配和 Excel 导出的基础骨架。

## 已完成内容

### 1. 项目结构

已建立任务书要求的主要目录：

```text
backend/
frontend/
collector-client/
docs/
scripts/
storage/workspaces/
```

### 2. 后端骨架

已完成 FastAPI 后端基础结构：

```text
backend/app/main.py
backend/app/api/
backend/app/core/
backend/app/schemas/
backend/app/models/
backend/app/services/
backend/app/repositories/
backend/app/engines/
```

已具备：

```text
FastAPI 应用入口
OpenAPI 文档
健康检查接口
开发登录接口
通用资源列表 / 创建 / 查询接口
内存数据服务
字段匹配、汇总、导出引擎占位
```

当前后端可以启动，并能访问：

```text
GET /api/v1/health
GET /api/v1/workspaces
POST /api/v1/auth/login
POST /api/v1/field-definitions
GET /openapi.json
```

### 3. 前端骨架

已完成 Vue 3 + TypeScript + Element Plus 管理后台基础结构：

```text
frontend/package.json
frontend/vite.config.ts
frontend/src/App.vue
frontend/src/router/index.ts
frontend/src/views/LoginView.vue
frontend/src/views/DashboardView.vue
frontend/src/views/GenericResourceView.vue
```

已具备：

```text
登录页
后台布局
左侧导航
仪表盘
通用资源管理页
后端 API 请求封装
```

当前前端页面是骨架级管理后台，用于连接后续模块，不是最终业务界面。

### 4. 数据库初始化 SQL

已新增：

```text
scripts/init_db.sql
```

当前 SQL 已覆盖平台骨架阶段核心表：

```text
workspaces
users
roles
user_workspaces
waybill_modes
waybill_templates
standard_detail_batches
standard_details
field_definitions
key_field_sets
match_rules
stalls
image_assets
report_batches
exception_records
export_records
operation_logs
```

SQL 已按最新平台口径设计，不包含 `product_alias_mappings`、`spec_mappings`、`product_images` 等预设业务概念表。

### 5. Windows 脚本

已新增：

```text
scripts/start_backend.bat
scripts/start_frontend_dev.bat
scripts/build_frontend.bat
scripts/start_all.bat
```

BAT 文件使用 ASCII 内容，避免 Windows 中文 echo 编码问题。

### 6. 采集端占位

已新增：

```text
collector-client/client.py
collector-client/README.md
```

当前只提供最小接口契约方向和心跳式创建记录示例，不包含真实平台采集逻辑。

### 7. 文档与环境

已新增或更新：

```text
.env.example
README.md
.gitignore
```

README 已包含：

```text
Python / Node / MySQL / Redis 环境说明
MySQL 初始化方式
后端启动方式
前端启动方式
默认开发账号
文件存储目录说明
```

## 已验证内容

已完成以下验证：

```text
Python compileall 通过
collector-client 脚本语法检查通过
后端临时 uvicorn 启动通过
GET /api/v1/health 返回正常
GET /api/v1/workspaces 返回正常
GET /openapi.json 返回正常
前端 package.json / tsconfig JSON 检查通过
git diff --check 通过
旧 product/spec/alias 业务预设术语搜索无残留
```

## 当前未完成内容

以下内容尚未进入真实实现：

```text
SQLAlchemy ORM 模型
Repository 层 workspace_id 强过滤
真实 MySQL 持久化
JWT 鉴权
密码哈希
角色权限控制
标准化 Excel 上传与解析
字段定义自动生成
关键字段组合配置的真实业务交互
图片上传与文件存储
档口匹配规则
报货汇总真实生成
Excel 三模式导出
异常记录与人工修正闭环
前端细分业务页面
自动化测试
```

## 当前限制

```text
1. 后端当前使用内存数据服务，重启后数据会丢失。
2. 当前登录为开发占位账号：admin / admin123。
3. 前端依赖尚未安装到本机 node_modules。
4. 当前机器 PATH 中未检测到 npm，因此前端 Vite build 尚未实际运行。
5. scripts/init_db.sql 是初始化 SQL，不是正式迁移系统。
```

## 风险提示

下一阶段必须优先处理以下风险：

```text
workspace_id 过滤必须落到 Repository 层，不能只依赖前端或接口参数。
不能让通用资源 API 演变成绕过权限和 workspace 的入口。
字段定义、关键字段组合、匹配规则必须保持用户配置驱动。
不能为了演示把具体业务字段或匹配关系写死在代码中。
```

## 阶段判断

当前阶段可判定为：

```text
项目骨架：完成
可启动后端：完成
OpenAPI：完成
前端骨架：完成
数据库持久化：未完成
P0 业务闭环：未完成
```

## 2026-06-11 追加进展：持久化基础层

本轮已开始推进下一阶段“数据库持久化与平台基础能力”。

已新增：

```text
SQLAlchemy 数据库连接
SQLAlchemy Base / 公共 mixin
第一批 ORM 模型
Repository 基类
workspace_id 查询过滤
JWT 生成与解析
PBKDF2 密码哈希
当前用户上下文
当前 workspace 请求头解析
开发环境自动建表与种子数据
数据库版登录接口
数据库版通用资源接口
后端 foundation 测试
前端 API token / X-Workspace-Id 请求头
```

已覆盖的 ORM 模型：

```text
Workspace
User
Role
UserWorkspace
Collector
CaptureTask
CaptureBatch
RawCaptureRecord
WaybillMode
WaybillTemplate
WaybillTemplateField
StandardDetailBatch
StandardDetail
FieldDefinition
FieldRoleConfig
KeyFieldSet
MatchRule
Stall
ImageAsset
ReportBatch
ReportLine
ExceptionRecord
ExportRecord
OperationLog
```

新增验证：

```text
pytest backend/tests -q 通过
Python compileall backend/app collector-client 通过
SQLite 临时库自动建表通过
admin 登录获取 JWT 通过
/auth/me 返回用户和 workspace 通过
创建 field-definitions 记录通过
Repository 自动写入 workspace_id 通过
```

当前仍未完成：

```text
明确资源服务替代通用资源接口
更细的角色权限策略
MySQL 实例上的实际联调
图片上传接口和文件 hash
前端工作空间选择 UI
前端配置页面细化
```
