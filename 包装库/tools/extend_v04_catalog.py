from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFilter
import cv2,numpy as np
R=Path(__file__).resolve().parents[1]
# Improve the demo plates using unobstructed portions of the supplied source.
p=next(x['path'] for x in json.loads((R/'sources/sources.json').read_text(encoding='utf8')) if x['id']=='V04')
def frame(t):
 c=cv2.VideoCapture(p);c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read();c.release();return Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)).resize((720,1280))
im=frame(17.65);a=np.array(im);mask=np.zeros(a.shape[:2],np.uint8);mask[48:188,45:185]=255;mask[940:1008,50:670]=255;Image.fromarray(cv2.inpaint(a,mask,4,cv2.INPAINT_TELEA)).save(R/'assets/V04/ingredient_bg.jpg')
im=frame(24.8);patch=im.crop((360,650,720,1280)).transpose(Image.Transpose.FLIP_LEFT_RIGHT);mask=Image.new('L',patch.size,255);draw=ImageDraw.Draw(mask)
for x in range(50):draw.line((310+x,0,310+x,629),fill=round((49-x)/49*255))
im.paste(patch,(0,650),mask);a=np.array(im);mask=np.zeros(a.shape[:2],np.uint8);mask[546:625,245:630]=255;Image.fromarray(cv2.inpaint(a,mask,4,cv2.INPAINT_TELEA)).save(R/'assets/V04/rose_bg.jpg')
# The gallery must derive its counts and filters from the catalog.
f=R/'tools/make_gallery.py';s=f.read_text(encoding='utf8');a=s.index('for c in D:');b=s.index("html='''",a);s=s[:a]+s[b:]
s=s.replace('三条参考视频','四条参考视频').replace('30 种包装','__COUNT__ 种包装').replace("+' / 30 项已标记'","+' / '+DATA.length+' 项已标记'")
s=s.replace("['全部','V01','V02','V03','T','C','L']","['全部','V01','V02','V03','V04','T','C','L','S','E']")
s=s.replace("L:'组合界面'","L:'组合界面',S:'字幕',E:'解释元素'")
s=s.replace("html.replace('__DATA__',json.dumps(D,ensure_ascii=False))","html.replace('__DATA__',json.dumps(D,ensure_ascii=False)).replace('__COUNT__',str(len(D)))")
s=s.replace('来源：用户提供的三条视频。当前 30 个初稿','来源：用户提供的四条视频。当前 __COUNT__ 个初稿')
s=s.replace("write_text(readme,encoding='utf8')","write_text(readme.replace('__COUNT__',str(len(D))),encoding='utf8')")
f.write_text(s,encoding='utf8')
f=R/'tools/write_catalog.py';s=f.read_text(encoding='utf8');s=s.replace('三条参考视频','四条参考视频').replace('共 30 种可复用样式','共 39 种可复用样式').replace('当前 30 项','当前 39 项')
s=s.replace("'V03':'视频 3｜如果在秋冬穿搭中加入色彩'","'V03':'视频 3｜如果在秋冬穿搭中加入色彩','V04':'视频 4｜考拉fufu 洗发水分享'")
s=s.replace("'L':'组合界面'","'L':'组合界面','S':'字幕','E':'解释元素'")
s=s.replace("observations[c['id']]","observations.get(c['id'],c.get('observation',''))")
f.write_text(s,encoding='utf8')
# Dedicated breakdown for the new reference, including items intentionally not templated.
data=[c for c in json.loads((R/'manifest.json').read_text(encoding='utf8')) if c['source_video']=='V04']
lines=['# V04｜考拉fufu 洗发水分享 · 包装拆解','','原片：37.433 秒，1080×1920，30fps。新增 R31–R39 共 9 项，均为待评审复刻稿。普通切镜、吹发计时实拍、手持产品、故意虚焦的吐槽镜头不额外计为包装。','','| 编号 | 代表位置 | 包装 | 结构与动作 | 可替换内容 |','|---|---|---|---|---|']
for c in data:lines.append(f"| {c['id']} | {c['source_time']:.2f}s | {c['name']} | {c['observation']} | 见 effect.html 中 TPL |")
lines+=['','## 与原库的关系','','- R31 / R32 / R39：白字黑边与浅金混排字幕，与 R13/R14 的粉色底条不同，单独保留。','- R33：与 R16 的矩形画中画同类，新增“产品实拍＋左下真实凭证”的位置与尺寸预设。','- R35 / R36：与 R11 同属素材背景＋口播前景，增加报告墙和花园的独立背景、位置、文字参数。','- R34 / R37 / R38：新增六圆递进标签、跟随式放大镜、柔边聚光灯。','','## 预览与差异','','每项提供可编辑 HTML、case.json、原片 reference.jpg/mp4、preview.mp4、poster.png 与 compare.jpg。预览为 360×640、15fps、静音；使用 720×1280 逻辑坐标，可输出 1080×1920。','','- 原字体不明，采用本机微软雅黑近似。','- 草本照片来自原片，旧字修补后重新叠可改标签；纹理和底图仍有修补差异。','- 报告截图为真实局部，部分裁切不足以呈现原报告全文，布局有重复占位；复用须换完整真实资料。','- 花园背景由原片静帧与相邻花丛局部拼接，非动态背景；口播是静帧蒙版，发丝边缘未达到原始分层质量。','- 放大镜与聚光灯的轨迹为手工近似，非自动人脸/物体跟踪。','- 示例中的成分、证明、数量与时长仅还原原片设计，不作为其他产品的事实依据。','- 原片音效尚未试听，未复制或虚构音效。']
(R/'sources/V04/包装拆解表.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('Extended catalog and gallery generators; wrote V04 breakdown')
