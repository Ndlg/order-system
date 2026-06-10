# 配置归属与隔离原则

## 核心结论

系统不以店铺作为一级对象，也不按店铺隔离数据。

不同用户维护的是不同的规则、鞋款定义、规格映射、图片绑定、档口归属和导出配置。因此，配置归属必须挂在 `workspace_id` 下。

```text
User
  ↓
Workspace
  ↓
Waybill Mode
  ↓
Field Roles / Product Alias Mapping / Spec Mapping / Images / Stalls / Export Rules
```

## 为什么不用店铺隔离

标准化明细里可能存在淘宝店铺名、抖店店铺名或其他来源字段，但这些字段只是业务数据的一部分。

系统真正处理的是：

```text
面单模式
标准化明细
用户自定义映射
报货汇总
Excel 导出
```

因此，店铺名只能作为筛选、展示、辅助字段，不允许成为系统核心模型。

## 工作空间隔离规则

每个用户默认拥有一个工作空间。用户可以创建多个工作空间，用于维护不同客户、不同业务规则或不同鞋款定义。

所有以下数据必须带 `workspace_id`：

```text
waybill_modes
waybill_templates
standard_detail_batches
standard_details
field_role_configs
product_alias_mappings
spec_mappings
stalls
product_images
report_batches
report_lines
exception_records
export_records
operation_logs
```

## 规则与鞋款定义归属

以下配置必须属于具体工作空间，不能做成全局共享配置：

```text
字段角色配置
鞋款简称映射
规格映射
商品图片绑定
档口归属
导出配置
异常修正规则
```

示例：

```text
用户A / 工作空间A：
  ac -> ACG
  5.0 -> 5.0
  炭黑 -> 二代炭黑

用户B / 工作空间B：
  ac -> 另一个鞋款定义
  5.0 -> 另一个分类
  炭黑 -> 其他规格名称
```

两个用户的数据和规则互不影响。

## 共享规则的正确方式

如果后续需要多个用户共同维护同一套规则，不要复制数据库，也不要按店铺共享。正确方式是：

```text
把多个用户加入同一个 workspace，并分配不同角色。
```

如果需要把一套规则复制给另一个用户，后续可以增加：

```text
导出配置包
导入配置包
复制工作空间配置
```

## 禁止事项

```text
禁止使用 shop_id 作为核心隔离字段。
禁止把店铺名做成系统一级对象。
禁止把鞋款简称映射做成全局唯一规则。
禁止把规格映射做成全局唯一规则。
禁止不同 workspace 共用同一套可变业务配置。
禁止用户跨 workspace 查询、导出、下载、修改数据。
```
