# 阶段 35：框架收紧与验证入口整理

## 背景

当前平台框架已经基本搭好，进入业务闭环前需要先做一次收紧：

```text
确认本地测试入口稳定。
确认 Docker 构建入口稳定。
确认采集器默认名称符合用户部署习惯。
确认原始采集内容和下载文档不继续暴露过多内部编号。
```

## 目标

```text
从项目根目录直接运行 pytest 能识别 backend/app。
采集器名称默认预填 Windows 主机名，用户只需要填写账号密码并登录保存。
旧配置里的空采集器名称、本机采集器、业务机采集器自动归一为 Windows 主机名。
原始采集 Excel 下载列口径收紧为用户能理解的来源信息。
```

## 已完成

```text
新增 pytest.ini，固定 testpaths=backend/tests，pythonpath=backend。
采集器核心配置增加 default_collector_name 和 normalize_collector_name。
采集器 GUI 打开时使用规范化后的采集器名称。
collector-client/config.example.json 中 collector_name 留空，由程序自动使用 Windows 主机名。
原始采集 Excel 下载移除采集任务ID、原始文档ID、来源序号等内部列。
原始采集 Excel 下载改为 ID、采集器、电脑名、来源组件、采集时间、状态、采集原文。
解析模式、原文格式、本地来源信息、解析诊断不再放进用户下载的原文主表。
后端测试同步覆盖新的原始采集 Excel 表头，防止内部列重新暴露。
```

## 验证

```text
后端 pytest 通过：7 passed, 1 warning。
采集器 client.py 和 gui.py 编译通过。
采集器空名称、旧默认名称会归一为当前 Windows 主机名。
tenant-ui Docker 构建通过。
platform-admin-ui Docker 构建通过。
backend Docker 构建通过。
```

## 当前结论

```text
框架验证入口已经更稳定。
采集器默认部署体验已收紧。
原始采集内容的用户可见口径与页面保持一致。
下一步可以继续推进抖店业务闭环：采集 -> 解析 -> 商品识别 -> SKU 图片匹配 -> 用户定义导出表头 -> 生成报货 Excel。
```
