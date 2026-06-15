# 阶段 40：我打模板规则应用到标准明细

> 日期：2026-06-12  
> 状态：待执行

## 背景

阶段 39 已经完成客户管理端“打印模板规则”最小 UI。客户可以在当前工作区保存我打模板定义，规则保存到 `print_template_configs.config`，并且商品识别页已经预留了以下字段：

```text
custom_product_text
custom_spec_text
custom_quantity_text
custom_size_text
```

但当前我打面单候选仍主要读取 `custom_area_raw_text`，并在前端临时推断尺码和数量。这样会导致：

```text
1. 客户保存的模板规则还没有真正影响 standard_details。
2. 商品识别页看到的是原文候选，不是规则拆分后的业务候选。
3. 尺码和数量推断留在前端，无法被后续导出、复核、异常处理复用。
4. 模板规则更新后，没有明确的批量重算入口。
```

阶段 40 要把“模板规则配置”推进为“标准明细派生字段生成能力”。

## 本轮目标

```text
把当前工作区已保存的我打模板规则应用到 cainiao_woda_printxml 标准明细。
根据 print_template_configs.config 生成 custom_product_text、custom_spec_text、custom_quantity_text、custom_size_text。
把规则应用结果保存回 standard_details.field_values。
商品识别页读取规则应用后的 custom_* 字段，不再依赖前端临时推断作为主口径。
提供模板规则试算和批量应用入口，方便客户确认规则效果。
```

## 业务边界

```text
1. 本阶段只处理菜鸟 woda / 我打中转模式：cainiao_woda_printxml。
2. 抖店和菜鸟店铺直打继续使用平台已解析结构化字段，不进入客户模板规则应用。
3. 平台仍不判断客户业务含义，只执行客户在当前工作区保存的拆分规则。
4. 不修改 raw_capture_records 原始记录。
5. 不修改平台后台 waybill_templates / waybill_template_fields。
6. 不跨 workspace 读取或应用模板规则。
7. 未匹配到模板规则的面单继续保留原始可见文字，但不能假装已经完成规则拆分。
```

## 数据口径

规则来源：

```text
print_template_configs
  waybill_mode = cainiao_woda_printxml
  is_enabled = true
  config.rule_type = custom_text_lines_v1
  config.source_template_key 对应 standard_details.field_values.print_template_key
```

标准明细来源：

```text
standard_details
  waybill_mode = cainiao_woda_printxml
  field_values.custom_area_lines
  field_values.custom_area_raw_text
  field_values.print_template_key
```

规则应用后写入：

```text
field_values.custom_product_text
field_values.custom_spec_text
field_values.custom_quantity_text
field_values.custom_size_text
field_values.print_template_config_id
field_values.print_template_config_label
field_values.print_template_rule_status
```

建议状态值：

```text
applied        已按客户模板规则生成 custom_* 字段
missing_config 当前明细没有匹配到启用的客户模板规则
empty_result   匹配到规则，但未能生成有效商品文字
```

## 规则应用逻辑

第一版只实现阶段 39 已保存的 `custom_text_lines_v1`。

```text
1. 从 standard_details.field_values.custom_area_lines 取原始行。
2. 如果 custom_area_lines 不存在，则从 custom_area_raw_text 按换行切分。
3. 使用 config.product_line_index / config.spec_line_index 读取商品行和规格行。
4. 使用 config.product_segment_text / config.spec_segment_text 作为客户手动指定片段的优先值。
5. 使用 config.quantity_segment_text / config.size_segment_text 作为数量和尺码的优先值。
6. 没有手动数量和尺码时，才使用后端统一推断。
7. 后端推断规则应复用阶段 39 已收紧的口径，避免把秒45、范27等商品编号误判为尺码。
8. 输出字段必须可重复计算，同一条明细和同一条规则多次应用应得到稳定结果。
```

## 后端整改

```text
新增模板规则应用服务，例如 backend/app/services/print_template_rules.py。
服务中提供纯函数 apply_custom_text_lines_rule(field_values, config)。
服务中提供按 workspace 批量应用的函数。
采集解析生成 standard_details 时，如果已有匹配的启用模板规则，自动应用一次。
新增或收紧 API，支持对单个 print_template_config 试算和批量应用。
批量应用时只更新同 workspace、同 waybill_mode、同 source_template_key 的 standard_details。
更新 print_template_config 后，可以让用户手动点击批量应用，避免保存规则时误批量覆盖。
删除或禁用模板规则时，不删除原始 custom_area_* 字段；已派生 custom_* 字段应标记为 missing_config 或在重算时清空。
```

建议 API：

```text
POST /api/v1/print-template-configs/{id}/preview
POST /api/v1/print-template-configs/{id}/apply
```

`preview` 输入可选 `standard_detail_id`，返回试算结果但不落库。  
`apply` 返回应用数量、跳过数量、空结果数量。

## 前端整改

打印模板规则页：

```text
新增“试算当前样本”能力，展示后端返回的 custom_* 字段。
新增“应用到已采集面单”按钮。
应用前弹出确认，说明只影响当前工作区和当前模板来源的已采集面单。
应用后刷新当前模板定义和样本状态。
```

商品识别页：

```text
选择我打模板后，候选主文字优先读取 custom_product_text。
规格 / 补充优先读取 custom_spec_text、custom_size_text、custom_quantity_text。
如果 custom_* 字段还没有生成，则提示先到“打印模板规则”应用模板。
保留 custom_area_raw_text 作为诊断查看，不再作为保存规则时的主候选。
移除我打候选中的前端临时尺码 / 数量推断主口径。
```

## 测试要求

后端测试：

```text
1. custom_text_lines_v1 能按行号和片段生成 custom_product_text / custom_spec_text。
2. 手动填写的 size_segment_text / quantity_segment_text 优先于自动推断。
3. 自动尺码推断不会把秒45、范27等商品编号误判为尺码。
4. 批量应用只更新当前 workspace 的 standard_details。
5. source_template_key 不匹配时不应用规则。
6. 没有匹配规则时，状态为 missing_config，原始 custom_area_raw_text 不丢失。
```

前端验证：

```text
1. 打印模板规则页可以试算当前样本。
2. 点击“应用到已采集面单”后，商品识别页能看到 custom_* 拆分结果。
3. 商品识别页选择我打模板后，不再把整段原文作为主候选。
4. 未应用模板时，页面提示先应用模板规则。
```

## 验收标准

```text
后端 pytest 通过。
前端 vue-tsc --noEmit 通过。
tenant-ui Docker 构建通过并重启。
backend Docker 构建通过并重启。
浏览器验证 /admin/print-template-rules 可试算并批量应用。
浏览器验证 /admin/matching 我打候选读取 custom_product_text / custom_spec_text / custom_quantity_text / custom_size_text。
当前工作区已有我打面单应用后，商品识别候选不再展示模板样例或纯前端临时推断结果。
```

## 风险与注意事项

```text
1. 不要把商品、尺码、数量的具体业务关系写死在平台代码里。
2. custom_* 字段是客户模板规则的派生结果，不是平台默认业务含义。
3. 同一工作区可能有多个客户模板定义，必须按 config.source_template_key 和用户选择的 config 精确应用。
4. 批量应用必须保护 workspace_id 和 tenant_id 边界。
5. 保存规则和批量应用最好分开，防止客户误点保存导致旧面单被重算。
6. 删除模板规则后，要避免商品识别页继续使用过期 custom_* 结果。
```

## 本阶段不做

```text
1. 不做一单多商品拆多行。
2. 不做最终报货 Excel 汇总。
3. 不做图片 / 档口自动匹配整改。
4. 不做平台解析模板管理页扩展。
5. 不做抖店字段规则自定义。
```

## 后续任务

```text
1. 一单多商品拆分为多条业务行。
2. 商品识别命中后进入 SKU 自动匹配和图片状态。
3. 把 custom_* 字段接入整理文档和报货 Excel 导出。
4. 模板规则变更后提供更清晰的重算记录和异常提示。
```
