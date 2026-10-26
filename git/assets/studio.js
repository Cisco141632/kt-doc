/* Browser-only learning models. No repository, shell or network access. */
(function (root) {
  'use strict';
  const clone = value => JSON.parse(JSON.stringify(value));
  const versions={base:'Our solar system\nEight planets orbit the Sun.',A:'Our amazing solar system\nEight planets orbit the Sun.',B:'Our amazing solar system\nEight planets orbit the Sun.\nThe Sun is a star.'};
  const snapshotMissions=[
    {id:3,title:'Commit A while keeping B as an unstaged edit',start:{head:'base',index:'base',work:'base'},hint:'Edit to A → stage → edit to B → commit. The index remembers A.',cue:'A commit takes its content from the index, even if the working file has changed again.'},
    {id:4,title:'Unstage A without losing the working version B',start:{head:'base',index:'A',work:'B'},hint:'Unstage changes the index. The working file should remain B.',cue:'Unstage changes the next proposed snapshot, not your working edits.'},
    {id:5,title:'Restore working content from the staged version A',start:{head:'base',index:'A',work:'B'},hint:'Restore the working file. In this operation, the source is the index, not HEAD.',cue:'Plain git restore -- path copies from the index by default. Here it restores A, not base.'}
  ];
  function snapshotStart(mission=0) {
    return {...snapshotMissions[mission].start,commits:0,message:'Choose a command and watch which lane changes.'};
  }
  function snapshotStep(current,action) {
    const s=clone(current);
    const messages={
      editA:'Editor: only the working file changed to A.',
      editB:'Editor: only the working file changed to B.',
      stage:'git add: copied the current working content into the index.',
      unstage:'git restore --staged: copied HEAD into the index; working edits remain.',
      restore:'git restore: replaced working content with the index version.',
      commit:s.index===s.head?'Nothing staged to commit.':'git commit: recorded the index as a new commit; the working file did not change.'
    };
    if(!(action in messages)) throw new Error('Unknown snapshot action');
    if(action==='editA') s.work='A';
    if(action==='editB') s.work='B';
    if(action==='stage') s.index=s.work;
    if(action==='unstage') s.index=s.head;
    if(action==='restore') s.work=s.index;
    if(action==='commit' && s.index!==s.head) {s.head=s.index;s.commits++;}
    s.message=messages[action];
    return s;
  }
  function snapshotGoal(s,mission,action) {
    return mission===0 ? action==='commit' && s.commits>0 && s.head==='A' && s.index==='A' && s.work==='B' :
      mission===1 ? action==='unstage' && s.head==='base' && s.index==='base' && s.work==='B' :
      action==='restore' && s.head==='base' && s.index==='A' && s.work==='A';
  }
  const n=(id,x,y,parents=[],candidate=false)=>({id,x,y,parents,candidate});
  const diverged=()=>[n('A',65,120),n('B',190,120,['A']),n('D',325,70,['B']),n('C',325,200,['B'])];
  const pointerChallenges=[
    {id:6,title:'Fast-forward',command:'On main at B: git merge --ff-only feature',ref:'main',start:'B',target:'C',topic:'merge',
      nodes:[n('A',65,130),n('B',230,130,['A']),n('C',410,130,['B'])],
      before:'Feature points at C. Main has no separate new commits.',
      why:'Main moves to the existing descendant C. No merge commit is created.',cue:'Fast-forward = move the name.'},
    {id:7,title:'Three-way merge',command:'On main at D: git merge feature',ref:'main',start:'D',target:'M',topic:'merge',
      nodes:[...diverged(),n('M',510,120,['D','C'],true)],
      before:'Feature points at C. D and C diverged from B. Assume you resolve conflicts, test and complete the merge.',
      why:'Main moves to M, whose parents are D and C. Both ancestry lines are preserved.',cue:'Merge = two histories meet.'},
    {id:8,title:'Rebase',command:'On feature at C: git rebase main',ref:'feature',start:'C',target:'C′',topic:'rebase',
      nodes:[...diverged(),n('C′',510,70,['D'],true)],
      before:'Main points at D. Assume replay succeeds with a nonempty change and any conflicts are resolved.',
      why:'Feature moves to C′, which replays the change on D and has a different parent and ID. Main remains at D.',cue:'Rebase = replay, then move the feature name.'},
    {id:9,title:'Revert a shared mistake',command:'On main at D: git revert C',ref:'main',start:'D',target:'R',topic:'undo-recovery',
      nodes:[n('A',55,130),n('B',175,130,['A']),n('C',295,130,['B']),n('D',415,130,['C']),n('R',545,130,['D'],true)],
      before:'C introduced a mistake. D is useful later work. Assume the revert is resolved and committed.',
      why:'Main moves forward to R, the corrective commit. C and D remain in the ancestry.',cue:'Revert = add a correction.'},
    {id:10,title:'Soft reset private work',command:'On main at C: git reset --soft B',ref:'main',start:'C',target:'B',topic:'undo-recovery',
      nodes:[n('A',65,130),n('B',230,130,['A']),n('C',410,130,['B'])],
      before:'This is private disposable history. You intend to move the branch while retaining the index and working file.',
      why:'Main moves back to B. Soft reset leaves the index and working content intact; it does not automatically delete C’s object.',cue:'Soft reset = move the name, keep staged and working content.'},
    {id:11,title:'Fetch the teammate’s update',command:'On main at B: git fetch origin',ref:'main',start:'B',target:'B',topic:'branches-remotes',
      nodes:[n('A',65,130),n('B',230,130,['A']),n('T',410,130,['B'])],
      before:'The server’s main is T. The usual fetch mapping updates origin/main to T. Where does your local main point afterward?',
      why:'Local main stays at B. The remote-tracking reference origin/main moves to T. Fetch alone does not integrate T into main.',cue:'Fetch = learn about remote history.'}
  ];
  const incidents=[
    {id:12,title:'The rejected push',topic:'branches-remotes',summary:'Your feature works locally. Git rejects your ordinary push because your teammate pushed first.',
      evidence:[['Status','On branch feature\nworking tree clean'],['After inspection','origin/feature has commit T\nyour feature has commit L\nboth descend from B'],['Team agreement','Shared feature branch.\nKeep the teammate’s work.\nUse merge to integrate.']],
      steps:[
        {prompt:'What should you do before choosing an integration action?',choices:[
          ['Force push immediately','This can remove the teammate’s commits from the branch. A rejection is a signal to inspect.'],
          ['Fetch and inspect both sides of the graph','Correct. Fresh remote information and both changes’ intent guide the integration.'],
          ['Delete the local branch','This risks losing your own useful work without diagnosing the divergence.']],correct:1},
        {prompt:'You confirm that T and L both matter. The team uses merges on this shared branch. Next?',choices:[
          ['Merge the fetched teammate branch, resolving for both intentions','Correct. Integrate the inspected origin/feature into your feature, resolving conflicts and reviewing the result.'],
          ['Reset hard to origin/feature','That replaces local state with the teammate’s tip and abandons your local line of work.'],
          ['Refresh the lease and push the same replacement','A newer expectation does not prove you preserved the teammate’s content.']],correct:0},
        {prompt:'The merge is complete. How do you finish?',choices:[
          ['Push with --force so it is faster','Force does not make this safer. The integration should permit a normal fast-forward update.'],
          ['Assume a clean text merge means correct behavior','Semantic conflicts can remain. Check the combined behavior.'],
          ['Review the combined diff, run tests, then push normally','Correct. If someone pushes again, another rejection means inspect that newer state.']],correct:2}],
      cue:'Rejected push → inspect → integrate → test → normal push.',
      commands:'git fetch origin\ngit log --graph --oneline --all\ngit merge origin/feature\n# Resolve as needed; inspect and test.\ngit push origin feature'},
    {id:13,title:'The missing committed project',topic:'undo-recovery',summary:'In a disposable repository, a mistaken reset moved your branch backward. A useful committed file vanished from the checkout.',
      evidence:[['What was recorded','The file was included in a commit.\nIt was not just an unsaved editor tab.'],['Current state','working tree clean\nmain points at an older commit'],['Clue','Local reflog still includes the earlier tip.\nNo cleanup or object pruning has run.']],
      steps:[
        {prompt:'Where do you look for evidence of the old branch tip?',choices:[
          ['Run cleanup to simplify the repository','Cleanup can remove recovery evidence. Inspect first.'],
          ['Inspect local reflog and show the candidate commit','Correct. Reflog records local reference movement; inspect the content to identify the right tip.'],
          ['Assume all recorded history is gone','Moving a branch name does not immediately erase every old commit object.']],correct:1},
        {prompt:'You found the exact commit and confirmed it contains the file. First preserve it how?',choices:[
          ['Guess HEAD@{1} and hard reset','The reflog position may have changed. A destructive reset is unnecessary just to preserve a found commit.'],
          ['Create a rescue branch at the inspected commit ID','Correct. A named reference makes the discovered commit reachable while you plan recovery.'],
          ['Force push the old tip to main','There is no evidence that replacing a shared remote branch is needed.']],correct:1},
        {prompt:'The rescued content is now reachable. What is the next decision?',choices:[
          ['Compare rescued and current work, then choose a reviewed integration','Correct. You may need a selected file, a cherry-pick or another deliberate integration; preserve unrelated work.'],
          ['Delete every newer commit','Later work may still be valuable. Recovery is not a reason to discard it.'],
          ['Promise this also recovers any never-saved file','Git cannot recover content it never recorded.']],correct:0}],
      cue:'Find → inspect → name the rescued tip → integrate deliberately.',
      commands:'git reflog --date=iso\ngit show OLD_TIP\ngit branch rescue/project OLD_TIP\ngit log --graph --oneline --all'},
    {id:14,title:'The rebase with two “correct” answers',topic:'conflicts',summary:'Rebasing your feature onto main stops in config.json. The main timeout must stay 20; the feature must increase retries to 3.',
      evidence:[['Base','timeout: 10\nretries: 1'],['Main / new base','timeout: 20\nretries: 1'],['Feature commit being replayed','timeout: 30\nretries: 3']],
      steps:[
        {prompt:'During this rebase, what does “ours” mean?',choices:[
          ['My original feature, because I wrote it','During rebase, that intuition is reversed. Check the operation and actual stage content.'],
          ['The new base plus commits already replayed','Correct. Theirs is the original commit being replayed.'],
          ['Whichever file has the newest timestamp','Ours/theirs are operation roles, not timestamps.']],correct:1},
        {prompt:'Which resolution preserves the two stated requirements?',choices:[
          ['Use timeout 20 and retries 3','Correct. Neither whole side contains both requirements; construct the intended combination.'],
          ['Accept the complete main side: 20 / 1','This loses the requested retry change.'],
          ['Accept both conflicting JSON blocks','Duplicate settings or invalid JSON do not resolve the intended behavior.']],correct:0},
        {prompt:'After editing the correct result, what comes next?',choices:[
          ['Skip the replayed commit','Skip omits its replay. It is not a generic conflict-fixing command.'],
          ['Run merge --continue','This operation is a rebase. Use the matching continuation.'],
          ['Stage, inspect, test and rebase --continue','Correct. Later replayed commits may need their own contextual resolution.']],correct:2}],
      cue:'Identify the operation → preserve intent → stage → test → continue.',
      commands:'git rebase --show-current-patch\ngit show :2:config.json\ngit show :3:config.json\n# Edit to timeout 20 / retries 3.\ngit add config.json\n# Inspect and test.\ngit rebase --continue'}
  ];
  const pairs=[
    {id:'staged',task:'Inspect what the next ordinary commit will contain',command:'git diff --staged',why:'Compare the index with HEAD before committing.'},
    {id:'fetch',task:'Download remote updates without integrating them',command:'git fetch origin',why:'Learn the remote state; your local branch normally stays put.'},
    {id:'revert',task:'Record an inverse of a shared bad commit',command:'git revert COMMIT',why:'Add a corrective commit and retain existing ancestry.'},
    {id:'reflog',task:'Find earlier local reference movements',command:'git reflog',why:'Use local recorded movements to find a candidate recovery tip.'},
    {id:'unstage',task:'Unstage a file while keeping working edits',command:'git restore --staged -- file',why:'Reset the index path from HEAD without discarding working content.'},
    {id:'rescue',task:'Keep an inspected old commit reachable by name',command:'git branch rescue/work COMMIT',why:'Create a reference before attempting more recovery operations.'},
    {id:'bisect',task:'Start searching for the commit that introduced a regression',command:'git bisect start',why:'Then supply good/bad boundaries and a repeatable classification test.'},
    {id:'continue',task:'Continue after resolving and staging a rebase conflict',command:'git rebase --continue',why:'Continue the matching operation; later commits may conflict too.'}
  ];
  function shuffle(items,rng=Math.random) {
    const a=[...items];
    for(let i=a.length-1;i>0;i--){const j=Math.floor(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
    return a;
  }
  function recallRound(questions,results,rng=Math.random) {
    const groups=[questions.filter(q=>results[q.id]===false),questions.filter(q=>!Object.hasOwn(results,q.id)),questions.filter(q=>results[q.id]===true)];
    return groups.flatMap(g=>shuffle(g,rng)).slice(0,5);
  }
  const correctFact='Eight planets orbit the Sun.', mistakenFact='Two planets orbit the Sun.';
  function beginnerStart(){return {work:correctFact,history:[{id:'A',text:correctFact,message:'Record the correct planet fact'}],selected:'A'};}
  function beginnerStep(current,action) {
    const s=clone(current);
    if(action==='mistake')s.work=mistakenFact;
    else if(action==='restore')s.work=s.history.find(v=>v.id===s.selected).text;
    else if(action==='save' && s.work!==s.history.at(-1).text) s.history.push({id:String.fromCharCode(65+s.history.length),text:s.work,message:s.work===correctFact?'Record the corrected fact':'Record the mistaken fact'});
    else if(action!=='save')throw new Error('Unknown beginner action');
    return s;
  }
  function beginnerGoal(s){return s.history.length>=3 && s.history.some(v=>v.text===mistakenFact) && s.history.at(-1).text===correctFact;}
  const api={versions,snapshotMissions,snapshotStart,snapshotStep,snapshotGoal,pointerChallenges,incidents,pairs,shuffle,recallRound,beginnerStart,beginnerStep,beginnerGoal};
  if(typeof module==='object' && module.exports) module.exports=api;
  if(!root.document) return;
  root.GitStudio=api;
  const $=(s,ctx=document)=>ctx.querySelector(s), $$=(s,ctx=document)=>Array.from(ctx.querySelectorAll(s));
  const L=root.GitLearning, esc=L.escape;
  const option=(value,text)=>'<option value="'+value+'">'+esc(text)+'</option>';
  const complete=id=>{L.completeMission(id);progress();};
  const badge=id=>L.missionDone(id)?'✓ Practised':'○ To practise';
  function progress() {
    if($('#studio-progress')) $('#studio-progress').textContent=Array.from({length:14},(_,i)=>i+3).filter(id=>L.missionDone(id)).length+' of 14 studio goals practised · saved in your learning progress';
  }
  const beginner=$('#beginner-lab');
  if(beginner) {
    let s=beginnerStart(),message='Version A is already recorded. Make a mistake to see why history helps.';
    beginner.innerHTML='<div class="beginner-goal"><span class="chip">Your first Git idea</span><h3>Keep the story, repair the sentence</h3><p id="beginner-goal" role="status"></p></div><div class="beginner-columns"><div class="paper-preview"><span class="eyebrow">Working project · what you are editing</span><h3>Our solar system</h3><p id="beginner-work"></p><span id="beginner-state" class="chip"></span></div><div class="paper-preview"><span class="eyebrow">Selected saved version</span><h3 id="beginner-selected"></h3><p id="beginner-saved"></p><button class="btn" id="beginner-restore">Use this version in the working project</button></div></div><div class="actions"><button class="btn" id="beginner-mistake">1 · Make a mistaken edit</button><button class="btn btn-primary" id="beginner-save">2 · Record a snapshot</button><button class="btn" id="beginner-reset">Start over</button></div><p class="meta">3 · Choose A below, use its saved content, then record the correction.</p><div id="beginner-history" class="snapshot-timeline" aria-label="Saved versions"></div><p id="beginner-feedback" class="studio-feedback" role="status"></p>';
    const render=()=>{
      const selected=s.history.find(v=>v.id===s.selected);
      $('#beginner-work').textContent=s.work; $('#beginner-saved').textContent=selected.text;
      $('#beginner-selected').textContent='Version '+selected.id;
      $('#beginner-state').textContent=s.work===s.history.at(-1).text?'Same as the latest saved version':'Changed · not recorded yet';
      $('#beginner-save').disabled=s.work===s.history.at(-1).text||s.history.length>=20;
      $('#beginner-history').innerHTML=s.history.map(v=>'<button class="version-stop" data-version="'+v.id+'" aria-pressed="'+(v.id===s.selected)+'"><b>'+v.id+'</b><span>'+esc(v.message)+'</span></button>').join('<span class="timeline-arrow" aria-hidden="true">→</span>');
      $$('[data-version]',beginner).forEach(b=>b.onclick=()=>{s.selected=b.dataset.version;render();$('[data-version="'+s.selected+'"]',beginner).focus();});
      $('#beginner-feedback').textContent=message;
      $('#beginner-goal').textContent=beginnerGoal(s)?'✓ You recovered the correct content and kept the mistake visible in history.':badge(17)+' · Record a mistake, restore A, then record the correction.';
    };
    ['mistake','restore','save'].forEach(action=>$('#beginner-'+action).onclick=()=>{
      s=beginnerStep(s,action);
      message=action==='save'?'Snapshot recorded. Earlier saved versions remain available.':action==='restore'?'The working sentence now matches the selected version. Record a snapshot to save the correction.':'The working sentence changed. Your saved history has not changed yet.';
      if(beginnerGoal(s))complete(17);render();
    });
    $('#beginner-reset').onclick=()=>{s=beginnerStart();message='Fresh model. Your recorded learning completion is kept.';render();};
    render();
  }
  const snapshot=$('#snapshot-studio');
  if(snapshot) {
    let mission=0,s=snapshotStart(),history=[],last='',log=[];
    snapshot.innerHTML='<div class="station-heading"><span class="chip">Manipulate the model</span><label class="field">Practice goal<select id="snapshot-mission">'+snapshotMissions.map((m,i)=>option(i,m.title)).join('')+'</select></label></div><div id="snapshot-lanes" class="snapshot-lanes"></div><div class="snapshot-status"><b>git status --short</b><code id="snapshot-status"></code></div><div class="command-pad"><button class="btn" data-snapshot="editA">Edit title → A</button><button class="btn" data-snapshot="editB">Add a fact → B</button><button class="btn" data-snapshot="stage">git add → stage</button><button class="btn btn-primary" data-snapshot="commit">git commit</button><button class="btn" data-snapshot="unstage">Unstage</button><button class="btn" data-snapshot="restore">Restore working file</button><button class="btn" id="snapshot-undo">Undo model step</button><button class="btn" id="snapshot-reset">Reset model</button></div><p id="snapshot-feedback" class="studio-feedback" role="status"></p><p id="snapshot-goal" role="status"></p><details class="reveal"><summary>Show a hint</summary><p id="snapshot-hint"></p></details><details><summary>Read the recent command trail</summary><ol id="snapshot-log"></ol></details><p class="meta">One tracked file, notes.txt. The restore button replaces working edits in this model. In a real repository, preserve needed edits before restoring.</p>';
    const render=()=>{
      const changed=last?['work','index','head'].filter(k=>s[k]!==last[k]):[];
      $('#snapshot-lanes').innerHTML=[['work','Working file','What you are editing'],['index','Staging area / index','Selected for the next commit'],['head','HEAD snapshot','What the latest commit recorded']].map(([key,title,sub],i)=>'<article class="snapshot-lane '+(changed.includes(key)?'just-changed':'')+'"><span class="lane-number">0'+(i+1)+'</span><h3>'+title+'</h3><small>'+sub+'</small><div class="version-tag">Version '+esc(s[key])+'</div><pre>'+esc(versions[s[key]])+'</pre></article>').join('');
      const status=(s.index===s.head?' ':'M')+(s.work===s.index?' ':'M');
      $('#snapshot-status').textContent=status==='  '?'Clean working tree':status+' notes.txt';
      $('#snapshot-status').title='First column: index versus HEAD. Second column: working file versus index.';
      $('#snapshot-feedback').textContent=s.message;
      $('#snapshot-goal').textContent=badge(snapshotMissions[mission].id)+' · '+snapshotMissions[mission].cue;
      $('#snapshot-hint').textContent=snapshotMissions[mission].hint;
      $('#snapshot-undo').disabled=!history.length;
      $('[data-snapshot="commit"]').disabled=s.index===s.head;
      $('#snapshot-log').innerHTML=log.map(x=>'<li>'+esc(x)+'</li>').join('');
    };
    $$('[data-snapshot]',snapshot).forEach(b=>b.onclick=()=>{
      const action=b.dataset.snapshot;
      history.push(clone(s));last=clone(s);s=snapshotStep(s,action);
      log=[...log,s.message].slice(-6);
      if(snapshotGoal(s,mission,action))complete(snapshotMissions[mission].id);
      render();
    });
    const reset=()=>{s=snapshotStart(mission);history=[];last='';log=[];render();};
    $('#snapshot-mission').onchange=()=>{mission=Number($('#snapshot-mission').value);reset();};
    $('#snapshot-reset').onclick=reset;
    $('#snapshot-undo').onclick=()=>{last=clone(s);s=history.pop();s.message='Undid a browser model step. This is not a Git undo command.';log.push(s.message);render();};
    render();
  }
  const pointer=$('#pointer-studio');
  if(pointer) {
    let selected=null,challenge=0,feedback='Place the badge before checking your prediction.';
    pointer.innerHTML='<label class="field">History challenge<select id="pointer-challenge">'+pointerChallenges.map((c,i)=>option(i,c.title)).join('')+'</select></label><p id="pointer-before"></p><code id="pointer-command" class="operation-banner"></code><div class="actions"><button class="branch-token" draggable="true" id="pointer-token">Branch badge</button><span class="meta">Drag the badge, or select a commit below.</span></div><div class="pointer-scroll"><div id="pointer-board" class="pointer-board"></div></div><p id="pointer-selection" class="meta" role="status"></p><div class="actions"><button class="btn btn-primary" id="pointer-check">Check my prediction</button><button class="btn" id="pointer-next">Next challenge →</button></div><p id="pointer-feedback" class="studio-feedback" role="status"></p><p id="pointer-complete" class="meta"></p>';
    const render=()=>{
      const c=pointerChallenges[challenge];
      $('#pointer-before').textContent=c.before;$('#pointer-command').textContent=c.command;
      $('#pointer-token').textContent=c.ref+' → '+(selected||'?');
      const lines=c.nodes.flatMap(node=>node.parents.map(id=>{
        const parent=c.nodes.find(n=>n.id===id);
        return '<path d="M'+parent.x+' '+parent.y+'L'+node.x+' '+node.y+'"/>';
      })).join('');
      $('#pointer-board').innerHTML='<svg viewBox="0 0 640 280" preserveAspectRatio="none" aria-hidden="true">'+lines+'</svg>'+c.nodes.map(node=>'<button class="commit-target '+(node.candidate?'candidate ':'')+(selected===node.id?'selected':'')+'" style="left:'+(node.x/640*100)+'%;top:'+(node.y/280*100)+'%" data-commit="'+node.id+'" aria-label="Predict '+esc(c.ref)+' at commit '+node.id+(node.candidate?', possible new commit':'')+'" aria-pressed="'+(selected===node.id)+'">'+node.id+(selected===node.id?'<span class="placed-ref">'+esc(c.ref)+'</span>':'')+'</button>').join('');
      $$('[data-commit]',pointer).forEach(button=>{
        const choose=()=>{selected=button.dataset.commit;feedback='Your prediction is set. Check it to compare with the operation’s effect.';render();$('[data-commit="'+selected+'"]',pointer).focus();};
        button.onclick=choose;
        button.ondragover=e=>e.preventDefault();
        button.ondrop=e=>{e.preventDefault();if(e.dataTransfer.getData('text/plain')==='git-studio-ref')choose();};
      });
      $('#pointer-selection').textContent=selected?'Predicted '+c.ref+' → '+selected:'Currently '+c.ref+' → '+c.start+'. Select its location after the operation.';
      $('#pointer-feedback').textContent=feedback;
      $('#pointer-complete').textContent=badge(c.id)+' · Challenge '+(challenge+1)+' of '+pointerChallenges.length;
    };
    $('#pointer-token').ondragstart=e=>{e.dataTransfer.setData('text/plain','git-studio-ref');};
    $('#pointer-token').onclick=()=>{$('[data-commit]',pointer).focus();};
    const reset=()=>{selected=null;feedback='Place the badge before checking your prediction.';render();};
    $('#pointer-challenge').onchange=()=>{challenge=Number($('#pointer-challenge').value);reset();};
    $('#pointer-check').onclick=()=>{
      const c=pointerChallenges[challenge];
      if(!selected)feedback='Select a commit first. You can use Tab and Enter, click, or drag the badge.';
      else if(selected===c.target){feedback='Correct. '+c.why+' Remember: '+c.cue;complete(c.id);}
      else feedback='Try again. '+c.why+' Choose the commit that matches that result.';
      render();
    };
    $('#pointer-next').onclick=()=>{challenge=(challenge+1)%pointerChallenges.length;$('#pointer-challenge').value=String(challenge);reset();};
    render();
  }
  const incident=$('#incident-studio');
  if(incident) {
    let active=0,phase=0,passed=false,feedback='';
    incident.innerHTML='<label class="field">Choose an incident<select id="incident-select">'+incidents.map((c,i)=>option(i,c.title)).join('')+'</select></label><p id="incident-summary" class="lead"></p><div id="incident-evidence" class="evidence-grid"></div><div id="incident-route" class="incident-route" aria-label="Decision progress"></div><div id="incident-step"></div><p id="incident-feedback" class="studio-feedback" role="status" tabindex="-1"></p><div class="actions"><button class="btn btn-primary" id="incident-next" disabled>Next decision →</button><button class="btn" id="incident-reset">Restart incident</button></div><p id="incident-complete" class="meta"></p>';
    const render=()=>{
      const c=incidents[active];
      $('#incident-summary').textContent=c.summary;
      $('#incident-evidence').innerHTML=c.evidence.map(([title,body])=>'<details><summary><span class="chip">Evidence</span> '+esc(title)+'</summary><pre>'+esc(body)+'</pre></details>').join('');
      $('#incident-route').innerHTML=['Inspect','Choose','Verify'].map((title,i)=>'<span class="'+(phase>i?'done':phase===i?'current':'')+'">'+(phase>i?'✓':i+1)+' · '+title+'</span>').join('<i aria-hidden="true">→</i>');
      $('#incident-feedback').textContent=feedback;
      $('#incident-complete').textContent=badge(c.id);
      $('#incident-next').disabled=!passed||phase===3;
      if(phase===3) {
        $('#incident-step').innerHTML='<div class="case-solved"><span class="chip">Case reviewed</span><h3>'+esc(c.cue)+'</h3><p>Explain why each step preserves the intended work. Then try the related real lab.</p><pre>'+esc(c.commands)+'</pre><a href="'+c.topic+'.html">Review the full lesson →</a></div>';
        return;
      }
      const q=c.steps[phase];
      $('#incident-step').innerHTML='<h3>'+esc(q.prompt)+'</h3><div class="decision-options">'+q.choices.map(([text],i)=>'<button class="decision-card" data-decision="'+i+'"'+(passed?' disabled':'')+'><span class="choice-letter">'+String.fromCharCode(65+i)+'</span><span>'+esc(text)+'</span></button>').join('')+'</div>';
      $$('[data-decision]',incident).forEach(b=>b.onclick=()=>{
        const index=Number(b.dataset.decision);passed=index===q.correct;
        feedback=q.choices[index][1];render();$('#incident-feedback').focus();
      });
    };
    const reset=()=>{phase=0;passed=false;feedback='Read the evidence before deciding.';render();};
    $('#incident-select').onchange=()=>{active=Number($('#incident-select').value);reset();};
    $('#incident-reset').onclick=reset;
    $('#incident-next').onclick=()=>{phase++;passed=false;feedback=phase===3?'You worked through every decision. Say the reasoning aloud once.':'';if(phase===3)complete(incidents[active].id);render();};
    reset();
  }
  const match=$('#match-studio');
  if(match) {
    let left=shuffle(pairs),right=shuffle(pairs),selected=null,matched=[],attempts=0,feedback='Choose an intention on the left, then its command on the right.';
    match.innerHTML='<div class="match-grid"><div><h3>What do you need?</h3><div id="match-tasks"></div></div><div><h3>Which command fits?</h3><div id="match-commands"></div></div><p id="match-feedback" class="studio-feedback" role="status" tabindex="-1"></p><p id="match-count" role="status"></p><button class="btn" id="match-reset">Shuffle and practise again</button>';
    const render=()=>{
      $('#match-tasks').innerHTML=left.map(p=>'<button class="match-card" data-task="'+p.id+'" aria-pressed="'+(selected===p.id)+'"'+(matched.includes(p.id)?' disabled':'')+'><span class="match-icon">'+(matched.includes(p.id)?'✓':'○')+'</span>'+esc(p.task)+'</button>').join('');
      $('#match-commands').innerHTML=right.map(p=>'<button class="match-card" data-command="'+p.id+'"'+(matched.includes(p.id)?' disabled':'')+'><span class="match-icon">'+(matched.includes(p.id)?'✓':'↔')+'</span><code>'+esc(p.command)+'</code></button>').join('');
      $('#match-feedback').textContent=feedback;$('#match-count').textContent=matched.length+' of 8 connected · '+attempts+' attempts';
      $$('[data-task]',match).forEach(b=>b.onclick=()=>{selected=b.dataset.task;feedback='Selected: '+pairs.find(p=>p.id===selected).task+'. Now choose its command.';render();$('[data-task="'+selected+'"]',match).focus();});
      $$('[data-command]',match).forEach(b=>b.onclick=()=>{
        if(!selected){feedback='Choose an intention first.';render();$('#match-feedback').focus();return;}
        attempts++;
        const p=pairs.find(p=>p.id===b.dataset.command);
        if(selected===p.id){matched.push(p.id);selected=null;feedback='Connected. '+p.why;if(matched.length===8){complete(15);feedback='All eight connected. '+attempts+' attempts. Say the effect before saying the command.';}}
        else feedback='That command serves another intention. '+p.why+' Keep your selected intention and try another command.';
        render();$('#match-feedback').focus();
      });
    };
    $('#match-reset').onclick=()=>{left=shuffle(pairs);right=shuffle(pairs);selected=null;matched=[];attempts=0;feedback='New arrangement. Match by meaning.';render();};
    render();
  }
  const recall=$('#recall-studio');
  if(recall) {
    let deck=[],index=0,answers={},started=false;
    recall.innerHTML='<div class="filters"><label class="field">Practice level<select id="recall-level"><option value="starter">Starter: files, commits, branches and merges</option><option value="all">All topics: include recovery and GitHub rules</option></select></label><button class="btn btn-primary" id="recall-start">Start five questions</button></div><p id="recall-status" class="meta" role="status"></p><div id="recall-card"></div><div id="recall-controls" class="actions"></div>';
    const pool=()=>root.GIT_DATA.questions.filter(q=>$('#recall-level').value==='all'||['foundations','daily-workflow','branches-remotes','merge'].includes(q.topic));
    const readiness=()=>{
      const results=L.recallResults(),missed=pool().filter(q=>results[q.id]===false).length;
      $('#recall-status').textContent=missed+' previously missed question'+(missed===1?'':'s')+' in this level will be prioritised. No countdown.';
    };
    const render=()=>{
      if(!started){readiness();return;}
      $('#recall-controls').innerHTML='';
      if(index>=deck.length) {
        const missed=deck.filter(q=>answers[q.id]!==q.correct),score=deck.length-missed.length;
        $('#recall-status').textContent='Round complete · '+score+' of '+deck.length+' correct on this pass.';
        $('#recall-card').innerHTML='<div class="round-summary"><span class="recall-ring">'+score+'/'+deck.length+'</span><div><h3>'+(missed.length?'Your next practice list':'Every answer correct this round')+'</h3><p>'+(missed.length?'Retry these now, then return another day to check recall.':'Explain one answer without looking, then verify it in a real lab.')+'</p></div></div>'+missed.map(q=>'<article class="recall-review"><b>'+esc(q.prompt)+'</b><p>'+esc(q.options[q.correct].text)+'</p><a href="'+q.topic+'.html">Revisit the explanation →</a></article>').join('');
        if(missed.length) {
          $('#recall-controls').innerHTML='<button class="btn btn-primary" id="recall-retry">Retry '+missed.length+' missed</button>';
          $('#recall-retry').onclick=()=>{deck=missed;answers={};index=0;render();};
        } else complete(16);
        return;
      }
      const q=deck[index],answered=Object.hasOwn(answers,q.id);
      $('#recall-status').textContent='Question '+(index+1)+' of '+deck.length+' · Predict first, then explain.';
      $('#recall-card').innerHTML='<form id="recall-form"><fieldset><legend>'+esc(q.prompt)+'</legend>'+q.options.map((o,i)=>'<label class="answer '+(answered&&i===q.correct?'correct':'')+'"><input type="radio" name="recall-choice" value="'+i+'"'+(answered?' disabled':'')+(answers[q.id]===i?' checked':'')+'><span>'+esc(o.text)+'</span></label>').join('')+'</fieldset>'+(!answered?'<button class="btn btn-primary">Check my answer</button>':'')+'<p id="recall-feedback" class="studio-feedback" role="status" tabindex="-1">'+(answered?(answers[q.id]===q.correct?'Correct. ':'Not yet. ')+esc(q.options[answers[q.id]].why)+(answers[q.id]!==q.correct?' Correct answer: '+esc(q.options[q.correct].text)+'. '+esc(q.options[q.correct].why):''):'')+'</p></form>';
      $('#recall-form').onsubmit=e=>{
        e.preventDefault();const input=$('input:checked',$('#recall-form'));
        if(!input){$('#recall-feedback').textContent='Choose an answer first.';return;}
        answers[q.id]=Number(input.value);L.recordRecall(q.id,answers[q.id]===q.correct);render();$('#recall-feedback').focus();
      };
      if(answered) {
        $('#recall-controls').innerHTML='<button class="btn" id="recall-next">'+(index===deck.length-1?'See my recap':'Next question →')+'</button>';
        $('#recall-next').onclick=()=>{index++;render();};
      }
    };
    $('#recall-start').onclick=()=>{deck=recallRound(pool(),L.recallResults());index=0;answers={};started=true;render();};
    $('#recall-level').onchange=()=>{started=false;$('#recall-card').innerHTML='';$('#recall-controls').innerHTML='';readiness();};
    render();
  }
  progress();
})(typeof window!=='undefined'?window:globalThis);
