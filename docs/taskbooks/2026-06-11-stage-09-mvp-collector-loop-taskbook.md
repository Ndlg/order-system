# 阶段 09：最小采集器身份、任务控制与原始记录回传闭环

> 日期：2026-06-11  
> 阶段状态：已完成最小版本  
> 阶段边界：只做可控模拟采集器，不接菜鸟、抖店真实打印组件

## 1. 阶段目标

本阶段目标是先跑通这一条最小闭环：

```text
客户管理页面生成采集器连接
  -> 采集器获得 collector_token
  -> 业务页面点击开始采集
  -> 后端创建 capture_task
  -> 采集器用 collector_token 心跳并发现任务
  -> 采集器上传模拟 raw_capture_records
  -> 业务页面点击结束采集
  -> 业务页面可查看本轮原始采集记录
```

本阶段不做：

```text
菜鸟打印组件真实读取
抖店打印组件真实读取
完整平台面单解析引擎
商品 / 图片 / 档口真实匹配
最终 Excel 报货单生成
```

## 2. 已完成后端能力

新增专用接口，避免用通用 CRUD 承载采集器协议：

```text
POST /api/v1/collector-control/register
GET  /api/v1/collector-control/status
POST /api/v1/collector-control/start
POST /api/v1/collector-control/stop

POST /api/v1/collector-runtime/heartbeat
POST /api/v1/collector-runtime/raw-records
```

身份边界：

```text
collector-control 使用员工 JWT。
collector-runtime 使用 X-Collector-Token。
采集器不使用员工账号密码。
collector_token 只代表采集器设备身份。
raw_capture_records 的 tenant_id / workspace_id 由后端根据 collector_token 写入。
后端不信任采集器自行传入 workspace_id。
```

数据表补齐：

```text
collectors.token_hash
collectors.is_enabled
capture_tasks.started_at
capture_tasks.ended_at
raw_capture_records.source_component
raw_capture_records.dedupe_key
raw_capture_records.captured_at
```

同时收紧：

```text
通用资源接口不返回 password_hash。
通用资源接口不返回 token_hash。
通用资源创建 / 更新不允许写 token_hash。
```

## 3. 已完成前端能力

客户管理页面：

```text
/admin/collector-connections
生成模拟采集器连接
显示采集器列表
显示 collector_token，一次性复制给本地模拟采集器
```

客户业务页面：

```text
/capture-records
显示采集器状态
点击开始采集 -> 创建 capture_task
点击结束采集 -> 关闭 capture_task
显示 raw_capture_records 列表
```

业务首页：

```text
新增采集控制入口
引导一线人员进入本轮采集控制
```

## 4. 已完成模拟采集器

文件：

```text
collector-client/client.py
collector-client/README.md
```

运行方式：

```powershell
python collector-client/client.py --base-url http://127.0.0.1:8000/api/v1 --token <collector_token>
```

模拟器行为：

```text
用 X-Collector-Token 心跳
读取 heartbeat 返回的当前采集任务
上传一条模拟 raw_payload
使用 dedupe_key 避免重复写入
```

## 5. 验证结果

```text
后端测试通过：4 passed, 1 warning。
前端 vue-tsc --noEmit 通过。
租户端 Vite build 通过。
平台后台 Vite build --config vite.server-admin.config.ts 通过。
```

## 6. 当前剩余风险

```text
还没有 Alembic 正式迁移。
collector_token 当前已按哈希保存，但还没有 token 轮换、吊销历史表和激活码表。
采集任务还没有独立 capture_session 表，当前复用 capture_tasks。
模拟器还没有本地离线队列。
raw_capture_records 还没有进入平台解析生成 standard_details。
```

## 7. 下一步建议

下一阶段建议进入：

```text
阶段 10：原始采集记录到客户可读面单信息的最小解析闭环
```

目标是先打通：

```text
raw_capture_records
  -> 平台共用解析逻辑
  -> standard_detail_batches
  -> standard_details.field_values
  -> 业务页面可预览客户可读面单信息
```
