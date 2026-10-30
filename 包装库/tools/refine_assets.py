from pathlib import Path
import cv2,numpy as np,json
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'assets';S=json.loads((R/'sources/sources.json').read_text(encoding='utf8'))
def frame(v,t):
 c=cv2.VideoCapture(S[v-1]['path']);c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read();c.release();return Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))
def clean(im,boxes):
 a=np.array(im.convert('RGB'));m=np.zeros(a.shape[:2],np.uint8)
 for x,y,w,h in boxes:m[y:y+h,x:x+w]=255
 return Image.fromarray(cv2.inpaint(a,m,4,cv2.INPAINT_TELEA))
clean(frame(1,26),[(165,965,400,57)]).save(A/'host1.jpg')
frame(1,28).crop((36,821,412,905)).save(A/'shopstrip.jpg')
# Crop photographs at their actual source boundaries.
for j,b in enumerate([(96,256,340,582),(380,256,624,582),(96,620,340,945),(380,620,624,945)]):frame(1,18).crop(b).save(A/f'grid{j}.jpg')
for name,box in [('girl.png',(8,700,245,90)),('girl2.png',(0,725,197,20)),('girl3.png',(0,655,277,55)),('hostcut.png',(0,370,360,60))]:
 im=Image.open(A/name);alpha=im.getchannel('A');fixed=clean(im,[box]).convert('RGBA');fixed.putalpha(alpha);fixed.save(A/name)
# Title overlays use clean adjacent shots rather than removing lettering over a face or clothing.
frame(3,.0).save(A/'intro.jpg')
frame(3,14).save(A/'work.jpg');frame(3,34).save(A/'city.jpg');frame(3,58).save(A/'date.jpg')
frame(3,20).save(A/'codesbg.jpg');frame(3,44).save(A/'featurebg.jpg');frame(3,76).save(A/'closingbg.jpg')
# The title-only source still has a natural caption; remove it so the editable overlay stands alone.
print('Refined source crops and demonstration plates')
