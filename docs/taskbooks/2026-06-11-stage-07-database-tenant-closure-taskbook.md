# 阶段 07：数据库租户归属与数据边界闭环任务书

> 日期：2026-06-11  
> 阶段状态：执行中，本轮完成数据库归属规则落地  
> 前置阶段：阶段 06 租户逻辑隔离与三端入口整改

## 1. 阶段背景

当前产品边界已经明确：

```text
平台不是固定商品/店铺/规格系统。
平台负责把采集器读到的杂乱 JSON / 文本整理成客户可读的面单信息。
用户后期在自己的工作区定义如何使用这些面单信息做关键字段、商品、图片、档口、匹配和导出。
服务端后台只维护客户账户映射、工作区、用户和平台共用的面单解析模式/模板。
客户业务页面和客户管理页面才处理采集、字段、图片、档口、异常和导出。
```

因此，在进入采集器开发之前，必须先把数据库中“数据属于哪个客户、哪个工作区、哪个入口可以维护”闭环。

## 2. 本阶段目标

```text
1. 明确第一版数据库采用单个平台数据库、多租户逻辑隔离。
2. 建立 tenant_id + workspace_id 的业务数据归属标准。
3. 补齐 ORM、Repository、初始化 SQL 和 SQLite 兼容迁移。
4. 确保账号 A 登录后上传或创建的数据只进入账号 A 可访问的 workspace。
5. 确保不同客户/工作区的数据不能互相读取、修改或创建。
6. 写入数据库设计文档，作为后续采集器和 P0 业务闭环的依据。
```

## 3. 数据库保存什么

平台数据库保存：

```text
客户/租户：tenants
工作区：workspaces
用户与角色：users、roles、user_workspaces
平台共用面单解析模式与模板：waybill_modes、waybill_templates、waybill_template_fields
采集器与原始数据：collectors、capture_tasks、capture_batches、raw_capture_records
标准化明细：standard_detail_batches、standard_details
客户自定义配置：field_definitions、field_role_configs、key_field_sets、match_rules
图片与档口资料：image_assets、stalls
报货、异常、导出和日志：report_batches、report_lines、exception_records、export_records、operation_logs
```

平台数据库不保存为一级固定对象：

```text
固定商品
固定店铺
固定规格
固定鞋款
固定行业字段含义
固定报货模板
```

如果客户要用“店铺名、商品简称、规格”等做匹配，它们只能作为客户基于面单信息定义的匹配字段/业务含义存在，不作为平台固定模型存在。

## 4. 本阶段实施范围

### 4.1 后端模型

```text
WorkspaceModel 统一增加 tenant_id + workspace_id。
Workspace 保留 tenant_id，作为客户到工作区的映射。
UserWorkspace 增加 tenant_id，便于用户所属租户快速识别。
```

### 4.2 仓储层

```text
创建 workspace 业务数据时：
  - 从当前用户上下文取得 workspace_id。
  - 校验当前用户是否可访问该 workspace。
  - 根据 workspaces.tenant_id 自动写入 tenant_id。

更新 workspace 业务数据时：
  - 不允许前端修改 tenant_id。
  - 不允许前端修改 workspace_id。
```

### 4.3 鉴权上下文

```text
/auth/me 返回当前用户可访问的 tenant_ids。
workspace 列表返回 workspace.tenant_id。
CurrentUser 保存 tenant_ids 和 workspace_ids。
```

### 4.4 数据库脚本

```text
scripts/init_db.sql 为所有 workspace 业务表补齐 tenant_id。
所有 workspace 业务表增加 tenant_id 索引。
SQLite 本地兼容迁移为历史开发库补齐 tenant_id 字段并按 workspace 回填。
```

### 4.5 文档

```text
新增 docs/DATABASE_DESIGN.md。
更新 README、任务书索引、当前进度报告。
保留旧阶段任务书，不覆盖。
```

## 5. 验收标准

本阶段完成后必须满足：

```text
1. 后端测试通过。
2. 前端租户 UI 构建通过。
3. 平台私有后台 UI 构建通过。
4. scripts/init_db.sql 中 workspace 业务表均有 tenant_id。
5. 创建 field_definitions 等业务记录时自动写入 tenant_id。
6. 双用户双 workspace 测试能证明不同 tenant/workspace 数据隔离。
7. /auth/me 能返回 tenant_ids 和 workspace.tenant_id。
8. 数据库设计文档能清楚回答“平台数据库保存什么、客户数据保存在哪、为什么不固定业务概念”。
```

## 6. 当前完成记录

已完成：

```text
WorkspaceModel 增加 tenant_id。
UserWorkspace 增加 tenant_id。
Repository 创建 workspace 业务数据时自动写入 tenant_id。
Repository 更新 workspace 业务数据时锁定 tenant_id 和 workspace_id。
Repository 允许平台维护 workspaces.tenant_id 映射。
系统管理员在后端可解析全部 workspace，用于平台后台维护客户映射；面单解析模式/模板已脱离 workspace，作为平台共用解析规则。
CurrentUser 增加 tenant_ids。
/auth/me 增加 tenant_ids 和 workspace.tenant_id。
种子数据为 default tenant/workspace/role/membership/waybill_mode 补齐 tenant_id。
启动种子逻辑会按 workspace 回填历史业务记录 tenant_id。
SQLite 兼容迁移补齐 workspace 业务表 tenant_id。
MySQL 初始化 SQL 补齐 workspace 业务表 tenant_id 与索引。
测试覆盖账号隔离和 tenant_id 写入。
新增数据库设计文档。
租户端移除旧 /client、/client-admin、/server-admin、/workbench 兼容路由，客户可见 URL 只保留 / 与 /admin。
```

阶段 07 后追加校正：

```text
此前代码把 waybill_modes、waybill_templates、waybill_template_fields 做成了 workspace-scoped。
这与最新确认的产品逻辑不一致，现已完成修复。
正确口径是：面单解析模式/模板是平台共用逻辑，用于把原始采集 JSON 整理成客户可读面单信息。
客户只维护解析后面单信息如何参与商品、图片、档口和导出匹配。
本轮已将 waybill_modes、waybill_templates、waybill_template_fields 从租户业务表中拆出，改为平台全局解析规则。
本轮已将 roles 写操作收紧为平台管理员权限，避免普通可写用户通过角色名提权。
本轮已修复软删除 role 仍参与权限计算的问题。
本轮已锁定 workspaces.tenant_id 的通用 PATCH 修改，避免历史业务数据归属不一致。
```

验证记录：

```text
后端 pytest backend/tests -q 通过，3 passed。
租户端 vue-tsc --noEmit 通过。
租户端 Vite build 通过。
平台私有后台 vue-tsc --noEmit 通过。
平台私有后台 Vite build --config vite.server-admin.config.ts 通过。
租户端构建产物未检出 server-admin、client-admin、/client、/workbench 旧入口字样。
git diff --check 通过，仅有 Windows CRLF 提示。
```

待后续阶段推进：

```text
正式 Alembic 迁移。
平台后台更细权限：平台管理员、客户管理员、业务人员。
采集器 API：注册、心跳、任务、原始记录上传、离线补传。
采集器适配器：菜鸟打印组件、抖店打印组件。
P0：标准化 Excel 到报货 Excel 闭环。
```

## 7. 下一阶段建议

数据库归属规则闭环后，建议进入采集器连接阶段，但不要直接写死菜鸟或抖店逻辑。

下一阶段应先做：

```text
1. 采集器注册接口。
2. 采集器心跳接口。
3. 原始采集记录上传接口。
4. 本地采集器 adapter 抽象。
5. 菜鸟打印组件 adapter 骨架。
6. 抖店打印组件 adapter 骨架。
7. 断网本地队列和恢复补传设计。
```

采集器上传的数据仍然只进入当前租户工作区的 `raw_capture_records`，不在采集器中定义业务字段含义。
