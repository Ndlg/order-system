# 阶段 24：面单原文识别样本标注 MVP

## 背景

复杂面单，尤其是“我打中转”这类自定义打印内容，不能只靠平台固定字段解析。

用户实际看到的是面单上的商品文字，例如商品款式、颜色、尺码、数量混在一起。客户管理员更容易通过“点选面单文字”的方式告诉系统：

```text
哪段文字代表商品
哪段文字代表规格
哪段文字代表尺码
哪段文字代表数量
```

本阶段先做最小可用标注页，用于验证交互和沉淀样本，不把复杂识别逻辑写死在系统中。

## 目标

```text
新增客户管理页“识别样本”。
客户可以粘贴面单商品原文。
系统把原文拆成候选片段。
客户点选候选片段，并放入商品关键词、规格、尺码、数量。
客户选择该原文对应的商品。
保存为当前工作区识别样本。
```

## 页面路径

```text
/admin/recognition-samples
```

## 数据保存策略

第一版暂不新增数据库表，复用当前工作区的 `match_rules` 保存样本：

```text
target_type: recognition_sample
target_id: 对应商品 ID
target_name: 对应商品名称
match_values.raw_text: 面单商品原文
match_values.product_keyword: 商品关键词
match_values.spec_text: 规格
match_values.size_text: 尺码
match_values.quantity_text: 数量
match_values.segments: 拆分出的候选片段
```

同时自动维护一个内部字段组合：

```text
key_field_sets.name: 识别样本字段
key_field_sets.purpose: recognition_sample
```

该字段组合不作为客户操作入口，只用于保存样本时满足现有数据结构。

## 已完成

```text
新增 RecognitionSampleLabelView.vue。
新增 /admin/recognition-samples 路由。
客户管理侧边栏增加“识别样本”入口。
客户管理首页增加“识别样本”卡片。
页面支持粘贴原文并拆分候选片段。
页面支持点击候选片段，并放入商品关键词、规格、尺码、数量。
页面支持尝试自动读取数量和尺码。
页面支持选择商品并保存样本。
页面支持查看已保存样本。
```

## 当前边界

```text
识别样本暂时只沉淀数据，不直接改变识别预览页的匹配结果。
自动填写只是辅助，不是最终识别算法。
后续需要把样本接入识别预览和整理文档生成流程。
后续可按使用效果决定是否把 recognition_sample 抽成独立数据表。
```

## 验证结果

```text
后端 pytest 通过：5 passed, 1 warning。
tenant-ui Docker 构建通过。
tenant-ui 容器已重启。
浏览器验证 /admin/recognition-samples 页面正常打开。
浏览器验证粘贴样例文本后可拆出候选片段。
```

## 下一步建议

```text
用真实采集批次挑选几条难识别面单，保存为样本。
把识别预览页接入识别样本：
  先命中商品关键词。
  再从样本中学习规格、尺码、数量的提取方式。
提供未识别行的快捷“转为样本”按钮。
形成“采集 -> 预览 -> 未识别 -> 标样本 -> 再预览”的闭环。
```
