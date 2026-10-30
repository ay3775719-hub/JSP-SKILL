from pathlib import Path
import json,cv2,math,argparse
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('id');p.add_argument('path');p.add_argument('--step',type=float,default=2);args=p.parse_args()
R=Path(__file__).resolve().parents[1];out=R/'sources'/args.id;out.mkdir(parents=True,exist_ok=True);src=Path(args.path)
c=cv2.VideoCapture(str(src));fps=c.get(cv2.CAP_PROP_FPS);dur=c.get(cv2.CAP_PROP_FRAME_COUNT)/fps;w=int(c.get(cv2.CAP_PROP_FRAME_WIDTH));h=int(c.get(cv2.CAP_PROP_FRAME_HEIGHT));font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
times=[i*args.step for i in range(math.ceil(dur/args.step))]
for batch in range(math.ceil(len(times)/24)):
 sheet=Image.new('RGB',(1296,1656),'#171717');d=ImageDraw.Draw(sheet)
 for i,t in enumerate(times[batch*24:batch*24+24]):
  c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read()
  if not ok:continue
  im=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB));im.resize((720,1280)).save(out/f'{t:06.1f}.jpg',quality=91);im.thumbnail((216,384));x=i%6*216;y=i//6*414;sheet.paste(im,(x,y));d.text((x+4,y+386),f'{int(t)//60:02}:{t%60:04.1f}',font=font,fill='white')
 sheet.save(out/f'contact_{batch+1}.jpg',quality=92)
c.release();info={'id':args.id,'path':str(src),'duration':dur,'width':w,'height':h,'fps':fps};file=R/'sources/sources.json';data=json.loads(file.read_text(encoding='utf8'));data=[s for s in data if s['id']!=args.id]+[info];file.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(info,ensure_ascii=True))
