---
name: audio-restore
description: 为直播切片规划音量、淡入淡出、降噪及爆音处理建议。用于音频预处理评估，只输出带能力状态的参数计划，不直接修复文件或虚构OpenFilm原生能力。
metadata:
  version: "0.1.0"
  author: openfilm-cut
---

# 音频修复参数规划

输入：原片与切片时间范围、音频问题描述、可用的实测电平/响度/削波证据、目标平台，以及执行引擎当前版本的能力说明。没有音频或检测结果时，标注 `assessment: unmeasured`，不虚构噪声强度、LUFS或峰值。

只输出计划，不处理音频文件。精品模式优先保证说话清晰和原声质感；用户限制为基础音量处理时，不安排专业修复。

## 能力映射

`audio_normalize`、`noise_reduce`、`clip_reduction`、`fade_in`、`fade_out` 是本技能的**规划字段**，不是承诺存在的OpenFilm命令。创建计划前读取调用方提供的版本能力，无法核实则 `native_mapping: null`、`status: needs_capability_check`。只为已核实能力填写实际映射。

已在OpenFilm 0.2.5核实的边界（其他版本须重新核实）：

- `<video>`/`<audio>` 的 `volume` 是线性固定增益，1为原电平，不是LUFS动态归一化。
- `overrides='[{"fade":[in_seconds,out_seconds]}]'` 是原生淡入淡出；同一视频上的fade同时影响画面与声音。
- 没有已核实的 `audio_normalize`、`noise_reduce`、`clip_reduction` 独立命令。不能把希望的降噪/修复参数直接写入film.html。无支持的复杂修复标为 `manual_required`，只输出人工点位。

有可靠的峰值测量时，可建议固定增益：`gain_db = target_peak_dbfs - measured_peak_dbfs`，`volume = 10 ** (gain_db / 20)`，留编码余量并在导出后复测。固定增益不改变动态范围，不能同时保证目标LUFS与峰值。增益不能修复已经失真的削波。区分采样峰值dBFS与真峰值dBTP，不互相冒用。

## 输出

JSON 对象：

- `clip_id`、`source_start`、`source_end`、`assessment`。
- `measurements`：实际测得的数值及检测来源；未知值为 `null`。
- `requested_targets`：目标LUFS、峰值及理由；目标不是实测或处理结果。
- `operations`：对象，包含上述5个规划字段。每项含 `requested`、`parameters`、`status`、`native_mapping`、`reason`；不适用参数用 `null`，不能把null转换成执行指令。
- `manual_markers`：复杂降噪、爆音或喷麦问题的位置、证据、说明。未取得成片映射时只给原片时间。
- `execution_status: planning_only`。

只有用户授权的执行步骤才能把 `status: supported` 的项转换为真实引擎语法；本技能不安装其他处理工具、不调用其他技能，也不把计划输出描述为修复完成。
