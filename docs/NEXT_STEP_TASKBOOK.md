# 当前下一步任务书

> 历史命名文件，后续不要覆盖成新阶段内容。正式阶段留档见 `docs/TASKBOOK_INDEX.md` 和 `docs/taskbooks/`。

> 适用范围：从当前管理 / 开发者验证台，推进到“用户工作台入口 + 管理后台入口”清晰分离的下一轮开发。  
> 上游依据：`docs/CODEX_TASKBOOK.md`、`docs/FRONTEND_ENTRYPOINTS.md`、`docs/NEXT_PHASE_TASKBOOK.md`  
> 当前前置状态：管理 / 开发者验证台已可运行，前端已中文化，数据库基础层与鉴权上下文已建立。

## 0. 本轮目标

本轮目标不是马上完成完整报货 Excel 闭环，而是先把前端产品骨架摆正：

```text
现有页面收拢为管理 / 开发者后台
  ↓
新增用户工作台入口
  ↓
按面单处理流程搭建用户工作台页面骨架
  ↓
接入登录态、workspace 上下文和基础 API
  ↓
让下一轮可以开始做标准化 Excel 上传、字段定义、匹配和导出闭环
```

完成后，项目应从“只有后台验证台”进入“用户工作台可继续开发”的状态。

## 1. 本轮原则

必须遵守：

```text
1. 当前通用资源 CRUD 只能作为管理 / 开发者后台，不作为最终用户流程。
2. 用户工作台必须围绕面单批次处理流程设计。
3. 用户工作台不预设固定业务字段。
4. 字段名称、字段含义、关键字段、图片匹配、档口匹配和导出方式都由用户后续定义。
5. workspace_id 仍然是最高数据隔离字段。
6. 不引入 shop_id、shops 或任何固定业务对象作为核心模型。
7. 不为了演示写死具体面单字段、图片匹配或档口匹配关系。
```

## 2. 交付范围

### 2.1 前端入口拆分

完成：

```text
登录后进入用户工作台默认入口
新增 /workbench 路由组
新增 /admin 路由组
现有通用资源页面迁移或归类到 /admin
顶部或侧边提供“用户工作台 / 管理后台”切换入口
根据当前用户角色预留入口显示控制
```

建议路由：

```text
/login
/workbench
/workbench/waybill-batches
/workbench/field-definition
/workbench/key-fields
/workbench/assets
/workbench/matching
/workbench/exceptions
/workbench/exports
/admin
/admin/workspaces
/admin/users
/admin/waybill-modes
/admin/waybill-templates
/admin/field-definitions
/admin/key-field-sets
/admin/match-rules
/admin/image-assets
/admin/stalls
/admin/raw-capture-records
```

### 2.2 用户工作台页面骨架

用户工作台第一屏必须让用户看到“下一步要处理什么”，而不是技术资源列表。

页面骨架：

```text
用户工作台首页
面单批次
字段定义
关键字段
图片与档口资料
匹配复核
异常处理
导出中心
```

工作台首页展示：

```text
当前工作空间
待处理面单批次
字段配置状态
图片匹配状态
档口匹配状态
异常数量
最近导出记录
下一步操作入口
```

### 2.3 面单批次流程骨架

先做流程壳，不要求本轮完成真实 Excel 解析。

完成：

```text
面单批次列表页
新建批次入口
上传标准化 Excel 的 UI 占位
识别结果预览区占位
字段读取结果占位
进入字段定义向导的按钮
```

说明：

```text
如果后端接口未完成，可以先用空状态和接口占位。
不能在前端写死示例业务字段作为正式逻辑。
允许使用 clearly marked 的开发示例数据，但必须集中在 mock/dev 文件中，后续可删除。
```

### 2.4 字段定义与关键字段流程骨架

完成：

```text
字段定义向导页面
关键字段选择页面
字段用途配置 UI 占位
关键字段组合 UI 占位
保存按钮接入现有 field-definitions / key-field-sets API 或使用明确占位状态
```

字段用途至少保留以下配置位置：

```text
是否显示
是否筛选
是否导出
是否参与关键字段匹配
是否参与图片匹配
是否参与档口匹配
是否参与汇总分组
是否作为数量字段
是否作为备注字段
```

### 2.5 图片与档口资料入口

完成：

```text
图片资料入口
档口资料入口
匹配规则入口
缺失资料提示占位
批量导入入口占位
```

本轮不要求完成真实图片上传和 Excel 图片嵌入，但页面结构必须能承接后续功能。

### 2.6 异常与导出入口

完成：

```text
异常处理页面骨架
报货汇总预览页面骨架
导出中心页面骨架
三种导出方式的选择 UI 占位
```

三种导出方式必须保留：

```text
合并 Sheet
分组 Sheet
分组文档
```

## 3. 后端配合任务

本轮后端只做支撑用户工作台骨架所需的最小补齐。

优先完成：

```text
/auth/me 返回当前用户、角色和可访问 workspace
/workspaces 支持当前用户 workspace 列表
资源列表接口返回分页结构或至少预留分页参数
standard-detail-batches 基础列表 / 创建接口
standard-details 基础列表接口
field-definitions 基础列表 / 创建 / 更新接口
key-field-sets 基础列表 / 创建 / 更新接口
match-rules 基础列表 / 创建 / 更新接口
```

暂不要求：

```text
完整 Excel 解析
真实报货汇总引擎
Excel 三模式真实导出
图片嵌入 Excel
采集端实时连接
复杂权限矩阵
```

## 4. 前端结构建议

建议调整为：

```text
frontend/src/layouts/
  AppShell.vue
  WorkbenchLayout.vue
  AdminLayout.vue

frontend/src/views/workbench/
  WorkbenchHomeView.vue
  WaybillBatchesView.vue
  FieldDefinitionWizardView.vue
  KeyFieldWizardView.vue
  AssetsAndStallsView.vue
  MatchingReviewView.vue
  ExceptionsView.vue
  ExportCenterView.vue

frontend/src/views/admin/
  AdminDashboardView.vue
  AdminResourceView.vue

frontend/src/router/
  index.ts
  workbenchRoutes.ts
  adminRoutes.ts
```

不要一次性追求复杂设计系统。先保证：

```text
路由清晰
入口清晰
流程清晰
接口边界清晰
用户不会把后台配置页误认为业务流程
```

## 5. 执行顺序

请按以下顺序推进：

```text
1. 梳理现有前端路由，把当前页面标记为管理 / 开发者后台。
2. 新增 WorkbenchLayout 和 AdminLayout。
3. 新增 /workbench 与 /admin 路由组。
4. 登录后默认进入 /workbench。
5. 把现有通用资源页面归入 /admin。
6. 新建用户工作台首页。
7. 新建面单批次页面骨架。
8. 新建字段定义向导页面骨架。
9. 新建关键字段选择页面骨架。
10. 新建图片与档口资料页面骨架。
11. 新建匹配复核、异常处理、导出中心页面骨架。
12. 接入当前 token 和 workspace 请求头。
13. 根据现有后端能力接入可用 API。
14. 对未完成后端能力使用空状态，不写死业务规则。
15. 更新 README、进度报告和任务书状态。
16. 运行前端 build、后端测试和启动验证。
```

## 6. 验收标准

本轮完成时必须满足：

```text
1. 前端存在清晰的用户工作台入口。
2. 前端存在清晰的管理 / 开发者后台入口。
3. 登录后默认进入用户工作台。
4. 现有通用资源 CRUD 不再被描述为最终用户工作台。
5. 用户工作台首页能展示当前工作空间和下一步处理入口。
6. 面单批次、字段定义、关键字段、图片档口、匹配复核、异常处理、导出中心页面骨架存在。
7. 页面文案全部中文。
8. Element Plus 中文包继续生效。
9. 前端 build 通过。
10. 后端基础测试通过。
11. 不新增任何预设业务字段写死逻辑。
12. 不新增 shop_id / shops 核心模型。
13. 文档同步更新。
```

## 7. 建议提交拆分

建议按以下 commit 拆分：

```text
1. docs: add next step workbench taskbook
2. feat: split frontend workbench and admin routes
3. feat: add user workbench shell
4. feat: add waybill batch and field wizard placeholders
5. feat: add matching exception and export placeholders
6. test: verify frontend build and backend foundation
```

## 8. 本轮完成后的下一步

本轮完成后，进入用户工作台 P0 闭环开发：

```text
标准化 Excel 上传
读取 Excel 表头
生成字段定义草稿
保存用户字段配置
选择关键字段组合
维护图片和档口匹配规则
生成匹配结果
提示异常并允许修正
生成报货汇总
三种 Excel 导出
```
