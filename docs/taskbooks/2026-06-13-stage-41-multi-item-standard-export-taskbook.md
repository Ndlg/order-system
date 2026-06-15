# 阶段 41：多商品面单按商品行展开整理导出

> 日期：2026-06-13  
> 状态：已完成本轮最小整改

## 背景

阶段 40 已经把我打模板字段推进到标准明细，`cainiao_woda_printxml` 面单可以保存 `custom_items`，每个商品行包含：

```text
product_text
sales_attr1_text
sales_attr2_text
quantity_text
remark_text
raw_text
```

商品识别页也可以把多商品面单拆成 `面单 ID-商品序号` 候选。但整理文档下载仍然按 `standard_details` 一张面单输出一行，这会导致一张面单有多个商品时，最终 Excel 无法完整表达业务结果。

## 本轮目标

```text
下载整理文档时，遇到包含 custom_items 的我打面单，按商品行展开输出。
同一张面单的公共字段保留，商品字段由每个 custom_items[i] 覆盖。
一张面单有 2 个商品，最终 Excel 生成 2 行；一张面单有 1 个商品，仍生成 1 行。
导出表头配置页补充我打商品行字段，用户可以选择商品文字、销售属性1、销售属性2、数量文字、备注字段。
导出过程不按商品行反复查数据库，先读取表头和标准明细，再在内存展开行。
```

## 业务边界

```text
1. 不把一张原始面单拆成多张 raw_capture_records。
2. 不把一张标准明细拆成多条 standard_details。
3. 多商品展开只发生在整理结果/Excel 行生成阶段。
4. 商品识别规则仍由用户维护，本阶段不新增自动批量命中规则。
5. 备注字段仍来自模板定义后的 custom_items[].remark_text。
6. 抖店和菜鸟店铺直接打印暂时保持一张标准明细一行。
```

## 导出行规则

```text
base_values = standard_detail.field_values

如果 base_values.custom_items 是非空数组：
  对每个 item 生成一行 export_values
  export_values 继承 base_values
  export_values.custom_product_text = item.product_text
  export_values.custom_sales_attr1_text = item.sales_attr1_text
  export_values.custom_sales_attr2_text = item.sales_attr2_text
  export_values.custom_spec_text = item.spec_text 或 item.sales_attr1_text
  export_values.custom_size_text = item.size_text 或 item.sales_attr2_text
  export_values.custom_quantity_text = item.quantity_text
  export_values.custom_item_remark_text = item.remark_text
  export_values.custom_item_index = 当前商品序号
  export_values.custom_item_count = 当前面单商品总数

如果没有 custom_items：
  使用 base_values 生成一行
```

## 导出字段

我打商品行可选字段：

```text
custom_product_text        商品文字
custom_sales_attr1_text    销售属性1
custom_sales_attr2_text    销售属性2
custom_quantity_text       数量文字
custom_item_remark_text    备注字段
custom_item_index          商品序号
custom_item_count          面单商品数
raw_document_id            原始面单 ID
print_template_config_label 面单模板
```

兼容字段：

```text
custom_spec_text 读取 custom_spec_text，缺失时回退 custom_sales_attr1_text。
custom_size_text 读取 custom_size_text，缺失时回退 custom_sales_attr2_text。
product_display_text 优先显示 custom_product_text，再回退平台商品字段。
quantity 优先显示 quantity，再回退 custom_quantity_text。
```

## 验收标准

```text
1. 后端 Python 编译通过。
2. 前端 tenant 构建通过。
3. 下载某个包含多商品我打面单的整理文档时，Excel 行数按商品行增加。
4. 多商品行中的商品文字、销售属性1、销售属性2、数量和备注字段分别来自对应 custom_items[i]。
5. 单商品面单仍输出一行，不重复。
6. 导出表头页可以选择我打商品行字段。
7. 浏览器验证导出表头页无前端控制台错误。
```

## 后续任务

```text
1. 把商品识别规则真正接入批量整理结果，输出匹配到的商品/SKU。
2. 商品/SKU 未命中时生成异常记录。
3. 图片和档口匹配接入商品行维度。
4. 大批量 Excel 改为后台任务和流式写出。
```
