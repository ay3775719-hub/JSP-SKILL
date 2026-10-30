from pathlib import Path
import cv2,json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];p=next(s['path'] for s in json.loads((R/'sources/sources.json').read_text(encoding='utf8')) if s['id']=='V04');c=cv2.VideoCapture(p);font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15)
for j,(a,b,step) in enumerate([(5.4,6.8,.1),(17.5,19.8,.15),(19.6,21.6,.15),(24,26.8,.2),(28,29.4,.1),(30,31,.08),(35.6,37.2,.15)]):
 times=[a+i*step for i in range(round((b-a)/step)+1)];sheet=Image.new('RGB',(len(times)*135,265),'#111');d=ImageDraw.Draw(sheet)
 for i,t in enumerate(times):
  c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read()
  if ok:sheet.paste(Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)).resize((135,240)),(i*135,0));d.text((i*135+2,242),f'{t:.2f}',font=font,fill='white')
 sheet.save(R/f'sources/V04/detail_{j}.jpg')
for t in [6,18.8,20.5,24.8,28.7,30.5,36.8]:
 c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read()
 if ok:Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)).resize((720,1280)).save(R/f'sources/V04/full_{t:.1f}.jpg',quality=93)
c.release()
