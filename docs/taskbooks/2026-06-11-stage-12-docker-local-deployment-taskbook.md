# 阶段 12：Docker 本地部署入口

> 日期：2026-06-11  
> 状态：已完成最小版本  
> 阶段定位：让非开发用户本机只依赖 Docker Desktop 启动系统服务，避免手动部署 Python、Node、npm、pip 等开发环境。

## 一、问题背景

本地服务器控制台虽然可以集中启动服务，但首次运行仍会创建 Python 虚拟环境并安装后端依赖，同时前端仍依赖 npm。对不熟悉开发环境的用户来说，这不是理想部署方式。

## 二、阶段目标

```text
使用 Docker 启动后端、客户 UI 和平台后台 UI。
本机只要求安装 Docker Desktop。
后端容器内运行 FastAPI。
前端容器内构建 Vue，并通过 Nginx 提供静态页面。
Nginx 将 /api 代理到后端容器。
默认使用容器数据卷中的 SQLite，自动建表和初始化默认账号。
```

## 三、已实现内容

新增文件：

```text
.dockerignore
docker-compose.yml
backend/Dockerfile
frontend/Dockerfile
frontend/docker/nginx.conf.template
scripts/docker_console.bat
scripts/docker_start.bat
scripts/docker_stop.bat
scripts/docker_status.bat
scripts/docker_logs.bat
```

容器服务：

```text
backend：FastAPI，暴露 8000
tenant-ui：客户业务/管理 UI，暴露 5173
platform-admin-ui：平台后台 UI，暴露 5174
```

默认地址：

```text
客户业务页：http://127.0.0.1:5173
客户管理页：http://127.0.0.1:5173/admin
平台后台：http://127.0.0.1:5174/admin
后端接口文档：http://127.0.0.1:8000/docs
```

默认账号：

```text
用户名：admin
密码：admin123
```

## 四、使用方式

纯 Docker 菜单：

```powershell
scripts\docker_console.bat
```

一键启动：

```powershell
scripts\docker_start.bat
```

命令行：

```powershell
docker compose up -d --build
docker compose ps
docker compose logs -f
docker compose down
```

## 五、边界说明

```text
Docker 入口用于启动服务器和 Web UI。
本机采集器需要读取 Windows 打印组件的本地 print.db，仍应作为 Windows 本机程序运行。
后续建议把采集器打包为 exe，避免业务机安装 Python。
生产部署时应替换 SECRET_KEY，并按生产方案切换 MySQL/Redis/正式数据卷和备份策略。
```

## 六、验证记录

```text
docker compose config 通过。
Docker 启动脚本为纯 bat，不依赖本机 Python/Node。
前端容器构建时在容器内执行 npm ci 和 npm run build。
后端容器启动时使用 AUTO_CREATE_TABLES=true 自动初始化 SQLite。
```
