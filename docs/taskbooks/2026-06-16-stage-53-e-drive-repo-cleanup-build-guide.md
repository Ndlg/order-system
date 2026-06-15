# 阶段 53：E 盘源码目录整理与构建说明

## 时间

2026-06-16（北京时间）

## 目标

```text
把 E 盘移动硬盘上的项目目录整理为干净源码目录。
保留 Git 仓库、源码、配置、测试和文档。
清理用户数据、本地依赖缓存、构建产物。
补充构建部署说明，方便后续提交 GitHub 或重新构建。
```

## 已清理

用户数据：

```text
storage 用户数据
local-dev.db
```

本地缓存和构建产物：

```text
.venv
.pytest_cache
frontend/node_modules
frontend/dist
frontend/dist-server-admin
__pycache__
```

## 已保留

```text
.git
backend
frontend
collector-client
scripts
docs
docker-compose.yml
docker-compose.site.yml
README.md
AGENTS.md
pytest.ini
.gitignore
.dockerignore
.env.example
```

空目录结构：

```text
storage/workspaces/.gitkeep
```

## 已新增文档

```text
docs/构建部署说明.md
```

文档内容包括：

```text
源码和用户数据边界
Docker 镜像 / 容器 / 数据卷含义
构建镜像命令
启动 / 停止现场服务命令
GitHub 提交流程
不应提交的本地缓存和用户数据
```

## GitHub 状态

```text
E 盘仓库保留 .git。
当前 git remote -v 没有输出，说明未配置远端或远端未保留在该目录。
后续推送 GitHub 前，需要确认新仓库 URL 并添加 origin。
```

## 未执行

```text
未在 E 盘构建 Docker 镜像。
未删除 C 盘现场 Docker 镜像。
未删除 C 盘现场 Docker 数据卷。
未停止 C 盘现场容器。
```

