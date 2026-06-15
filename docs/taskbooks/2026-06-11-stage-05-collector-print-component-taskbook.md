# 阶段 05 任务书：采集器与打印组件连接

> 适用范围：在阶段 04 工作空间上下文闭环后，制作部署在用户业务机上的采集器，并完成采集器与系统平台的数据连接。  
> 上游依据：`docs/CODEX_TASKBOOK.md`、`docs/WAYBILL_DRIVEN_DESIGN.md`、`docs/taskbooks/2026-06-11-stage-04-workspace-context-closure-taskbook.md`  
> 当前前置状态：平台已具备登录、workspace 上下文、基础资源隔离和用户工作台入口；`collector-client/` 只有最小心跳脚手架。

## 0. 阶段目标

本阶段目标是建立“业务机采集器 → 系统平台 → 原始采集记录 → 用户工作台”的采集闭环。

目标链路：

```text
用户业务机
  ↓
本地采集器
  ↓
读取打印组件数据
  ↓
生成原始采集记录 raw_payload
  ↓
带 collector_id / workspace_id / source_machine 回传平台
  ↓
平台保存 RawCaptureRecord
  ↓
用户工作台查看采集批次和原始记录
  ↓
后续进入面单模式识别和标准化明细生成
```

已知优先适配的打印组件：

```text
菜鸟打印组件
抖店打印组件
```

注意：

```text
本阶段不预设这两个组件的内部协议。
具体读取方式需要通过官方文档、组件配置、实际业务机环境和可观测输出确认。
采集器必须采用适配器模式，不能把某一个打印组件写死为唯一来源。
```

## 1. 阶段原则

必须遵守：

```text
1. 采集器部署在用户业务机上，而不是只运行在服务器。
2. 一台用户机器可以运行一个采集器实例。
3. 一个 workspace 可以绑定多个采集器。
4. 所有采集数据必须带 workspace_id。
5. 所有采集数据必须带 collector_id、source_machine、source_index 或等价追踪信息。
6. 原始采集内容统一写入 raw_payload，不假设一定是 JSON。
7. payload_format 必须记录原始内容格式。
8. 采集器只负责采集和回传，不负责写死业务字段含义。
9. 菜鸟、抖店等打印组件必须通过 adapter 插件接入。
10. 采集器断网时必须能本地缓存，恢复后补传。
11. 不引入 shop_id、shops 或固定业务对象作为隔离模型。
```

## 2. 采集器定位

采集器是用户业务机上的本地客户端。

它负责：

```text
注册采集器
维持心跳
识别本机可用打印组件
监听或读取打印组件产生的数据
记录原始打印 / 面单内容
去重
本地缓存
断点续传
回传平台
上报状态和错误
```

它不负责：

```text
定义面单字段业务含义
决定哪些字段参与图片匹配
决定哪些字段参与档口匹配
生成最终报货 Excel
绕过用户配置直接生成结果
```

## 3. 采集器架构

建议结构：

```text
collector-client/
  collector/
    app.py
    config.py
    identity.py
    heartbeat.py
    queue.py
    sender.py
    adapters/
      base.py
      cainiao.py
      doudian.py
      file_watch.py
    storage/
      sqlite_queue.py
    logs/
  client.py
  README.md
```

核心抽象：

```text
CollectorIdentity
CollectorConfig
PrintComponentAdapter
CaptureEvent
LocalQueue
PlatformSender
HeartbeatService
```

Adapter 接口建议：

```text
detect() -> AdapterStatus
start() -> None
poll() -> list[CaptureEvent]
stop() -> None
```

CaptureEvent 统一字段：

```text
workspace_id
collector_id
source_machine
source_component
source_component_version
source_index
document_id
payload_format
raw_payload
source_columns
captured_at
dedupe_key
```

## 4. 平台后端交付范围

### 4.1 采集器注册

接口建议：

```text
POST /collectors/register
POST /collectors/heartbeat
GET /collectors
PATCH /collectors/{id}
```

注册内容：

```text
workspace_id
collector_id
collector_name
source_machine
client_version
supported_adapters
remark
```

心跳内容：

```text
workspace_id
collector_id
online_status
last_seen_at
adapter_status
queue_size
last_error
```

### 4.2 采集任务

接口建议：

```text
POST /capture-tasks
GET /capture-tasks
PATCH /capture-tasks/{id}
```

采集任务状态：

```text
待开始
采集中
已暂停
已完成
失败
已取消
```

### 4.3 原始采集记录回传

接口建议：

```text
POST /raw-capture-records/batch
GET /raw-capture-records
GET /raw-capture-records/{id}
```

批量回传内容：

```text
workspace_id
collector_id
capture_task_id
records[]
```

每条 records 内容：

```text
source_machine
source_component
source_index
document_id
waybill_mode
payload_format
raw_payload
source_columns
parsed_payload
dedupe_key
captured_at
```

后端要求：

```text
按 workspace_id 校验权限
按 collector_id 校验归属
按 dedupe_key 去重
保存 raw_payload 原文
保存 payload_format
不覆盖原始采集内容
允许 parsed_payload 为空
```

## 5. 打印组件适配范围

### 5.1 菜鸟打印组件适配器

目标：

```text
识别业务机是否安装 / 运行菜鸟打印组件
确认可读取的输出位置或数据接口
读取打印任务或面单原文
转换为 CaptureEvent
```

待确认内容：

```text
组件安装路径
本地端口或通信方式
日志 / 缓存 / spool 文件位置
打印任务唯一标识
打印内容格式
是否可获取完整面单原文
是否需要用户授权或登录态
```

### 5.2 抖店打印组件适配器

目标：

```text
识别业务机是否安装 / 运行抖店打印组件
确认可读取的输出位置或数据接口
读取打印任务或面单原文
转换为 CaptureEvent
```

待确认内容：

```text
组件安装路径
本地端口或通信方式
日志 / 缓存 / spool 文件位置
打印任务唯一标识
打印内容格式
是否可获取完整面单原文
是否需要用户授权或登录态
```

### 5.3 通用文件监听适配器

为降低第一版风险，本阶段建议同时做一个通用文件监听适配器。

用途：

```text
监听用户指定目录
读取新增 text / json / csv / xlsx 文件
生成 raw_capture_records
用于没有明确打印组件接口时的兜底采集方式
```

## 6. 采集器本地能力

必须具备：

```text
本机唯一 collector_id
配置文件
平台地址配置
workspace_id / collector token 配置
心跳
本地队列
失败重试
去重
日志文件
优雅退出
Windows 启动方式
```

本地配置示例：

```text
collector_id
collector_name
workspace_id
platform_base_url
collector_token
enabled_adapters
poll_interval_seconds
queue_db_path
log_path
```

## 7. 前端交付范围

开发者管理员后台：

```text
不维护采集器和采集数据。
只维护用户、工作空间、面单模式和面单模板。
```

用户工作台：

```text
采集器连接入口
采集器在线状态
采集器最后心跳时间
采集器来源机器
采集器启用 / 停用
采集任务列表
原始采集记录列表
原始采集内容查看
采集错误查看
面单批次页显示来自采集器的批次
原始采集记录可进入后续字段定义流程
显示当前 workspace 下采集器状态摘要
```

## 8. 不在本阶段做的内容

```text
完整面单模板解析
完整字段提取规则引擎
报货汇总
Excel 三模式导出
图片嵌入 Excel
采集器自动升级
复杂远程控制
读取任何未经用户授权的本机敏感数据
```

## 9. 执行顺序

请按以下顺序推进：

```text
1. 调研菜鸟打印组件、抖店打印组件在业务机上的可观测输出方式。
2. 固化采集器配置文件格式。
3. 设计 PrintComponentAdapter 抽象。
4. 实现 collector identity。
5. 实现本地 SQLite 队列。
6. 实现 heartbeat。
7. 实现平台 collector 注册 / 心跳接口。
8. 实现 raw_capture_records 批量回传接口。
9. 实现通用文件监听适配器。
10. 实现菜鸟打印组件 adapter 骨架。
11. 实现抖店打印组件 adapter 骨架。
12. 用户工作台补齐采集连接和原始采集记录页面。
13. 用户工作台面单批次页接入采集记录入口。
14. 增加 collector 单元测试和后端接口测试。
15. 在一台本地 Windows 机器上做端到端联调。
16. 更新 README、进度报告和任务书索引。
```

## 10. 验收标准

本阶段完成时必须满足：

```text
1. 采集器可以在 Windows 用户机器上启动。
2. 采集器可以注册到平台。
3. 平台可以看到采集器在线状态。
4. 采集器可以发送心跳。
5. 采集器可以通过至少一个 adapter 生成 CaptureEvent。
6. 采集器断网时可以本地缓存。
7. 网络恢复后可以补传。
8. 平台可以保存 raw_capture_records。
9. raw_capture_records 按 workspace_id 隔离。
10. 用户工作台可以查看采集器和原始采集记录。
11. 用户工作台可以看到采集来源入口。
12. 不假设 raw_payload 一定是 JSON。
13. 不写死具体业务字段。
14. 不新增 shop_id / shops 核心模型。
15. 后端测试通过。
16. 采集器基础测试通过。
```

## 11. 风险与待确认

```text
1. 菜鸟打印组件和抖店打印组件是否提供稳定本地接口，需要实际业务机确认。
2. 如果组件只产生加密或私有缓存，需要寻找官方导出、日志或打印任务兜底方式。
3. 采集器需要明确用户授权范围，不能读取无关本机数据。
4. 多业务机同时采集时，需要 dedupe_key 避免重复记录。
5. 采集器本地队列需要考虑长期离线和磁盘占用。
```

## 12. 本阶段完成后的下一步

本阶段完成后，进入：

```text
采集记录
  ↓
面单模式识别
  ↓
面单模板解析
  ↓
生成标准化明细
  ↓
用户字段定义和关键字段配置
```

也就是从“采集器连接平台”推进到“采集数据自动进入面单读取和标准化流程”。

## 追加勘误：平台后台与租户端口边界

> 记录日期：2026-06-11  
> 原因：后续确认平台后台 UI 不能暴露给租户，采集相关页面也不能放入平台后台。

本任务书中出现的“用户工作台”在后续实现中拆分为：

```text
业务页面：查看采集记录、面单批次、异常处理和导出。
管理页面：维护采集连接、采集器绑定、字段定义、图片、档口和匹配规则。
```

平台后台 UI 只维护平台控制面数据，并使用独立私有端口，不承载采集器连接、采集任务和原始采集记录。

## 追加勘误：采集控制入口归属

> 记录日期：2026-06-11  
> 原因：进一步确认用户体验应由客户业务 UI 统一控制业务机采集器。

本阶段采集器交互口径修正为：

```text
采集器静默运行并连接服务器。
采集器绑定、连接配置、在线状态维护放在客户管理页面。
开始采集、结束采集放在客户业务页面。
一线人员点击开始采集后，正常使用菜鸟 / 抖店等打印组件打印订单。
打印结束后，一线人员点击结束采集。
采集器关闭本轮采集并回传原始打印 / 面单信息。
平台保存 raw_capture_records，并开始解析成客户可读面单信息。
后续再根据客户定义的字段、匹配规则、图片和档口资料生成最终 Excel 报货单。
```

边界说明：

```text
业务页面负责本轮采集控制和采集记录查看。
管理页面负责采集器连接、绑定、启停策略和状态维护。
平台后台不承载采集器连接、采集任务、原始采集记录或客户业务配置。
```

## 追加勘误：采集器注册、连接与账号关系

> 记录日期：2026-06-11  
> 原因：明确采集器的设备身份、员工账号、workspace 归属和采集任务之间的关系，避免后续把采集器做成员工账号登录。

核心原则：

```text
员工账号登录客户业务 UI / 客户管理 UI。
采集器不使用员工账号密码登录。
采集器使用设备身份连接服务器。
采集器注册成功后获得 collector_token。
collector_token 只代表某个 collector 设备身份，不代表某个员工账号。
collector 绑定到 tenant + workspace。
某次 capture_task / capture_session 记录由哪个用户点击开始采集。
raw_capture_records 由服务器根据 collector_token 解析出来的 collector/workspace/tenant 写入归属。
```

推荐绑定流程：

```text
客户管理员登录管理页面。
在当前 workspace 生成采集器激活码 / 绑定码。
业务机安装采集器。
采集器输入激活码 / 绑定码。
采集器向服务器注册。
服务器校验激活码并绑定 tenant_id + workspace_id + collector_id。
服务器返回 collector_token。
采集器本地保存 collector_token，后续静默连接、心跳、接收任务和上传原始数据。
```

推荐业务采集流程：

```text
员工账号登录业务页面。
员工点击开始采集。
服务器在当前 workspace 创建 capture_task / capture_session，并记录 started_by 用户。
服务器向该 workspace 下的采集器下发开始指令。
员工正常打印订单。
员工点击结束采集。
服务器关闭本轮任务，并记录 ended_by 用户。
采集器回传本轮 raw_payload。
服务器根据 collector_token 反查 collector 的 tenant_id / workspace_id。
服务器写入 raw_capture_records，不信任采集器自行传入的 workspace_id。
```

数据关系口径：

```text
collector 属于 workspace。
capture_task / capture_session 由 user 发起。
raw_capture_records 属于 collector + task/session + workspace。
采集器对应的是客户工作空间，不直接对应某个员工账号。
账号 A 点击开始采集，只能控制账号 A 当前 workspace 下绑定的采集器。
采集器回传的数据只能进入它已绑定的 workspace。
```

后端实现要求：

```text
采集器接口必须使用 collector_token 鉴权。
collector_token 应只保存哈希或等价安全凭据，不明文落库。
上传原始记录时，后端根据 collector_token 确定 tenant_id、workspace_id 和 collector_id。
后端必须拒绝 collector_token 与 capture_task workspace 不一致的上传。
后端必须记录 capture_task 的 started_by、ended_by 或等价审计字段。
激活码 / 绑定码必须有过期时间、使用次数限制和撤销能力。
采集器解绑或停用后，旧 collector_token 必须失效。
```
