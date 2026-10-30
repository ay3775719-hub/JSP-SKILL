from pathlib import Path
import json,cv2,math
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];p=Path(str(Path.home()/'Downloads/douyin')+'/@考拉fufu 谁不想急头白脸体验一把全头炸毛的烦恼？！ 1080P.mp4');out=R/'sources/V04';out.mkdir(parents=True,exist_ok=True)
c=cv2.VideoCapture(str(p));fps=c.get(cv2.CAP_PROP_FPS);duration=c.get(cv2.CAP_PROP_FRAME_COUNT)/fps;width=int(c.get(cv2.CAP_PROP_FRAME_WIDTH));height=int(c.get(cv2.CAP_PROP_FRAME_HEIGHT));font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
times=[i*.5 for i in range(math.ceil(duration*2))]
for batch in range(math.ceil(len(times)/24)):
 sheet=Image.new('RGB',(6*216,4*414),'#161616');draw=ImageDraw.Draw(sheet)
 for i,t in enumerate(times[batch*24:batch*24+24]):
  c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read()
  if not ok:continue
  im=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB));im.save(out/f'{t:05.1f}.jpg',quality=90);im.thumbnail((216,384));x=i%6*216;y=i//6*414;sheet.paste(im,(x,y));draw.text((x+5,y+386),f'{t:.2f}s',font=font,fill='white')
 sheet.save(out/f'contact_{batch+1}.jpg',quality=92)
c.release();info={'id':'V04','path':str(p),'duration':duration,'width':width,'height':height,'fps':fps};sources=json.loads((R/'sources/sources.json').read_text(encoding='utf8'));sources=[s for s in sources if s['id']!='V04'];sources.append(info);(R/'sources/sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(info,ensure_ascii=True))
