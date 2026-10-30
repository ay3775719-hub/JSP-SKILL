from pathlib import Path
import cv2,json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'sources'; OUT.mkdir(parents=True,exist_ok=True)
prefixes=['平价好看衣服店铺之毕业之后穿什么_','被问爆了的bra分享_','np如果在秋冬穿搭中加入色彩_']
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20)
sources=[]
for k,prefix in enumerate(prefixes,1):
 p=next((Path.home()/'Downloads').glob(prefix+'*.mp4'))
 cap=cv2.VideoCapture(str(p)); fps=cap.get(cv2.CAP_PROP_FPS); duration=cap.get(cv2.CAP_PROP_FRAME_COUNT)/fps
 folder=OUT/f'V{k:02}'; folder.mkdir(exist_ok=True)
 times=list(range(0,int(duration),2))
 for batch in range((len(times)+19)//20):
  sheet=Image.new('RGB',(5*216,4*414),'#171717'); draw=ImageDraw.Draw(sheet)
  for j,t in enumerate(times[batch*20:(batch+1)*20]):
   cap.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,frame=cap.read()
   if not ok: continue
   im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)); im.save(folder/f'{t:03}.jpg',quality=88)
   im.thumbnail((216,384)); x=(j%5)*216;y=(j//5)*414
   sheet.paste(im,(x,y));draw.text((x+5,y+385),f'V{k:02}  {t//60:02}:{t%60:02}',font=font,fill='white')
  sheet.save(folder/f'contact_{batch+1}.jpg',quality=90)
 cap.release();sources.append(dict(id=f'V{k:02}',path=str(p),duration=duration,width=720,height=1280,fps=fps))
(OUT/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(sources,ensure_ascii=True))
