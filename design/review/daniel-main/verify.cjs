// Local review tooling only. Install Playwright outside the shipped prototype:
// npm install --prefix .test-tools --no-package-lock playwright@1.51.1
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || '../../../.test-tools/node_modules/playwright');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname,'../../..');
const results = [];
const ok = message => results.push(message);
const server = http.createServer((req,res) => {
  const pathname = new URL(req.url,'http://localhost').pathname;
  const file = path.resolve(root,'.' + (pathname === '/' ? '/index.html' : pathname));
  if (!file.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
  try { const data = fs.readFileSync(file); res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml'})[path.extname(file)] || 'application/octet-stream'); res.end(data); }
  catch { res.writeHead(404).end(); }
});
(async () => {
  await new Promise(resolve => server.listen(4173,'127.0.0.1',resolve));
  const browser = await chromium.launch({executablePath:process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
  try {
    const context = await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
    const page = await context.newPage();
    const requests = []; const errors = [];
    page.on('request',req => requests.push(req.url()));
    page.on('pageerror',error => errors.push(error.message));
    await page.goto('http://127.0.0.1:4173/');
    await page.screenshot({path:path.join(__dirname,'desktop.png'),fullPage:true});
    await page.locator('.hero').screenshot({path:path.join(__dirname,'desktop-hero.png')});
    assert.equal(await page.locator('h1').innerText(),'Faith in\nthe fire.');
    await page.keyboard.press('Tab'); assert.equal(await page.locator(':focus').innerText(),'Skip to study');
    await page.keyboard.press('Enter'); assert.equal(await page.locator(':focus').getAttribute('id'),'main');
    await page.locator('[href="#discovery"]').first().click();
    assert.equal(new URL(page.url()).hash,'#discovery');
    await page.locator('[value="deep"]').check(); assert.equal(await page.locator('.deep-content').isVisible(),true);
    assert.equal(new URL(page.url()).hash,'#discovery');
    await page.locator('[value="essential"]').check(); assert.equal(await page.locator('.deep-content').isVisible(),false);
    for(let i=0;i<3;i++) {
      await page.locator(`[data-scene="${i}"]`).click();
      assert.equal(await page.locator('#reveals summary').count(),1);
      for(let j=0;j<3;j++) { await page.locator('#reveals summary').nth(j).focus(); await page.keyboard.press('Enter'); await page.waitForTimeout(70); }
      assert.equal(await page.locator('#reveals details[open]').count(),3);
    }
    ok('All three accounts reveal command → response → outcome with keyboard Enter.');
    await page.locator('[href="#reflection"]').first().click();
    await page.goBack(); assert.equal(new URL(page.url()).hash,'#discovery');
    await page.goForward(); assert.equal(new URL(page.url()).hash,'#reflection');
    ok('Native anchor back/forward and mode changes preserve section orientation.');
    const sample = '<img src=x onerror=alert(1)> Private test';
    await page.locator('#thought').fill(sample);
    await page.evaluate(() => Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text => { window.copiedText = text; }}}));
    await page.locator('#copy').click(); assert.equal(await page.evaluate(() => window.copiedText),sample);
    await page.evaluate(() => Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async () => { throw Error('denied'); }}}));
    await page.locator('#copy').click(); assert.match(await page.locator('#save-status').innerText(),/selected/);
    assert.equal(await page.locator('#thought').evaluate(el => el.selectionEnd-el.selectionStart),sample.length);
    await page.evaluate(() => Object.defineProperty(navigator,'share',{configurable:true,value:undefined}));
    await page.locator('#share').click(); assert.match(await page.locator('#save-status').innerText(),/unavailable/);
    await page.evaluate(() => Object.defineProperty(navigator,'share',{configurable:true,value:async data => {window.sharedText=data.text;}}));
    await page.locator('#share').click(); assert.equal(await page.evaluate(() => window.sharedText),sample);
    await page.evaluate(() => Object.defineProperty(navigator,'share',{configurable:true,value:async () => {throw new DOMException('cancel','AbortError');}}));
    await page.locator('#share').click(); assert.match(await page.locator('#save-status').innerText(),/canceled/);
    const downloadEvent = page.waitForEvent('download'); await page.locator('#download').click();
    const download = await downloadEvent; assert.equal(download.suggestedFilename(),'daniel-reflection.txt');
    assert.equal(fs.readFileSync(await download.path(),'utf8'),sample);
    await page.locator('#clear').click(); assert.equal(await page.locator('#thought').inputValue(),'');
    ok('Copy success and denied fallback; share success/cancel/unavailable branches; downloaded text bytes; clear verified. Native share UI uses mocks and still needs real-device review.');
    await page.locator('#thought').fill(sample); await page.reload(); assert.equal(await page.locator('#thought').inputValue(),'');
    assert.equal(await page.evaluate(() => localStorage.length + sessionStorage.length),0);
    assert.equal((await context.cookies()).length,0);
    assert.equal((await page.evaluate(() => indexedDB.databases())).length,0);
    assert.equal(await page.locator('#reflection img').count(),0);
    assert.ok(requests.every(url => url.startsWith('http://127.0.0.1:4173/')));
    ok('No external requests during complete study/export flow; storage/cookies empty; reflection clears on reload; markup input stays text.');
    const blocked = await page.evaluate(async () => {
      const violations=[]; document.addEventListener('securitypolicyviolation',event => violations.push(event.violatedDirective));
      await fetch('/should-not-connect').catch(() => {});
      const script=document.createElement('script'); script.textContent='window.inlineRan=true'; document.body.append(script);
      await new Promise(resolve => setTimeout(resolve,100));
      return {violations,inlineRan:window.inlineRan};
    });
    assert.ok(blocked.violations.includes('connect-src')); assert.ok(blocked.violations.includes('script-src-elem')); assert.equal(blocked.inlineRan,undefined);
    ok('Browser enforced CSP: same-origin fetch blocked by connect-src none; inline script blocked.');
    assert.equal(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior),'auto');
    ok('Reduced-motion preference disables smooth scrolling; no animation loops.');
    for (const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:844});
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    }
    await page.setViewportSize({width:390,height:844}); await page.goto('http://127.0.0.1:4173/');
    await page.screenshot({path:path.join(__dirname,'mobile.png'),fullPage:true});
    await page.locator('.hero').screenshot({path:path.join(__dirname,'mobile-hero.png')});
    const perf = await page.evaluate(() => ({resources:performance.getEntriesByType('resource').map(r=>({name:r.name.split('/').pop(),bytes:r.decodedBodySize})),domContentLoaded:Math.round(performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd)}));
    ok('No horizontal overflow at 320, 390, 768, 1440 CSS pixels. Desktop and mobile screenshots captured.');
    ok('Local mobile timing (not a device benchmark): '+JSON.stringify(perf));
    for (const legacy of ['adventure','journal']) {
      await page.goto('http://127.0.0.1:4173/'+legacy+'.html');
      await page.waitForURL('**/index.html');
      assert.equal(await page.locator('#hero-title').innerText(),'Faith in\nthe fire.');
    }
    ok('Legacy Adventure and Journal URLs redirect to the single Daniel experience.');
    await page.setViewportSize({width:320,height:844});
    await page.evaluate(()=>document.documentElement.style.fontSize='200%');
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth));
    ok('320px viewport also reflows at 200% text size.');
    assert.deepEqual(errors,[]); ok('No uncaught browser errors.');
    fs.writeFileSync(path.join(__dirname,'results.json'),JSON.stringify({date:new Date().toISOString(),browser:browser.version(),results},null,2)+'\n');
    console.log(results.join('\n'));
  } finally { await browser.close(); server.close(); }
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
