/* Filterable Docker interview question bank and checklist progress. */
(function () {
  'use strict';

  const QUESTIONS = [
    {
      level: 'beginner', topic: 'Concepts',
      question: 'What problem does Docker solve?',
      short: 'Docker packages an application with its runtime and dependencies into a portable image, so the same artifact can run consistently in different environments.',
      points: ['Repeatable environments', 'Dependency isolation', 'One build artifact from test to production'],
      follow: 'What can still differ between environments even when the image is identical?',
    },
    {
      level: 'beginner', topic: 'Concepts',
      question: 'What is the difference between an image and a container?',
      short: 'An image is an immutable package and template. A container is a running or stopped instance created from that image, with its own writable layer and runtime settings.',
      points: ['One image can create many containers', 'Deleting a container does not delete the image', 'Persistent data should not depend on the writable layer'],
      follow: 'What happens to a running container after you rebuild its image?',
    },
    {
      level: 'beginner', topic: 'Runtime',
      question: 'How are docker run and docker start different?',
      short: 'docker run creates a new container from an image and starts it. docker start starts an existing stopped container with its existing writable layer and configuration.',
      points: ['run = create + start', 'start does not accept a new image', 'Repeated docker run commands create repeated containers'],
      follow: 'When would docker restart still show old application code?',
    },
    {
      level: 'beginner', topic: 'Networking',
      question: 'Explain -p 8080:80.',
      short: 'Docker publishes host port 8080 and forwards it to port 80 in the container. Users connect to localhost:8080; the application must actually listen on port 80 inside.',
      points: ['Order is HOST:CONTAINER', 'The host port can change without changing the app', 'EXPOSE alone does not publish'],
      follow: 'Why might the mapping exist while the browser still cannot connect?',
    },
    {
      level: 'beginner', topic: 'Build',
      question: 'What does a Dockerfile do?',
      short: 'A Dockerfile is a version-controlled list of instructions Docker uses to build an image: choose a base, copy files, install dependencies, set metadata and define the startup command.',
      points: ['Dockerfile is input; image is output', 'Each instruction can create a cacheable layer', 'It does not run the production container by itself'],
      follow: 'What files should be excluded from the build context?',
    },
    {
      level: 'beginner', topic: 'Data',
      question: 'Why use a volume?',
      short: 'A volume stores data outside a container’s disposable writable layer, so data can survive container replacement and be managed independently of the image.',
      points: ['Good for database data', 'Lifecycle is separate from a container', 'Backups and permissions still need a plan'],
      follow: 'How is a named volume different from a bind mount?',
    },
    {
      level: 'intermediate', topic: 'Build',
      question: 'How does Docker’s build cache work, and how do you optimize it?',
      short: 'Docker can reuse the result of an instruction when its inputs and the preceding build state have not changed. Put stable, expensive dependency steps before frequently changing source code.',
      points: ['A changed layer invalidates later dependent layers', 'Copy lock files before the full source tree', '.dockerignore reduces context and invalidation noise'],
      follow: 'Why is COPY . . before npm install usually slow?',
    },
    {
      level: 'intermediate', topic: 'Build',
      question: 'What is a multi-stage build?',
      short: 'It is one Dockerfile with multiple FROM stages. A builder stage compiles or tests; the final stage copies only the required artifacts, leaving tools and intermediate files behind.',
      points: ['Smaller runtime image', 'Reduced attack surface', 'Separate build and runtime dependencies'],
      follow: 'Can you build or debug only one named stage?',
    },
    {
      level: 'intermediate', topic: 'Runtime',
      question: 'What is the difference between CMD and ENTRYPOINT?',
      short: 'ENTRYPOINT defines the executable the container acts as; CMD supplies its default arguments or, without ENTRYPOINT, the default command. Runtime arguments replace CMD more naturally than ENTRYPOINT.',
      points: ['Use JSON exec form for signal handling', 'docker run image args replaces CMD', '--entrypoint deliberately overrides ENTRYPOINT'],
      follow: 'Why can shell-form commands mishandle stop signals?',
    },
    {
      level: 'intermediate', topic: 'Networking',
      question: 'How do containers find each other?',
      short: 'Containers on the same user-defined Docker network use built-in DNS and connect by container or Compose service name. They use the target container’s internal port, not its published host port.',
      points: ['localhost means the current container', 'Compose creates a default project network', 'Publishing is mainly for traffic from outside that network'],
      follow: 'Should an app connect to a Compose database at localhost:5432?',
    },
    {
      level: 'intermediate', topic: 'Data',
      question: 'Compare a bind mount and a named volume.',
      short: 'A bind mount exposes a specific host path and is convenient for live source code. A named volume is managed by Docker and is usually better for application data such as a database.',
      points: ['Bind mounts depend on host paths', 'Named volumes are portable across container replacements', 'Both bypass the image’s writable layer at the mount point'],
      follow: 'What happens to files already present at a mount target?',
    },
    {
      level: 'intermediate', topic: 'Operations',
      question: 'What makes a useful health check?',
      short: 'A useful check tests the smallest application behavior that proves the container can serve its role, with suitable timeout, interval, retries and startup grace period.',
      points: ['Running is not the same as healthy', 'Avoid a check that is heavier than normal traffic', 'Readiness and liveness are different concerns in orchestrators'],
      follow: 'Should a health endpoint fail when an optional dependency is unavailable?',
    },
    {
      level: 'intermediate', topic: 'Operations',
      question: 'How would you reduce a Docker image size?',
      short: 'Start with a smaller trusted base, use a multi-stage build, install only runtime dependencies, remove package-manager caches in the same layer and exclude unnecessary context files.',
      points: ['Measure with docker image history', 'Fewer layers alone is not the real goal', 'Do not sacrifice maintainability blindly'],
      follow: 'Why does deleting a large file in a later layer not remove it from earlier layers?',
    },
    {
      level: 'advanced', topic: 'Security',
      question: 'How would you harden a production container?',
      short: 'Use a trusted minimal image, run as non-root, keep secrets outside the image, drop unneeded capabilities, avoid privileged mode and sensitive mounts, use read-only filesystems where possible, set resource limits and scan/rebuild regularly.',
      points: ['Docker socket access is highly privileged', 'Container root is still a risk', 'Security includes the daemon and host, not only the Dockerfile'],
      follow: 'When would rootless Docker or user-namespace remapping help?',
    },
    {
      level: 'advanced', topic: 'Runtime',
      question: 'Why is PID 1 special inside a container?',
      short: 'The container’s main process becomes PID 1. It must receive and handle termination signals and reap orphaned child processes; shell wrappers that do not exec the app can break graceful shutdown.',
      points: ['Prefer exec-form CMD or ENTRYPOINT', 'Use exec in entrypoint scripts', 'Use --init when the application cannot reap children'],
      follow: 'What happens between docker stop and docker kill?',
    },
    {
      level: 'advanced', topic: 'Delivery',
      question: 'How do you make image deployments reproducible and rollbacks safe?',
      short: 'Build once in CI, test it, tag it with an immutable version or commit, record its digest and promote that same image through environments. Keep the previous version and make data migrations backward compatible.',
      points: ['Do not rebuild for each environment', 'A mutable tag is not an exact identity', 'A code rollback does not roll back database state'],
      follow: 'When is deploying by digest preferable to deploying by tag?',
    },
    {
      level: 'advanced', topic: 'Operations',
      question: 'What happens when a container exceeds its memory limit?',
      short: 'The kernel can terminate processes in the container for out-of-memory use, commonly producing exit code 137. Diagnose with inspect, events and metrics; then fix the leak or tune a measured limit and reservation.',
      points: ['Containers have no limits unless configured', 'Restart policies can hide repeated crashes', 'CPU limits throttle rather than usually killing'],
      follow: 'Why is “just increase the limit” not a complete answer?',
    },
    {
      level: 'advanced', topic: 'Platform',
      question: 'How do multi-platform images work?',
      short: 'A multi-platform tag points to an image index containing platform-specific manifests, such as linux/amd64 and linux/arm64. The registry client selects the matching image for the host.',
      points: ['Binaries must match OS and CPU architecture', 'Buildx can build multiple targets', 'Emulation is convenient but can be slower'],
      follow: 'What causes an exec format error after an image pull?',
    },
  ];

  const KNOWN_KEY = 'docker-kt-interview-known';
  const STANDARDS_KEY = 'docker-kt-standards-done';

  function initQuestionBank() {
    const root = document.getElementById('interview-bank');
    if (!root || !window.DockerKT) return;
    const esc = window.DockerKT.esc;
    let level = 'all';
    let topic = 'all';
    let query = '';
    let known = new Set(window.DockerKT.store.get(KNOWN_KEY, []));

    root.innerHTML = `
      <div class="interview-tools">
        <label class="interview-search"><span class="sr-only">Search questions</span><input type="search" placeholder="Search questions…" data-search></label>
        <div class="filter-row" data-levels>
          <button class="btn btn-small is-on" type="button" data-level="all">All levels</button>
          <button class="btn btn-small" type="button" data-level="beginner">Beginner</button>
          <button class="btn btn-small" type="button" data-level="intermediate">Intermediate</button>
          <button class="btn btn-small" type="button" data-level="advanced">Advanced</button>
        </div>
        <select data-topic aria-label="Filter by topic"><option value="all">All topics</option></select>
        <button class="btn btn-primary btn-small" type="button" data-random>Give me one question</button>
      </div>
      <div class="interview-summary"><b data-visible></b><span data-known-count></span></div>
      <div class="interview-list" data-list></div>`;

    const topics = [...new Set(QUESTIONS.map((item) => item.topic))].sort();
    const topicSelect = root.querySelector('[data-topic]');
    topics.forEach((name) => {
      const option = document.createElement('option');
      option.value = name;
      option.textContent = name;
      topicSelect.appendChild(option);
    });

    function visibleQuestions() {
      const term = query.toLowerCase();
      return QUESTIONS.map((item, index) => ({ ...item, index })).filter((item) =>
        (level === 'all' || item.level === level) &&
        (topic === 'all' || item.topic === topic) &&
        (!term || `${item.question} ${item.short} ${item.topic} ${item.points.join(' ')}`.toLowerCase().includes(term)));
    }

    function render() {
      const items = visibleQuestions();
      root.querySelector('[data-visible]').textContent = `${items.length} question${items.length === 1 ? '' : 's'} shown`;
      root.querySelector('[data-known-count]').textContent = `${known.size} of ${QUESTIONS.length} marked confident`;
      root.querySelector('[data-list]').innerHTML = items.length ? items.map((item) => `
        <details class="interview-question${known.has(item.index) ? ' is-known' : ''}" data-question="${item.index}">
          <summary>
            <span class="badge ${item.level === 'beginner' ? 'ok' : item.level === 'intermediate' ? 'info' : 'warn'}">${esc(item.level)}</span>
            <b>${esc(item.question)}</b>
            <span class="question-topic">${esc(item.topic)}</span>
          </summary>
          <div class="interview-answer">
            <span class="callout-title">30-second answer</span>
            <p>${esc(item.short)}</p>
            <span class="callout-title">Points to include</span>
            <ul>${item.points.map((point) => `<li>${esc(point)}</li>`).join('')}</ul>
            <div class="follow-up"><b>Likely follow-up:</b> ${esc(item.follow)}</div>
            <button class="btn btn-small${known.has(item.index) ? ' is-on' : ''}" type="button" data-known="${item.index}">${known.has(item.index) ? '✓ I can explain this' : 'Mark as confident'}</button>
          </div>
        </details>`).join('') : '<div class="callout warn"><span class="callout-title">No matches</span><p>Try a different word or clear one of the filters.</p></div>';
    }

    root.querySelector('[data-search]').addEventListener('input', (event) => {
      query = event.target.value.trim();
      render();
    });
    root.querySelector('[data-levels]').addEventListener('click', (event) => {
      const button = event.target.closest('[data-level]');
      if (!button) return;
      level = button.dataset.level;
      root.querySelectorAll('[data-level]').forEach((item) => item.classList.toggle('is-on', item === button));
      render();
    });
    topicSelect.addEventListener('change', () => {
      topic = topicSelect.value;
      render();
    });
    root.querySelector('[data-list]').addEventListener('click', (event) => {
      const button = event.target.closest('[data-known]');
      if (!button) return;
      const index = Number(button.dataset.known);
      if (known.has(index)) known.delete(index);
      else known.add(index);
      window.DockerKT.store.set(KNOWN_KEY, [...known]);
      render();
    });
    root.querySelector('[data-random]').addEventListener('click', () => {
      const items = visibleQuestions();
      if (!items.length) return;
      const picked = items[Math.floor(Math.random() * items.length)];
      const detail = root.querySelector(`[data-question="${picked.index}"]`);
      if (!detail) return;
      root.querySelectorAll('.interview-question').forEach((item) => { item.open = false; });
      detail.open = true;
      detail.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });

    render();
  }

  function initStandards() {
    const list = document.querySelector('[data-standard-list]');
    if (!list || !window.DockerKT) return;
    const checks = [...list.querySelectorAll('input[type="checkbox"]')];
    const saved = new Set(window.DockerKT.store.get(STANDARDS_KEY, []));
    checks.forEach((check) => { check.checked = saved.has(check.value); });

    function render() {
      const done = checks.filter((check) => check.checked).map((check) => check.value);
      const percent = Math.round((done.length / checks.length) * 100);
      document.querySelector('[data-standard-progress]').style.width = `${percent}%`;
      document.querySelector('[data-standard-count]').textContent = `${done.length} of ${checks.length} understood`;
      window.DockerKT.store.set(STANDARDS_KEY, done);
      checks.forEach((check) => check.closest('.standard-card').classList.toggle('is-done', check.checked));
    }

    checks.forEach((check) => check.addEventListener('change', render));
    render();
  }

  document.addEventListener('DOMContentLoaded', () => {
    initQuestionBank();
    initStandards();
  });
})();
