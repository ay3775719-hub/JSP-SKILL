// V04 专用模板，避免改变既有 R01–R30 的渲染行为。
const stage=document.getElementById('stage'),q=new URLSearchParams(location.search);
window.META={width:720,height:1280,dur:3,sfx:[]};window.previewMode=q.get('preview')==='1';
const clamp=x=>Math.max(0,Math.min(1,x));
function node(tag,style={}){let n=document.createElement(tag);Object.assign(n.style,{position:'absolute',boxSizing:'border-box',...style});stage.append(n);return n}
function image(src,x,y,w,h,style={}){let n=node('img',{left:x+'px',top:y+'px',width:w+'px',height:h+'px',objectFit:'fill',...style});n.src=src;return n}
function label(s,x,y,size,color='#fff',style={}){let n=node('div',{left:x+'px',top:y+'px',fontFamily:'Microsoft YaHei,sans-serif',fontSize:size+'px',fontWeight:'400',lineHeight:'1.2',whiteSpace:'pre',color,webkitTextStroke:(TPL.strokeWidth||2.6)+'px '+(TPL.stroke||'#161616'),paintOrder:'stroke fill',...style});n.textContent=s;return n}
function centered(s,y,size,color='#fff',style={}){return label(s,360,y,size,color,{transform:'translateX(-50%)',...style})}
function segments(list,y,size=TPL.fontSize){let n=node('div',{left:'360px',top:y+'px',transform:'translateX(-50%)',display:'flex',alignItems:'baseline',whiteSpace:'pre',fontFamily:'Microsoft YaHei,sans-serif',lineHeight:'1.2'});for(const s of list){let e=document.createElement('span');Object.assign(e.style,{fontSize:(s.size||size)+'px',color:s.color||'#fff',webkitTextStroke:(TPL.strokeWidth||2.6)+'px #161616',paintOrder:'stroke fill'});e.textContent=s.text;n.append(e);}return n}
function tracked(t){let ks=TPL.keyframes||[[0,360,640]];let a=ks[0],b=a;for(let i=1;i<ks.length;i++){b=ks[i];if(t<=b[0]){let p=clamp((t-a[0])/(b[0]-a[0]));return [a[1]+(b[1]-a[1])*p,a[2]+(b[2]-a[2])*p]}a=b}return [b[1],b[2]]}
window.render=async t=>{stage.replaceChildren();stage.style.transform=`scale(${innerWidth/720})`;if((window.previewMode||!window.CASE.transparent)&&TPL.background)image(TPL.background,0,0,720,1280);let [cx,cy]=tracked(t);
switch(TPL.kind){
case 'outlineCaption':centered(TPL.text,TPL.y,TPL.fontSize,TPL.color);break;
case 'goldCaption':segments(TPL.segments,TPL.y,40);break;
case 'proofInset':if(t>=(TPL.start||0))image(TPL.image,TPL.x,TPL.y,TPL.w,TPL.h);break;
case 'ingredients':TPL.images.forEach((src,i)=>{if(t<(TPL.times[i]||0))return;let [x,y,d]=TPL.positions[i];image(src,x,y,d,d,{borderRadius:'50%',objectFit:'cover'});label(TPL.labels[i],x+d/2,y+d*.44,TPL.fontSize,'#fff',{transform:'translateX(-50%)'})});break;
case 'reportWall':{
node('div',{inset:'0',background:'radial-gradient(ellipse at 30% 40%,#faf7ed,#e7ddc9)'});
let boxes=[[5,63,355,390],[360,63,323,392],[5,412,320,793],[360,455,324,745]];boxes.forEach((b,i)=>image(TPL.images[i%TPL.images.length],...b,{boxShadow:'5px 8px 12px #0004'}));image(TPL.foreground,TPL.foregroundX,TPL.foregroundY,TPL.foregroundW,1280);centered(TPL.text,945,TPL.fontSize);break;}
case 'roseScene':image(TPL.foreground,0,0,720,1280);label(t<TPL.switchAt?TPL.text:TPL.second,TPL.textX,TPL.textY,TPL.fontSize,t<TPL.switchAt?TPL.color:'#fff',{transform:'rotate(6deg)'});break;
case 'magnifier':{
let r=TPL.radius,p=clamp(t/(TPL.enterDuration||.1)),n=node('div',{left:cx-r+'px',top:cy-r+'px',width:r*2+'px',height:r*2+'px',borderRadius:'50%',overflow:'hidden',opacity:String(p),transform:`scale(${.94+.06*p})`});let im=document.createElement('img');im.src=TPL.image;Object.assign(im.style,{position:'absolute',width:720*TPL.zoom+'px',height:1280*TPL.zoom+'px',left:r-cx*TPL.zoom+'px',top:r-cy*TPL.zoom+'px'});n.append(im);
const NS='http://www.w3.org/2000/svg';let svg=document.createElementNS(NS,'svg');svg.setAttribute('width',720);svg.setAttribute('height',1280);Object.assign(svg.style,{position:'absolute',inset:0,opacity:String(p)});let c=document.createElementNS(NS,'circle');Object.entries({cx,cy,r,fill:'none',stroke:TPL.color,'stroke-width':TPL.strokeWidth,'stroke-dasharray':TPL.dash+' '+TPL.gap}).forEach(([k,v])=>c.setAttribute(k,v));svg.append(c);stage.append(svg);break;}
case 'spotlight':{
let hole=TPL.radius,p=clamp(t/(TPL.enterDuration||.08));node('div',{inset:'0',background:`radial-gradient(circle ${hole+TPL.feather}px at ${cx}px ${cy}px, transparent ${Math.max(0,hole-TPL.feather)}px, rgba(0,0,0,${TPL.darkness*p}) ${hole+TPL.feather}px)`});break;}
case 'twoLine':centered(TPL.first,TPL.firstY,TPL.fontSize);if(t>=TPL.delay)segments(TPL.segments,TPL.secondY,TPL.fontSize);break;
}
};
addEventListener('resize',()=>stage.style.transform=`scale(${innerWidth/720})`);addEventListener('message',e=>{if(e.data?.type==='render')window.render(e.data.time);if(e.data?.type==='update'){Object.assign(TPL,e.data.tpl);window.render(e.data.time||1.8)}});window.render(0);
