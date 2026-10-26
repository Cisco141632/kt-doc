const {test}=require('node:test');
const assert=require('node:assert/strict');
const {Model,leaves,tokenize}=require('../assets/simulator.js');

test('detach preserves pane identity and reattach returns to it',()=>{
  const m=new Model();
  m.run('tmux new -s learn');
  const pane=m.window().active;
  m.run('detach');
  assert.equal(m.attached,null);
  assert.equal(m.sessions.length,1);
  m.run('attach -t learn');
  assert.equal(m.window().active,pane);
  assert.ok(m.events.has('returned:learn'));
});
test('nested split preserves original pane and zoom is view-only',()=>{
  const m=new Model();m.create('work');
  const first=m.window().active;
  m.run('split-window -h');m.run('split-window -v');
  assert.deepEqual(leaves(m.window().tree),[0,1,2]);
  assert.equal(m.window().tree.dir,'h');
  assert.equal(m.window().tree.b.dir,'v');
  m.run('select-pane -t %'+first);m.run('resize-pane -Z');
  assert.equal(m.window().zoom,true);
  assert.equal(leaves(m.window().tree).length,3);
  m.run('resize-pane -Z');assert.equal(m.window().zoom,false);
});
test('windows retain panes through selection and last-window navigation',()=>{
  const m=new Model();m.create('work');
  const first=m.window().active;
  m.run('new-window -n tests');const tests=m.window().active;
  m.run('new-window -n logs');
  m.run('select-window -t tests');assert.equal(m.window().active,tests);
  m.run('last-window');assert.equal(m.window().name,'logs');
  m.run('select-window -t 0');assert.equal(m.window().active,first);
});
test('closing last pane cascades only through its own window and session',()=>{
  const m=new Model();m.create('keep');m.create('scratch');
  m.run('split-window -h');m.run('kill-pane');
  assert.equal(leaves(m.window().tree).length,1);
  m.run('exit');
  assert.equal(m.attached,null);
  assert.deepEqual(m.sessions.map(s=>s.name),['keep']);
});
test('targeted cleanup after detach preserves other sessions',()=>{
  const m=new Model();m.create('keep');m.create('scratch');
  m.run('detach-client');m.run("kill-session -t '=scratch'");
  assert.deepEqual(m.sessions.map(s=>s.name),['keep']);
  assert.throws(()=>m.run('kill-session'),/needs -t/);
  assert.equal(m.sessions.length,1);
});
test('layouts retain every pane ID and active pane',()=>{
  const m=new Model();m.create('work');
  for(let i=0;i<4;i++)m.run('split-window -h');
  const ids=leaves(m.window().tree), active=m.window().active;
  for(const layout of ['tiled','even-horizontal','even-vertical','main-vertical','main-horizontal']){
    m.run('select-layout '+layout);
    assert.deepEqual(leaves(m.window().tree),ids);
    assert.equal(m.window().active,active);
  }
});
test('layout cycling changes geometry without losing panes and remembers detach context',()=>{
  const m=new Model();m.create('first');m.create('second');
  m.run('split-window -h');
  const ids=leaves(m.window().tree);
  m.run('select-layout even-horizontal');m.run('next-layout');
  assert.equal(m.window().layoutName,'even-vertical');
  assert.deepEqual(leaves(m.window().tree),ids);
  m.run('detach-client');
  assert.equal(m.lastDetached,'second');
});
test('unsupported commands and malformed flags cannot mutate state',()=>{
  const m=new Model();m.create('work');
  const snapshot=JSON.stringify(m.sessions);
  for(const command of ['split-window -h -v','split-window -x','new-session -s','select-pane -t 9','new-window -n -h','kill-session -t absent','new-window extra','tmux new-session -s work','tmux send-keys -t %0 text','tmux ls; rm -rf /']){
    assert.throws(()=>m.run(command),command);
    assert.equal(JSON.stringify(m.sessions),snapshot,command);
  }
});
test('tokenizer understands quotes and refuses incomplete commands',()=>{
  assert.deepEqual(tokenize("tmux new -s 'learn'"),['tmux','new','-s','learn']);
  assert.throws(()=>tokenize("tmux new -s 'learn"),/Unclosed quote/);
  assert.throws(()=>tokenize('ls | cat'),/Shell operators/);
});
