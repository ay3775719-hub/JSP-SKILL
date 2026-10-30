from pathlib import Path
import json,math,subprocess,sys
SOURCE=sys.argv[1] if len(sys.argv)>1 else "V04"
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];data=json.loads((R/'manifest.json').read_text(encoding='utf8'));new=[c for c in data if c['source_video']==SOURCE];font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20)
def sheet(cases,dest,cols=3):
 out=Image.new('RGB',(cols*300,math.ceil(len(cases)/cols)*566),'#171717');d=ImageDraw.Draw(out)
 for i,c in enumerate(cases):
  im=Image.open(R/'cases'/c['folder']/'poster.png').resize((300,533));x=i%cols*300;y=i//cols*566;out.paste(im,(x,y));d.text((x+6,y+535),c['id']+' '+c['name'][:11],font=font,fill='white')
 out.save(dest,quality=93)
sheet(new,R/'sources'/SOURCE/'新增包装总览.jpg');sheet(data,R/'预览总览.jpg',5)
# A montage with labels above each independent 3s preview, without altering case previews.
cfg=json.loads((R/'tools/runtime.json').read_text(encoding='utf8'));parts=[]
for c in new:
 folder=R/'cases'/c['folder'];label=R/'sources'/SOURCE/(c['id']+'_label.txt');label.write_text(c['id']+' '+c['name'],encoding='utf8')
 # English ID is sufficient for the video; full Chinese labels are in the contact sheet and gallery.
 part=R/'sources'/SOURCE/(c['id']+'_montage.mp4');vf="pad=360:676:0:36:color=0x171717,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+c['id']+"':fontcolor=white:fontsize=22:x=12:y=7"
 subprocess.run([cfg['ffmpeg'],'-v','error','-y','-i',str(folder/'preview.mp4'),'-vf',vf,'-an','-c:v','libx264','-crf','22',str(part)],check=True);parts.append(part)
file=R/'sources'/SOURCE/'montage.txt';file.write_text(''.join("file '"+str(p).replace('\\','/')+"'\n" for p in parts),encoding='utf8')
subprocess.run([cfg['ffmpeg'],'-v','error','-y','-f','concat','-safe','0','-i',str(file),'-c','copy','-movflags','+faststart',str(R/'sources'/SOURCE/'新增包装预览合集.mp4')],check=True)
print('Made '+SOURCE+' overview images and labeled preview montage')
