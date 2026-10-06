/* Docker learning path — the interactive diagrams.
   Each one starts itself only if its container element is on the page. */
(function () {
  'use strict';

  /* ---------- 1. Container lifecycle playground (commands.html) ---------- */

  function initLifecycle() {
    const el = document.getElementById('lifecycle');
    if (!el) return;

    const STATES = {
      none: { label: 'No container', note: 'nothing exists yet', ps: 'no', psa: 'no', files: 'nothing to keep' },
      created: { label: 'Created', note: 'exists, not started', ps: 'no', psa: 'yes', files: 'kept' },
      running: { label: 'Running', note: 'app is working', ps: 'yes', psa: 'yes', files: 'kept' },
      paused: { label: 'Paused', note: 'frozen in memory', ps: 'yes (Paused)', psa: 'yes', files: 'kept' },
      exited: { label: 'Exited', note: 'stopped, still on disk', ps: 'no', psa: 'yes', files: 'kept' },
    };
    const ACTIONS = {
      none: [
        { cmd: 'docker run -d --name web nginx:alpine', to: 'running', say: 'Created a new container and started it in one step.' },
        { cmd: 'docker create --name web nginx:alpine', to: 'created', say: 'Created the container but did not start it.' },
      ],
      created: [
        { cmd: 'docker start web', to: 'running', say: 'Started the container.' },
        { cmd: 'docker rm web', to: 'none', say: 'Removed the container. Its files are gone.' },
      ],
      running: [
        { cmd: 'docker stop web', to: 'exited', say: 'Asked the app to shut down. The container still exists.' },
        { cmd: 'docker pause web', to: 'paused', say: 'Froze every process in the container.' },
        { cmd: 'docker restart web', to: 'running', say: 'Stopped and started again. Same container, same files.' },
        { cmd: 'docker rm -f web', to: 'none', say: 'Force-removed a running container. Its files are gone.' },
      ],
      paused: [
        { cmd: 'docker unpause web', to: 'running', say: 'Continued exactly where it was frozen.' },
      ],
      exited: [
        { cmd: 'docker start web', to: 'running', say: 'Started the same container again. Files written before are still there.' },
        { cmd: 'docker rm web', to: 'none', say: 'Removed the container. Its files are gone.' },
      ],
    };

    let state = 'none';
    const log = [];

    el.innerHTML = `
      <span class="widget-title">Try it · container lifecycle</span>
      <div class="states"></div>
      <div class="widget-row"><span class="label">Commands you can run now:</span><span data-actions class="widget-row" style="margin:0"></span></div>
      <div class="facts"></div>
      <pre class="mini-term" aria-live="polite"></pre>`;
    const statesBox = el.querySelector('.states');
    const actionsBox = el.querySelector('[data-actions]');
    const factsBox = el.querySelector('.facts');
    const term = el.querySelector('.mini-term');

    function render() {
      statesBox.innerHTML = Object.keys(STATES).map((key) =>
        `<div class="state${key === state ? ' is-current' : ''}">${STATES[key].label}<small>${STATES[key].note}</small></div>`).join('');
      const s = STATES[state];
      factsBox.innerHTML = `
        <div><b>Shown by docker ps?</b>${s.ps}</div>
        <div><b>Shown by docker ps -a?</b>${s.psa}</div>
        <div><b>Files inside the container</b>${s.files}</div>`;
      actionsBox.innerHTML = '';
      ACTIONS[state].forEach((action) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'btn btn-small';
        button.textContent = action.cmd.split(' ').slice(0, action.cmd.includes(' -f ') ? 3 : 2).join(' ');
        button.title = action.cmd;
        button.addEventListener('click', () => {
          log.push(`$ ${action.cmd}`, `  → ${action.say}`);
          state = action.to;
          render();
        });
        actionsBox.appendChild(button);
      });
      term.textContent = log.length ? log.slice(-8).join('\n') : 'Click a command above to see what happens.';
      term.scrollTop = term.scrollHeight;
    }
    render();
  }

  /* ---------- 2. Build cache simulator (dockerfile.html) ---------- */

  function initCacheSim() {
    const el = document.getElementById('cache-sim');
    if (!el) return;

    // "watches" says which of your edits makes this line's input different from last time.
    const ORDERS = {
      good: {
        label: 'Dependencies first (recommended)',
        layers: [
          { line: 'FROM python:3.13-slim', secs: 0, watches: [] },
          { line: 'WORKDIR /app', secs: 0, watches: [] },
          { line: 'COPY requirements.txt .', secs: 1, watches: ['deps'] },
          { line: 'RUN pip install -r requirements.txt', secs: 30, watches: [] },
          { line: 'COPY . .', secs: 1, watches: ['deps', 'code'] },
          { line: 'CMD ["gunicorn", "app:app"]', secs: 0, watches: [] },
        ],
      },
      bad: {
        label: 'Copy everything first (slow)',
        layers: [
          { line: 'FROM python:3.13-slim', secs: 0, watches: [] },
          { line: 'WORKDIR /app', secs: 0, watches: [] },
          { line: 'COPY . .', secs: 1, watches: ['deps', 'code'] },
          { line: 'RUN pip install -r requirements.txt', secs: 30, watches: [] },
          { line: 'CMD ["gunicorn", "app:app"]', secs: 0, watches: [] },
        ],
      },
    };
    const CHANGES = { none: 'Nothing', code: 'app.py (my code)', deps: 'requirements.txt (a dependency)' };

    let order = 'good';
    let change = 'code';

    el.innerHTML = `
      <span class="widget-title">Try it · which layers are rebuilt?</span>
      <div class="widget-row"><span class="label">Dockerfile order:</span><span data-order class="widget-row" style="margin:0"></span></div>
      <div class="widget-row"><span class="label">What did you change since the last build?</span><span data-change class="widget-row" style="margin:0"></span></div>
      <div class="layers"></div>
      <p class="result-line" aria-live="polite"></p>
      <p class="widget-note">Times are only an illustration (30 seconds for installing dependencies). The rule is real: the first changed layer and every layer below it are rebuilt.</p>`;
    const orderBox = el.querySelector('[data-order]');
    const changeBox = el.querySelector('[data-change]');
    const layersBox = el.querySelector('.layers');
    const result = el.querySelector('.result-line');

    function buttons(box, options, current, onPick) {
      box.innerHTML = '';
      Object.keys(options).forEach((key) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'btn btn-small' + (key === current ? ' is-on' : '');
        button.textContent = options[key].label || options[key];
        button.addEventListener('click', () => onPick(key));
        box.appendChild(button);
      });
    }

    function render() {
      buttons(orderBox, ORDERS, order, (key) => { order = key; render(); });
      buttons(changeBox, CHANGES, change, (key) => { change = key; render(); });
      let broken = false;
      let total = 0;
      layersBox.innerHTML = ORDERS[order].layers.map((layer) => {
        if (layer.watches.includes(change)) broken = true;
        if (broken) total += layer.secs;
        return `<div class="layer-row ${broken ? 'is-rebuilt' : 'is-cached'}">
          <code>${window.DockerKT.esc(layer.line)}</code>
          <span class="badge ${broken ? 'warn' : 'ok'}">${broken ? 'REBUILT' : 'CACHED'}</span>
        </div>`;
      }).join('');
      result.textContent = total === 0
        ? 'Build time: about 0 seconds. Everything comes from the cache.'
        : `Build time: about ${total} second${total === 1 ? '' : 's'}.` + (order === 'bad' && change === 'code' ? ' You changed one line of code and waited for every dependency to install again.' : '');
    }
    render();
  }

  /* ---------- 3. Port mapping (storage-network.html) ---------- */

  function initPortMap() {
    const el = document.getElementById('portmap');
    if (!el) return;
    el.innerHTML = `
      <span class="widget-title">Try it · read a port mapping</span>
      <div class="widget-row">
        <label for="pm-host">Host port</label><input id="pm-host" type="number" min="1" max="65535" value="8080">
        <label for="pm-cont">Container port</label><input id="pm-cont" type="number" min="1" max="65535" value="80">
      </div>
      <div class="portmap">
        <div class="box">Your browser<b data-url></b></div>
        <span class="arrow" aria-hidden="true">→</span>
        <div class="box">Your machine (host)<b data-host></b></div>
        <span class="arrow" aria-hidden="true">→</span>
        <div class="box">Container<b data-cont></b></div>
      </div>
      <pre class="mini-term" data-cmd></pre>
      <p class="widget-note" data-note aria-live="polite"></p>`;
    const host = el.querySelector('#pm-host');
    const cont = el.querySelector('#pm-cont');

    function render() {
      const h = host.value || '?';
      const c = cont.value || '?';
      el.querySelector('[data-url]').textContent = `localhost:${h}`;
      el.querySelector('[data-host]').textContent = `port ${h}`;
      el.querySelector('[data-cont]').textContent = `port ${c}`;
      el.querySelector('[data-cmd]').textContent = `docker run -d -p ${h}:${c} nginx:alpine`;
      el.querySelector('[data-note]').textContent = c === '80'
        ? `The left number (${h}) is what you type in the browser. The right number (${c}) is where nginx listens inside the container.`
        : `nginx listens on port 80 inside the container. With container port ${c} the traffic arrives at a port where nothing is listening, so the page will not load. The right number must match the app.`;
    }
    host.addEventListener('input', render);
    cont.addEventListener('input', render);
    render();
  }

  /* ---------- 4. Code, image, container: what actually changes (rebuild.html) ---------- */

  function initRebuildSim() {
    const el = document.getElementById('rebuild-sim');
    if (!el) return;

    const start = () => ({ code: 1, image: 1, container: 1, old: 0, log: [] });
    let s = start();

    el.innerHTML = `
      <span class="widget-title">Try it · what actually changes?</span>
      <div class="portmap" data-boxes></div>
      <div class="widget-row" data-buttons></div>
      <pre class="mini-term" aria-live="polite"></pre>
      <p class="widget-note">Press "Edit the code" first, then try the other buttons in any order and watch which box changes.</p>`;
    const boxes = el.querySelector('[data-boxes]');
    const buttons = el.querySelector('[data-buttons]');
    const term = el.querySelector('.mini-term');

    const ACTIONS = [
      { label: 'Edit the code', run() {
        s.code += 1;
        return [`(you save app.py: version ${s.code})`, 'Only the file on your machine changed. The image and the container are untouched.'];
      } },
      { label: 'docker build', run() {
        if (s.image === s.code) return ['$ docker build -t hello-docker:1.0 .', 'Nothing changed since the last build. Every step is CACHED and the image is exactly the same one.'];
        s.old += 1;
        s.image = s.code;
        return ['$ docker build -t hello-docker:1.0 .', `New image, built from version ${s.image}. The name hello-docker:1.0 now points to it. The old image stays on disk without a name. The running container was not touched.`];
      } },
      { label: 'docker restart', run() {
        return ['$ docker restart hello', `The same container, started again. It still uses the image it was created from (version ${s.container}).`];
      } },
      { label: 'docker rm -f + docker run', run() {
        const same = s.container === s.image;
        s.container = s.image;
        return ['$ docker rm -f hello && docker run -d --name hello hello-docker:1.0', same
          ? 'A new container, but from the same image as before, so the app looks the same.'
          : `A new container, created from the current image. The app now shows version ${s.container}.`];
      } },
      { label: 'Start over', run() { s = start(); return null; } },
    ];

    function box(title, text, fresh) {
      return `<div class="box ${fresh ? 'is-fresh' : 'is-stale'}">${title}<b>${text}</b><span class="badge ${fresh ? 'ok' : 'warn'}">${fresh ? 'up to date' : 'outdated'}</span></div>`;
    }

    function render() {
      boxes.innerHTML =
        box('Your code (app.py)', `version ${s.code}`, true) +
        '<span class="arrow" aria-hidden="true">→</span>' +
        box('Image hello-docker:1.0', `built from version ${s.image}`, s.image === s.code) +
        '<span class="arrow" aria-hidden="true">→</span>' +
        box('Container hello', `running version ${s.container}`, s.container === s.code);
      term.textContent = (s.log.length ? s.log.slice(-6).join('\n') : 'Everything is in sync: code, image and container are all version 1.')
        + (s.old ? `\n\nOld images without a name on disk: ${s.old}` : '');
      term.scrollTop = term.scrollHeight;
    }

    ACTIONS.forEach((action) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'btn btn-small';
      button.textContent = action.label;
      button.addEventListener('click', () => {
        const lines = action.run();
        if (lines) s.log.push(lines[0], '  → ' + lines[1]);
        render();
      });
      buttons.appendChild(button);
    });
    render();
  }

  document.addEventListener('DOMContentLoaded', () => {
    initLifecycle();
    initCacheSim();
    initPortMap();
    initRebuildSim();
  });
})();
