# 当前进度报告

> 报告日期：2026-06-11  
> 当前阶段：平台骨架阶段完成  
> 报告基线：`b188639 chore: scaffold platform application`，并已追加记录 `43085a9 feat: add database foundation and auth context` 后的进展

## 2026-06-14 追加修正：商品规则按版式指纹兜底命中

本轮根据“一个都匹配不到”的现场反馈，修正商品识别规则与我打模板绑定方式：

```text
问题原因：规则绑定的是模板配置 ID，但已采集面单里有历史空 ID 或已删除旧 ID，导致关键词匹配前就被模板过滤拦掉。
后端识别改为优先使用稳定的 printXML 版式指纹匹配，同步兼容模板 ID 和模板名称。
接口读取旧规则时，会根据当前模板配置临时补齐真实版式指纹，不要求用户重建规则。
补齐逻辑会读取模板历史记录，模板被用户删除后，旧规则仍能从软删除记录找回版式指纹。
前端后续新建规则时，会同时保存模板配置 key 和真实版式指纹。
```

真实数据验证：

```text
当前三条规则已被补齐为 printxml:cb9c8469df0b / printxml:c863897829c2 指纹。
15:01 批次：12 个商品行，已匹配 10 个，剩余 2 个为商品命中但 SKU 未命中。
17:11 批次：2 个商品行，已匹配 2 个。
17:49 批次：秒67 175 / 默认类商品仍未命中，原因是当前未建立对应商品主类规则。
```

验证结果：

```text
后端 pytest 通过：9 passed。
frontend npm run build:tenant 通过。
git diff --check 通过。
backend / tenant-ui Docker 构建并重启完成。
浏览器验证 127.0.0.1:5173 可加载到登录页。
```

## 2026-06-13 追加修正：导出表头页面简化

本轮根据“导出表头这个页面做的很复杂”的反馈，收紧管理员导出表头页：

```text
主页面不再选择多个导出样式。
导出表头固定为：商品名称、销售属性1、SKU图片、销售属性2、数量。
前面的我打模板、菜鸟模板、抖店模板只负责识别商品、SKU 和图片。
导出表头页只展示固定表头和最近批次的报货预览。
主页面不再展示 custom_product_text 等系统 key，也不再展示面单ID、面单模板等过程字段。
```

验证结果：

```text
frontend npm run build:tenant 通过。
git diff --check 通过。
tenant-ui Docker 构建并重启完成。
浏览器当前处于登录页，未代输密码；需要登录后刷新查看新页面。
```

## 2026-06-13 追加修正：最终报货表五列输出

本轮根据“类似这样就行了，不管是哪种方式的模板，最后都是输出这样的就行”的反馈，调整导出中心和报货 Excel：

```text
报货 Excel 第一张 Sheet 固定输出：商品名称、销售属性1、SKU图片、销售属性2、数量。
我打、菜鸟直打、抖店直打只影响前面的识别过程，最后统一进入同一张报货表。
同一个商品/SKU/图片自动汇总，销售属性2合并展示，数量累加。
SKU图片插入 Excel 第三列，并在导出中心预览中显示同样的图片。
未命中和冲突行不混入报货表，下载 Excel 时另放到“异常明细” Sheet。
```

验证结果：

```text
后端 pytest 通过：7 passed。
frontend npm run build:tenant 通过。
git diff --check 通过。
```

## 2026-06-12 最新推进：商品识别读取已采集面单

本轮根据“不要上传，系统不是有采集过的吗，直接选择读取就行”的反馈，收紧客户管理端商品识别页面：

```text
商品识别页取消“读取采集 Excel / 上传采集 Excel”入口。
旧的 /api/v1/matching/excel-preview 上传预览接口已移除。
页面直接读取当前工作区的 standard_details 已采集整理结果。
候选文字按当前选择的面单模式、参与识别字段和我打模板过滤。
抖店 / 菜鸟店铺直打使用平台已解析字段作为候选来源。
我打模式先选择当前工作区保存的我打模板，再读取匹配模板下的自定义打印区原文。
点击候选面单“使用”后，回填面单关键词用于保存商品识别规则。
```

验证结果：

```text
frontend vue-tsc --noEmit 通过。
frontend vite build 通过。
tenant-ui Docker 构建并重启完成。
浏览器验证 /admin/matching 已显示“读取已采集面单”，不再显示上传 Excel 入口。
```

## 2026-06-12 追加修正：我打已采集原文可见

本轮根据“我打面单没有识别到、候选表格拥挤”的反馈修正商品识别页：

```text
当前工作区确认存在 94 条 cainiao_woda_printxml 面单和 8 条 douyin_cloud_print 面单。
我打模式没有保存模板定义时，也会先展示已采集的我打自定义区原文。
保存商品识别规则时仍然要求先选择我打模板，避免未定义字段含义就保存规则。
候选面单表格增加高度、行距和主要文字列宽，去掉固定操作列。
结构化模式候选主文字不再拼入单独的数量行，数量进入规格 / 补充信息展示。
```

验证结果：

```text
frontend vue-tsc --noEmit 通过。
frontend vite build 通过。
后端 pytest 通过：6 passed, 1 warning。
tenant-ui Docker 构建并重启完成。
浏览器验证选择“菜鸟 woda 打印平台”后显示 94 条候选面单，不再显示空状态。
```

## 2026-06-12 追加修正：打印模板规则列表口径

本轮根据“列表应该是已经定义好的模板，新建默认新建我打模板定义”的反馈修正打印模板规则页：

```text
左侧列表改为“已定义模板列表”，只显示当前工作区已保存的客户模板定义。
平台默认的菜鸟 woda 打印平台解析模板不再作为列表行展示。
新增“新建我打模板”按钮，默认基于平台后台维护的我打解析模板创建客户定义。
右侧移除重复的“已有客户定义”表格，避免左右两处重复展示同一批模板。
```

验证结果：

```text
frontend vue-tsc --noEmit 通过。
后端 pytest 通过：6 passed, 1 warning。
tenant-ui Docker 构建并重启完成。
浏览器验证左侧显示模板1、模板2两条已定义模板。
浏览器验证点击“新建我打模板”后进入空白新建表单，仍基于默认我打平台模板。
```

## 2026-06-12 追加修正：我打候选字段展示纠偏

本轮根据“模板定义值固定显示到每条候选面单上，感觉不对”的反馈修正商品识别页：

```text
参与识别字段下的我打模板说明改为“模板样例；实际以每条面单为准”。
候选面单的规格 / 补充不再展示模板样例里的固定值。
候选面单改为从当前面单原文临时推断尺码和数量。
尺码推断只认更明确的位置，如 43*1、鞋码:42、逗号后独立尺码。
避免把秒45、范27等商品编号误判成尺码。
```

验证结果：

```text
frontend vue-tsc --noEmit 通过。
frontend vite build 通过。
后端 pytest 通过：6 passed, 1 warning。
tenant-ui Docker 构建并重启完成。
浏览器验证固定样例 C6全白 / 43 / 1 不再重复出现在所有候选行。
浏览器验证秒45、范27不再被误判成尺码。
```

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
frontend/src/layouts/AppShell.vue
frontend/src/layouts/WorkbenchLayout.vue
frontend/src/layouts/AdminLayout.vue
frontend/src/views/workbench/
frontend/src/views/admin/
```

已具备：

```text
登录页
用户工作台布局
管理 / 开发者后台布局
左侧导航
用户工作台流程页面骨架
后台资源管理页
后端 API 请求封装
```

当前前端已拆分为用户工作台入口和管理 / 开发者后台入口。

补充定位：

```text
当前 Vue 前端应视为管理 / 开发者验证入口。
它用于验证登录、接口、资源模型、workspace 隔离和基础 CRUD。
它不是最终面向普通业务用户的工作台。
最终用户工作台需要按“读取面单 → 定义字段 → 关键字段匹配 → 异常处理 → 导出 Excel”的任务流单独搭建。
```

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
3. 当前机器常规 PATH 中未检测到 npm；本机开发验证使用 Codex bundled Node / npm。
4. scripts/init_db.sql 是初始化 SQL，不是正式迁移系统。
5. 当前前端是管理 / 开发者验证入口，普通用户工作台尚未搭建。
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

## 2026-06-11 追加进展：前端中文化与入口定位

本轮根据当前界面形态，明确了前端入口边界：

```text
当前已搭建前端：管理 / 开发者验证入口
后续必须新增：面向普通用户的用户工作台
```

已完成：

```text
Element Plus 中文语言包接入
Day.js 中文区域设置接入
登录页、导航、工作台、通用资源页中文化
API 错误提示中文兜底
前端构建验证通过
新增前端入口与受众边界文档
新增当前下一步任务书
新增阶段任务书索引
将阶段 02、阶段 03 任务书复制到 docs/taskbooks/ 独立留档
README、主任务书、阶段任务书、平台边界、面单驱动设计文档同步更新
```

当前判断：

```text
管理 / 开发者验证入口：可用
用户工作台：当时未开始，后续已建立入口和流程骨架
前端业务闭环：未完成
```

## 2026-06-11 追加进展：用户工作台入口与后台拆分

本轮已开始执行阶段 03。

已完成：

```text
App.vue 改为单纯路由出口
新增通用 AppShell
新增 WorkbenchLayout
新增 AdminLayout
新增 /workbench 路由组
新增 /admin 路由组
登录后默认进入 /workbench
旧 /dashboard 和原扁平资源地址重定向到 /admin
现有通用资源 CRUD 归入管理 / 开发者后台
新增用户工作台首页
新增面单批次页面骨架
新增字段定义向导页面骨架
新增关键字段页面骨架
新增图片与档口页面骨架
新增匹配复核、异常处理、导出中心页面骨架
删除旧 DashboardView 和 GenericResourceView，避免入口混淆
README 增加 /workbench 与 /admin 入口说明
阶段 03 任务书更新执行进度
```

验证：

```text
前端 npm run build 通过
后端 python -m pytest backend/tests -q 通过
本地浏览器验证 /workbench 可访问
本地浏览器验证 /admin 可访问
本地浏览器验证旧 /waybill-modes 重定向到 /admin/waybill-modes
旧英文界面文案搜索未发现残留
前端未新增 shop_id / shops 核心逻辑
```

当前判断：

```text
用户工作台入口：已建立
管理 / 开发者后台入口：已建立
用户工作台流程骨架：已建立
标准化 Excel 上传：未完成
字段读取与字段定义保存：未完成
P0 报货 Excel 闭环：未完成
```

## 2026-06-11 追加校对：workspace 隔离能力与闭环缺口

本轮校对问题：

```text
平台框架是否已经可以？
不同用户不同工作空间是否读取不同数据？
```

结论：

```text
后端 workspace 隔离核心能力已经成立。
前端工作空间选择器尚未完成，因此还没有形成完整用户体验闭环。
```

已做临时验证：

```text
创建 workspace A / workspace B
创建 Alice / Bob
Alice 只绑定 workspace A
Bob 只绑定 workspace B
Alice 创建 a_field
Bob 创建 b_field
Alice 列表只能看到 a_field
Bob 列表只能看到 b_field
Alice 查询 workspace B 返回 403
Alice 使用 workspace B 创建记录返回 403
Alice 按 id 读取 Bob 记录返回 404
Alice /workspaces 只返回 workspace A
```

已新增阶段任务书：

```text
docs/taskbooks/2026-06-11-stage-04-workspace-context-closure-taskbook.md
```

阶段 04 目标：

```text
前端接入 /auth/me
建立 session / workspace 上下文
新增工作空间选择器
API 自动携带当前 X-Workspace-Id
切换 workspace 后重新加载资源数据
永久化双用户双 workspace 隔离测试
完成“不同用户读取不同 workspace 数据”的前后端闭环
```

## 2026-06-11 追加进展：workspace 上下文闭环执行

本轮已开始执行阶段 04，并完成核心闭环。

已完成：

```text
新增 backend/tests/test_workspace_isolation.py
后端永久测试覆盖双用户双 workspace 隔离
新增 frontend/src/stores/session.ts
登录后自动调用 /auth/me
路由守卫保护 /workbench 和 /admin
旧 workspace_id 不属于当前用户时自动修正
AppShell 顶部加入工作空间选择器
API 列表请求按当前 workspace_id 追加 workspace_id 查询参数
AdminResourceView 在 workspace 切换后自动重新加载
WorkbenchHomeView 显示真实当前 workspace
```

验证：

```text
后端 python -m pytest backend/tests -q 通过，2 passed
前端 npm run build 通过
浏览器验证登录后进入 /workbench 并加载用户 session
浏览器验证 /admin/field-definitions 默认 workspace 只显示 default_demo_field
浏览器验证切换到第二 workspace 后只显示 second_demo_field
```

当前判断：

```text
后端 workspace 隔离：已永久化测试
前端 workspace 选择器：已完成
API 当前 workspace 请求：已完成
多 workspace 数据切换体验：已验证
不同账号不同 workspace 的前后端闭环：核心能力已具备
```

## 2026-06-11 追加规划：采集器与打印组件连接

根据下一步方向，已新增阶段 05 任务书：

```text
docs/taskbooks/2026-06-11-stage-05-collector-print-component-taskbook.md
```

阶段 05 目标：

```text
制作部署在用户业务机上的采集器
连接系统平台
注册采集器并维持心跳
读取业务机上的打印组件数据
优先适配菜鸟打印组件和抖店打印组件
回传 raw_capture_records
支持本地队列、断网缓存和恢复补传
为后续面单模式识别和标准化明细生成提供原始数据
```

关键设计结论：

```text
采集器必须采用 adapter 模式。
菜鸟、抖店只是第一批 adapter，不能写死为唯一来源。
采集器只采集和回传 raw_payload，不定义业务字段含义。
打印组件具体读取方式需要在真实业务机环境中确认。
```

## 2026-06-11 追加修正：开发者管理员与用户采集边界

本轮根据产品边界修正：

```text
开发者管理员不维护采集信息。
开发者管理员只维护用户、工作空间和平台共用的面单解析模式/模板。
采集器连接、采集任务、原始采集记录都属于用户工作空间数据。
采集端由用户工作台连接，并上传到当前用户 workspace。
```

已调整：

```text
管理后台菜单移除采集端、采集任务、原始采集记录、字段定义、图片、档口、报表、异常和导出入口
用户工作台新增采集连接入口
用户工作台新增采集记录入口
旧 /admin/collectors、/admin/raw-capture-records 等地址重定向到用户工作台
阶段 05 任务书修正采集相关页面归属
README、平台边界、前端入口、主任务书同步修正
```

验证：

```text
前端 npm run build 通过
后端 python -m pytest backend/tests -q 通过，2 passed
浏览器验证 /admin 只显示后台概览、工作空间、用户、解析模式、解析模板
浏览器验证 /workbench 显示采集连接、采集记录
浏览器验证 /admin/raw-capture-records 重定向到 /workbench/capture-records
```

## 2026-06-11 追加修正：平台后台 UI 与租户端 UI 端口隔离

本轮根据最新产品边界修正：

```text
平台后台 UI 不能暴露给租户。
平台后台 UI 必须与租户端 UI 使用不同入口、不同端口和不同构建产物。
租户端 UI 只包含业务页面和管理页面。
```

已新增阶段任务书：

```text
docs/taskbooks/2026-06-11-stage-06-tenant-three-portal-correction-taskbook.md
```

已调整前端结构：

```text
租户端 UI 默认入口：/
租户端 UI 管理入口：/admin
平台后台 UI 私有入口：5174 端口上的 /admin
租户端路由不再 import 平台后台路由
新增 frontend/server-admin.html
新增 frontend/src/server-admin-main.ts
新增 frontend/src/router/serverAdminIndex.ts
新增 frontend/vite.server-admin.config.ts
新增 scripts/start_platform_admin_frontend_dev.bat
```

开发端口约定：

```text
租户端 UI：http://127.0.0.1:5173
平台后台 UI：http://127.0.0.1:5174/admin
```

已调整后端租户基础：

```text
新增 Tenant ORM 模型
Workspace 新增 tenant_id
新增 /api/v1/tenants 基础资源入口
默认种子数据创建 default tenant
本地 SQLite 自动补齐 workspaces.tenant_id 列
普通用户不能访问 tenants 和 users 服务端控制面资源
```

当前判断：

```text
平台后台 UI 与租户端 UI 的代码入口已分离
平台后台 UI 不应部署在租户公网端口
租户端 UI 保留业务页面和管理页面
租户层已进入基础模型阶段，后续还要继续补齐 tenant_admin / operator 权限策略
```

验证：

```text
租户端前端构建通过
平台后台前端构建通过
后端 python -m pytest backend/tests -q 通过，2 passed
租户端 dist 未检出服务端后台页面文案
```

## 2026-06-11 追加进展：数据库租户归属与数据边界闭环

本轮根据“数据库方面要先做好”的要求，先收口第一版数据库保存范围和租户归属规则。

已明确：
```text
第一版采用单个平台数据库、多租户逻辑隔离。
tenant_id 表示客户/租户归属。
workspace_id 表示客户工作区归属和当前访问控制边界。
客户业务数据必须同时带 tenant_id + workspace_id。
平台服务端后台只维护客户、工作区、用户和平台共用的面单解析模式/模板。
采集、字段、关键字段、图片、档口、匹配、异常和导出属于客户工作区数据。
```

已完成实现：
```text
WorkspaceModel 统一增加 tenant_id。
UserWorkspace 增加 tenant_id。
Repository 创建 workspace 业务数据时自动根据 workspace 写入 tenant_id。
Repository 更新 workspace 业务数据时禁止篡改 tenant_id 和 workspace_id。
Repository 保留平台维护 workspaces.tenant_id 映射的能力。
系统管理员在后端可解析全部 workspace，用于平台后台维护客户映射；面单解析模式/模板已脱离 workspace，作为平台共用解析规则。
CurrentUser 增加 tenant_ids。
/auth/me 返回 tenant_ids 和 workspace.tenant_id。
种子数据补齐 default tenant、workspace、role、membership、waybill_mode 的租户归属。
启动种子逻辑会按 workspace 回填历史业务记录 tenant_id。
SQLite 兼容迁移补齐历史开发库中的 tenant_id 字段。
scripts/init_db.sql 补齐所有 workspace 业务表的 tenant_id 和索引。
前端 CurrentUser 类型补齐 tenant_ids。
新增 docs/DATABASE_DESIGN.md。
新增阶段 07 独立任务书，未覆盖旧阶段任务书。
租户端移除旧 /client、/client-admin、/server-admin、/workbench 兼容路由，客户可见 URL 只保留 / 与 /admin。
```

阶段判断：
```text
数据库租户归属规则：已落地
新库初始化 SQL：已同步
本地 SQLite 历史库兼容迁移：已同步
账号 A 上传/创建数据写入账号 A 当前 workspace 的后端规则：已具备
跨账号、跨 workspace 数据隔离：已有测试覆盖
正式 Alembic 迁移：未开始
采集器真实连接：下一阶段推进
```

验证记录：
```text
后端 pytest backend/tests -q 通过，3 passed。
租户端 vue-tsc --noEmit 通过。
租户端 Vite build 通过。
平台私有后台 vue-tsc --noEmit 通过。
平台私有后台 Vite build --config vite.server-admin.config.ts 通过。
租户端构建产物未检出 server-admin、client-admin、/client、/workbench 旧入口字样。
git diff --check 通过，仅有 Windows CRLF 提示。
```

## 2026-06-11 追加校正：面单解析规则归属

本轮复核后确认前一条判断需要修正：

```text
平台后台不应该“管理所有客户工作区里的面单模式/模板”。
平台应该维护一套全平台共用的面单解析逻辑。
采集器读到的原始内容通常是杂乱 JSON / 文本，不能直接交给客户。
平台解析规则负责把原始采集内容整理成客户可读的面单信息。
客户在自己的管理页面维护的是：如何基于这些面单信息匹配商品、图片、档口、汇总和导出。
```

已修复的代码偏差：

```text
waybill_modes、waybill_templates、waybill_template_fields 已从 WorkspaceModel 改为 BaseModel。
三类表已改为平台全局解析规则，不再由 tenant_id + workspace_id 隔离。
scripts/init_db.sql 已移除这三类表的 tenant_id、workspace_id 和租户索引。
平台解析规则 API 已要求平台管理员权限。
standard_details 和 raw_capture_records 仍然是客户 workspace 数据。
field_definitions、key_field_sets、match_rules、image_assets、stalls 仍然是客户自定义配置。
```

同时修复权限问题：

```text
roles 写操作已收紧为平台管理员权限，避免普通可写用户通过改角色名提权为 system_admin。
鉴权上下文已忽略软删除角色，避免被删除角色继续授权。
workspaces.tenant_id 已禁止通过通用 PATCH 修改，避免工作区迁移时造成历史业务数据归属不一致。
新增后端测试覆盖角色提权防护、软删除角色失效、平台解析规则全局作用域。
```

## 2026-06-11 追加复查：代码边界收紧

本轮根据“再次收紧代码和检查目前代码问题”的要求，完成了一次进入采集器开发前的代码质量门。

已修复：
```text
登录态只从有效工作区、有效角色派生权限。
角色必须与 membership 的 tenant_id 和 workspace_id 匹配，错配角色不再授权。
软删除角色不再授予 workspace_ids、tenant_ids、roles，也不能继续写入业务数据。
没有有效角色的账号不能写入数据。
Repository 创建记录时锁定 id、审计字段、is_deleted。
Repository 更新记录时锁定 id、审计字段、is_deleted。
workspace 业务数据创建时继续由后端覆盖 tenant_id + workspace_id。
前端租户业务页面、租户管理页面、平台后台页面中文乱码已修复。
```

新增任务书：
```text
docs/taskbooks/2026-06-11-stage-08-code-tightening-check-taskbook.md
```

验证记录：
```text
后端测试通过：4 passed, 1 warning。
前端 vue-tsc --noEmit 通过。
租户端 Vite build 通过。
平台后台 Vite build --config vite.server-admin.config.ts 通过。
租户端 dist 未检出乱码和旧入口字符串。
git diff --check 通过，仅有 Windows CRLF 提示。
```

当前判断：
```text
数据库边界、权限边界、前端入口边界已具备进入采集器阶段的基础。
下一步建议继续阶段 05：采集器注册、心跳、本地队列、菜鸟/抖店 adapter 调研和 raw_capture_records 回传。
```

## 2026-06-11 追加校准：业务 UI 控制采集

本轮进一步确认 P0 用户体验：

```text
采集器静默运行并连接服务器。
用户在客户业务 UI 点击开始采集。
用户正常打印订单。
用户在客户业务 UI 点击结束采集。
采集器回传本轮原始打印 / 面单信息。
平台解析为客户可读面单信息。
系统按客户定义规则匹配商品、图片、档口。
用户生成最终 Excel 报货单。
```

已同步调整：
```text
业务首页新增本轮采集控制入口。
采集记录页新增开始采集、结束采集、刷新采集器按钮骨架。
采集器绑定、连接配置和状态维护仍归客户管理页面。
阶段 05 任务书追加采集控制入口归属勘误。
主任务书和前端入口文档同步修正。
```

## 2026-06-11 追加校准：采集器注册、连接与账号关系

本轮进一步确认采集器身份关系：

```text
员工账号登录客户业务 UI / 客户管理 UI。
采集器不使用员工账号密码登录。
采集器注册后使用 collector_token 作为设备身份连接服务器。
collector_token 对应 collector，collector 绑定 tenant + workspace。
采集器对应客户 workspace，不直接对应某个员工账号。
某次采集任务记录由哪个 user 点击开始采集和结束采集。
raw_capture_records 的 tenant_id / workspace_id 由服务器根据 collector_token 反查写入。
后端不能信任采集器自行传入 workspace_id。
```

已同步记录：
```text
阶段 05 任务书追加采集器注册、连接与账号关系勘误。
阶段 08 任务书追加采集器身份关系记录。
数据库设计文档补充 collector、collector_token、capture_task/session、raw_capture_records 的归属规则。
主任务书补充采集器设备身份原则。
```

## 2026-06-11 追加进展：最小采集器闭环

本轮根据“先做最小版本，暂时不用管真实适配”的要求，完成阶段 09 最小采集器闭环。

新增任务书：
```text
docs/taskbooks/2026-06-11-stage-09-mvp-collector-loop-taskbook.md
```

后端已完成：
```text
POST /api/v1/collector-control/register
GET  /api/v1/collector-control/status
POST /api/v1/collector-control/start
POST /api/v1/collector-control/stop
POST /api/v1/collector-runtime/heartbeat
POST /api/v1/collector-runtime/raw-records
```

前端已完成：
```text
客户管理页面可生成模拟采集器连接并显示 collector_token。
客户业务采集页可开始采集、结束采集、查看采集器状态和 raw_capture_records。
业务首页保留采集控制入口。
```

模拟采集器已完成：
```text
collector-client/client.py
使用 X-Collector-Token 心跳。
发现采集任务后上传一条模拟 raw_payload。
不接真实菜鸟 / 抖店打印组件。
```

验证记录：
```text
后端 pytest backend/tests -q 通过：4 passed, 1 warning。
前端 vue-tsc --noEmit 通过。
租户端 Vite build 通过。
平台后台 Vite build --config vite.server-admin.config.ts 通过。
```

当前判断：
```text
采集器身份、开始采集、心跳、原始记录回传、结束采集已具备最小可验证闭环。
下一步应进入 raw_capture_records -> standard_details 的平台解析最小闭环。
```

## 2026-06-11 追加进展：本地服务器控制台

本轮根据“新手部署不友好”的反馈，新增本地服务器控制台。

新增文件：

```text
scripts/server_console.py
scripts/server_console.bat
docs/taskbooks/2026-06-11-stage-11-local-server-console-taskbook.md
```

当前能力：

```text
一键启动客户系统：后端 API + 客户 UI。
启动全部：后端 API + 客户 UI + 平台后台 UI。
查看服务状态：PID、端口、URL、日志路径。
打开客户业务页、客户管理页、平台后台。
安装/更新依赖。
输入 collector_token 后启动本机采集器。
停止由控制台启动的服务。
```

使用入口：

```powershell
scripts\server_console.bat
```

阶段判断：

```text
本地新手部署入口已收拢。
下一步仍回到 raw_capture_records -> standard_details 的平台解析最小闭环。
```

## 2026-06-11 追加进展：Docker 本地部署入口

本轮根据“不想在本机部署 Python 和各种环境”的反馈，新增 Docker 本地部署方案。

新增文件：

```text
.dockerignore
docker-compose.yml
backend/Dockerfile
frontend/Dockerfile
frontend/docker/nginx.conf.template
scripts/docker_console.bat
scripts/docker_start.bat
scripts/docker_stop.bat
scripts/docker_status.bat
scripts/docker_logs.bat
docs/taskbooks/2026-06-11-stage-12-docker-local-deployment-taskbook.md
```

当前能力：

```text
使用 Docker Desktop 一键启动后端、客户 UI 和平台后台 UI。
后端容器暴露 8000。
客户 UI 容器暴露 5173。
平台后台 UI 容器暴露 5174。
前端容器内完成 npm ci 和 Vue 构建，本机不需要 Node/npm。
后端容器内安装 Python 依赖，本机不需要 Python/pip。
默认使用 Docker volume 中的 SQLite，并自动建表和初始化 admin/admin123。
```

使用入口：

```powershell
scripts\docker_console.bat
```

阶段判断：

```text
本地服务端部署可以优先走 Docker。
采集器因需要读取 Windows 打印组件本地数据库，后续应单独打包为 Windows exe，而不是放入 Linux 容器。
```

## 2026-06-11 追加进展：本地打印组件任务库复制采集器

本轮根据本机真实打印组件排查，确认采集器第一版不需要先做网络抓包或字段解析，可以优先采用本地 SQLite 任务库复制方案。

已确认：

```text
菜鸟打印组件 CNPrintClient.exe 会写入 C:\Program Files (x86)\CNPrintTool\resources\print.db。
云打印客户端 CloudPrintClient.exe 会写入 C:\Program Files (x86)\CloudPrintClient\resources\print.db。
两个组件均存在 task(taskID, msg, time) 表。
task.msg 是完整原始 JSON，是当前采集器最应该复制上传的对象。
采集器职责收敛为 copy：识别组件、记录水位、读取新增 task、上传 raw_payload。
平台后端负责解析 raw_payload 为客户可读面单信息，再进入客户自定义匹配和 Excel 导出。
```

已新增阶段任务书：

```text
docs/taskbooks/2026-06-11-stage-10-local-print-db-copy-taskbook.md
```

阶段判断：

```text
采集器真实数据入口已确认。
本地 print.db adapter、采集水位、去重上传和 README 更新已完成最小版本。
下一步应进入 raw_capture_records -> standard_details 的平台解析最小闭环。
```

## 2026-06-11 追加进展：框架健康检查与业务闭环启动判断

本轮在进入业务完整流程前，对当前框架做了一次收口检查。

已验证：

```text
Docker backend / redis / tenant-ui / platform-admin-ui 均可正常运行。
客户业务页面 http://127.0.0.1:5173 可访问。
客户管理页面 http://127.0.0.1:5173/admin 可访问。
平台后台页面 http://127.0.0.1:5174/admin 可访问。
后端健康接口 http://127.0.0.1:8000/api/v1/health 返回正常。
后端容器内 pytest -q 通过：4 passed, 1 warning。
```

本轮收紧：

```text
Docker 本地部署端口改为只绑定 127.0.0.1，避免平台后台和后端在局域网裸露。
backend/Dockerfile 增加 PYTHONPATH=/app/backend，保证容器内测试命令稳定。
frontend/.dockerignore 增加 node_modules / dist / dist-server-admin 忽略，减少前端 Docker 构建上下文。
```

当前框架判断：

```text
单平台数据库 + 多租户逻辑隔离方向成立。
tenant_id + workspace_id 数据归属方向成立。
客户业务 UI、客户管理 UI、平台后台 UI 三端分工成立。
采集器注册、collector_token、心跳、任务控制和 raw_capture_records 回传最小闭环成立。
平台共用面单解析规则表已经存在，但 raw_capture_records -> standard_details 的真实解析闭环还未完成。
```

已知噪音：

```text
后端日志中出现旧接口 POST /api/waybill/agent/poll 的 404。
当前仓库代码已不再使用该地址，现采集器地址为 /api/v1/collector-runtime/heartbeat 和 /api/v1/collector-runtime/raw-records。
该问题不阻断当前框架，但正式演示前应清理旧页面、旧进程或外部工具请求来源。
```

下一步建议：

```text
先做最小业务模拟闭环，而不是直接铺完整业务系统。
优先打通 raw_capture_records -> standard_details -> 客户可读面单信息 -> 关键字段 -> 最小匹配 -> Excel 报货单。
```

## 2026-06-11 追加进展：采集器客户端可部署化收紧

本轮根据“先做采集器”的调整，优先推进业务机采集器。

新增 / 修改：

```text
collector-client/client.py
collector-client/config.example.json
collector-client/collector_configure.bat
collector-client/collector_start.bat
collector-client/collector_check.bat
collector-client/build_windows_exe.bat
collector-client/README.md
docs/taskbooks/2026-06-11-stage-14-collector-client-hardening-taskbook.md
```

采集器新增能力：

```text
默认配置文件：%LOCALAPPDATA%\OrderSystemCollector\collector-config.json
默认状态文件：%LOCALAPPDATA%\OrderSystemCollector\collector-state.json
默认日志文件：%LOCALAPPDATA%\OrderSystemCollector\collector.log
支持 --save-config 保存服务器地址和 collector_token。
支持 --check 检查本机组件、配置和服务器 heartbeat。
支持持久化 idle_watermarks 和 capture_watermarks。
支持 bat 配置、启动、检查。
预留 Windows exe 打包脚本。
```

服务端同步增强：

```text
collectors 新增 status_payload。
collector heartbeat 上报 adapter_status、queue_size、last_error 后，服务端会保存。
后续客户管理页可以展示每台业务机上的菜鸟 / 云打印组件状态。
```

验证记录：

```text
python -m py_compile collector-client/client.py 通过。
collector-client/client.py --check 通过。
collector-client/collector_check.bat 通过。
使用真实 collector_token 验证 --save-config --check 通过。
使用账号密码验证 --login --save-config --check 通过。
本机检测到 cainiao-cnprint ready，task_count=32，max_rowid=32。
本机检测到 cloud-print-client ready，task_count=1，max_rowid=1。
后端容器 pytest -q 通过：4 passed, 1 warning。
端到端验证：账号密码登录临时采集器 -> 开始采集 -> collector --simulate 上传 1 条 raw_capture_record -> 停止采集。
```

当前仍未完成：

```text
正式 Windows exe 尚未构建和业务机验收。
采集器尚未做开机自启动 / Windows 服务安装。
客户管理页尚未展示 status_payload。
采集器已经支持账号密码登录绑定租户 / 工作区；后续可再升级为一次性激活码或二维码绑定。
```

## 2026-06-11 追加修正：采集器账号密码登录绑定

根据最新确认，采集器连接方式调整为：

```text
采集器自身输入账号密码登录服务器。
服务器根据账号所属租户 / 工作区创建或更新 collector。
collector 自动绑定 tenant_id + workspace_id。
服务器返回 collector_token。
采集器本地保存 collector_token，不保存密码。
后续心跳、任务拉取和 raw_capture_records 上传继续使用 collector_token。
```

本轮同步改动：

```text
新增 POST /api/v1/collector-runtime/login。
collector-client 支持 --username、--password、--workspace-id、--collector-id、--collector-name、--login。
collector_configure.bat 改为输入账号密码和可选 workspace_id。
客户管理页采集连接文案改为账号密码登录绑定，不再引导复制 token。
```

验证结果：

```text
后端 pytest -q 通过：4 passed, 1 warning。
租户 UI Docker 构建通过。
采集器账号密码登录端到端通过：login -> save config -> check -> start capture -> simulate upload -> raw_capture_records。
```

## 2026-06-11 追加进展：采集器可视化验收闭环

本轮完成采集器连接状态与采集回传的页面化验收。

新增 / 修改：

```text
frontend/src/views/workbench/CollectorConnectionsView.vue
frontend/src/views/workbench/CaptureRecordsView.vue
frontend/src/services/api.ts
frontend/src/styles/base.css
docs/taskbooks/2026-06-11-stage-15-collector-visual-acceptance-taskbook.md
```

客户管理页新增：

```text
已连接业务机数量
在线采集器数量
ready 打印组件数量
采集器列表
采集器展开行
adapter_status 展示
print.db 路径、task_count、max_rowid
```

客户业务页新增：

```text
本轮状态
在线采集器数量
本轮回传条数
累计原始记录
最近采集任务
每个任务回传条数
原始记录表
raw_payload 展开查看
```

验证结果：

```text
tenant-ui Docker build 通过。
后端 pytest -q 通过：4 passed, 1 warning。
浏览器打开 /admin/collector-connections 正常。
浏览器打开 /capture-records 正常。
本机采集器 online。
页面显示 ready 打印组件数量为 2。
展开采集器可看到 Cainiao CNPrintClient ready，task_count=32，max_rowid=32。
展开采集器可看到 CloudPrintClient ready，task_count=1，max_rowid=1。
业务页开始采集后进入“采集中”。
采集器模拟上传 1 条 raw_capture_record。
业务页显示本轮回传 1 条，并能看到 mvp-simulator 原始记录。
结束采集后最近任务显示 completed。
```

当前判断：

```text
采集器连接、采集、回传已经具备可视化验收闭环。
下一步可以继续做 Windows exe / 自启动，或进入 raw_capture_records -> standard_details 的最小解析闭环。
```

## 2026-06-11 追加进展：采集器可见客户端

本轮根据“采集器客户端我看不见”的验收反馈，补齐业务机上的窗口版采集器入口。

新增 / 修改：

```text
collector-client/gui.py
collector-client/collector_gui.bat
collector-client/build_windows_exe.bat
collector-client/README.md
docs/taskbooks/2026-06-11-stage-16-collector-visible-client-taskbook.md
```

窗口版采集器能力：

```text
填写服务器地址、账号、密码、工作区和采集器名称。
登录并保存 collector_token，本机不保存密码。
检查服务器心跳。
展示本机菜鸟 / 云打印组件状态、task_count、max_rowid 和 print.db 路径。
启动 / 停止持续监听服务器采集任务。
显示实时运行日志。
```

边界确认：

```text
采集器窗口的“启动监听”只代表业务机客户端连接服务器并等待任务。
客户业务 UI 里的“开始采集 / 结束采集”仍然是本轮采集的统一控制入口。
当前是最小窗口客户端，尚未做托盘常驻、开机自启动和 Windows 服务安装。
```

## 2026-06-11 追加进展：平台解析模板与采集结果整理 MVP

本轮根据“先在服务器后台维护模板，并用当前抓取面单生成抖店解析结果”的方向，完成平台解析模板和整理结果最小闭环。

新增 / 修改：

```text
backend/app/services/waybill_parser.py
backend/app/services/bootstrap.py
backend/app/api/routes/collector_runtime.py
frontend/src/views/workbench/WaybillBatchesView.vue
docs/taskbooks/2026-06-11-stage-17-platform-parser-template-mvp-taskbook.md
```

平台后台已内置：

```text
抖店 / CloudPrint 解析模式 douyin_cloud_print
菜鸟云打印解析模式 cainiao_cloud_print
抖店 CloudPrint 面单解析 v1
菜鸟云打印面单解析 v1
模板字段 logistics_no、order_no、shop_name、product_short_text、quantity 等
```

后端能力：

```text
上传 raw_capture_records 后自动尝试解析。
新增 POST /api/v1/collector-control/parse-records 支持对历史采集任务重跑解析。
解析成功后生成 standard_details，并回写 raw_capture_records.standard_detail_id、waybill_mode、parsed_payload、status。
```

本机任务 5 解析结果：

```text
parsed: 2
抖店物流单号：YT0045101273987
抖店平台订单号：6926919240176008395
抖店店铺名：帅意体育
抖店商品简称：【新款5.0跑鞋透气超轻减】5.0黑白紫 38.5 1 件
抖店数量：1
菜鸟自定义区文本：秒55 d，,C6全白，43*1
```

客户业务页：

```text
http://127.0.0.1:5173/waybill-batches
```

现在展示整理后的 `standard_details`，不再只是 raw JSON。

## 2026-06-11 追加修正：采集器在线与监听状态区分

本轮根据真实打印后未采集到的反馈，定位原因：

```text
本机两个打印组件已经写入新任务：
CloudPrintClient rowid=2，时间 2026-06-11 20:24:46。
Cainiao CNPrintClient rowid=33，时间 2026-06-11 20:25:28。
服务器任务 5 在 20:24:32 开始、20:26:28 结束。
但采集器窗口当时只打开，未处于监听状态，因此没有在任务 5 活动期间拉取并上传这两条数据。
```

已补救：

```text
将这两条真实打印记录补传到任务 5，raw_capture_records inserted=2。
```

已修正框架逻辑：

```text
collector heartbeat 增加 runtime_status。
单次检查上报 checking。
持续监听上报 listening。
客户管理页和采集记录页增加“监听中采集器”指标。
窗口版采集器在已有 token 时打开后自动启动监听。
```

## 2026-06-11 追加整改：菜鸟来源拆分与解析结果修正

本轮根据真实打印样例和业务判断，修正阶段 17 中把菜鸟组件统一当成一种解析模式的问题。

新增阶段任务书：

```text
docs/taskbooks/2026-06-11-stage-18-cainiao-source-split-taskbook.md
```

核心结论：

```text
同一个本地打印组件不等于同一种平台解析模式。
解析模板应按 component + source + payload_shape 判断。
菜鸟店铺直接打印可以抽取结构化订单字段。
菜鸟 woda 打印平台中转时，标准面单字段多为加密或脱敏。
woda 的 printXML / CDATA 用户自定义区只保存原文，不解释为商品、规格或数量。
一个 raw_capture_record 内如果包含多个 document，必须生成多条 standard_details。
```

已完成代码整改：

```text
backend/app/services/waybill_parser.py
backend/app/services/bootstrap.py
backend/app/api/routes/collector_runtime.py
backend/tests/test_foundation.py
frontend/src/views/workbench/WaybillBatchesView.vue
docs/CODEX_TASKBOOK.md
docs/TASKBOOK_INDEX.md
```

新增 / 调整平台解析模式：

```text
douyin_cloud_print       抖店 / CloudPrint
cainiao_direct_shop      菜鸟店铺直接打印
cainiao_woda_printxml    菜鸟 woda 打印平台
cainiao_cloud_print      菜鸟云打印（遗留，默认禁用）
```

验证结果：

```text
后端 pytest -q 通过：4 passed, 1 warning。
py_compile 通过：waybill_parser.py、bootstrap.py、collector_runtime.py。
测试覆盖菜鸟店铺直打、菜鸟 woda 多 document 拆分、抖店 CloudPrint 解析。
Docker 后端、客户 UI、平台后台 UI 已重建并启动。
平台后台 /admin/waybill-modes 已显示 cainiao_direct_shop、cainiao_woda_printxml，并禁用 legacy cainiao_cloud_print。
任务 5 已用 force=true 重跑解析：parsed=2，客户业务页显示菜鸟 woda 1、抖店 1。
```

下一步建议：

```text
先用真实打印样例重新跑一轮采集和 force 解析，验收页面字段。
随后做平台后台解析模板详情页。
再进入客户管理页的字段选择、关键字段规则、商品图片、档口匹配和 Excel 导出。
```

## 2026-06-11 追加整改：面单批次按采集任务隔离

本轮根据页面验收反馈修正两个体验问题：

```text
问题 1：客户业务页把当前工作区全部 standard_details 混在一起展示，新打印批次会和旧批次混杂。
问题 2：菜鸟 woda 中转面单无法提供可用业务字段，却以空字段行进入主表，显得系统未完善。
```

已完成整改：

```text
客户业务页增加采集任务选择器，默认选择最新任务。
主表改为“本轮可处理面单”，只展示当前任务下可进入匹配和导出的明细。
受限采集进入“采集诊断”，不进入匹配和导出。
菜鸟 woda 解析状态改为 limited，不再生成 standard_details。
force=true 重跑解析会清理旧的 woda 明细。
业务页不再展示数据库内部 ID，改用本轮序号、最近一轮 / 上一轮等业务文案。
采集诊断区明确展示“菜鸟 / 我打中转”、原始文档 ID、受限原因和可见原文，方便确认数据没有丢失。
```

## 2026-06-11 追加纠偏：商品文字是主数据

本轮根据业务反馈再次校正解析口径：

```text
系统后续要匹配的是商品、规格、备注等可见文字。
物流单号、平台订单号、店铺名可以保留，但不是本阶段主信息。
菜鸟 / 我打 woda 虽然拿不到完整标准面单字段，但 printXML / CDATA 中能读取到商品文字，因此应进入主流程。
```

已完成调整：

```text
菜鸟 woda 的 custom_area_raw_text 同步写入 product_full_text、product_short_text、spec_text。
菜鸟 woda 重新生成 standard_details，不再作为 limited 诊断记录处理。
客户业务页主表改为“本轮商品信息”，商品文字成为第一主列。
来源、辅助单号、图片、档口保留为辅助列。
未识别区仅用于完全没有读到可用商品文字的采集内容。
```

验证结果：

```text
后端 pytest -q 通过：4 passed, 1 warning。
py_compile 通过：waybill_parser.py。
Docker backend / tenant-ui 构建通过。
```

## 2026-06-11 追加进展：客户侧配置与大批量查看 MVP

本轮按“平台端先封板，开始做用户端管理页和业务页”的方向推进。

新增阶段任务书：

```text
docs/taskbooks/2026-06-11-stage-19-client-config-workflow-mvp-taskbook.md
```

已完成：

```text
业务页本轮商品信息支持搜索、来源筛选和分页。
通用资源列表 limit 上限从 500 提升到 2000，方便大批量采集验证。
字段用途页展示平台解析字段，并自动同步到当前工作区配置。
关键字段页可保存商品匹配组合和来源追溯组合。
图片与档口页可手动新增图片资料和档口资料。
匹配规则页可建立“商品关键词 -> 图片 / 档口”的最小规则。
```

验证结果：

```text
后端 pytest -q 通过：4 passed, 1 warning。
py_compile 通过：resources.py、waybill_parser.py。
Docker backend / tenant-ui 构建通过并已重启。
浏览器验证 /waybill-batches、/admin/field-definition、/admin/matching 可正常打开。
```

当前判断：

```text
客户侧管理页已经从占位进入最小可配置阶段。
下一步建议让用户先跑一轮大批量采集，再基于真实商品文字保存字段、关键字段、图片档口和关键词规则。
随后实现自动匹配执行按钮，将规则命中结果回写到商品明细。
```

字段页纠偏：

```text
字段不再表达为“客户定义候选字段”。
平台解析模板已经提供商品信息、规格文本、数量、来源、辅助单号等平台字段。
客户管理页改为“字段用途”，进入页面时自动同步平台字段到当前工作区配置。
页面不再显示“采集字段候选”“保存默认字段”“未保存”。
客户管理员后续只配置字段是否参与匹配、显示和导出。
```

验证结果：

```text
后端 pytest -q 通过：4 passed, 1 warning。
py_compile 通过：waybill_parser.py。
Docker tenant-ui 构建通过，包含 vue-tsc 类型检查。
```

## 2026-06-11 追加纠偏：商品是父级，SKU 是子级

本轮根据业务反馈修正商品图片导入模型：

```text
商品名称不是从 ZIP 或图片文件名自动推断。
客户应先在管理页创建商品，例如“匡威商品”。
客户选中这个商品后，再上传这个商品对应的 SKU 图片 ZIP。
ZIP 里的 SKU 图片全部归属到当前选中的商品下面。
最终形成：商品 -> 多个 SKU -> SKU 图片。
```

已完成：

```text
新增 products 数据模型和 product_skus 数据模型。
新增 /products、/product-skus 通用资源接口。
新增 /products/{product_id}/sku-zip 上传接口。
接口会校验当前 product_id 属于当前 workspace，避免跨租户导入。
SKU 图片文件保存到 workspace_id / product_id 目录下。
图片元数据保存到 image_assets，SKU 记录绑定 image_asset_id。
客户管理页新增“商品/SKU”入口。
页面流程改为“新增商品 -> 选择商品 -> 上传该商品的 SKU ZIP -> 查看 SKU 列表”。
```

当前支持口径：

```text
当前最小版本只导入 ZIP 中 SKU图 目录下的图片。
详情图、主图、页面展示图暂不进入匹配流程。
商品名称始终以客户创建和选中的商品为准。
文件名只用于辅助生成 SKU 名称，不写入匹配关键词。
商品 / SKU 页面不维护关键词，商品识别规则只负责把面单关键词关联到商品。
SKU 由系统使用面单商品文字与该商品下的 SKU 名称自动匹配。
```

验证结果：

```text
后端 pytest 通过：5 passed, 1 warning。
后端 py_compile 通过。
Docker backend / tenant-ui 构建通过并已重启。
浏览器验证 /admin/products 页面正常打开。
未选择商品时 SKU 上传禁用，符合“先定义商品，再上传 SKU 包”的流程。
```

下一步建议：

```text
继续把自动匹配逻辑调整为“面单商品文字 -> 商品 -> SKU -> 图片 / 档口”。
补商品识别规则页，并补图片预览和 SKU 自动匹配结果复核。
再把匹配结果回写到标准面单明细，并进入 Excel 报货单导出。
```

## 2026-06-11 追加纠偏：客户侧不再暴露字段用途和关键字段

本轮根据业务反馈修正客户管理页流程：

```text
服务端提供面单解析能力。
业务端使用解析出来的商品文字、规格文字、数量等结果去关联商品。
客户不需要先进入“字段用途”或“关键字段”两个抽象页面。
```

已完成：

```text
客户管理页左侧移除“字段用途”。
客户管理页左侧移除“关键字段”。
旧地址 /admin/field-definition 和 /admin/key-fields 自动跳转到 /admin/matching。
“匹配规则”改名为“商品识别”。
商品识别页不再展示字段说明表，客户直接输入面单上看到的商品关键词。
商品识别页不再展示关键词命中统计，避免客户误解为必须依赖系统候选字段。
商品识别页支持输入关键词并关联到商品，不再人工指定 SKU。
SKU 由系统使用面单商品文字与该商品下的 SKU 名称自动匹配。
系统内部仍自动维护商品识别所需的 key_field_set，但不再暴露给客户操作。
```

验证结果：

```text
后端 pytest 通过：5 passed, 1 warning。
tenant-ui Docker 构建通过并已重启。
```

## 2026-06-11 追加进展：采集信息导入与识别预览页

本轮根据“做个导入采集信息预览匹配识别商品的页面”的要求，新增阶段 22。

新增任务书：

```text
docs/taskbooks/2026-06-11-stage-22-recognition-import-preview-taskbook.md
```

已完成：

```text
客户管理页新增“识别预览”入口。
新增 /admin/recognition-preview 页面。
页面支持从采集任务导入 standard_details。
页面支持临时粘贴面单商品文字做预览。
预览时先按商品识别规则命中商品。
商品命中后，在该商品下自动匹配 SKU。
展示导入数、商品命中数、SKU 命中数、图片就绪数。
展示每条面单商品文字、商品识别结果、SKU 自动匹配结果、图片预览和状态。
```

当前边界：

```text
本阶段只是预览，不把识别结果写回 standard_details。
SKU 自动匹配为最小启发式算法，后续需要用真实大批量样本继续调优。
档口匹配和 Excel 报货单导出还未接入。
```

验证结果：

```text
tenant-ui Docker 构建通过。
后端 pytest 通过：5 passed, 1 warning。
浏览器验证 /admin/recognition-preview 页面正常打开。
浏览器验证临时粘贴一条面单商品文字后可生成预览行。
```

## 2026-06-11 追加进展：采集任务文档下载与表头定义

本轮根据“采集任务采集的原文和识别后生成的文档提供下载”的要求，新增阶段 23。

新增任务书：

```text
docs/taskbooks/2026-06-11-stage-23-task-document-download-and-definition-taskbook.md
```

已完成：

```text
新增采集任务原文 Excel 下载接口。
新增采集任务整理结果 Excel 下载接口。
采集记录页最近任务增加“原文 / 整理”下载按钮。
面单批次页当前任务增加“下载原文 / 下载整理文档”按钮。
识别预览页增加可编辑表头定义草稿。
客户保存后，整理文档表头写入当前 workspace。
整理结果下载只按当前 workspace 已保存表头输出，不再使用平台固定表头。
```

当前口径：

```text
原文文档用于诊断采集器回传内容，结构由平台提供。
整理文档是客户业务文档，表头和取值来源必须由客户定义。
商品简称 / 规格 / 尺码 / 数量只是可保存的示例表头，不固定在系统中。
```

验证结果：

```text
后端 pytest 通过：5 passed, 1 warning。
backend Docker 构建通过。
tenant-ui Docker 构建通过。
```

## 2026-06-11 追加进展：面单原文识别样本标注 MVP

本轮根据“复杂自定义文字需要客户自己点选定义”的方向，新增阶段 24。

新增任务书：

```text
docs/taskbooks/2026-06-11-stage-24-recognition-sample-labeling-taskbook.md
```

已完成：

```text
客户管理页新增“识别样本”入口。
新增 /admin/recognition-samples 页面。
页面支持粘贴面单商品原文。
页面支持把原文拆成候选片段。
页面支持点选片段并放入商品关键词、规格、尺码、数量。
页面支持选择该原文对应的商品。
页面支持保存当前工作区识别样本。
页面支持查看已保存样本。
```

当前口径：

```text
识别样本不是平台固定规则。
识别样本属于客户工作区数据。
本阶段先验证交互和沉淀样本。
后续再把样本接入识别预览、未识别行复核和整理文档生成。
```

验证结果：

```text
后端 pytest 通过：5 passed, 1 warning。
tenant-ui Docker 构建通过。
tenant-ui 容器已重启。
浏览器验证 /admin/recognition-samples 页面正常打开。
浏览器验证粘贴样例文本后可拆出候选片段。
```

## 2026-06-11 追加修正：识别预览显式规则收紧

本轮根据“没有定义 5.0，为什么系统识别到 5.0”的反馈，新增阶段 25。

新增任务书：

```text
docs/taskbooks/2026-06-11-stage-25-recognition-preview-explicit-rules-taskbook.md
```

问题原因：

```text
识别预览页原先有商品名称兜底匹配。
当商品库存在名为“5.0”的商品时，即使客户没有维护“5.0”识别规则，系统也会用商品名称自动命中。
```

已完成：

```text
移除商品名称兜底匹配。
识别预览只使用客户显式维护的商品识别规则。
识别预览接入识别样本中的 product_keyword。
命中信息增加来源显示：商品识别规则 / 识别样本。
```

当前口径：

```text
商品名称只是商品资料，不自动等同于识别规则。
客户没有在商品识别或识别样本里定义的关键词，不应该自动命中商品。
```

验证结果：

```text
后端 pytest 通过：5 passed, 1 warning。
tenant-ui Docker 构建通过。
tenant-ui 容器已重启。
```

## 2026-06-15 追加：现场 Alpha 整改与发布收口启动

本轮根据项目当前进度评估，确认系统已经跑通真实业务主链路，但仍处于现场验证 Alpha。后续不再继续无序堆功能，先按步骤做源码、采集器、样本回归、报货 Excel 和部署文档收口。

新增任务书：

```text
docs/taskbooks/2026-06-15-stage-48-site-alpha-hardening-taskbook.md
```

新增配套清单：

```text
docs/PROJECT_RECTIFICATION_TASK_LIST.md
```

阶段 48 整改范围：

```text
1. 源码冻结与工作树收口。
2. 采集器产品化整改，正式交付物收口为“订单系统采集器.exe”。
3. 面单解析与识别回归集，沉淀现场问题样本。
4. 报货 Excel 与档口流程验收。
5. 部署、迁移和发布文档收口。
```

当前执行原则：

```text
先稳定主链路，再扩展高级配置。
现场问题必须沉淀成测试样本。
采集器不再以 bat/vbs/临时脚本作为正式交付方式。
识别不确定时必须暴露异常，不自动猜。
重解析、清库、远程业务机操作必须先确认影响范围。
```

## 2026-06-15 追加：阶段 48 P0 源码冻结审计

本轮开始执行 P0 第一项“源码冻结与工作树收口”，只做审计和文档更新，不清库、不重解析、不连接业务机。

新增审计记录：

```text
docs/taskbooks/2026-06-15-stage-48-p0-source-freeze-audit.md
```

已确认运行基线：

```text
源码目录：<PROJECT_DIR>
Compose 项目：order-system
租户端：0.0.0.0:5173
平台端：127.0.0.1:5174
后端：127.0.0.1:8000
数据卷：order-system-data
数据库：/data/order-system.db，约 14MB
```

工作树审计结果：

```text
修改：44
删除：12
未跟踪：34

主要变更集中在：
backend：解析、识别、采集器运行时、报货导出、档口与账号。
frontend：管理后台、工作台、商品/SKU、档口库、识别规则、导出版式。
collector-client：单 exe/token/后台循环方向收口。
docs：阶段 40-48 任务书和整改清单。
storage：存在应从版本中移除的运行文件和预览图。
```

当前判断：

```text
collector-client/assets 下的图标资产应进入版本管理。
storage/collector-review 和 review zip 是人工审核产物，不应入库。
storage/collector-test、storage/server-console、storage/sku-import-preview 属于运行垃圾，应在后续 P0-1 中从版本中移除并由 .gitignore 接管。
storage/parser-samples 如仍需保留，应迁移为 tests fixtures 或 docs reference。
```

下一步建议：

```text
执行 P0-1：清理 storage 跟踪状态和 .gitignore。
执行前不动业务数据库，不影响当前 Docker 服务。
```

## 2026-06-15 追加：阶段 48 P0-1 Storage 忽略规则收口

本轮继续推进 P0-1 的低风险部分，只调整版本管理边界：

```text
1. .gitignore 新增 storage/collector-review/。
2. .gitignore 新增 storage/*-review.zip。
3. 本地 storage/collector-review/订单系统采集器.exe 保留，供人工审核，不删除。
4. storage/订单系统采集器-review.zip 保留在本地，但不进入 git 状态。
```

当前 storage 判断：

```text
storage/collector-test/collector-state.json：历史运行状态，保持删除，后续随清理提交移出版本。
storage/server-console/backend-deps.ok：历史运行标记，保持删除，后续随清理提交移出版本。
storage/sku-import-preview/*.png：历史 SKU 预览图，保持删除，后续随清理提交移出版本。
collector-client/assets/*.png / *.ico：采集器正式图标资产，应进入版本管理。
```

本轮未执行：

```text
未清库。
未重解析。
未删除 review exe。
未连接业务机。
```

## 2026-06-15 追加：阶段 48 P0-2 采集器交付物核对

本轮继续推进 P0-2 的本地核对部分，只检查交付物、下载包和参数说明，不连接业务机。

当前 collector-client 目录：

```text
collector-client/client.py
collector-client/build_windows_exe.bat
collector-client/README.md
collector-client/config.example.json
collector-client/assets/order-system-collector-icon.png
collector-client/assets/order-system-collector.ico
collector-client/dist/订单系统采集器.exe
```

后端下载 ZIP 实际内容：

```text
订单系统采集器/VERSION.txt
订单系统采集器/订单系统采集器.exe
订单系统采集器/参数说明.txt
```

已确认：

```text
下载 ZIP 不包含 Python 源码。
下载 ZIP 不包含 bat/vbs。
下载 ZIP 不包含测试环境 IP。
参数说明包含 base-url、token、collector-name、loop、save-config、check、log-file。
参数说明明确禁止业务机运行 Python、bat/vbs、系统账号密码和后端 8000 端口。
backend/tests/test_collector_client_runtime.py 通过：2 passed。
```

仍需业务机验证：

```text
任务管理器进程名是否显示为“订单系统采集器.exe”。
无黑框后台启动是否在三台业务机都成立。
关闭 SSH 会话后采集器是否仍运行。
后端重启 / 网络中断后采集器是否保持等待重连。
三台业务机旧 bat/vbs/临时采集器是否已清理。
```

## 2026-06-13 追加记录：我打模板识别引擎当前已知缺陷

本轮确认我打模板识别引擎已能覆盖当前店铺常见运行方式：按 printXML 版式指纹命中客户模板，单商品和多商品统一读取为商品项列表，商品项内包含商品文字、销售属性1、销售属性2、数量和备注字段；商品识别和导出可以按商品项展开。

当前先记录以下缺陷，不作为现场验证阻塞项：

```text
1. 商品项边界主要依赖内置解析规则，不是完全由用户自定义。
2. 用户暂时不能配置“一个商品项从哪里开始、到哪里结束”。
3. 跨多行商品、无常见数量标记、多商品混入备注等复杂面单可能仍需补规则。
4. 当前店铺业务先按现有引擎跑起来，等真实业务稳定后，再根据失败样本集中增强模板解析能力。
```

## 2026-06-13 追加记录：进入报货 Excel 导出阶段

新增阶段 46：

```text
docs/taskbooks/2026-06-13-stage-46-report-excel-export-closure-taskbook.md
```

当前判断：

```text
模板识别、商品项拆分、商品主类识别和 SKU 自动匹配已经能支撑当前店铺现场验证。
下一阶段进入导出闭环，目标是从监听批次的商品识别结果生成可用报货 Excel。
现有“下载整理文档”只按字段表头导出，不等同于最终报货单。
导出阶段第一版先做无图片 Excel：一行一个商品项，展示商品、SKU、数量、匹配状态和异常原因。
SKU 图片嵌入、档口拆分、分组 Sheet 和后台异步导出放到后续增强。
```

本轮已完成：

```text
新增后端报货 Excel 下载接口 /api/v1/collector-control/tasks/{task_id}/recognition-report。
报货 Excel 使用商品识别预览同一套 recognize_detail_items 结果。
导出中心从占位页改为可用页：选择监听批次、查看识别汇总、预览商品行、下载报货 Excel。
前端 tenant 构建通过。
后端相关 pytest 通过：6 passed。
浏览器验证 /exports 可打开，能显示最近批次、商品行汇总和报货结果预览。
backend 和 tenant-ui 容器已重建并启动。
```

追加完成：

```text
管理员导出表头页新增预设导出表头。
预设包括：我打报货基础、抖店基础整理、菜鸟直打基础整理、物流核对。
用户可一键用模板替换当前表头，替换后仍可编辑表头名称、字段和排序。
导出表头页补充菜鸟/淘宝店铺直打字段说明。
新增导出 Excel 预览表，按当前已定义表头和最近采集样例展示。
未保存表头时，预览区先展示“我打报货基础”临时预览。
前端 tenant 构建通过。
浏览器验证 /admin/export-headers 可打开，预设区和 Excel 预览区显示正常，控制台无错误。
```

混合批次导出纠偏：

```text
明确一次监听批次可能混合我打、菜鸟/淘宝直打和抖店直打。
正式报货 Excel 改为按该批次全部商品识别结果统一导出，不按面单来源拆开。
报货 Excel 增加“报货图”列。
报货图根据识别命中的 SKU 绑定图片嵌入 Excel。
SKU 已命中但未绑定图片时，不阻断导出，报货图列留空。
抖店/菜鸟直打的 SKU 自动匹配补充读取 product_short_text、spec_text、product_full_text、buyer_remark 和 seller_remark。
导出中心预览增加报货图绑定状态和已绑定图片数量。
后端相关 pytest 通过：7 passed。
前端 tenant 构建通过。
```

追加完成：

```text
导出中心报货结果预览中的报货图列改为直接展示 SKU 图片缩略图。
缩略图来源为识别命中的 SKU 绑定图片 sku_image_asset_id。
没有绑定图片时仍显示未绑定状态。
tenant-ui 容器已重建。
```

导出表头预设语义修正：

```text
原“套用”会把多个预设叠加保存，容易导致导出预览出现大量重复或无关列。
按钮改为“替换当前表头”。
点击模板时弹出确认，说明会清空当前表头并重新生成。
执行时先删除当前工作区已启用导出表头，再写入所选模板字段。
tenant-ui 构建通过并已重建。
```

关联任务书：

```text
docs/taskbooks/2026-06-13-stage-45-business-site-validation-readiness-taskbook.md
```

## 2026-06-12 追加修正：商品识别页隐藏模板样例

本轮根据“不要显示给用户”的反馈，继续收紧客户管理端商品识别页。

已完成：

```text
商品识别页的我打模板参与识别字段只显示字段名称。
隐藏“模板样例：...”这类内部辅助说明，不再把模板样例暴露给用户。
已采集面单候选列表按面单 ID 倒序展示，新采集面单排在上方。
阶段记录追加到 docs/taskbooks/2026-06-12-stage-39-client-template-rule-ui-taskbook.md。
```

## 2026-06-12 追加修正：我打模板识别码与客户模板边界

本轮根据“我打模板公开，商品名称 / 规格 / 数量是否真的无法解析，以及不同客户不同模板怎么识别”的反馈，新增阶段 38。

新增任务书：

```text
docs/taskbooks/2026-06-12-stage-38-woda-template-fingerprint-taskbook.md
```

已完成：

```text
菜鸟 woda / 我打中转继续读取 printXML / CDATA 中的可见商品区原文。
后端新增 print_template_key，用去除具体文字后的 printXML 布局生成模板识别码。
后端新增 print_template_source，标记模板识别来源。
后端新增 custom_area_lines，保留自定义区每段可见文字。
客户批次详情可展示模板识别码相关字段。
测试覆盖同一 printXML 布局生成同一个模板识别码。
```

当前口径：

```text
平台不破解 encryptedData。
平台负责识别面单模式、读取可见商品区原文、生成模板识别码。
平台不知道每个客户模板字段的业务含义。
客户管理员后续在自己工作区按模板识别码定义拆分规则。
不同客户的模板规则仍按 tenant_id / workspace_id 隔离。
```

验证结果：

```text
后端 pytest 通过：7 passed, 1 warning。
backend/app/services/waybill_parser.py py_compile 通过。
tenant-ui Docker 构建通过。
platform-admin-ui Docker 构建通过。
```

## 2026-06-12 追加修正：客户管理端打印模板规则 UI

本轮根据“三种面单模式，其他两种已经能识别模板规则，要做合理 Web UI 给用户”的反馈，新增阶段 39。

新增任务书：

```text
docs/taskbooks/2026-06-12-stage-39-client-template-rule-ui-taskbook.md
```

已完成：

```text
新增 print_template_configs 工作区级配置表。
新增 /api/v1/print-template-configs 通用资源接口。
客户管理侧边栏新增“打印模板规则”。
客户管理首页新增“打印模板规则”入口。
新增 /admin/print-template-rules 页面。
页面按当前工作区已采集 standard_details 汇总模板组。
抖店 / 菜鸟店铺直打显示平台已解析字段样例。
菜鸟 woda / 我打中转显示自定义区行文字、拆分规则和预览。
旧解析样本标记为“旧样本”，不再把菜鸟标准模板 URL 当作我打模板识别码。
```

当前口径：

```text
三种面单模式进入同一个模板管理入口。
结构化模式只需要客户确认样例和后续选择字段用途。
自定义文本模式需要客户定义拆分规则。
模板规则按 tenant_id / workspace_id 保存，不能跨客户共享。
```

验证结果：

```text
后端 pytest 通过：7 passed, 1 warning。
后端 py_compile 通过。
tenant-ui Docker 构建通过。
backend Docker 构建通过。
backend 和 tenant-ui 已重启。
浏览器验证 http://127.0.0.1:5173/admin/print-template-rules 可打开。
```

阶段 39 追加修正：

```text
我打模板规则页增加“设为商品 / 设为规格”行按钮。
已保存的我打自定义模板规则支持删除定义。
抖店 / 菜鸟店铺直打只读展示平台字段样例，不提供删除按钮。
浏览器验证已定义我打模板显示删除入口，平台已解析模板操作列显示为“-”。
```

阶段 39 追加修正 2：

```text
平台已解析模板不再显示客户采集到的真实业务样例值。
“样例”列改为“原始字段”，只展示 shopName、productInfo、ITEM_INFO 等原始字段名。
我打模板样本选择器只显示当前工作区面单 ID。
我打模板可从原始面单可见文字片段中点击设置商品、规格、尺码、数量。
浏览器验证抖店模板字段区不再出现店铺名或商品标题真实样例。
```

阶段 39 追加修正 3：

```text
客户管理端模板列表改为读取平台后台维护的 waybill_modes / waybill_templates / waybill_template_fields。
业务端不再根据采集样本里的 templateCode、templateURL 或 printXML 指纹自行生成模板行。
采集样本只挂到对应平台面单模式下面，用于显示样本数量和给我打自定义模板提供可见文字。
平台模板名称以服务端后台模板为准，客户自定义名称只作为当前工作区定义显示。
普通客户账号可以读取平台模板目录，但不能新增、修改、删除平台模板。
```

阶段 39 追加修正 4：

```text
我打自定义打印区增加“新建定义”入口。
模板列表操作列对我打自定义模板显示“新建”，平台已解析模板仍显示“-”。
右侧模板详情头部增加“新建定义”按钮。
新建定义会清空当前表单，底部保存按钮切换为“新建定义”。
保存时按当前采集样本的 print_template_key 保存客户定义，不修改平台模板。
浏览器验证“新建定义”按钮出现，并能进入新建状态。
```

阶段 39 追加修正 5：

```text
打印模板规则页收窄为专门维护“我打面单模板”。
抖店 / 菜鸟店铺直打不再显示在打印模板规则页，它们只在商品识别等业务页面展示平台字段。
我打模板新建定义使用独立客户定义 key，修复误用 platform-template key 导致保存唯一键冲突的问题。
右侧增加“已有客户定义”列表，保存后的客户模板定义会显示在这里，可编辑或删除。
商品识别页改为读取平台后台模板字段，展示原始字段路径供用户查看和选择参与识别。
后端资源创建遇到唯一键冲突时返回 409，不再返回 500。
浏览器验证打印模板规则页只显示我打模板；商品识别页显示平台模板原始字段。
```

阶段 39 追加修正 6：

```text
商品识别页选择“菜鸟 woda 打印平台”时，改为先选择当前工作区已保存的我打客户模板。
我打商品识别不再直接展示 source_platform、raw_document_id 等 woda 平台原始字段。
我打模板下拉读取 print_template_configs。
选中我打模板后，参与识别字段来自模板定义出的商品文字、规格文字、数量文字和尺码文字。
没有我打模板定义时，商品识别页提示先去“打印模板规则”新建模板。
浏览器验证选择“菜鸟 woda 打印平台”后出现“我打模板”下拉，并且不再显示 woda 原始平台字段。
```

## 2026-06-12 追加整理：框架收紧与验证入口整理

本轮根据“先收紧代码，整理一下”的要求，新增阶段 35。
新增任务书：

```text
docs/taskbooks/2026-06-12-stage-35-framework-tightening-taskbook.md
```

已完成：

```text
新增 pytest.ini，让项目根目录直接运行 pytest 能识别 backend/app。
采集器名称默认使用 Windows 主机名。
旧配置中的空采集器名称、本机采集器、业务机采集器会自动归一为 Windows 主机名。
原始采集 Excel 下载移除采集任务ID、原始文档ID、来源序号等内部列。
原始采集 Excel 下载改为 ID、采集器、电脑名、来源组件、采集时间、状态、采集原文。
解析模式、原文格式、本地来源信息、解析诊断不再放进用户下载的原文主表。
后端测试同步保护新的原始采集 Excel 表头。
```

验证结果：

```text
后端 pytest 通过：7 passed, 1 warning。
采集器 client.py 和 gui.py 编译通过。
tenant-ui Docker 构建通过。
platform-admin-ui Docker 构建通过。
backend Docker 构建通过。
```

当前结论：

```text
平台框架已经可以继续承载下一步业务闭环开发。
当前更应该收敛到抖店最小闭环：采集、解析、商品识别、SKU 图片匹配、用户定义导出表头、生成报货 Excel。
```

## 2026-06-12 追加清理：探索代码清理

本轮根据“之前软删除的一部分探索代码怎么处理 / 清理一下”的要求，新增阶段 36。
新增任务书：

```text
docs/taskbooks/2026-06-12-stage-36-exploration-code-cleanup-taskbook.md
```

已完成：

```text
删除识别样本标注探索页 RecognitionSampleLabelView.vue。
删除识别导入预览探索页 RecognitionImportPreviewView.vue。
删除图片与档口独立管理探索页 AssetsAndStallsView.vue。
移除客户管理路由中的 /admin/assets、/admin/recognition-samples、/admin/recognition-preview。
旧 /admin/image-assets、/admin/stalls、/image-assets、/stalls 直接重定向到 /admin/products。
旧 /admin/field-definitions、/field-definitions 直接重定向到 /admin/export-headers。
删除只服务探索页的 sample-label-layout、sample-raw-panel、sample-segment-section、sample-section-title 样式。
```

保留内容：

```text
历史任务书和进度记录继续保留，不覆盖阶段历史。
商品/SKU、商品识别、导出表头、采集连接继续作为客户管理页正式入口。
```

验证结果：

```text
后端 pytest 通过：7 passed, 1 warning。
tenant-ui Docker 构建通过。
platform-admin-ui Docker 构建通过。
前端源码中已无 RecognitionSampleLabelView、RecognitionImportPreviewView、AssetsAndStallsView 引用。
```

## 2026-06-12 追加收紧：服务端后台资源页收紧

本轮根据“这些是什么 / 进一步收紧”的反馈，新增阶段 37。
新增任务书：

```text
docs/taskbooks/2026-06-12-stage-37-server-admin-resource-tightening-taskbook.md
```

已完成：

```text
ServerAdminResourceView.vue 从通用数据库编辑器改为只读资源清单。
移除右侧 JSON 新建记录入口。
移除 createRecord、Plus 图标、payload JSON 编辑器和新建按钮。
解析模式页只显示 douyin_cloud_print、cainiao_direct_shop、cainiao_woda_printxml。
解析模式页隐藏 Manual upload。
解析模式页隐藏 cainiao_cloud_print 遗留模式。
解析模式页表头改为 解析模式、模式编码、数据来源、说明、状态。
删除不再使用的 resource-layout 和 editor-panel 样式。
```

验证结果：

```text
后端 pytest 通过：7 passed, 1 warning。
tenant-ui Docker 构建通过。
platform-admin-ui Docker 构建通过。
platform-admin-ui 容器已重启。
浏览器验证 /admin/waybill-modes：
  显示 3 条正式解析模式。
  不显示 Manual upload。
  不显示 cainiao_cloud_print 遗留模式。
  不显示 JSON 新建记录入口。
```

## 2026-06-12 追加修正：采集控制页面单数口径

本轮根据“这个页面每次按钮不固定，然后这个回传的数量应该是面单的数量而不是我点击打印的次数”的反馈，新增阶段 30。

新增任务书：

```text
docs/taskbooks/2026-06-12-stage-30-capture-task-waybill-count-taskbook.md
```

问题判断：

```text
客户业务页不能把 raw_capture_records 数量当作面单数量。
raw_capture_records 更适合作为采集诊断信息。
业务主统计应当展示平台整理后可处理的面单数量。
```

已完成：

```text
采集记录页新增加载 standard_details。
本轮面单数量按 capture_task_id 关联整理结果统计。
面单数量按 raw_document_id / logistics_no / order_no 去重。
“本轮回传”改为“本轮面单”。
最近采集任务表头“回传”改为“面单”。
本轮采集摘要“回传 N 条”改为“面单 N 单”。
采集控制按钮增加固定宽度和独立布局，避免状态变化时跳动。
```

当前口径：

```text
业务主数量 = 已整理出的面单数。
原始回传数量只在“原始采集内容”区域作为诊断数据存在。
如果原始采集记录暂时无法整理为面单，面单数显示为 0。
```

验证结果：

```text
后端 pytest 通过：6 passed, 1 warning。
tenant-ui Docker 构建通过。
tenant-ui 容器已重启。
浏览器验证 /capture-records：
  三个控制按钮宽度固定为 112px。
  任务列表显示“面单”列。
  统计卡片显示“本轮面单”。
  页面业务统计区不再显示“回传”旧口径。
```

## 2026-06-12 追加修正：整理文档旧表头定义清理

本轮根据“这个列头在哪里定义了，没有定义过”的反馈，新增阶段 31。

新增任务书：

```text
docs/taskbooks/2026-06-12-stage-31-export-header-cleanup-taskbook.md
```

问题判断：

```text
整理文档下载接口本身是从 field_definitions 读取表头。
当前 Docker 数据库里有历史探索阶段写入的 7 条导出字段。
这些字段不是用户在当前客户管理页明确配置的。
旧识别预览页仍残留“导出表头定义示例”和保存 field_definitions 的能力。
```

已完成：

```text
将当前 workspace 1 的历史导出字段全部软删除并禁用。
涉及字段包括 product_full_text、product_display_text、spec_text、inferred_size、quantity、source_platform、raw_document_id。
移除旧识别预览页保存导出表头定义的逻辑。
整理文档未配置表头时只输出提示，不再输出伪业务列。
提示文案改为“当前工作区还没有定义整理文档表头，暂不生成业务整理文档。”
```

当前口径：

```text
原文文档继续用于诊断采集内容。
整理文档必须等客户明确配置导出表头后再生成。
当前抖店第一版不使用历史示例字段作为默认导出表头。
后续需要单独做正式的报货单表头 / 导出字段定义页面。
```

验证结果：

```text
后端 pytest 通过：6 passed, 1 warning。
backend Docker 构建通过并已重启。
tenant-ui Docker 构建通过并已重启。
下载当前任务整理文档验证：
  A1 = 提示
  A2 = 当前工作区还没有定义整理文档表头，暂不生成业务整理文档。
  max_column = 1。
```

## 2026-06-12 追加进展：抖店字段说明与导出表头定义

本轮根据“把抖店面单读取到的字段 shop-name、item 啥的这些原始字段的含义展示给用户，让用户自行定义表头”的反馈，新增阶段 32。

新增任务书：

```text
docs/taskbooks/2026-06-12-stage-32-douyin-export-header-definition-taskbook.md
```

已完成：

```text
新增后端 POST /api/v1/export-field-definitions/upsert。
该接口可以恢复历史软删除过的同 code 导出字段，避免重新定义表头时撞唯一约束。
客户管理端新增 /admin/export-headers 页面。
客户管理侧边栏和首页新增“导出表头”入口。
页面展示抖店原始字段、系统字段编码、字段含义和当前工作区真实样例。
页面支持客户管理员选择字段，自定义表头名称和导出排序。
页面支持编辑和删除已定义表头。
旧 /admin/field-definition 重定向到 /admin/export-headers。
```

当前口径：

```text
平台负责把抖店原始字段解释清楚。
客户管理员负责决定哪些字段进入整理文档，以及 Excel 表头叫什么。
整理文档不再使用系统默认业务表头。
```

验证结果：

```text
后端 pytest 通过：7 passed, 1 warning。
backend Docker 构建通过并已重启。
tenant-ui Docker 构建通过并已重启。
浏览器验证 /admin/export-headers：
  显示“导出表头”。
  显示“抖店字段说明 / 自定义表头 / 已定义表头”。
  包含 shopName、productInfo、productShortInfo 字段说明。
  包含“保存表头”按钮。
```

## 2026-06-12 追加修复：抖店多 document 解析

本轮根据“我打印两条订单，采集结果只有一个”的反馈，新增阶段 33。

新增任务书：

```text
docs/taskbooks/2026-06-12-stage-33-douyin-multi-document-parse-taskbook.md
```

问题判断：

```text
采集器已上传原始记录。
抖店打印组件这次只新增一条 task row，但该 row 的 JSON 中 task.documents = 2。
旧解析器只从整份 JSON 里取一份最佳 data，导致一条 raw 只生成一条面单。
正确口径是：raw_capture_record 是打印组件任务记录，不等于面单数。
抖店面单数应按 task.documents[] 拆分。
```

已完成：

```text
抖店解析器改为遍历 task.documents[]。
每个 document 独立读取 data 并生成 StandardDetail。
field_values 增加 document_sequence。
保留旧兜底逻辑，兼容没有标准 documents 结构的抖店 payload。
后端测试新增一条抖店 raw 内含两张面单的覆盖。
对当前任务 10 执行 force reparse。
```

验证结果：

```text
后端 pytest 通过：7 passed, 1 warning。
backend Docker 构建通过并已重启。
任务 10 强制重解析后生成两条面单：
  YT0043623738399，document_sequence = 1。
  YT0043296031991，document_sequence = 2。
浏览器验证 /capture-records 中任务 10 的“面单”列显示 2。
```

## 2026-06-12 追加修正：按面单模式和字段绑定商品识别

本轮根据“抖店也有卖家和买家备注字段，按三种模式利用平台解析字段做商品识别”的方向，新增阶段 34。

新增任务书：

```text
docs/taskbooks/2026-06-12-stage-34-field-bound-product-recognition-taskbook.md
```

问题判断：

```text
商品识别规则不能继续默认匹配所有字段。
抖店和菜鸟店铺直打属于平台已解析字段，客户只需要选择哪些字段参与识别。
菜鸟 woda / 我打中转只能读取自定义打印文字，字段含义应留给用户后续模板定义。
```

已完成：

```text
新增 frontend/src/views/workbench/waybillFieldCatalog.ts 作为三种面单模式的字段目录。
商品识别页新增面单模式选择。
商品识别页新增参与识别字段选择。
抖店默认字段包含商品信息、商品简称、规格文本、买家备注、卖家备注。
菜鸟店铺直打默认字段包含商品信息、买家备注、卖家备注。
菜鸟 woda 默认字段为自定义打印文字。
保存商品识别规则时，将 mode_code 和 fields 写入 match_values。
规则列表展示模式和识别字段。
识别预览按规则指定字段匹配关键词，不再默认匹配所有文本。
SKU 自动匹配使用当前面单模式默认识别字段。
```

当前口径：

```text
平台负责解析面单字段。
客户管理员负责选择哪些字段用于商品识别。
规则必须绑定字段，避免“4.0 标题里包含 5.0”时因为全局文本匹配造成误识别。
```

验证结果：

```text
后端 pytest 通过：7 passed, 1 warning。
tenant-ui Docker 构建通过。
tenant-ui 容器已重启。
浏览器验证 /admin/matching：
  页面显示“商品识别”。
  页面显示“面单模式”。
  页面显示“参与识别字段”。
  抖店模式显示买家备注和卖家备注。
```

## 2026-06-11 追加修正：客户管理端删除操作补齐

本轮根据“这些页面都没有删除按钮”的反馈，新增阶段 28。

新增任务书：

```text
docs/taskbooks/2026-06-11-stage-28-client-admin-delete-actions-taskbook.md
```

已完成：

```text
新增前端 deleteRecord 通用 API。
商品识别规则列表增加删除按钮。
商品列表增加删除按钮。
SKU 列表增加删除按钮。
采集连接列表增加移除按钮。
所有删除/移除操作增加确认弹窗。
删除成功后自动刷新当前列表。
```

当前口径：

```text
删除走后端软删除，不做前端假删除。
商品识别规则删除后不再参与后续匹配。
商品和 SKU 删除后从当前工作区列表移除。
采集器移除后，业务机重新登录可以再次连接。
```

验证结果：

```text
后端 pytest 通过：5 passed, 1 warning。
tenant-ui Docker 构建通过。
tenant-ui 容器已重启。
浏览器验证商品识别页出现删除按钮。
浏览器验证商品/SKU 页出现删除按钮。
浏览器验证采集连接页出现移除按钮。
```

## 2026-06-11 追加进展：商品识别页读取采集 Excel

本轮根据“这里加一个读取采集到的 Excel，这样可以直接选择面单匹配商品”的反馈，新增阶段 29。

新增任务书：

```text
docs/taskbooks/2026-06-11-stage-29-matching-excel-preview-taskbook.md
```

已完成：

```text
新增 POST /api/v1/matching/excel-preview。
后端使用 openpyxl 读取 .xlsx 第一张表。
自动识别商品标题 / 商品信息 / 商品名称 / 商品简称 / 商品显示文字等列。
支持读取规格列和数量列。
重复的商品标题 + 规格会合并并统计出现次数。
商品识别页新增“读取采集 Excel”上传区域。
上传后展示 Excel 候选商品标题。
点击候选行“使用”可回填商品识别关键词。
```

当前口径：

```text
Excel 读取只是辅助录入商品识别关键词。
用户仍需选择关联商品并保存规则。
系统不根据 Excel 自动批量生成规则。
第一版只支持 .xlsx。
```

验证结果：

```text
后端 pytest 通过：6 passed, 1 warning。
backend Docker 构建通过。
tenant-ui Docker 构建通过。
backend 和 tenant-ui 容器已重启。
浏览器验证商品识别页出现“读取采集 Excel”上传区域。
```

## 2026-06-11 追加修正：抖店第一版客户端收口

本轮根据“先做好抖店，其他后面再说，客户端把后面加的东西先取消”的反馈，新增阶段 27。

新增任务书：

```text
docs/taskbooks/2026-06-11-stage-27-douyin-client-scope-trim-taskbook.md
```

已完成：

```text
客户管理侧边栏移除识别样本、识别预览、图片与档口入口。
客户管理首页移除识别样本、识别预览、图片与档口卡片。
旧地址 /admin/recognition-samples 重定向到 /admin/matching。
旧地址 /admin/recognition-preview 重定向到 /admin/matching。
旧地址 /admin/assets 重定向到 /admin/products。
商品识别页面文案改为抖店商品标题关键词口径。
```

当前口径：

```text
抖店字段类型由平台端固定解析。
客户端不定义抖店字段类型。
客户端只维护采集连接、商品/SKU 和“抖店商品标题关键词 -> 我的商品”。
菜鸟、我打、自定义字段标注等探索入口暂不暴露给客户。
```

验证结果：

```text
后端 pytest 通过：5 passed, 1 warning。
tenant-ui Docker 构建通过。
tenant-ui 容器已重启。
```

## 2026-06-11 追加修正：商品识别冲突保护

本轮根据“4.0 商品标题里也有 5.0，系统会识别成 4.0 还是 5.0”的反馈，新增阶段 26。

新增任务书：

```text
docs/taskbooks/2026-06-11-stage-26-product-match-conflict-guard-taskbook.md
```

问题判断：

```text
如果同一条面单同时命中 4.0 和 5.0 两个商品，系统不能自动选一个。
旧逻辑会按关键词长度和规则顺序选中一个商品，存在错误出单风险。
```

已完成：

```text
识别预览新增商品冲突检测。
商品识别规则和识别样本会先汇总所有命中候选。
同一商品命中多个关键词时，只保留该商品下最长关键词作为候选说明。
多个不同商品同时命中时，标记为“商品冲突”。
商品冲突行不继续匹配 SKU。
商品冲突行不显示为“可生成”。
结果筛选增加“商品冲突”。
商品识别列展示冲突候选商品、关键词和来源。
```

当前口径：

```text
商品冲突必须暴露给客户管理员处理。
后续需要继续补规则能力：必须词、排除词、组合规则、人工确认回写样本。
```

验证结果：

```text
后端 pytest 通过：5 passed, 1 warning。
tenant-ui Docker 构建通过。
tenant-ui 容器已重启。
```
