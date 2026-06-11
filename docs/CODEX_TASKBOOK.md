# 订单整理系统 8.0 Codex 项目任务书

> 本文档是当前项目的唯一主任务书。其他文档如与本文档冲突，以本文档为准。

## 0. 项目定位

从空仓库开始搭建完整项目，不保留旧系统源码，不复刻旧系统硬编码逻辑。

项目名称：订单整理系统

系统定位：面单模式驱动的可配置报货 Excel 平台。

最终目标：

```text
采集工具或用户上传数据
  ↓
系统识别面单模式
  ↓
系统按面单模板生成标准化明细
  ↓
用户在 Web 界面定义面单字段、关键字段、图片匹配、档口匹配和导出方式
  ↓
系统生成可直接发给档口的报货 Excel
```

系统要做的是平台框架，不是业务规则定制。

系统只负责提供通用能力：

```text
面单模式识别
原始采集内容留存
面单模板解析
标准化明细管理
面单字段配置器
关键字段匹配配置器
图片信息管理
档口资料维护
报货汇总引擎
Excel 导出引擎
异常提示与人工修正入口
多用户工作空间隔离
```

系统不负责在代码里定义任何具体业务规则。

---

## 1. 最高原则

必须严格遵守以下原则：

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

一句话原则：

```text
系统只识别和处理面单模式，其他业务规则都交给用户定义。
```

---

## 2. 技术栈

必须使用：

```text
前端：Vue 3 + TypeScript + Element Plus
后端：Python FastAPI
数据库：MySQL
缓存：Redis
Excel 处理：openpyxl
图片处理：Pillow
部署目标：Windows 内网服务器优先
```

不要生成 Java Spring Boot 或 Node.js NestJS 版本。第一版统一使用 FastAPI。

---

## 3. 多用户与数据隔离

服务器端启动后面向多个用户使用。第一版采用单库多工作空间模式：

```text
一个 MySQL 数据库
多个 Workspace 工作空间
每个 Workspace 维护自己的面单模式、模板、标准化明细、字段定义、关键字段匹配、图片、档口、报货批次和导出记录
```

关系：

```text
User
  ↓
Workspace
  ↓
Waybill Mode
  ↓
Templates / Standard Details / Field Definitions / Key Fields / Match Rules / Images / Stalls / Reports / Exports
```

要求：

```text
1. workspace_id 是最高数据隔离字段。
2. 一个用户可以属于一个或多个 workspace。
3. 一个 workspace 可以有多个用户。
4. 所有业务表必须带 workspace_id。
5. 后端 Repository 层必须强制按当前用户可访问的 workspace_id 过滤。
6. 文件存储必须按 workspace_id 分目录。
7. Redis key 必须带 workspace_id 前缀。
8. 禁止用户跨 workspace 查询、下载、导出、修改数据。
```

文件目录：

```text
storage/
  workspaces/
    workspace_1/
      raw/
      standard/
      exports/
      uploads/
        images/
        mapping-imports/
    workspace_2/
      raw/
      standard/
      exports/
      uploads/
        images/
        mapping-imports/
```

Redis key 示例：

```text
workspace:{workspace_id}:task:{task_id}
workspace:{workspace_id}:collector:{collector_id}
workspace:{workspace_id}:export:{export_id}
```

---

## 4. 项目目录结构

必须按前后端分离 + 采集端预留搭建：

```text
order-system/
  backend/                    # FastAPI 后端
  frontend/                   # Vue 3 管理后台
  collector-client/           # 面单采集工具客户端，第一版只做框架和接口契约
  docs/                       # 项目文档
  scripts/                    # Windows 启动、初始化、构建脚本
  storage/
    workspaces/               # 按 workspace_id 隔离文件
```

后端分层：

```text
api/          # 路由层，只做参数接收和响应
schemas/      # Pydantic 入参出参模型
models/       # SQLAlchemy ORM 模型
services/     # 应用服务
repositories/ # 数据访问，必须强制 workspace_id 过滤
engines/      # 面单解析、字段匹配、汇总、导出等引擎
core/         # 配置、鉴权、异常、日志
```

前端模块：

```text
src/views/login
src/views/dashboard
src/views/workspaces
src/views/waybill-modes
src/views/waybill-templates
src/views/collectors
src/views/capture-tasks
src/views/raw-capture-records
src/views/standard-details
src/views/field-definitions
src/views/field-roles
src/views/key-field-sets
src/views/match-rules
src/views/stalls
src/views/image-assets
src/views/report-batches
src/views/exceptions
src/views/export-records
src/views/users
```

---

## 5. 核心业务链路

### 5.1 采集阶段

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

第一版采集工具只做接口契约和最小客户端框架，不要求完成真实平台采集逻辑。

### 5.2 标准化阶段

```text
原始采集记录
  ↓
识别面单模式
  ↓
匹配面单模板
  ↓
执行字段提取规则
  ↓
生成标准化明细
  ↓
可导出标准化 Excel
```

原始采集内容不一定是 JSON。统一使用 `raw_payload`，禁止使用 `raw_json` 作为核心字段名。

### 5.3 报货阶段

```text
标准化明细
  ↓
用户定义面单字段和字段角色
  ↓
用户选择参与匹配的关键字段
  ↓
用户配置关键字段匹配规则
  ↓
用户配置图片和档口匹配结果
  ↓
用户选择导出方式
  ↓
系统生成报货 Excel
```

系统只执行用户配置，不在代码中内置具体规则。

---

## 6. 标准化明细字段

第一版标准化明细不预设业务字段。系统只固定平台追踪字段，面单业务字段来自用户上传 Excel 表头或面单模板提取规则。

平台追踪字段建议为：

```text
id
workspace_id
standard_detail_batch_id
面单模式
完整原文
字段值集合
图片匹配状态
档口匹配状态
任务ID
文档ID
任务时间
采集端ID
来源机器
来源序号
原始内容
```

说明：

```text
面单模式：系统核心字段，用于判断使用哪类模板和配置。
完整原文：从面单或打印信息中提取的完整原文，可为空。
字段值集合：JSON 或明细子表，保存用户定义面单字段的值。
图片匹配状态：展示字段，用于提示图片是否按用户配置匹配成功。
档口匹配状态：展示字段，用于提示档口是否按用户配置匹配成功。
任务ID、文档ID、任务时间、采集端ID、来源机器、来源序号：采集追踪字段。
原始内容：原始采集内容，不限定 JSON。
```

禁止在平台层固定任何业务字段。所有业务字段名称和含义都只能由用户后续创建和定义。

---

## 7. 原始采集数据设计

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

表：`raw_capture_records`

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

Web 页面按钮名称：

```text
查看原始采集内容
下载原始采集数据
下载原始采集包
```

不要写成：

```text
下载 raw_json
下载原始 JSON
```

---

## 8. 功能模块要求

### 8.1 用户、角色与工作空间

角色：

```text
系统管理员
管理员
运营人员
仓库人员
只读人员
```

权限：

```text
系统管理员：可管理所有 workspace。
管理员：管理所属 workspace 的用户、面单模式、模板、配置和数据。
运营人员：采集、导入、标准化、配置维护、异常处理、报货导出。
仓库人员：查看报货结果、下载报货 Excel。
只读人员：只查看，不修改。
```

第一版实现 JWT 登录、用户管理、角色管理、workspace 选择。

### 8.2 面单模式管理

系统核心对象是面单模式。

功能：

```text
新增面单模式
编辑面单模式
启用 / 停用面单模式
配置默认模板
查看该面单模式下的标准化明细、配置和报货批次
```

字段：

```text
workspace_id
面单模式名称
面单模式编码
输入格式
备注
是否启用
```

### 8.3 面单模板管理

面单模板用于把原始采集内容转换为标准化明细。

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

### 8.4 标准化明细管理

支持：

```text
从原始采集记录生成标准化明细
直接上传标准化 Excel
标准化明细预览
标准化明细筛选
导出标准化 Excel
```

第一版必须支持直接上传标准化 Excel，这是 P0 优先闭环。

### 8.5 面单字段与关键字段配置

用户必须能配置标准化明细中有哪些面单字段，以及哪些字段参与后续匹配、汇总和导出。

字段配置包括：

```text
workspace_id
面单模式ID，可选
字段名称
字段编码
数据类型
是否显示
是否可筛选
是否参与关键字段匹配
是否参与图片匹配
是否参与档口匹配
是否参与汇总分组
是否作为数量字段
是否作为备注字段
是否导出
导出顺序
```

说明：

```text
字段名称和业务含义由用户定义。
系统只提供字段配置能力，不预设任何字段一定代表某类业务对象。
关键字段是用户选择的字段集合，用于匹配图片、档口、汇总分组或导出拆分。
```

### 8.6 关键字段组合配置

由用户维护，不允许写死。

功能：

```text
workspace_id
面单模式ID，可选
配置名称
用途：图片匹配 / 档口匹配 / 汇总分组 / 导出拆分
关键字段列表
匹配优先级
是否启用
```

### 8.7 关键字段匹配规则

由用户维护，不允许写死。

功能：

```text
workspace_id
面单模式ID，可选
关键字段组合ID
匹配字段值
匹配目标类型：图片 / 档口 / 导出分组 / 其他用户自定义目标
匹配目标ID
匹配目标名称
是否启用
匹配优先级
批量导入
批量导出
未匹配值自动收集
人工修正入口
```

匹配字段值可以是单字段，也可以是多个用户定义字段组成的组合键。

### 8.8 图片信息管理

图片必须按 workspace 隔离，重新上传或批量导入匹配关系。

支持：

```text
单张上传
批量上传
批量导入图片匹配关系
按用户定义关键字段组合绑定图片
图片预览
图片缺失提示
```

存储原则：

```text
MySQL 只存图片元数据、路径、hash、绑定关系。
图片文件存 storage/workspaces/{workspace_id}/uploads/images/ 或后续对象存储。
禁止将图片二进制作为 BLOB 存入 MySQL。
```

### 8.9 档口管理

档口是报货对象，由用户维护。

功能：

```text
workspace_id
档口名称
联系人
备注
是否启用
按用户定义关键字段组合绑定档口
```

### 8.10 报货汇总

报货汇总引擎只执行用户配置。

第一版提供默认汇总能力：

```text
按用户配置的关键字段组合分组
按用户配置匹配图片
按用户配置匹配档口
对用户指定的数量字段求和
对用户指定的备注字段保留或合并
按用户选择的导出字段生成结果
```

注意：默认行为只能作为可编辑配置默认值，不能写成不可变业务规则。

字段排序必须支持用户配置。对于被用户声明为数字类型的字段，必须支持数字排序。

### 8.11 异常处理

异常类型：

```text
面单模式无法识别
面单模板无法识别
原始内容解析失败
用户定义字段缺失
关键字段缺失
关键字段组合未匹配
数量字段异常
图片未匹配
档口未匹配
导出配置缺失
```

异常支持人工修正后重新生成报货结果。

### 8.12 Excel 导出

必须支持三种输出方式：

```text
1. 合并 Sheet
   所有报货数据输出到一个 Sheet。

2. 分组 Sheet
   一个 Excel 文件，按用户配置的字段或档口拆成多个 Sheet。

3. 分组文档
   按用户配置的字段或档口拆成多个 Excel 文件，打包 ZIP 下载。
```

Excel 输出列由用户配置。系统可以提供可编辑默认模板，但不得把任何业务列写死为唯一模板。

必须支持图片嵌入 Excel，图片自适应单元格，设置列宽、行高、边框、表头样式。

### 8.13 采集端与采集任务

第一版采集端只做框架和接口契约。

采集端管理字段：

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

采集任务状态：

```text
待开始
采集中
已完成
失败
已取消
```

---

## 9. 数据库核心表

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
field_definitions
field_role_configs
key_field_sets
match_rules
stalls
image_assets
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

禁止出现：

```text
shops
shop_id
```

除非它们只是标准化明细中的普通列名，不得作为数据库隔离模型或业务主表。

---

## 10. 后端接口最低要求

至少实现：

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
/field-definitions
/field-role-configs
/key-field-sets
/match-rules
/stalls
/image-assets
/report-batches
/exceptions
/export-records
```

必须提供 OpenAPI 文档。

---

## 11. 前端页面最低要求

至少搭建：

```text
登录页
首页仪表盘
工作空间管理
面单模式管理
面单模板管理
标准化明细
面单字段定义
字段角色配置
关键字段配置
匹配规则配置
图片信息管理
档口管理
报货批次
异常处理
导出记录
采集端管理
采集任务管理
原始采集数据
用户管理
```

第一版页面可以先实现业务闭环，不追求复杂 UI。

---

## 12. 第一版开发优先级

### P0：标准化 Excel 到报货 Excel

优先完成平台闭环：

```text
用户登录
工作空间管理
面单模式管理
上传标准化 Excel
读取 Excel 表头并生成面单字段
面单字段与字段角色配置
关键字段组合配置
图片上传和匹配规则配置
档口匹配规则配置
档口管理
报货汇总生成
异常提示
三种模式导出 Excel
```

P0 验收目标：

```text
上传一份包含面单字段的 Excel 后，系统可以根据当前 workspace 的面单模式、用户定义字段、关键字段匹配规则、图片和档口配置，生成报货 Excel。
```

### P1：原始采集记录与面单模板解析

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

## 13. Windows 部署要求

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

## 14. 禁止事项

必须严格禁止：

```text
禁止保留旧系统源码。
禁止把具体用户业务对象名称写死在代码中。
禁止把用户业务对象作为系统一级固定对象。
禁止使用 shop_id 作为核心数据隔离字段。
禁止创建 shops 表作为业务主表。
禁止把具体用户业务概念写死在代码中。
禁止把具体面单字段写死在业务逻辑中。
禁止假设原始采集内容一定是 JSON。
禁止使用 raw_json 作为核心原始数据字段名。
禁止把 Excel 导出列写死为唯一模板。
禁止把业务规则写在 Controller 或前端页面里。
禁止为了演示功能写固定 if/else 业务规则。
禁止导入后覆盖原始采集内容。
禁止绕过用户配置直接生成报货结果。
禁止将图片二进制作为 BLOB 存入 MySQL。
```

允许存在默认示例数据，但示例数据必须通过初始化配置写入数据库，不能写在业务代码里。

---

## 15. 验收标准

第一阶段验收必须满足：

```text
1. 项目目录结构完整，前后端可分别启动。
2. 后端 OpenAPI 可访问。
3. 前端登录后可进入管理后台。
4. 可创建工作空间、面单模式、用户定义字段、关键字段组合、图片信息和档口。
5. 可上传图片并按用户定义关键字段组合配置匹配规则。
6. 可上传标准化 Excel。
7. 可生成标准化明细批次。
8. 可自动识别关键字段缺失、关键字段未匹配、图片缺失、档口缺失异常。
9. 修正异常后可重新生成报货结果。
10. 可导出三种 Excel：合并 Sheet、分组 Sheet、分组文档。
11. 导出的 Excel 必须包含图片列，图片嵌入单元格。
12. 操作日志、导出记录、异常记录可查询。
13. 所有业务数据按 workspace_id 隔离。
14. 不存在 shop_id 核心隔离逻辑。
15. Windows 启动脚本可用。
```

---

## 16. Codex 执行顺序

请按顺序执行：

```text
1. 初始化项目目录结构。
2. 初始化后端 FastAPI 工程。
3. 初始化前端 Vue 3 工程。
4. 编写数据库模型与迁移脚本。
5. 实现登录、用户、角色、工作空间基础模块。
6. 实现面单模式管理。
7. 实现标准化 Excel 上传与解析。
8. 实现面单字段与字段角色配置。
9. 实现关键字段组合、匹配规则、档口管理、图片信息管理。
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
