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

  /* ---------- 4. Named-volume replacement walkthrough (storage-network.html) ---------- */

  function initVolumeLifecycle() {
    const el = document.getElementById('volume-life');
    if (!el) return;

    const STEPS = [
      {
        label: 'Start', title: 'Nothing has been created yet',
        command: '# no container and no volume',
        note: 'The image may exist, but there is no runtime data yet.',
        volume: 'none', first: 'none', second: 'none', active: 'volume', next: 'Create volume',
      },
      {
        label: 'Create', title: 'Create storage with its own lifecycle',
        command: '$ docker volume create db_data',
        note: 'Docker creates an empty named volume. It is not owned by any one container.',
        volume: 'empty', first: 'none', second: 'none', active: 'volume', next: 'Start v1',
      },
      {
        label: 'Write', title: 'Container v1 writes into the mounted volume',
        command: "$ docker run -d --name db-v1 -v db_data:/data alpine sh -c 'echo customer=42 > /data/db.txt; sleep 1d'",
        note: 'The path /data is a doorway into db_data. The file goes into the volume, not the container layer.',
        volume: 'data', first: 'running', second: 'none', active: 'first', next: 'Remove v1',
      },
      {
        label: 'Replace', title: 'Remove container v1',
        command: '$ docker rm -f db-v1',
        note: 'The container is gone. db_data is a separate Docker object, so customer=42 is still safe.',
        volume: 'data', first: 'removed', second: 'none', active: 'volume', next: 'Start v2',
      },
      {
        label: 'Reuse', title: 'Mount the same volume into container v2',
        command: '$ docker run -d --name db-v2 -v db_data:/data alpine sleep 1d',
        note: 'This is a fresh container with a fresh writable layer, but /data points to the existing volume.',
        volume: 'data', first: 'removed', second: 'running', active: 'second', next: 'Read data',
      },
      {
        label: 'Read', title: 'The new container reads the old data',
        command: '$ docker exec db-v2 cat /data/db.txt\ncustomer=42',
        note: 'Container v2 did not receive files from v1. Both containers mounted the same independent volume.',
        volume: 'data', first: 'removed', second: 'reading', active: 'second', next: 'Remove v2',
      },
      {
        label: 'Keep', title: 'Remove container v2 as well',
        command: '$ docker rm -f db-v2\n$ docker volume ls',
        note: 'No containers remain, but db_data and its file still exist. A future container can mount it again.',
        volume: 'data', first: 'removed', second: 'removed', active: 'volume', next: 'Delete volume',
      },
      {
        label: 'Delete', title: 'Delete the volume deliberately',
        command: '$ docker volume rm db_data',
        note: 'This removes the storage object and its data. A volume helps data survive containers; it is not a backup.',
        volume: 'removed', first: 'removed', second: 'removed', active: 'volume', next: 'Start again',
      },
    ];

    let current = 0;
    el.innerHTML = `
      <span class="widget-title">Step by step · named-volume lifecycle</span>
      <div class="storage-step-track" data-track></div>
      <div class="storage-stage">
        <div class="storage-object container-object" data-first>
          <span class="object-kicker">Disposable</span><b>Container v1</b><span data-first-state></span>
        </div>
        <span class="mount-link" aria-hidden="true">↔</span>
        <div class="storage-object volume-object" data-volume>
          <span class="object-kicker">Independent storage</span><b>Volume: db_data</b>
          <span class="volume-file" data-file></span>
        </div>
        <span class="mount-link" aria-hidden="true">↔</span>
        <div class="storage-object container-object" data-second>
          <span class="object-kicker">Replacement</span><b>Container v2</b><span data-second-state></span>
        </div>
      </div>
      <div class="storage-explain" aria-live="polite">
        <div><span class="badge info" data-count></span><h4 data-title></h4><p data-note></p></div>
        <pre class="mini-term" data-command></pre>
      </div>
      <div class="storage-controls">
        <button class="btn btn-small" type="button" data-back>← Back</button>
        <button class="btn btn-small btn-primary" type="button" data-next></button>
        <button class="btn btn-small" type="button" data-reset>Reset</button>
      </div>`;

    const track = el.querySelector('[data-track]');
    const trackButtons = STEPS.map((step, index) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.innerHTML = `<span>${index + 1}</span>${step.label}`;
      button.addEventListener('click', () => show(index));
      track.appendChild(button);
      return button;
    });
    const first = el.querySelector('[data-first]');
    const volume = el.querySelector('[data-volume]');
    const second = el.querySelector('[data-second]');
    const back = el.querySelector('[data-back]');
    const next = el.querySelector('[data-next]');
    const reset = el.querySelector('[data-reset]');

    function containerLabel(state) {
      if (state === 'running') return '● running and mounted';
      if (state === 'reading') return '● reading customer=42';
      if (state === 'removed') return '× removed';
      return 'not created';
    }

    function show(index) {
      current = Math.max(0, Math.min(index, STEPS.length - 1));
      const step = STEPS[current];
      trackButtons.forEach((button, i) => {
        button.classList.toggle('is-current', i === current);
        button.classList.toggle('is-past', i < current);
      });
      [first, volume, second].forEach((node) => node.classList.remove('is-active'));
      ({ first, volume, second })[step.active].classList.add('is-active');
      first.dataset.state = step.first;
      second.dataset.state = step.second;
      volume.dataset.state = step.volume;
      el.querySelector('[data-first-state]').textContent = containerLabel(step.first);
      el.querySelector('[data-second-state]').textContent = containerLabel(step.second);
      el.querySelector('[data-file]').textContent = step.volume === 'data' ? '▤ db.txt · customer=42' : step.volume === 'empty' ? 'empty' : step.volume === 'removed' ? '× data deleted' : 'not created';
      el.querySelector('[data-count]').textContent = `Step ${current + 1} of ${STEPS.length}`;
      el.querySelector('[data-title]').textContent = step.title;
      el.querySelector('[data-note]').textContent = step.note;
      el.querySelector('[data-command]').textContent = step.command;
      back.disabled = current === 0;
      next.textContent = current === STEPS.length - 1 ? '↻ Start again' : `${step.next} →`;
      reset.hidden = current === 0;
    }

    back.addEventListener('click', () => show(current - 1));
    next.addEventListener('click', () => show(current === STEPS.length - 1 ? 0 : current + 1));
    reset.addEventListener('click', () => show(0));
    show(0);
  }

  /* ---------- 5. Bind-mount mirror (storage-network.html) ---------- */

  function initBindMirror() {
    const el = document.getElementById('bind-mirror');
    if (!el) return;
    const initial = () => ({ version: 1, readOnly: true, container: true, log: [] });
    let state = initial();

    el.innerHTML = `
      <span class="widget-title">Try it · bind-mount mirror</span>
      <div class="widget-row" data-mode></div>
      <div class="mount-mirror">
        <div class="mirror-side host-side">
          <span class="object-kicker">Your machine</span><b>./site/index.html</b>
          <span class="file-preview" data-host-file></span>
        </div>
        <div class="mirror-bridge"><span data-arrow>→</span><b data-mount-label></b><small>same file, two paths</small></div>
        <div class="mirror-side container-side" data-container-side>
          <span class="object-kicker">nginx container</span><b>/usr/share/nginx/html/index.html</b>
          <span class="file-preview" data-container-file></span>
        </div>
      </div>
      <div class="widget-row" data-actions></div>
      <pre class="mini-term" data-log aria-live="polite"></pre>
      <p class="widget-note">Suggested order: edit on the host → try a container write in read-only mode → switch to read-write → remove and recreate the container.</p>`;

    const modeBox = el.querySelector('[data-mode]');
    const actions = el.querySelector('[data-actions]');

    function actionButton(label, run, disabled) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'btn btn-small';
      button.textContent = label;
      button.disabled = disabled;
      button.addEventListener('click', () => { run(); render(); });
      actions.appendChild(button);
    }

    function render() {
      modeBox.innerHTML = '<span class="label">Mount mode:</span>';
      [['Read-only :ro', true], ['Read-write', false]].forEach(([label, value]) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = `btn btn-small${state.readOnly === value ? ' is-on' : ''}`;
        button.textContent = label;
        button.addEventListener('click', () => {
          state.readOnly = value;
          state.log.push(value ? '$ remount with :ro\n  → container writes are blocked' : '$ remount without :ro\n  → both sides may write');
          render();
        });
        modeBox.appendChild(button);
      });

      el.querySelector('[data-host-file]').textContent = `<h1>File version ${state.version}</h1>`;
      el.querySelector('[data-container-file]').textContent = state.container ? `<h1>File version ${state.version}</h1>` : 'container removed';
      el.querySelector('[data-container-side]').classList.toggle('is-removed', !state.container);
      el.querySelector('[data-arrow]').textContent = state.readOnly ? '→' : '↔';
      el.querySelector('[data-mount-label]').textContent = state.readOnly ? 'bind mount · :ro' : 'bind mount · read-write';

      actions.innerHTML = '';
      actionButton('1. Edit host file', () => {
        state.version += 1;
        state.log.push(`$ edit ./site/index.html\n  → container immediately sees Host edit ${state.version}; no rebuild`);
      }, false);
      actionButton('2. Write from container', () => {
        if (state.readOnly) state.log.push('$ echo change > /usr/share/nginx/html/index.html\n  → Read-only file system; host file protected');
        else {
          state.version += 1;
          state.log.push(`$ echo change > /usr/share/nginx/html/index.html\n  → host file changed too (version ${state.version})`);
        }
      }, !state.container);
      actionButton('3. Remove container', () => {
        state.container = false;
        state.log.push('$ docker rm -f site\n  → container gone; ./site/index.html remains on the host');
      }, !state.container);
      actionButton('4. Start fresh container', () => {
        state.container = true;
        state.log.push(`$ docker run … -v "$(pwd)/site:/usr/share/nginx/html${state.readOnly ? ':ro' : ''}" nginx:alpine\n  → fresh container sees Host edit ${state.version}`);
      }, state.container);
      actionButton('Reset', () => { state = initial(); }, false);
      el.querySelector('[data-log]').textContent = state.log.length ? state.log.slice(-8).join('\n') : '$ docker run -v "$(pwd)/site:/usr/share/nginx/html:ro" nginx:alpine\n  → both paths point to the same host file';
    }

    render();
  }

  /* ---------- 6. Network request-path tracer (storage-network.html) ---------- */

  function initNetworkPath() {
    const el = document.getElementById('network-path');
    if (!el) return;

    const ROUTES = {
      browser: {
        label: 'Browser → web', result: 'success',
        nodes: [
          ['Source', 'Browser on host'],
          ['Address used', 'localhost:8080'],
          ['Docker route', '-p 8080:80'],
          ['Destination', 'web container :80'],
        ],
        notes: [
          'The request begins outside Docker, in a program on your machine.',
          'The browser connects to the host port: the left side of the mapping.',
          'Docker forwards host port 8080 to port 80 in the container.',
          'nginx receives the request on its real listening port, 80.',
        ],
        command: 'docker run -d --name web -p 8080:80 nginx:alpine',
      },
      containers: {
        label: 'api → db', result: 'success',
        nodes: [
          ['Source', 'api container'],
          ['Address used', 'db:5432'],
          ['Docker route', 'DNS + labnet'],
          ['Destination', 'db container :5432'],
        ],
        notes: [
          'The request begins inside the api container.',
          'api uses the destination container name and its internal port.',
          'Docker DNS resolves db, then the private network carries the packet. No -p is needed.',
          'Postgres receives the connection on port 5432.',
        ],
        command: 'DATABASE_URL=postgres://user:pass@db:5432/app',
      },
      host: {
        label: 'container → host', result: 'success',
        nodes: [
          ['Source', 'api container'],
          ['Address used', 'host.docker.internal:9000'],
          ['Docker route', 'host gateway'],
          ['Destination', 'host process :9000'],
        ],
        notes: [
          'The request begins inside a container, but the target runs directly on your machine.',
          'localhost would point back to api. The special hostname identifies the host.',
          'Docker routes the request out through the host gateway.',
          'The program listening on port 9000 of the host receives it. On Linux Engine, add the host-gateway mapping.',
        ],
        command: 'docker run --add-host=host.docker.internal:host-gateway my-api:1.0',
      },
      trap: {
        label: 'localhost trap', result: 'failure',
        nodes: [
          ['Source', 'api container'],
          ['Wrong address', 'localhost:5432'],
          ['Actual route', 'back to api itself'],
          ['Result', 'connection refused'],
        ],
        notes: [
          'The application begins inside api and wants to reach db.',
          'Inside api, localhost always means api itself.',
          'The packet never enters the Docker network and never reaches db.',
          'Fix the address to db:5432 and put both containers on the same user-defined network.',
        ],
        command: 'wrong: localhost:5432\nright: db:5432',
      },
    };

    let routeKey = 'browser';
    let hop = 0;
    el.innerHTML = `
      <span class="widget-title">Try it · trace a network request</span>
      <div class="route-tabs" data-routes></div>
      <div class="route-map" data-map></div>
      <div class="route-explain" aria-live="polite"><b data-hop-title></b><p data-hop-note></p></div>
      <pre class="mini-term" data-route-command></pre>
      <div class="route-controls">
        <button class="btn btn-small" type="button" data-route-back>← Previous hop</button>
        <button class="btn btn-small btn-primary" type="button" data-route-next>Next hop →</button>
        <span data-hop-count></span>
      </div>`;

    const tabs = el.querySelector('[data-routes]');
    Object.keys(ROUTES).forEach((key) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'btn btn-small';
      button.textContent = ROUTES[key].label;
      button.dataset.route = key;
      button.addEventListener('click', () => { routeKey = key; hop = 0; render(); });
      tabs.appendChild(button);
    });

    const back = el.querySelector('[data-route-back]');
    const next = el.querySelector('[data-route-next]');

    function render() {
      const route = ROUTES[routeKey];
      tabs.querySelectorAll('button').forEach((button) => button.classList.toggle('is-on', button.dataset.route === routeKey));
      el.querySelector('[data-map]').innerHTML = route.nodes.map((node, index) => `
        ${index ? '<span class="route-arrow" aria-hidden="true">→</span>' : ''}
        <div class="route-node${index < hop ? ' is-past' : ''}${index === hop ? ' is-current' : ''}${index === route.nodes.length - 1 && hop === index ? ` is-${route.result}` : ''}">
          <small>${node[0]}</small><b>${node[1]}</b>
        </div>`).join('');
      el.querySelector('[data-hop-title]').textContent = route.nodes[hop][0];
      el.querySelector('[data-hop-note]').textContent = route.notes[hop];
      el.querySelector('[data-route-command]').textContent = route.command;
      el.querySelector('[data-hop-count]').textContent = `Hop ${hop + 1} of ${route.nodes.length}`;
      back.disabled = hop === 0;
      next.disabled = hop === route.nodes.length - 1;
      next.textContent = hop === route.nodes.length - 2 ? 'Show result →' : 'Next hop →';
    }

    back.addEventListener('click', () => { if (hop > 0) { hop -= 1; render(); } });
    next.addEventListener('click', () => { if (hop < ROUTES[routeKey].nodes.length - 1) { hop += 1; render(); } });
    render();
  }

  /* ---------- 7. Code, image, container: what actually changes (rebuild.html) ---------- */

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
    initVolumeLifecycle();
    initBindMirror();
    initNetworkPath();
    initRebuildSim();
  });
})();
