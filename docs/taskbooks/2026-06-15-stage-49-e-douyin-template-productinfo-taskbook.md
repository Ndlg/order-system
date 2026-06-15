# 阶段 49：E 盘抖店 productInfo 模板化整改

## 背景

当前 E 盘项目已恢复到 C 盘项目基线，状态接近“E 盘业务服务重启完成，尚未开始抖店模板整改”的进度点。

之前临时整改中出现过两个偏差：

```text
1. 抖店维护页暴露了过多平台 JSON 字段，用户被迫理解主字段、候选字段。
2. 后续又临时新增了“抖店备注原文”可见字段，偏离了最初要做成“像我打模板一样维护”的方向。
```

本阶段重新从 E 盘基线开始，先收紧目标，再开始改源码。

## 本阶段目标

```text
1. 只修改 E 盘项目，不再修改 C 盘项目。
2. 打印模板规则页重新纳入抖店模板维护入口，和我打模板共用同一个入口。
3. 抖店模板维护以 productInfo 作为唯一前台主原文。
4. 用户在 productInfo 原文预览中点击文字片段，定义标准字段：
   商品 / 销售属性1 / 销售属性2 / 数量 / 备注。
5. 保存后的抖店模板规则写入 print_template_configs，后端解析 standard_details 时应用该规则。
6. 后端输出统一标准字段，供商品识别和导出继续使用。
```

## 关键口径

```text
productInfo 是前台维护的主原文，等价于我打 printXML 中可见商品区原文。
productShortInfo、sPInfo、sPSInfo、buyerRemark、remark 等抖店字段只允许作为后台兜底候选，不在模板维护页面让用户直接维护。
页面不新增“抖店备注原文”独立区域。
页面不展示“主商品原文 / 候选字段”这种平台字段配置 UI。
```

## 非目标

```text
1. 不重新设计商品识别引擎。
2. 不改采集器。
3. 不清空业务数据。
4. 不改 C 盘项目。
5. 不新增可见的抖店备注字段入口。
6. 不把 productShortInfo 作为抖店模板前台主字段。
```

## 实施任务清单

### 1. 前端模板入口

```text
打印模板规则页保留我打模板能力。
同页增加抖店模板组。
抖店组标题显示平台为“抖店 / CloudPrint”。
抖店组内展示 productInfo 原文预览。
用户点击 productInfo 片段后，可赋值到标准字段。
当前已选字段区显示 商品 / 销售属性1 / 销售属性2 / 数量 / 备注。
保存后标准化预览只展示标准字段，不展示平台候选字段配置。
```

### 2. 前端保存结构

```text
抖店模板保存为 rule_type = platform_text_template_v1。
primary_text_field 固定为 product_full_text。
candidate_text_fields 后台保留 product_short_text、sp_info、sps_info、buyer_remark、seller_remark。
field_mappings 保存用户点选的 segment_text。
sample_preview 保存标准字段预览。
```

### 3. 后端解析应用

```text
parse_douyin_cloud_print 支持读取当前工作区 print_template_configs。
旧配置即使 primary_text_field 写成 product_short_text，也统一按 product_full_text 作为主字段。
存在 field_mappings 时，优先使用 segment_text 覆盖 custom_product_text、custom_sales_attr1_text、custom_sales_attr2_text、custom_quantity_text、custom_item_remark_text。
没有模板时继续保持原平台解析逻辑，不影响已有采集闭环。
```

### 4. 测试与验收

```text
后端测试覆盖：
- 抖店默认解析仍可输出标准字段。
- 抖店模板保存映射后，解析结果按 field_mappings 输出。
- 旧配置 primary_text_field 错写时，仍以 productInfo 为主字段。

前端检查：
- vue-tsc --noEmit 通过。
- 页面不出现“抖店备注原文”。
- 页面不出现面向用户的候选字段维护 UI。
```

### 5. 部署策略

```text
先完成源码和测试。
测试通过后再构建 backend 和 tenant-ui。
只重启 E 盘 backend / tenant-ui。
不动 Redis，不动数据卷。
```

## 风险与控制

```text
风险 1：旧抖店配置仍影响解析。
控制：后端统一归一 primary_text_field，避免旧配置把主字段拉回 productShortInfo。

风险 2：前端又暴露平台字段，导致用户理解成本上升。
控制：抖店维护页只展示 productInfo 原文和标准字段。

风险 3：已解析旧数据不会自动变化。
控制：说明新逻辑只影响后续解析或重新解析后的 standard_details。
```

## 验收口径

```text
1. 进入打印模板规则页，可以看到抖店模板维护入口。
2. 抖店维护区域只围绕 productInfo 原文选择字段。
3. 保存模板后，后端解析抖店面单时按模板映射生成标准字段。
4. 服务重启后 http://127.0.0.1:8000/ 和 http://127.0.0.1:5173/ 返回 200。
```

## 2026-06-15 执行记录

```text
本次按确认后的口径推进 E 盘项目：

1. 抖店结构化字段固定映射
   trackNo 继续保留为物流单号。
   templateCode 继续保留为模板来源。
   shopName 继续保留为店铺名。
   productInfo 直接写入 custom_product_text。
   productCount 直接归一为 custom_quantity_text。
   remark 直接写入 custom_item_remark_text。

2. 抖店模板只补销售属性
   保存规则类型实际落地为 douyin_product_info_v1。
   后端按 templateCode 查找当前工作区 print_template_configs。
   命中配置后，只从 productInfo 的 field_mappings 中读取 custom_sales_attr1_text / custom_sales_attr2_text。
   不再把 productShortInfo、sPInfo、sPSInfo 暴露为前台主维护字段。

3. 商品识别字段收口
   抖店、菜鸟直打、我打在商品识别配置里均收口为 4 个业务字段：
   商品信息 / 商品文字、销售属性1、销售属性2、备注字段。
   不再展示物流单号、订单号、店铺名、商品简称、规格文本、数量文字等干扰字段。

4. 打印模板规则入口
   打印模板规则页同时纳入抖店和我打模板。
   抖店样本读取 productInfo 作为原文。
   抖店页面只允许用户把 productInfo 片段赋值给销售属性1 / 销售属性2。
   商品、数量、备注在预览中自动来自 productInfo / productCount / remark。

5. 验证与部署
   后端针对性测试：
   docker run --rm -v <PROJECT_DRIVE>\...\order-system:/app -w /app order-system-backend:latest python -m pytest backend/tests/test_direct_print_standardization.py backend/tests/test_woda_template_config.py backend/tests/test_woda_printxml_parser.py
   结果：18 passed。

   前端验证：
   vue-tsc --noEmit 通过。
   vite build 通过。

   已重建并替换 E 盘 backend / tenant-ui。
   Redis 和数据卷未重建、未清空。
   健康检查：
   http://127.0.0.1:8000/ -> 200
   http://127.0.0.1:5173/ -> 200
```

## 2026-06-15 追加修正

```text
根据现场复核，打印模板规则入口继续收紧：

1. 模板维护第一层按打印组件分为两类：
   - 抖店打印组件
   - 菜鸟打印组件

2. 抖店不再按平台模板配置粗分，而是按采集样本中的 templateCode 归类。
   templateCode 等同于抖店面单模板指纹，用于判断“同一个模板”。

3. 菜鸟 / 我打继续按 printXML 布局指纹归类。

4. 抖店 productInfo 增加基础拆分：
   从最后一个 】 后面的尾部文字拆出销售属性1、销售属性2、数量候选。
   商品原文和数量仍由平台字段自动提供。
   模板维护时只允许用户选择销售属性1 / 销售属性2。

5. 后端同步增加 productInfo 基础拆分兜底：
   没有模板配置时，也会从 productInfo 尾部拆出 custom_sales_attr1_text / custom_sales_attr2_text。
   已保存模板配置时，仍以模板 field_mappings.segment_text 为准。

验证：
后端 targeted pytest：18 passed。
frontend vue-tsc --noEmit：通过。
frontend vite build：通过。
已重建并重启 E 盘 backend / tenant-ui。
健康检查：
http://127.0.0.1:8000/ -> 200
http://127.0.0.1:5173/ -> 200
```

## 2026-06-15 追加修正：回填抖店历史标准字段，消除 5.0 / 4.0 误冲突

```text
现场现象：
商品识别页中，抖店面单出现“商品名称同时命中多个商品：5.0、4.0”。
例如面单商品标题里同时带有 5.0 和 4.0，但实际规格尾部是 5.0二代白紫 / 40。

排查结果：
当前抖店商品规则只匹配 custom_sales_attr1_text，这是正确方向。
冲突原因不是规则本身，而是历史入库的抖店标准字段没有按新的 productInfo 拆分逻辑重算：
custom_sales_attr1_text 中仍然混入了整段商品标题，导致 5.0 和 4.0 同字段同时命中。

处理：
1. 使用当前后端解析逻辑重算未删除的 douyin_cloud_print 标准明细，共 62 条。
2. custom_sales_attr1_text 从“整段标题 + 属性”回填为干净的销售属性，例如：
   5.0二代白紫
   4.0二代黑灰
3. custom_sales_attr2_text 保持尺码，例如 40 / 42.5。
4. 同步补齐 print_template_config_id / print_template_config_key / print_template_config_label，
   让旧批次明细也关联到当前启用的抖店版式读取规则。

验证：
当前任务 17 重新跑识别预览：
total 119
matched 110
fallback_matched 3
product_unmatched 7
sku_unmatched 2
conflict 0

结论：
该冲突不合理，已通过回填历史标准字段消除。
剩余未命中属于商品规则或 SKU 资料缺失，不属于 5.0 / 4.0 互相误判。
```

## 2026-06-15 追加修正：删除识别规则后候选面单闪回“待识别”

```text
现场现象：
每次删除商品识别规则后，读取已采集面单区域会整体变成“待识别 / 识别中”，
需要等一会儿或再次刷新后才恢复识别结果。

排查结果：
后端删除 match_rules 只是软删除规则，不会把 standard_details 改成 pending。
问题在前端商品识别页：
删除规则后先调用 load()，load() 已经会重新请求本批次 recognition-preview；
但 removeRule() 下一行又把 recognitionPreview 清空，导致候选区退回 pending 展示。

修正：
移除删除规则后的 recognitionPreview.value = null。
现在删除规则后保留旧预览，后台重新拉取预览，返回后再替换成最新结果。

验证：
frontend vue-tsc --noEmit：通过。
frontend vite build：通过。
已只重建并重启 E 盘 tenant-ui。
http://127.0.0.1:5173/ -> 200。
```

## 2026-06-15 追加修正：读取规则必须绑定到具体版式

```text
现场复核发现：
我打组件下每个已识别版式都显示“自定义规则 2”，
这是错误展示。原因是前端把整个我打组件的规则总数展示到了每个版式上，
并且旧逻辑会用同组件第一条规则作为兜底。

修正：
1. 已识别版式状态改为按当前版式指纹统计：
   - 已配置
   - 已配置 N
   - 待配置
   - 系统默认（抖店默认读取）

2. 去掉“同组件第一条规则兜底”。
   自定义读取规则必须通过 source_template_key 绑定到当前版式指纹。

3. 自定义读取规则列表增加“绑定版式”列，
   明确每条规则服务哪个版式指纹。

当前概念：
版式 = 系统自动识别的分组依据，不需要用户创建。
读取规则 = 用户可选维护的字段拆分覆盖项，必须绑定版式。

验证：
frontend vue-tsc --noEmit：通过。
frontend vite build：通过。
已只重建并重启 E 盘 tenant-ui。
http://127.0.0.1:5173/ -> 200
```

## 2026-06-15 追加修正：版式指纹与读取规则概念收口

```text
现场复核发现：
页面把“系统识别出来的版式指纹”和“用户自定义字段读取规则”都叫模板，
导致用户误解为：既然系统已经识别了指纹，为什么还要再定义模板。

口径收口：
1. 版式指纹是系统自动识别的结果，用户不需要创建。
2. 字段读取规则是可选覆盖项。
   默认读取可直接使用，只有默认拆分不准时才需要新增或调整规则。

前端修正：
1. 页面标题从“打印模板规则”改为“版式与字段规则”。
2. “模板指纹列表”改为“已识别版式”。
3. “已定义模板列表”改为“自定义读取规则”。
4. “模板名称 / 新建定义 / 删除定义 / 保存修改”等文案统一改为
   “规则名称 / 新增规则 / 删除规则 / 保存规则”。
5. 抖店没有自定义规则时显示“系统默认”，不再显示“待定义”。
6. 抖店有自定义规则时显示“自定义规则 N”，表达这是覆盖规则，不是必须再建模板。

验证：
frontend vue-tsc --noEmit：通过。
frontend vite build：通过。
已只重建并重启 E 盘 tenant-ui。
http://127.0.0.1:5173/ -> 200
```

## 2026-06-15 追加修正：抖店模板组样本导航

```text
现场发现打印模板规则页在抖店组件下只看到 1 个样本。

排查结果：
当前采集任务 17 的抖店标准明细批次为 19，共 17 张抖店面单。
这些面单按 templateCode 分成 5 个模板组：
- yt_76_130_v2：10 张
- C1l6hp4vo0dyqw：3 张
- C1l6jpg5mc02kv：2 张
- C1l6hd3x4ctyqx：1 张
- C1l6htbykivlma：1 张

截图中选中的 YT0047668236931 属于 C1l6hd3x4ctyqx，这个模板组本身只有 1 张，
不是抖店只识别出 1 张，而是 UI 没有把“当前组件全部样本”和“当前模板组样本”区分清楚。

修正：
1. 打印模板规则页左侧新增“模板指纹列表”。
   按当前组件展示每个 templateCode / printXML 指纹组及样本数。

2. 右侧样本下拉继续只展示当前模板组内样本。
   同时显示：
   - 当前模板 N 张
   - 当前组件 N 张
   - 整批 N 张

3. 模板归类区域显示当前为第几个模板组，避免误以为只采集了一个样本。

验证：
frontend vue-tsc --noEmit：通过。
frontend vite build：通过。
已只重建并重启 E 盘 tenant-ui，未重启 backend，未触碰 Redis / 数据卷。
http://127.0.0.1:5173/ -> 200。
```

## 2026-06-15 追加修正：抖店模板指纹改为主模板 URL

```text
现场复核发现：
抖店同一个面单版式下，不同店铺会产生不同 templateCode。
因此 templateCode 不能作为跨店铺模板指纹。

进一步排查：
抖店原始 CloudPrint payload 的 contents 中包含 templateURL。
其中主模板 URL 形如：
https://lf3-cm.ecombdstatic.com/obj/logistics-davinci/template/v2/yuantong_76_130.xml

同一 payload 里还可能包含 publicElements / customerElements。
这些元素会随店铺变化，不能参与模板指纹。

修正：
1. 抖店 print_template_key 改为优先使用主 templateURL 归一后的 key：
   url:obj/logistics-davinci/template/v2/yuantong_76_130.xml

2. templateCode 继续保留为原始来源字段：
   field_values.template_code

3. print_template_source 改为 douyin_template_url。

4. 抖店模板配置不再把某张样本的 segment_text 当固定输出值。
   后端根据 extractor 动态读取 productInfo 中的销售属性1 / 销售属性2，
   避免同版式多店铺后把所有面单都读成同一个属性。

5. 前端打印模板规则页显示“抖店版式 yuantong_76_130.xml”，
   保存规则的匹配说明改为“抖店模板地址相同”。

当前库回填：
已把 62 条可定位 templateURL 的抖店标准明细回填为主模板 URL key。
已把 1 条已有抖店模板定义迁移到主模板 URL key。

复查：
当前抖店批次 19 已从 5 个 templateCode 组收口为 1 个版式组：
url:obj/logistics-davinci/template/v2/yuantong_76_130.xml
该组共 17 张，覆盖 5 个 templateCode 和 7 个店铺。

验证：
backend targeted pytest：19 passed。
frontend vue-tsc --noEmit：通过。
frontend vite build：通过。
已重建并重启 E 盘 backend / tenant-ui。
健康检查：
http://127.0.0.1:8000/ -> 200
http://127.0.0.1:5173/ -> 200
```
