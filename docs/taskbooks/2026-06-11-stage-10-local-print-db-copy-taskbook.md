# 阶段 10：本地打印组件任务库复制采集器

> 日期：2026-06-11  
> 状态：已完成最小版本  
> 阶段定位：把前一阶段的模拟采集器推进为真实业务机最小采集器。采集器只复制原始打印任务数据，平台后端再做解析和业务含义整理。

## 一、阶段结论

本阶段已通过本机只读排查确认，菜鸟打印组件和云打印客户端都会把打印任务写入本地 SQLite 数据库。

```text
菜鸟打印组件：
C:\Program Files (x86)\CNPrintTool\resources\print.db

云打印客户端：
C:\Program Files (x86)\CloudPrintClient\resources\print.db
```

两个数据库均存在相同的基础表：

```text
task(taskID, msg, time)
document(documentID, taskID, retVal, retMsg)
upload(...)
```

其中 `task.msg` 是平台需要采集的核心原始数据。采集器当前不负责解释字段含义，只负责把新增 `msg` 原样复制到系统。

## 二、产品边界

### 采集器负责

```text
识别本机打印组件
读取本机 print.db 中新增的 task 记录
按采集任务水位过滤历史数据
生成 source_component、source_index、dedupe_key
上传完整 raw_payload 到 raw_capture_records
维持 collector_token 心跳和设备状态
```

### 采集器不负责

```text
不定义店铺、商品、规格、档口等业务概念
不在业务机解析客户字段含义
不在业务机做商品匹配、图片匹配或 Excel 汇总
不解密加密字段
不替代平台面单解析规则
```

### 平台后端负责

```text
保存 raw_capture_records
根据 source_component 和原始 JSON 解析成客户可读的面单信息
把解析结果交给客户自定义字段、关键字段、商品图片、档口和导出规则
生成最终 Excel 报货单
```

## 三、采集水位规则

为避免打印组件长期不重启导致历史任务重复进入下一轮采集，采集器必须使用水位机制。

```text
无采集任务时：
采集器持续记录每个组件 task 表当前最大 rowid，作为空闲水位。

首次发现平台返回 active capture task 时：
采集器以该组件最近一次空闲水位作为本轮 start_rowid。
如果采集器是在采集任务开始后才启动，退化为使用当前最大 rowid，避免上传历史数据。

采集中：
只读取 rowid > 本轮已上传水位的记录。

上传成功后：
把本轮已上传水位推进到成功上传的最大 rowid。

服务端：
继续用 collector_id + source_component + taskID + msg hash 做去重兜底。
```

## 四、本机验证记录

### 菜鸟打印组件

```text
进程：CNPrintClient.exe
路径：C:\Program Files (x86)\CNPrintTool
端口：13528 WebSocket，13529 Secure WebSocket，13530/13531 文件服务
任务库：resources\print.db
task.msg：完整 JSON
常见结构：cmd / requestID / version / task
task.documents[].contents[]：addData / encryptedData / templateURL / printXML
```

补充观察：

```text
不同面单打印后，协议结构保持一致。
templateURL/ver 基础指纹可保持一致，但 encryptedData、printXML 和 addData 字段会变化。
recipient.phone 等字段可能缺失，后续解析器必须按可选字段处理。
```

### 云打印客户端

```text
进程：CloudPrintClient.exe
路径：C:\Program Files (x86)\CloudPrintClient
端口：13888 WebSocket，13898/13999 辅助端口
任务库：resources\print.db
task.msg：完整 JSON
常见结构：cmd / isOpen / previewType / requestID / task / version
task.documents[].contents[]：encryptedData / params / signature / templateURL / data
```

补充观察：

```text
实际打印后 task 表从空变为 1 条。
data 中已经存在 orderId、trackNo、shopName、productInfo、productShortInfo、productCount 等可读字段。
采集器仍然只复制原始 msg，不在本地解释这些字段。
```

## 五、阶段任务

### P0：最小真实采集闭环

```text
[x] 确认菜鸟打印组件本地任务库路径和表结构
[x] 确认云打印客户端本地任务库路径和表结构
[x] 采集器新增本地 SQLite adapter
[x] 采集器心跳上报 adapter 状态
[x] 采集器按空闲水位和采集中水位读取新增 task
[x] 采集器上传 raw_payload 到 /collector-runtime/raw-records
[x] 采集器保留模拟模式，便于无打印组件环境验证
[x] 更新采集器 README
[x] 完成语法验证
```

### P1：增强但不阻塞本阶段

```text
[ ] 本地持久化 outbox，支持断网后恢复补传
[ ] 更精确的结束采集边界，服务端可返回 recently_completed task 和 ended_at
[ ] 自动识别更多安装路径或多版本组件
[ ] 对本地数据库读取失败、锁定、损坏做更完整告警
```

## 六、验收标准

```text
业务 UI 点击开始采集后，采集器能发现 active task。
用户打印菜鸟或云打印订单后，采集器只上传本轮新增 task.msg。
下一轮采集不会重复上传上一轮任务。
raw_capture_records 中保留 source_component、source_index、dedupe_key 和完整 raw_payload。
无打印组件环境下，采集器能通过 adapter_status 告知 missing，不影响心跳。
```

## 八、实现记录

已实现文件：

```text
collector-client/client.py
collector-client/README.md
```

实现要点：

```text
默认扫描菜鸟和云打印两个本地 print.db。
通过只读 SQLite 连接读取 task 表。
无 active capture task 时持续更新 idle watermark。
发现 active capture task 后只读取 rowid > watermark 的新增任务。
上传 raw_payload 时保留 source_component、source_index、source_columns 和 dedupe_key。
保留 --simulate 模式，便于没有真实打印组件时验证 collector_token、heartbeat 和 raw-records。
```

验证记录：

```text
python -m py_compile collector-client/client.py 通过。
本机只读 adapter 检查通过：
cainiao-cnprint task_count=32 max_rowid=32
cloud-print-client task_count=1 max_rowid=1
```

## 七、后续阶段建议

阶段 10 完成后，下一步进入：

```text
raw_capture_records -> 标准面单信息 standard_details 的最小解析闭环
```

解析器优先支持：

```text
菜鸟 printXML / addData 的可读字段抽取
云打印 contents[].data 的可读字段抽取
保留解析失败记录和原始 payload 追溯能力
```
