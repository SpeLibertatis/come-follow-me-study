const {chromium}=require(process.env.PLAYWRIGHT_MODULE || '../../../.test-tools/node_modules/playwright');
const http=require('node:http'),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../../..');
const server=http.createServer((req,res)=>{const file=path.resolve(root,'.'+new URL(req.url,'http://localhost').pathname);if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}try{res.setHeader('Content-Type',({'.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml'})[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));}catch{res.writeHead(404).end();}});
(async()=>{await new Promise(r=>server.listen(4174,'127.0.0.1',r));const browser=await chromium.launch({executablePath:process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});const results=[];try{
const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'});let errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(r.url()+': '+r.status());});page.on('request',r=>assert.equal(new URL(r.url()).hostname,'127.0.0.1'));
for(const name of ['index','adventure','journal']){
 await page.setViewportSize({width:1440,height:1000});await page.goto('http://127.0.0.1:4174/'+name+'.html');await page.screenshot({path:path.join(__dirname,name+'-desktop.png'),fullPage:true});
 await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').innerText(),'Skip to study');await page.keyboard.press('Enter');assert.equal(await page.locator(':focus').getAttribute('id'),'main');
 for(const width of [390,320]){await page.setViewportSize({width,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));if(width===390)await page.screenshot({path:path.join(__dirname,name+'-mobile.png'),fullPage:true});}
 await page.evaluate(()=>document.documentElement.style.fontSize='200%');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.evaluate(()=>document.documentElement.style.fontSize='');
 results.push(name+': desktop/mobile screenshots; 320px reflow; 200% text; keyboard skip link; first-party assets.');
}
await page.goto('http://127.0.0.1:4174/adventure.html');await page.locator('[data-go="story0"]:visible').click();assert.equal(await page.locator(':focus').getAttribute('id'),'story0');await page.locator('#story0 summary').nth(0).click();await page.locator('#story0 summary').nth(1).waitFor({state:'visible'});await page.locator('#story0 summary').nth(1).click();await page.locator('#story0 summary').nth(2).waitFor({state:'visible'});await page.locator('[data-go="story1"]:visible').click();await page.goBack();assert(await page.locator('#story0').isVisible());await page.goForward();assert(await page.locator('#story1').isVisible());results.push('Adventure: ordered disclosure, focus transfer, back/forward preserve progress.');
await page.goto('http://127.0.0.1:4174/adventure.html#finish');assert(await page.locator('#finish').isVisible());
for(const name of ['adventure','journal']){
 await page.goto('http://127.0.0.1:4174/'+name+'.html'+(name==='adventure'?'#finish':'#reflection'));await page.locator('#private-thought').fill('Private test reflection');
 await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw Error('denied')}}}));await page.locator('[data-save="copy"]').click();assert.match(await page.locator('.save-status').innerText(),/selected/);
 await page.evaluate(()=>Object.defineProperty(navigator,'share',{configurable:true,value:undefined}));await page.locator('[data-save="share"]').click();assert.match(await page.locator('.save-status').innerText(),/unavailable/);
 await page.evaluate(()=>Object.defineProperty(navigator,'share',{configurable:true,value:async()=>{throw new DOMException('Canceled','AbortError')}}));await page.locator('[data-save="share"]').click();assert.match(await page.locator('.save-status').innerText(),/canceled/);
 const download=page.waitForEvent('download');await page.locator('[data-save="download"]').click();assert.equal((await download).suggestedFilename(),'my-scripture-reflection.txt');
 await page.reload();assert.equal(await page.locator('#private-thought').inputValue(),'');results.push(name+': copy failure fallback, unavailable/canceled share, explicit download, reload clears note (browser API mocks; not native-device evidence).');
}
assert.deepEqual(errors,[]);fs.writeFileSync(path.join(__dirname,'results.json'),JSON.stringify({passed:results,limitations:['Native-device share and screen-reader testing not performed.']},null,2));console.log(results.join('\n'));
}finally{await browser.close();server.close();}})().catch(e=>{console.error(e);server.close();process.exitCode=1;});


