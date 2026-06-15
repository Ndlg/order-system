# 阶段 08：代码边界收紧与复查任务书

> 日期：2026-06-11  
> 阶段状态：已完成本轮代码收紧与验证  
> 阶段性质：进入采集器与 P0 闭环前的质量门，不替代阶段 05 采集器任务书

## 1. 背景

阶段 07 已经把数据库归属规则收口为：

```text
单个平台数据库
多租户逻辑隔离
客户业务数据使用 tenant_id + workspace_id
面单解析模式、模板、模板字段属于平台全局解析规则
客户管理页面只维护字段用途、关键字段、图片、档口、匹配和导出配置
```

在进入采集器制作前，需要再次检查代码是否存在不合理的权限洞、系统字段可被篡改、前端文案乱码、旧入口暴露等问题。

## 2. 本轮目标

```text
1. 收紧登录态权限派生规则。
2. 防止软删除角色、错配角色继续授予权限。
3. 防止普通接口创建或更新系统字段。
4. 修复前端三端页面中文乱码。
5. 确认租户端构建产物不暴露旧客户可见入口。
6. 跑通后端测试、前端类型检查和两套前端构建。
```

## 3. 已完成修复

### 3.1 后端权限上下文

```text
get_current_user 只从有效 workspace 派生权限。
get_current_user 只从未删除、且 tenant_id/workspace_id 与 membership 匹配的角色派生权限。
软删除角色不再授予 roles、tenant_ids、workspace_ids。
角色与 membership 跨工作区错配时，不再授予 system_admin 或 workspace 访问权。
没有有效角色的用户不能写入数据。
```

### 3.2 通用 Repository 系统字段保护

```text
创建记录时忽略前端传入的 id、created_at、updated_at、created_by、updated_by、is_deleted。
创建 workspace 业务数据时继续由后端根据当前 workspace 写入 workspace_id 和 tenant_id。
更新记录时锁定 id、审计字段、is_deleted。
更新 workspace 业务数据时继续锁定 tenant_id 和 workspace_id。
更新 workspaces 时继续禁止通用 PATCH 修改 tenant_id。
```

### 3.3 前端中文与入口可见性

```text
修复租户业务页面、租户管理页面、平台后台页面的中文乱码。
租户端默认 / 仍是业务页面。
租户端 /admin 仍是客户公司管理页面。
平台私有后台独立入口仍是 5174 端口 /admin。
租户端构建产物未检出 server-admin、client-admin、/client、/workbench 旧入口字样。
```

## 4. 新增验证覆盖

```text
软删除 system_admin 角色不会授予系统管理员权限。
软删除角色不会继续授予 workspace 写入能力。
跨 workspace/tenant 错配的 system_admin 角色不会授予系统管理员权限。
前端传入 tenant_id、workspace_id、created_by、is_deleted 时，后端会忽略或覆盖。
平台全局面单解析模式不会带 tenant_id/workspace_id。
客户业务记录仍自动写入当前 workspace 对应 tenant_id/workspace_id。
```

## 5. 验证结果

```text
后端测试：
<USER_HOME>\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest backend/tests -q
结果：4 passed, 1 warning

前端类型检查：
node node_modules/vue-tsc/bin/vue-tsc.js --noEmit
结果：通过

租户端构建：
node node_modules/vite/bin/vite.js build
结果：通过

平台后台构建：
node node_modules/vite/bin/vite.js build --config vite.server-admin.config.ts
结果：通过

构建产物扫描：
租户端 dist 未检出乱码和旧入口字符串

代码格式检查：
git diff --check 通过，仅有 Windows CRLF 提示
```

## 6. 当前剩余风险

```text
1. 仍未引入 Alembic 正式迁移，当前只有初始化 SQL 和 SQLite 兼容迁移。
2. 权限模型仍是 system_admin / readonly / operator 等字符串级粗粒度模型，后续需要 tenant_admin、operator 等角色策略。
3. 平台解析引擎仍未真正实现，只完成了全局解析规则的数据边界。
4. 前端仍是流程骨架，真实采集、解析、字段配置、匹配和导出还未闭环。
5. 采集器与菜鸟、抖店打印组件的真实读取方式仍需在业务机环境验证。
```

## 7. 下一步建议

```text
1. 进入阶段 05：采集器与打印组件连接。
2. 先设计采集器注册、心跳、本地队列、上传 raw_capture_records 的接口契约。
3. 再做菜鸟、抖店 adapter 的真实业务机调研和最小读取验证。
4. 同步补 P0：raw_capture_records -> 平台解析 -> standard_details 的最小闭环。
```

## 8. 追加记录：采集器身份关系

2026-06-11 已进一步确认：

```text
采集器不使用员工账号密码登录。
采集器注册后使用 collector_token 作为设备身份。
collector_token 对应 collector，而 collector 绑定 tenant + workspace。
员工账号只负责在业务 UI 点击开始采集 / 结束采集。
capture_task / capture_session 记录由哪个用户发起和结束。
raw_capture_records 的 tenant_id / workspace_id 必须由服务器根据 collector_token 反查写入。
后端不能信任采集器自行传入 workspace_id 来决定数据归属。
```
