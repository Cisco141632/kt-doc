const assert=require('node:assert/strict');
const {test}=require('node:test');
const S=require('../assets/studio.js');

test('beginner model distinguishes editing, recording and recovering with new history',()=>{
  const original=S.beginnerStart();
  const dirty=S.beginnerStep(original,'mistake');
  assert.equal(original.history.length,1);
  assert.equal(dirty.history.length,1);
  assert.notEqual(dirty.work,dirty.history[0].text);
  const mistake=S.beginnerStep(dirty,'save');
  assert.equal(mistake.history.length,2);
  const restored=S.beginnerStep(mistake,'restore');
  assert.equal(restored.work,original.work);
  assert.equal(restored.history.length,2);
  assert.equal(S.beginnerGoal(restored),false);
  const corrected=S.beginnerStep(restored,'save');
  assert.equal(corrected.history.length,3);
  assert.equal(corrected.history[1].text,dirty.work);
  assert.equal(S.beginnerGoal(corrected),true);
  assert.equal(S.beginnerStep(corrected,'save').history.length,3,'no empty snapshots');
});
test('staging captures a version; later edits do not sneak into a commit',()=>{
  let s=S.snapshotStart();
  for(const action of ['editA','stage','editB'])s=S.snapshotStep(s,action);
  assert.deepEqual([s.head,s.index,s.work],['base','A','B']);
  const committed=S.snapshotStep(s,'commit');
  assert.deepEqual([committed.head,committed.index,committed.work],['A','A','B']);
  assert.equal(S.snapshotGoal(committed,0,'commit'),true);
  assert.equal(S.snapshotStep(committed,'commit').commits,1);
});
test('unstage and restore change different layers and do not mutate previous state',()=>{
  const start=S.snapshotStart(1);
  const unstaged=S.snapshotStep(start,'unstage');
  assert.deepEqual([unstaged.head,unstaged.index,unstaged.work],['base','base','B']);
  assert.equal(S.snapshotGoal(unstaged,1,'unstage'),true);
  const restored=S.snapshotStep(S.snapshotStart(2),'restore');
  assert.deepEqual([restored.head,restored.index,restored.work],['base','A','A']);
  assert.equal(S.snapshotGoal(restored,2,'restore'),true);
  assert.equal(start.index,'A');
  assert.throws(()=>S.snapshotStep(start,'force'),/Unknown/);
});
test('all graph predictions have valid parents, distinct goals and honest target semantics',()=>{
  assert.equal(new Set(S.pointerChallenges.map(c=>c.id)).size,6);
  for(const c of S.pointerChallenges) {
    assert.ok(c.nodes.some(n=>n.id===c.start));
    assert.ok(c.nodes.some(n=>n.id===c.target));
    for(const n of c.nodes)for(const id of n.parents) {
      const parent=c.nodes.find(p=>p.id===id);
      assert.ok(parent && parent.x<n.x);
    }
  }
  assert.equal(S.pointerChallenges[1].nodes.find(n=>n.id==='M').parents.length,2);
  assert.deepEqual(S.pointerChallenges[2].nodes.find(n=>n.id==='C′').parents,['D']);
  assert.equal(S.pointerChallenges[5].start,S.pointerChallenges[5].target,'fetch does not move local main');
});
test('each incident has evidence, three decisions, and explanations for every choice',()=>{
  assert.equal(S.incidents.length,3);
  for(const c of S.incidents) {
    assert.equal(c.evidence.length,3);
    assert.equal(c.steps.length,3);
    for(const q of c.steps) {
      assert.ok(Number.isInteger(q.correct)&&q.correct>=0&&q.correct<q.choices.length);
      for(const [text,why] of q.choices)assert.ok(text.length>10&&why.length>30);
    }
  }
});
test('recall prioritises missed questions, then unseen, without duplicate or omitted candidates',()=>{
  const questions=Array.from({length:10},(_,i)=>({id:'q'+i}));
  const results={q0:true,q1:true,q7:false,q9:false};
  const round=S.recallRound(questions,results,()=>0.5);
  assert.deepEqual(new Set(round.slice(0,2).map(q=>q.id)),new Set(['q7','q9']));
  assert.equal(new Set(round.map(q=>q.id)).size,5);
  assert.ok(round.slice(2).every(q=>!Object.hasOwn(results,q.id)));
  assert.equal(S.recallRound(questions.slice(0,2),{},()=>0).length,2);
  assert.equal(S.pairs.length,8);
  assert.equal(new Set(S.pairs.map(p=>p.id)).size,8);
  assert.deepEqual(new Set(S.shuffle(questions,()=>0)),new Set(questions));
});
