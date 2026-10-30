from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'manifest.json').read_text(encoding='utf8'))
html='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>我的包装库 · 样片拆解</title><style>
*{box-sizing:border-box}body{margin:0;background:#f4f1eb;color:#302d28;font:15px/1.65 'Microsoft YaHei',sans-serif}header{padding:34px 5vw 25px;border-bottom:1px solid #d9d2c6;background:#faf8f4}h1{margin:0;font-size:32px}p{max-width:900px;margin:12px 0}.sub{color:#7a7167}nav{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}button,a.btn{font:inherit;border:1px solid #c9c0b2;border-radius:6px;background:#fff;padding:7px 14px;color:#302d28;cursor:pointer;text-decoration:none}button.active{background:#342f29;color:#fff}main{padding:24px 5vw}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:20px}.card{background:white;border:1px solid #ded7cd;border-radius:9px;overflow:hidden;cursor:pointer}.card img{width:100%;height:340px;object-fit:contain;background:#252320}.card .body{padding:14px}.card h3{font-size:16px;margin:0}.chip{font-size:12px;color:#826536}dialog{width:min(1080px,96vw);max-height:95vh;padding:24px;border:1px solid #cfc5b6;border-radius:12px;background:#faf8f4}dialog::backdrop{background:#000b}.close{float:right}.pair{display:flex;gap:20px;justify-content:center}.pair>div{width:min(36vw,290px)}video,iframe{display:block;width:100%;aspect-ratio:9/16;border:0;background:#282522}label{display:inline-block;font-size:13px;color:#6c6257}input{font:inherit;padding:5px;border:1px solid #c9c0b2;border-radius:4px;max-width:270px}#editor{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}#note{background:#efe8db;padding:10px;border-radius:6px}#choice{display:flex;gap:8px;flex-wrap:wrap;margin:15px 0}a{color:#725627}.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.small{font-size:12px}.status{font-size:12px;color:#9a7138}#progress{font-size:13px}@media(max-width:600px){header,main{padding:20px}.pair{gap:8px}dialog{padding:12px}.card img{height:300px}}</style>
<header><div class="sub">五条参考视频 / 竖屏 9:16 / 本地工作库</div><h1>我的包装库</h1><p>__COUNT__ 种包装已拆分成可复用初稿。先看原片位置与视觉结构，再逐项选择「要 / 改 / 不要」。所有项目仍为待评审，正式入库 0 项。</p><p class="sub small">每项包含原片截取、独立预览、文字与图片参数。预览为静音，未校准原片音效。花体字体、手工人物蒙版和卷页弯曲仍有复刻差异。</p><div class="row"><a class="btn" href="包装拆解表.md">打开拆解表</a><a class="btn" href="包装拆解表.csv" download>下载 CSV</a><button id="export">导出评审意见</button><span id="progress"></span></div><nav id="filters"></nav></header><main><div class="grid" id="grid"></div></main>
<dialog id="detail"><button class="close" id="close">关闭</button><h2 id="title"></h2><div class="sub" id="meta"></div><p id="when"></p><div class="pair"><div><label>原片 · 从代表位置起 3 秒</label><video id="ref" controls muted playsinline></video></div><div><label>模板 · 可改字预览</label><iframe id="tpl"></iframe></div></div><div class="row"><button id="play">同步播放</button><button id="stop">停在 1.8 秒</button><a id="download" download>下载模板预览 MP4</a><a id="source" target="_blank">打开模板文件</a></div><div id="editor"></div><div id="note"></div><div id="choice"><button data-choice="要">要</button><button data-choice="改">改</button><button data-choice="不要">不要</button><input id="comment" placeholder="修改意见，例如标题向上挪 20px"></div><div class="small sub">选择会保存在此浏览器。导出评审意见后交给 Codex，再更新正式目录与编号。</div></dialog>
<script>const DATA=__DATA__;const $=s=>document.querySelector(s);let filter=new URLSearchParams(location.search).get('source')||'全部',current,raf,begin;let reviews={};try{reviews=JSON.parse(localStorage.getItem('packaging-review-v1')||'{}')}catch{};const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));function path(c,f){return 'cases/'+c.folder+'/'+f}function save(){localStorage.setItem('packaging-review-v1',JSON.stringify(reviews));draw()}
function draw(){let d=DATA.filter(c=>filter==='全部'||c.source_video===filter||c.section===filter);$('#grid').innerHTML=d.map(c=>'<article class="card" data-id="'+c.id+'"><img loading="lazy" src="'+path(c,'poster.png')+'"><div class="body"><div class="chip">'+c.source_video+' / '+c.source_time.toFixed(1)+'s / '+c.section+'</div><h3>'+c.id+' '+esc(c.name)+'</h3><div class="status">'+(reviews[c.id]?.choice||'待评审')+'</div></div></article>').join('');$('#grid').querySelectorAll('.card').forEach(n=>n.onclick=()=>open(n.dataset.id));$('#progress').textContent=Object.keys(reviews).length+' / '+DATA.length+' 项已标记';}
for(let f of ['全部','V01','V02','V03','V04','V05','T','C','L','S','E']){let b=document.createElement('button');b.textContent=({T:'标题',C:'小标题 / 关键词',L:'组合界面',S:'字幕',E:'解释元素'})[f]||f;b.onclick=()=>{filter=f;$('#filters').querySelectorAll('button').forEach(x=>x.classList.toggle('active',x===b));draw()};$('#filters').append(b)}
function stop(){cancelAnimationFrame(raf);$('#ref').pause()}function send(t){$('#tpl').contentWindow.postMessage({type:'render',time:t},'*')}function open(id){stop();current=DATA.find(c=>c.id===id);$('#title').textContent=current.id+' '+current.name;$('#meta').textContent=current.source+' · '+current.status;$('#when').textContent='使用场景：'+current.when;$('#ref').src=path(current,'reference.mp4');$('#tpl').src=path(current,'effect.html')+'?preview=1';$('#tpl').onload=()=>send(1.8);$('#download').href=path(current,'preview.mp4');$('#source').href=path(current,'effect.html');$('#note').textContent=current.notes||'文字、图片与位置独立可改；对照原片确认后再入库。';$('#comment').value=reviews[id]?.comment||'';$('#editor').replaceChildren();for(let key of ['text','second','subtitle','brand','color','fontSize']){if(current.tpl[key]===undefined)continue;let lab=document.createElement('label');lab.textContent=({text:'主文字',second:'第二行',subtitle:'副标题',brand:'店名',color:'颜色',fontSize:'字号'})[key]+' ';let inp=document.createElement('input');inp.value=current.tpl[key];inp.oninput=()=>{$('#tpl').contentWindow.postMessage({type:'update',tpl:{[key]:key==='fontSize'?Number(inp.value):inp.value},time:1.8},'*')};lab.append(inp);$('#editor').append(lab)}$('#detail').showModal();}
$('#close').onclick=()=>{stop();$('#detail').close()};$('#detail').addEventListener('close',stop);$('#play').onclick=()=>{stop();$('#ref').currentTime=0;$('#ref').play();begin=performance.now();function tick(now){let t=(now-begin)/1000;if(t>3){stop();return}send(t);raf=requestAnimationFrame(tick)}raf=requestAnimationFrame(tick)};$('#stop').onclick=()=>{stop();$('#ref').currentTime=1.8;send(1.8)};$('#choice').querySelectorAll('button').forEach(b=>b.onclick=()=>{reviews[current.id]={choice:b.dataset.choice,comment:$('#comment').value,name:current.name};save();$('#meta').textContent=current.source+' · 已标记：'+b.dataset.choice});$('#comment').onchange=()=>{if(reviews[current.id]){reviews[current.id].comment=$('#comment').value;save()}};$('#export').onclick=()=>{let a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(reviews,null,2)],{type:'application/json'}));a.download='包装库评审意见.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};draw();</script></html>'''
(R/'index.html').write_text(html.replace('__DATA__',json.dumps(D,ensure_ascii=False)).replace('__COUNT__',str(len(D))),encoding='utf8')
readme='''# 我的包装库

来源：用户提供的五条视频。当前 __COUNT__ 个初稿，均为待评审；正式入库 0 项。

## 先看什么

1. `包装拆解表.md`：逐项列出代表时间、结构、动作和使用场景。
2. `index.html`：双击打开本地预览页，筛选视频/分类；点卡片查看原片与模板，同步播放并留下评审意见。
3. 每个 `cases/Rxx_名称/`：`effect.html` 是模板，`case.json` 是说明，`reference.jpg/mp4` 是原片，`preview.mp4` 是独立预览，`compare.jpg` 是左右对照。

## 复用

复制某个 case 文件夹到新项目，保留相对路径依赖（assets、effects、fonts），改 `effect.html` 顶部 TPL。主文字、颜色、字号、图片路径和 start/duration 为参数。preview=1 显示示意底图；透明文字层不加此参数时背景透明。图片槽支持 JPG/PNG，本机 Chrome 支持的视频槽可填写 MP4/WebM。实际剪辑使用原始无字视频、真实截图及透明人物素材。

本机重渲单个预览：`node tools/render_all.cjs R13`。
本机导出 1080×1920 ProRes 4444：`node tools/render_all.cjs R13 --alpha`。透明文字类为透明输出，组合界面自带底图为不透明画面。输出到该 case 的 export.mov。运行前检查 tools/runtime.json 中的本机依赖路径。

## 待确认的差异

- 花体以 Great Vibes 近似，原片字体未知。字体随库提供，许可见 fonts/OFL.txt。
- 没有无字原片与原始人物分层。部分预览改用相邻镜头；部分背景由静帧修补，人物为手工轮廓演示，发丝与衣边仍需精修。
- R25 的三个图片槽目前用同一人像占位，原片是三种不同姿态。
- R29 目前用透视翻入近似原片卷页，尚未实现弯曲网格。
- 预览为 360×640 / 15fps / 3 秒、静音。原片截取供动作对照，未逐帧校准所有出入点，未试听原片音效。
- 所有文本均为可编辑层。评论与商品页保留真实截图；截图内容本身须替换图片。

评审时按编号回复「要 / 改 / 不要」。预览页的选择仅保存在浏览器，不自动将模板标为正式入库。导出 JSON 交给 Codex 后再更新编号和目录。

## 来源与署名

工作流参考「AI 剪辑包装 Skill」，作者：大象学长（全网同名），CC BY-NC 4.0。原始说明：https://q52zkkpo8s.feishu.cn/wiki/CmwewoJnmibaRrkWcNec3FPfnRf 。用户提供的参考视频、照片和截图仅用于本次本地拆解与对照，权利归原作者。字体许可另见 fonts/OFL.txt。
'''
(R/'使用说明.md').write_text(readme.replace('__COUNT__',str(len(D))),encoding='utf8')
print('Gallery and instructions ready')
