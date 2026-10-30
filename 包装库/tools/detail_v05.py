from pathlib import Path
import json,cv2
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];p=next(s['path'] for s in json.loads((R/'sources/sources.json').read_text(encoding='utf8')) if s['id']=='V05');c=cv2.VideoCapture(p);font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',16)
for t in [1.8,4.2,15.7,17.5,21.7,24.8,34.5,37.5,49.5,57,64.5,70,106,144]:
 c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read()
 if ok:Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)).resize((720,1280)).save(R/f'sources/V05/full_{t:05.1f}.jpg',quality=94)
for k,(a,b,step) in enumerate([(0.1,2.7,.2),(3.5,6.5,.25),(16.7,19.4,.2),(20.6,22.8,.2),(31,35.5,.3),(47.7,50.5,.2),(143,144.9,.15)]):
 times=[a+i*step for i in range(round((b-a)/step)+1)];out=Image.new('RGB',(len(times)*135,265),'#111');d=ImageDraw.Draw(out)
 for i,t in enumerate(times):
  c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read()
  if ok:out.paste(Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)).resize((135,240)),(135*i,0));d.text((135*i+3,242),f'{t:.2f}',font=font,fill='white')
 out.save(R/f'sources/V05/detail_{k}.jpg')
c.release()
