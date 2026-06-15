# 下一阶段任务书

> 历史命名文件，后续不要覆盖成新阶段内容。正式阶段留档见 `docs/TASKBOOK_INDEX.md` 和 `docs/taskbooks/`。

> 适用阶段：数据库持久化与平台基础能力阶段  
> 上游依据：`docs/CODEX_TASKBOOK.md`  
> 当前前置状态：`43085a9 feat: add database foundation and auth context`

## 0. 阶段目标

下一阶段目标是把当前“可启动骨架”推进到“可持久化、可鉴权、可按 workspace 隔离访问”的平台基础版本。

当前已搭建的前端属于管理 / 开发者验证入口，用来验证接口、模型、鉴权和 workspace 隔离。它不是最终面向普通业务用户的工作台。

本阶段不追求完整报货 Excel 闭环，优先解决后续所有业务模块都会依赖的基础能力：

```text
MySQL ORM 模型
数据库连接
Repository 层 workspace_id 强过滤
JWT 登录
用户 / 角色 / 工作空间关系
面单模式管理
面单字段定义
关键字段组合
匹配规则
图片信息与档口基础管理
操作日志基础记录
```

## 1. 阶段原则

必须继续遵守以下原则：

```text
1. 不预设任何业务字段。
2. 不把用户业务对象做成系统一级固定对象。
3. 所有可变配置必须挂在 workspace_id 下。
4. 所有 Repository 查询必须强制 workspace_id 过滤。
5. 禁止使用 shop_id 作为核心隔离字段。
6. 禁止创建 shops 表作为业务主表。
7. 禁止把具体面单字段、图片匹配、档口匹配关系写死在业务代码中。
```

## 2. 交付范围

### 2.1 后端持久化

完成：

```text
数据库连接配置
SQLAlchemy Base
Session 管理
ORM 模型
Repository 基类
workspace_id 查询过滤
分页查询基础结构
软删除基础结构
created_at / updated_at / created_by / updated_by 字段维护
```

第一批 ORM 模型至少包含：

```text
User
Role
UserWorkspace
Workspace
WaybillMode
WaybillTemplate
StandardDetailBatch
StandardDetail
FieldDefinition
FieldRoleConfig
KeyFieldSet
MatchRule
Stall
ImageAsset
ReportBatch
ExceptionRecord
ExportRecord
OperationLog
Collector
CaptureTask
CaptureBatch
RawCaptureRecord
```

### 2.2 鉴权与工作空间上下文

完成：

```text
JWT 登录
密码哈希
当前用户解析
当前 workspace 选择
用户可访问 workspace 校验
系统管理员 / 管理员 / 运营人员 / 仓库人员 / 只读人员角色枚举
只读角色禁止写操作
```

接口要求：

```text
POST /auth/login
GET /auth/me
GET /workspaces
POST /workspaces
```

### 2.3 通用资源接口收敛

当前通用资源接口只适合骨架阶段。下一阶段要逐步收敛成明确服务：

```text
workspaces
waybill-modes
field-definitions
key-field-sets
match-rules
stalls
image-assets
```

每个资源至少支持：

```text
列表
详情
创建
更新
软删除
启用 / 停用
```

### 2.4 前端基础能力

完成：

```text
登录状态保存
退出登录
工作空间选择
API token 自动附带
请求失败提示
基础表格分页
创建 / 编辑弹窗
只读角色页面禁用写操作
```

本阶段前端定位：

```text
1. 保留管理 / 开发者后台，继续用于资源管理和接口验证。
2. 明确该后台不是最终用户工作台。
3. 开始预留用户工作台路由与页面结构，但不要求本阶段完成完整业务闭环。
4. 后续 P0 闭环必须通过用户工作台承载，而不是通用资源 CRUD 页面。
```

优先细化页面：

```text
工作空间管理
面单模式管理
面单字段定义
关键字段配置
匹配规则配置
图片信息管理
档口管理
```

### 2.5 文件与图片基础存储

完成：

```text
storage/workspaces/{workspace_id}/uploads/images/
图片上传接口
图片元数据入库
hash 计算
按 workspace_id 分目录保存
禁止图片 BLOB 入库
```

## 3. 不在本阶段做的内容

以下内容暂不作为本阶段验收条件：

```text
完整标准化 Excel 导入解析
原始采集模板解析全能力
报货汇总完整引擎
Excel 三模式导出完整样式
Excel 图片嵌入
采集端实时连接
复杂权限矩阵
配置包导入导出
```

这些内容进入后续 P0 闭环阶段。

## 4. 执行顺序

请按以下顺序推进：

```text
1. 建立 SQLAlchemy 数据库连接和 Session。
2. 建立 ORM 模型和公共 mixin。
3. 建立 Repository 基类并强制 workspace_id 过滤。
4. 替换内存数据服务中的核心资源为数据库访问。
5. 实现用户、角色、工作空间基础数据。
6. 实现 JWT 登录和当前用户上下文。
7. 实现工作空间选择与访问校验。
8. 实现面单模式管理接口。
9. 实现面单字段定义接口。
10. 实现关键字段组合接口。
11. 实现匹配规则接口。
12. 实现档口和图片信息基础接口。
13. 前端接入登录、token、workspace。
14. 前端细化字段、关键字段、匹配规则、图片、档口页面。
15. 预留用户工作台入口和面单批次处理流程页面骨架。
16. 增加基础测试和启动验证。
17. 更新 README 和进度报告。
18. 提交并推送阶段 commit。
```

当前执行进度：

```text
1. 建立 SQLAlchemy 数据库连接和 Session：已完成
2. 建立 ORM 模型和公共 mixin：已完成
3. 建立 Repository 基类并强制 workspace_id 过滤：已完成
4. 替换内存数据服务中的核心资源为数据库访问：部分完成
5. 实现用户、角色、工作空间基础数据：部分完成
6. 实现 JWT 登录和当前用户上下文：已完成
7. 实现工作空间选择与访问校验：部分完成
8-14. 资源服务与前端细化：待推进
15. 用户工作台入口和流程页面骨架：待推进
16. 增加基础测试和启动验证：部分完成
```

## 5. 验收标准

本阶段完成时必须满足：

```text
1. 后端可连接 MySQL。
2. 后端 OpenAPI 可访问。
3. 用户可登录并获取 JWT。
4. /auth/me 可返回当前用户和可访问 workspace。
5. 用户只能访问自己所属 workspace 的数据。
6. Repository 层存在强制 workspace_id 过滤。
7. 可创建、编辑、停用面单模式。
8. 可创建、编辑、停用面单字段定义。
9. 可配置关键字段组合。
10. 可配置图片 / 档口匹配规则。
11. 可创建档口和图片信息。
12. 图片文件按 workspace_id 分目录保存。
13. 前端可登录、选择 workspace，并操作上述基础模块。
14. 前端明确区分管理 / 开发者后台与用户工作台入口。
15. 不存在 shop_id 核心隔离逻辑。
16. 不存在预设业务字段写死逻辑。
17. 后端基础测试通过。
```

## 6. 建议提交拆分

建议按以下 commit 拆分，避免一次混入过多内容：

```text
1. feat: add database models and session
2. feat: enforce workspace scoped repositories
3. feat: add jwt auth and workspace context
4. feat: persist field and match configuration APIs
5. feat: add image and stall management APIs
6. feat: wire frontend auth and workspace selection
7. feat: separate admin console and user workbench shell
8. feat: refine configuration management views
9. test: add backend foundation tests
```

## 7. 阶段完成后的下一步

本阶段完成后，进入 P0 业务闭环阶段：

```text
标准化 Excel 上传
读取 Excel 表头并生成字段定义
生成标准化明细批次
关键字段匹配图片和档口
异常提示
报货汇总生成
三种 Excel 导出
```
