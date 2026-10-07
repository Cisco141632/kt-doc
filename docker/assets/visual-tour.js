/* Interactive visual walkthrough for visual-tour.html. */
(function () {
  'use strict';

  const STEPS = [
    {
      label: 'Files',
      title: 'Start with app files and a Dockerfile',
      command: 'project/\n├── app.py\n├── requirements.txt\n└── Dockerfile',
      output: 'These are ordinary files on your laptop. Docker has not created anything yet.',
      next: 'Build the image',
      image: false,
      container: 'none',
      browser: 'idle',
      active: 'source',
    },
    {
      label: 'Build',
      title: 'Build a reusable image',
      command: '$ docker build -t hello-web:1.0 .',
      output: 'Docker reads the Dockerfile, executes its steps as layers, then saves the result as hello-web:1.0.',
      terminal: '[1/4] FROM python:3.13-slim\n[2/4] COPY requirements.txt .\n[3/4] RUN pip install -r requirements.txt\n[4/4] COPY . .\n✓ tagged hello-web:1.0',
      next: 'Run a container',
      image: true,
      container: 'none',
      browser: 'idle',
      active: 'image',
    },
    {
      label: 'Run',
      title: 'Create and start a container',
      command: '$ docker run -d --name web -p 8080:8000 hello-web:1.0',
      output: 'Docker adds a small writable layer, starts the app and connects host port 8080 to container port 8000.',
      terminal: 'c51f3a789d28\n✓ container web is running',
      next: 'Send a request',
      image: true,
      container: 'running',
      browser: 'idle',
      active: 'container',
    },
    {
      label: 'Request',
      title: 'Send traffic through the published port',
      command: '$ curl http://localhost:8080',
      output: 'The request reaches port 8080 on your laptop. Docker forwards it to port 8000 inside the container, where the app answers.',
      terminal: 'Hello from container c51f3a789d28!',
      next: 'Inspect it',
      image: true,
      container: 'running',
      browser: 'success',
      active: 'browser',
    },
    {
      label: 'Inspect',
      title: 'Check status and read logs',
      command: '$ docker ps\n$ docker logs web',
      output: 'docker ps shows running containers. docker logs shows what the main process has written to standard output and error.',
      terminal: 'NAME   IMAGE           STATUS       PORTS\nweb    hello-web:1.0   Up 1 minute  0.0.0.0:8080→8000\n\nGET / 200 OK',
      next: 'Stop it',
      image: true,
      container: 'running',
      browser: 'success',
      active: 'engine',
    },
    {
      label: 'Stop',
      title: 'Stop the process safely',
      command: '$ docker stop web',
      output: 'The app stops, but the container and its writable files still exist. The image is untouched.',
      terminal: 'web\n✓ container exists with status Exited',
      next: 'Remove the container',
      image: true,
      container: 'stopped',
      browser: 'blocked',
      active: 'container',
    },
    {
      label: 'Remove',
      title: 'Remove the stopped container',
      command: '$ docker rm web',
      output: 'The container is gone. The read-only image still exists, so another docker run can create a fresh container in seconds.',
      terminal: 'web\n✓ image hello-web:1.0 is still available',
      next: 'Remove the image',
      image: true,
      container: 'none',
      browser: 'idle',
      active: 'image',
    },
    {
      label: 'Clean image',
      title: 'Optionally remove the image',
      command: '$ docker rmi hello-web:1.0',
      output: 'Now both the container and image are gone. Your source files and Dockerfile are still safe on your laptop.',
      terminal: 'Untagged: hello-web:1.0\nDeleted: sha256:86f…\n✓ back where you started',
      next: 'Start again',
      image: false,
      container: 'none',
      browser: 'idle',
      active: 'source',
    },
  ];

  function initJourney() {
    const el = document.getElementById('visual-journey');
    if (!el) return;
    let current = 0;

    el.innerHTML = `
      <div class="journey-progress" role="tablist" aria-label="Docker journey steps"></div>
      <div class="journey-canvas">
        <div class="journey-node source-node" data-node="source">
          <span class="node-kicker">On your laptop</span>
          <b>App + Dockerfile</b>
          <div class="file-stack" aria-hidden="true"><span>app.py</span><span>requirements.txt</span><span>Dockerfile</span></div>
        </div>
        <span class="flow-arrow" aria-hidden="true">→</span>
        <div class="journey-node engine-node" data-node="engine">
          <span class="node-kicker">Background service</span>
          <b>Docker Engine</b>
          <span class="engine-gear" aria-hidden="true">⚙</span>
        </div>
        <span class="flow-arrow" aria-hidden="true">→</span>
        <div class="journey-node image-node" data-node="image">
          <span class="node-kicker">Read-only</span>
          <b>Image</b>
          <div class="image-layers" aria-hidden="true"><span></span><span></span><span></span></div>
          <small data-image-status>No image yet</small>
        </div>
        <span class="flow-arrow" aria-hidden="true">→</span>
        <div class="journey-node container-node" data-node="container">
          <span class="node-kicker">Isolated process</span>
          <b>Container</b>
          <span class="container-status" data-container-status>Not created</span>
        </div>
        <div class="browser-node" data-node="browser">
          <span class="browser-bar"><i></i><i></i><i></i><b>localhost:8080</b></span>
          <div class="browser-screen" data-browser-status>Waiting for a container</div>
        </div>
        <span class="request-path" data-request-path aria-hidden="true">request → :8080 → :8000</span>
      </div>
      <div class="journey-explain" aria-live="polite">
        <div>
          <span class="badge info" data-step-count></span>
          <h3 data-title></h3>
          <p data-output></p>
        </div>
        <pre class="mini-term" data-terminal></pre>
      </div>
      <div class="journey-controls">
        <button class="btn" type="button" data-back>← Back</button>
        <button class="btn btn-primary" type="button" data-next></button>
        <button class="btn" type="button" data-reset>Reset</button>
      </div>`;

    const progress = el.querySelector('.journey-progress');
    const buttons = STEPS.map((step, index) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.setAttribute('role', 'tab');
      button.innerHTML = `<span>${index + 1}</span>${step.label}`;
      button.addEventListener('click', () => show(index));
      progress.appendChild(button);
      return button;
    });

    const back = el.querySelector('[data-back]');
    const next = el.querySelector('[data-next]');
    const reset = el.querySelector('[data-reset]');
    const sourceNode = el.querySelector('[data-node="source"]');
    const engineNode = el.querySelector('[data-node="engine"]');
    const imageNode = el.querySelector('[data-node="image"]');
    const containerNode = el.querySelector('[data-node="container"]');
    const browserNode = el.querySelector('[data-node="browser"]');

    function show(index) {
      current = Math.max(0, Math.min(index, STEPS.length - 1));
      const step = STEPS[current];
      buttons.forEach((button, i) => {
        button.classList.toggle('is-current', i === current);
        button.classList.toggle('is-past', i < current);
        button.setAttribute('aria-selected', i === current ? 'true' : 'false');
      });

      [sourceNode, engineNode, imageNode, containerNode, browserNode].forEach((node) => node.classList.remove('is-active'));
      const activeNode = el.querySelector(`[data-node="${step.active}"]`);
      if (activeNode) activeNode.classList.add('is-active');

      imageNode.classList.toggle('has-image', step.image);
      el.querySelector('[data-image-status]').textContent = step.image ? 'hello-web:1.0' : 'No image yet';

      containerNode.dataset.state = step.container;
      const status = step.container === 'running' ? '● Running' : step.container === 'stopped' ? '■ Exited' : 'Not created';
      el.querySelector('[data-container-status]').textContent = status;

      browserNode.dataset.state = step.browser;
      el.querySelector('[data-browser-status]').textContent = step.browser === 'success'
        ? '200 OK · Hello!'
        : step.browser === 'blocked' ? 'Cannot connect' : 'Waiting for a container';
      el.querySelector('[data-request-path]').classList.toggle('is-visible', step.browser === 'success');

      el.querySelector('[data-step-count]').textContent = `Step ${current + 1} of ${STEPS.length}`;
      el.querySelector('[data-title]').textContent = step.title;
      el.querySelector('[data-output]').textContent = step.output;
      el.querySelector('[data-terminal]').textContent = `${step.command}${step.terminal ? `\n\n${step.terminal}` : ''}`;

      back.disabled = current === 0;
      next.textContent = current === STEPS.length - 1 ? '↻ Start again' : `${step.next} →`;
      reset.hidden = current === 0;
    }

    back.addEventListener('click', () => show(current - 1));
    next.addEventListener('click', () => show(current === STEPS.length - 1 ? 0 : current + 1));
    reset.addEventListener('click', () => show(0));
    show(0);
  }

  function initRunBuilder() {
    const el = document.getElementById('run-builder');
    if (!el) return;

    el.innerHTML = `
      <div class="builder-controls">
        <label><span>Image</span><select data-image>
          <option value="nginx:alpine" data-port="80">nginx:alpine (web server)</option>
          <option value="hello-web:1.0" data-port="8000">hello-web:1.0 (our app)</option>
          <option value="postgres:17" data-port="5432">postgres:17 (database)</option>
        </select></label>
        <label><span>Container name</span><input type="text" value="web" maxlength="24" data-name></label>
        <label><span>Host port</span><input type="number" value="8080" min="1" max="65535" data-host-port></label>
        <label class="check-control"><input type="checkbox" checked data-detach><span><b>Run in background</b><small>Adds <code>-d</code></small></span></label>
        <label class="check-control"><input type="checkbox" checked data-publish><span><b>Publish a port</b><small>Adds <code>-p</code></small></span></label>
        <label class="check-control"><input type="checkbox" checked data-remove><span><b>Auto-remove when stopped</b><small>Adds <code>--rm</code></small></span></label>
      </div>
      <div class="builder-result">
        <span class="widget-title">Your command</span>
        <div class="command-output"><code data-command></code><button class="btn btn-small" type="button" data-copy>Copy</button></div>
        <div class="builder-network">
          <div><small>Browser / client</small><b data-client>localhost:8080</b></div>
          <span aria-hidden="true">→</span>
          <div><small>Your machine</small><b data-host>port 8080</b></div>
          <span aria-hidden="true">→</span>
          <div><small>Container</small><b data-container>nginx:alpine · port 80</b></div>
        </div>
        <ul class="command-parts" data-parts></ul>
        <p class="builder-warning" data-warning aria-live="polite"></p>
      </div>`;

    const image = el.querySelector('[data-image]');
    const name = el.querySelector('[data-name]');
    const hostPort = el.querySelector('[data-host-port]');
    const detach = el.querySelector('[data-detach]');
    const publish = el.querySelector('[data-publish]');
    const remove = el.querySelector('[data-remove]');
    const copyButton = el.querySelector('[data-copy]');

    function safeName(value) {
      return value.trim().replace(/[^a-zA-Z0-9_.-]/g, '-').replace(/^-+|-+$/g, '') || 'web';
    }

    function selectedPort() {
      return image.options[image.selectedIndex].dataset.port;
    }

    function render() {
      const containerPort = selectedPort();
      const port = Math.max(1, Math.min(65535, Number(hostPort.value) || 8080));
      const containerName = safeName(name.value);
      const pieces = ['docker run'];
      if (detach.checked) pieces.push('-d');
      if (remove.checked) pieces.push('--rm');
      pieces.push(`--name ${containerName}`);
      if (publish.checked) pieces.push(`-p ${port}:${containerPort}`);
      pieces.push(image.value);
      const command = pieces.join(' ');

      el.querySelector('[data-command]').textContent = command;
      el.querySelector('[data-client]').textContent = publish.checked ? `localhost:${port}` : 'No host address';
      el.querySelector('[data-host]').textContent = publish.checked ? `port ${port}` : 'Port not published';
      el.querySelector('[data-container]').textContent = `${image.value} · port ${containerPort}`;
      el.querySelector('.builder-network').classList.toggle('is-blocked', !publish.checked);
      el.querySelector('[data-parts]').innerHTML = [
        `<li><code>docker run</code><span>Create and start a new container.</span></li>`,
        detach.checked ? `<li><code>-d</code><span>Give your terminal back while the app runs.</span></li>` : `<li><code>no -d</code><span>Keep logs attached to this terminal; press Ctrl+C to stop.</span></li>`,
        remove.checked ? `<li><code>--rm</code><span>Delete the container automatically after it stops.</span></li>` : `<li><code>no --rm</code><span>Keep the stopped container so you can inspect or restart it.</span></li>`,
        `<li><code>--name ${containerName}</code><span>Give the container a human-friendly name.</span></li>`,
        publish.checked ? `<li><code>-p ${port}:${containerPort}</code><span>Send host port ${port} to the app's port ${containerPort}.</span></li>` : `<li><code>no -p</code><span>The container can run, but your browser cannot reach it from the host.</span></li>`,
        `<li><code>${image.value}</code><span>Create the container from this image.</span></li>`,
      ].join('');
      el.querySelector('[data-warning]').textContent = publish.checked
        ? `Open localhost:${port} to reach the app. The right-hand port stays ${containerPort} because that is where this image listens.`
        : 'No port is published. Other containers on the same Docker network may still reach it, but your host browser cannot.';
    }

    [image, name, hostPort, detach, publish, remove].forEach((control) => {
      control.addEventListener(control.type === 'text' || control.type === 'number' ? 'input' : 'change', render);
    });

    copyButton.addEventListener('click', () => {
      const command = el.querySelector('[data-command]').textContent;
      const copied = () => {
        copyButton.textContent = 'Copied';
        window.setTimeout(() => { copyButton.textContent = 'Copy'; }, 1500);
      };
      const fallback = () => {
        const area = document.createElement('textarea');
        area.value = command;
        document.body.appendChild(area);
        area.select();
        try { document.execCommand('copy'); } catch (error) { copyButton.textContent = 'Press Ctrl+C'; }
        area.remove();
        copied();
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(command).then(copied, fallback);
      else fallback();
    });

    render();
  }

  document.addEventListener('DOMContentLoaded', () => {
    initJourney();
    initRunBuilder();
  });
})();
