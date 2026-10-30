from pathlib import Path
import json,cv2,numpy as np
from PIL import Image,ImageDraw,ImageFilter
R=Path(__file__).resolve().parents[1];A=R/'assets/V04';A.mkdir(parents=True,exist_ok=True)
source=next(s for s in json.loads((R/'sources/sources.json').read_text(encoding='utf8')) if s['id']=='V04')
def frame(t):
 c=cv2.VideoCapture(source['path']);c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read();c.release();assert ok;return Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)).resize((720,1280))
def save(im,name):im.save(A/name);return '../../assets/V04/'+name
def clean(im,boxes):
 ar=np.array(im.convert('RGB'));mask=np.zeros(ar.shape[:2],np.uint8)
 for x,y,w,h in boxes:mask[y:y+h,x:x+w]=255
 return Image.fromarray(cv2.inpaint(ar,mask,4,cv2.INPAINT_TELEA))
def masked(im,pts,name):
 ar=np.array(im.convert('RGB'));poly=np.zeros(ar.shape[:2],np.uint8);cv2.fillPoly(poly,[np.array(pts,np.int32)],255)
 near=cv2.dilate(poly,np.ones((9,9),np.uint8));inside=cv2.erode(poly,np.ones((9,9),np.uint8));mask=np.where(near==0,cv2.GC_BGD,cv2.GC_PR_BGD).astype(np.uint8);mask[poly>0]=cv2.GC_PR_FGD;mask[inside>0]=cv2.GC_FGD
 try:cv2.grabCut(ar,mask,None,np.zeros((1,65),np.float64),np.zeros((1,65),np.float64),3,cv2.GC_INIT_WITH_MASK);alpha=np.where((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD),255,0).astype(np.uint8)
 except:alpha=poly
 out=im.convert('RGBA');out.putalpha(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(.5)));return save(out,name)
portrait=save(clean(frame(16.7),[(160,940,420,65)]),'portrait.jpg')
product=save(clean(frame(5.35),[(250,930,300,65)]),'product.jpg')
proof=save(frame(6).crop((63,666,265,952)),'proof_real.jpg')
im=frame(18.8);ingredientImages=[]
for i,(box,rect) in enumerate([((54,54,177,177),(4,48,115,51)),((220,54,352,186),(3,48,125,55)),((398,54,530,186),(0,42,132,57)),((74,240,198,364),(0,45,124,57)),((231,250,365,384),(5,39,125,57)),((396,230,544,378),(14,55,130,57))]):ingredientImages.append(save(clean(im.crop(box),[rect]),f'ingredient_{i}.jpg'))
ingredientBg=save(clean(frame(18.8),[(40,35,520,365),(60,930,610,75)]),'ingredient_bg.jpg')
documents=[]
im=frame(20.5)
for i,box in enumerate([(5,63,360,438),(360,63,683,455),(5,805,201,1205),(513,456,684,1200)]):documents.append(save(im.crop(box),f'report_real_{i}.jpg'))
reportHost=masked(im,[(326,445),(376,445),(413,458),(430,496),(445,550),(455,606),(454,645),(469,665),(489,706),(506,743),(516,797),(512,842),(500,875),(473,890),(448,869),(437,840),(435,907),(417,933),(288,936),(261,907),(254,859),(228,836),(219,796),(205,752),(204,685),(215,642),(234,635),(245,617),(254,559),(266,501),(290,469)],'report_host.png')
im=frame(24.8);roseBg=save(im.crop((300,0,720,490)).resize((720,1280)),'rose_bg.jpg')
roseHost=masked(im,[(169,698),(225,697),(258,718),(273,759),(282,809),(287,856),(307,891),(319,957),(324,1050),(323,1120),(297,1174),(300,1279),(50,1279),(55,1180),(31,1116),(0,1076),(0,861),(25,841),(36,858),(47,920),(55,979),(81,967),(96,869),(108,806),(114,749),(137,716)],'rose_host.png')
magnifyBg=save(clean(frame(28.0),[(130,938,490,65)]),'magnify_bg.jpg')
spotBg=save(clean(frame(30.0),[(110,935,530,65)]),'spot_bg.jpg')
closingBg=save(clean(frame(35.8),[(200,930,360,65)]),'closing_bg.jpg')
plainBg=save(clean(frame(9.2),[(180,940,370,65)]),'plain_bg.jpg')
data=json.loads((R/'manifest.json').read_text(encoding='utf8'));new=[]
def add(name,section,kind,t,when,tpl,notes,observation,related=None,ref=None):
 id=f'R{31+len(new):02}';folder=id+'_'+name;case=dict(id=id,name=name,section=section,kind=kind,status='待评审',when=when,how='修改 effect.html 顶部 TPL；所有时间和轨迹由 render(t) 驱动；替换图片槽时填本地相对路径。',sfx='静音预览；原片声音尚未试听，不臆配音效。',source=f'V04 {int(t)//60:02}:{int(t)%60:02}（{t:.2f}s）',source_video='V04',source_time=t,source_ref_time=ref or t,transparent=section not in ['L'],width=720,height=1280,duration=3,folder=folder,notes=notes,tpl=tpl,observation=observation,related=related or [])
 p=R/'cases'/folder;p.mkdir(exist_ok=True);frame(ref or t).save(p/'reference.jpg',quality=94)
 (p/'case.json').write_text(json.dumps(case,ensure_ascii=False,indent=2),encoding='utf8')
 (p/'effect.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>'+id+' '+name+'</title><link rel="stylesheet" href="../../effects/style.css"><div id="stage"></div><script>\n// 参数区：替换文字、图片、位置、时间或 keyframes。\nconst TPL = '+json.dumps(dict(kind=kind,**tpl),ensure_ascii=False,indent=2)+';\nwindow.CASE='+json.dumps({'id':id,'name':name,'transparent':case['transparent']},ensure_ascii=False)+';</script><script src="../../effects/v04.js"></script></html>',encoding='utf8');new.append(case)
add('白字黑描边口播字幕','S','outlineCaption',9.2,'日常口播与真实演示的常规字幕',dict(text='那以前我也是啊',background=plainBg,fontSize=42,color='#ffffff',stroke='#161616',strokeWidth=2.6,y=943),'字体以本机微软雅黑近似；无原字体文件。字幕无色底，与 R13 粉色字幕区分。','居中单行白字、细黑描边，位于画面下部；整句硬切。',['R13'])
add('浅金色混排重点词','C','goldCaption',5.6,'在一句话内强调一个关键短词',dict(segments=[{'text':'“药监局” ','color':'#eeecc0','size':40},{'text':'防脱','color':'#eeecc0','size':52},{'text':'认证买的','color':'#ffffff','size':40}],background=product,y=520,strokeWidth=2.5),'文字来自原片，只复刻混排结构；示例字样不替新产品作事实确认。','同一句内以浅金色和更大字号突出短词，其余部分白字黑边。',['R31'])
add('真实凭证左下插图','L','proofInset',5.6,'手持产品时插入用户提供的真实凭证',dict(background=product,image=proof,x=63,y=666,w=202,h=286,start=.02),'凭证为原片真实局部截图，未仿造文件、印章或文字；实际复用须换对应真实资料。','产品镜头保持全屏，真实凭证直角缩图在左下硬切出现。',['R16'])
add('草本成分六圆递进','E','ingredients',17.65,'在产品实拍上分批介绍多个成分或组成项',dict(background=ingredientBg,images=ingredientImages,labels=['侧柏叶','姜根','山茶籽','何首乌','人参','当归'],positions=[[54,54,123],[220,54,132],[398,54,132],[74,240,124],[231,250,134],[396,230,148]],times=[0,.18,.27,.54,.67,.8],fontSize=40),'图片与文字已分层。演示圆图来自原片并修补旧字，植物纹理和无字底图存在修补差异；须以实际产品资料替换成分名称。','上部六张圆形成分图按上排、下排陆续累积出现，中心叠白色黑边标签。',ref=19.0)
add('报告墙与中下口播人物','L','reportWall',19.75,'讲解多份真实报告或证明材料时保留口播人物',dict(images=documents,foreground=reportHost,foregroundX=0,foregroundY=0,foregroundW=720,text='还有那么多',fontSize=48),'报告素材均为原片截图局部，部分位置重复用于示意布局，不能当作完整报告；原人物静帧蒙版边缘仍需精修。实际复用应换完整真实报告与透明口播。','浅纸纹底铺多张报告，带轻阴影；中下叠透明人物，上下层分离。',['R11','R15'],ref=20.5)
add('花园背景与左下口播','L','roseScene',24.4,'讲香味、氛围等感受时切换场景背景',dict(background=roseBg,foreground=roseHost,text='雾玫瑰的高级香',second='真的好好闻！',textX=250,textY=554,fontSize=46,color='#eeecc0',switchAt=1.55),'花园底图为原片花丛局部静帧放大，构图和运动不等同原动态背景；口播为静帧蒙版，换透明视频可动。','玫瑰花园全屏，口播人物置左下；上方浅金字幕斜置，随后切换为白色短句。',['R11'],ref=24.8)
add('虚线圆形跟随放大镜','E','magnifier',28.1,'产品局部、标签或细节需要放大时',dict(background=magnifyBg,image=magnifyBg,radius=145,zoom=1.32,keyframes=[[0,345,785],[1,360,780],[2,374,764],[3,360,777]],dash=18,gap=11,strokeWidth=5,color='#ffffff',enterDuration=.12),'圆内从同一无字静帧重新取样放大，圆心轨迹为对照原片手动近似；实际视频须设置相应跟随坐标。','标签处出现白色虚线圆，圆内实像放大，圆心随目标小范围移动。',ref=28.7)
add('跟随人脸的柔边聚光灯','E','spotlight',30.08,'突出说话人表情或一句重点判断',dict(background=spotBg,radius=255,feather=28,darkness=.58,keyframes=[[0,365,500],[1,360,520],[2,385,510],[3,370,520]],enterDuration=.08),'预览使用未压暗的相邻帧，不是原片已经压暗的底图；轨迹为手动近似。支持透明遮罩，可直接叠口播。','整屏压暗，人脸附近保留柔边亮圆，圆心随脸移动；无额外装饰线。',ref=30.5)
add('双行白金结果字幕','S','twoLine',36.15,'数量或利益点的结尾总结',dict(background=closingBg,first='买两瓶',segments=[{'text':'直接能用','color':'#ffffff'},{'text':'大半年','color':'#eeecc0'},{'text':'！','color':'#ffffff'}],firstY=932,secondY=1007,fontSize=44,strokeWidth=2.5,delay=.18),'数量、使用时长仅为原片示例文字；模板复用时填写已确认的文案。','第一行白字短句先出现，第二行稍后进入，核心结果用浅金色强调。',['R31','R32'],ref=36.8)
ids={c['id'] for c in new};assert not any(c['id'] in ids for c in data),'New IDs already exist; refusing overwrite'
data.extend(new);(R/'manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
(R/'sources/V04/新增模板.json').write_text(json.dumps(new,ensure_ascii=False,indent=2),encoding='utf8')
print(f'Added {len(new)} draft cases R31–R39; total {len(data)}')
