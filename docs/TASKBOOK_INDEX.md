# 阶段任务书索引

> 本索引用于保留每个阶段的任务书。后续阶段只能新增任务书文件，不允许覆盖或改写旧阶段任务书作为新阶段任务书使用。

## 留档规则

```text
1. 每个阶段必须有独立任务书文件。
2. 阶段任务书文件名必须包含日期、阶段编号和阶段主题。
3. 已完成或已发布的阶段任务书只允许追加勘误，不允许改写成新阶段内容。
4. 新阶段开始时，在 docs/taskbooks/ 下新增文件。
5. 新增后必须更新本索引。
6. README 只链接本索引和当前阶段文件，避免旧任务书被误覆盖。
```

建议命名：

```text
docs/taskbooks/YYYY-MM-DD-stage-XX-topic-taskbook.md
```

## 主任务书

- [Codex 项目任务书](CODEX_TASKBOOK.md)

主任务书是总纲，不替代阶段任务书。阶段任务书必须服从主任务书。

## 阶段任务书

### 阶段 01：项目定位与平台边界

状态：已完成基础文档同步

相关文档：

```text
docs/CODEX_TASKBOOK.md
docs/PLATFORM_SCOPE.md
docs/WAYBILL_DRIVEN_DESIGN.md
docs/CONFIG_SCOPE.md
```

说明：

```text
该阶段确定系统不是固定业务订单系统，而是面单读取、用户定义字段和用户配置驱动的平台。
```

### 阶段 02：数据库持久化与平台基础能力

状态：推进中

任务书：

- [2026-06-11-stage-02-database-foundation-taskbook.md](taskbooks/2026-06-11-stage-02-database-foundation-taskbook.md)

目标：

```text
数据库连接
ORM 模型
Repository workspace_id 强过滤
JWT 登录
用户 / 角色 / 工作空间
基础资源接口
管理 / 开发者后台基础能力
```

### 阶段 03：用户工作台入口与后台拆分

状态：推进中，前端入口拆分和用户工作台页面骨架已完成

任务书：

- [2026-06-11-stage-03-workbench-entry-taskbook.md](taskbooks/2026-06-11-stage-03-workbench-entry-taskbook.md)

目标：

```text
保留当前管理 / 开发者验证台
新增用户工作台入口
拆分 /workbench 与 /admin 路由
搭建面单批次处理流程页面骨架
为 P0 标准化 Excel 到报货 Excel 闭环做准备
```

### 阶段 04：工作空间上下文与多用户数据隔离闭环

状态：推进中，核心闭环已完成，待阶段提交与后续 P0 接入

任务书：

- [2026-06-11-stage-04-workspace-context-closure-taskbook.md](taskbooks/2026-06-11-stage-04-workspace-context-closure-taskbook.md)

目标：

```text
前端接入 /auth/me
建立 session / workspace 上下文
新增工作空间选择器
API 自动携带当前 X-Workspace-Id
切换 workspace 后重新加载资源数据
永久化双用户双 workspace 隔离测试
完成“不同用户读取不同 workspace 数据”的前后端闭环
```

### 阶段 05：采集器与打印组件连接

状态：待推进，已被阶段 06 的入口与端口边界修正约束

任务书：

- [2026-06-11-stage-05-collector-print-component-taskbook.md](taskbooks/2026-06-11-stage-05-collector-print-component-taskbook.md)

目标：

```text
制作部署在用户业务机上的采集器
连接系统平台
注册采集器并维持心跳
通过适配器读取打印组件数据
优先适配菜鸟打印组件和抖店打印组件
回传 raw_capture_records
支持本地队列、断网缓存和恢复补传
为平台面单解析和标准化明细生成提供原始数据
```

### 阶段 06：租户逻辑隔离与三端入口整改

状态：已完成最小版本

任务书：

- [2026-06-11-stage-06-tenant-three-portal-correction-taskbook.md](taskbooks/2026-06-11-stage-06-tenant-three-portal-correction-taskbook.md)

目标：

```text
确认第一版采用单个平台数据库、多租户逻辑隔离
新增租户 / 客户层基础模型
将平台后台 UI 与租户端 UI 端口隔离
租户端 UI 只包含业务页面和管理页面
平台后台 UI 只维护客户 / 租户、工作空间、用户、平台共用面单解析模式和解析模板
确保采集、字段、图片、档口、异常和导出都留在租户端 UI
```

### 阶段 07：数据库租户归属与数据边界闭环

状态：执行中，本轮已完成核心数据库归属整改

任务书：

- [2026-06-11-stage-07-database-tenant-closure-taskbook.md](taskbooks/2026-06-11-stage-07-database-tenant-closure-taskbook.md)

目标：
```text
明确第一版单平台数据库、多租户逻辑隔离方案
补齐 tenant_id + workspace_id 数据归属标准，并将面单解析规则收口为平台全局能力
让账号登录、上传、创建的数据自动进入当前账号可访问的 workspace
将所有客户业务数据限制在客户工作区内
补齐 ORM、Repository、初始化 SQL、SQLite 兼容迁移和测试
新增数据库设计文档，作为采集器和 P0 闭环前置依据
```

### 阶段 08：代码边界收紧与复查

状态：已完成本轮代码收紧与验证

任务书：

- [2026-06-11-stage-08-code-tightening-check-taskbook.md](taskbooks/2026-06-11-stage-08-code-tightening-check-taskbook.md)

目标：
```text
进入采集器和 P0 闭环前，再次收紧权限派生、系统字段保护、前端中文文案和构建产物可见入口。
```

### 阶段 09：最小采集器身份、任务控制与原始记录回传闭环

状态：已完成最小版本

任务书：

- [2026-06-11-stage-09-mvp-collector-loop-taskbook.md](taskbooks/2026-06-11-stage-09-mvp-collector-loop-taskbook.md)

目标：
```text
先不接真实打印组件，跑通 collector_token、心跳、开始采集、结束采集和 raw_capture_records 回传。
```

## 当前工作指向

当前已完成阶段 09 的最小采集器闭环，下一步建议进入原始采集记录到客户可读面单信息的最小解析闭环。

优先顺序：

```text
1. 保持阶段 07/08/09 的数据库边界、权限边界、采集器身份边界和前端入口约束。
2. 从 raw_capture_records 生成 standard_details 的最小解析闭环。
3. 业务页面展示客户可读面单信息。
4. 再推进用户字段用途、关键字段、图片档口匹配和 Excel 导出。
5. 菜鸟 / 抖店真实 adapter 等平台协议稳定后再接入。
```

### 阶段 10：本地打印组件任务库复制采集器

状态：已完成最小版本

任务书：

- [2026-06-11-stage-10-local-print-db-copy-taskbook.md](taskbooks/2026-06-11-stage-10-local-print-db-copy-taskbook.md)

目标：

```text
基于本机验证结果，把采集器从模拟器推进为真实业务机最小采集器。
采集器只负责识别菜鸟/云打印本地 print.db，按采集水位复制新增 task.msg，并上传 raw_capture_records。
业务字段解析、商品匹配、图片匹配、档口匹配和 Excel 导出继续留在平台后端与客户配置层完成。
```

### 阶段 11：本地服务器控制台

状态：已完成最小版本

任务书：

- [2026-06-11-stage-11-local-server-console-taskbook.md](taskbooks/2026-06-11-stage-11-local-server-console-taskbook.md)

目标：

```text
为新手部署和阶段验收提供一个本地服务器控制台。
一键启动后端、客户 UI、平台后台，集中查看状态、日志、常用地址，并支持启动本机采集器。
```

### 阶段 12：Docker 本地部署入口

状态：已完成最小版本

任务书：

- [2026-06-11-stage-12-docker-local-deployment-taskbook.md](taskbooks/2026-06-11-stage-12-docker-local-deployment-taskbook.md)

目标：

```text
让本机只依赖 Docker Desktop 启动后端、客户 UI 和平台后台 UI。
避免新手手动部署 Python、Node、npm、pip 等开发环境。
```

### 阶段 13：框架健康检查与业务闭环启动判断

状态：已完成
任务书：

- [2026-06-11-stage-13-framework-health-check-taskbook.md](taskbooks/2026-06-11-stage-13-framework-health-check-taskbook.md)

目标：

```text
在进入完整业务流程前，对当前平台框架、部署入口、权限边界、三端页面分工和采集链路基础能力做一次收口检查。
结论：框架可以继续推进；下一步建议先做最小业务模拟闭环。
```

### 阶段 14：采集器客户端可部署化收紧

状态：已完成本轮最小版本
任务书：

- [2026-06-11-stage-14-collector-client-hardening-taskbook.md](taskbooks/2026-06-11-stage-14-collector-client-hardening-taskbook.md)

目标：

```text
根据“先做采集器”的调整，把采集器从开发脚本推进为更接近业务机可运行客户端的最小版本。
补齐账号密码登录绑定、配置文件、持久水位、检查命令、bat 启动入口、服务端组件状态保存和后续 Windows exe 打包入口。
采集器连接方式已从“客户管理页复制 token”调整为“采集器自身账号密码登录”。
服务器根据登录账号所属 workspace 自动绑定 tenant_id + workspace_id，并返回采集器运行 token。
```

### 阶段 15：采集器连接状态与采集回传可视化验收

状态：已完成本轮最小版本
任务书：

- [2026-06-11-stage-15-collector-visual-acceptance-taskbook.md](taskbooks/2026-06-11-stage-15-collector-visual-acceptance-taskbook.md)

目标：

```text
把采集器连接、组件状态、采集任务、回传数量和 raw_payload 展示到客户管理页和业务页。
让客户可以按“打开采集器 -> 页面看到在线 -> 开始采集 -> 回传记录 -> 结束采集”的路径验收。
```

### 阶段 16：采集器可见客户端

状态：已完成本轮最小版本
任务书：

- [2026-06-11-stage-16-collector-visible-client-taskbook.md](taskbooks/2026-06-11-stage-16-collector-visible-client-taskbook.md)

目标：

```text
补齐业务机上可以直接看到的采集器窗口。
客户可以在窗口里登录保存、检查连接、查看打印组件状态、启动 / 停止监听和查看实时日志。
采集开始 / 结束仍由客户业务 UI 统一控制。
```

### 阶段 17：平台解析模板与采集结果整理 MVP

状态：已完成本轮最小版本
任务书：

- [2026-06-11-stage-17-platform-parser-template-mvp-taskbook.md](taskbooks/2026-06-11-stage-17-platform-parser-template-mvp-taskbook.md)

目标：

```text
先把抖店 / CloudPrint 和菜鸟云打印解析模板置入平台后台。
采集器上传 raw_capture_records 后，后端自动生成客户可读 standard_details。
客户业务页从 raw JSON 展示转向整理后的面单字段展示。
```

### 阶段 18：菜鸟来源拆分与解析结果整改

状态：已完成本轮最小版本
任务书：

- [2026-06-11-stage-18-cainiao-source-split-taskbook.md](taskbooks/2026-06-11-stage-18-cainiao-source-split-taskbook.md)

目标：

```text
修正“同一打印组件等于同一解析模式”的假设。
将菜鸟店铺直接打印和菜鸟 woda 打印平台拆成不同平台解析模式。
店铺直打抽结构化订单字段；woda 中转从 printXML / CDATA 抽取可见商品文字。
客户业务页按采集任务隔离批次，主表优先展示本轮商品信息。
物流单号、平台订单号、店铺名等作为辅助字段，后续匹配以商品文字为主。
```

### 阶段 19：客户侧配置与大批量采集查看 MVP

状态：已完成本轮最小版本
任务书：

- [2026-06-11-stage-19-client-config-workflow-mvp-taskbook.md](taskbooks/2026-06-11-stage-19-client-config-workflow-mvp-taskbook.md)

目标：

```text
平台端 MVP 先封板，开始推进客户业务页和客户管理页。
业务页支持按采集任务查看本轮商品信息，并提供搜索、来源筛选和分页。
客户管理页支持字段定义、关键字段组合、图片资料、档口资料和关键词匹配规则的最小配置。
下一步进入自动匹配执行和 Excel 导出。
```

### 阶段 20：商品父级与 SKU 图片导入整改

状态：已完成本轮最小版本
任务书：

- [2026-06-11-stage-20-product-sku-image-import-taskbook.md](taskbooks/2026-06-11-stage-20-product-sku-image-import-taskbook.md)

目标：

```text
修正客户侧商品图片配置模型。
客户先创建商品，再选择该商品上传 SKU 图片 ZIP。
系统把 ZIP 中的 SKU 图片导入到这个商品下面，形成“商品 -> 多个 SKU -> 图片”的关系。
商品名称不从 ZIP 推断，始终由客户定义。
```

### 阶段 21：客户侧商品识别流程纠偏

状态：已完成本轮最小版本
任务书：

- [2026-06-11-stage-21-product-identification-flow-correction-taskbook.md](taskbooks/2026-06-11-stage-21-product-identification-flow-correction-taskbook.md)

目标：

```text
移除客户管理页中无效的“字段用途”和“关键字段”入口。
平台服务端负责解析面单并提供可读商品文字。
客户业务端直接使用解析出的商品文字配置商品识别规则，SKU 由系统自动匹配。
```

### 阶段 22：采集信息导入与识别预览页

状态：已完成本轮最小版本
任务书：

- [2026-06-11-stage-22-recognition-import-preview-taskbook.md](taskbooks/2026-06-11-stage-22-recognition-import-preview-taskbook.md)

目标：

```text
新增识别预览页。
支持导入采集任务或临时粘贴面单商品文字。
预览商品规则命中、SKU 自动匹配和图片状态。
本阶段只做预览，不回写数据库。
```

### 阶段 23：采集任务文档下载与表头定义

状态：已完成本轮最小版本
任务书：

- [2026-06-11-stage-23-task-document-download-and-definition-taskbook.md](taskbooks/2026-06-11-stage-23-task-document-download-and-definition-taskbook.md)

目标：

```text
同一轮采集任务提供原文文档和整理后文档下载。
整理后文档的表头不固定在系统中。
客户管理员可以保存当前工作区的表头定义。
下载整理文档时按当前工作区已保存表头输出。
```

### 阶段 24：面单原文识别样本标注 MVP

状态：已完成本轮最小版本
任务书：

- [2026-06-11-stage-24-recognition-sample-labeling-taskbook.md](taskbooks/2026-06-11-stage-24-recognition-sample-labeling-taskbook.md)

目标：

```text
新增客户管理页“识别样本”。
客户可以粘贴复杂面单商品原文，系统拆分候选片段。
客户点选片段并标成商品关键词、规格、尺码和数量。
样本保存到当前工作区，为后续识别引擎学习和预览闭环做准备。
```

### 阶段 25：识别预览显式规则收紧

状态：已完成本轮修正
任务书：

- [2026-06-11-stage-25-recognition-preview-explicit-rules-taskbook.md](taskbooks/2026-06-11-stage-25-recognition-preview-explicit-rules-taskbook.md)

目标：

```text
识别预览不再把商品名称当作兜底识别规则。
只有客户明确维护过的商品识别规则或识别样本才允许命中商品。
页面显示命中来源，避免用户误解系统如何识别。
```

### 阶段 26：商品识别冲突保护

状态：已完成本轮修正
任务书：

- [2026-06-11-stage-26-product-match-conflict-guard-taskbook.md](taskbooks/2026-06-11-stage-26-product-match-conflict-guard-taskbook.md)

目标：

```text
同一条面单文字同时命中多个不同商品时，不自动选择。
识别预览显示“商品冲突”。
冲突行不进入 SKU 自动匹配，也不显示为可生成。
页面列出冲突候选商品和命中关键词。
```

### 阶段 27：抖店第一版客户端收口

状态：已完成本轮修正
任务书：

- [2026-06-11-stage-27-douyin-client-scope-trim-taskbook.md](taskbooks/2026-06-11-stage-27-douyin-client-scope-trim-taskbook.md)

目标：

```text
客户管理端先收敛到抖店第一版。
只保留采集连接、商品/SKU、商品识别。
隐藏识别样本、识别预览、图片与档口等探索入口。
商品识别页面改为“抖店商品标题关键词 -> 我的商品”的明确口径。
```

### 阶段 28：客户管理端删除操作补齐

状态：已完成本轮修正
任务书：

- [2026-06-11-stage-28-client-admin-delete-actions-taskbook.md](taskbooks/2026-06-11-stage-28-client-admin-delete-actions-taskbook.md)

目标：

```text
当前抖店第一版客户管理页补齐删除/移除操作。
商品识别规则、商品、SKU、采集连接都可以由用户清理。
删除操作必须有确认弹窗，并走后端软删除接口。
```

### 阶段 29：商品识别页读取采集 Excel

状态：已完成本轮最小版本
任务书：

- [2026-06-11-stage-29-matching-excel-preview-taskbook.md](taskbooks/2026-06-11-stage-29-matching-excel-preview-taskbook.md)

目标：

```text
商品识别页支持上传采集导出的 .xlsx。
系统读取商品标题候选，用户点击候选回填关键词。
用户再选择自己的商品并保存规则。
Excel 读取只辅助录入，不自动批量生成规则。
```

### 阶段 30：采集控制页面单数口径修正

状态：已完成本轮修正
任务书：

- [2026-06-12-stage-30-capture-task-waybill-count-taskbook.md](taskbooks/2026-06-12-stage-30-capture-task-waybill-count-taskbook.md)

目标：

```text
采集控制页按钮位置稳定，不随状态变化跳动。
“回传”数量改为按整理后的面单数量统计。
原始采集记录仍保留为诊断信息，不作为业务主数量。
```

### 阶段 31：整理文档旧表头定义清理

状态：已完成本轮修正
任务书：

- [2026-06-12-stage-31-export-header-cleanup-taskbook.md](taskbooks/2026-06-12-stage-31-export-header-cleanup-taskbook.md)

目标：

```text
清理历史探索阶段写入的错误导出表头。
没有客户明确配置导出表头时，不生成伪业务整理文档。
移除旧隐藏页面保存导出表头定义的能力。
```

### 阶段 32：抖店字段说明与导出表头定义

状态：已完成本轮最小版本
任务书：

- [2026-06-12-stage-32-douyin-export-header-definition-taskbook.md](taskbooks/2026-06-12-stage-32-douyin-export-header-definition-taskbook.md)

目标：

```text
客户管理端展示抖店面单可读取字段的含义和真实样例。
客户管理员选择字段并自定义整理文档 Excel 表头。
保存后的表头进入当前工作区 field_definitions。
```

### 阶段 33：抖店一条打印任务多面单解析修复

状态：已完成本轮修复
任务书：

- [2026-06-12-stage-33-douyin-multi-document-parse-taskbook.md](taskbooks/2026-06-12-stage-33-douyin-multi-document-parse-taskbook.md)

目标：

```text
抖店一条 raw_capture_record 中包含多个 task.documents 时，按 document 拆成多张面单。
修复“打印两条订单但只生成一条采集结果”的问题。
```

### 阶段 34：按面单模式和字段绑定商品识别规则

状态：已完成本轮修正
任务书：

- [2026-06-12-stage-34-field-bound-product-recognition-taskbook.md](taskbooks/2026-06-12-stage-34-field-bound-product-recognition-taskbook.md)

目标：

```text
商品识别规则从“关键词匹配所有文本”收紧为“面单模式 + 参与识别字段 + 关键词 + 目标商品”。
抖店默认识别字段包含商品信息、商品简称、规格文本、买家备注和卖家备注。
菜鸟店铺直打默认识别字段包含商品信息、买家备注和卖家备注。
菜鸟 woda 暂时只使用自定义打印文字，字段含义留给后续用户模板定义。
```

### 阶段 35：框架收紧与验证入口整理

状态：已完成本轮收紧
任务书：

- [2026-06-12-stage-35-framework-tightening-taskbook.md](taskbooks/2026-06-12-stage-35-framework-tightening-taskbook.md)

目标：

```text
从项目根目录直接运行 pytest 能识别 backend/app。
采集器名称默认预填 Windows 主机名，旧默认名称自动归一。
原始采集 Excel 下载列口径收紧，不再暴露采集任务ID、原始文档ID、来源序号等内部编号。
原始采集 Excel 主表只保留用户可理解的采集来源和采集原文。
```

### 阶段 36：探索代码清理

状态：已完成本轮清理
任务书：

- [2026-06-12-stage-36-exploration-code-cleanup-taskbook.md](taskbooks/2026-06-12-stage-36-exploration-code-cleanup-taskbook.md)

目标：

```text
删除不再进入正式业务路径的探索页面代码。
清理旧路由重定向和探索页样式残留。
保留历史任务书，不把探索代码继续软保留在正式前端源码里。
```

### 阶段 37：服务端后台资源页收紧

状态：已完成本轮收紧
任务书：

- [2026-06-12-stage-37-server-admin-resource-tightening-taskbook.md](taskbooks/2026-06-12-stage-37-server-admin-resource-tightening-taskbook.md)

目标：

```text
服务端后台不再显示通用 JSON 新建记录框。
解析模式页只显示当前正式支持的 3 种平台解析模式。
隐藏 Manual upload 和 cainiao_cloud_print 遗留模式。
```

### 阶段 38：我打模板识别码与客户模板边界

状态：已完成本轮最小修正
任务书：

- [2026-06-12-stage-38-woda-template-fingerprint-taskbook.md](taskbooks/2026-06-12-stage-38-woda-template-fingerprint-taskbook.md)

目标：

```text
我打 / woda 模式读取 printXML 可见商品区原文。
按 printXML 布局生成模板识别码，用于区分同一客户的不同打印模板。
模板识别码只作为分组依据，不作为商品关键词匹配字段。
客户模板含义后续在客户工作区按模板识别码自行定义。
```

### 阶段 39：客户管理端打印模板规则 UI

状态：已完成本轮最小版本
任务书：

- [2026-06-12-stage-39-client-template-rule-ui-taskbook.md](taskbooks/2026-06-12-stage-39-client-template-rule-ui-taskbook.md)

目标：

```text
新增客户管理端“打印模板规则”页面。
仅展示我打面单模板，抖店 / 菜鸟店铺直打不在此页面维护。
菜鸟 woda / 我打中转展示自定义区样本，并提供行级拆分规则配置、预览和客户定义列表。
模板规则保存到当前工作区的 print_template_configs。
采集样本只用于样本数量和我打自定义拆分，不再在业务端自行生成模板行。
商品识别页读取平台模板字段，平台已解析字段只用于查看和选择参与识别。
商品识别页的我打模式需要先选择当前工作区已保存的我打客户模板。
商品识别页直接读取当前工作区已采集面单，不再上传采集 Excel。
我打模式即使未保存模板定义，也先展示当前工作区已采集自定义区原文；保存规则时仍要求选择我打模板。
打印模板规则页左侧只展示已保存的客户模板定义，新建入口默认基于平台我打模板创建新定义。
商品识别页中我打候选不再使用模板样例冒充每条面单的规格 / 尺码 / 数量，候选补充信息改为基于当前面单原文临时推断。
商品识别页隐藏我打字段的“模板样例”辅助说明，已采集面单候选按面单 ID 倒序显示。
```

### 阶段 40：我打模板规则应用到标准明细

状态：待执行
任务书：

- [2026-06-12-stage-40-woda-template-rule-application-taskbook.md](taskbooks/2026-06-12-stage-40-woda-template-rule-application-taskbook.md)

目标：

```text
把当前工作区保存的我打模板规则应用到 cainiao_woda_printxml 标准明细。
根据 print_template_configs.config 生成 custom_product_text、custom_spec_text、custom_quantity_text、custom_size_text。
商品识别页读取规则应用后的 custom_* 字段，不再依赖前端临时推断作为主口径。
提供模板规则试算和批量应用入口。
```

### 阶段 41：多商品面单按商品行展开整理导出

状态：已完成本轮最小整改
任务书：

- [2026-06-13-stage-41-multi-item-standard-export-taskbook.md](taskbooks/2026-06-13-stage-41-multi-item-standard-export-taskbook.md)

目标：

```text
下载整理文档时，遇到包含 custom_items 的我打面单，按商品行展开输出。
同一张面单的公共字段保留，商品字段由每个 custom_items[i] 覆盖。
导出表头配置页补充我打商品行字段，用户可以选择商品文字、销售属性1、销售属性2、数量文字、备注字段。
本阶段不把一张原始面单拆成多张 raw_capture_records，也不拆成多条 standard_details。
```

### 阶段 42：已采集面单按监听批次归档读取

状态：已完成本轮最小整改
任务书：

- [2026-06-13-stage-42-capture-batch-archive-taskbook.md](taskbooks/2026-06-13-stage-42-capture-batch-archive-taskbook.md)

目标：

```text
打印模板规则页读取样本前，先选择监听批次。
商品识别页读取已采集面单前，先选择监听批次。
默认选择最近一轮包含整理面单的监听批次。
批次切换后，样本列表、候选面单和候选商品行都只来自当前批次。
已保存的模板定义和商品/SKU 识别规则仍按工作区保存，可跨批次复用。
```

### 阶段 43：商品/SKU 识别执行引擎

状态：执行中，本轮先做批次预览闭环
任务书：

- [2026-06-13-stage-43-product-sku-recognition-engine-taskbook.md](taskbooks/2026-06-13-stage-43-product-sku-recognition-engine-taskbook.md)

目标：

```text
新增后端商品/SKU 识别执行服务。
以监听批次为输入，读取该批次 standard_details。
我打多商品面单按 custom_items 展开为商品行。
每个商品行先匹配商品名称，再在该商品下匹配 SKU。
SKU 主匹配使用销售属性1，匹配不到时使用备注字段兜底。
商品识别页增加“预览本批次识别结果”。
```

### 阶段 44：商品主类识别与 SKU 自动匹配

状态：执行中，本轮修正商品识别规则口径
任务书：

- [2026-06-13-stage-44-optional-sku-auto-match-taskbook.md](taskbooks/2026-06-13-stage-44-optional-sku-auto-match-taskbook.md)

目标：

```text
商品识别页的关联 SKU 改为可选。
用户保存规则时，只要能识别商品主类即可。
商品主类可以通过商品文字识别，也可以通过销售属性1/销售属性2/备注字段识别。
后端识别引擎在命中商品后，自动用面单销售属性匹配该商品下的 SKU。
保留用户显式选择 SKU 的能力，作为少量特殊规则的锁定命中。
```

### 阶段 45：业务现场验证准备与采集器下载入口

状态：执行中，本轮准备真实业务现场验证
任务书：

- [2026-06-13-stage-45-business-site-validation-readiness-taskbook.md](taskbooks/2026-06-13-stage-45-business-site-validation-readiness-taskbook.md)

目标：

```text
客户管理员登录系统后可以直接下载采集器 ZIP。
后端在部署镜像内提供 collector-client 打包下载接口。
进入现场验证前清理当前工作区旧业务数据，并保留账号、租户、工作区和平台解析模板。
客户可重新上传商品/SKU、创建我打模板、配置商品识别规则，并用真实采集数据验证识别结果。
```

### 阶段 46：报货 Excel 导出闭环

状态：已完成本轮第一版接入
任务书：

- [2026-06-13-stage-46-report-excel-export-closure-taskbook.md](taskbooks/2026-06-13-stage-46-report-excel-export-closure-taskbook.md)

目标：

```text
新增报货 Excel 下载能力。
导出中心可以选择监听批次，并下载该批次商品识别结果。
导出数据以商品识别结果为准，而不是只导出 standard_details 原字段。
一张面单多个商品时，每个商品项输出一行；单商品面单也按一个商品项输出一行。
Excel 中展示商品、SKU、数量、匹配状态和异常原因。
第一版先生成无图片报货表，图片嵌入和复杂分组放到后续阶段。
```

### 阶段 47：商品规则模板指纹兜底修复

状态：已完成本轮修复
任务书：

- [2026-06-14-stage-47-template-fingerprint-recognition-fix-taskbook.md](taskbooks/2026-06-14-stage-47-template-fingerprint-recognition-fix-taskbook.md)

目标：

```text
商品识别规则不再只依赖会变化的模板配置 ID。
已采集历史面单即使模板 ID 为空或过期，也能按版式指纹匹配规则。
新建规则时保存真实版式指纹，避免模板重命名、删除、重建后规则失效。
```

### 阶段 48：现场 Alpha 整改与发布收口

状态：待执行，作为当前整改总任务书
任务书：

- [2026-06-15-stage-48-site-alpha-hardening-taskbook.md](taskbooks/2026-06-15-stage-48-site-alpha-hardening-taskbook.md)

配套清单：

- [PROJECT_RECTIFICATION_TASK_LIST.md](PROJECT_RECTIFICATION_TASK_LIST.md)

P0 审计记录：

- [2026-06-15-stage-48-p0-source-freeze-audit.md](taskbooks/2026-06-15-stage-48-p0-source-freeze-audit.md)

目标：

```text
冻结当前现场 Alpha 基线。
收口源码、采集器、解析识别回归、报货 Excel、部署迁移文档。
把项目从现场边跑边修推进到可控客户验证版。
```

### 阶段 49：E 盘抖店 productInfo 模板化整改

状态：待执行，当前从 C 盘基线恢复后的 E 盘专项整改
任务书：

- [2026-06-15-stage-49-e-douyin-template-productinfo-taskbook.md](taskbooks/2026-06-15-stage-49-e-douyin-template-productinfo-taskbook.md)

目标：

```text
只修改 E 盘项目。
打印模板规则页重新纳入抖店模板维护入口。
抖店前台维护只围绕 productInfo 原文，不暴露候选 JSON 字段维护。
用户像我打模板一样点击原文片段，定义 商品 / 销售属性1 / 销售属性2 / 数量 / 备注。
后端解析抖店时应用保存的 field_mappings，并统一输出标准字段。
```

### 阶段 50：采集器掉线与心跳时间显示排查

状态：已完成排查，等待管理员权限放行本机 5173 入站
任务书：

- [2026-06-16-stage-50-collector-offline-network-diagnosis.md](taskbooks/2026-06-16-stage-50-collector-offline-network-diagnosis.md)

目标：

```text
确认三台业务机采集器掉线原因。
修正采集连接页和采集记录页的 UTC 原始时间显示。
定位采集器无法回连服务器的网络阻断点，并给出恢复动作。
```

### 阶段 53：E 盘源码目录整理与构建说明

状态：已完成
任务书：

- [2026-06-16-stage-53-e-drive-repo-cleanup-build-guide.md](taskbooks/2026-06-16-stage-53-e-drive-repo-cleanup-build-guide.md)

构建说明：

- [构建部署说明.md](构建部署说明.md)

目标：

```text
把 E 盘移动硬盘上的项目目录整理为干净源码目录。
保留 Git 仓库、源码、配置、测试和文档。
清理用户数据、本地依赖缓存、构建产物。
补充构建部署说明，方便后续提交 GitHub 或重新构建。
```

### 阶段 54：源码上传前去个人化清理

状态：已完成
任务书：

- [2026-06-16-stage-54-source-sanitization-taskbook.md](taskbooks/2026-06-16-stage-54-source-sanitization-taskbook.md)

目标：

```text
将待上传源码目录整理为通用项目形态。
清理个人名称、现场地址、本机路径、业务现场专用 Docker 命名和用户数据残留。
保留源码、配置、测试和通用构建部署说明，方便后续提交 GitHub。
```
