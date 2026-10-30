import json,cv2
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1]; sources=json.loads((root/'sources/sources.json').read_text(encoding='utf8'))
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
windows={1:[(0,5,.4),(11,15,.4),(27,29,.2),(70,74,.4)],2:[(13.5,18,.3),(41,43,.2),(79,81,.2)],3:[(0,5,.4),(5,7,.2),(9,11,.2),(23,25,.2),(39,41,.2)]}
for v,ww in windows.items():
 cap=cv2.VideoCapture(sources[v-1]['path'])
 for wi,(a,b,step) in enumerate(ww):
  times=[a+i*step for i in range(int((b-a)/step)+1)]
  sheet=Image.new('RGB',(len(times)*180,345),'#111'); draw=ImageDraw.Draw(sheet)
  for i,t in enumerate(times):
   cap.set(0 if False else cv2.CAP_PROP_POS_MSEC,t*1000);ok,fr=cap.read()
   if ok: sheet.paste(Image.fromarray(cv2.cvtColor(fr,cv2.COLOR_BGR2RGB)).resize((180,320)),(i*180,0));draw.text((i*180,322),f'{t:.2f}',fill='white',font=font)
  sheet.save(root/f'sources/V{v:02}/detail_{wi}.jpg')
 cap.release()
