# 阶段 19：客户侧配置与大批量采集查看 MVP

> 阶段定位：平台端 MVP 先封板，开始推进客户业务页和客户管理页。目标是让用户大批量采集后能看清本轮商品信息，并能配置后续匹配所需的字段、关键字段、图片、档口和关键词规则。

## 1. 本阶段目标

```text
业务页按采集任务查看本轮商品信息。
业务页支持商品文字搜索、来源筛选和分页，准备承接大批量采集。
客户管理页从占位状态推进为最小可配置状态。
字段用途页展示平台解析层提供的字段，并自动同步到当前工作区字段配置。
关键字段页能保存默认组合，为图片和档口匹配提供字段基础。
图片与档口页能维护最小资料记录。
匹配规则页能建立“商品关键词 -> 图片 / 档口”的最小规则。
```

## 2. 已完成内容

业务页：

```text
frontend/src/views/workbench/WaybillBatchesView.vue

本轮商品信息表以商品文字为主列。
支持搜索商品文字、单号、店铺。
支持按来源筛选。
支持分页，默认每页 50 条。
接口读取上限提升到 2000，方便本轮大批量验证。
```

客户管理页：

```text
frontend/src/views/workbench/FieldDefinitionWizardView.vue
frontend/src/views/workbench/KeyFieldWizardView.vue
frontend/src/views/workbench/AssetsAndStallsView.vue
frontend/src/views/workbench/MatchingReviewView.vue
frontend/src/styles/base.css
backend/app/api/routes/resources.py
```

字段用途页：

```text
平台字段由系统解析模板提供，不让客户维护候选字段。
页面展示商品信息、规格文本、数量、来源、辅助单号等平台字段。
进入页面时自动把平台字段同步到当前工作区 field_definitions。
客户管理员只查看 / 后续配置字段是否用于匹配、显示和导出。
```

关键字段页：

```text
展示可用于匹配的字段。
支持一键保存商品匹配组合和来源追溯组合到 key_field_sets。
```

图片与档口页：

```text
支持手动新增图片资料记录。
支持手动新增档口资料记录。
```

匹配规则页：

```text
支持输入商品关键词。
支持选择匹配目标为档口或图片。
支持保存 match_rules。
支持展示当前关键词命中多少条商品信息。
```

## 3. 当前边界

```text
图片资料目前只是记录名称和路径 / 备注，尚未接真实图片上传。
匹配规则目前是关键词规则，尚未实现自动匹配引擎批量回写 image_match_status / stall_match_status。
Excel 导出还未接入本轮商品信息和匹配结果。
字段用途目前以平台默认用途为主，复杂编辑后置。
关键字段目前以默认保存为主，复杂编辑后置。
```

## 4. 验证结果

```text
后端 pytest -q 通过：4 passed, 1 warning。
py_compile 通过：resources.py、waybill_parser.py。
Docker backend / tenant-ui 构建通过。
Docker backend / tenant-ui 已重启。
浏览器验证：
  /waybill-batches 显示本轮商品信息、搜索和筛选。
  /admin/field-definition 显示平台字段和当前字段用途，不再显示候选保存状态。
  /admin/matching 显示新增规则和商品关键词。
```

## 5. 下一步建议

```text
1. 用户跑一轮大批量采集，观察本轮商品信息数量、搜索和分页表现。
2. 查看字段用途页，确认平台字段用途是否符合本工作区导出和匹配需要。
3. 在关键字段页保存默认组合。
4. 在图片与档口页维护少量测试资料。
5. 在匹配规则页建立几条关键词规则。
6. 下一阶段实现自动匹配执行按钮，并把匹配结果回写到商品明细。
```
