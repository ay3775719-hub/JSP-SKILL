// Local renderer: uses existing Playwright and ffmpeg, no network requests.
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url'),{spawn,execFileSync}=require('child_process');
const ROOT=path.resolve(__dirname,'..');const config=JSON.parse(fs.readFileSync(path.join(ROOT,'tools','runtime.json'),'utf8'));
const {chromium}=require(config.playwright);
const manifest=JSON.parse(fs.readFileSync(path.join(ROOT,'manifest.json'),'utf8'));
const only=process.argv.find(x=>/^R\d\d$/.test(x));const alpha=process.argv.includes('--alpha');
async function encode(page,c,file,preview=true){
 let fps=alpha?30:15, w=alpha?1080:360,h=alpha?1920:640;
 await page.setViewportSize({width:w,height:h});
 await page.goto(pathToFileURL(path.join(ROOT,'cases',c.folder,'effect.html')).href+(preview?'?preview=1':''));
 const preload=[c.tpl?.background,c.tpl?.image,c.tpl?.foreground,c.tpl?.paper,...(c.tpl?.images||[])].filter(s=>typeof s==='string'&&/\.(jpg|jpeg|png|webp)$/i.test(s));
 await page.evaluate(async urls=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));await Promise.all(urls.map(src=>new Promise(resolve=>{const i=new Image();i.onload=()=>i.decode().then(resolve,resolve);i.onerror=resolve;i.src=src;})));},preload);
 let args=['-hide_banner','-loglevel','error','-y','-f','image2pipe','-framerate',String(fps),'-vcodec','png','-i','pipe:0','-an'];
 args.push(...(alpha?['-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le']:['-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart']),file);
 let ff=spawn(config.ffmpeg,args,{windowsHide:true});let errors='';ff.stderr.on('data',x=>errors+=x);ff.stdin.on('error',()=>{});let done=new Promise((resolve,reject)=>ff.on('close',code=>code===0?resolve():reject(new Error(errors))));
 for(let i=0;i<Math.round(c.duration*fps);i++){
  await page.evaluate(t=>window.render(t),i/fps);let b=await page.screenshot({type:'png',omitBackground:alpha});
  if(!ff.stdin.write(b))await new Promise(resolve=>ff.stdin.once('drain',resolve));
 }
 ff.stdin.end();await done;
 await page.evaluate(()=>window.render(1.8));await page.screenshot({path:path.join(ROOT,'cases',c.folder,alpha?'overlay.png':'poster.png'),omitBackground:alpha});
}
(async()=>{
 const browser=await chromium.launch({executablePath:config.chrome,headless:true,args:['--allow-file-access-from-files','--force-color-profile=srgb']});const page=await browser.newPage();let errors=[];page.on('pageerror',e=>errors.push(e.message));
 try {for(const c of manifest.filter(c=>!only||c.id===only)){
  const folder=path.join(ROOT,'cases',c.folder);
  await encode(page,c,path.join(folder,alpha?'export.mov':'preview.mp4'),!alpha);
  if(!alpha){let source=JSON.parse(fs.readFileSync(path.join(ROOT,'sources','sources.json'),'utf8')).find(s=>s.id===c.source_video);
   execFileSync(config.ffmpeg,['-hide_banner','-loglevel','error','-y','-ss',String(c.source_time),'-i',source.path,'-t','3','-an','-vf','scale=360:640','-r','15','-c:v','libx264','-crf','23','-movflags','+faststart',path.join(folder,'reference.mp4')],{windowsHide:true});
   execFileSync(config.ffmpeg,['-hide_banner','-loglevel','error','-y','-i',path.join(folder,'reference.jpg'),'-i',path.join(folder,'poster.png'),'-filter_complex','[0:v]scale=360:640[a];[a][1:v]hstack=inputs=2','-frames:v','1',path.join(folder,'compare.jpg')],{windowsHide:true});
  }
  console.log(c.id+' '+c.name+' OK');
 }if(errors.length)throw new Error(errors.join('\n'));}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
