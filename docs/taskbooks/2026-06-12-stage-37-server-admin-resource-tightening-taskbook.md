# 阶段 37：服务端后台资源页收紧

## 背景

平台后台解析模式页仍然保留了早期通用资源管理器形态：

```text
直接显示数据库字段名。
显示 Manual upload 这类早期探索模式。
显示菜鸟云打印遗留模式。
右侧暴露 JSON 新建记录入口。
```

这些内容对平台开发者调试有用，但不适合继续作为正式服务端后台 UI。

## 目标

```text
服务端后台资源页不再暴露 JSON 新建记录框。
解析模式页只显示当前正式支持的解析模式。
解析模式页隐藏 Manual upload 和 cainiao_cloud_print 遗留模式。
解析模式页使用中文业务表头。
保留后端数据和历史记录，不破坏解析兼容逻辑。
```

## 已完成

```text
重写 ServerAdminResourceView.vue 为只读资源清单。
移除 createRecord、Plus 图标、payload JSON 编辑器和新建按钮。
为 tenants、workspaces、users、waybill-modes、waybill-templates、waybill-template-fields 配置固定中文列。
waybill-modes 页面仅显示 douyin_cloud_print、cainiao_direct_shop、cainiao_woda_printxml。
waybill-modes 页面不显示 Manual upload。
waybill-modes 页面不显示 cainiao_cloud_print 遗留模式。
删除已经不用的 resource-layout 和 editor-panel 样式。
```

## 验证

```text
后端 pytest 通过：7 passed, 1 warning。
tenant-ui Docker 构建通过。
platform-admin-ui Docker 构建通过。
platform-admin-ui 容器已重启。
浏览器验证 /admin/waybill-modes：
  表头为 解析模式 / 模式编码 / 数据来源 / 说明 / 状态。
  仅显示 3 条正式模式。
  不显示 Manual upload。
  不显示 cainiao_cloud_print 遗留模式。
  不显示 JSON 新建记录入口。
```

## 当前结论

```text
服务端后台解析模式页已经从通用数据库调试器收紧为正式资源清单。
后续客户、工作区、用户也应该继续从只读清单推进到专用维护表单，而不是恢复 JSON 编辑器。
```
