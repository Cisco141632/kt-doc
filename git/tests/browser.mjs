/* Dependency-free Chromium smoke tests using the DevTools protocol.
 * Run: node git/tests/browser.mjs [path-to-chromium]
 * Node 22+ is needed for its built-in WebSocket client.
 */
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {createServer} from 'node:http';
import {readFile, mkdtemp, writeFile, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve, dirname, extname, sep, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const repository=resolve(dirname(fileURLToPath(import.meta.url)),'../..');
const profile=await mkdtemp(join(tmpdir(),'kt-git-browser-'));
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml'};
const server=createServer(async(req,res)=>{
  try {
    const path=decodeURIComponent(new URL(req.url,'http://local').pathname);
    const file=resolve(repository,'.'+path+(path.endsWith('/')?'index.html':''));
    if(!file.startsWith(repository+sep))throw new Error('outside root');
    const data=await readFile(file);
    res.writeHead(200,{'Content-Type':mime[extname(file)]||'text/plain'});res.end(data);
  }catch{res.writeHead(404);res.end('Not found');}
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port+'/git/';
const browser=spawn(process.argv[2]||'chromium',['--headless','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'],{stdio:['ignore','ignore','pipe']});
let ws, session, nextID=1, stderr='', errors=[], missing=[], pending=new Map();
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
try {
  const endpoint=await new Promise((resolve,reject)=>{
    const timer=setTimeout(()=>reject(new Error('Chromium startup timeout: '+stderr.slice(-2000))),20000);
    browser.on('error',reject);
    browser.stderr.on('data',data=>{
      stderr+=data.toString();
      const match=stderr.match(/DevTools listening on (ws:\/\/\S+)/);
      if(match){clearTimeout(timer);resolve(match[1]);}
    });
    browser.on('exit',code=>{clearTimeout(timer);reject(new Error('Chromium exited '+code+': '+stderr.slice(-2000)));});
  });
  ws=new WebSocket(endpoint);
  await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
  function send(method,params={},target=session) {
    const id=nextID++;
    return new Promise((resolve,reject)=>{
      const timer=setTimeout(()=>{pending.delete(id);reject(new Error('CDP timeout: '+method));},15000);
      pending.set(id,{resolve,reject,timer});
      ws.send(JSON.stringify({id,method,params,...(target?{sessionId:target}:{})}));
    });
  }
  ws.addEventListener('message',event=>{
    const m=JSON.parse(event.data);
    if(m.id&&pending.has(m.id)){
      const p=pending.get(m.id);pending.delete(m.id);clearTimeout(p.timer);
      if(m.error)p.reject(new Error(JSON.stringify(m.error)));else p.resolve(m.result);
    }
    if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails.text+' '+(m.params.exceptionDetails.exception?.description||''));
    if(m.method==='Network.responseReceived'&&m.params.response.status>=400)missing.push(m.params.response.url);
    if(m.method==='Page.javascriptDialogOpening')send('Page.handleJavaScriptDialog',{accept:true}).catch(()=>{});
  });
  const {targetId}=await send('Target.createTarget',{url:'about:blank'},null);
  session=(await send('Target.attachToTarget',{targetId,flatten:true},null)).sessionId;
  await send('Page.enable');await send('Runtime.enable');await send('Network.enable');
  const evaluate=async expression=>{
    const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});
    if(r.exceptionDetails)throw new Error(r.exceptionDetails.exception?.description||r.exceptionDetails.text);
    return r.result.value;
  };
  async function until(expression) {
    for(let i=0;i<100;i++){if(await evaluate(expression))return;await sleep(50);}
    throw new Error('Condition did not become true: '+expression);
  }
  async function visit(id) {
    await send('Page.navigate',{url:base+id+'.html'});
    await until('document.readyState === "complete" && document.body.dataset.module === '+JSON.stringify(id));
  }
  const click=selector=>evaluate('document.querySelector('+JSON.stringify(selector)+').click()');
  const change=(selector,value)=>evaluate('(()=>{const el=document.querySelector('+JSON.stringify(selector)+');el.value='+JSON.stringify(value)+';el.dispatchEvent(new Event("change",{bubbles:true}));})()');
  const fill=(selector,value)=>evaluate('(()=>{const el=document.querySelector('+JSON.stringify(selector)+');el.value='+JSON.stringify(value)+';el.dispatchEvent(new Event("input",{bubbles:true}));})()');
  async function screenshot(name){
    const result=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});
    await writeFile(join(tmpdir(),name),Buffer.from(result.data,'base64'));
  }
  await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
  await visit('index');
  const ids=await evaluate('GIT_DATA.modules.map(m=>m.id)');
  for(const id of ids){
    await visit(id);
    assert.equal(await evaluate('document.querySelectorAll("h1").length'),1);
    assert.equal(await evaluate('document.documentElement.scrollWidth <= innerWidth+1'),true,'desktop overflow: '+id);
  }
  await visit('index');await screenshot('kt-git-desktop.png');
  console.log('PASS: all 23 desktop pages, scripts and local resources.');
  await click('#mark-done');
  await visit('foundations');
  assert.match(await evaluate('document.querySelector("#course-progress").textContent'),/1 of 23/);
  await click('.theme-toggle');
  const theme=await evaluate('document.documentElement.dataset.theme');
  await visit('quiz');
  assert.equal(await evaluate('document.documentElement.dataset.theme'),theme);
  await evaluate('document.querySelector("#quiz-card form").requestSubmit()');
  assert.match(await evaluate('document.querySelector("#quiz-card .feedback").textContent'),/Choose an answer/);
  const first=await evaluate('GIT_DATA.questions[0]');
  const wrong=(first.correct+1)%3;
  await click('#quiz-card input[value="'+wrong+'"]');
  await evaluate('document.querySelector("#quiz-card form").requestSubmit()');
  assert.match(await evaluate('document.querySelector("#quiz-card .feedback").textContent'),/Not quite/);
  assert.match(await evaluate('document.querySelector("#quiz-score").textContent'),/0 correct \/ 1 answered/);
  await click('#quiz-retry');
  await click('#quiz-card input[value="'+first.correct+'"]');
  await evaluate('document.querySelector("#quiz-card form").requestSubmit()');
  assert.match(await evaluate('document.querySelector("#quiz-score").textContent'),/1 correct \/ 1 answered/);
  await visit('quiz');
  assert.equal(await evaluate('document.querySelectorAll("#quiz-card input:disabled").length'),3);
  await change('#quiz-topic','conflicts');
  assert.match(await evaluate('document.querySelector("#quiz-position").textContent'),/of 4/);
  await change('#quiz-view','missed');
  assert.match(await evaluate('document.querySelector("#quiz-card").textContent'),/Nothing here/);
  // Exercise every answer explanation and reach the end of the complete quiz.
  await change('#quiz-view','all');await change('#quiz-topic','all');
  const all=await evaluate('GIT_DATA.questions');
  for(let i=0;i<all.length;i++){
    if(i!==0){await click('#quiz-card input[value="'+all[i].correct+'"]');await evaluate('document.querySelector("#quiz-card form").requestSubmit()');}
    assert.match(await evaluate('document.querySelector("#quiz-card .feedback").textContent'),/Correct/);
    if(i<all.length-1)await click('#quiz-next');
  }
  assert.match(await evaluate('document.querySelector("#quiz-score").textContent'),/60 correct \/ 60 answered/);
  assert.equal(await evaluate('document.querySelector("#quiz-next").disabled'),true);
  console.log('PASS: quiz validation, explanations, retry, topic filtering, persistence and all 60 correct answers.');
  await visit('troubleshooting');
  await fill('#issue-search','lease');
  assert.ok(await evaluate('document.querySelectorAll(".issue:not([hidden])").length')>0);
  await fill('#issue-search','zz-no-match-xyz');
  assert.equal(await evaluate('document.querySelector("#issue-empty").hidden'),false);
  await fill('#issue-search','');await change('#issue-category','history');
  assert.ok(await evaluate('Array.from(document.querySelectorAll(".issue:not([hidden])")).every(x=>x.dataset.category==="history")'));
  await visit('reference');await fill('#command-search','rebase');
  assert.ok(await evaluate('document.querySelectorAll("#command-table tbody tr:not([hidden])").length')>0);
  await fill('#command-search','zz-no-match-xyz');
  assert.equal(await evaluate('document.querySelector("#command-empty").hidden'),false);
  await visit('practice');await click('[data-lab="staging-0"]');
  await visit('practice');
  assert.equal(await evaluate('document.querySelector("[data-lab=staging-0]").checked'),true);
  await visit('recap');
  assert.equal(await evaluate('document.querySelector("#card-known").disabled'),true);
  await click('#flashcard');await click('#card-known');
  assert.equal(await evaluate('Object.keys(JSON.parse(localStorage.getItem("git-learning-v1")).cards).length'),1);
  assert.match(await evaluate('document.querySelector("#card-position").textContent'),/of 47/);
  await click('#flashcard');await click('#card-again');
  assert.equal(await evaluate('Object.values(JSON.parse(localStorage.getItem("git-learning-v1")).cards).filter(c=>c.due===0).length'),1);
  // Invalid import must not overwrite the existing attempt.
  await evaluate('(()=>{const input=document.querySelector("#import-progress"), transfer=new DataTransfer();transfer.items.add(new File(["{}"],"bad.json",{type:"application/json"}));input.files=transfer.files;input.dispatchEvent(new Event("change"));})()');
  await until('document.querySelector("#progress-message").textContent.startsWith("Import failed")');
  assert.equal(await evaluate('Object.keys(JSON.parse(localStorage.getItem("git-learning-v1")).answers).length'),60);
  // Valid import is schema-filtered and keeps only recognized identifiers.
  await evaluate('(()=>{const data={format:"git-learning-progress",progress:{version:1,done:["foundations","unknown"],answers:{q1:0},labs:[],cards:{},missions:[0]}},input=document.querySelector("#import-progress"),transfer=new DataTransfer();transfer.items.add(new File([JSON.stringify(data)],"good.json",{type:"application/json"}));input.files=transfer.files;input.dispatchEvent(new Event("change"));})()');
  await until('document.querySelector("#progress-message").textContent.startsWith("Progress imported")');
  assert.deepEqual(await evaluate('JSON.parse(localStorage.getItem("git-learning-v1")).done'),['foundations']);
  console.log('PASS: troubleshooting/reference filters, lab persistence, recall scheduling and validated backup imports.');
  await visit('playground');
  // Explore every graph state; every operation must have readable explanations.
  const scenes=await evaluate('GitVisuals.scenes.map(s=>({id:s.id,count:s.steps.length}))');
  for(const scene of scenes) {
    await change('#graph-scene',scene.id);
    for(let i=0;i<scene.count;i++) {
      assert.ok((await evaluate('document.querySelector("#graph-explanation").textContent')).length>50);
      assert.equal(await evaluate('document.querySelectorAll("#graph-picture svg").length'),1);
      if(i<scene.count-1)await click('#graph-next');
    }
    assert.equal(await evaluate('document.querySelector("#graph-next").disabled'),true);
  }
  await change('#graph-scene','merge');await click('#graph-next');
  await evaluate('document.querySelector("#graph-explorer").scrollIntoView({behavior:"instant",block:"center"})');
  await screenshot('kt-git-playground.png');
  // Both operations identify the sides, reject mechanical choices, and accept the intended result.
  for(const operation of ['merge','rebase']) {
    await change('#conflict-operation',operation);
    await click('#conflict-check');
    assert.match(await evaluate('document.querySelector("#conflict-feedback").textContent'),/not valid JSON/);
    await click('#conflict-ours');
    assert.match(await evaluate('document.querySelector("#conflict-feedback").textContent'),/behavior is wrong/);
    await click('#conflict-theirs');
    assert.match(await evaluate('document.querySelector("#conflict-feedback").textContent'),/behavior is wrong/);
    await fill('#conflict-input','{"timeout":20,"retries":3}');
    await click('#conflict-check');
    assert.match(await evaluate('document.querySelector("#conflict-complete").textContent'),/completed/);
  }
  await change('#push-mode','lease');await click('#push-evaluate');
  assert.match(await evaluate('document.querySelector("#push-feedback").textContent'),/Rejected/);
  await click('#push-fetch');await change('#push-prediction','accept');await click('#push-evaluate');
  assert.match(await evaluate('document.querySelector("#push-feedback").textContent'),/Prediction correct.*Accepted/);
  await change('#push-mode','explicit');await change('#push-prediction','reject');await click('#push-evaluate');
  assert.match(await evaluate('document.querySelector("#push-feedback").textContent'),/Prediction correct.*Rejected/);
  await click('#perm-evaluate');
  assert.match(await evaluate('document.querySelector("#perm-feedback").textContent'),/Blocked/);
  await change('#perm-role','admin');await change('#perm-scope','write');await change('#perm-action','direct');
  await click('#perm-evaluate');
  assert.match(await evaluate('document.querySelector("#perm-feedback").textContent'),/Blocked/);
  await change('#perm-role','write');await change('#perm-action','merge');await change('#perm-approvals','2');await click('#perm-checks');await click('#perm-evaluate');
  assert.match(await evaluate('document.querySelector("#perm-feedback").textContent'),/Allowed/);
  assert.equal(await evaluate('JSON.parse(localStorage.getItem("git-learning-v1")).missions.length'),3);
  // A keyboard activation works without a pointer.
  await evaluate('document.querySelector("#graph-reset").focus()');
  await send('Page.bringToFront');
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',text:'\r',windowsVirtualKeyCode:13});
  await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
  await until('document.querySelector("#graph-position").textContent.includes("Step 1")');
  console.log('PASS: all 8 graph stories, conflict operations, push race, permission gates, 3 saved exercises and keyboard activation.');
  await visit('why-git');
  await click('#beginner-mistake');
  assert.equal(await evaluate('document.querySelectorAll("[data-version]").length'),1);
  assert.match(await evaluate('document.querySelector("#beginner-state").textContent'),/not recorded/);
  await click('#beginner-save');
  assert.equal(await evaluate('document.querySelectorAll("[data-version]").length'),2);
  await click('[data-version="A"]');await click('#beginner-restore');
  assert.match(await evaluate('document.querySelector("#beginner-work").textContent'),/Eight/);
  await click('#beginner-save');await click('[data-version="B"]');
  assert.match(await evaluate('document.querySelector("#beginner-saved").textContent'),/Two/);
  assert.match(await evaluate('document.querySelector("#beginner-goal").textContent'),/recovered/);
  await click('#beginner-reset');
  assert.equal(await evaluate('document.querySelectorAll("[data-version]").length'),1);
  assert.equal(await evaluate('GitLearning.missionDone(17)'),true);
  await evaluate('document.querySelector("#time-machine").scrollIntoView({behavior:"instant",block:"start"})');
  await screenshot('kt-git-beginner.png');
  await visit('studio');
  const step=action=>click('[data-snapshot="'+action+'"]');
  for(const action of ['editA','stage','editB'])await step(action);
  assert.equal(await evaluate('document.querySelector("#snapshot-status").textContent'),'MM notes.txt');
  await step('commit');
  assert.equal(await evaluate('document.querySelector("#snapshot-status").textContent'),' M notes.txt');
  assert.equal(await evaluate('GitLearning.missionDone(3)'),true);
  await step('editA');await click('#snapshot-undo');
  assert.equal(await evaluate('document.querySelector("#snapshot-status").textContent'),' M notes.txt');
  await change('#snapshot-mission','1');await step('unstage');
  assert.equal(await evaluate('GitLearning.missionDone(4)'),true);
  await change('#snapshot-mission','2');await step('restore');
  assert.equal(await evaluate('GitLearning.missionDone(5)'),true);
  await evaluate('document.querySelector("#snapshots").scrollIntoView({behavior:"instant",block:"start"})');
  await screenshot('kt-git-studio.png');
  const predictions=await evaluate('GitStudio.pointerChallenges.map(c=>({target:c.target,wrong:c.nodes.find(n=>n.id!==c.target).id}))');
  for(let i=0;i<predictions.length;i++) {
    await change('#pointer-challenge',String(i));
    await click('[data-commit="'+predictions[i].wrong+'"]');await click('#pointer-check');
    assert.match(await evaluate('document.querySelector("#pointer-feedback").textContent'),/Try again/);
    await click('[data-commit="'+predictions[i].target+'"]');await click('#pointer-check');
    assert.match(await evaluate('document.querySelector("#pointer-feedback").textContent'),/Correct/);
  }
  // Optional drag interaction and keyboard fallback both set the same prediction.
  await change('#pointer-challenge','0');
  await evaluate('(()=>{const data=new DataTransfer();data.setData("text/plain","git-studio-ref");document.querySelector("[data-commit=C]").dispatchEvent(new DragEvent("drop",{dataTransfer:data,bubbles:true,cancelable:true}));})()');
  assert.equal(await evaluate('document.querySelector("[data-commit=C]").getAttribute("aria-pressed")'),'true');
  await evaluate('document.querySelector("[data-commit=B]").focus()');
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',text:'\r',windowsVirtualKeyCode:13});
  await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
  assert.equal(await evaluate('document.querySelector("[data-commit=B]").getAttribute("aria-pressed")'),'true');
  const cases=await evaluate('GitStudio.incidents.map(c=>c.steps.map(q=>q.correct))');
  for(let i=0;i<cases.length;i++) {
    await change('#incident-select',String(i));
    await click('#incident-evidence summary');
    assert.equal(await evaluate('document.querySelector("#incident-evidence details").open'),true);
    for(const correct of cases[i]) {
      await click('[data-decision="'+((correct+1)%3)+'"]');
      assert.equal(await evaluate('document.querySelector("#incident-next").disabled'),true);
      await click('[data-decision="'+correct+'"]');
      assert.match(await evaluate('document.querySelector("#incident-feedback").textContent'),/Correct/);
      await click('#incident-next');
    }
    assert.equal(await evaluate('document.querySelectorAll(".case-solved").length'),1);
  }
  await click('[data-command]');
  assert.match(await evaluate('document.querySelector("#match-feedback").textContent'),/intention first/);
  await click('[data-task="staged"]');await click('[data-command="fetch"]');
  assert.match(await evaluate('document.querySelector("#match-feedback").textContent'),/another intention/);
  const pairIDs=await evaluate('GitStudio.pairs.map(p=>p.id)');
  for(const id of pairIDs){await click('[data-task="'+id+'"]');await click('[data-command="'+id+'"]');}
  assert.match(await evaluate('document.querySelector("#match-count").textContent'),/8 of 8/);
  assert.equal(await evaluate('document.querySelectorAll("#match-studio button:disabled").length'),16);
  const originalQuiz=await evaluate('JSON.stringify(JSON.parse(localStorage.getItem("git-learning-v1")).answers)');
  await click('#recall-start');
  await evaluate('document.querySelector("#recall-form").requestSubmit()');
  assert.match(await evaluate('document.querySelector("#recall-feedback").textContent'),/Choose an answer/);
  for(let i=0;i<5;i++) {
    const q=await evaluate('GIT_DATA.questions.find(q=>q.prompt===document.querySelector("#recall-form legend").textContent)');
    const answer=i===0?(q.correct+1)%3:q.correct;
    await click('#recall-form input[value="'+answer+'"]');
    await evaluate('document.querySelector("#recall-form").requestSubmit()');
    await click('#recall-next');
  }
  assert.match(await evaluate('document.querySelector("#recall-status").textContent'),/4 of 5/);
  assert.equal(await evaluate('Object.values(GitLearning.recallResults()).filter(x=>!x).length'),1);
  await click('#recall-retry');
  const retry=await evaluate('GIT_DATA.questions.find(q=>q.prompt===document.querySelector("#recall-form legend").textContent)');
  await click('#recall-form input[value="'+retry.correct+'"]');
  await evaluate('document.querySelector("#recall-form").requestSubmit()');
  await click('#recall-next');
  assert.match(await evaluate('document.querySelector("#recall-status").textContent'),/1 of 1/);
  assert.equal(await evaluate('JSON.stringify(JSON.parse(localStorage.getItem("git-learning-v1")).answers)'),originalQuiz);
  assert.equal(await evaluate('JSON.parse(localStorage.getItem("git-learning-v1")).missions.length'),18);
  await evaluate('GitLearning.recordRecall("q3",false)');
  await visit('studio');await click('#recall-start');
  assert.equal(await evaluate('document.querySelector("#recall-form legend").textContent'),await evaluate('GIT_DATA.questions.find(q=>q.id==="q3").prompt'));
  assert.match(await evaluate('document.querySelector("#studio-progress").textContent'),/14 of 14/);
  await visit('recap');
  await evaluate('(()=>{const state=JSON.parse(localStorage.getItem("git-learning-v1"));state.studioRecall={q3:false,q4:true,q5:"invalid",unknown:true};state.missions.push(999);const backup={format:"git-learning-progress",progress:state},transfer=new DataTransfer();transfer.items.add(new File([JSON.stringify(backup)],"studio.json",{type:"application/json"}));const input=document.querySelector("#import-progress");input.files=transfer.files;input.dispatchEvent(new Event("change"));})()');
  await until('document.querySelector("#progress-message").textContent.startsWith("Progress imported")');
  assert.deepEqual(await evaluate('GitLearning.recallResults()'),{q3:false,q4:true});
  assert.equal(await evaluate('JSON.parse(localStorage.getItem("git-learning-v1")).missions.length'),18);
  assert.match(await evaluate('document.querySelector("#progress-summary").textContent'),/1 studio questions to revisit/);
  console.log('PASS: beginner history, all 14 studio goals, wrong-answer paths, drag/keyboard choices, separate recall scoring and persisted weak-question priority.');
  await send('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});
  for(const id of ids){
    await visit(id);
    assert.equal(await evaluate('document.documentElement.scrollWidth <= innerWidth+1'),true,'mobile overflow: '+id);
  }
  await visit('playground');await click('.mobile-menu');
  assert.equal(await evaluate('document.querySelector(".mobile-menu").getAttribute("aria-expanded")'),'true');
  await click('.mobile-menu');
  await evaluate('document.querySelector("#conflict-tool").scrollIntoView({behavior:"instant",block:"start"})');await screenshot('kt-git-mobile.png');
  await visit('why-git');
  await evaluate('document.querySelector("#story").scrollIntoView({behavior:"instant",block:"start"})');
  await screenshot('kt-git-beginner-mobile.png');
  await visit('studio');
  await click('[data-snapshot="editA"]');await click('[data-snapshot="stage"]');
  await click('[data-snapshot="editB"]');await click('[data-snapshot="commit"]');
  assert.equal(await evaluate('document.querySelector("#snapshot-status").textContent'),' M notes.txt');
  await click('[data-commit="C"]');await click('#pointer-check');
  assert.match(await evaluate('document.querySelector("#pointer-feedback").textContent'),/Correct/);
  for(let i=0;i<6;i++) {
    await change('#pointer-challenge',String(i));
    assert.equal(await evaluate('(()=>{const b=document.querySelector("#pointer-board").getBoundingClientRect();return Array.from(document.querySelectorAll("[data-commit]")).every(n=>{const r=n.getBoundingClientRect();return r.left>=b.left&&r.right<=b.right});})()'),true,'all graph nodes fit on mobile');
  }
  await change('#pointer-challenge','1');await click('[data-commit="M"]');await click('#pointer-check');
  await evaluate('document.querySelector("#pointers").scrollIntoView({behavior:"instant",block:"start"})');
  await screenshot('kt-git-studio-mobile.png');
  console.log('PASS: all 23 pages at 390px, responsive navigation and mobile screenshot.');
  // Core content and module navigation remain available without JavaScript.
  await send('Emulation.setScriptExecutionDisabled',{value:true});
  await send('Page.navigate',{url:base+'foundations.html'});await sleep(300);
  await send('Emulation.setScriptExecutionDisabled',{value:false});
  assert.equal(await evaluate('document.documentElement.classList.contains("js")'),false);
  assert.ok(await evaluate('document.querySelector("main").textContent.includes("Three places where your content can exist")'));
  assert.equal(await evaluate('document.querySelectorAll("#course-nav a").length'),23);
  await send('Emulation.setScriptExecutionDisabled',{value:true});
  await send('Page.navigate',{url:base+'why-git.html'});await sleep(300);
  await send('Emulation.setScriptExecutionDisabled',{value:false});
  assert.equal(await evaluate('document.documentElement.classList.contains("js")'),false);
  assert.match(await evaluate('document.querySelector("#meaning").textContent'),/deliberately record/);
  assert.match(await evaluate('document.querySelector("#time-machine").textContent'),/A: correct fact/);
  // Malformed and denied storage both degrade to a usable in-memory experience.
  await visit('index');
  await evaluate('localStorage.setItem("git-learning-v1","not-json")');
  await visit('recap');
  assert.equal(await evaluate('JSON.parse(localStorage.getItem("git-learning-v1")).done.length'),0);
  const injection=await send('Page.addScriptToEvaluateOnNewDocument',{source:'Object.defineProperty(window,"localStorage",{get(){throw new Error("storage denied for test")}});'});
  await visit('recap');await click('#mark-done');await click('#flashcard');await click('#card-known');
  assert.match(await evaluate('document.querySelector("#course-progress").textContent'),/this visit only/);
  await visit('why-git');await click('#beginner-mistake');await click('#beginner-save');
  assert.equal(await evaluate('document.querySelectorAll("[data-version]").length'),2);
  await visit('studio');await click('#recall-start');
  assert.equal(await evaluate('document.querySelectorAll("#recall-form input").length'),3);
  await send('Page.removeScriptToEvaluateOnNewDocument',{identifier:injection.identifier});
  console.log('PASS: no-JavaScript reading, malformed progress and storage-denied fallback.');
  assert.deepEqual(errors,[],'Uncaught browser exceptions');
  assert.deepEqual(missing,[],'Missing resources');
  console.log('PASS: no browser runtime errors or failed local resources. Screenshots: /tmp/kt-git-*.png');
}finally{
  if(ws)ws.close();
  for(const p of pending.values()){clearTimeout(p.timer);}
  browser.kill('SIGTERM');
  await new Promise(r=>server.close(r));
  await rm(profile,{recursive:true,force:true}).catch(()=>{});
}
