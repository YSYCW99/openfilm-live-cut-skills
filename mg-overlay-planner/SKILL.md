---
name: mg-overlay-planner
description: 为财经等口播切片规划MG动画卡点、信息卡片和重点标注，输出成片点位与本地素材引用并避让人脸。只做规划，不生成动画、下载素材或执行剪辑。
metadata:
  version: "0.1.0"
  author: openfilm-cut
---

# MG透明动画点位规划

输入：完整切片文稿、成片时间轴、平台、画布尺寸、本地动画清单、人物活动区域、字幕和钩子保留区。清单应包含实际路径、时长、尺寸、可编辑文字范围及已知alpha支持情况。

只有源时间时，先按剪接与变速映射为成片时间；只有文字时，不编造卡点秒数。没有本地素材时，保留点位建议但 `asset_file: null`、`status: awaiting_asset`，不能声称动画已经制作或插入。

## 支持的规划类型

- `3item-slide`：口播确有3个要点时，逐条滑入；不足3点时不能补造信息。
- `circle-arrow`：圈选原画面中的真实对象，箭头随对象位置变化；位置未知时待人工定位。
- `compare-card`：对比两组已在内容中出现的信息，不能新增数字或伪造优劣结论。
- `single-highlight`：单行重点文字强调。
- `tip-bubble`：短提示气泡。

## 避让与节奏

1. `no_cover_face=true`。右上/右下仅是候选位置，不代表天然无人脸。依据人物整个活动区及源画面变换到成片后的坐标，检查动画完整运动路径及入场/出场包围框。
2. 同时避让字幕、钩子和其他重要信息。无可靠人物区域时，优先使用整个源视频矩形外的空白区域；否则 `status: needs_layout_check`，不得标通过。
3. 匹配口播观点、数据、对比和强调的实际时刻；前3秒优先规划明确的视觉钩子，但不能遮挡脸或同时堆叠多个强动画。
4. 使用成片秒数，最多三位小数，满足 `0 <= timeline_t_in < timeline_t_out <= clip_duration`。间隔长短以可读性和口播为准，不能只按平均字数分配。
5. 仅引用已有本地透明素材。扩展名 `.mp4` 不保证有alpha；常见H.264 MP4不提供可直接假定的透明度。保留调用方素材要求，并标注实际codec/alpha核验状态；可用格式须由当前OpenFilm及渲染器核实，不能静默改格式或下载转码工具。

## 输出

JSON 对象 `clip_id`、`canvas`、`no_cover_face`、`overlays`。每个点位包含：

- `timeline_t_in`、`timeline_t_out`：成片秒数。
- `animation_type`：上述类型之一。
- `asset_file`：已确认本地路径或 `null`；`asset_in`、`asset_out` 指素材自身时间。
- `position`：`x`、`y`、`width`、`height`，成片画布像素，不能用原片坐标替代。
- `opacity`：0–1；`layer_note`：前后关系、入场方向及要强调的实际文字。
- `face_check`：`passed`、`needs_review` 或 `unknown`，附依据和安全余量。
- `status`：`planned`、`awaiting_asset`、`needs_layout_check` 或 `unsupported`。
- `native_mapping`：未核实前为 `null`。

`add_overlay` 是概念性动作名称，不是已核实的OpenFilm命令。当前已核实OpenFilm 0.2.5通过独立section中的 `<video>` 或 `<iframe>` 叠加素材/页面；轨道上方覆盖下方，位置由clip的left/top/width/height定义，动态页面由window.film.frame(t)驱动。这里只做规划，不能生成页面或动画文件，也不能写入film.html。后续由获授权的执行步骤核实真实语法并实施，遵守用户确认门槛及锁定轨道。
