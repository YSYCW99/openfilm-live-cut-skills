# OpenFilm Live Cut Skills

六个直播切片配套规划技能，版本0.1.0，作者标识openfilm-cut。各文件夹可以独立安装；不附带Whisper模型、素材库、动画资产或专业音频修复引擎。

- `live-highlight-selector`：全文预处理、高光筛选、原片时间和语义闭环。
- `content-compliance-scanner`：检查候选完整原文，输出风险证据及保留/排除清单。
- `audio-restore`：音频问题评估与参数规划，区分原生可执行和人工处理。
- `broll-matcher`：本地素材匹配或人工素材标签、成片插入点位。
- `platform-copy-writer`：分平台主标题、3条备选标题、话题和简介。
- `mg-overlay-planner`：透明MG动画点位、素材引用和人脸/字幕避让规划。

## 安装到Codex

在Codex中使用已安装的skill-installer，发送：

```text
$skill-installer 请从 https://github.com/YSYCW99/openfilm-live-cut-skills 安装这六个根目录技能：
live-highlight-selector
content-compliance-scanner
audio-restore
broll-matcher
platform-copy-writer
mg-overlay-planner
```

也可将所需文件夹完整复制到个人技能目录（通常为`~/.codex/skills/`），每个文件夹保留自己的`SKILL.md`。安装后下一轮对话可调用。安装不改变当前对话的技能白名单或用户批准门槛。

`SKILL.md`使用name、description及metadata字段；版本保存在metadata.version。manifest.yml保留发布描述，standard字段沿用提交者标记，不是认证或额外运行时协议；Codex入口是SKILL.md。

## 工作流

转写全文 → 高光筛选 → 文本自检 → 按需要规划MG/B-roll/音频 → 输出编排契约 → 用户确认 → 执行引擎 → 发布文案与检查。

六个技能均为说明与规划能力，不会自动互相调用、安装依赖、发布内容或启动渲染。只有调用方授权时才执行后续步骤；如果调用方只允许特定技能，白名单优先。上面的顺序是示例，具体交付顺序以用户要求为准。

## OpenFilm能力边界

已在OpenFilm 0.2.5核实：原生项目为film.html及其文件夹；speed变速、volume固定增益、overrides.fade淡入淡出；section轨道中的video/img/iframe用于编排。其他版本执行前重新核实。

`audio_normalize`、`noise_reduce`、`clip_reduction`、`insert_broll`、`add_overlay`是草案中的规划标签，不应当作已存在的原生命令。复杂降噪/爆音修复若不受支持，标人工处理；没有已核实素材则返回null并等待人工补充。MP4后缀不保证透明通道，不承诺.ofproj格式。

文本自检不是法律结论或平台审核保证。时间戳的毫秒显示不等于1毫秒精度。动画避脸须覆盖运动路径，不能只凭“右上角”就判定通过。

## 校验

```sh
python -m pip install PyYAML
python scripts/validate_skills.py
```

校验器检查六个入口与manifest的YAML、名称、版本及必填元数据；不替代真实素材上的行为评估。
