# 阶段 13：框架健康检查与业务闭环启动判断

> 阶段定位：在进入完整业务流程前，对当前平台框架、部署入口、权限边界、三端页面分工和采集链路基础能力做一次收口检查。

## 1. 本阶段目标

```text
确认当前框架是否已经具备继续推进业务闭环的基础。
确认三端页面分工没有重新混淆。
确认 Docker 本地部署可以作为新手验收入口。
确认多租户 / 多工作区数据边界仍然成立。
确认下一步应该直接全量推进，还是先做最小业务模拟闭环。
```

## 2. 已检查内容

### 2.1 Docker 服务

当前 Docker 服务可以正常启动：

```text
backend
redis
tenant-ui
platform-admin-ui
```

当前本地访问入口：

```text
客户业务页面：http://127.0.0.1:5173
客户管理页面：http://127.0.0.1:5173/admin
平台后台页面：http://127.0.0.1:5174/admin
后端接口文档：http://127.0.0.1:8000/docs
```

本阶段已将 Docker 本地部署端口收紧为只绑定 `127.0.0.1`：

```text
127.0.0.1:8000 -> backend
127.0.0.1:5173 -> tenant-ui
127.0.0.1:5174 -> platform-admin-ui
```

这符合“平台后台 UI 不应在客户网络中裸露”的当前本地部署原则。

### 2.2 后端验证

后端容器内测试已通过：

```text
4 passed, 1 warning
```

测试覆盖当前关键边界：

```text
登录和当前用户解析
workspace 数据隔离
平台全局 waybill_modes 不带 tenant_id / workspace_id
客户业务数据自动写入 tenant_id / workspace_id
collector_token 绑定 collector / tenant / workspace
raw_capture_records 归属由服务器根据 collector_token 写入
```

本阶段已补充后端 Docker 镜像环境变量：

```text
PYTHONPATH=/app/backend
```

目的是让容器内直接执行 `pytest -q` 也能稳定找到 `app` 包。

### 2.3 前端三端分工

当前三端入口仍然保持清晰：

```text
5173 /       客户业务页面
5173 /admin  客户管理页面
5174 /admin  平台后台页面
```

页面职责仍然按当前项目口径划分：

```text
客户业务页面：
开始采集、结束采集、查看采集记录、后续导出报货单。

客户管理页面：
采集器连接、字段定义、关键字段、图片、档口、匹配规则。

平台后台页面：
客户 / 租户、工作区、用户、平台共用面单解析模式 / 解析模板 / 模板字段。
不维护客户业务数据。
```

本阶段补充 `frontend/.dockerignore`，避免 Docker 构建前端时把 `node_modules`、`dist`、`dist-server-admin` 一起带入构建上下文。

### 2.4 当前已知噪音

后端日志中观察到有旧地址持续请求：

```text
POST /api/waybill/agent/poll -> 404
```

仓库当前代码已不再使用该地址，现有采集器使用：

```text
POST /api/v1/collector-runtime/heartbeat
POST /api/v1/collector-runtime/raw-records
```

判断：这更像是本机某个旧页面、旧进程或外部工具仍在请求旧接口。它不阻断当前框架，但正式演示前应清理旧请求来源，避免日志噪音影响判断。

## 3. 当前框架判断

框架层面可以继续推进。

目前已经具备：

```text
统一后端 API
单平台数据库 + 多租户逻辑隔离
tenant_id + workspace_id 数据归属
客户业务 UI / 客户管理 UI / 平台后台 UI 三端分离
平台共用解析规则表
采集器注册、token、心跳、任务控制和原始记录回传
本地打印组件 print.db 复制采集器最小能力
Docker 本地部署入口
```

目前还没有完成：

```text
raw_capture_records -> standard_details 的真实解析闭环
客户看到的标准面单信息页面
客户字段定义与解析字段的联动
商品 / 图片 / 档口匹配闭环
Excel 报货单生成
平台后台解析规则的可视化配置器
采集器 Windows exe 打包与自启动
```

## 4. 下一步建议

不建议马上一次性做完整业务系统。

建议先做“最小业务模拟闭环”，原因：

```text
当前最核心风险不是页面数量，而是数据链路是否完整。
需要先让一条原始采集记录完整走到标准面单信息，再走到匹配和 Excel。
一旦最小闭环成立，后续页面和规则都可以围绕真实数据继续扩展。
```

推荐下一阶段目标：

```text
阶段 14：最小业务模拟闭环
```

范围建议：

```text
1. 允许用一条模拟 raw_payload 或已采集 raw_capture_records 作为输入。
2. 后端实现最小 parser，把 raw_payload 解析成 standard_details.field_values。
3. 客户业务页面显示标准面单信息。
4. 客户管理页面可以把解析出的字段标记为关键字段。
5. 用最小匹配规则匹配一个商品图片 / 档口。
6. 生成一个最小 Excel 报货单。
```

验收标准：

```text
用户可以登录客户业务页面。
点击开始采集或使用模拟采集。
系统产生 raw_capture_records。
系统解析生成 standard_details。
客户能看到整理后的面单信息，而不是杂乱 JSON。
客户能定义最小关键字段。
系统按关键字段生成一份最小 Excel 报货单。
```

## 5. 阶段结论

```text
当前平台框架可继续推进。
数据库和租户边界基本成立。
三端 UI 分工基本成立。
Docker 本地部署入口可用于验收。
下一步应优先做最小业务模拟闭环，而不是直接铺完整功能。
```
