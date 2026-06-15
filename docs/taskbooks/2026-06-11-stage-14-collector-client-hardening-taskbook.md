# 阶段 14：采集器客户端可部署化收紧

> 阶段定位：根据“先做采集器”的调整，把采集器从开发脚本推进为更接近业务机可运行客户端的最小版本。

## 1. 本阶段目标

```text
采集器可以保存本地配置。
采集器可以用账号密码登录服务器，并按账号所属工作区自动绑定租户。
采集器可以保存本地采集水位。
采集器可以通过检查命令确认本机打印组件状态。
采集器心跳可以把本机组件状态保存到服务端。
采集器可以通过 bat 脚本进行配置、启动和检查。
为后续 Windows exe 打包预留入口。
```

## 2. 已完成内容

### 2.1 采集器配置文件

新增默认配置位置：

```text
%LOCALAPPDATA%\OrderSystemCollector\collector-config.json
```

新增示例：

```text
collector-client/config.example.json
```

配置内容包括：

```text
base_url
collector_token
username
workspace_id
collector_id
collector_name
interval
batch_size
simulate
adapters
```

### 2.1.1 账号登录绑定

本轮按产品口径调整为：

```text
采集器自身输入账号密码登录服务器。
服务器根据账号所属 workspace 绑定 collector。
collector 自动写入 tenant_id + workspace_id。
服务器返回 collector_token。
采集器本地保存 collector_token，但不保存密码。
后续心跳和上传继续使用 collector_token。
```

如果账号只有一个工作区，采集器可以不传 workspace_id。
如果账号有多个工作区，采集器配置时必须传 workspace_id。

### 2.2 采集器持久状态

新增默认状态文件：

```text
%LOCALAPPDATA%\OrderSystemCollector\collector-state.json
```

状态内容包括：

```text
idle_watermarks
capture_watermarks
```

这让采集器不再完全依赖进程内存保存水位，重启后可以继续保留已知边界。

### 2.3 采集器日志

新增默认日志：

```text
%LOCALAPPDATA%\OrderSystemCollector\collector.log
```

### 2.4 采集器命令

当前支持：

```text
--save-config  保存配置
--check        检查本机组件和服务器心跳
--loop         持续运行采集
--simulate     模拟上传，不读本地 print.db
```

### 2.5 Windows bat 入口

新增：

```text
collector-client/collector_configure.bat
collector-client/collector_start.bat
collector-client/collector_check.bat
collector-client/build_windows_exe.bat
```

用途：

```text
collector_configure.bat：输入服务器地址、账号、密码和可选 workspace_id，自动登录并保存 token。
collector_start.bat：按已保存配置启动采集器。
collector_check.bat：检查本机组件和服务器连接。
build_windows_exe.bat：开发机打包单文件 Windows exe。
```

### 2.6 服务端心跳状态保存

新增 `collectors.status_payload`。

采集器 heartbeat 上报：

```text
adapter_status
queue_size
last_error
received_at
```

服务端保存后，后续客户管理页面可以展示每台业务机是否检测到菜鸟 / 云打印组件，以及组件状态是 ready、missing 还是 error。

## 3. 验证记录

本机组件检查：

```text
cainiao-cnprint: ready, task_count=32, max_rowid=32
cloud-print-client: ready, task_count=1, max_rowid=1
```

代码验证：

```text
python -m py_compile collector-client/client.py 通过
collector-client/client.py --check 通过
collector-client/collector_check.bat 通过
后端容器 pytest -q 通过：4 passed, 1 warning
使用真实 collector_token 验证 --save-config --check 通过
使用账号密码验证 --login --save-config --check 通过
```

端到端验证：

```text
通过账号密码登录临时采集器。
启动一轮采集任务。
采集器使用 --simulate 心跳并发现 active task。
采集器上传 1 条 mvp-simulator raw_capture_record。
停止采集任务。
```

## 4. 当前仍未完成

```text
正式 Windows exe 产物尚未构建和验收。
采集器尚未做开机自启动 / Windows 服务安装。
采集器尚未做图形化托盘状态。
采集器已经支持账号密码登录绑定租户 / 工作区。
当前账号密码只在配置时输入并用于换取 token，配置文件不保存密码。
后续如需更强安全体验，可再升级为一次性激活码或二维码绑定。
客户管理页尚未展示 status_payload 中的本机组件状态。
断网期间没有单独 outbox 文件，但上传失败不会推进水位，恢复后可重试；服务端 dedupe_key 兜底。
```

## 5. 下一步建议

```text
1. 在客户管理页展示采集器 status_payload，方便用户判断业务机连接和打印组件状态。
2. 构建并验证 order-system-collector.exe。
3. 做 Windows 开机自启动或服务安装脚本。
4. 再进入 raw_capture_records -> standard_details 的最小业务解析闭环。
```
