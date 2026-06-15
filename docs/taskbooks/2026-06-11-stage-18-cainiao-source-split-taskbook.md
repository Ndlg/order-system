# 阶段 18：菜鸟来源拆分与解析结果整改

> 阶段定位：阶段 17 已经把 raw JSON 整理成 `standard_details`，但把菜鸟组件统一归入 `cainiao_cloud_print` 会误导系统。真实验证后确认，同一个菜鸟本地组件会承载不同上游来源，必须按来源和负载形态拆平台解析模板。

## 1. 本阶段目标

```text
修正“同一打印组件 = 同一解析模式”的错误假设。
把菜鸟店铺直接打印和菜鸟 woda 打印平台中转拆成两个平台解析模式。
店铺直接打印抽取结构化面单字段。
woda 打印平台从 printXML / CDATA 中抽取可见商品文字。
一个 raw_capture_record 内含多个 document 时，按 document 生成多条 standard_details。
客户业务页按采集任务查看本轮商品信息，物流单号、订单号、店铺名作为辅助字段。
```

## 2. 核心认知修正

```text
采集器只负责复制本地 print.db 新增任务并回传服务器。
解析层负责判断原始 JSON 属于哪一种平台解析模板。
解析模板不是按本地组件名唯一确定，而是按 component + source + payload_shape 判断。
客户自定义区域由客户定义业务含义，平台只能保存原文，不能写死商品、规格、数量等语义。
```

## 3. 已完成整改

后端解析模式：

```text
douyin_cloud_print       抖店 / CloudPrint
cainiao_direct_shop      菜鸟店铺直接打印
cainiao_woda_printxml    菜鸟 woda 打印平台
cainiao_cloud_print      菜鸟云打印（遗留，默认禁用）
```

识别规则：

```text
菜鸟店铺直接打印：
  contents[].data 存在 WAIBILLNO_BAR_CODE、ORDER_ID、SHOP_NAME 等结构化字段

菜鸟 woda 打印平台：
  documentID 包含 -woda-
  标准面单字段多为加密或脱敏
  printXML / CDATA 作为 custom_area_raw_text 保存，同时写入 product_full_text / product_short_text / spec_text
  只要读取到这些可见商品文字，就生成 standard_details 并进入匹配主流程
```

店铺直接打印当前抽取字段：

```text
logistics_no
order_no
shop_name
product_full_text
product_short_text
quantity
buyer_memo
seller_memo
print_time
raw_document_id
```

woda 打印平台当前抽取字段：

```text
source_platform
raw_document_id
product_full_text
product_short_text
spec_text
encrypted_waybill
custom_area_raw_text
sender_masked
recipient_masked
document_sequence
template_urls
```

## 4. 代码改动范围

```text
backend/app/services/waybill_parser.py
backend/app/services/bootstrap.py
backend/app/api/routes/collector_runtime.py
backend/tests/test_foundation.py
frontend/src/views/workbench/WaybillBatchesView.vue
docs/CODEX_TASKBOOK.md
docs/TASKBOOK_INDEX.md
docs/CURRENT_PROGRESS_REPORT.md
```

关键能力：

```text
parse_raw_capture_record 支持返回多条 ParsedWaybill。
POST /api/v1/collector-control/parse-records 支持 force=true 重跑历史解析。
force=true 会软删除上次解析生成的全部 detail_ids，避免一条 raw 拆多条明细时重复累积。
平台后台种子数据新增菜鸟店铺直打和菜鸟 woda 两套模板。
客户业务页默认按最新采集任务展示，不再混合显示全工作区历史明细。
客户业务页主表改为本轮商品信息，优先展示商品/备注/规格等可见文字。
物流单号、平台订单号、店铺名等字段保留为辅助信息。
只有完全没有读到可用商品文字的采集内容，才进入未识别区。
```

## 5. 验证结果

```text
后端 pytest -q 通过：4 passed, 1 warning。
py_compile 通过：waybill_parser.py、bootstrap.py、collector_runtime.py。
测试覆盖：
  抖店 / CloudPrint 结构化解析
  菜鸟店铺直接打印结构化解析
  菜鸟 woda 单条 raw 内多 document 拆成多条 standard_details
  force=true 重跑解析不会留下重复 woda 明细
  woda custom_area_raw_text 同步进入 product_full_text / product_short_text / spec_text
```

## 6. 当前边界

```text
平台后台目前仍是资源表格型页面，不是完整模板编辑器。
解析规则仍是内置代码模板，不是可视化规则引擎。
woda 中转面单的标准面单字段受加密限制，第一版不尝试还原运单和收件人。
用户自定义区 / printXML 中读取到的商品文字会进入匹配主流程，后续由客户规则定义如何匹配图片和档口。
历史已解析数据需要用 force=true 重跑，才会从遗留 cainiao_cloud_print 切换到新模式。
客户业务页当前按采集任务隔离显示；后续还需要把“生成报货单”也绑定到选中的采集任务。
```

## 7. 下一步建议

```text
1. 用真实任务重新采集一轮菜鸟直打、菜鸟 woda 和抖店样例，确认页面字段展示。
2. 做平台后台解析模板详情页，让开发者管理员能看清每种模板能提供哪些字段。
3. 进入客户管理页的字段选择和关键字段规则定义。
4. 再接商品图片、档口匹配和报货 Excel 预览导出。
```
