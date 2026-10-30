// AI 剪辑包装 Skill · 作者：大象学长（全网同名）· CC BY-NC 4.0，分享须署名，不得商用售卖
// 包装复刻稿共用：字体、缓动、按时间取值、建元素、帧序列
// 复刻稿里用 <script src="../../effects/lib.js"></script> 引进来（项目里的副本写 lib.js 的绝对路径或相对路径都行）
// 画布 1920×1080；所有动画都写成 t（秒）的函数，渲染时逐帧调用 window.render(t)
const LIB_URL = document.currentScript.src;
const FONT_DIR = new URL('../fonts/', LIB_URL).href;     // 库根目录的 fonts/
const ASSET = new URL('../assets/', LIB_URL).href;       // 帧序列等素材：assets/<名字>/0001.jpg…

// 字体：fonts/ 里有这几个文件就用（思源黑体、阿里巴巴普惠体都免费可商用），没有就退回系统字体
document.head.insertAdjacentHTML('beforeend', `<style>
@font-face{font-family:HeiH;font-weight:900;src:url(${FONT_DIR}SourceHanSansCN-Heavy.otf),url(${FONT_DIR}SourceHanSansCN-Heavy.ttf),local("PingFang SC Semibold"),local("Microsoft YaHei Bold")}
@font-face{font-family:HeiM;font-weight:500;src:url(${FONT_DIR}SourceHanSansCN-Medium.otf),url(${FONT_DIR}SourceHanSansCN-Medium.ttf),local("PingFang SC Medium"),local("Microsoft YaHei")}
@font-face{font-family:PuHui;font-weight:900;src:url(${FONT_DIR}AlibabaPuHuiTi-3-105-Heavy.ttf),local("PingFang SC Semibold"),local("Microsoft YaHei Bold")}
html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:transparent}
*{box-sizing:border-box}
.abs{position:absolute}
</style>`);
const HEI = `HeiH, "PingFang SC", "Microsoft YaHei", sans-serif`;

// 品牌色：换成你自己的⁠​‌​​​‌​​​‌​‌‌​​​​‌​‌‌​​​​‌​‌‌​‌​​​‌​‌‌​‌​‌​​​​​‌​‌​‌​‌‌​​‌​‌​​​​​​‌​‌‌​‌​​‌‌​​‌​​​‌‌​​​​​​‌‌​​‌​​​‌‌​‌‌​​​‌‌​​​‌​​‌‌​​​​​​‌‌​​‌​​​‌‌‌​​‌​​‌​‌‌​‌​‌​‌​‌‌​​​‌‌​​​‌⁠
const YEL = '#FCC840', INK = '#1b1a17';

const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const E = {
  lin: (x) => x,
  out: (x) => 1 - Math.pow(1 - x, 3),
  expo: (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)),          // 有分量的字落定用这个，不回弹
  inOut: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  back: (x) => { const c = 1.70158, c3 = c + 1; return 1 + c3 * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); },
};
// 在 [t0, t0+d] 内把 a 过渡到 b
const tw = (t, t0, d, a, b, ease = E.out) => a + (b - a) * ease(clamp((t - t0) / d));
// [t0, t0+d] 内的进度 0–1
const p = (t, t0, d) => clamp((t - t0) / d);
const F = (frame) => frame / 30;   // 帧 → 秒（30fps）

function el(tag, css = {}, parent = document.body, html = '') {
  const e = document.createElement(tag);
  e.className = 'abs';
  Object.assign(e.style, css);
  if (html) e.innerHTML = html;
  parent.appendChild(e);
  return e;
}
const tf = (e, s) => (e.style.transform = s);

// 帧序列：底层视频（比如口播）抽成 jpg 放进页面里画，这样口播也能缩放 / 移动 / 放进画框
//   ffmpeg -ss <起始秒> -i 口播.mp4 -frames:v <帧数> -vf scale=3840:-1 -q:v 3 assets/<名字>/%04d.jpg
const seqSrc = (name, t) => `${ASSET}${name}/${String(Math.floor(t * 30) + 1).padStart(4, '0')}.jpg`;
async function setFrame(img, src) {
  if (img.dataset.src === src) return;
  img.dataset.src = src;
  img.src = src;
  await img.decode();
}
function seqImg(css = {}, parent = document.body) {
  return el('img', {display: 'block', objectFit: 'cover', ...css}, parent);
}

// 逐字上滑：每个字在遮罩里从下往上滑（14 帧 expo，字间隔 3 帧），返回 render(t)
function riseChars(txt, t0, o = {}) {
  const size = o.size ?? 120, x = o.x ?? 960, y = o.y ?? 400, gap = o.step ?? 3 / 30;
  const box = el('div', {left: x + 'px', top: y + 'px', height: Math.round(size * 1.25) + 'px', overflow: 'hidden', display: 'flex', transform: o.center === false ? '' : 'translateX(-50%)'});
  const chars = [...txt].map((ch) => el('span', {position: 'relative', display: 'inline-block', font: `900 ${size}px/${Math.round(size * 1.25)}px ${HEI}`, color: o.color ?? '#fff',
    textShadow: o.shadow ?? '0 8px 26px rgba(0,0,0,.45)', whiteSpace: 'pre'}, box, ch === ' ' ? ' ' : ch));
  return (t) => chars.forEach((c, i) => tf(c, `translateY(${(1 - E.expo(clamp((t - t0 - i * gap) / (14 / 30)))) * size * 1.25}px)`));
}
