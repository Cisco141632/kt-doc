/* Dependency-free browser checks. Run: node azure/tests/browser.mjs [chromium]
 * Uses Node 22+ WebSocket and Chromium's DevTools protocol; installs nothing.
 */
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {createServer} from 'node:http';
import {readFile, mkdtemp, writeFile, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve, dirname, extname, sep, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const repository = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const profile = await mkdtemp(join(tmpdir(), 'kt-azure-browser-'));
const mime = {'.html':'text/html', '.js':'text/javascript', '.css':'text/css', '.svg':'image/svg+xml'};
const server = createServer(async (req, res) => {
  try {
    const path = decodeURIComponent(new URL(req.url, 'http://local').pathname);
    const file = resolve(repository, '.' + path + (path.endsWith('/') ? 'index.html' : ''));
    if (!file.startsWith(repository + sep)) throw new Error('Outside repository');
    const content = await readFile(file);
    res.writeHead(200, {'Content-Type': mime[extname(file)] || 'text/plain'});
    res.end(content);
  } catch { res.writeHead(404); res.end('Not found'); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const base = `http://127.0.0.1:${server.address().port}/azure/`;
const browser = spawn(process.argv[2] || '/snap/bin/chromium', [
  '--headless', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
  '--no-first-run', '--no-default-browser-check', '--remote-debugging-port=0',
  '--user-data-dir=' + profile, 'about:blank'
], {stdio:['ignore', 'ignore', 'pipe']});
let socket, session, nextId = 1, stderr = '', dialogAccept = true, dialogs = 0;
const pending = new Map(), errors = [], missing = [];
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
try {
  const endpoint = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('Chromium startup timed out: ' + stderr.slice(-2000))), 20000);
    browser.on('error', reject);
    browser.stderr.on('data', bytes => {
      stderr += bytes.toString();
      const match = stderr.match(/DevTools listening on (ws:\/\/\S+)/);
      if (match) { clearTimeout(timer); resolve(match[1]); }
    });
    browser.on('exit', code => { clearTimeout(timer); reject(new Error(`Chromium exited ${code}: ${stderr.slice(-2000)}`)); });
  });
  socket = new WebSocket(endpoint);
  await new Promise((resolve, reject) => {
    socket.addEventListener('open', resolve, {once:true});
    socket.addEventListener('error', reject, {once:true});
  });
  function send(method, params = {}, target = session) {
    const id = nextId++;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => { pending.delete(id); reject(new Error('CDP timed out: ' + method)); }, 15000);
      pending.set(id, {resolve, reject, timer});
      socket.send(JSON.stringify({id, method, params, ...(target ? {sessionId:target} : {})}));
    });
  }
  socket.addEventListener('message', event => {
    const message = JSON.parse(event.data);
    if (message.id && pending.has(message.id)) {
      const entry = pending.get(message.id);
      pending.delete(message.id); clearTimeout(entry.timer);
      if (message.error) entry.reject(new Error(JSON.stringify(message.error)));
      else entry.resolve(message.result);
    }
    if (message.method === 'Runtime.exceptionThrown') {
      const detail = message.params.exceptionDetails;
      errors.push(detail.exception?.description || detail.text);
    }
    if (message.method === 'Network.responseReceived' && message.params.response.status >= 400) missing.push(message.params.response.url);
    if (message.method === 'Page.javascriptDialogOpening') {
      dialogs++;
      send('Page.handleJavaScriptDialog', {accept:dialogAccept}).catch(() => {});
    }
  });
  const {targetId} = await send('Target.createTarget', {url:'about:blank'}, null);
  session = (await send('Target.attachToTarget', {targetId, flatten:true}, null)).sessionId;
  await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
  async function evaluate(expression) {
    const result = await send('Runtime.evaluate', {expression, returnByValue:true, awaitPromise:true});
    if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
    return result.result.value;
  }
  async function until(expression) {
    for (let i = 0; i < 120; i++) { if (await evaluate(expression)) return; await sleep(40); }
    throw new Error('Condition did not become true: ' + expression);
  }
  async function visit(id) {
    await send('Page.navigate', {url:base + id + '.html'});
    await until(`document.readyState === 'complete' && document.body.dataset.module === ${JSON.stringify(id)}`);
  }
  async function viewport(width, height = 1000) {
    await send('Emulation.setDeviceMetricsOverride', {width, height, deviceScaleFactor:1, mobile:width < 700});
  }
  const click = selector => evaluate(`document.querySelector(${JSON.stringify(selector)}).click()`);
  const value = selector => evaluate(`document.querySelector(${JSON.stringify(selector)}).textContent`);
  const fill = (selector, content, type = 'input') => evaluate(`(() => {const el = document.querySelector(${JSON.stringify(selector)}); el.value = ${JSON.stringify(content)}; el.dispatchEvent(new Event(${JSON.stringify(type)}, {bubbles:true}));})()`);
  const change = (selector, content) => fill(selector, content, 'change');
  const checked = (selector, content) => evaluate(`(() => {const el = document.querySelector(${JSON.stringify(selector)}); el.checked = ${JSON.stringify(content)}; el.dispatchEvent(new Event('change', {bubbles:true}));})()`);
  const submit = selector => evaluate(`document.querySelector(${JSON.stringify(selector)}).requestSubmit()`);
  async function screenshot(name) {
    const shot = await send('Page.captureScreenshot', {format:'png', captureBeyondViewport:false});
    await writeFile(join(tmpdir(), name), Buffer.from(shot.data, 'base64'));
  }
  async function noOverflow(width, id) {
    const sizes = await evaluate('({scroll:document.documentElement.scrollWidth, body:document.body.scrollWidth, viewport:innerWidth, client:document.documentElement.clientWidth})');
    const offenders = sizes.scroll > width + 1 ? await evaluate(`Array.from(document.querySelectorAll('body *')).map(el => ({tag:el.tagName, cls:el.className, right:Math.round(el.getBoundingClientRect().right), width:Math.round(el.getBoundingClientRect().width), text:el.textContent.slice(0,100)})).filter(el => el.right > ${width + 1}).slice(0,14)`) : [];
    if (sizes.scroll > width + 1) {
      await screenshot('kt-azure-overflow.png');
      console.log('OVERFLOW DETAIL', await evaluate(`Array.from(document.querySelectorAll('body *')).filter(el=>el.scrollWidth>el.clientWidth+2).map(el=>({tag:el.tagName,cls:el.className,scroll:el.scrollWidth,client:el.clientWidth,overflow:getComputedStyle(el).overflowX,parents:[el.parentElement?.tagName,el.parentElement?.className]})).slice(0,25)`));
    }
    assert.ok(sizes.scroll <= width + 1, `${id}: horizontal overflow at ${width}px: ${JSON.stringify({sizes,offenders})}`);
  }
  const storage = () => evaluate('JSON.parse(localStorage.getItem("azure-storage-learning-v1"))');
  const lab = id => `[data-lab="${id}"]`;
  const control = (id, name) => `${lab(id)} [data-control="${name}"]`;
  const action = (id, name) => `${lab(id)} [data-action="${name}"]`;
  const output = id => value(`${lab(id)} [data-output]`);

  await viewport(1440);
  await visit('index');
  const ids = await evaluate('AZURE_DATA.modules.map(module => module.id)');
  const lessonIds = await evaluate('AZURE_DATA.lessonIds');
  assert.equal(ids.length, 16, '11 lessons and five supporting pages');
  assert.equal(lessonIds.length, 11);
  for (const id of ids) {
    await visit(id);
    assert.equal(await evaluate('document.querySelectorAll("h1").length'), 1, 'One h1: ' + id);
    assert.ok(await evaluate('document.querySelector("main").textContent.length') > 350, 'Readable lesson: ' + id);
    assert.equal(await evaluate('document.querySelectorAll("#course-nav a").length'), ids.length);
    await noOverflow(1440, id);
  }
  await visit('index'); await screenshot('kt-azure-desktop.png');
  assert.equal(await evaluate('getComputedStyle(document.querySelector("#menu-toggle")).display'), 'none', 'Mobile menu hidden on desktop');
  console.log(`PASS: ${ids.length} desktop pages, readable content, complete navigation and no overflow.`);

  await visit('foundations'); await click('#mark-done');
  assert.equal(await evaluate('document.querySelector("#mark-done").getAttribute("aria-pressed")'), 'true');
  await visit('access');
  assert.match(await value('#course-progress'), /1 of 11/);
  await click('.theme-toggle');
  const theme = await evaluate('document.documentElement.dataset.theme');
  await visit('keys');
  assert.equal(await evaluate('document.documentElement.dataset.theme'), theme);
  await click('.theme-toggle');
  await fill('#nav-search', 'migration');
  assert.equal(await evaluate('document.querySelectorAll("[data-nav-item]:not([hidden])").length'), 1);
  await fill('#nav-search', 'zz-no-such-module');
  assert.equal(await evaluate('document.querySelector("#nav-empty").hidden'), false);
  await fill('#nav-search', '');
  console.log('PASS: lesson completion, cross-page persistence, theme persistence and navigation search.');

  await visit('quiz');
  const questions = await evaluate('AZURE_DATA.questions');
  const first = questions[0];
  await submit('#quiz-card form');
  assert.match(await value('#quiz-card .feedback'), /Choose an answer/);
  await click(`#quiz-card input[value="${(first.correct + 1) % first.options.length}"]`);
  await submit('#quiz-card form');
  assert.match(await value('#quiz-card .feedback'), /Not quite/);
  assert.match(await value('#quiz-score'), /0 correct \/ 1 answered/);
  await change('#quiz-mode', 'missed');
  assert.match(await value('#quiz-position'), /of 1/);
  await click('#quiz-card [data-retry]');
  await click(`#quiz-card input[value="${first.correct}"]`);
  await submit('#quiz-card form');
  assert.match(await value('#quiz-card .feedback'), /Correct/);
  await visit('quiz');
  assert.equal(await evaluate('document.querySelectorAll("#quiz-card input:disabled").length'), first.options.length);
  await change('#quiz-topic', 'ownership');
  assert.match(await value('#quiz-position'), new RegExp('of ' + questions.filter(q => q.topic === 'ownership').length));
  await change('#quiz-topic', 'all');
  for (let i = 0; i < questions.length; i++) {
    const question = questions[i];
    if (i) {
      await click(`#quiz-card input[value="${question.correct}"]`);
      await submit('#quiz-card form');
    }
    assert.match(await value('#quiz-card .feedback'), /Correct/, question.id);
    if (i < questions.length - 1) await click('#quiz-next');
  }
  assert.match(await value('#quiz-score'), new RegExp(`${questions.length} correct / ${questions.length} answered`));
  assert.equal(await evaluate('document.querySelector("#quiz-next").disabled'), true);
  await change('#quiz-mode', 'missed');
  assert.match(await value('#quiz-card'), /No questions/);
  await change('#quiz-mode', 'unanswered');
  assert.match(await value('#quiz-card'), /No questions/);
  await visit('foundations');
  assert.equal(await evaluate('document.querySelectorAll("[data-lesson-check] .question").length'), 2);
  assert.equal(await evaluate('document.querySelectorAll("[data-lesson-check] input:not(:disabled)").length'), 0);
  console.log(`PASS: all ${questions.length} quiz answers, explanations, empty submission, retry, filters, persistence and shared lesson checks.`);

  await visit('glossary');
  await fill('#glossary-search', 'signed');
  assert.ok(await evaluate('document.querySelectorAll("[data-glossary]:not([hidden])").length') > 0);
  await fill('#glossary-search', 'zz-no-matching-word');
  assert.equal(await evaluate('document.querySelector("#glossary-empty").hidden'), false);
  await fill('#glossary-search', '');

  await visit('practice');
  assert.equal(await evaluate('document.querySelectorAll("[data-lab-kind]").length'), 7);
  assert.equal(await evaluate('(() => {const ids = [...document.querySelectorAll("[id]")].map(el => el.id); return ids.length === new Set(ids).size;})()'), true, 'Unique IDs across all labs');
  await fill(control('explorer', 'prefix'), 'cases/214');
  assert.match(await output('explorer'), /2 matching blobs/);
  await fill(control('explorer', 'prefix'), 'cases/214/');
  assert.match(await output('explorer'), /1 matching blob/);
  await fill(control('explorer', 'content'), 'Edited only in demo');
  await click(action('explorer', 'write')); await click(action('explorer', 'write'));
  assert.match(await output('explorer'), /Overwritten/);
  await change(control('explorer', 'account'), 'delhistore');
  assert.match(await output('explorer'), /Delhi original/);
  assert.doesNotMatch(await output('explorer'), /Exact key contents: Edited only in demo/);

  await click(action('sas', 'test'));
  assert.match(await output('sas'), /allow|success|200/i);
  await fill(control('sas', 'elapsed'), '300'); await click(action('sas', 'test'));
  assert.match(await output('sas'), /expired|403/i);
  await fill(control('sas', 'elapsed'), '0');
  await change(control('sas', 'operation'), 'write'); await click(action('sas', 'test'));
  assert.match(await output('sas'), /permission|403/i);

  await change(control('routing', 'preset'), 'bare');
  assert.match(await output('routing'), /silent deployment fallback/);
  await change(control('routing', 'preset'), 'deployment');
  assert.match(await output('routing'), /Deployment root matched first/);
  await change(control('routing', 'preset'), 'customer');
  assert.match(await output('routing'), /delhistore/);
  await change(control('routing', 'config'), 'conflict');
  assert.match(await output('routing'), /Conflicting root mappings/);
  await change(control('routing', 'config'), 'configured');
  await fill(control('routing', 'key'), 'https://[');
  assert.match(await output('routing'), /could not be parsed/i);
  await click(action('routing', 'reset'));
  await checked(control('paths', 'exists'), false);
  assert.match(await output('paths'), /MISSING/);
  await change(control('paths', 'mode'), 'built');
  assert.match(await output('paths'), /REBUILT/);
  for (let i = 0; i < 8; i++) await click(action('journey', 'next'));
  assert.match(await output('journey'), /Step 9 of 9/);
  assert.equal(await evaluate(`document.querySelector(${JSON.stringify(action('journey', 'next'))}).disabled`), true);
  await checked(control('migration', 'blobs'), true);
  assert.match(await output('migration'), /found|available|exists/i);
  await checked(control('migration', 'bare'), true);
  assert.match(await output('migration'), /deployment|demostore/i);

  await click(action('debugging', 'diagnose'));
  assert.match(await output('debugging'), /at least two/);
  const incidents = await evaluate('AzureStorageModel.DEBUG_CASES.map(c => ({id:c.id,cause:c.cause}))');
  for (const incident of incidents) {
    await change(control('debugging', 'scenario'), incident.id);
    await click(action('debugging', 'evidence-path'));
    await click(action('debugging', 'evidence-route'));
    await change(control('debugging', 'diagnosis'), incident.cause);
    await click(action('debugging', 'diagnose'));
    assert.match(await output('debugging'), /Correct\./);
  }
  assert.match(await value('#lab-progress'), /7 of 7/);
  assert.equal((await storage()).labs.length, 7);
  await evaluate('document.querySelector("[data-lab=routing]").scrollIntoView({behavior:"instant",block:"start"})');
  await screenshot('kt-azure-routing.png');
  await visit('practice');
  assert.match(await value('#lab-progress'), /7 of 7/);
  await screenshot('kt-azure-practice.png');
  console.log('PASS: all seven lab milestones, isolation, prefix boundaries, grant expiry, routing conflicts, path rebuilding, migration and incident evidence.');

  await visit('reference');
  async function importProgress(content, filename = 'progress.json') {
    await evaluate(`(() => {const input = document.querySelector('#import-progress'), transfer = new DataTransfer(); transfer.items.add(new File([${JSON.stringify(content)}], ${JSON.stringify(filename)}, {type:'application/json'})); input.files = transfer.files; input.dispatchEvent(new Event('change', {bubbles:true}));})()`);
  }
  await importProgress('{}');
  await until('document.querySelector("#progress-status").textContent.startsWith("Import failed")');
  assert.equal(Object.keys((await storage()).answers).length, questions.length, 'Invalid import preserves progress');
  const imported = {course:'azure-storage', version:1, done:['foundations','unknown','foundations'], labs:['sas','unknown'], answers:{[first.id]:first.correct, [questions[1].id]:999, unknown:0}};
  await importProgress(JSON.stringify(imported));
  await until('document.querySelector("#progress-status").textContent.startsWith("Imported progress")');
  assert.deepEqual((await storage()).done, ['foundations']);
  assert.deepEqual((await storage()).labs, ['sas']);
  assert.deepEqual((await storage()).answers, {[first.id]:first.correct});
  await evaluate(`(() => {const original = URL.createObjectURL, click = HTMLAnchorElement.prototype.click; window.__restoreExport = () => {URL.createObjectURL = original; HTMLAnchorElement.prototype.click = click;}; URL.createObjectURL = blob => {window.__exportedProgress = blob.text(); return original(blob);}; HTMLAnchorElement.prototype.click = function () {if (!this.download) return click.call(this);};})()`);
  await click('#export-progress');
  const exported = await evaluate('(async () => JSON.parse(await window.__exportedProgress))()');
  assert.equal(exported.course, 'azure-storage');
  assert.deepEqual(exported.done, ['foundations']);
  await evaluate('window.__restoreExport()');
  dialogAccept = false; await click('#reset-progress');
  assert.deepEqual((await storage()).done, ['foundations'], 'Cancelled reset keeps data');
  dialogAccept = true; await click('#reset-progress');
  assert.deepEqual(await storage(), {version:1,done:[],labs:[],answers:{}});
  assert.equal(dialogs, 2, 'Both reset choices use confirmation');
  console.log('PASS: glossary filtering, validated imports, export contents, invalid-import preservation and confirmed/cancelled reset.');

  await viewport(375, 900);
  for (const id of ids) {
    await visit(id); await noOverflow(375, id);
  }
  await visit('index'); await screenshot('kt-azure-mobile.png');
  await click('#menu-toggle');
  assert.equal(await evaluate('document.querySelector("#menu-toggle").getAttribute("aria-expanded")'), 'true');
  assert.notEqual(await evaluate('getComputedStyle(document.querySelector("#course-nav")).display'), 'none');
  await send('Input.dispatchKeyEvent', {type:'keyDown', key:'Escape', code:'Escape', windowsVirtualKeyCode:27});
  assert.equal(await evaluate('document.querySelector("#menu-toggle").getAttribute("aria-expanded")'), 'false');
  await visit('practice');
  await evaluate('document.querySelector("[data-lab=routing]").scrollIntoView({behavior:"instant",block:"start"})');
  await screenshot('kt-azure-routing-mobile.png');
  console.log(`PASS: ${ids.length} mobile pages at 375px, mobile navigation and Escape-key close.`);

  for (const id of ids) {
    await send('Emulation.setScriptExecutionDisabled', {value:true});
    await send('Page.navigate', {url:base + id + '.html'}); await sleep(180);
    await send('Emulation.setScriptExecutionDisabled', {value:false});
    await until(`document.readyState === 'complete' && document.body.dataset.module === ${JSON.stringify(id)}`);
    assert.equal(await evaluate('document.documentElement.classList.contains("js")'), false, 'No-JS class: ' + id);
    assert.ok(await evaluate('document.querySelector("main").textContent.length') > 350, 'No-JS content: ' + id);
    assert.equal(await evaluate('document.querySelectorAll("#course-nav a").length'), ids.length);
    assert.notEqual(await evaluate('getComputedStyle(document.querySelector("#course-nav")).display'), 'none');
    await noOverflow(375, 'No-JS ' + id);
  }
  await visit('index');
  await evaluate('localStorage.setItem("azure-storage-learning-v1", "not-json")');
  await visit('foundations');
  assert.equal(await evaluate('document.querySelector("#storage-status").hidden'), false);
  await click('#mark-done');
  assert.deepEqual((await storage()).done, ['foundations']);
  const injection = await send('Page.addScriptToEvaluateOnNewDocument', {source:'Object.defineProperty(window,"localStorage",{get(){throw new Error("Storage denied for browser test")}});'});
  await visit('foundations'); await click('#mark-done');
  assert.equal(await evaluate('document.querySelector("#mark-done").getAttribute("aria-pressed")'), 'true');
  assert.equal(await evaluate('document.querySelector("#storage-status").hidden'), false);
  await click('.theme-toggle');
  await send('Page.removeScriptToEvaluateOnNewDocument', {identifier:injection.identifier});
  console.log(`PASS: all ${ids.length} pages readable without JavaScript; malformed and denied storage degrade safely.`);

  assert.deepEqual(errors, [], 'Uncaught browser exceptions');
  assert.deepEqual(missing, [], 'Missing local resources');
  console.log('PASS: no browser exceptions or missing local resources. Screenshots: /tmp/kt-azure-{desktop,mobile,routing,routing-mobile,practice}.png');
} finally {
  if (socket) socket.close();
  for (const entry of pending.values()) clearTimeout(entry.timer);
  browser.kill('SIGTERM');
  await new Promise(resolve => server.close(resolve));
  await rm(profile, {recursive:true, force:true}).catch(() => {});
}
