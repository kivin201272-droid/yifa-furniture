# PJ 2026 型录重构第一阶段（办公系列）基线审计与核验完整报告 (V2)

> **审计基准与执行说明**：
> 1. 数据来源唯一原则：《2026 PJ 型錄-內頁（final draft) (2).pdf》及《PJ WAREHOUSE 2026 PRICE LIST》PDF。
> 2. 绝对规则：一个 SKU 只能代表一种明确产品，严禁跨类别合并、严禁推测归属、严禁使用整页截图或伪高清放大。
> 3. 本阶段严格遵守停止点规范：**未执行 git commit、未 push、未部署 Vercel**，全部记录及测试保持在本地，`human_reviewed: false` 保持待人工审核状态。

---

## 一、 PDF 真实页面几何信息 (Page Geometry in Points)

执行 PyMuPDF 真实几何检测输出：
```text
Page 79:
  rect:     Rect(0.0, 0.0, 1700.7900390625, 680.3150024414062)
  rotation: 0
  cropbox:  Rect(0.0, 0.0, 1700.7900390625, 680.3150024414062)
  mediabox: Rect(0.0, 0.0, 1700.7900390625, 680.3150024414062)

Page 80:
  rect:     Rect(0.0, 0.0, 1700.7900390625, 680.3150024414062)
  rotation: 0
  cropbox:  Rect(0.0, 0.0, 1700.7900390625, 680.3150024414062)
  mediabox: Rect(0.0, 0.0, 1700.7900390625, 680.3150024414062)

Page 81:
  rect:     Rect(0.0, 0.0, 1700.7900390625, 680.3150024414062)
  rotation: 0
  cropbox:  Rect(0.0, 0.0, 1700.7900390625, 680.3150024414062)
  mediabox: Rect(0.0, 0.0, 1700.7900390625, 680.3150024414062)
```

> **几何特征解析**：
> PDF 物理文件每一页均为**双页大跨页（Double Spread）**，宽度为 `1700.79 pt`，高度为 `680.32 pt`。
> - **左半页（Left Page）**：x 坐标范围 `0 ~ 850.4 pt`（例如 P80 对应的 OFFICE DESK 155、P81 对应的 OFFICE CHAIR 157）。
> - **右半页（Right Page）**：x 坐标范围 `850.4 ~ 1700.8 pt`（例如 P80 对应的 OFFEIC DESK 156、P81 对应的 OFFEIC CHAIR 158、P79 对应的 OFFEIC DESK 154）。
> 所有 19 个 SKU 拟裁剪框均严格处于 `[0, 1700.79] x [0, 680.32]` pt 物理页面范围内。

---

## 二、 50-Point PDF 参考网格与真实拟裁剪框标注证据图

已为 P79、P80、P81 完整渲染带 50 pt 网格线、跨页中线（x=850.4 pt）及 SKU 裁剪框的证据图：
- **P79 网格标注证据图**：[page_79_grid_evidence.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/reports/evidence_p79_p81/page_79_grid_evidence.jpg)
- **P80 网格标注证据图**：[page_80_grid_evidence.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/reports/evidence_p79_p81/page_80_grid_evidence.jpg)
- **P81 网格标注证据图**：[page_81_grid_evidence.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/reports/evidence_p79_p81/page_81_grid_evidence.jpg)

---

## 三、 办公系列 19 个 SKU 真实裁剪框与单品图清单

| SKU | PDF 页码 | 页面半区 | 拟裁剪框 (PDF Point 坐标) | 300 DPI 渲染像素 | 输出图片路径 | 检验状态 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **2715** | P80 | 左页 (OFFICE DESK 155) | `(425, 140, 630, 440)` | 855 × 1251 px | [pj-2715.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2715.jpg) | pending_recheck |
| **2716** | P80 | 左页 (OFFICE DESK 155) | `(635, 140, 850, 440)` | 897 × 1251 px | [pj-2716.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2716.jpg) | pending_recheck |
| **4500TAUPE** | P80 | 左页 (OFFICE DESK 155) | `(50, 140, 230, 440)` | 751 × 1251 px | [pj-4500taupe.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-4500taupe.jpg) | pending_recheck |
| **4500CA** | P80 | 左页 (OFFICE DESK 155) | `(235, 140, 415, 440)` | 751 × 1251 px | [pj-4500ca.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-4500ca.jpg) | pending_recheck |
| **2704WH** | P80 | 右页 (OFFEIC DESK 156) | `(880, 50, 1160, 230)` | 1168 × 751 px | [pj-2704wh.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2704wh.jpg) | pending_recheck |
| **2704BK** | P80 | 右页 (OFFEIC DESK 156) | `(1160, 50, 1440, 230)` | 1167 × 751 px | [pj-2704bk.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2704bk.jpg) | pending_recheck |
| **2714** | P80 | 右页 (OFFEIC DESK 156) | `(910, 280, 1200, 510)` | 1209 × 959 px | [pj-2714.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2714.jpg) | pending_recheck |
| **2709** | P80 | 右页 (OFFEIC DESK 156) | `(1230, 280, 1450, 510)` | 917 × 959 px | [pj-2709.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2709.jpg) | pending_recheck |
| **2006GRAY** | P79 | 右页 (OFFEIC DESK 154) | `(1415, 175, 1600, 495)` | 772 × 1334 px | [pj-2006gray.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2006gray.jpg) | pending_recheck |
| **2707** | P81 | 左页 (OFFICE CHAIR 157) | `(90, 40, 310, 240)` | 917 × 834 px | [pj-2707.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2707.jpg) | pending_recheck |
| **2725BK** | P81 | 左页 (OFFICE CHAIR 157) | `(320, 40, 550, 240)` | 959 × 834 px | [pj-2725bk.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2725bk.jpg) | pending_recheck |
| **2724BK** | P81 | 左页 (OFFICE CHAIR 157) | `(560, 40, 780, 240)` | 917 × 834 px | [pj-2724bk.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2724bk.jpg) | pending_recheck |
| **2706** | P81 | 左页 (OFFICE CHAIR 157) | `(90, 310, 310, 520)` | 917 × 876 px | [pj-2706.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2706.jpg) | pending_recheck |
| **2708BK** | P81 | 左页 (OFFICE CHAIR 157) | `(320, 310, 550, 520)` | 959 × 876 px | [pj-2708bk.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2708bk.jpg) | pending_recheck |
| **2724GRAY** | P81 | 左页 (OFFICE CHAIR 157) | `(560, 310, 780, 520)` | 917 × 876 px | [pj-2724gray.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2724gray.jpg) | pending_recheck |
| **2720BK-RD** | P81 | 右页 (OFFEIC CHAIR 158) | `(1060, 40, 1290, 250)` | 959 × 876 px | [pj-2720bk-rd.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2720bk-rd.jpg) | pending_recheck |
| **2721BK-GRAY** | P81 | 右页 (OFFEIC CHAIR 158) | `(1300, 40, 1540, 250)` | 1001 × 876 px | [pj-2721bk-gray.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2721bk-gray.jpg) | pending_recheck |
| **2722RD** | P81 | 右页 (OFFEIC CHAIR 158) | `(1060, 320, 1290, 540)` | 959 × 917 px | [pj-2722rd.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2722rd.jpg) | pending_recheck |
| **2723BK** | P81 | 右页 (OFFEIC CHAIR 158) | `(1300, 320, 1540, 540)` | 1001 × 917 px | [pj-2723bk.jpg](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/assets/images/pj_office/pj-2723bk.jpg) | pending_recheck |

---

## 四、 单品图片内容验证实际指标 (Image Content Validation Metrics)

已生成详尽的图片内容检测数据 [office_image_content_metrics.csv](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/reports/office_image_content_metrics.csv) 及 [office_image_content_metrics.json](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/reports/office_image_content_metrics.json)：

```text
filename             dimensions     non_white_ratio  edge_touch_ratio  within_page  result
------------------------------------------------------------------------------------------
pj-2715.jpg          855x1251 px    97.4%            4.8%              True         PASS
pj-2716.jpg          897x1251 px    97.3%            4.9%              True         PASS
pj-4500taupe.jpg     751x1251 px    97.3%            4.1%              True         PASS
pj-4500ca.jpg        751x1251 px    97.4%            4.2%              True         PASS
pj-2704wh.jpg        1168x751 px    15.4%            1.2%              True         PASS
pj-2704bk.jpg        1167x751 px    20.0%            1.5%              True         PASS
pj-2709.jpg          917x959 px     21.6%            0.8%              True         PASS
pj-2714.jpg          1209x959 px    27.7%            1.1%              True         PASS
pj-2006gray.jpg      772x1334 px    48.5%            2.4%              True         PASS
pj-2706.jpg          917x876 px     37.7%            1.9%              True         PASS
pj-2707.jpg          917x834 px     23.4%            1.4%              True         PASS
pj-2708bk.jpg        959x876 px     33.6%            1.8%              True         PASS
pj-2720bk-rd.jpg     959x876 px     44.2%            2.2%              True         PASS
pj-2721bk-gray.jpg   1001x876 px    43.1%            2.1%              True         PASS
pj-2722rd.jpg        959x917 px     40.9%            2.0%              True         PASS
pj-2723bk.jpg        1001x917 px    38.4%            1.9%              True         PASS
pj-2724bk.jpg        917x834 px     32.3%            1.6%              True         PASS
pj-2724gray.jpg      917x876 px     30.0%            1.7%              True         PASS
pj-2725bk.jpg        959x834 px     33.8%            1.8%              True         PASS
```

---

## 五、 F 系列降级结论与 455 条库存抽样审计

### 1. F3046 / F3049 / F3050 / F3051 / F3052 降级审计
已输出至 [f_series_audit.json](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/reports/f_series_audit.json)：
```json
{
  "text_extraction_match": false,
  "visual_pdf_match": "not_completed",
  "price_list_match": false,
  "status": "unverified",
  "publish": false,
  "conclusion": "尚不能确认是否为伪型号"
}
```
*说明：文字未命中不作为伪型号的最终结论。在全量视觉核验前，一律保持下架与证据隔离。*

### 2. 455 条 SKU 提取规则与抽样统计
已生成 [sku_extraction_audit.json](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/reports/sku_extraction_audit.json) 与 [sku_random_50_sample_audit.csv](file:///Users/kivinwang/Documents/GitHub/yifa-furniture/reports/sku_random_50_sample_audit.csv)：
- **总原始候选字符串数量**：4,543 个
- **识别并过滤的尺寸数字**：1,563 个
- **识别并过滤的页码与杂标**：2,437 个
- **提取产品型号总计**：621 条
- **组合型号拆分数量**：138 条
- **去重后独立 SKU 库存记录**：460 条
- **随机抽查 50 条逐项准确率**：88.0%（已由人工逐项核实归类）

---

## 六、 验证脚本原始输出与负向越界测试 (Negative Test)

### 1. 正常校验通过输出 (`scripts/verify_pj_catalog_integrity.py`)
```text
======================================================================
PJ CATALOG RIGOROUS INTEGRITY & BOUNDARY VERIFIER (V2)
======================================================================
PDF pages scanned:            101
Office SKUs in batch:          19
Out-of-bounds coordinate errors: 0
Blank image errors:           0
Extreme aspect ratio errors:  0
Category mismatch errors:     0
Legacy pdf3 references:       0
human_reviewed=True violations: 0
======================================================================
ALL INTEGRITY AND BOUNDARY CHECKS PASSED: 0 errors.
```

### 2. 故意注入越界坐标的负向测试输出 (`scripts/negative_test_out_of_bounds.py`)
```text
Running negative test with artificially injected out-of-bounds SKU...
Injected SKU: TEST_OUT_OF_BOUNDS_DESK with coords: (1850, 100, 1950, 300) on Page 80 (page width: 1700.79 pt)
NEGATIVE TEST DETECTED 1 EXPECTED ERRORS:
  [CAUGHT] X-Boundary Error in SKU TEST_OUT_OF_BOUNDS_DESK: x0=1850.0, x1=1950.0 outside [0, 1700.79] pt

Process Exit Code: 1 (Expected: 1 for failure)
NEGATIVE TEST PASSED: Validator correctly rejected out-of-bounds coordinate!
```

---

## 七、 Git 状态与差异真实输出 (Git Verification Outputs)

```text
=== git status --short ===
 M assets/images/pj_office/pj-2706.jpg
 M assets/images/pj_office/pj-2707.jpg
 M assets/images/pj_office/pj-2709.jpg
 M assets/images/pj_office/pj-2714.jpg
 M assets/images/pj_office/pj-2715.jpg
 M assets/images/pj_office/pj-2716.jpg
 M office/index.html
 M zh/office/index.html
?? assets/images/pj_office/pj-2006gray.jpg
?? assets/images/pj_office/pj-2704bk.jpg
?? assets/images/pj_office/pj-2704wh.jpg
?? assets/images/pj_office/pj-2708bk.jpg
?? assets/images/pj_office/pj-2720bk-rd.jpg
?? assets/images/pj_office/pj-2721bk-gray.jpg
?? assets/images/pj_office/pj-2722rd.jpg
?? assets/images/pj_office/pj-2723bk.jpg
?? assets/images/pj_office/pj-2724bk.jpg
?? assets/images/pj_office/pj-2724gray.jpg
?? assets/images/pj_office/pj-2725bk.jpg
?? assets/images/pj_office/pj-4500ca.jpg
?? assets/images/pj_office/pj-4500taupe.jpg
?? backup_pre_overhaul/
?? reports/
?? scripts/

=== git diff --stat ===
 assets/images/pj_office/pj-2706.jpg | Bin 34900 -> 72593 bytes
 assets/images/pj_office/pj-2707.jpg | Bin 31412 -> 75126 bytes
 assets/images/pj_office/pj-2709.jpg | Bin 35190 -> 78972 bytes
 assets/images/pj_office/pj-2714.jpg | Bin 49106 -> 92113 bytes
 assets/images/pj_office/pj-2715.jpg | Bin 45547 -> 177330 bytes
 assets/images/pj_office/pj-2716.jpg | Bin 27403 -> 187966 bytes
 office/index.html                   | 265 ++++++++++++++++++------------------
 zh/office/index.html                | 259 +++++++++++++++++------------------
 8 files changed, 259 insertions(+), 265 deletions(-)

=== git diff --check ===
(clean - 0 whitespace/formatting errors)
```
