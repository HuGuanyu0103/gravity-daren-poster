#!/usr/bin/env node
/*
 * 引力专项达人档案 — 长图截图脚本
 * 用无头 Chromium 把 template.html 渲染成整页竖版长图 PNG。
 *
 * 用法：
 *   xvfb-run -a node shot.js <html文件> <输出png> [宽度=941]
 * 例：
 *   xvfb-run -a node shot.js template.html 引力专项档案·某达人.png
 *
 * 依赖：playwright-core + 已安装的 chromium（见 README）。
 */
const { chromium } = require('/tmp/node_modules/playwright-core');
const path = require('path');

const htmlArg = process.argv[2] || 'template.html';
const outArg  = process.argv[3] || 'out.png';
const width   = parseInt(process.argv[4] || '941', 10);
const CHROME  = process.env.CHROME_PATH || '/opt/playwright/chromium-1234/chrome-linux64/chrome';

(async () => {
  const browser = await chromium.launch({
    executablePath: CHROME,
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'],
  });
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  await page.setViewportSize({ width, height: 1400 });
  const url = 'file://' + path.resolve(htmlArg);
  await page.goto(url, { waitUntil: 'networkidle' });
  const el = await page.$('.page');
  await el.screenshot({ path: path.resolve(outArg) });
  await browser.close();
  console.log('[OK] 已输出长图:', outArg);
})().catch(e => { console.error('[ERR]', e.message); process.exit(1); });
