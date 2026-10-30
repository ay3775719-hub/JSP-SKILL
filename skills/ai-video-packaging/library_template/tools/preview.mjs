// AI 剪辑包装 Skill · 作者：大象学长（全网同名）· CC BY-NC 4.0，分享须署名，不得商用售卖
// 截复刻稿某几秒的静帧，快速看位置 / 字号 / 状态（不用渲整段）
//   node preview.mjs <effect.html> <秒> [<秒> …]   → 同文件夹 frame_<秒>.png（透明处带底色）
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import puppeteer from 'puppeteer-core';

const [src, ...times] = process.argv.slice(2);
if (!src || !times.length) { console.log('用法：node preview.mjs <effect.html> <秒> [<秒> …]'); process.exit(1); }
const html = path.resolve(src);
const CHROME = process.env.CHROME_PATH || ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  '/usr/bin/google-chrome', '/usr/bin/chromium'].find((p) => fs.existsSync(p));
let bg = '#2b2b2b';
try { bg = JSON.parse(fs.readFileSync(path.join(path.dirname(html), 'case.json'), 'utf8')).preview_bg || bg; } catch {}
const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--allow-file-access-from-files', '--force-color-profile=srgb'] });
const page = await browser.newPage();
page.on('pageerror', (e) => console.error('页面报错：', e.message));
await page.setViewport({ width: 1920, height: 1080 });
await page.goto(pathToFileURL(html).href);
await page.evaluate((c) => { document.documentElement.style.background = c; }, bg);
for (const s of times) {
  await page.evaluate(async (t) => { await document.fonts.ready; await window.render(t); }, Number(s));
  const out = path.join(path.dirname(html), `frame_${s}.png`);
  await page.screenshot({ path: out });
  console.log(out);
}
await browser.close();
process.exit(0);
