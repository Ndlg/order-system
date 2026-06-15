# 阶段 16：采集器可见客户端

> 阶段定位：采集器底层已经能登录、心跳、检测打印组件和回传 raw_capture_records，但客户侧缺少一个可以直接看到的客户端窗口。本阶段补齐业务机上的可见客户端入口。

## 1. 本阶段目标

```text
客户双击后能看到采集器窗口。
窗口能填写服务器地址、账号、密码、工作区和采集器名称。
窗口能执行登录并保存 token，本机不保存密码。
窗口能检查服务器心跳和本机打印组件状态。
窗口能启动 / 停止持续监听。
窗口能显示菜鸟 / 云打印 print.db 的 task_count 和 max_rowid。
窗口能显示实时日志，便于新手验收和排错。
窗口打开且已保存 token 时，应自动进入监听状态，避免客户只打开窗口但未实际采集。
Web UI 应区分“在线”和“监听中”，避免把单次检查心跳误认为采集器正在工作。
继续保持“开始采集 / 结束采集”由客户业务 UI 统一控制。
```

## 2. 已完成内容

新增文件：

```text
collector-client/gui.py
collector-client/collector_gui.bat
```

修改文件：

```text
collector-client/build_windows_exe.bat
collector-client/README.md
```

可视化客户端能力：

```text
读取默认配置 %LOCALAPPDATA%\OrderSystemCollector\collector-config.json。
复用现有账号密码登录接口 /collector-runtime/login。
登录成功后保存 collector_token，不保存密码。
复用现有 heartbeat 和 raw-records 上传逻辑。
复用现有本地 print.db adapter。
启动监听后持续心跳并等待服务器上的 active capture task。
停止监听后关闭本地循环，不改变服务器采集任务状态。
心跳增加 runtime_status，支持 checking / listening 区分。
客户管理页和采集记录页增加“监听中采集器”指标。
已保存 token 的窗口版客户端打开后自动开始监听。
```

## 3. 入口说明

开发阶段源码入口：

```bat
collector-client\collector_gui.bat
```

未来客户机优先使用打包产物：

```text
collector-client\dist\order-system-collector-ui.exe
```

命令行版本仍保留：

```text
collector-client\dist\order-system-collector.exe
```

## 4. 当前边界

```text
当前窗口是最小可见客户端，不是最终托盘程序。
暂未做开机自启动。
暂未做 Windows 服务安装。
暂未做断网本地 outbox 文件队列。
监听中不等于开始采集；开始 / 结束采集仍由客户业务 UI 控制。
```

## 5. 下一步建议

```text
1. 构建并验证 order-system-collector-ui.exe。
2. 增加开机自启动 / 托盘常驻。
3. 增加心跳超时离线判断。
4. 进入 raw_capture_records -> standard_details 的最小解析闭环。
```
