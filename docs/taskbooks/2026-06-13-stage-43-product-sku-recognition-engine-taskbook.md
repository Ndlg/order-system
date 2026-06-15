# 阶段 43：商品/SKU 识别执行引擎

> 日期：2026-06-13  
> 状态：执行中，本轮先做批次预览闭环

## 背景

阶段 42 已经把“读取已采集面单”收口到监听批次，用户可以在商品识别页按批次维护商品/SKU 规则。但当前规则主要停留在录入和展示层：规则保存到 `match_rules` 后，还没有一个后端引擎按批次逐商品行执行匹配，也没有统一输出命中商品、命中 SKU、兜底命中、未命中和冲突原因。

这会导致页面上看起来能配置规则，但导出和批量处理还不能稳定复用这些规则。

## 本轮目标

```text
新增后端商品/SKU 识别执行服务。
以监听批次为输入，读取该批次 standard_details。
我打多商品面单按 custom_items 展开为商品行。
每个商品行先匹配商品名称，再在该商品下匹配 SKU。
SKU 主匹配使用销售属性1，匹配不到时使用备注字段兜底。
输出每个商品行的识别状态、商品、SKU、命中规则、命中字段和原因。
商品识别页增加“预览本批次识别结果”，让用户能验证规则是否可复用。
```

## 识别流程

```text
监听批次 capture_task_id
  ↓
standard_details
  ↓
展开商品行
  ↓
按 mode_code / print_template_config_id / product_keyword 匹配商品规则
  ↓
在命中的商品范围内，按 sku_field + keyword 匹配 SKU
  ↓
主 SKU 未命中时，按 sku_fallback_field + sku_fallback_keyword 匹配
  ↓
输出 matched / product_unmatched / sku_unmatched / conflict
```

## 匹配规则

```text
商品匹配：
  woda 使用 custom_product_text 对 product_keyword。
  其他面单模式使用 fields 中配置的字段拼接文本对 keyword。

SKU 匹配：
  woda 优先 custom_sales_attr1_text 对 keyword。
  woda 兜底 custom_item_remark_text 对 sku_fallback_keyword。
  非 woda 当前仍按 fields + keyword 兼容预览。

冲突：
  同一商品行命中多个不同商品，状态为 conflict。
  同一商品下命中多个不同 SKU，状态为 conflict。
```

## 业务边界

```text
1. 本阶段先做预览，不直接改写 standard_details。
2. 不改变商品/SKU 资料模型。
3. 不改变 match_rules 保存结构，只消费现有 match_values。
4. 不在导出 Excel 中写入识别结果，导出接入放到下一阶段。
5. 不做复杂分词和相似度，先使用可解释的包含/相等匹配。
```

## 验收标准

```text
1. 后端新增识别预览接口，按 capture_task_id 返回商品行识别结果。
2. 多商品面单返回多条 item 结果。
3. 商品命中、SKU命中、备注兜底命中、未命中和冲突状态可区分。
4. 商品识别页能点击预览当前批次。
5. 前端 tenant 构建通过。
6. 后端 Python 编译和新增测试通过。
7. 浏览器验证商品识别页预览无控制台错误。
```

## 后续任务

```text
1. 把识别结果持久化到商品行维度。
2. 整理文档导出增加商品/SKU识别结果字段。
3. 未命中和冲突结果写入异常记录。
4. 支持后台批量执行和大批量分页。
5. 后续按用户需求增加精确匹配、包含匹配、正则匹配等可配置匹配方式。
```
