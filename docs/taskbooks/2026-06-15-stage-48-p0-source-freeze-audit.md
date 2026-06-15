# 阶段 48 P0：源码冻结与工作树审计记录

> 审计时间：2026-06-15  
> 审计目标：确认当前现场 Alpha 运行基线，按模块分类工作树变更，给后续拆分提交和清理运行垃圾提供依据。

## 当前运行基线

当前运行源码目录：

```text
<PROJECT_DIR>
```

Docker Compose 项目：

```text
order-system
```

当前服务：

```text
backend             order-system-backend:latest             127.0.0.1:8000->8000
tenant-ui           order-system-tenant-ui:latest           0.0.0.0:5173->80
platform-admin-ui   order-system-platform-admin-ui:latest   127.0.0.1:5174->80
redis               redis:7-alpine                                internal
```

当前数据卷：

```text
order-system-data
```

数据库文件：

```text
/data/order-system.db
```

数据库大小：

```text
约 14MB
```

当前数据卷内已存在备份参考：

```text
/data/order-system-backup-for-migration.db
```

## 工作树统计

当前 `git status --porcelain` 统计：

```text
修改：44
删除：12
未跟踪：34
```

按模块粗分：

```text
backend：24 项
frontend：30 项
collector-client：10 项
docs：13 项
storage：8 项
compose/scripts/root：4 项
```

> 注：带中文文件名的 storage 路径在 git porcelain 输出中会被引号转义，统计时已按 storage 归类。

## 后端变更包

核心修改：

```text
backend/Dockerfile
backend/app/api/router.py
backend/app/api/routes/collector_runtime.py
backend/app/api/routes/product_assets.py
backend/app/api/routes/resources.py
backend/app/core/database.py
backend/app/engines/matching.py
backend/app/models/entities.py
backend/app/repositories/base.py
backend/app/services/bootstrap.py
backend/app/services/waybill_parser.py
backend/tests/test_foundation.py
scripts/init_db.sql
```

新增核心文件：

```text
backend/app/api/routes/platform_accounts.py
backend/app/services/product_recognition.py
backend/app/services/woda_fields.py
backend/app/services/woda_printxml_parser.py
backend/app/services/woda_template_matcher.py
backend/tests/test_collector_client_runtime.py
backend/tests/test_direct_print_standardization.py
backend/tests/test_multi_item_export_rows.py
backend/tests/test_product_recognition.py
backend/tests/test_recognition_report_export.py
backend/tests/test_woda_printxml_parser.py
backend/tests/test_woda_template_config.py
```

建议拆分提交：

```text
1. 平台/客户账号与路由。
2. 采集器运行时、心跳清理、采集器下载。
3. 我打 printXML 解析与模板匹配。
4. 商品/SKU 识别引擎。
5. 档口、图片和报货导出模型/接口。
6. 数据库补列和 init SQL。
```

## 前端变更包

核心修改：

```text
frontend/docker/nginx.conf.template
frontend/src/layouts/AppShell.vue
frontend/src/layouts/ClientAdminLayout.vue
frontend/src/layouts/ServerAdminLayout.vue
frontend/src/router/clientAdminRoutes.ts
frontend/src/router/serverAdminIndex.ts
frontend/src/router/serverAdminRoutes.ts
frontend/src/router/tenantRedirects.ts
frontend/src/services/api.ts
frontend/src/styles/base.css
frontend/src/views/client-admin/ClientAdminHomeView.vue
frontend/src/views/server-admin/ServerAdminDashboardView.vue
frontend/src/views/workbench/CaptureRecordsView.vue
frontend/src/views/workbench/CollectorConnectionsView.vue
frontend/src/views/workbench/ExceptionsView.vue
frontend/src/views/workbench/ExportCenterView.vue
frontend/src/views/workbench/ExportHeaderDefinitionView.vue
frontend/src/views/workbench/MatchingReviewView.vue
frontend/src/views/workbench/PrintTemplateRulesView.vue
frontend/src/views/workbench/ProductCatalogView.vue
frontend/src/views/workbench/WaybillBatchesView.vue
frontend/src/views/workbench/waybillFieldCatalog.ts
```

新增核心文件：

```text
frontend/src/views/server-admin/CustomerAccountsView.vue
frontend/src/views/workbench/StallCatalogView.vue
frontend/src/views/workbench/printTemplateRuleMapping.ts
frontend/src/views/workbench/productRecognitionRulePayload.ts
frontend/src/views/workbench/reportExportLayout.ts
frontend/src/views/workbench/wodaFields.ts
frontend/src/views/workbench/wodaStructure.ts
```

删除项：

```text
frontend/src/views/server-admin/ServerAdminResourceView.vue
```

建议拆分提交：

```text
1. 管理后台导航和客户账号页。
2. 客户工作台：采集连接、模板规则、商品识别。
3. 商品/SKU、档口库、图片维护。
4. 报货导出中心与导出表头版式管理。
5. 全局样式和布局收紧。
```

## 采集器变更包

核心修改：

```text
collector-client/README.md
collector-client/build_windows_exe.bat
collector-client/client.py
collector-client/config.example.json
```

删除旧入口：

```text
collector-client/collector_check.bat
collector-client/collector_configure.bat
collector-client/collector_gui.bat
collector-client/collector_start.bat
collector-client/gui.py
```

新增资产：

```text
collector-client/assets/order-system-collector-icon.png
collector-client/assets/order-system-collector.ico
```

当前 review 产物：

```text
storage/collector-review/订单系统采集器.exe
storage/collector-review/VERSION.txt
storage/collector-review/参数说明.txt
```

结论：

```text
collector-client/assets 应进入版本管理。
storage/collector-review 是本轮人工审核产物，不应作为源码入库。
旧 bat/vbs/gui.py 删除方向符合“单 exe 收口”目标，但提交前需要再次确认下载 ZIP 不再引用旧文件。
```

## 文档变更包

核心修改：

```text
README.md
docs/CURRENT_PROGRESS_REPORT.md
docs/TASKBOOK_INDEX.md
```

新增文档：

```text
docs/INITIAL_LANDING_CHECKLIST.md
docs/PROJECT_RECTIFICATION_TASK_LIST.md
docs/taskbooks/2026-06-12-stage-40-woda-template-rule-application-taskbook.md
docs/taskbooks/2026-06-13-stage-41-multi-item-standard-export-taskbook.md
docs/taskbooks/2026-06-13-stage-42-capture-batch-archive-taskbook.md
docs/taskbooks/2026-06-13-stage-43-product-sku-recognition-engine-taskbook.md
docs/taskbooks/2026-06-13-stage-44-optional-sku-auto-match-taskbook.md
docs/taskbooks/2026-06-13-stage-45-business-site-validation-readiness-taskbook.md
docs/taskbooks/2026-06-13-stage-46-report-excel-export-closure-taskbook.md
docs/taskbooks/2026-06-14-stage-47-template-fingerprint-recognition-fix-taskbook.md
docs/taskbooks/2026-06-15-stage-48-site-alpha-hardening-taskbook.md
```

本文件为阶段 48 P0 审计补充记录。

## Storage 清理判断

已跟踪但应从版本中移除的运行文件/预览图：

```text
storage/collector-test/collector-state.json
storage/server-console/backend-deps.ok
storage/sku-import-preview/*.png
```

未跟踪且不应入库的运行/交付产物：

```text
storage/collector-review/
storage/订单系统采集器-review.zip
```

历史 parser 样本：

```text
storage/parser-samples/*.json
storage/parser-samples/*.md
```

处理建议：

```text
1. storage/parser-samples 如果仍用于样本回归，应迁移到 backend/tests/fixtures 或 docs/reference。
2. storage/collector-test、storage/server-console、storage/sku-import-preview 应从版本中移除并由 .gitignore 接管。
3. storage/collector-review 和 review zip 保持未跟踪，不入库。
```

## 下一步执行包

建议后续按以下顺序拆分：

```text
P0-1：清理 storage 跟踪状态和 .gitignore。
P0-2：采集器正式交付物核对和 ZIP 内容测试。
P0-3：后端解析/识别/导出测试样本归档。
P0-4：前端导出和规则维护 UI 验收。
P0-5：README 和现场部署文档补齐。
```

## 当前不执行的操作

```text
不清库。
不重解析历史数据。
不连接业务机。
不删除未确认的用户业务数据。
不提交 git。
```
