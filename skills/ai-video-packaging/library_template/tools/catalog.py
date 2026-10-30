# AI 剪辑包装 Skill · 作者：大象学长（全网同名）· CC BY-NC 4.0
# 读 cases/*/case.json，更新 目录.md 里「编号总表」那一段（标记线以下自动生成，标记线以上的「场景 → 编号」表手写，不会被覆盖）
# 用法：python3 tools/catalog.py
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = '<!-- 以下是编号总表，由 tools/catalog.py 自动生成，不要手改 -->'
SECTIONS = {'L': '组合界面', 'BG': '动态背景', 'T': '大标题 / 大字', 'C': '小标题 / 关键词', 'E': '解释元素', 'S': '字幕', 'R': '待入库（复刻中）'}

cases = []
for f in sorted(ROOT.glob('cases/*/case.json')):
    d = json.loads(f.read_text(encoding='utf-8'))
    if d.get('status') == '不要' or d.get('hidden'):
        continue
    d['_dir'] = f.parent.name
    d['_preview'] = (f.parent / 'preview.mp4').exists()
    cases.append(d)

lines = [MARK, '', '## 编号总表', '']
for sec, name in SECTIONS.items():
    rows = [c for c in cases if c.get('section') == sec]
    if not rows:
        continue
    lines += [f'### {sec} · {name}', '', '| 编号 | 名字 | 什么时候用 | 怎么改 | 音效 | 预览 |', '|---|---|---|---|---|---|']
    for c in sorted(rows, key=lambda c: c['id']):
        cell = lambda k: str(c.get(k, '')).replace('|', '｜').replace('\n', ' ')
        pv = f'[看](cases/{c["_dir"]}/preview.mp4)' if c['_preview'] else '还没渲'
        lines.append(f'| {c["id"]} | {cell("name")} | {cell("when")} | {cell("how")} | {cell("sfx")} | {pv} |')
    lines.append('')

md = ROOT / '目录.md'
head = md.read_text(encoding='utf-8').split(MARK)[0].rstrip() + '\n\n' if md.exists() else '# 我的包装库\n\n'
md.write_text(head + '\n'.join(lines) + '\n', encoding='utf-8')
print(f'目录.md 已更新：{len(cases)} 个包装')
