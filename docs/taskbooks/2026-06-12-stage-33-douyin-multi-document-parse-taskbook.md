# 阶段 33：抖店一条打印任务多面单解析修复

## 背景

用户反馈：一轮采集中打印了两条抖店订单，但采集结果只显示一条面单。

排查确认：

```text
采集器确实只上传了一条 raw_capture_record。
但这条抖店打印组件记录里包含 task.documents = 2。
旧抖店解析器只从整份 JSON 中寻找一份最佳 data，因此只生成一条 standard_detail。
```

## 问题

```text
抖店打印组件可能把多张面单合并在同一条 task row 的 documents 数组中。
平台解析层必须按 documents 拆分面单。
不能把一条 raw_capture_record 简单等同于一张面单。
```

## 已完成

```text
抖店解析器新增按 task.documents[] 遍历。
每个 document 独立读取 data。
每个 document 独立生成一条 ParsedWaybill / StandardDetail。
field_values 增加 document_sequence。
保留旧兜底逻辑：如果 payload 没有标准 documents 结构，仍可按旧方式寻找一份 data。
后端测试新增“一条抖店 raw 中两个 document”用例。
对用户刚才的任务 10 执行强制重解析。
```

## 验证结果

```text
后端 pytest 通过：7 passed, 1 warning。
backend Docker 构建通过并已重启。
任务 10 强制重解析结果：
  detail 114: YT0043623738399 / document_sequence 1
  detail 115: YT0043296031991 / document_sequence 2
浏览器验证 /capture-records：
  任务 10 的“面单”列显示 2。
```
