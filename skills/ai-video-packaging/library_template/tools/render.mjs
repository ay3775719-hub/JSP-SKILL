// AI 剪辑包装 Skill · 作者：大象学长（全网同名）· CC BY-NC 4.0，分享须署名，不得商用售卖
// 复刻稿 effect.html → 视频
//   node render.mjs <effect.html> [输出.mov] [--opaque] [--preview] [--hd]
//   默认：透明 ProRes 4444（4K，带 alpha），放剪辑软件上层轨道
//   --opaque：不透明 ProRes 422 HQ（画面里自带口播的版式）
//   --preview：库里的预览 preview.mp4（H.264，透明处垫底色，带 META.sfx 里的音效），输出到 effect.html 同一文件夹
//   --hd：按 1080p 出（默认 4K）
// 页面要提供 window.META = {dur, sfx?: [[音效名, 秒], …]} 和 window.render(t)
// 需要：Node 18+、ffmpeg、Chrome；第一次在 tools/ 里跑 npm install
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import puppeteer from 'puppeteer-core';

const args = process.argv.slice(2);
const flags = new Set(args.filter((a) => a.startsWith('--')));
const [src, outArg] = args.filter((a) => !a.startsWith('--'));
if (!src) { console.log('用法：node render.mjs <effect.html> [输出.mov] [--opaque] [--preview] [--hd]'); process.exit(1); }
const html = path.resolve(src);
const opaque = flags.has('--opaque'), preview = flags.has('--preview'), scale = flags.has('--hd') ? 1 : 2;
const LIB = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

const CHROME = process.env.CHROME_PATH || [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
].find((p) => fs.existsSync(p));
if (!CHROME) { console.error('找不到 Chrome：装一个 Chrome，或者设置环境变量 CHROME_PATH'); process.exit(1); }
const FFMPEG = process.env.FFMPEG || 'ffmpeg';

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true,
  args: ['--allow-file-access-from-files', '--force-color-profile=srgb', '--hide-scrollbars'] });
const page = await browser.newPage();
page.on('pageerror', (e) => console.error('页面报错：', e.message));
await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: scale });
await page.goto(pathToFileURL(html).href);
await page.evaluate(() => document.fonts.ready);
const meta = await page.evaluate(() => window.META);
const n = Math.round(meta.dur * 30);
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'pkg-render-'));
const ext = opaque ? 'jpg' : 'png';
let prev = null, reused = 0;
for (let i = 0; i < n; i++) {
  // 画面没变（DOM 一模一样）就复制上一帧，停留段不用重新截图
  const sig = await page.evaluate(async (t) => { await window.render(t); return document.body.innerHTML; }, i / 30);
  const f = path.join(tmp, `${String(i).padStart(4, '0')}.${ext}`);
  if (sig === prev && i > 0) { fs.copyFileSync(path.join(tmp, `${String(i - 1).padStart(4, '0')}.${ext}`), f); reused++; continue; }
  prev = sig;
  await page.screenshot(opaque ? { path: f, type: 'jpeg', quality: 95 } : { path: f, omitBackground: true });
}
await browser.close();

const input = ['-framerate', '30', '-i', path.join(tmp, `%04d.${ext}`)];
let out;
if (preview) {
  // 预览：透明处垫底色（case.json 的 preview_bg，默认深灰），按峰值对齐配上音效
  out = outArg ? path.resolve(outArg) : path.join(path.dirname(html), 'preview.mp4');
  let bg = '#2b2b2b';
  try { bg = JSON.parse(fs.readFileSync(path.join(path.dirname(html), 'case.json'), 'utf8')).preview_bg || bg; } catch {}
  const peaks = (() => { try { return JSON.parse(fs.readFileSync(path.join(LIB, 'sfx', 'peaks.json'), 'utf8')); } catch { return {}; } })();
  const sfx = (meta.sfx || []).map(([name, t]) => {
    const file = fs.readdirSync(path.join(LIB, 'sfx')).find((f) => path.parse(f).name === name && !f.endsWith('.json'));
    if (!file) { console.warn(`音效 ${name} 不在 sfx/ 里，预览先不带这一声`); return null; }
    const peak = (peaks[name]?.peak_frame ?? 0) / 30;
    return { file: path.join(LIB, 'sfx', file), delay: Math.max(0, t - peak), gain: peaks[name]?.gain_db ?? 0 };
  }).filter(Boolean);
  const a = [], fc = [`color=c=${bg}:s=${1920 * scale}x${1080 * scale}:r=30:d=${meta.dur}[bg];[bg][0:v]overlay=format=auto,format=yuv420p[v]`];
  sfx.forEach((s, i) => { a.push('-i', s.file); fc.push(`[${i + 1}:a]adelay=${Math.round(s.delay * 1000)}:all=1,volume=${s.gain}dB[a${i}]`); });
  if (sfx.length) fc.push(`${sfx.map((_, i) => `[a${i}]`).join('')}amix=inputs=${sfx.length}:normalize=0,apad,atrim=0:${meta.dur}[a]`);
  execFileSync(FFMPEG, ['-loglevel', 'error', '-y', ...input, ...a, '-filter_complex', fc.join(';'), '-map', '[v]', ...(sfx.length ? ['-map', '[a]', '-c:a', 'aac'] : []),
    '-frames:v', String(n), '-c:v', 'libx264', '-crf', '20', '-movflags', '+faststart', out]);
} else {
  out = outArg ? path.resolve(outArg) : html.replace(/\.html$/, '.mov');
  const enc = opaque ? ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le'] : ['-c:v', 'prores_ks', '-profile:v', '4', '-pix_fmt', 'yuva444p10le'];
  fs.mkdirSync(path.dirname(out), { recursive: true });
  execFileSync(FFMPEG, ['-loglevel', 'error', '-y', ...input, '-frames:v', String(n), ...enc, out]);
}
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`完成：${out}（${n} 帧，${preview ? '预览' : opaque ? '不透明' : '透明'}，复用 ${reused} 帧）`);
process.exit(0);
