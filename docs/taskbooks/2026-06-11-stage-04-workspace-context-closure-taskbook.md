# 阶段 04 任务书：工作空间上下文与多用户数据隔离闭环

> 适用范围：完善“不同用户进入系统后读取不同 workspace 数据”的完整闭环。  
> 上游依据：`docs/CODEX_TASKBOOK.md`、`docs/CONFIG_SCOPE.md`、`docs/taskbooks/2026-06-11-stage-02-database-foundation-taskbook.md`、`docs/taskbooks/2026-06-11-stage-03-workbench-entry-taskbook.md`  
> 当前前置状态：后端 Repository 已具备 workspace_id 强过滤能力，临时验证已确认两个用户不能互相读取 workspace 数据；前端已拆分 `/workbench` 与 `/admin`，但尚未提供工作空间选择器。

## 0. 阶段目标

本阶段目标是把“后端已经能隔离 workspace”推进为“用户在前端使用时也能正确进入自己的 workspace，并且只能读取自己的数据”。

闭环主线：

```text
用户登录
  ↓
前端调用 /auth/me
  ↓
获取当前用户、角色、可访问 workspace 列表
  ↓
自动选择或让用户选择 workspace
  ↓
前端统一写入当前 workspace_id
  ↓
所有 API 自动携带 X-Workspace-Id
  ↓
后端校验用户是否有该 workspace 权限
  ↓
Repository 按 allowed workspace 过滤数据
  ↓
前端只展示当前 workspace 的数据
```

本阶段完成后，平台框架应达到：

```text
不同用户登录后进入自己的工作空间
同一用户可在自己有权限的多个工作空间之间切换
切换工作空间后页面数据同步变化
无权限 workspace 请求被后端拒绝并由前端中文提示
```

## 1. 阶段原则

必须遵守：

```text
1. workspace_id 是最高数据隔离字段。
2. 前端只能从 /auth/me 返回的 workspaces 中选择当前 workspace。
3. 禁止前端手写或猜测用户没有权限的 workspace_id。
4. 后端继续作为最终权限裁决点，不能只依赖前端选择器。
5. 用户切换 workspace 后，所有资源列表必须重新加载。
6. localStorage 中旧 workspace_id 如果已不属于当前用户，必须自动修正。
7. 不引入 shop_id、shops 或任何固定业务对象作为隔离模型。
8. 不把用户业务字段写死为系统字段。
```

## 2. 交付范围

### 2.1 后端能力确认与补齐

确认或补齐：

```text
GET /auth/me 返回当前用户信息
GET /auth/me 返回角色列表
GET /auth/me 返回当前用户可访问 workspace 列表
GET /workspaces 非 system_admin 只能返回当前用户有权限的 workspace
所有 workspace-scoped 资源列表按 allowed workspace 过滤
指定 workspace_id 查询时，无权限返回 403
创建 workspace-scoped 资源时，X-Workspace-Id 无权限返回 403
按 id 读取其他 workspace 记录时，不泄露数据
```

现有能力判断：

```text
/auth/me：已有基础返回
Repository workspace 过滤：已有基础实现
临时双用户双 workspace 隔离验证：已通过
永久化测试：待补
```

### 2.2 后端永久化隔离测试

把临时验证沉淀为正式测试。

新增测试建议：

```text
backend/tests/test_workspace_isolation.py
```

测试场景：

```text
1. 创建 workspace A / workspace B。
2. 创建 user A / user B。
3. user A 只绑定 workspace A。
4. user B 只绑定 workspace B。
5. user A 创建字段记录 A。
6. user B 创建字段记录 B。
7. user A 列表只能看到记录 A。
8. user B 列表只能看到记录 B。
9. user A 查询 workspace B 列表返回 403。
10. user A 使用 X-Workspace-Id: B 创建记录返回 403。
11. user A 按 id 读取记录 B 返回 404 或不泄露数据。
12. user A 的 /workspaces 只返回 workspace A。
```

### 2.3 前端认证上下文

新增前端认证 / 工作空间上下文管理。

建议文件：

```text
frontend/src/services/session.ts
frontend/src/stores/session.ts
```

必须具备：

```text
token 保存
当前用户保存
角色列表保存
workspace 列表保存
当前 workspace_id 保存
登录后拉取 /auth/me
刷新页面后恢复 session
workspace_id 不合法时自动切到第一个可访问 workspace
退出登录清理 token、用户和 workspace_id
```

说明：

```text
可以优先使用 Pinia store。
如果先用轻量 service，也必须保证后续可迁移到 Pinia。
```

### 2.4 前端工作空间选择器

在 `AppShell` 顶部加入工作空间选择器。

要求：

```text
显示当前 workspace 名称
多个 workspace 时可下拉切换
只有一个 workspace 时显示单项状态
无 workspace 时显示中文错误提示
切换 workspace 后写入 localStorage
切换 workspace 后触发当前页面资源重新加载
```

页面影响：

```text
/workbench 首页状态应显示当前 workspace
/admin 资源页应按当前 workspace 读取
旧 localStorage workspace_id 不属于当前用户时必须修正
```

### 2.5 API 请求统一携带 workspace

完善 `frontend/src/services/api.ts`。

要求：

```text
所有需要鉴权的请求自动携带 Authorization
所有 workspace-scoped 请求自动携带 X-Workspace-Id
当前 workspace_id 必须来自 session store / session service
后端返回 401 时提示登录失效
后端返回 403 时提示无该工作空间权限
```

注意：

```text
不能继续硬编码默认 workspace_id = 1 作为长期逻辑。
允许开发环境在 /auth/me 尚未加载前临时回退，但必须在加载后修正。
```

### 2.6 前端页面联动

至少完成：

```text
登录成功后进入 /workbench，并完成 /auth/me 拉取
AppShell 显示当前用户和工作空间
AdminResourceView 根据 workspace 切换重新加载
WorkbenchHomeView 显示当前 workspace
未登录访问 /workbench 或 /admin 时跳转 /login
```

路由守卫要求：

```text
无 token：跳转 /login
有 token 但未加载 /auth/me：先加载 session
/login 页面已有 token 时可跳转 /workbench
```

### 2.7 前端验证数据

本阶段可以使用后端测试或开发种子数据创建两个 workspace 和两个用户。

要求：

```text
不同用户登录后，工作空间列表不同。
不同用户看到的字段定义列表不同。
同一用户切换 workspace 后，资源列表变化。
无权限 workspace 请求显示中文 403 提示。
```

## 3. 不在本阶段做的内容

以下不作为本阶段验收：

```text
标准化 Excel 真实上传解析
读取 Excel 表头生成字段定义草稿
图片上传和 hash
档口匹配真实规则编辑器
报货汇总引擎
Excel 三模式真实导出
采集端实时连接
复杂角色权限矩阵
```

这些进入后续 P0 业务闭环阶段。

## 4. 执行顺序

请按以下顺序推进：

```text
1. 新增后端 workspace 隔离永久测试。
2. 确认 /auth/me 返回用户、角色和 workspaces。
3. 前端新增 session store / service。
4. 前端登录成功后调用 /auth/me。
5. 实现未登录路由守卫。
6. 实现当前 workspace 初始化逻辑。
7. AppShell 顶部加入工作空间选择器。
8. API 请求改为从 session 读取当前 workspace_id。
9. AdminResourceView 在 workspace 切换后重新加载数据。
10. WorkbenchHomeView 显示真实当前 workspace。
11. 处理 token 失效、无 workspace、403 无权限中文提示。
12. 增加前端本地浏览器验证。
13. 更新 README、进度报告和任务书索引。
14. 运行前端 build。
15. 运行后端 pytest。
16. 提交并推送阶段 commit。
```

## 5. 验收标准

本阶段完成时必须满足：

```text
1. 后端永久测试覆盖双用户双 workspace 隔离。
2. /auth/me 能返回当前用户、角色、workspace 列表。
3. 前端登录后自动加载 /auth/me。
4. 前端有工作空间选择器。
5. 当前 workspace_id 不再长期硬编码为 1。
6. 切换 workspace 后资源列表重新加载。
7. 用户不能选择 / 使用自己无权限的 workspace。
8. 无权限 workspace 请求返回 403 并中文提示。
9. localStorage 中旧 workspace_id 不合法时自动修正。
10. 未登录访问 /workbench 或 /admin 会跳转 /login。
11. 前端 build 通过。
12. 后端 pytest 通过。
13. 不新增 shop_id / shops 核心模型。
14. 不新增预设业务字段写死逻辑。
15. 文档同步更新。
```

## 6. 建议提交拆分

建议按以下 commit 拆分：

```text
1. test: add workspace isolation coverage
2. feat: add frontend session context
3. feat: add workspace selector
4. feat: reload resources by workspace context
5. docs: update workspace context task progress
```

## 7. 本阶段完成后的下一步

本阶段完成后，进入 P0 业务闭环第一段：

```text
标准化 Excel 上传
  ↓
读取 Excel 表头
  ↓
生成字段定义草稿
  ↓
用户确认字段定义
  ↓
进入关键字段选择
```

该阶段会真正开始把“面单读取”接入用户工作台。

## 8. 当前执行进度

更新时间：2026-06-11

已完成：

```text
1. 新增后端 workspace 隔离永久测试。
2. 确认 /auth/me 返回用户、角色和 workspaces。
3. 前端新增 Pinia session store。
4. 前端登录成功后调用 /auth/me。
5. 实现未登录路由守卫。
6. 实现当前 workspace 初始化和旧 workspace_id 自动修正逻辑。
7. AppShell 顶部加入工作空间选择器。
8. API 列表请求按当前 workspace_id 追加查询参数。
9. AdminResourceView 在 workspace 切换后重新加载数据。
10. WorkbenchHomeView 显示真实当前 workspace。
11. 401 / 403 错误已有中文提示兜底。
12. 前端 build 已通过。
13. 后端 pytest 已通过。
14. 本地浏览器已验证 /workbench 登录后加载 session。
15. 本地浏览器已验证 /admin/field-definitions 按当前 workspace 过滤。
16. 本地浏览器已验证切换 workspace 后资源列表变化。
```

待完成：

```text
1. 退出登录后的 redirect 细节优化。
2. 多角色入口显示控制细化。
3. MySQL 实例联调。
4. 阶段提交与推送。
```
