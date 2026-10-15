/* CI/CD learning path — navigation, progress, diagrams and code helpers. */
(function () {
  'use strict';

  const MODULES = [
    { id: 'index', file: 'index.html', title: 'What is CI/CD?', mins: 15, desc: 'The problem, the vocabulary and the complete path from commit to production.' },
    { id: 'foundations', file: 'foundations.html', title: 'Pipeline foundations', mins: 20, desc: 'Triggers, stages, jobs, runners, artifacts, gates and a healthy pipeline shape.' },
    { id: 'ci', file: 'continuous-integration.html', title: 'Continuous integration', mins: 25, desc: 'Pull requests, fast feedback, test layers, quality gates and branch protection.' },
    { id: 'docker', file: 'docker-artifacts.html', title: 'Docker & artifacts', mins: 30, desc: 'Build once, tag immutably, scan, publish and promote the exact same image.' },
    { id: 'delivery', file: 'delivery-environments.html', title: 'Delivery & environments', mins: 25, desc: 'Development, staging and production, approvals, configuration and database changes.' },
    { id: 'deploy', file: 'deployment-strategies.html', title: 'Deployment strategies', mins: 25, desc: 'Recreate, rolling, blue-green, canary, feature flags and safe rollback.' },
    { id: 'security', file: 'security.html', title: 'Pipeline security', mins: 25, desc: 'Secrets, least privilege, dependency and image scans, SBOMs and provenance.' },
    { id: 'gitops', file: 'iac-gitops.html', title: 'IaC, Kubernetes & GitOps', mins: 25, desc: 'Terraform, Kubernetes, Helm and reconciliation-based delivery.' },
    { id: 'observe', file: 'observability.html', title: 'Observe & improve', mins: 20, desc: 'Health, logs, metrics, traces, release verification and delivery performance.' },
    { id: 'practice', file: 'practice.html', title: 'Hands-on pipeline', mins: 45, desc: 'Create a GitHub Actions pipeline that tests and publishes a Docker image.' },
    { id: 'quiz', file: 'quiz.html', title: 'Knowledge check', mins: 20, desc: 'Scenario-based questions with immediate explanations.' },
    { id: 'cheatsheet', file: 'cheatsheet.html', title: 'Cheat sheet', mins: 10, desc: 'Pipeline blueprint, tool map, commands, release checklist and troubleshooting.' },
  ];

  const THEME_KEY = 'cicd-kt-theme';
  const DONE_KEY = 'cicd-kt-done';
  const MERMAID_SRC = 'https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.min.js';
  const LANG_LABELS = { sh: 'Terminal', console: 'Terminal', yaml: 'YAML', dockerfile: 'Dockerfile', text: 'Text', json: 'JSON', hcl: 'Terraform' };
  const root = document.documentElement;
  root.classList.add('js');

  const store = {
    get(key, fallback) {
      try { const raw = localStorage.getItem(key); return raw === null ? fallback : JSON.parse(raw); }
      catch (error) { return fallback; }
    },
    set(key, value) {
      try { localStorage.setItem(key, JSON.stringify(value)); } catch (error) { /* optional progress only */ }
    },
  };

  function esc(value) {
    return String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  const systemDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  root.dataset.theme = store.get(THEME_KEY, null) || (systemDark ? 'dark' : 'light');

  const icon = document.createElement('link');
  icon.rel = 'icon';
  icon.href = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230a66c2'/%3E%3Ctext x='16' y='22' font-family='Arial' font-size='15' font-weight='700' text-anchor='middle' fill='white'%3ECI%3C/text%3E%3C/svg%3E";
  document.head.appendChild(icon);

  function activeId() { return document.body.dataset.module || ''; }
  function doneList() {
    const known = MODULES.map((module) => module.id);
    return store.get(DONE_KEY, []).filter((id) => known.includes(id));
  }
  function setDone(id, value) {
    const list = doneList().filter((item) => item !== id);
    if (value) list.push(id);
    store.set(DONE_KEY, list);
    renderSidebar();
    renderPager();
  }

  function renderSidebar() {
    const side = document.getElementById('sidebar');
    if (!side) return;
    const active = activeId();
    const done = doneList();
    const items = MODULES.map((module, index) => {
      const isActive = module.id === active;
      const isDone = done.includes(module.id);
      return `<li class="${isActive ? 'is-active' : ''} ${isDone ? 'is-done' : ''}">
        <a href="${module.file}"${isActive ? ' aria-current="page"' : ''}>
          <span class="num">${isDone ? '✓' : index + 1}</span><span class="t">${esc(module.title)}</span><span class="mins">${module.mins} min</span>
        </a>${isActive ? '<ul class="toc"></ul>' : ''}</li>`;
    }).join('');
    const pct = Math.round((done.length / MODULES.length) * 100);
    side.innerHTML = `<a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">CI</span>
        <span>CI/CD learning path<small>From commit to safe production</small></span></a>
      <div class="progress"><div class="progress-bar"><span style="width:${pct}%"></span></div>${done.length} of ${MODULES.length} modules done</div>
      <nav aria-label="Modules"><ol class="modules">${items}</ol></nav>
      <button class="btn btn-small theme-toggle" type="button">${root.dataset.theme === 'dark' ? 'Light theme' : 'Dark theme'}</button>`;

    const toc = side.querySelector('.toc');
    if (toc) document.querySelectorAll('main section[id] > h2').forEach((heading) => {
      const item = document.createElement('li');
      item.innerHTML = `<a href="#${heading.parentElement.id}">${esc(heading.textContent)}</a>`;
      toc.appendChild(item);
    });
    side.querySelector('.theme-toggle').addEventListener('click', () => {
      root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
      store.set(THEME_KEY, root.dataset.theme);
      renderSidebar();
      renderMermaid();
    });
  }

  function renderEyebrow() {
    const head = document.querySelector('.page-head');
    const index = MODULES.findIndex((module) => module.id === activeId());
    if (!head || index < 0) return;
    const eyebrow = document.createElement('p');
    eyebrow.className = 'eyebrow';
    eyebrow.textContent = `Module ${index + 1} of ${MODULES.length} · about ${MODULES[index].mins} minutes`;
    head.prepend(eyebrow);
  }

  function renderPager() {
    const main = document.querySelector('main');
    const index = MODULES.findIndex((module) => module.id === activeId());
    if (!main || index < 0) return;
    let pager = main.querySelector('.pager');
    if (!pager) { pager = document.createElement('footer'); pager.className = 'pager'; main.appendChild(pager); }
    const previous = MODULES[index - 1];
    const next = MODULES[index + 1];
    const isDone = doneList().includes(MODULES[index].id);
    pager.innerHTML = `${previous ? `<a class="btn" href="${previous.file}">← ${esc(previous.title)}</a>` : ''}<span class="spacer"></span>
      <button class="btn${isDone ? ' is-on' : ''}" type="button" data-done>${isDone ? '✓ Done (click to undo)' : 'Mark module as done'}</button>
      ${next ? `<a class="btn btn-primary" href="${next.file}">Next: ${esc(next.title)} →</a>` : ''}`;
    pager.querySelector('[data-done]').addEventListener('click', () => setDone(MODULES[index].id, !isDone));
  }

  function renderCards() {
    const target = document.querySelector('[data-module-cards]');
    if (!target) return;
    target.innerHTML = MODULES.map((module, index) => `<a class="card" href="${module.file}"><span class="tag">Module ${index + 1} · ${module.mins} min</span><b>${esc(module.title)}</b><small>${esc(module.desc)}</small></a>`).join('');
  }

  function highlight(text, lang) {
    let continued = false;
    return text.split('\n').map((line) => {
      if (lang === 'console') {
        const command = line.startsWith('$ ') || continued;
        const prompt = line.startsWith('$ ');
        continued = command && line.endsWith('\\');
        return command ? `${prompt ? '<span class="tok-prompt">$ </span>' : ''}${esc(prompt ? line.slice(2) : line)}` : `<span class="tok-out">${esc(line)}</span>`;
      }
      if (/^\s*#/.test(line)) return `<span class="tok-com">${esc(line)}</span>`;
      let html = esc(line);
      if (lang === 'dockerfile') html = html.replace(/^([A-Z]+)(?=\s)/, '<span class="tok-key">$1</span>');
      if (lang === 'yaml') html = html.replace(/^(\s*(?:- )?)([\w.-]+)(:)(?=\s|$)/, '$1<span class="tok-key">$2</span>$3');
      return html.replace(/(\s)(#\s.*)$/, '$1<span class="tok-com">$2</span>');
    }).join('\n');
  }

  function copyText(text, lang) {
    if (lang !== 'console') return text;
    const commands = [];
    let continued = false;
    text.split('\n').forEach((line) => {
      if (line.startsWith('$ ')) commands.push(line.slice(2));
      else if (continued) commands.push(line);
      else return;
      continued = line.endsWith('\\');
    });
    return commands.join('\n');
  }

  function copy(value, button) {
    const success = () => { button.textContent = 'Copied'; setTimeout(() => { button.textContent = 'Copy'; }, 1400); };
    const fallback = () => {
      const area = document.createElement('textarea'); area.value = value; area.style.position = 'fixed'; area.style.opacity = '0';
      document.body.appendChild(area); area.select();
      try { document.execCommand('copy'); success(); } catch (error) { button.textContent = 'Select manually'; }
      area.remove();
    };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(value).then(success, fallback); else fallback();
  }

  function enhanceCode() {
    document.querySelectorAll('pre[data-lang]').forEach((pre) => {
      if (pre.dataset.enhanced) return;
      pre.dataset.enhanced = '1';
      const lang = pre.dataset.lang;
      const value = pre.textContent.replace(/\s+$/, '');
      pre.innerHTML = highlight(value, lang);
      const wrap = document.createElement('div'); wrap.className = 'code';
      const head = document.createElement('div'); head.className = 'code-head';
      const label = document.createElement('span'); label.textContent = pre.dataset.title || LANG_LABELS[lang] || lang;
      const button = document.createElement('button'); button.type = 'button'; button.textContent = 'Copy';
      button.addEventListener('click', () => copy(copyText(value, lang), button));
      head.append(label, button); pre.replaceWith(wrap); wrap.append(head, pre);
    });
  }

  let mermaidReady = false;
  function loadMermaid() {
    const blocks = document.querySelectorAll('pre.mermaid');
    if (!blocks.length) return;
    blocks.forEach((block) => { block.dataset.src = block.textContent; });
    const script = document.createElement('script'); script.src = MERMAID_SRC;
    script.onload = () => { mermaidReady = true; renderMermaid(); };
    script.onerror = () => blocks.forEach((block) => block.classList.add('mermaid-failed'));
    document.head.appendChild(script);
  }
  function renderMermaid() {
    if (!mermaidReady || !window.mermaid) return;
    const css = getComputedStyle(root); const token = (name) => css.getPropertyValue(name).trim();
    window.mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'base', themeVariables: {
      darkMode: root.dataset.theme === 'dark', fontFamily: token('--font'), background: token('--surface'),
      primaryColor: token('--accent-soft'), primaryTextColor: token('--text'), primaryBorderColor: token('--accent'),
      secondaryColor: token('--surface-2'), secondaryTextColor: token('--text'), secondaryBorderColor: token('--border'),
      lineColor: token('--muted'), textColor: token('--text'), clusterBkg: token('--surface-2'), clusterBorder: token('--border'), edgeLabelBackground: token('--surface'),
    }});
    const blocks = [...document.querySelectorAll('pre.mermaid')];
    blocks.forEach((block) => { block.removeAttribute('data-processed'); block.classList.remove('mermaid-failed'); block.textContent = block.dataset.src; });
    window.mermaid.run({ nodes: blocks }).catch(() => blocks.filter((block) => !block.querySelector('svg')).forEach((block) => { block.textContent = block.dataset.src; block.classList.add('mermaid-failed'); }));
  }

  function initSteppers() {
    document.querySelectorAll('[data-stepper]').forEach((element) => {
      const steps = [...element.querySelectorAll(':scope > .step')]; if (!steps.length) return;
      let current = 0; const track = document.createElement('div'); track.className = 'stepper-track';
      const panel = document.createElement('div'); panel.className = 'stepper-panel'; panel.setAttribute('aria-live', 'polite');
      steps.forEach((step) => panel.appendChild(step));
      const controls = document.createElement('div'); controls.className = 'stepper-controls';
      controls.innerHTML = '<button class="btn btn-small" type="button">← Back</button><button class="btn btn-small btn-primary" type="button">Next step →</button><span></span>';
      const [back, next, count] = controls.children;
      const nodes = steps.map((step, index) => { const node = document.createElement('button'); node.type = 'button'; node.className = 'stepper-node'; node.innerHTML = `<b>${index + 1}</b>${esc(step.dataset.label || '')}`; node.addEventListener('click', () => show(index)); track.appendChild(node); return node; });
      function show(index) { current = index; steps.forEach((step, i) => step.classList.toggle('is-current', i === index)); nodes.forEach((node, i) => { node.classList.toggle('is-current', i === index); node.classList.toggle('is-past', i < index); }); back.disabled = index === 0; next.disabled = index === steps.length - 1; count.textContent = `Step ${index + 1} of ${steps.length}`; }
      back.addEventListener('click', () => show(current - 1)); next.addEventListener('click', () => show(current + 1));
      element.classList.add('stepper'); element.append(track, panel, controls); show(0);
    });
  }

  /* ---------- Active recall checks ---------- */

  function initChecks() {
    document.querySelectorAll('[data-check]').forEach((exercise, exerciseIndex) => {
      const options = [...exercise.querySelectorAll('[data-option]')];
      const feedback = exercise.querySelector('[data-feedback]');
      const explanation = exercise.dataset.explain || '';
      options.forEach((option, optionIndex) => {
        option.type = 'button';
        option.addEventListener('click', () => {
          if (exercise.dataset.answered) return;
          exercise.dataset.answered = 'true';
          const correct = option.hasAttribute('data-correct');
          exercise.classList.add(correct ? 'is-correct' : 'is-wrong');
          options.forEach((item) => {
            item.disabled = true;
            if (item.hasAttribute('data-correct')) item.classList.add('is-ok');
          });
          if (!correct) option.classList.add('is-bad');
          if (feedback) {
            feedback.className = `ex-feedback ${correct ? 'ok' : 'bad'}`;
            feedback.innerHTML = `<b>${correct ? 'Correct.' : 'Not quite.'}</b> ${explanation}`;
          }
          exercise.dispatchEvent(new CustomEvent('recallanswered', { bubbles: true, detail: { correct, exerciseIndex, optionIndex } }));
        });
      });
    });
  }

  window.CICDKT = { MODULES, store, setDone, doneList };
  document.addEventListener('DOMContentLoaded', () => { renderEyebrow(); renderCards(); renderSidebar(); renderPager(); enhanceCode(); initSteppers(); initChecks(); loadMermaid(); });
})();
