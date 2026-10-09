/* Prediction-first simulations for common-doubts.html. */
(function () {
  'use strict';

  function choiceButtons(box, options, current, onPick) {
    box.innerHTML = '';
    options.forEach((option) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = `btn btn-small${option.value === current ? ' is-on' : ''}`;
      button.textContent = option.label;
      button.addEventListener('click', () => onPick(option.value));
      box.appendChild(button);
    });
  }

  /* ---------- Listening address and published-port simulator ---------- */

  function initListenLab() {
    const el = document.getElementById('listen-lab');
    if (!el) return;
    const state = { bind: 'loopback', publish: 'local', client: 'host' };

    const BINDS = [
      { value: 'loopback', label: '127.0.0.1:8000' },
      { value: 'all', label: '0.0.0.0:8000' },
    ];
    const PUBLISH = [
      { value: 'none', label: 'No -p' },
      { value: 'all', label: '-p 8080:8000' },
      { value: 'local', label: '-p 127.0.0.1:8080:8000' },
    ];
    const CLIENTS = [
      { value: 'same', label: 'Inside same container' },
      { value: 'host', label: 'Browser on host' },
      { value: 'remote', label: 'Another computer' },
    ];

    el.innerHTML = `
      <span class="widget-title">Predict, then test · will the request connect?</span>
      <div class="doubt-controls">
        <div><b>1. Application listens on</b><span data-bind-buttons></span></div>
        <div><b>2. Container starts with</b><span data-publish-buttons></span></div>
        <div><b>3. Request comes from</b><span data-client-buttons></span></div>
      </div>
      <div class="connection-route">
        <div class="connection-node" data-source><small>Request source</small><b data-source-text></b></div>
        <span aria-hidden="true">→</span>
        <div class="connection-node" data-host><small>Host publishing</small><b data-host-text></b></div>
        <span aria-hidden="true">→</span>
        <div class="connection-node" data-interface><small>Container network</small><b>port 8000</b></div>
        <span aria-hidden="true">→</span>
        <div class="connection-node" data-app><small>Application</small><b data-app-text></b></div>
      </div>
      <div class="prediction-box">
        <span>Make your prediction:</span>
        <button class="btn btn-small" type="button" data-predict="works">It works</button>
        <button class="btn btn-small" type="button" data-predict="fails">It fails</button>
        <b data-prediction></b>
      </div>
      <div class="connection-result" data-result aria-live="polite">
        <b data-result-title>Choose your prediction</b><p data-result-note>The answer stays hidden until you predict.</p>
      </div>`;

    const bindBox = el.querySelector('[data-bind-buttons]');
    const publishBox = el.querySelector('[data-publish-buttons]');
    const clientBox = el.querySelector('[data-client-buttons]');

    function outcome() {
      if (state.client === 'same') {
        return {
          works: true,
          note: `A program inside the same container can connect to ${state.bind === 'loopback' ? '127.0.0.1' : 'the container address'}. Port publishing is not involved.`,
        };
      }
      if (state.publish === 'none') return { works: false, note: 'There is no published host port, so this request has no route into the container.' };
      if (state.client === 'remote' && state.publish === 'local') return { works: false, note: 'The host port is bound to host loopback (127.0.0.1), so only this host can use it.' };
      if (state.bind === 'loopback') return { works: false, note: 'Docker forwards the packet into the container, but the app listens only on the container’s private loopback interface.' };
      return { works: true, note: 'The host port is reachable, Docker forwards it, and the app accepts traffic on the container network interface.' };
    }

    function hideAnswer() {
      const result = el.querySelector('[data-result]');
      result.className = 'connection-result';
      el.querySelector('[data-result-title]').textContent = 'Choose your prediction';
      el.querySelector('[data-result-note]').textContent = 'The answer stays hidden until you predict.';
      el.querySelector('[data-prediction]').textContent = '';
    }

    function render() {
      choiceButtons(bindBox, BINDS, state.bind, (value) => { state.bind = value; render(); hideAnswer(); });
      choiceButtons(publishBox, PUBLISH, state.publish, (value) => { state.publish = value; render(); hideAnswer(); });
      choiceButtons(clientBox, CLIENTS, state.client, (value) => { state.client = value; render(); hideAnswer(); });
      el.querySelector('[data-source-text]').textContent = state.client === 'same' ? '127.0.0.1:8000' : state.client === 'host' ? '127.0.0.1:8080' : 'host-ip:8080';
      el.querySelector('[data-host-text]').textContent = state.client === 'same' ? 'not used' : state.publish === 'none' ? 'not published' : state.publish === 'local' ? 'host-only :8080' : 'all host addresses :8080';
      el.querySelector('[data-app-text]').textContent = state.bind === 'loopback' ? '127.0.0.1:8000' : '0.0.0.0:8000';
      el.querySelector('[data-host]').classList.toggle('is-muted', state.client === 'same');
    }

    el.querySelectorAll('[data-predict]').forEach((button) => button.addEventListener('click', () => {
      const actual = outcome();
      const predictedWorks = button.dataset.predict === 'works';
      const correct = predictedWorks === actual.works;
      const result = el.querySelector('[data-result]');
      result.className = `connection-result ${actual.works ? 'is-success' : 'is-failure'}`;
      el.querySelector('[data-prediction]').textContent = correct ? '✓ Good prediction' : 'Not this time—follow the route';
      el.querySelector('[data-result-title]').textContent = actual.works ? 'Connection succeeds' : 'Connection fails';
      el.querySelector('[data-result-note]').textContent = actual.note;
    }));

    render();
  }

  /* ---------- WORKDIR isolation simulator ---------- */

  function initWorkdirLab() {
    const el = document.getElementById('workdir-lab');
    if (!el) return;
    const initial = () => ({ mode: 'isolated', a: 1, b: 1, shared: 1, log: [] });
    let state = initial();

    el.innerHTML = `
      <span class="widget-title">Try it · same path, different storage</span>
      <div class="widget-row" data-workdir-mode></div>
      <div class="workdir-host">
        <span>Your physical machine</span>
        <div class="workdir-containers">
          <div class="workdir-container"><small>Container A · image api</small><b>/app</b><span data-file-a></span></div>
          <div class="workdir-container"><small>Container B · image worker</small><b>/app</b><span data-file-b></span></div>
        </div>
        <div class="shared-folder" data-shared-folder><small>External storage</small><b>./shared</b><span data-shared-file></span></div>
      </div>
      <div class="widget-row" data-workdir-actions></div>
      <pre class="mini-term" data-workdir-log aria-live="polite"></pre>`;

    const modeBox = el.querySelector('[data-workdir-mode]');
    const actions = el.querySelector('[data-workdir-actions]');

    function addAction(label, run) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'btn btn-small';
      button.textContent = label;
      button.addEventListener('click', () => { run(); render(); });
      actions.appendChild(button);
    }

    function render() {
      choiceButtons(modeBox, [
        { value: 'isolated', label: 'Normal: isolated filesystems' },
        { value: 'shared', label: 'Mount the same ./shared folder' },
      ], state.mode, (value) => {
        state.mode = value;
        state.log.push(value === 'isolated' ? '$ no shared mount\n  → /app in A and B are unrelated' : '$ mount ./shared:/app in both containers\n  → both /app paths now show the same host folder');
        render();
      });

      const aVersion = state.mode === 'shared' ? state.shared : state.a;
      const bVersion = state.mode === 'shared' ? state.shared : state.b;
      el.querySelector('[data-file-a]').textContent = `note.txt · version ${aVersion}`;
      el.querySelector('[data-file-b]').textContent = `note.txt · version ${bVersion}`;
      el.querySelector('[data-shared-folder]').classList.toggle('is-visible', state.mode === 'shared');
      el.querySelector('[data-shared-file]').textContent = `note.txt · version ${state.shared}`;

      actions.innerHTML = '';
      addAction('Write in Container A', () => {
        if (state.mode === 'shared') state.shared += 1;
        else state.a += 1;
        state.log.push(`$ container-a: echo update > /app/note.txt\n  → ${state.mode === 'shared' ? 'Container B sees it because both mount ./shared' : 'only Container A changes'}`);
      });
      addAction('Write in Container B', () => {
        if (state.mode === 'shared') state.shared += 1;
        else state.b += 1;
        state.log.push(`$ container-b: echo update > /app/note.txt\n  → ${state.mode === 'shared' ? 'Container A sees it because both mount ./shared' : 'only Container B changes'}`);
      });
      addAction('Reset', () => { state = initial(); });
      el.querySelector('[data-workdir-log]').textContent = state.log.length ? state.log.slice(-8).join('\n') : 'Both containers say /app, but each starts with its own filesystem. Write in one and watch the other.';
    }

    render();
  }

  /* ---------- ENTRYPOINT + CMD resolver ---------- */

  function initCommandLab() {
    const el = document.getElementById('command-lab');
    if (!el) return;

    const SCENARIOS = [
      {
        label: 'Use defaults', run: 'docker run report',
        entrypoint: '["python"]', cmd: '["app.py", "--mode", "daily"]', args: 'none',
        final: 'python app.py --mode daily', note: 'No runtime arguments were given, so CMD supplies the default arguments to ENTRYPOINT.',
      },
      {
        label: 'Replace CMD', run: 'docker run report worker.py --once',
        entrypoint: '["python"]', cmd: '["app.py", "--mode", "daily"]', args: 'worker.py --once',
        final: 'python worker.py --once', note: 'Everything after the image name replaces CMD, while ENTRYPOINT remains python.',
      },
      {
        label: 'Replace ENTRYPOINT', run: 'docker run --entrypoint sh report',
        entrypoint: '["python"]', cmd: '["app.py", "--mode", "daily"]', args: '--entrypoint sh',
        final: 'sh', note: '--entrypoint deliberately replaces the image ENTRYPOINT. In this example no command arguments are supplied.',
      },
      {
        label: 'CMD without ENTRYPOINT', run: 'docker run simple',
        entrypoint: 'none', cmd: '["python", "app.py"]', args: 'none',
        final: 'python app.py', note: 'Without ENTRYPOINT, CMD is the complete default command.',
      },
    ];
    let current = 0;

    el.innerHTML = `
      <span class="widget-title">Try it · resolve the final process</span>
      <div class="command-scenarios" data-command-scenarios></div>
      <div class="command-formula">
        <div><small>Image ENTRYPOINT</small><b data-entrypoint></b></div><span>+</span>
        <div><small>Image CMD</small><b data-cmd></b></div><span>+</span>
        <div><small>docker run change</small><b data-args></b></div>
      </div>
      <div class="final-command"><small>Final process</small><b data-final></b></div>
      <pre class="mini-term" data-run-command></pre>
      <p class="widget-note" data-command-note></p>`;

    const scenarioBox = el.querySelector('[data-command-scenarios]');
    SCENARIOS.forEach((scenario, index) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'btn btn-small';
      button.textContent = scenario.label;
      button.addEventListener('click', () => { current = index; render(); });
      scenarioBox.appendChild(button);
    });

    function render() {
      const scenario = SCENARIOS[current];
      [...scenarioBox.children].forEach((button, index) => button.classList.toggle('is-on', index === current));
      el.querySelector('[data-entrypoint]').textContent = scenario.entrypoint;
      el.querySelector('[data-cmd]').textContent = scenario.cmd;
      el.querySelector('[data-args]').textContent = scenario.args;
      el.querySelector('[data-final]').textContent = scenario.final;
      el.querySelector('[data-run-command]').textContent = `$ ${scenario.run}\n→ ${scenario.final}`;
      el.querySelector('[data-command-note]').textContent = scenario.note;
    }

    render();
  }

  /* ---------- PID 1 and signals ---------- */

  function initSignalLab() {
    const el = document.getElementById('signal-lab');
    if (!el) return;
    const FLOWS = {
      exec: [
        ['Running', 'gunicorn is PID 1 and serves requests.'],
        ['SIGTERM', 'docker stop sends SIGTERM directly to gunicorn.'],
        ['Graceful exit', 'gunicorn stops accepting work, finishes safely, and exits before the timeout.'],
      ],
      shell: [
        ['Running', '/bin/sh is PID 1; gunicorn is its child process.'],
        ['SIGTERM', 'docker stop sends SIGTERM to /bin/sh.'],
        ['Signal risk', 'The shell may not forward the signal, so gunicorn may keep running.'],
        ['Forced stop', 'After the grace period, Docker sends SIGKILL. Incomplete work may be lost.'],
      ],
    };
    let mode = 'exec';
    let stage = 0;

    el.innerHTML = `
      <span class="widget-title">Try it · follow docker stop</span>
      <div class="widget-row" data-signal-mode></div>
      <div class="signal-flow" data-signal-flow></div>
      <div class="signal-message" aria-live="polite"><b data-signal-title></b><p data-signal-note></p></div>
      <div class="widget-row">
        <button class="btn btn-small btn-primary" type="button" data-signal-next></button>
        <button class="btn btn-small" type="button" data-signal-reset>Reset</button>
      </div>`;

    const modeBox = el.querySelector('[data-signal-mode]');
    const next = el.querySelector('[data-signal-next]');

    function render() {
      choiceButtons(modeBox, [
        { value: 'exec', label: 'Exec form: CMD ["gunicorn", …]' },
        { value: 'shell', label: 'Shell form: CMD gunicorn …' },
      ], mode, (value) => { mode = value; stage = 0; render(); });
      const flow = FLOWS[mode];
      el.querySelector('[data-signal-flow]').innerHTML = flow.map((item, index) => `
        ${index ? '<span aria-hidden="true">→</span>' : ''}
        <div class="signal-step${index < stage ? ' is-past' : ''}${index === stage ? ' is-current' : ''}"><small>${index + 1}</small><b>${item[0]}</b></div>`).join('');
      el.querySelector('[data-signal-title]').textContent = flow[stage][0];
      el.querySelector('[data-signal-note]').textContent = flow[stage][1];
      next.disabled = stage === flow.length - 1;
      next.textContent = stage === 0 ? 'Run docker stop →' : 'Next event →';
    }

    next.addEventListener('click', () => { if (stage < FLOWS[mode].length - 1) { stage += 1; render(); } });
    el.querySelector('[data-signal-reset]').addEventListener('click', () => { stage = 0; render(); });
    render();
  }

  /* ---------- Compose interpolation vs container environment ---------- */

  function initEnvLab() {
    const el = document.getElementById('env-lab');
    if (!el) return;
    el.innerHTML = `
      <span class="widget-title">Try it · where does the value go?</span>
      <div class="env-controls">
        <label><span>.env HOST_PORT</span><input type="number" min="1" max="65535" placeholder="leave blank" data-host-port></label>
        <label><span>.env APP_PORT</span><input type="number" min="1" max="65535" value="8000" data-app-port></label>
        <label class="check-control"><input type="checkbox" data-pass-env><span><b>Pass APP_PORT with environment:</b><small>Turn this off to prove .env alone does not inject it.</small></span></label>
      </div>
      <div class="env-pipeline">
        <div><small>1 · .env input</small><pre data-env-source></pre></div>
        <span aria-hidden="true">→</span>
        <div><small>2 · Resolved compose model</small><pre data-env-compose></pre></div>
        <span aria-hidden="true">→</span>
        <div><small>3 · Inside container</small><pre data-env-container></pre></div>
      </div>
      <p class="builder-warning" data-env-note aria-live="polite"></p>`;

    const host = el.querySelector('[data-host-port]');
    const app = el.querySelector('[data-app-port]');
    const pass = el.querySelector('[data-pass-env]');

    function validPort(input, fallback) {
      const value = Number(input.value);
      return value >= 1 && value <= 65535 ? String(value) : fallback;
    }

    function render() {
      const hostPort = validPort(host, '8080');
      const appPort = validPort(app, '8000');
      const hostWasDefault = !host.value;
      el.querySelector('[data-env-source]').textContent = `${host.value ? `HOST_PORT=${hostPort}\n` : '# HOST_PORT is not set\n'}APP_PORT=${appPort}`;
      el.querySelector('[data-env-compose]').textContent = `services:\n  web:\n    ports:\n      - "${hostPort}:${appPort}"${pass.checked ? `\n    environment:\n      APP_PORT: "${appPort}"` : ''}`;
      el.querySelector('[data-env-container]').textContent = pass.checked ? `APP_PORT=${appPort}` : 'APP_PORT is not set';
      el.querySelector('[data-env-note]').textContent = `${hostWasDefault ? 'HOST_PORT used the ${HOST_PORT:-8080} fallback. ' : 'HOST_PORT came from .env. '}The port mapping is part of the Compose model.${pass.checked ? ' APP_PORT also enters the container because environment: passes it.' : ' APP_PORT stays outside because .env alone only supplies interpolation values.'}`;
    }

    [host, app].forEach((input) => input.addEventListener('input', render));
    pass.addEventListener('change', render);
    render();
  }

  document.addEventListener('DOMContentLoaded', () => {
    initListenLab();
    initWorkdirLab();
    initCommandLab();
    initSignalLab();
    initEnvLab();
  });
})();
