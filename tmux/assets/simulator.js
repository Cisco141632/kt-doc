/* A bounded educational model, never a shell or a real tmux executor. */
(function (global) {
  'use strict';
  const leaves = node => node.id !== undefined ? [node.id] : leaves(node.a).concat(leaves(node.b));
  const replace = (node, id, replacement) => {
    if (node.id !== undefined) return node.id === id ? replacement : node;
    return {dir:node.dir, a:replace(node.a,id,replacement), b:replace(node.b,id,replacement)};
  };
  const remove = (node,id) => {
    if (node.id !== undefined) return node.id === id ? null : node;
    const a=remove(node.a,id), b=remove(node.b,id);
    return !a ? b : !b ? a : {dir:node.dir,a,b};
  };
  function tokenize(line) {
    let tokens=[], word='', quote=null, escaped=false, started=false;
    for (const char of line.trim()) {
      if (escaped) { word+=char; escaped=false; started=true; continue; }
      if (char === '\\' && quote !== "'") { escaped=true; started=true; continue; }
      if (quote) { if (char === quote) quote=null; else word+=char; started=true; continue; }
      if (char === '"' || char === "'") { quote=char; started=true; continue; }
      if (/\s/.test(char)) { if (started) tokens.push(word); word=''; started=false; continue; }
      if (';|&><'.includes(char)) throw new Error('Shell operators are outside this simulator. Enter one supported tmux command.');
      word+=char; started=true;
    }
    if (quote || escaped) throw new Error('Unclosed quote or trailing escape. Complete the command first.');
    if (started) tokens.push(word);
    return tokens;
  }
  class Model {
    constructor() { this.sessions=[]; this.attached=null; this.lastDetached=null; this.nextPane=0; this.events=new Set(); }
    session() {
      const s=this.sessions.find(s=>s.name===this.attached);
      if (!s) throw new Error('No client attached. Create a session or attach to an existing one first.');
      return s;
    }
    window() { const s=this.session(); return s.windows.find(w=>w.index===s.current); }
    validName(name) {
      if (!/^[a-zA-Z0-9_-]{1,32}$/.test(name)) throw new Error('This model uses names of 1–32 letters, digits, hyphens or underscores.');
    }
    create(name) {
      this.validName(name);
      if (this.sessions.some(s=>s.name===name)) throw new Error('duplicate session: ' + name + '. Attach or switch to it instead.');
      if (this.sessions.length>=6) throw new Error('This teaching model is limited to six sessions. Close a disposable session or reset the model.');
      const pane=this.nextPane++;
      this.sessions.push({name,current:0,last:null,windows:[{index:0,name:'shell',tree:{id:pane},active:pane,zoom:false}]});
      this.attached=name; this.events.add('created:'+name);
      return 'Created session '+name+' with window 0 and pane %'+pane+'. The client is attached.';
    }
    selectWindow(index) {
      const s=this.session(), w=s.windows.find(w=>w.index===index);
      if (!w) throw new Error('No window at index '+index+'. Use list-windows.');
      if (s.current!==index) { s.last=s.current; s.current=index; }
      this.events.add('window:'+w.name);
      return 'Current window: '+w.index+':'+w.name+'. Its active pane receives input.';
    }
    split(dir) {
      const w=this.window();
      if (leaves(w.tree).length>=8) throw new Error('This model limits each window to eight panes. Use a new window.');
      const id=this.nextPane++;
      w.tree=replace(w.tree,w.active,{dir,a:{id:w.active},b:{id}});
      w.active=id; w.zoom=false; this.events.add('split:'+dir);
      return 'Created pane %'+id+(dir==='h' ? ' beside' : ' below')+' the previous active pane. Focus moved to the new pane.';
    }
    focus(target) {
      const w=this.window(), ids=leaves(w.tree);
      const id=target.startsWith('%') ? Number(target.slice(1)) : ids[Number(target)];
      if (!/^%?\d+$/.test(target) || !ids.includes(id)) throw new Error('Pane not found in this window. Use its displayed index or %ID.');
      w.active=id; this.events.add('focus:'+ids.indexOf(id));
      return 'Active pane: '+ids.indexOf(id)+' (%'+id+'). Normal input goes here.';
    }
    closePane() {
      const s=this.session(), w=this.window(), id=w.active;
      const next=remove(w.tree,id);
      this.events.add('closed-pane');
      if (next) { w.tree=next; w.active=leaves(next)[0]; w.zoom=false; return 'Pane %'+id+' closed. Its simulated shell ended; remaining panes still exist.'; }
      s.windows=s.windows.filter(x=>x!==w);
      if (s.windows.length) { s.current=s.windows[0].index; s.last=null; return 'Last pane closed, so its window ended. Other windows remain.'; }
      this.sessions=this.sessions.filter(x=>x!==s); this.attached=null;
      return 'Last pane and window closed, so session '+s.name+' ended.'+(this.sessions.length ? ' Other sessions remain; attach to one.' : ' No sessions remain; the simulated server is stopped.');
    }
    layout(name) {
      const allowed=['tiled','even-horizontal','even-vertical','main-horizontal','main-vertical'];
      if (!allowed.includes(name)) throw new Error('Supported layouts: '+allowed.join(', ')+'.');
      const w=this.window(), ids=leaves(w.tree);
      function tree(items,dir,alternate) {
        if (items.length===1) return {id:items[0]};
        const mid=Math.ceil(items.length/2);
        return {dir,a:tree(items.slice(0,mid),alternate?(dir==='h'?'v':'h'):dir,alternate),b:tree(items.slice(mid),alternate?(dir==='h'?'v':'h'):dir,alternate)};
      }
      if (name.startsWith('main-') && ids.length>1) {
        const dir=name==='main-vertical'?'h':'v';
        w.tree={dir,a:{id:ids[0]},b:tree(ids.slice(1),dir==='h'?'v':'h',false)};
      } else w.tree=tree(ids,name==='even-vertical'?'v':'h',name==='tiled');
      w.zoom=false; w.layoutName=name; this.events.add('layout:'+name);
      return 'Applied '+name+' (schematic geometry). All existing pane IDs and simulated programs remain.';
    }
    run(line) {
      const tokens=tokenize(line);
      if (tokens[0]==='tmux') tokens.shift();
      if (!tokens.length) throw new Error('Enter a supported command, or type help.');
      const aliases={new:'new-session',ls:'list-sessions',attach:'attach-session',a:'attach-session',detach:'detach-client',neww:'new-window',splitw:'split-window',lsp:'list-panes',lsw:'list-windows',renamew:'rename-window',selectw:'select-window',selectp:'select-pane'};
      const input=tokens.shift(), cmd=aliases[input]||input;
      const specs={
        'new-session':{'-s':true},'list-sessions':{},'attach-session':{'-t':true},'switch-client':{'-t':true},'detach-client':{},
        'new-window':{'-n':true},'list-windows':{},'rename-window':{},'select-window':{'-t':true},'next-window':{},'previous-window':{},'last-window':{},
        'split-window':{'-h':false,'-v':false},'select-pane':{'-t':true},'list-panes':{},'resize-pane':{'-Z':false},'select-layout':{},'next-layout':{},
        'kill-pane':{},'kill-session':{'-t':true},'exit':{},'help':{}
      };
      if (!Object.hasOwn(specs,cmd)) throw new Error('Unsupported simulation command: '+cmd+'. Type help for the implemented subset; use the real-terminal labs for other commands.');
      const opts={}, args=[];
      while (tokens.length) {
        const t=tokens.shift();
        if (t.startsWith('-')) {
          if (!Object.hasOwn(specs[cmd],t) || Object.hasOwn(opts,t)) throw new Error('Unsupported or repeated flag '+t+' for '+cmd+'. Type help.');
          opts[t]=specs[cmd][t] ? tokens.shift() : true;
          if (opts[t]===undefined || typeof opts[t]==='string' && opts[t].startsWith('-')) throw new Error('Flag '+t+' needs a value.');
        } else args.push(t);
      }
      const namedArgument=['rename-window','select-layout'].includes(cmd);
      if (args.length !== (namedArgument?1:0)) throw new Error(cmd+(namedArgument?' requires one name.':' does not accept positional arguments in this model.'));
      const need = key => { if (!opts[key]) throw new Error(cmd+' needs '+key+' and a target.'); return opts[key]; };
      switch (cmd) {
        case 'help': return 'Model commands: new-session [-s name] (new); list-sessions (ls); attach-session -t name (attach/a); switch-client -t name; detach-client (detach); new-window [-n name] (neww); list-windows (lsw); rename-window name (renamew); select-window -t name-or-index (selectw); next-window; previous-window; last-window; split-window [-h|-v] (splitw); select-pane -t index-or-%ID (selectp); list-panes (lsp); resize-pane -Z; select-layout tiled/even-horizontal/even-vertical/main-horizontal/main-vertical; kill-pane; kill-session -t name; exit. Prefix buttons are also supported. Other flags and shell syntax are outside this model.';
        case 'new-session': {
          let n=0; while (this.sessions.some(s=>s.name===String(n))) n++;
          return this.create(opts['-s']||String(n));
        }
        case 'list-sessions':
          this.events.add('listed-sessions');
          return this.sessions.length ? this.sessions.map(s=>s.name+': '+s.windows.length+' windows'+(s.name===this.attached?' (attached)':' (detached)')).join('\n') : 'no server running in this model';
        case 'attach-session':
        case 'switch-client': {
          const target=need('-t').replace(/^=/,'');
          if (cmd==='switch-client') this.session();
          if (!this.sessions.some(s=>s.name===target)) throw new Error('Session not found: '+target+'. Check list-sessions.');
          this.attached=target; this.events.add('attached:'+target);
          if (this.events.has('detached:'+target)) this.events.add('returned:'+target);
          return 'Client now attached to '+target+'. Existing windows and panes were preserved.';
        }
        case 'detach-client': {
          const s=this.session(); this.events.add('detached:'+s.name); this.lastDetached=s.name; this.attached=null;
          return 'Detached from '+s.name+'. The session and its panes remain on the simulated server.';
        }
        case 'new-window': {
          const s=this.session();
          if (s.windows.length>=8) throw new Error('This model limits a session to eight windows.');
          const name=opts['-n']||'shell'; this.validName(name);
          let index=0; while (s.windows.some(w=>w.index===index)) index++;
          const id=this.nextPane++;
          s.windows.push({index,name,tree:{id},active:id,zoom:false});
          s.windows.sort((a,b)=>a.index-b.index);
          return this.selectWindow(index)+' Created one new shell pane.';
        }
        case 'list-windows': return this.session().windows.map(w=>w.index+':'+w.name+' ('+leaves(w.tree).length+' panes)'+(w.index===this.session().current?' *':'')).join('\n');
        case 'rename-window': { this.validName(args[0]); this.window().name=args[0]; return 'Renamed the current window to '+args[0]+'.'; }
        case 'select-window': {
          const target=need('-t'), s=this.session();
          const w=s.windows.find(w=>String(w.index)===target||w.name===target);
          if (!w) throw new Error('Window not found: '+target+'. Use list-windows.');
          return this.selectWindow(w.index);
        }
        case 'next-window':
        case 'previous-window': {
          const s=this.session(), i=s.windows.findIndex(w=>w.index===s.current);
          return this.selectWindow(s.windows[(i+(cmd==='next-window'?1:-1)+s.windows.length)%s.windows.length].index);
        }
        case 'last-window': {
          const s=this.session();
          if (s.last===null) throw new Error('No previous window yet. Select another window first.');
          return this.selectWindow(s.last);
        }
        case 'split-window':
          if (opts['-h']&&opts['-v']) throw new Error('Choose either -h or -v, not both.');
          return this.split(opts['-h']?'h':'v');
        case 'select-pane': return this.focus(need('-t'));
        case 'list-panes': {
          const w=this.window(); this.events.add('listed-panes');
          return leaves(w.tree).map((id,i)=>i+': %'+id+(id===w.active?' (active)':'')+' simulated shell').join('\n');
        }
        case 'resize-pane': {
          if (!opts['-Z']) throw new Error('Only resize-pane -Z is implemented. Use real labs to practise cell-by-cell resizing.');
          const w=this.window(); w.zoom=!w.zoom; this.events.add(w.zoom?'zoomed':'unzoomed');
          return w.zoom?'Zoomed the active pane. Other panes still exist.':'Restored the full pane layout.';
        }
        case 'select-layout': return this.layout(args[0]);
        case 'next-layout': {
          const names=['even-horizontal','even-vertical','main-horizontal','main-vertical','tiled'];
          return this.layout(names[(names.indexOf(this.window().layoutName)+1)%names.length]);
        }
        case 'kill-pane':
        case 'exit': return this.closePane();
        case 'kill-session': {
          const target=need('-t').replace(/^=/,'');
          if (!this.sessions.some(s=>s.name===target)) throw new Error('Session not found: '+target+'. Nothing was removed.');
          this.sessions=this.sessions.filter(s=>s.name!==target);
          if (this.attached===target) this.attached=null;
          this.events.add('killed:'+target);
          return 'Ended session '+target+' and its simulated programs. '+this.sessions.length+' other session(s) remain.';
        }
      }
    }
  }
  if (typeof module !== 'undefined' && module.exports) module.exports={Model,leaves,tokenize};
  if (!global.document) return;
  const root=document.getElementById('playground');
  if (!root) return;
  const esc=global.TmuxLearning.escape, $=s=>root.querySelector(s);
  const has=(m,name)=>m.sessions.some(s=>s.name===name);
  const event=(m,name)=>m.events.has(name);
  const missions=[
    {title:'01 · Leave and return', intro:'Create learn, detach from it, then attach again. Watch the difference between the client and server.',
      hint:'new-session -s learn → detach-client → attach-session -t learn',
      setup:()=>{}, checks:[
        ['Create a session named learn',m=>has(m,'learn')],
        ['Detach while learn still exists',m=>event(m,'detached:learn')],
        ['Reattach to the same session',m=>event(m,'returned:learn')&&m.attached==='learn']
      ]},
    {title:'02 · Organize your project',intro:'Start with an editor window. Create tests and logs windows, then select tests.',
      hint:'new-window -n tests → new-window -n logs → select-window -t tests',
      setup:m=>{m.create('project');m.window().name='editor';},
      checks:[
        ['Keep the original editor window',m=>m.sessions[0]?.windows.some(w=>w.name==='editor')],
        ['Create both tests and logs windows',m=>['tests','logs'].every(n=>m.sessions[0]?.windows.some(w=>w.name===n))],
        ['Return focus to tests',m=>m.attached==='project'&&m.window().name==='tests']
      ]},
    {title:'03 · Split, focus and zoom',intro:'Build three panes with both split directions, focus pane 0, zoom it, then restore the view.',
      hint:'split-window -h → split-window -v → select-pane -t 0 → resize-pane -Z twice',
      setup:m=>{m.create('project');},
      checks:[
        ['Use both split directions and keep three panes',m=>m.attached==='project'&&leaves(m.window().tree).length===3&&event(m,'split:h')&&event(m,'split:v')],
        ['Explicitly focus pane index 0',m=>event(m,'focus:0')],
        ['Zoom and then restore the layout',m=>event(m,'zoomed')&&event(m,'unzoomed')&&m.attached==='project'&&!m.window().zoom]
      ]},
    {title:'04 · Recover the hidden panes',intro:'Only one pane is visible. Diagnose before rebuilding: inspect panes, unzoom, apply tiled, and select pane 1.',
      hint:'list-panes → resize-pane -Z → select-layout tiled → select-pane -t 1',
      setup:m=>{m.create('incident');m.split('h');m.split('v');m.window().zoom=true;},
      checks:[
        ['Inspect the pane list',m=>event(m,'listed-panes')],
        ['Restore the view and choose tiled',m=>event(m,'unzoomed')&&event(m,'layout:tiled')],
        ['Keep all three panes and focus pane 1',m=>m.attached==='incident'&&leaves(m.window().tree).length===3&&leaves(m.window().tree).indexOf(m.window().active)===1&&event(m,'focus:1')]
      ]},
    {title:'05 · Switch project contexts',intro:'api and notes already exist. Switch to notes, add a research window, then return to api and list sessions.',
      hint:'switch-client -t notes → new-window -n research → switch-client -t api → list-sessions',
      setup:m=>{m.create('api');m.create('notes');m.attached='api';},
      checks:[
        ['Switch to notes using the existing client',m=>event(m,'attached:notes')],
        ['Create research inside notes',m=>m.sessions.find(s=>s.name==='notes')?.windows.some(w=>w.name==='research')],
        ['Return to api and inspect sessions',m=>m.attached==='api'&&event(m,'attached:api')&&event(m,'listed-sessions')]
      ]},
    {title:'06 · Clean up only the scratch work',intro:'keep has work to preserve. scratch has two panes. Close one scratch pane, detach, then end only scratch.',
      hint:'kill-pane → detach-client → kill-session -t scratch',
      setup:m=>{m.create('keep');m.create('scratch');m.split('h');},
      checks:[
        ['Close an individual scratch pane first',m=>event(m,'closed-pane')],
        ['Detach from scratch',m=>event(m,'detached:scratch')],
        ['End scratch and preserve keep',m=>!has(m,'scratch')&&has(m,'keep')&&event(m,'killed:scratch')]
      ]}
  ];
  let model, missionIndex=0, log=[], prefix=false;
  root.innerHTML='<div class="filters"><label class="field">Practice mode<select id="sim-mission">'+missions.map((m,i)=>'<option value="'+i+'">'+esc(m.title)+'</option>').join('')+'<option value="free">Free practice</option></select></label><button class="btn" id="sim-reset">Reset workspace</button></div><div class="mission" id="sim-goals"></div><div class="actions sim-controls"><button class="btn" data-command="tmux new-session -s learn">Create learn</button><button class="btn" data-command="tmux split-window -h">% Split beside</button><button class="btn" data-command="tmux split-window -v">&quot; Split below</button><button class="btn" id="sim-window">c New window</button><button class="btn" id="sim-focus">o Next pane</button><button class="btn" data-command="tmux resize-pane -Z">z Zoom</button><button class="btn" data-command="tmux select-layout tiled">Tiled layout</button><button class="btn" data-command="tmux detach-client">d Detach</button><button class="btn" id="sim-attach">Reattach</button><button class="btn" data-command="tmux list-sessions">List sessions</button></div><div class="terminal"><div class="terminal-head"><span>TMUX SIMULATOR · NO REAL COMMANDS RUN</span><span id="sim-connection"></span></div><div class="terminal-body" id="sim-screen"></div><div class="terminal-status" id="sim-status"></div><div class="terminal-log" id="sim-log" aria-label="Simulated command history"></div><label for="sim-input">Enter a supported command · type help for syntax</label><form id="sim-form"><input id="sim-input" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="tmux new-session -s learn"><button class="btn btn-primary" type="submit">Run</button></form></div><p id="sim-feedback" role="status"></p>';
  function paneHTML(node,w,ids) {
    if (node.id!==undefined) return '<button class="sim-pane '+(node.id===w.active?'is-active':'')+'" data-pane="'+node.id+'" aria-pressed="'+(node.id===w.active)+'"><b>pane '+ids.indexOf(node.id)+' · %'+node.id+(node.id===w.active?' · ACTIVE':'')+'</b><small>simulated shell<br>$ <span aria-hidden="true">▌</span></small></button>';
    return '<div class="sim-node '+(node.dir==='v'?'vertical':'')+'">'+paneHTML(node.a,w,ids)+paneHTML(node.b,w,ids)+'</div>';
  }
  function render() {
    if (model.attached) {
      const s=model.session(),w=model.window(),ids=leaves(w.tree);
      $('#sim-connection').textContent='client attached';
      $('#sim-screen').innerHTML='<div class="sim-node">'+paneHTML(w.zoom?{id:w.active}:w.tree,w,ids)+'</div>';
      $('#sim-status').innerHTML='<b>['+esc(s.name)+']</b>'+s.windows.map(x=>'<button data-window="'+x.index+'" aria-pressed="'+(x.index===s.current)+'">'+x.index+':'+esc(x.name)+(x.index===s.current?'*':'')+(x.zoom?' Z':'')+'</button>').join('');
    } else {
      $('#sim-connection').textContent='client detached';
      $('#sim-screen').innerHTML='<p>Outside the tmux client.</p><p>'+model.sessions.length+' session(s) remain on the simulated server.</p><p>'+(model.sessions.length?'Attach to an existing session to return to its workspace.':'Create a session to start the simulated server.')+'</p>';
      $('#sim-status').textContent='server: '+(model.sessions.length?'running · '+model.sessions.map(s=>s.name).join(', '):'stopped');
    }
    $('#sim-log').textContent=log.slice(-12).join('\n');
    $('#sim-log').scrollTop=$('#sim-log').scrollHeight;
    if (missionIndex==='free') $('#sim-goals').innerHTML='<h3>Free practice</h3><p>Create sessions, arrange panes and observe state. The model resets when you reload the page or choose a mission.</p>';
    else {
      const m=missions[missionIndex],checks=m.checks.map(([text,test])=>({text,done:!!test(model)})), complete=checks.every(c=>c.done);
      const previously=global.TmuxLearning.missionDone(missionIndex);
      if (complete) global.TmuxLearning.completeMission(missionIndex);
      $('#sim-goals').innerHTML='<h3>'+esc(m.title)+'</h3><p>'+esc(m.intro)+'</p><ol>'+checks.map(c=>'<li class="'+(c.done?'done':'')+'">'+(c.done?'✓ ':'○ ')+esc(c.text)+'</li>').join('')+'</ol><details><summary>Show a hint</summary><p>'+esc(m.hint)+'</p></details><p class="meta">'+(complete?'Mission complete. Choose another mission above.':previously?'Previously completed. This attempt starts fresh.':'Progress is checked against this simulated workspace.')+'</p>';
      if (complete&&!previously) $('#sim-feedback').textContent='Mission complete: '+m.title;
    }
  }
  function reset() {
    model=new Model(); prefix=false; log=[];
    if (missionIndex!=='free') missions[missionIndex].setup(model);
    model.events.clear();
    $('#sim-input').value='';
    $('#sim-feedback').textContent='Workspace reset. '+(missionIndex==='free'?'Free practice ready.':missions[missionIndex].intro);
    render();
  }
  function run(command) {
    log.push('$ '+command);
    try { const output=model.run(command);log.push(output);$('#sim-feedback').textContent=output; }
    catch(error) { log.push('Notice: '+error.message);$('#sim-feedback').textContent=error.message; }
    render();
  }
  $('#sim-form').addEventListener('submit',e=>{e.preventDefault();run($('#sim-input').value);$('#sim-input').value='';prefix=false;});
  root.addEventListener('click',e=>{
    const b=e.target.closest('button');if(!b)return;
    if(b.dataset.command)run(b.dataset.command);
    if(b.dataset.pane!==undefined)run('select-pane -t %'+b.dataset.pane);
    if(b.dataset.window!==undefined)run('select-window -t '+b.dataset.window);
  });
  $('#sim-mission').addEventListener('change',e=>{missionIndex=e.target.value==='free'?'free':Number(e.target.value);reset();});
  $('#sim-reset').addEventListener('click',reset);
  $('#sim-window').addEventListener('click',()=>run('new-window'));
  $('#sim-focus').addEventListener('click',()=>{
    try { const w=model.window(),ids=leaves(w.tree);run('select-pane -t '+((ids.indexOf(w.active)+1)%ids.length)); }
    catch(error){$('#sim-feedback').textContent=error.message;}
  });
  $('#sim-attach').addEventListener('click',()=>{
    if(!model.sessions.length){$('#sim-feedback').textContent='No session exists yet. Create one first.';return;}
    const recent=model.sessions.find(s=>s.name===model.lastDetached)||model.sessions[0];
    run('attach-session -t '+recent.name);
  });
  $('#sim-input').addEventListener('keydown',e=>{
    if(e.ctrlKey&&e.key.toLowerCase()==='b'){e.preventDefault();prefix=true;$('#sim-feedback').textContent='Prefix received. Release Ctrl+b, then press an action key.';return;}
    if(!prefix||['Control','Shift','Alt','Meta'].includes(e.key))return;
    e.preventDefault();prefix=false;
    const keymap={'%':'split-window -h','"':'split-window -v',c:'new-window',z:'resize-pane -Z',d:'detach-client',n:'next-window',p:'previous-window',l:'last-window',' ':'next-layout'};
    if(e.key==='o')$('#sim-focus').click();
    else if(Object.hasOwn(keymap,e.key))run(keymap[e.key]);
    else if(/^[0-9]$/.test(e.key))run('select-window -t '+e.key);
    else $('#sim-feedback').textContent='That prefix key is outside this model. Use a supported button or command.';
  });
  reset();
})(typeof window !== 'undefined' ? window : globalThis);
