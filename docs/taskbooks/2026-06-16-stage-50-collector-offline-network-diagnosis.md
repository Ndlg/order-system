# 阶段 50：采集器掉线与心跳时间显示排查

## 时间

2026-06-16 02:22（北京时间）

## 现场现象

采集连接页显示三台业务机采集器掉线，最后心跳时间显示为原始 UTC ISO 字符串，例如：

```text
2026-06-15T08:52:37.885519+00:00
```

该时间换算为北京时间为：

```text
2026-06-15 16:52:37
```

## 排查结果

服务器侧：

```text
order-system-backend Up 6 hours
order-system-tenant-ui Up
http://127.0.0.1:8000/ -> 200
http://127.0.0.1:5173/ -> 200
```

数据库中三台业务机最后心跳均停留在 2026-06-15 16:52 左右（北京时间）：

```text
左边  2026-06-15T08:52:37+00:00
中间  2026-06-15T08:52:35+00:00
右边  2026-06-15T08:52:35+00:00
```

业务机进程：

```text
左边  订单系统采集器.exe 仍在运行
中间  订单系统采集器.exe 仍在运行
右边  订单系统采集器.exe 仍在运行
```

业务机本地日志：

```text
collector network error: <urlopen error timed out>
```

业务机到服务器连通性：

```text
ping <SERVER_IP> 正常
TCP <SERVER_IP>:5173 TIMEOUT
```

结论：

```text
不是后端挂掉。
不是 token 失效。
不是采集器进程退出。
是业务机到服务器 <SERVER_IP> 的 TCP 入站方向被挡住，采集器无法访问 http://<SERVER_IP>:5173/api/v1。
当前 Codex shell 无管理员权限，无法直接添加 Windows 防火墙规则。
```

## 已完成修正

前端时间显示修正：

```text
采集连接页：最后心跳、最后状态上报改为本地时间格式。
采集记录页：最后心跳、当前任务开始时间改为本地时间格式。
```

验证：

```text
frontend vue-tsc --noEmit：通过
frontend vite build：通过
tenant-ui 已重建并重启
http://127.0.0.1:5173/ -> 200
```

## 需要管理员权限执行的恢复动作

在服务器本机用“管理员 PowerShell”执行：

```powershell
New-NetFirewallRule -DisplayName "Order System Tenant UI 5173" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5173 -Profile Any
```

执行后，业务机采集器当前仍在循环重连，通常 10-20 秒内会恢复心跳。

