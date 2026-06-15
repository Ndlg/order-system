# 阶段 32：抖店字段说明与导出表头定义

## 背景

抖店面单已经可以被平台解析出 `shopName`、`productInfo`、`productShortInfo`、`productCount` 等字段。

客户不应该直接面对杂乱 JSON，也不应该被系统强行生成固定 Excel 表头。平台应该把“抖店原始字段 -> 系统字段 -> 字段含义 -> 样例”展示清楚，再让客户管理员自行定义整理文档表头。

## 目标

```text
客户管理端新增“导出表头”页面。
展示抖店可读取字段的原始字段名、系统字段编码、含义和真实样例。
客户可以选择字段并自定义 Excel 表头名称和排序。
保存后的表头写入当前工作区 field_definitions。
历史软删除过的同名字段可以恢复，避免唯一约束导致无法重新定义。
```

## 已完成

```text
新增后端 POST /api/v1/export-field-definitions/upsert。
该接口按 workspace_id + code 查找 field_definitions，包括已软删除记录。
如果存在旧记录，则恢复并更新表头名称、字段编码、排序和导出状态。
如果不存在，则创建当前工作区的新导出字段。
新增客户管理页 /admin/export-headers。
客户管理侧边栏新增“导出表头”入口。
客户管理首页新增“导出表头”卡片。
导出表头页展示抖店字段说明：
  shopName -> shop_name
  productInfo / item -> product_full_text
  productShortInfo -> product_short_text / spec_text
  productCount -> product_count_text / quantity
  trackNo -> logistics_no
  orderId -> order_no
  buyerRemark -> buyer_remark
  remark -> seller_remark
  sPInfo -> sp_info
  sPSInfo -> sps_info
  templateCode -> template_code
  parentTemplateCode -> parent_template_code
页面从当前工作区 standard_details 读取真实样例。
页面支持保存、编辑和删除导出表头。
旧 /admin/field-definition 重定向到 /admin/export-headers。
```

## 当前口径

```text
平台负责解析抖店字段并解释字段含义。
客户管理员负责决定哪些字段进入整理文档，以及 Excel 表头叫什么。
系统不再默认生成固定业务表头。
```

## 验证结果

```text
后端 pytest 通过：7 passed, 1 warning。
backend Docker 构建通过并已重启。
tenant-ui Docker 构建通过并已重启。
浏览器验证 /admin/export-headers：
  页面标题为“导出表头”。
  显示“抖店字段说明 / 自定义表头 / 已定义表头”。
  页面包含 shopName、productInfo、productShortInfo。
  页面包含“保存表头”按钮。
```
