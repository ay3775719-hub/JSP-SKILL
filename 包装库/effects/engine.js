/* AI 剪辑包装库：720×1280 逻辑坐标，按 render(t) 确定性绘制。
 * 原 skill：大象学长，CC BY-NC 4.0。此项目新增引擎与样片复刻稿。
 */
const stage=document.getElementById('stage');
const clamp=x=>Math.max(0,Math.min(1,x));
const ease=x=>1-Math.pow(1-clamp(x),4);
const query=new URLSearchParams(location.search);
window.META={width:720,height:1280,dur:TPL.duration||3,sfx:[]};
window.previewMode=query.get('preview')==='1';
const videoCache=new Map();let activeVideos=[];
function el(tag,styles={},cls=''){const n=document.createElement(tag);n.className='item '+cls;Object.assign(n.style,styles);stage.append(n);return n;}
function text(s,x,y,size,color='#fff',cls='',extra={}){let n=el('div',{left:x+'px',top:y+'px',fontSize:size+'px',color,...extra},'txt '+cls);n.textContent=s;return n;}
function image(src,x,y,w,h,extra={}){if(!src)return;let n;
 if(/\.(mp4|mov|webm)(\?|$)/i.test(src)){n=videoCache.get(src);if(!n){n=document.createElement('video');n.src=src;n.muted=true;n.preload='auto';videoCache.set(src,n);}n.className='item photo';Object.assign(n.style,{left:x+'px',top:y+'px',width:w+'px',height:h+'px',...extra});stage.append(n);activeVideos.push(n);}
 else {n=el('img',{left:x+'px',top:y+'px',width:w+'px',height:h+'px',objectFit:/\.png(\?|$)/i.test(src)?'contain':'cover',...extra},'photo');n.src=src;}return n;}
function backdrop(src){image(src,0,0,720,1280);}
function editorial(){text(TPL.heading||'Statement Piece',0,118,40,'#eeecc0','serif',{width:'720px',textAlign:'center',fontWeight:700});text(TPL.subtitle||'wanwan share',435,172,37,'#eeecc0','script');}
function number(){text(TPL.brand||'OGOKO',220,78,39,'#fff','serif',{fontWeight:700});text(TPL.text||'Number 01',46,125,TPL.fontSize||90,'#fff','script');}
function pink(s,size){let n=text(s,0,1070,size,TPL.color||'#fff','',{left:'50%',transform:'translateX(-50%)',padding:'8px 16px',borderRadius:'9px',background:TPL.fill||'#eeb6c7b0',textShadow:'0 1px 2px #fff3',fontWeight:600,letterSpacing:'3px'});n.style.background=hexAlpha(TPL.fill||'#eeb6c7',TPL.opacity??.69);return n;}
function hexAlpha(hex,opacity){return /^#[\da-f]{6}$/i.test(hex)?hex+Math.round(opacity*255).toString(16).padStart(2,'0'):hex;}
function setEntry(n,t,delay=0,type='cut'){if(!n)return;let p=ease((t-delay)/.28);n.style.opacity=t>=delay?'1':'0';if(type==='slide')n.style.transform=`translateY(${(1-p)*35}px)`;}
window.render=async function(raw){
 const t=raw-(TPL.start||0);stage.replaceChildren();activeVideos=[];
 stage.style.transform=`scale(${innerWidth/720})`;
 const layout=!window.CASE.transparent;
 if((window.previewMode||layout)&&TPL.background)backdrop(TPL.background);
 if(t<0)return;
 const color=TPL.color||'#fff';
 switch(TPL.kind){
 case 'editorial':text(TPL.text,0,118,TPL.fontSize,color,'serif',{width:'720px',textAlign:'center',fontWeight:700});text(TPL.subtitle,435,173,37,color,'script');break;
 case 'number':number();break;
 case 'announcement':image(TPL.image,36,821,376,84);text(TPL.text,50,925,TPL.fontSize,color,'serif',{fontWeight:700});break;
 case 'scatter':{let positions=[[36,145],[36,245],[555,790],[190,943]];TPL.texts.forEach((s,i)=>{let n=text(s,...positions[i%4],TPL.fontSize,color,'hand',{fontWeight:700});setEntry(n,t,TPL.times[i]||0);});break;}
 case 'gold':text(TPL.text,75,973,TPL.fontSize,color,'hand',{transform:'rotate(-4deg)',textShadow:'0 0 10px #d5cd7e'});break;
 case 'collage':case 'cover':{
  let boxes=[[45,150,295,390,-5],[415,210,262,275,6],[45,590,300,345,-6]];
  TPL.images.forEach((s,i)=>{let [x,y,w,h,r]=boxes[i];let n=image(s,x,y,w,h,{transform:`rotate(${r}deg)`,boxShadow:'0 8px 12px #0003'});setEntry(n,t,i*.12);});
  if(TPL.kind==='cover'){image(TPL.foreground,376,445,290,825,{filter:'drop-shadow(0 0 6px white)'});text(TPL.text,84,956,TPL.fontSize,color,'hand');}break;}
 case 'grid':editorial();TPL.images.forEach((s,i)=>{let n=image(s,96+(i%2)*284,256+Math.floor(i/2)*364,244,325);setEntry(n,t,i*.08);});break;
 case 'lineup':editorial();image(TPL.images[0],18,250,252,860);image(TPL.images[1],265,224,197,744);image(TPL.images[2],438,312,277,858);break;
 case 'browser':editorial();image(TPL.image,217,245,467,623,{boxShadow:'0 10px 16px #0005'});image(TPL.foreground,8,450,252,705);break;
 case 'product':number();image(TPL.image,425,110,257,501,{boxShadow:'0 10px 16px #0004'});image(TPL.foreground,0,350,430,920);break;
 case 'hostpip':number();image(TPL.image,36,226,431,568);image(TPL.foreground,330,590,360,525);break;
 case 'single':number();image(TPL.image,90,245,537,695,{boxShadow:'0 9px 12px #0004'});break;
 case 'pinkbar':case 'pinkbig':pink(TPL.text,TPL.fontSize);break;
 case 'comments':{let boxes=[[57,38,436,108],[32,151,656,89],[32,242,656,143],[32,668,594,86],[33,760,593,98],[43,875,540,76],[33,973,653,89],[33,1130,542,66]];
 TPL.images.forEach((s,i)=>{let j=i<3?i+5:i-3;let n=image(s,...boxes[i]);setEntry(n,t,j*.13);});pink(TPL.text,54);break;}
 case 'pip':image(TPL.image,27,630,373,486);break;
 case 'blackwindow':{el('div',{inset:'0',background:'#000'});image(TPL.background,153,275,414,735);text(TPL.text,0,1076,TPL.fontSize,color,'',{left:'50%',transform:'translateX(-50%)',background:TPL.fill,padding:'4px 15px',borderRadius:'7px'});break;}
 case 'scriptTitle':{let y=TPL.y;let f=TPL.fontSize;let w=650;let style={width:w+'px',textAlign:'center',textShadow:'none'};text(TPL.text,35,y,f,color,'script',style);text(TPL.subtitle,35,y+f*.79,35,color,'script',style);text(TPL.second,35,y+f*.99,f*1.06,color,'script',style);break;}
 case 'behindLook':text(TPL.text,38,550,TPL.fontSize,color,'script',{width:'650px',textAlign:'center',textShadow:'none'});image(TPL.foreground,TPL.foregroundX,TPL.foregroundY,TPL.foregroundW,840);break;
 case 'masthead':text(TPL.text,0,113,TPL.fontSize,color,'script',{width:'720px',textAlign:'center'});text(TPL.subtitle,0,183,29,'#fff','',{left:'50%',transform:'translateX(-50%)',padding:'1px 7px',background:'#301510c9'});break;
 case 'codes':TPL.items.forEach((i,j)=>{let n=text(i.text,i.x,i.y,TPL.fontSize,color,'serif');setEntry(n,t,j*.1);});break;
 case 'echo':{image(TPL.images[0],25,440,180,530);image(TPL.images[2],510,360,260,745);image(TPL.images[1],199,345,305,835);text(TPL.text,0,113,43,'#f6edc4','script',{width:'720px',textAlign:'center'});text(TPL.subtitle,0,183,29,'#fff','',{left:'50%',transform:'translateX(-50%)',padding:'1px 7px',background:'#301510c9'});break;}
 case 'notebook':{text(TPL.text,280,400,TPL.fontSize,color,'script',{transform:'rotate(18deg)',textShadow:'none'});image(TPL.foreground,180,540,385,690,{filter:'drop-shadow(4px 2px 0 white)'});[[270,495],[520,880],[160,760],[550,1000]].forEach(([x,y],i)=>text(i%2?'✧':'✶',x,y,48,'#e9f8a0','',{textShadow:'none',transform:`rotate(${i*13}deg)`}));break;}
 case 'features':TPL.texts.forEach((s,i)=>text(s,390,450+i*43,TPL.fontSize,color,'serif',{background:'#281c1966',padding:'3px'}));break;
 case 'closing':TPL.texts.forEach((s,i)=>text(s,0,752+i*40,TPL.fontSize,color,'serif',{left:'50%',transform:'translateX(-50%)',textAlign:'center',background:'#281c1966',padding:'2px 7px'}));break;
 case 'pageflip':{number();let p=ease(t/.5);image(TPL.image,133,195,454,825,{transform:`perspective(900px) rotateY(${(1-p)*-85}deg) rotate(${(1-p)*-6}deg)`,transformOrigin:'left center',boxShadow:'12px 10px 18px #0004'});break;}
 }
 if(TPL.x||TPL.yOffset){for(const n of [...stage.children].slice((layout||window.previewMode)?1:0)){n.style.marginLeft=(TPL.x||0)+'px';n.style.marginTop=(TPL.yOffset||0)+'px';}}
 for(const v of activeVideos){if(v.readyState<1)await new Promise((resolve,reject)=>{v.onloadedmetadata=resolve;v.onerror=()=>reject(new Error('无法读取视频 '+v.src));});let target=Math.min(Math.max(0,t),Math.max(0,v.duration-.05));if(Math.abs(v.currentTime-target)>.02)await new Promise(resolve=>{v.onseeked=resolve;v.currentTime=target;});}
};
window.addEventListener('resize',()=>stage.style.transform=`scale(${innerWidth/720})`);
window.addEventListener('message',e=>{if(e.data?.type==='render')window.render(e.data.time);if(e.data?.type==='update'){Object.assign(TPL,e.data.tpl);window.render(e.data.time||1.5);}});
window.render(0);
