/* Educational models only. No Git commands, credentials or network requests. */
(function (root) {
  'use strict';
  const node = (id,x,y,parents=[],refs=[],ghost=false) => ({id,x,y,parents,refs,ghost});
  const A = () => node('A',70,105);
  const B = (refs=[]) => node('B',200,105,['A'],refs);
  const C = (refs=['feature'],ghost=false) => node('C',330,205,['B'],refs,ghost);
  const D = (refs=['main']) => node('D',330,105,['B'],refs);
  const step = (text,nodes) => ({text,nodes});
  const scenes = [
    {id:'fast-forward',title:'Fast-forward: move the name',steps:[
      step('Main points at B. Feature adds C, a later commit whose parent is B. No commits have diverged.',[A(),B(['main']),node('C',330,105,['B'],['feature'])]),
      step('git merge --ff-only feature moves main to C. It creates no merge commit. Both names now point at the same existing commit.',[A(),B(),node('C',330,105,['B'],['main','feature'])])
    ]},
    {id:'merge',title:'Three-way merge: keep both histories',steps:[
      step('Main added D; feature added C. B is their common ancestor. Git compares base B, current D and incoming C.',[A(),B(),C(),D()]),
      step('Resolve any conflicts and test the combined behavior. Merge commit M has two parents: D first, C second. Main moves to M; feature stays at C.',[A(),B(),C(),D([]),node('M',490,105,['D','C'],['main'])])
    ]},
    {id:'rebase',title:'Rebase: apply changes after a newer starting point',steps:[
      step('Feature has C and main has D, both after B. Save a backup before rewriting work. Rebasing will apply the change again B → C on D.',[A(),B(),C(),D()]),
      step('While applying a change again, ours is the new base D plus any commits already applied again. Theirs is the original feature commit being applied again. Resolve for needed behavior, then continue.',[A(),B(),C(),D()]),
      step('C′ has a different parent and therefore a different ID. Feature moves to C′. C still exists via a backup or reflog for some time; rebase is not instant object deletion.',[A(),B(),C(['backup'],true),D(),node('C′',490,105,['D'],['feature'])])
    ]},
    {id:'squash',title:'Squash merge: one combined change',steps:[
      step('Feature has C and E. Main has D. A squash can stage their combined result on main.',[A(),B(),C([]),D(),node('E',460,205,['C'],['feature'])]),
      step('git merge --squash feature stages a result; it does not commit or record a merge parent. After you commit, S has only D as its parent. Feature history remains separate.',[A(),B(),C([]),D([]),node('E',460,205,['C'],['feature']),node('S',580,105,['D'],['main'])])
    ]},
    {id:'revert',title:'Revert: add a correcting commit',steps:[
      step('C introduced a bug. D adds unrelated useful work after C. Main is already shared.',[A(),B(),node('C',330,105,['B']),node('D',460,105,['C'],['main'])]),
      step('git revert C creates R that reverses C’s change in the current context. C and D remain ancestors. Conflicts are possible; test the outcome. No branch history is rewritten.',[A(),B(),node('C',330,105,['B']),node('D',460,105,['C']),node('R',590,105,['D'],['main'])])
    ]},
    {id:'reset',title:'Reset: move the current branch back',steps:[
      step('Local main points to C. First distinguish committed work from staged and unstaged work.',[A(),B(),node('C',330,105,['B'],['main'])]),
      step('git reset --soft B moves main to B and keeps staging and working files. Mixed also resets staging. Hard resets both and can overwrite local work. The branch movement is the same; the file effects differ.',[A(),B(['main']),node('C',330,105,['B'],['old tip · reflog'],true)])
    ]},
    {id:'fetch',title:'Fetch: learn what the server has',steps:[
      step('Your local main and cached origin/main point at B. The actual server has advanced to T. Remote-tracking names are your local records, not live server pointers.',[A(),B(['main','origin/main']),node('T',440,105,['B'],['server main'])]),
      step('git fetch origin downloads objects and updates origin/main to T with the usual fetch mapping. Your local main, index and working files stay at B.',[A(),B(['main']),node('T',440,105,['B'],['origin/main','server main'])])
    ]},
    {id:'force',title:'Force push: replace a server branch tip',steps:[
      step('You rewrote C as C′. Meanwhile a teammate added T on top of C. The server points at T.',[A(),B(),C([]),node('T',490,205,['C'],['server feature']),node('C′',490,105,['B'],['local feature'])]),
      step('An accepted force push moves the server feature name to C′. C and T are no longer ancestors of that branch. Other refs, clones or reflogs may still retain them. This does not erase all copies.',[A(),B(),C([],true),node('T',490,205,['C'],['old server tip'],true),node('C′',490,105,['B'],['local + server feature'])])
    ]}
  ];
  function resolveConflict(text) {
    let value;
    try { value=JSON.parse(text); } catch (_) { return {ok:false,message:'This is not valid JSON yet. Remove conflict markers, choose the intended values, and keep JSON punctuation valid.'}; }
    if (!value || Array.isArray(value) || typeof value !== 'object' || Object.keys(value).length !== 2 ||
      (text.match(/"timeout"\s*:/g)||[]).length!==1 || (text.match(/"retries"\s*:/g)||[]).length!==1)
      return {ok:false,message:'Keep exactly one timeout and one retries property. Duplicate or extra settings can hide mistakes.'};
    if (value.timeout!==20 || value.retries!==3)
      return {ok:false,message:'Valid JSON, but the behavior is wrong. Keep the approved timeout of 20 from main and retries of 3 from feature. Taking an entire side loses one requirement.'};
    return {ok:true,message:'Resolved: timeout 20, retries 3. Both requirements survive. In Git: inspect the diff, run the relevant tests, git add config.json, then continue the operation shown above.'};
  }
  function simulatePush({mode,remote='T',tracking='C',expected='C',protectedBranch=false}) {
    if (!['normal','force','lease','explicit'].includes(mode)) throw new Error('Unknown push mode');
    if (mode==='normal') return {allowed:false,lost:false,message:'Rejected: C′ does not descend from the current server commit. A normal push cannot replace this history.'};
    if (protectedBranch) return {allowed:false,lost:false,message:'Rejected by the modeled server rule: force pushes are disabled. A lease does not bypass repository policy.'};
    if (mode==='lease' && tracking!==remote) return {allowed:false,lost:false,message:'Rejected: the current server commit differs from your local last-known server position. Fetch and inspect the teammate’s changes before deciding what to do.'};
    if (mode==='explicit' && expected!==remote) return {allowed:false,lost:false,message:'Rejected: the current server commit differs from saved exact expected C. The teammate’s T remains on the server branch, even if a background fetch updated origin/feature.'};
    return {allowed:true,lost:remote==='T',message:remote==='T' ?
      'Accepted in this model: server feature now points at C′. Teammate commit T is no longer reachable from that branch. A tracking-based lease allowed this after fetch because it expected T; it never checked that you incorporated T.' :
      'Accepted in this model: the expected remote state still matches. C is replaced by C′ on this branch. A lease checks concurrent movement, not whether the rewrite keeps everyone’s intent.'};
  }
  function evaluatePermission(s) {
    const canWrite=['write','maintain','admin'].includes(s.role);
    const gates=[
      {name:'Signed-in account',ok:s.identity,why:'The credential must sign in as a valid account.'},
      {name:'Repository selected',ok:s.selected,why:'This limited personal token must include the correct repository.'},
      {name:'Organization approval',ok:s.approved,why:'This scenario requires approval of the token by the organization.'},
      {name:'Repository role',ok:canWrite,why:'This action needs Write or higher; a token cannot elevate a Read or Triage user.'},
      {name:'Token access',ok:s.scope==='write',why:'The modeled operation needs Contents: write. A broader repository role cannot add missing token permissions.'}
    ];
    if(s.action==='direct') gates.push({name:'Required pull request',ok:!s.requirePR||s.bypass,why:'A required-PR rule blocks direct pushes unless the actor has an explicitly applicable bypass.'});
    if(s.action==='merge') {
      gates.push({name:'Required approvals',ok:s.approvals>=2||s.bypass,why:'This example requires two approvals of the current change.'});
      gates.push({name:'Required checks',ok:s.checks||s.bypass,why:'This example requires successful checks for the revision being merged.'});
    }
    return {allowed:gates.every(g=>g.ok),gates};
  }
  const api={scenes,resolveConflict,simulatePush,evaluatePermission};
  if(typeof module==='object' && module.exports) module.exports=api;
  if(!root.document) return;
  root.GitVisuals=api;
  const $=s=>document.querySelector(s);
  const esc=root.GitLearning.escape;
  const options=(items)=>items.map(([value,label])=>'<option value="'+value+'">'+esc(label)+'</option>').join('');
  const finish=id=>root.GitLearning.completeMission(id);
  const badge=id=>root.GitLearning.missionDone(id) ? '✓ Exercise completed' : 'Exercise not completed yet';
  const graphRoot=$('#graph-explorer');
  if(graphRoot) {
    graphRoot.innerHTML='<h3>Watch where the branch names point</h3><label class="field">Operation<select id="graph-scene">'+options(scenes.map(s=>[s.id,s.title]))+'</select></label><div id="graph-picture" class="graph-scroll"></div><p id="graph-explanation" role="status"></p><p id="graph-position" class="meta"></p><div class="actions"><button class="btn" id="graph-prev">← Previous step</button><button class="btn btn-primary" id="graph-next">Next step →</button><button class="btn" id="graph-reset">Restart</button></div><p class="meta">Lines connect each commit to its parents on the left. Labels name branches or saved positions. Faded circles show older history. These are simplified pictures; no Git commands run here.</p>';
    let index=0;
    const render=()=>{
      const scene=scenes.find(s=>s.id===$('#graph-scene').value), current=scene.steps[index];
      const lines=current.nodes.flatMap(n=>n.parents.map(id=>{
        const p=current.nodes.find(p=>p.id===id);
        return '<path class="edge" d="M'+p.x+' '+p.y+' L'+n.x+' '+n.y+'"/>';
      })).join('');
      const nodes=current.nodes.map(n=>'<g'+(n.ghost?' class="faded"':'')+'><circle class="node" cx="'+n.x+'" cy="'+n.y+'" r="20"/><text x="'+n.x+'" y="'+(n.y+5)+'" text-anchor="middle" font-size="14">'+esc(n.id)+'</text>'+n.refs.map((r,i)=>'<text class="label" text-anchor="middle" x="'+n.x+'" y="'+(n.y-34-i*18)+'">'+esc(r)+'</text>').join('')+'</g>').join('');
      $('#graph-picture').innerHTML='<svg class="graph-canvas" viewBox="0 0 700 270" role="img" aria-labelledby="graph-title graph-desc"><title id="graph-title">'+esc(scene.title)+'</title><desc id="graph-desc">'+esc(current.text)+'</desc>'+lines+nodes+'</svg>';
      $('#graph-explanation').textContent=current.text;
      $('#graph-position').textContent='Step '+(index+1)+' of '+scene.steps.length;
      $('#graph-prev').disabled=index===0;
      $('#graph-next').disabled=index===scene.steps.length-1;
    };
    $('#graph-scene').onchange=()=>{index=0;render();};
    $('#graph-prev').onclick=()=>{index--;render();};
    $('#graph-next').onclick=()=>{index++;render();};
    $('#graph-reset').onclick=()=>{index=0;render();};
    render();
  }
  const conflictRoot=$('#conflict-tool');
  if(conflictRoot) {
    conflictRoot.innerHTML='<h3>Keep both requirements</h3><p>Product requirement: main’s approved timeout <b>20</b> and feature’s retries <b>3</b>. Remove markers and produce valid JSON.</p><label class="field">Operation<select id="conflict-operation"><option value="merge">On main: git merge feature</option><option value="rebase">On feature: git rebase main</option></select></label><div class="tool-grid"><div><b>Base</b><pre>{"timeout": 10, "retries": 1}</pre></div><div><b>Main</b><pre>{"timeout": 20, "retries": 1}</pre></div><div><b>Feature</b><pre>{"timeout": 30, "retries": 3}</pre></div></div><p id="conflict-context" class="note"></p><label class="field" for="conflict-input">config.json — edit the conflict</label><textarea id="conflict-input" spellcheck="false" autocapitalize="off"></textarea><div class="actions"><button class="btn btn-primary" id="conflict-check">Check resolution</button><button class="btn" id="conflict-ours">Try whole ours</button><button class="btn" id="conflict-theirs">Try whole theirs</button><button class="btn" id="conflict-reset">Reset conflict</button></div><p id="conflict-feedback" role="status"></p><p id="conflict-complete" class="meta"></p>';
    const reset=()=>{
      const rebase=$('#conflict-operation').value==='rebase';
      $('#conflict-context').textContent=rebase?'Rebase: ours = main (the new base), theirs = the feature commit being applied again. Stage and run git rebase --continue after testing.':'Merge on main: ours = current main, theirs = incoming feature. Stage and run git merge --continue after testing.';
      $('#conflict-input').value='{\n<<<<<<< HEAD\n  "timeout": 20,\n  "retries": 1\n||||||| base\n  "timeout": 10,\n  "retries": 1\n=======\n  "timeout": 30,\n  "retries": 3\n>>>>>>> '+(rebase?'feature commit being applied again':'feature')+'\n}\n';
      $('#conflict-feedback').textContent='Both whole-side choices are valid JSON but fail one requirement. Try them, then combine the intended values.';
      $('#conflict-complete').textContent=badge(0);
    };
    const check=()=>{
      const result=resolveConflict($('#conflict-input').value);
      $('#conflict-feedback').textContent=result.message;
      if(result.ok) finish(0);
      $('#conflict-complete').textContent=badge(0);
    };
    $('#conflict-check').onclick=check;
    $('#conflict-ours').onclick=()=>{$('#conflict-input').value='{\n  "timeout": 20,\n  "retries": 1\n}';check();};
    $('#conflict-theirs').onclick=()=>{$('#conflict-input').value='{\n  "timeout": 30,\n  "retries": 3\n}';check();};
    $('#conflict-reset').onclick=reset; $('#conflict-operation').onchange=reset; reset();
  }
  const pushRoot=$('#push-tool');
  if(pushRoot) {
    pushRoot.innerHTML='<h3>Predict a push after a teammate changed the branch</h3><p>Your rewritten feature tip is C′, with parent B. Previously the remote was B → C. A teammate may have added T after C. Your saved exact expected ID remains C.</p><div class="tool-grid"><label class="field">Push mode<select id="push-mode">'+options([['normal','Normal push'],['force','--force'],['lease','--force-with-lease (tracking-based)'],['explicit','--force-with-lease=refs/heads/feature:C']])+'</select></label><label class="field">Your prediction<select id="push-prediction"><option value="reject">Reject</option><option value="accept">Accept</option></select></label></div><label class="answer"><input type="checkbox" id="push-race" checked> Teammate has pushed T</label><label class="answer"><input type="checkbox" id="push-protected"> Server blocks force pushes</label><div class="actions"><button class="btn" id="push-fetch">Simulate background fetch</button><button class="btn" id="push-reset">Reset tracking to C</button></div><div id="push-refs" class="tool-grid"></div><button class="btn btn-primary" id="push-evaluate">Evaluate this push</button><p id="push-feedback" role="status"></p><p id="push-complete" class="meta"></p><p class="meta">C/C′/T stand for full commit IDs here. Each check starts from the displayed state and changes no real project. Goal: predict the explicit lease rejecting T, with force pushes otherwise allowed.</p>';
    let tracking='C';
    const render=()=>{
      $('#push-refs').innerHTML='<p>Local feature<br><strong>C′</strong></p><p>Actual server feature<br><strong>'+($('#push-race').checked?'T':'C')+'</strong></p><p>Local origin/feature<br><strong>'+tracking+'</strong></p><p>Saved expected ID<br><strong>C</strong></p>';
      $('#push-feedback').textContent='Choose your prediction, then evaluate.';
      $('#push-complete').textContent=badge(1);
    };
    $('#push-fetch').onclick=()=>{tracking=$('#push-race').checked?'T':'C';render();};
    $('#push-reset').onclick=()=>{tracking='C';render();};
    ['#push-race','#push-mode','#push-protected'].forEach(s=>$(s).onchange=render);
    $('#push-evaluate').onclick=()=>{
      const s={mode:$('#push-mode').value,remote:$('#push-race').checked?'T':'C',tracking,expected:'C',protectedBranch:$('#push-protected').checked};
      const result=simulatePush(s), predicted=$('#push-prediction').value===(result.allowed?'accept':'reject');
      $('#push-feedback').textContent=(predicted?'Prediction correct. ':'Prediction needs revision. ')+result.message;
      if(predicted && s.mode==='explicit' && s.remote==='T' && !s.protectedBranch && !result.allowed) finish(1);
      $('#push-complete').textContent=badge(1);
    };
    render();
  }
  const permissionRoot=$('#permission-tool');
  if(permissionRoot) {
    permissionRoot.innerHTML='<h3>Find the missing access gate</h3><p>Scenario: a same-repository pull request, authenticated with a fine-grained PAT. Goal: allow the merge with the <b>Write</b> role, Contents: write, two approvals, passing checks, a required-PR rule, and no bypass.</p><div class="tool-grid"><label class="field">Repository role<select id="perm-role">'+options(['read','triage','write','maintain','admin'].map(x=>[x,x]))+'</select></label><label class="field">Token Contents permission<select id="perm-scope">'+options([['read','Read'],['write','Write'],['none','None']])+'</select></label><label class="field">Action<select id="perm-action">'+options([['merge','Merge the PR'],['direct','Push directly to main'],['feature','Push an ordinary feature branch']])+'</select></label><label class="field">Current approvals<select id="perm-approvals">'+options([['0','0'],['1','1'],['2','2']])+'</select></label></div><div class="tool-grid">'+[['identity','Signed in as a valid account',true],['selected','Token includes this repository',true],['approved','Token approved by organization',true],['require','Require PR for main',true],['checks','Required checks passed',false],['bypass','This account has an allowed exception',false]].map(([id,label,checked])=>'<label class="answer"><input type="checkbox" id="perm-'+id+'"'+(checked?' checked':'')+'>'+label+'</label>').join('')+'</div><button class="btn btn-primary" id="perm-evaluate">Check access</button><div id="perm-gates" class="gate-list"></div><p id="perm-feedback" role="status"></p><p id="perm-complete" class="meta"></p><p class="meta">This example checks only the settings shown here. Real access can also depend on SSO, IP policy, endpoint-specific scopes, workflow-file permissions, rule targets, merge queue and other rules. Here only main has PR/check rules; bypass affects only the modeled rules, never sign-in or credential capabilities.</p>';
    $('#perm-evaluate').onclick=()=>{
      const s={role:$('#perm-role').value,scope:$('#perm-scope').value,action:$('#perm-action').value,approvals:Number($('#perm-approvals').value),identity:$('#perm-identity').checked,selected:$('#perm-selected').checked,approved:$('#perm-approved').checked,requirePR:$('#perm-require').checked,checks:$('#perm-checks').checked,bypass:$('#perm-bypass').checked};
      const result=evaluatePermission(s);
      $('#perm-gates').innerHTML=result.gates.map(g=>'<p><b>'+(g.ok?'✓ Pass: ':'✕ Blocked: ')+esc(g.name)+'</b><br>'+esc(g.why)+'</p>').join('');
      $('#perm-feedback').textContent=result.allowed?'Allowed by every gate in this model. Verify actual repository and organization settings before relying on access.':'Blocked. Fix each failed gate; increasing a role does not solve every layer.';
      if(result.allowed && s.action==='merge' && s.role==='write' && s.requirePR && !s.bypass) finish(2);
      $('#perm-complete').textContent=badge(2);
    };
    $('#perm-complete').textContent=badge(2);
  }
})(typeof window!=='undefined'?window:globalThis);
