---
name: broll-matcher
description: 根据切片全文和成片时间轴规划B-roll点位，匹配已提供的本地素材或返回待人工填充的标签。只输出规划，不自动下载、生成或插入素材。
metadata:
  version: "0.1.0"
  author: openfilm-cut
---

# B-roll匹配与点位

输入：切片全文、原片到成片的时间映射、主题、画布尺寸、人物与字幕保留区；可选本地素材清单、版权/使用范围信息，以及 `urgent` 模式。

## 规则

1. 精品模式按需要规划，加急模式默认返回空点位并说明关闭；用户明确要求时按其选择执行。
2. 只从实际提供的本地素材中匹配。缺少素材时 `asset_file: null`、`status: awaiting_asset`，给出可供人工查找的 `material_tag`，不编造素材ID或文件路径，不下载、不生成素材。
3. 选择能解释口播内容的画面，避免把示意/历史素材包装成当前事件现场。记录来源和使用限制；未知时标待核对，不能宣称已获授权。
4. `t_in`、`t_out` 为成片秒数，保留三位小数。每个区间满足 `0 <= t_in < t_out <= clip_duration`。原片时间先按已知变速/剪接映射换算，不直接拿原片秒数当成片秒数。
5. 不遮挡人脸、字幕和关键原始信息；不知道画面布局时仅给语义候选，不声称位置校验通过。无素材时原片继续播放，不留下黑洞。

## 输出

JSON 对象 `clip_id`、`enabled`、`reason`、`broll_points`。每个点位包括：

- `t_in`、`t_out`、`material_tag`、`asset_file`。
- `blend_mode`（默认 `normal`）、`opacity`（0–1）、`position`（画布像素的x/y/width/height）、`layer_note`。
- `status`（`matched`、`awaiting_asset`、`needs_layout_check`）、`source_note`、`rights_note`。
- `native_mapping`：未验证执行能力前为 `null`。

`insert_broll` 只能作为上层概念性动作标签，不能声称它是OpenFilm原生命令。已核实OpenFilm 0.2.5可用独立section轨道中的 `<video>` / `<img>` 及相对素材路径实现叠加，轨道顶部覆盖底部；执行时仍须核对版本并保留已有锁定轨道。本技能只输出数据，不写film.html或启动OpenFilm。遵守调用方技能白名单及确认门槛。
