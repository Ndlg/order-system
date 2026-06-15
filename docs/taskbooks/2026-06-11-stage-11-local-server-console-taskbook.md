# 阶段 11：本地服务器控制台

> 日期：2026-06-11  
> 状态：已完成最小版本  
> 阶段定位：降低新手本地部署和验收难度，把分散的后端、客户 UI、平台后台和采集器启动入口收拢到一个本地控制台。

## 一、问题背景

现阶段系统已经拆分出多个入口：

```text
后端 API：8000
客户业务/管理 UI：5173
平台服务端后台 UI：5174
本机采集器：collector-client/client.py
```

如果继续让新手分别记住多个 bat、端口和启动顺序，部署体验会很差，也不利于后续验收。

## 二、阶段目标

```text
提供一个本地服务器控制台。
支持一键启动客户系统。
支持启动全部服务。
支持查看服务状态和端口可访问状态。
支持打开常用页面。
支持启动本机采集器。
支持停止由控制台启动的服务。
集中保存日志和 PID 状态。
```

## 三、已实现内容

新增文件：

```text
scripts/server_console.py
scripts/server_console.bat
```

控制台功能：

```text
一键启动客户系统：后端 API + 客户 UI
启动全部：后端 API + 客户 UI + 平台后台 UI
查看服务状态：PID + 端口探测 + URL + 日志路径
打开客户业务页：http://127.0.0.1:5173
打开客户管理页：http://127.0.0.1:5173/admin
打开平台后台：http://127.0.0.1:5174/admin
启动本机采集器：输入 collector_token 后后台运行采集器
安装/更新依赖：后端 venv/pip + 前端 npm install
停止全部服务：停止控制台记录的服务 PID
```

日志目录：

```text
logs/server-console/
```

状态目录：

```text
storage/server-console/
```

## 四、命令入口

交互式控制台：

```powershell
scripts\server_console.bat
```

命令式入口：

```powershell
python scripts\server_console.py --start
python scripts\server_console.py --start-all
python scripts\server_console.py --status
python scripts\server_console.py --stop
python scripts\server_console.py --install
python scripts\server_console.py --collector-token <collector_token>
```

## 五、阶段边界

```text
当前控制台是本地开发/验收工具，不是生产环境进程守护系统。
生产部署后续仍应考虑 Windows 服务、Docker Compose 或正式进程管理器。
控制台只管理它自己启动过的 PID；如果服务由旧 bat 或其他工具启动，控制台可探测端口，但不会强行接管 PID。
```

## 六、验证记录

```text
python -m py_compile scripts/server_console.py 通过。
python scripts/server_console.py --status 可输出服务状态和常用地址。
控制台可识别当前 8000/5173/5174 端口状态。
```
