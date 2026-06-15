# 阶段 47：商品规则模板指纹兜底修复任务书

## 背景

业务现场反馈：商品识别规则已经存在，但识别预览里“一个都匹配不到”。

现场数据库排查后确认，规则本身和关键词不是主要问题。问题发生在规则执行前的模板过滤阶段：

```text
规则绑定模板配置 ID：4 / 5。
部分已采集面单保存的模板配置 ID 为空。
部分已采集面单保存的是已删除旧模板 ID：1。
这些面单实际都带有稳定的 printXML 版式指纹，例如 printxml:c863897829c2。
```

因此旧逻辑只按模板配置 ID 判断时，会把本该命中的规则全部过滤掉。

## 目标

```text
1. 商品识别规则不再只依赖会变化的模板配置 ID。
2. 已采集历史面单即使模板 ID 为空或过期，也能按版式指纹匹配规则。
3. 新建规则时保存真实版式指纹，避免后续复发。
4. 不要求用户清空规则或重建规则。
```

## 整改内容

### 后端识别引擎

文件：

```text
backend/app/services/product_recognition.py
```

调整：

```text
rule_applies_to_row 支持按 print_template_source_key / source_template_key / print_template_key 判断。
模板匹配优先级：版式指纹 > 模板配置 ID > 模板名称。
字段列表兼容历史逗号字符串保存方式。
```

### 后端接口层

文件：

```text
backend/app/api/routes/collector_runtime.py
```

调整：

```text
识别预览 / 导出前读取规则时，按当前 print_template_configs 给旧规则临时补齐 print_template_source_key。
补齐时读取当前工作区的模板历史记录，包括已软删除模板，避免用户删除模板后旧规则丢失版式指纹。
补齐逻辑不写回数据库，不修改用户已有业务数据。
```

### 前端规则保存

文件：

```text
frontend/src/views/workbench/MatchingReviewView.vue
```

调整：

```text
新建商品识别规则时，同时保存模板配置 key 和真实 printXML 版式指纹。
```

## 真实数据验证

当前规则补齐结果：

```text
规则 1：模板1 -> printxml:cb9c8469df0b
规则 2：模板2 -> printxml:c863897829c2
规则 4：模板2 -> printxml:c863897829c2
```

当前批次结果：

```text
15:01 批次：12 个商品行，已匹配 10 个，2 个 SKU 未命中。
17:11 批次：2 个商品行，已匹配 2 个。
17:49 批次：3 个商品行，商品未命中；原因是尚未建立秒67 175 / 默认类商品主类规则。
```

## 验证命令

```text
docker compose exec -T backend python -m pytest /app/backend/tests/test_product_recognition.py /app/backend/tests/test_recognition_report_export.py
npm run build:tenant
git diff --check
docker compose up -d --build backend tenant-ui
```

验证结果：

```text
后端 pytest：9 passed。
前端构建：通过。
Docker 重建：backend / tenant-ui 已启动。
浏览器：127.0.0.1:5173 可加载登录页。
```

## 后续事项

```text
1. 给秒67 175 / 默认类商品建立商品主类规则后，再验证 17:49 批次。
2. 若 SKU 仍未命中，检查对应 SKU 名称、关键词或备注兜底字段。
3. 模板重命名、删除、重建不应再依赖内部 ID；识别以版式指纹作为同类面单身份。
```
