# 阶段 36：探索代码清理

## 背景

前期为了验证业务路径，曾经做过一些探索页面和临时入口：

```text
识别样本标注页。
识别导入预览页。
图片与档口独立管理页。
旧的 assets / recognition-preview / recognition-samples 路由重定向。
```

这些探索内容已经不在当前正式产品路径中。当前正式路径收敛为：

```text
客户业务页：采集记录、面单批次、异常处理、导出中心。
客户管理页：采集连接、商品/SKU、商品识别、导出表头。
平台后台：客户、工作区、用户、平台解析模式/模板维护。
```

## 目标

```text
删除不再被正式路由引用的探索页面文件。
删除只服务探索页面的样式残留。
修正旧资源地址重定向到当前正式页面。
保留历史任务书和进度记录，不覆盖阶段历史。
```

## 已完成

```text
删除 frontend/src/views/workbench/RecognitionSampleLabelView.vue。
删除 frontend/src/views/workbench/RecognitionImportPreviewView.vue。
删除 frontend/src/views/workbench/AssetsAndStallsView.vue。
移除客户管理路由中的 /admin/assets、/admin/recognition-samples、/admin/recognition-preview。
旧 /admin/image-assets、/admin/stalls、/image-assets、/stalls 直接重定向到 /admin/products。
旧 /admin/field-definitions、/field-definitions 直接重定向到 /admin/export-headers。
删除 sample-label-layout、sample-raw-panel、sample-segment-section、sample-section-title 等探索页样式。
保留导出表头仍在使用的 field-sample 和 sample-active-segment 样式。
```

## 验证

```text
后端 pytest 通过：7 passed, 1 warning。
tenant-ui Docker 构建通过。
platform-admin-ui Docker 构建通过。
前端源码中已无 RecognitionSampleLabelView、RecognitionImportPreviewView、AssetsAndStallsView 引用。
```

## 当前结论

```text
探索页面已从正式代码中删除，不再作为软删除代码长期保留。
历史任务书继续保留，作为阶段过程记录。
当前客户管理页保留最小正式入口：采集连接、商品/SKU、商品识别、导出表头。
```
