# 我的包装库

用「AI 剪辑包装」Skill 建的包装库。结构：

- `目录.md`：场景 → 编号表 + 编号总表。剪片时 AI 先查这里。
- `cases/<编号>_<名字>/`：一个包装一个文件夹（`case.json` 说明、`effect.html` 模板、`preview.mp4` 预览）。
- `effects/lib.js`：所有模板共用的工具。
- `fonts/`、`sfx/`：字体和音效。
- `tools/`：`render.mjs`（模板 → 透明视频 / 预览）、`preview.mjs`（截静帧）、`catalog.py`（更新目录）、`cut_check.py`（查剪辑点脏帧）。

第一次用：`cd tools && npm install`（需要 Node.js 18+、ffmpeg、Chrome）。

试一下：
```bash
cd tools
node render.mjs ../cases/C04_黄色划线标签/effect.html --preview
python3 catalog.py
```
