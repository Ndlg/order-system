# 阶段 17：平台解析模板与采集结果整理 MVP

> 阶段定位：采集器已经能把原始打印 JSON 回传到 `raw_capture_records`，但客户看到 raw JSON 没有意义。本阶段把解析模板先放进平台后台，并让后端生成客户可读的 `standard_details`。

## 1. 本阶段目标

```text
平台后台维护系统支持的面单解析模式。
先内置抖店 / CloudPrint 解析模板。
同时内置菜鸟云打印的第一版可见文本解析模板。
采集器上传 raw_capture_records 后，后端自动解析并生成 standard_details。
已采集的历史 raw 记录可以手动重跑解析。
客户业务页能看到整理后的面单信息，而不是只看到 raw JSON。
```

## 2. 已完成内容

新增：

```text
backend/app/services/waybill_parser.py
POST /api/v1/collector-control/parse-records
```

平台后台种子数据：

```text
waybill_modes:
  douyin_cloud_print      抖店 / CloudPrint
  cainiao_cloud_print     菜鸟云打印

waybill_templates:
  抖店 CloudPrint 面单解析 v1
  菜鸟云打印面单解析 v1

waybill_template_fields:
  logistics_no
  order_no
  shop_name
  product_short_text
  product_full_text
  spec_text
  quantity
  raw_document_id
  custom_area_text
  template_urls
```

抖店 / CloudPrint 当前抽取字段：

```text
物流单号 logistics_no
平台订单号 order_no
店铺名 shop_name
商品信息 product_full_text
商品简称 product_short_text
数量文本 product_count_text
数量 quantity
规格文本 spec_text
模板编码 template_code
```

菜鸟云打印当前抽取字段：

```text
原始文档 ID raw_document_id
自定义区可见文本 custom_area_text
模板地址 template_urls
```

客户业务页：

```text
http://127.0.0.1:5173/waybill-batches
```

现在会展示 `standard_details` 整理结果。

## 3. 本机样例结果

任务 5 已重跑解析：

```text
parsed: 2
unsupported: 0
skipped: 0
```

抖店 / CloudPrint 样例：

```text
物流单号：YT0045101273987
平台订单号：6926919240176008395
店铺名：帅意体育
商品简称：【新款5.0跑鞋透气超轻减】5.0黑白紫 38.5 1 件
数量：1
```

菜鸟样例：

```text
原始文档 ID：605896604751236096-woda-605173262217911040+++0
自定义区文本：秒55 d，,C6全白，43*1
```

## 4. 当前边界

```text
当前模板是内置模板，不是完整可视化模板编辑器。
抖店模板已能从当前样例中抽出客户可读字段。
菜鸟模板受加密数据限制，第一版只抽可见自定义区文本。
商品简称、规格、数量后续还要进入客户自定义匹配规则。
```

## 5. 下一步建议

```text
1. 在平台后台为解析模板做更友好的只读详情页。
2. 在客户管理页定义关键字段和匹配规则。
3. 把 standard_details 接入商品图片和档口匹配。
4. 生成报货预览表，再做 Excel 导出。
```
