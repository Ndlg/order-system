# 配置归属与隔离原则

> 本文档是辅助原则文档。如与 `docs/CODEX_TASKBOOK.md` 冲突，以 `docs/CODEX_TASKBOOK.md` 为准。

## 核心结论

系统面向多个用户，但不按任何预设业务对象隔离数据，也不以任何预设业务对象作为整理主线。

不同用户维护不同字段定义、关键字段组合、图片匹配、档口匹配和导出配置。因此，所有可变业务配置必须挂在 `workspace_id` 下。

```text
User
  ↓
Workspace
  ↓
Waybill Mode
  ↓
Field Definitions / Key Fields / Match Rules / Images / Stalls / Reports / Exports
```

## 工作空间是什么

`workspace` 是系统最高数据隔离边界。

一个用户可以有一个或多个 workspace。多个用户也可以加入同一个 workspace 共同维护同一套配置。

每个 workspace 独立维护：

```text
面单模式
面单模板
标准化明细
面单字段定义
字段角色配置
关键字段组合
关键字段匹配规则
图片信息
档口资料
报货批次
导出记录
异常记录
操作日志
```

## 面单字段的定位

标准化明细里的业务字段全部来自用户上传 Excel 表头、面单模板提取规则或用户手工定义。

这些字段可以用于：

```text
展示
筛选
导出
关键字段匹配
图片匹配
档口匹配
用户自定义分组
辅助备注
```

但不能作为系统预设的：

```text
一级对象
数据隔离边界
固定整理主线
必须字段
固定业务规则
```

## 必须带 workspace_id 的数据

以下表必须带 `workspace_id`：

```text
waybill_modes
waybill_templates
standard_detail_batches
standard_details
field_definitions
field_role_configs
key_field_sets
match_rules
stalls
image_assets
report_batches
report_lines
exception_records
export_records
operation_logs
raw_capture_records
capture_tasks
capture_batches
collectors
```

## 配置不得全局共享

以下配置不能做成全局唯一规则，必须属于具体 workspace：

```text
面单字段定义
字段角色配置
关键字段组合
图片匹配规则
档口匹配规则
导出配置
异常修正规则
```

不同 workspace 的配置互不影响。

## 共享规则的正确方式

如果多个用户要维护同一套规则，不要写成全局规则。

正确方式：

```text
把多个用户加入同一个 workspace，并分配不同角色。
```

如果要把一套规则复制给另一个用户，后续可以增加：

```text
导出配置包
导入配置包
复制工作空间配置
```

## 禁止事项

```text
禁止使用 shop_id 作为核心隔离字段。
禁止创建 shops 表作为业务主表。
禁止把用户业务对象做成系统一级固定对象。
禁止把字段定义做成全局唯一规则。
禁止把关键字段匹配规则做成全局唯一规则。
禁止不同 workspace 共用同一套可变业务配置。
禁止用户跨 workspace 查询、导出、下载、修改数据。
```
