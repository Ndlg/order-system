# 订单整理系统 8.0 Codex 项目任务书

## 0. 执行定位

从空仓库开始搭建一个完整项目，不保留旧系统源码，不复刻旧系统硬编码逻辑。

项目名称：订单整理系统

系统定位：面单采集数据标准化与档口报货 Excel 生成系统。

最终目标：

```text
把面单采集工具返回的原始采集数据，经过面单模式解析和标准化处理，再通过用户自定义映射，生成可直接发给档口的报货 Excel。
```

本项目不是单店铺定制工具，也不是店铺管理系统。系统核心只认识：

```text
用户空间 / 工作空间
面单模式
面单模板
标准化明细
字段角色
鞋款简称映射
规格映射
图片绑定
档口归属
报货汇总
Excel 导出
```

店铺名、淘宝店铺名、抖店店铺名等，只能作为标准化明细中的普通字段存在，不能作为系统一级业务对象，也不能用店铺作为系统核心隔离边界。

所有面单差异、鞋款差异、规格差异、图片差异、档口差异、导出格式差异，都必须通过配置实现。

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

第一版统一使用 FastAPI，不要生成 Java Spring Boot 或 Node.js NestJS 版本。

---

## 2. 多用户与数据隔离原则

服务器端启动后会面向多个用户使用，但系统不按“店铺”隔离数据。第一版采用：

```text
一个 MySQL 数据库
多个用户空间 / 工作空间 workspace
每个 workspace 下维护自己的面单模式、模板、标准化明细、映射、图片、档口、报货批次、导出记录
```

核心原则：

```text
1. workspace 是最高数据隔离边界。
2. 一个用户可以属于一个或多个 workspace。
3. 一个 workspace 可以有多个用户。
4. 所有业务表必须带 workspace_id。
5. 后端查询必须强制按当前用户可访问的 workspace_id 过滤。
6. 文件存储必须按 workspace_id 分目录。
7. Redis key 必须带 workspace_id 前缀。
8. 禁止用户跨 workspace 查询、下载、导出、修改数据。
9. 店铺名只作为标准化明细字段，不作为系统数据隔离边界。
```

推荐文件目录隔离：

```text
storage/
  workspaces/
    workspace_1/
      raw/
      standard/
      exports/
      uploads/
        product-images/
        mapping-imports/
    workspace_2/
      raw/
      standard/
      exports/
      uploads/
        product-images/
        mapping-imports/
```

推荐 Redis key：

```text
workspace:{workspace_id}:task:{task_id}
workspace:{workspace_id}:collector:{collector_id}
workspace:{workspace_id}:export:{export_id}
```

---

## 3. 总体架构

项目必须按前后端分离 + 采集端预留的结构搭建：

```text
order-system/
  backend/                    # FastAPI 后端
  frontend/                   # Vue 3 管理后台
  collector-client/           # 面单采集工具客户端，第一版先搭框架与接口契约
  docs/                       # 项目文档
  scripts/                    # Windows 启动、初始化、构建脚本
  storage/
    workspaces/               # 按 workspace_id 隔离文件
```

后端必须分层：

```text
api/          # 路由层，只做参数接收和响应
schemas/      # Pydantic 入参出参模型
models/       # SQLAlchemy ORM 模型
services/     # 应用服务
repositories/ # 数据访问，必须强制 workspace_id 过滤
engines/      # 解析、映射、汇总、导出等引擎
core/         # 配置、鉴权、异常、日志
```

前端必须分模块：

```text
src/views/login
src/views/dashboard
src/views/workspaces
src/views/collectors
src/views/capture-batches
src/views/waybill-modes
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

## 4. 核心业务链路

系统必须按三段式设计。

### 4.1 采集阶段

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

### 4.2 标准化阶段

```text
原始采集记录
  ↓
面单模式识别
  ↓
面单模板匹配
  ↓
字段提取规则解析
  ↓
生成标准化明细
  ↓
可导出标准化 Excel
```

注意：原始采集内容不一定是 JSON。统一使用 `raw_payload`，不要使用 `raw_json` 作为核心字段名。

### 4.3 报货阶段

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

## 5. 标准化明细字段

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

字段说明：

- `面单模式`：采集工具或模板识别出的面单模式，是系统核心字段。
- `完整原文`：从面单或打印信息中提取出的完整商品/订单原文。
- `店铺名`：普通展示字段，可能是淘宝店铺名、抖店店铺名或其他来源；系统不以店铺名作为核心对象。
- `商品简称`：从原文或模板中提取出的鞋款简称。
- `规格`：原始规格或颜色规格。
- `尺码`：商品尺码。
- `数量`：商品数量，默认允许为 1。
- `备注`：解析备注或人工备注。
- `图片识别`：已识别 / 未识别。
- `任务ID、文档ID、任务时间、采集端ID、来源机器、来源序号`：采集链路追踪信息。
- `原始内容`：原始采集内容，不限定 JSON。

这些字段作为第一版固定字段。后续可以扩展为动态字段，但当前版本先围绕这套字段做完整闭环。

---

## 6. 原始采集数据设计

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
workspace_id
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

## 7. 主要模块要求

### 7.1 用户、角色与工作空间

角色：

```text
系统管理员
管理员
运营人员
仓库人员
只读人员
```

权限：

- 系统管理员：可管理所有 workspace。
- 管理员：管理所属 workspace 的用户、面单模式、模板、映射、图片、档口和数据。
- 运营人员：采集、导入、标准化、映射维护、异常处理、报货导出。
- 仓库人员：查看报货结果、下载报货 Excel。
- 只读人员：只查看，不修改。

第一版实现基础 JWT 登录、用户管理、角色管理、workspace 选择即可。

### 7.2 面单模式管理

系统核心对象是面单模式，不是店铺。

功能：

```text
新增面单模式
编辑面单模式
启用 / 停用面单模式
配置默认模板
查看该面单模式下的标准化明细、映射和报货批次
```

字段建议：

```text
workspace_id
面单模式名称
面单模式编码
输入格式
备注
是否启用
```

### 7.3 采集端管理

支持采集端注册、绑定、心跳、状态查看。

字段：

```text
workspace_id
采集端ID
采集端名称
来源机器
客户端版本
在线状态
最后心跳时间
备注
```

### 7.4 采集任务管理

支持创建采集任务、查看任务状态、查看实时日志、查看回传记录。

状态：

```text
待开始
采集中
已完成
失败
已取消
```

### 7.5 原始采集记录管理

功能：

```text
列表查询
查看原始内容
按批次下载原始采集数据
按单条下载原始内容
查看解析状态
```

### 7.6 面单模板管理

面单模板不只支持 JSON Path，必须支持通用字段提取规则。

模板字段：

```text
workspace_id
面单模式ID
模板名称
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

### 7.7 标准化明细管理

支持：

```text
从原始采集记录生成标准化明细
直接上传标准化 Excel
标准化明细预览
标准化明细筛选
导出标准化 Excel
```

第一版必须支持直接上传标准化 Excel，这是优先闭环。

### 7.8 字段角色配置

用户必须能配置标准化明细中哪一列承担业务角色。

角色包括：

```text
面单模式字段
来源店铺字段，可选，仅作为普通字段
鞋款简称字段
规格字段
尺码字段
数量字段
备注字段
完整原文字段
```

示例：

```text
面单模式字段 = 面单模式
来源店铺字段 = 店铺名
鞋款简称字段 = 商品简称
规格字段 = 规格
尺码字段 = 尺码
数量字段 = 数量
备注字段 = 备注
```

注意：来源店铺字段只是普通字段角色，不允许由此产生店铺管理模型。

### 7.9 鞋款简称映射

由用户维护，不允许写死。

功能：

```text
workspace_id
面单模式ID，可选
来源简称
标准鞋款
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

### 7.10 规格映射

由用户维护，不允许写死。

功能：

```text
workspace_id
面单模式ID，可选
原始规格
标准规格
标准鞋款
绑定档口
绑定图片
是否启用
批量导入
批量导出
未映射值自动收集
```

### 7.11 档口管理

档口是报货对象，不是数据隔离对象。

功能：

```text
workspace_id
档口名称
联系人
备注
是否启用
绑定标准鞋款 / 标准规格
```

### 7.12 商品图片管理

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

图片存储原则：

```text
MySQL 只存图片元数据、路径、hash、绑定关系。
图片文件存 storage/workspaces/{workspace_id}/uploads/product-images/ 或后续对象存储。
禁止将图片二进制作为 BLOB 存入 MySQL。
```

### 7.13 报货汇总

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

### 7.14 异常处理

异常类型：

```text
面单模式无法识别
面单模板无法识别
原始内容解析失败
标准字段缺失
鞋款简称未映射
规格未映射
尺码无法识别
数量异常
图片未绑定
档口未绑定
导出模板缺失
```

异常支持人工修正后重新生成报货结果。

### 7.15 Excel 导出

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

## 8. 数据库核心表建议

第一版至少包含：

```text
users
roles
user_roles
workspaces
user_workspaces
collectors
capture_tasks
capture_batches
raw_capture_records
waybill_modes
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
workspace_id
created_at
updated_at
created_by
updated_by
is_deleted
```

业务表不得使用 `shop_id` 作为核心隔离字段。

---

## 9. 后端接口最低要求

至少实现以下接口组：

```text
/auth/login
/auth/me
/workspaces
/users
/roles
/collectors
/capture-tasks
/capture-batches
/raw-capture-records
/waybill-modes
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

## 10. 前端页面最低要求

至少搭建以下页面：

```text
登录页
首页仪表盘
工作空间管理
面单模式管理
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

## 11. 第一版开发优先级

### P0：先跑通标准化 Excel 到报货 Excel

必须优先完成：

```text
用户登录
工作空间管理
面单模式管理
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
上传一份标准化 Excel 后，系统可以根据当前 workspace 的面单模式和用户维护的映射关系，生成类似“鞋款分类 | 规格 | 图片 | 尺码 | 数量 | 备注”的档口报货 Excel。
```

### P1：接入原始采集记录与面单模板解析

完成：

```text
上传原始采集文件
保存 raw_payload
配置面单模式
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

## 12. Windows 部署要求

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

## 13. 禁止事项

必须严格遵守：

```text
禁止保留旧系统源码。
禁止把具体店铺名称写死在代码中。
禁止把店铺作为系统一级业务对象。
禁止使用 shop_id 作为核心数据隔离字段。
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
禁止将图片二进制作为 BLOB 存入 MySQL。
```

允许存在默认示例数据，但示例数据必须通过初始化配置写入数据库，不能写在业务代码里。

---

## 14. 验收标准

第一阶段验收必须满足：

```text
1. 项目目录结构完整，前后端可分别启动。
2. 后端 OpenAPI 可访问。
3. 前端登录后可进入管理后台。
4. 可创建工作空间、面单模式、档口、鞋款简称映射、规格映射。
5. 可上传商品图片并绑定到标准鞋款 + 标准规格。
6. 可上传标准化 Excel。
7. 可生成标准化明细批次。
8. 可自动识别未映射鞋款简称、未映射规格、图片缺失、档口缺失异常。
9. 修正异常后可重新生成报货结果。
10. 可导出三种 Excel：合并 Sheet、鞋款档口 Sheet、鞋款档口文档。
11. 导出的 Excel 必须包含图片列，图片嵌入单元格。
12. 操作日志、导出记录、异常记录可查询。
13. 不存在 shop_id 核心隔离逻辑。
14. 所有业务数据按 workspace_id 隔离。
15. Windows 启动脚本可用。
```

---

## 15. Codex 执行顺序

请按以下顺序执行，不要跳跃式开发：

```text
1. 初始化项目目录结构。
2. 初始化后端 FastAPI 工程。
3. 初始化前端 Vue 3 工程。
4. 编写数据库模型与迁移脚本。
5. 实现登录、用户、角色、工作空间基础模块。
6. 实现面单模式管理。
7. 实现标准化 Excel 上传与解析。
8. 实现字段角色配置。
9. 实现鞋款简称映射、规格映射、档口管理、图片管理。
10. 实现报货汇总引擎。
11. 实现异常处理。
12. 实现 Excel 三模式导出。
13. 实现原始采集记录和面单模板框架。
14. 实现采集端接口契约和最小客户端框架。
15. 补齐前端页面。
16. 补齐 Windows 脚本和 README。
17. 编写基础测试与示例数据。
```

每完成一个阶段，提交清晰 commit，不要一次性混合大量无关改动。
