from pathlib import Path
import cv2,json,numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];A=R/'assets/V04';p=next(s['path'] for s in json.loads((R/'sources/sources.json').read_text(encoding='utf8')) if s['id']=='V04')
def frame(t):
 c=cv2.VideoCapture(p);c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read();c.release();assert ok;return Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)).resize((720,1280))
def erase_glyphs(im,boxes):
 ar=np.array(im.convert('RGB')).astype(np.float32)
 for x,y,w,h in boxes:
  # Column interpolation preserves vertical hair, bottle and arm edges in these static demo plates.
  top=ar[max(0,y-2):y,x:x+w].mean(axis=0);bottom=ar[y+h:y+h+2,x:x+w].mean(axis=0)
  for j in range(h):
   p=j/max(1,h-1);ar[y+j,x:x+w]=top*(1-p)+bottom*p
 return Image.fromarray(np.clip(ar,0,255).astype(np.uint8))
for t,name,boxes in [(9.2,'plain_bg.jpg',[(180,940,370,65)]),(16.7,'portrait.jpg',[(160,940,420,65)]),(5.35,'product.jpg',[(225,782,280,56)]),(28.0,'magnify_bg.jpg',[(130,938,490,65)]),(30.0,'spot_bg.jpg',[(110,935,530,65)]),(35.8,'closing_bg.jpg',[(200,930,360,65)])]:erase_glyphs(frame(t),boxes).save(A/name)
im=frame(17.65);erase_glyphs(im,[(50,940,620,68)]).save(A/'ingredient_bg.jpg')
im=frame(24.8);patch=im.crop((360,650,720,1280)).transpose(Image.Transpose.FLIP_LEFT_RIGHT);mask=Image.new('L',patch.size,255);draw=ImageDraw.Draw(mask)
for x in range(50):draw.line((310+x,0,310+x,629),fill=round((49-x)/49*255))
maskar=np.array(mask).astype(np.float32)
for y in range(100):maskar[y]*=y/99
mask=Image.fromarray(maskar.astype(np.uint8))
im.paste(patch,(0,650),mask);erase_glyphs(im,[(245,546,385,79)]).save(A/'rose_bg.jpg')
data=json.loads((R/'manifest.json').read_text(encoding='utf8'))
case=next(c for c in data if c['id']=='R36');case['source_ref_time']=26.2;frame(26.2).save(R/'cases'/case['folder']/'reference.jpg',quality=94);(R/'cases'/case['folder']/'case.json').write_text(json.dumps(case,ensure_ascii=False,indent=2),encoding='utf8');(R/'manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print('Refined text cleanup masks; retained surrounding image structure')
