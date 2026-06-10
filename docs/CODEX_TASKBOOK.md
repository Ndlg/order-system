# 订单整理系统 8.0 Codex 项目任务书

## 0. 执行定位

从空仓库开始搭建一个完整项目，不保留旧系统源码，不复刻旧系统硬编码逻辑。

项目名称：订单整理系统

系统定位：面单采集数据标准化与档口报货 Excel 生成系统。

最终目标：

```text
把面单采集工具返回的原始采集数据，经过标准化处理和用户自定义映射，生成可直接发给档口的报货 Excel。
```

本项目不是单店铺定制工具，而是可配置平台。所有店铺差异、面单差异、鞋款差异、规格差异、图片差异、档口差异、导出格式差异，都必须通过配置实现。

---

## 1. 技术栈要求

必须使用以下技术栈：

```text
前端：Vue 3 + TypeScript + Element Plus
后端：Python FastAPI
数据库：MySQL
缓存：Redis
Excel 处理：openpyxl
图片处理：Pillow
部署目标：Windows 内网服务器优先
```

不要再生成 Java Spring Boot 或 Node.js NestJS 版本。第一版统一使用 FastAPI。

---

## 2. 总体架构

项目必须按前后端分离 + 采集端预留的结构搭建：

```text
order-system/
  backend/                    # FastAPI 后端
  frontend/                   # Vue 3 管理后台
  collector-client/           # 面单采集工具客户端，第一版先搭框架与接口契约
  docs/                       # 项目文档
  scripts/                    # Windows 启动、初始化、构建脚本
  storage/
    raw/                      # 原始采集文件 / 原始采集包
    standard/                 # 标准化 Excel 文件
    exports/                  # 报货导出 Excel 文件
    uploads/
      product-images/         # 商品图片
      mapping-imports/        # 批量导入映射文件
```

后端必须分层：

```text
api/          # 路由层，只做参数接收和响应
schemas/      # Pydantic 入参出参模型
models/       # SQLAlchemy ORM 模型
services/     # 应用服务
repositories/ # 数据访问
engines/      # 解析、映射、汇总、导出等引擎
core/         # 配置、鉴权、异常、日志
```

前端必须分模块：

```text
src/views/login
src/views/dashboard
src/views/shops
src/views/collectors
src/views/capture-batches
src/views/waybill-templates
src/views/standard-details
src/views/field-roles
src/views/product-aliases
src/views/spec-mappings
src/views/stalls
src/views/product-images
src/views/report-batches
src/views/exceptions
src/views/export-records
src/views/users
```

---

## 3. 核心业务链路

系统必须按三段式设计。

### 3.1 采集阶段

```text
采集工具连接服务端
  ↓
服务端创建采集任务
  ↓
采集工具开始采集
  ↓
采集内容实时回传服务端
  ↓
服务端保存原始采集记录
  ↓
Web 端可查看、下载原始采集数据
```

第一版采集工具细节可以先做接口契约和最小客户端框架，不要求完成真实平台采集逻辑。

### 3.2 标准化阶段

```text
原始采集记录
  ↓
面单模板识别
  ↓
字段提取规则解析
  ↓
生成标准化明细
  ↓
可导出标准化 Excel
```

注意：原始采集内容不一定是 JSON。统一使用 `raw_payload`，不要使用 `raw_json` 作为核心字段名。

### 3.3 报货阶段

```text
标准化明细
  ↓
字段角色配置
  ↓
鞋款简称映射
  ↓
规格映射
  ↓
图片绑定
  ↓
档口归属
  ↓
生成报货汇总
  ↓
三种方式导出 Excel
```

系统最终处理的是标准化明细，不直接依赖原始采集格式。

---

## 4. 标准化明细字段

第一版标准化明细字段先固定为以下字段：

```text
面单模式
完整原文
店铺名
商品简称
规格
尺码
数量
备注
图片识别
任务ID
文档ID
任务时间
采集端ID
来源机器
来源序号
原始内容
```

这些字段作为第一版固定字段。后续可以扩展为动态字段，但当前版本先围绕这套字段做完整闭环。

字段说明：

- `面单模式`：采集工具或模板识别出的面单模式。
- `完整原文`：从面单或打印信息中提取出的完整商品/订单原文。
- `店铺名`：可能是淘宝店铺名、抖店店铺名或其他来源；如果暂时无法解析，允许为空或由批次默认店铺补充。
- `商品简称`：从原文或模板中提取出的鞋款简称。
- `规格`：原始规格或颜色规格。
- `尺码`：商品尺码。
- `数量`：商品数量，默认允许为 1。
- `备注`：解析备注或人工备注。
- `图片识别`：已识别 / 未识别。
- `任务ID、文档ID、任务时间、采集端ID、来源机器、来源序号`：采集链路追踪信息。
- `原始内容`：原始采集内容，不限定 JSON。

---

## 5. 原始采集数据设计

禁止假设原始采集数据一定是 JSON，也禁止假设一定存在 `raw_json` 字段。

统一概念：

```text
RawCaptureRecord：原始采集记录
raw_payload：原始采集内容
payload_format：原始内容格式
source_columns：原始列快照
parsed_payload：解析后的结构化内容，可为空
```

`payload_format` 支持：

```text
json
xml
text
excel_row
mixed
unknown
```

建议表：`raw_capture_records`

字段建议：

```text
id
capture_batch_id
task_id
document_id
collector_id
source_machine
source_index
waybill_mode
payload_format
raw_payload              # LONGTEXT，不强制 JSON
source_columns           # JSON，保存原始列快照
parsed_payload           # JSON，可为空
standard_detail_id
status
created_at
updated_at
```

Web 页面按钮名称必须使用：

```text
查看原始采集内容
下载原始采集数据
下载原始采集包
```

不要写成“下载 raw_json”或“下载原始 JSON”。

---

## 6. 主要模块要求

### 6.1 用户与权限

角色：

```text
管理员
运营人员
仓库人员
只读人员
```

权限：

- 管理员：所有权限。
- 运营人员：采集、导入、标准化、映射维护、异常处理、报货导出。
- 仓库人员：查看报货结果、下载报货 Excel。
- 只读人员：只查看，不修改。

第一版实现基础 JWT 登录、用户管理、角色管理即可。

### 6.2 店铺管理

支持多个店铺。

字段：

```text
店铺名称
店铺类型：淘宝 / 抖店 / 1688 / 其他
备注
是否启用
```

店铺名来源不固定，用户可以通过字段角色配置指定标准化明细中哪一列代表店铺，也可以在导入批次时设置默认店铺。

### 6.3 采集端管理

支持采集端注册、绑定、心跳、状态查看。

字段：

```text
采集端ID
采集端名称
来源机器
客户端版本
在线状态
最后心跳时间
备注
```

### 6.4 采集任务管理

支持创建采集任务、查看任务状态、查看实时日志、查看回传记录。

状态：

```text
待开始
采集中
已完成
失败
已取消
```

### 6.5 原始采集记录管理

功能：

```text
列表查询
查看原始内容
按批次下载原始采集数据
按单条下载原始内容
查看解析状态
```

### 6.6 面单模板管理

面单模板不只支持 JSON Path，必须支持通用字段提取规则。

模板字段：

```text
模板名称
面单模式
输入格式
识别条件
字段提取规则
是否启用
版本号
```

字段提取方式预留：

```text
json_path
excel_column
xml_path
regex
text_contains
fixed_value
```

第一版至少实现：

```text
excel_column
json_path
regex
fixed_value
```

### 6.7 标准化明细管理

支持：

```text
从原始采集记录生成标准化明细
直接上传标准化 Excel
标准化明细预览
标准化明细筛选
导出标准化 Excel
```

第一版必须支持直接上传标准化 Excel，这是优先闭环。

### 6.8 字段角色配置

用户必须能配置标准化明细中哪一列承担业务角色。

角色包括：

```text
店铺字段
鞋款简称字段
规格字段
尺码字段
数量字段
备注字段
完整原文字段
```

示例：

```text
店铺字段 = 店铺名
鞋款简称字段 = 商品简称
规格字段 = 规格
尺码字段 = 尺码
数量字段 = 数量
备注字段 = 备注
```

### 6.9 鞋款简称映射

由用户维护，不允许写死。

功能：

```text
来源简称
标准鞋款
所属店铺
是否启用
批量导入
批量导出
未映射值自动收集
```

示例：

```text
4.0      -> 4.0
5.0      -> 5.0
ac       -> ACG
vap2025  -> VAP
```

这些只是示例数据，不得写死到业务逻辑。

### 6.10 规格映射

由用户维护，不允许写死。

功能：

```text
原始规格
标准规格
标准鞋款
所属店铺
绑定档口
绑定图片
是否启用
批量导入
批量导出
未映射值自动收集
```

### 6.11 档口管理

功能：

```text
档口名称
联系人
备注
是否启用
绑定鞋款 / 规格
```

### 6.12 商品图片管理

商品图片必须重新上传，不依赖旧系统路径。

支持：

```text
单张上传
批量上传
批量导入图片关系
按标准鞋款 + 标准规格绑定图片
图片预览
图片缺失提示
```

### 6.13 报货汇总

默认汇总规则：

```text
按 标准鞋款 + 标准规格 + 商品图片 + 档口 分组
尺码合并展示
数量汇总
备注保留
```

默认报货字段：

```text
鞋款分类
规格
图片
尺码
数量
备注
```

尺码排序必须支持数字排序，包括 36.5、37.5、40.5、42.5。

### 6.14 异常处理

异常类型：

```text
面单模板无法识别
原始内容解析失败
标准字段缺失
店铺无法识别
鞋款简称未映射
规格未映射
尺码无法识别
数量异常
图片未绑定
档口未绑定
导出模板缺失
```

异常支持人工修正后重新生成报货结果。

### 6.15 Excel 导出

必须支持三种输出方式：

1. 合并 Sheet
   - 所有报货数据输出到一个 Sheet。

2. 鞋款档口 Sheet
   - 一个 Excel 文件，按鞋款 / 档口拆成多个 Sheet。

3. 鞋款档口文档
   - 按鞋款 / 档口拆成多个 Excel 文件，打包 ZIP 下载。

Excel 默认列：

```text
鞋款分类 | 规格 | 图片 | 尺码 | 数量 | 备注
```

必须支持图片嵌入 Excel，图片自适应单元格，设置列宽、行高、边框、表头样式。

---

## 7. 数据库核心表建议

第一版至少包含：

```text
users
roles
user_roles
shops
collectors
capture_tasks
capture_batches
raw_capture_records
waybill_templates
waybill_template_fields
standard_detail_batches
standard_details
field_role_configs
product_alias_mappings
spec_mappings
stalls
product_images
report_batches
report_lines
exception_records
export_records
operation_logs
```

所有业务表建议保留：

```text
id
created_at
updated_at
created_by
updated_by
is_deleted
```

涉及店铺的数据必须保留：

```text
shop_id
```

---

## 8. 后端接口最低要求

至少实现以下接口组：

```text
/auth/login
/auth/me
/users
/roles
/shops
/collectors
/capture-tasks
/capture-batches
/raw-capture-records
/waybill-templates
/standard-detail-batches
/standard-details
/field-role-configs
/product-alias-mappings
/spec-mappings
/stalls
/product-images
/report-batches
/exceptions
/export-records
```

必须提供 OpenAPI 文档。

---

## 9. 前端页面最低要求

至少搭建以下页面：

```text
登录页
首页仪表盘
店铺管理
采集端管理
采集任务管理
原始采集数据
面单模板管理
标准化明细
字段角色配置
鞋款简称映射
规格映射
档口管理
商品图片管理
报货批次
异常处理
导出记录
用户管理
```

第一版页面可以先实现业务闭环，不追求复杂 UI。

---

## 10. 第一版开发优先级

### P0：先跑通标准化 Excel 到报货 Excel

必须优先完成：

```text
用户登录
店铺管理
上传标准化 Excel
读取固定标准字段
字段角色配置
鞋款简称映射
规格映射
商品图片上传
档口管理
报货汇总生成
异常提示
三种模式导出 Excel
```

P0 验收目标：

```text
上传一份标准化 Excel 后，系统可以根据用户维护的映射关系，生成类似“鞋款分类 | 规格 | 图片 | 尺码 | 数量 | 备注”的档口报货 Excel。
```

### P1：接入原始采集记录与面单模板解析

完成：

```text
上传原始采集文件
保存 raw_payload
配置面单模板
解析生成标准化明细
下载原始采集数据
导出标准化 Excel
```

### P2：采集工具实时连接服务端

完成：

```text
采集端注册
心跳
任务下发
状态上报
日志上报
原始采集内容回传
断线重连
```

---

## 11. Windows 部署要求

必须提供：

```text
.env.example
scripts/init_db.sql
scripts/start_backend.bat
scripts/start_frontend_dev.bat
scripts/build_frontend.bat
scripts/start_all.bat
```

README 必须说明：

```text
Python 环境安装
Node.js 环境安装
MySQL 初始化
Redis 启动
后端启动
前端启动
默认管理员账号
文件目录说明
```

BAT 文件内容必须使用 ASCII，避免中文 echo 导致 Windows 编码问题。

---

## 12. 禁止事项

必须严格遵守：

```text
禁止保留旧系统源码。
禁止把具体店铺名称写死在代码中。
禁止把具体鞋款名称写死在代码中。
禁止把具体规格名称写死在代码中。
禁止把具体面单字段写死在业务逻辑中。
禁止假设原始采集内容一定是 JSON。
禁止使用 raw_json 作为核心原始数据字段名。
禁止把 Excel 导出列写死为唯一模板。
禁止把业务规则写在 Controller 或前端页面里。
禁止为了演示功能写固定 if/else 业务规则。
禁止导入后覆盖原始采集内容。
禁止绕过映射配置直接生成报货结果。
```

允许存在默认示例数据，但示例数据必须通过初始化配置写入数据库，不能写在业务代码里。

---

## 13. 验收标准

第一阶段验收必须满足：

```text
1. 项目目录结构完整，前后端可分别启动。
2. 后端 OpenAPI 可访问。
3. 前端登录后可进入管理后台。
4. 可创建店铺、档口、鞋款简称映射、规格映射。
5. 可上传商品图片并绑定到标准鞋款 + 标准规格。
6. 可上传标准化 Excel。
7. 可生成标准化明细批次。
8. 可自动识别未映射鞋款简称、未映射规格、图片缺失、档口缺失异常。
9. 修正异常后可重新生成报货结果。
10. 可导出三种 Excel：合并 Sheet、鞋款档口 Sheet、鞋款档口文档。
11. 导出的 Excel 必须包含图片列，图片嵌入单元格。
12. 操作日志、导出记录、异常记录可查询。
13. Windows 启动脚本可用。
```

---

## 14. Codex 执行顺序

请按以下顺序执行，不要跳跃式开发：

```text
1. 初始化项目目录结构。
2. 初始化后端 FastAPI 工程。
3. 初始化前端 Vue 3 工程。
4. 编写数据库模型与迁移脚本。
5. 实现登录、用户、角色、店铺基础模块。
6. 实现标准化 Excel 上传与解析。
7. 实现字段角色配置。
8. 实现鞋款简称映射、规格映射、档口管理、图片管理。
9. 实现报货汇总引擎。
10. 实现异常处理。
11. 实现 Excel 三模式导出。
12. 实现原始采集记录和面单模板框架。
13. 实现采集端接口契约和最小客户端框架。
14. 补齐前端页面。
15. 补齐 Windows 脚本和 README。
16. 编写基础测试与示例数据。
```

每完成一个阶段，提交清晰 commit，不要一次性混合大量无关改动。
