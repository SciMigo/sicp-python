// Local Chrome QA: node tools/check_layout.mjs MODULE [BASE_URL]
import {createRequire} from 'node:module';
import {mkdirSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const require=createRequire(import.meta.url);
const {chromium}=require(path.resolve(root,'../scimigo-learn/node_modules/playwright'));
const moduleId=process.argv[2];
if (!/^\d{2}-[a-z0-9-]+$/.test(moduleId??'')) throw Error('Provide a module id');
const base=process.argv[3]??'http://127.0.0.1:8768';
const out=path.join(root,'output/review',moduleId);mkdirSync(out,{recursive:true});
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE_PATH??'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
try {
 for (const width of [1366,390]) for (const theme of ['light','dark']) {
  const page=await browser.newPage({viewport:{width,height:850},colorScheme:theme});
  await page.goto(`${base}/output/reading/${moduleId}.html`);
  const geometry=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
  if (geometry.width!==geometry.scroll) throw Error(`Lesson overflow: ${JSON.stringify({theme,...geometry})}`);
  await page.screenshot({path:path.join(out,`lesson-${width}-${theme}.png`)});
  for(let i=0;i<await page.locator('figure').count();i++) await page.locator('figure').nth(i).screenshot({path:path.join(out,`figure-${i}-${width}-${theme}.png`)});
  const contrast=await page.evaluate(()=>{
   function luminance(rgb){const c=rgb.match(/[\d.]+/g).slice(0,3).map(x=>Number(x)/255).map(x=>x<=0.04045?x/12.92:((x+0.055)/1.055)**2.4);return .2126*c[0]+.7152*c[1]+.0722*c[2];}
   const results=[];
   for(const selector of ['body','.admonition']) {
    const node=document.querySelector(selector); if(!node) continue;
    const css=getComputedStyle(node), fg=luminance(css.color);
    let bg=css.backgroundColor;
    if(bg==='rgba(0, 0, 0, 0)') bg=getComputedStyle(document.body).backgroundColor;
    if(bg==='rgba(0, 0, 0, 0)') bg='rgb(255, 255, 255)';
    const b=luminance(bg);results.push({selector,ratio:(Math.max(fg,b)+.05)/(Math.min(fg,b)+.05)});
   }return results;
  });
  if(contrast.some(x=>x.ratio<4.5)) throw Error('Low contrast: '+JSON.stringify(contrast));
  console.log(`lesson ${width} ${theme}: no overflow, contrast ${contrast.map(x=>x.ratio.toFixed(2)).join(', ')}`);
  await page.close();
 }
 const page=await browser.newPage({viewport:{width:390,height:850}});
 await page.goto(`${base}/preview/?module=${moduleId}`);
 await page.waitForSelector('#runtime.ready',{timeout:180000});
 await page.click('#run');await page.waitForFunction(()=>!document.getElementById('run').disabled,{timeout:60000});
 await page.screenshot({path:path.join(out,'lab-mobile.png'),fullPage:true});
 const geometry=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
 if(geometry.width!==geometry.scroll) throw Error('Lab overflow: '+JSON.stringify(geometry));
 const source=await page.locator('.cm-content').innerText();
 if(!source.startsWith('def ')) throw Error('Editable function is not shown first');
 console.log('mobile starter runs and displays the editable function first; no overflow');
} finally {await browser.close();}
