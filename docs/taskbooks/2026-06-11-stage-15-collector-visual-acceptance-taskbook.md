# 阶段 15：采集器连接状态与采集回传可视化验收

> 阶段定位：采集器底层连接、任务发现和回传已经具备最小能力，本阶段把这些状态展示到客户管理页和客户业务页，让客户可以直接验收。

## 1. 本阶段目标

```text
客户管理页能看到哪些业务机采集器已连接。
客户管理页能看到采集器是否在线、最后心跳、设备标识、来源机器。
客户管理页能看到采集器检测到的本机打印组件状态。
客户业务页能看到本轮采集任务状态和回传条数。
客户业务页能看到最近采集任务和原始回传记录。
原始记录可以展开查看 raw_payload，方便验证采集器确实有回传。
```

## 2. 已完成内容

### 2.1 客户管理页采集连接

页面：

```text
http://127.0.0.1:5173/admin/collector-connections
```

新增展示：

```text
已连接业务机数量
在线采集器数量
ready 打印组件数量
绑定方式：账号
采集器列表
采集器展开行
打印组件 adapter_status
```

采集器展开后可看到：

```text
最后状态上报时间
本地队列 queue_size
最近错误 last_error
Cainiao CNPrintClient 状态
CloudPrintClient 状态
print.db 路径
task_count
max_rowid
```

### 2.2 客户业务页采集记录

页面：

```text
http://127.0.0.1:5173/capture-records
```

新增展示：

```text
本轮状态
在线采集器数量
本轮回传条数
累计原始记录
当前 active task 摘要
最近采集任务
每个任务回传条数
原始采集记录表
raw_payload 展开查看
```

### 2.3 前端类型

`CollectorRecord` 新增：

```text
status_payload.adapter_status
status_payload.queue_size
status_payload.last_error
status_payload.received_at
```

用于展示采集器上报的本机组件状态。

## 3. 验证记录

构建与测试：

```text
tenant-ui Docker build 通过。
后端 pytest -q 通过：4 passed, 1 warning。
后端 health 返回 200。
客户业务页 / 客户管理页返回 200。
```

浏览器验收：

```text
客户管理页显示 1 台本机采集器 online。
客户管理页显示 ready 打印组件数量为 2。
展开本机采集器后，可看到：
  Cainiao CNPrintClient ready，task_count=32，max_rowid=32。
  CloudPrintClient ready，task_count=1，max_rowid=1。
客户业务页显示在线采集器 1。
点击开始采集后页面进入“采集中”。
采集器模拟上传 1 条 raw_capture_record。
客户业务页显示本轮回传 1 条。
原始记录表显示 mvp-simulator 记录。
点击结束采集后任务状态变为 completed。
```

## 4. 当前边界

```text
当前可视化展示的是 raw_capture_records 原始数据。
raw_payload 仍是原始 JSON，不是客户可读面单字段。
采集器状态在线/离线目前依赖心跳写入 online_status，尚未做超时自动置 offline。
页面暂未提供采集器解绑、停用、重命名等管理操作。
```

## 5. 下一步建议

```text
1. 做采集器 Windows exe 打包和业务机运行方式验收。
2. 做心跳超时离线判断。
3. 做 raw_capture_records -> standard_details 的最小解析闭环。
4. 在业务页把 raw JSON 整理成客户可读面单信息。
```
