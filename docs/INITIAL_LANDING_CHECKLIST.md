# 初期落地使用清单

更新时间：2026-06-14

这份清单用于项目进入店铺现场试运行前的收口。目标不是把所有高级能力一次做完，而是保证当前已经能跑通的链路稳定、目录干净、数据可备份、问题可追踪。

## 当前可落地链路

```text
商品 / SKU / SKU 图片维护
-> 我打模板字段定义
-> 商品主类识别规则
-> SKU 自动匹配
-> 监听批次采集
-> 异常检查
-> 报货 Excel 预览和下载
```

当前重点支持我打 / 菜鸟 woda 打印平台链路。抖店和菜鸟直打可以进入同一个识别和导出出口，但现场第一轮应先用最常见业务流程压测。

## 本次目录整理

已创建源码备份：

```text
<BACKUP_DIR>\order-system-source-20260614-035947.zip
<BACKUP_DIR>\order-system-working-diff-20260614-035947.patch
<BACKUP_DIR>\order-system-untracked-files-20260614-035947.txt
<BACKUP_DIR>\order-system-backup-manifest-20260614-035947.txt
```

已清理本地可再生成目录：

```text
.pytest_cache/
backend/**/__pycache__/
collector-client/__pycache__/
collector-client/dist/
frontend/dist/
frontend/dist-server-admin/
logs/
storage/collector-build/
storage/collector-test/
storage/server-console/
storage/sku-import-preview/
迁移根目录下误留的空 frontend/
```

已补充 `.gitignore`，避免采集器包、临时预览、服务台缓存继续污染源码目录。

## 目录边界

需要保留并纳入源码管理：

```text
backend/
collector-client/
docs/
frontend/docker/
frontend/src/
scripts/
storage/parser-samples/
storage/workspaces/.gitkeep
docker-compose.yml
README.md
pytest.ini
```

不要纳入源码管理：

```text
.venv/
frontend/node_modules/
frontend/dist/
frontend/dist-server-admin/
collector-client/dist/
logs/
local-dev.db
storage/workspaces/*
storage/collector-build/
storage/collector-test/
storage/server-console/
storage/sku-import-preview/
```

说明：`frontend/node_modules/` 和 `.venv/` 是开发依赖目录，当前未清理，避免继续开发时反复安装。只要做 Docker 部署，它们不是运行必需品。

## 现场启动

推荐使用 Docker：

```powershell
docker compose up -d --build backend tenant-ui platform-admin-ui
```

端口边界：

```text
5173：租户端和业务现场使用入口，可绑定 0.0.0.0。
5174：平台后台，只给本机或内网管理员使用。
8000：后端 API，默认只绑定 127.0.0.1，不建议直接暴露给公网或业务网段。
```

采集器服务地址只填写服务器 IP：

```text
服务器IP
```

采集器会自动补齐为 `http://服务器IP:5173/api/v1`。原因：5173 前端容器已经代理 `/api/v1` 到后端，业务机不需要直接访问 8000。只有在明确配置了内网防火墙和鉴权边界时，才考虑让采集器直连 `http://服务器IP:8000/api/v1`。

## 采集器交付

现场业务电脑只交付最小可运行 exe，不交付 Python 源码、开发 bat 或命令行程序。

当前 exe 输出位置：

```text
collector-client/dist/order-system-collector.exe
```

平台下载接口会优先打包这个 exe，下载包内容应只有：

```text
order-system-collector.exe
README.md
config.example.json
使用说明.txt
```

采集器窗口只保留现场需要的信息：

```text
服务器IP
账号 / 密码
设备名称
工作区ID
采集器状态
服务器状态
登录状态
本机打印组件状态
运行日志
```

不在现场窗口展示设备 ID、模拟模式、源码路径、复杂命令行参数和开发调试按钮。

## 数据备份

源码备份不等于业务数据备份。现场试运行前后都要单独备份 Docker 数据卷。

当前 Docker 数据在命名卷中：

```text
order-system-data
```

其中至少包含：

```text
/data/order-system.db
/data/workspaces/
```

建议每次现场测试前先备份：

```powershell
$ts = Get-Date -Format 'yyyyMMdd-HHmmss'
docker cp order-system-backend:/data/order-system.db "<BACKUP_DIR>\order-system-db-$ts.db"
docker cp order-system-backend:/data/workspaces "<BACKUP_DIR>\order-system-workspaces-$ts"
```

清空业务数据前必须确认已备份。不要只备份代码。

## 现场验收顺序

1. 登录租户端，确认账号、工作区、页面入口正常。
2. 在商品/SKU 页面新建商品，上传或手动补齐 SKU 图片。
3. 在打印模板规则页面选择一批真实面单，定义商品文字、销售属性1、销售属性2、数量字段。
4. 在商品识别页面建立商品主类规则，SKU 尽量让系统按销售属性自动匹配。
5. 启动采集器，开始监听，打印一小批真实面单。
6. 结束监听后检查批次数量、已识别商品、异常列表。
7. 在导出中心选择该批次，检查 SKU 图片、销售属性2排序、数量。
8. 下载 Excel，和人工报货表对照。
9. 记录未识别、错识别、无图、数量异常四类问题。

## 当前已知限制

这些不是本轮阻塞项，但需要保留记录：

```text
1. 模板识别主要依赖 printXML 版式指纹，同版式不同字段布局极端变化时仍需人工验证。
2. 备注商品暂时不做特殊自动判断，应由用户在商品识别规则中指定备注字段参与识别或兜底。
3. SKU 图片缺失不应阻断导出，只在 Excel 中留空或进入低级别异常提示。
4. 销售属性1 / 销售属性2堆叠是报货表版式设置，不应影响前面的商品识别结果。
5. 删除模板后，规则必须继续依靠稳定版式指纹匹配，不能只依赖数据库 ID。
6. 业务现场不要直接清空 Docker volume，必须先备份数据库和 workspaces 文件。
```

## 继续开发前注意

```text
1. 不要再新增临时页面来解决正式流程问题，优先收口到现有入口。
2. 导出 Excel 以后只认统一五列表头：商品名称、销售属性1、SKU图片、销售属性2、数量。
3. 商品识别只负责识别商品主类和 SKU，导出版式只负责展示和汇总。
4. 复杂配置要有默认预设，用户可以改，但不能要求用户从零理解所有参数。
5. 每次现场改动后至少跑后端识别/导出测试，再重建 Docker。
```
