/* Docker learning path — shared behaviour for every page.
   Loaded in <head> so the theme is applied before the page paints. */
(function () {
  'use strict';

  // Single source of truth for navigation. To add a page, add one line here.
  const MODULES = [
    { id: 'index', file: 'index.html', title: 'What is Docker?', mins: 10, desc: 'The idea, the four key words, containers vs virtual machines, and your first container.' },
    { id: 'commands', file: 'commands.html', title: 'Everyday commands', mins: 20, desc: 'Every daily command explained with one simple example.' },
    { id: 'dockerfile', file: 'dockerfile.html', title: 'Build your own image', mins: 25, desc: 'Write a Dockerfile, understand layers and caching, and use multi-stage builds.' },
    { id: 'rebuild', file: 'rebuild.html', title: 'Change, build, run', mins: 15, desc: 'What really happens when you change code, build again, restart or run again.' },
    { id: 'storage-network', file: 'storage-network.html', title: 'Data & networking', mins: 20, desc: 'Volumes, bind mounts, ports, and how containers talk to each other.' },
    { id: 'compose', file: 'compose.html', title: 'Docker Compose', mins: 20, desc: 'Run an app and its database together from one file.' },
    { id: 'pipeline', file: 'pipeline.html', title: 'From laptop to production', mins: 20, desc: 'Registries, versions, deploys and rollbacks: how an image reaches a real server.' },
    { id: 'real-world', file: 'real-world.html', title: 'Real-world issues', mins: 20, desc: 'Problems teams really hit in production, and how to fix and prevent them.' },
    { id: 'practice', file: 'practice.html', title: 'Practice lab', mins: 30, desc: 'Type the command or fill in the blank, then check your answer.' },
    { id: 'quiz', file: 'quiz.html', title: 'Quiz', mins: 20, desc: 'Short tests for each topic, with an explanation after every question.' },
    { id: 'cheatsheet', file: 'cheatsheet.html', title: 'Cheat sheet', mins: 5, desc: 'All commands on one page, plus quick fixes for common errors.' },
  ];

  const THEME_KEY = 'docker-kt-theme';
  const DONE_KEY = 'docker-kt-done';
  const MERMAID_SRC = 'https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.min.js';
  const LANG_LABELS = { sh: 'Terminal', console: 'Terminal', dockerfile: 'Dockerfile', yaml: 'YAML', python: 'Python', text: 'Text', json: 'JSON' };

  const root = document.documentElement;
  root.classList.add('js');

  // localStorage can throw (private windows, blocked site data). The pages must work without it.
  const store = {
    get(key, fallback) {
      try {
        const raw = localStorage.getItem(key);
        return raw === null ? fallback : JSON.parse(raw);
      } catch (e) {
        return fallback;
      }
    },
    set(key, value) {
      try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* not saved, page still works */ }
    },
  };

  function esc(text) {
    return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  const systemDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  root.dataset.theme = store.get(THEME_KEY, null) || (systemDark ? 'dark' : 'light');

  // The tab icon is set here once for every page, so the browser does not ask the server for /favicon.ico.
  const icon = document.createElement('link');
  icon.rel = 'icon';
  icon.href = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230a66c2'/%3E%3Ctext x='16' y='23' font-family='Arial,sans-serif' font-size='20' font-weight='700' text-anchor='middle' fill='white'%3ED%3C/text%3E%3C/svg%3E";
  document.head.appendChild(icon);

  /* ---------- Progress ---------- */

  function doneList() {
    const known = MODULES.map((m) => m.id);
    return store.get(DONE_KEY, []).filter((id) => known.includes(id));
  }

  function setDone(id, isDone) {
    const list = doneList().filter((x) => x !== id);
    if (isDone) list.push(id);
    store.set(DONE_KEY, list);
    renderSidebar();
    renderPager();
  }

  /* ---------- Sidebar ---------- */

  function activeId() { return document.body.dataset.module || ''; }

  function renderSidebar() {
    const side = document.getElementById('sidebar');
    if (!side) return;
    const active = activeId();
    const done = doneList();
    const items = MODULES.map((m, i) => {
      const isActive = m.id === active;
      const isDone = done.includes(m.id);
      const cls = [isActive ? 'is-active' : '', isDone ? 'is-done' : ''].join(' ').trim();
      return `<li class="${cls}">
        <a href="${m.file}"${isActive ? ' aria-current="page"' : ''}>
          <span class="num">${isDone ? '✓' : i + 1}</span>
          <span class="t">${esc(m.title)}</span>
          <span class="mins">${m.mins} min</span>
        </a>${isActive ? '<ul class="toc"></ul>' : ''}
      </li>`;
    }).join('');
    const pct = Math.round((done.length / MODULES.length) * 100);
    side.innerHTML = `
      <a class="brand" href="index.html">
        <span class="brand-mark" aria-hidden="true">D</span>
        <span>Docker learning path<small>From zero to running your own stack</small></span>
      </a>
      <div class="progress">
        <div class="progress-bar"><span style="width:${pct}%"></span></div>
        ${done.length} of ${MODULES.length} modules done
      </div>
      <nav aria-label="Modules"><ol class="modules">${items}</ol></nav>
      <button class="btn btn-small theme-toggle" type="button">${root.dataset.theme === 'dark' ? 'Light theme' : 'Dark theme'}</button>`;

    const toc = side.querySelector('.toc');
    if (toc) {
      document.querySelectorAll('main section[id] > h2').forEach((h2) => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = '#' + h2.parentElement.id;
        a.textContent = h2.textContent;
        li.appendChild(a);
        toc.appendChild(li);
      });
    }

    side.querySelector('.theme-toggle').addEventListener('click', () => {
      root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
      store.set(THEME_KEY, root.dataset.theme);
      renderSidebar();
      renderMermaid();
    });
  }

  /* ---------- Page head and pager ---------- */

  function renderEyebrow() {
    const head = document.querySelector('.page-head');
    const index = MODULES.findIndex((m) => m.id === activeId());
    if (!head || index < 0) return;
    const p = document.createElement('p');
    p.className = 'eyebrow';
    p.textContent = `Module ${index + 1} of ${MODULES.length} · about ${MODULES[index].mins} minutes`;
    head.prepend(p);
  }

  function renderPager() {
    const main = document.querySelector('main');
    const index = MODULES.findIndex((m) => m.id === activeId());
    if (!main || index < 0) return;
    let pager = main.querySelector('.pager');
    if (!pager) {
      pager = document.createElement('footer');
      pager.className = 'pager';
      main.appendChild(pager);
    }
    const prev = MODULES[index - 1];
    const next = MODULES[index + 1];
    const isDone = doneList().includes(MODULES[index].id);
    pager.innerHTML = `
      ${prev ? `<a class="btn" href="${prev.file}">← ${esc(prev.title)}</a>` : ''}
      <span class="spacer"></span>
      <button class="btn${isDone ? ' is-on' : ''}" type="button" data-done>${isDone ? '✓ Done (click to undo)' : 'Mark module as done'}</button>
      ${next ? `<a class="btn btn-primary" href="${next.file}">Next: ${esc(next.title)} →</a>` : ''}`;
    pager.querySelector('[data-done]').addEventListener('click', () => setDone(MODULES[index].id, !isDone));
  }

  function renderModuleCards() {
    const box = document.querySelector('[data-module-cards]');
    if (!box) return;
    box.innerHTML = MODULES.map((m, i) => `
      <a class="card" href="${m.file}">
        <span class="tag">Module ${i + 1} · ${m.mins} min</span>
        <b>${esc(m.title)}</b>
        <small>${esc(m.desc)}</small>
      </a>`).join('');
  }

  /* ---------- Code blocks: light highlighting + copy button ---------- */

  function highlight(text, lang) {
    let inCommand = false;
    return text.split('\n').map((line) => {
      if (lang === 'console') {
        const isCommand = line.startsWith('$ ') || inCommand;
        const hadPrompt = line.startsWith('$ ');
        inCommand = isCommand && line.endsWith('\\');
        if (!isCommand) return `<span class="tok-out">${esc(line)}</span>`;
        return hadPrompt ? `<span class="tok-prompt">$ </span>${esc(line.slice(2))}` : esc(line);
      }
      if (/^\s*#/.test(line)) return `<span class="tok-com">${esc(line)}</span>`;
      let html = esc(line);
      if (lang === 'dockerfile') html = html.replace(/^([A-Z]+)(?=\s)/, '<span class="tok-key">$1</span>');
      if (lang === 'yaml') html = html.replace(/^(\s*(?:- )?)([\w.-]+)(:)(?=\s|$)/, '$1<span class="tok-key">$2</span>$3');
      return html.replace(/(\s)(#\s.*)$/, '$1<span class="tok-com">$2</span>');
    }).join('\n');
  }

  // In a "console" block only the lines you type are copied, not the sample output.
  function copyText(text, lang) {
    if (lang !== 'console') return text;
    const out = [];
    let inCommand = false;
    text.split('\n').forEach((line) => {
      if (line.startsWith('$ ')) out.push(line.slice(2));
      else if (inCommand) out.push(line);
      else return;
      inCommand = line.endsWith('\\');
    });
    return out.join('\n');
  }

  function copy(text, button) {
    const done = () => {
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = 'Copy'; }, 1500);
    };
    const fallback = () => {
      const area = document.createElement('textarea');
      area.value = text;
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      try { document.execCommand('copy'); done(); } catch (e) { button.textContent = 'Press Ctrl+C'; }
      area.remove();
    };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fallback);
    else fallback();
  }

  function enhanceCode(scope) {
    (scope || document).querySelectorAll('pre[data-lang]').forEach((pre) => {
      if (pre.dataset.enhanced) return;
      pre.dataset.enhanced = '1';
      const lang = pre.dataset.lang;
      const text = pre.textContent.replace(/\s+$/, '');
      pre.innerHTML = highlight(text, lang);

      const wrap = document.createElement('div');
      wrap.className = 'code';
      const head = document.createElement('div');
      head.className = 'code-head';
      const label = document.createElement('span');
      label.textContent = pre.dataset.title || LANG_LABELS[lang] || lang;
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = 'Copy';
      button.addEventListener('click', () => copy(copyText(text, lang), button));
      head.append(label, button);
      pre.replaceWith(wrap);
      wrap.append(head, pre);
    });
  }

  /* ---------- Mermaid diagrams ---------- */

  let mermaidReady = false;

  function loadMermaid() {
    const blocks = document.querySelectorAll('pre.mermaid');
    if (!blocks.length) return;
    blocks.forEach((block) => { block.dataset.src = block.textContent; });
    const script = document.createElement('script');
    script.src = MERMAID_SRC;
    script.onload = () => { mermaidReady = true; renderMermaid(); };
    script.onerror = () => blocks.forEach((block) => block.classList.add('mermaid-failed'));
    document.head.appendChild(script);
  }

  // Mermaid needs real colour values, so read them from the CSS tokens of the current theme.
  function renderMermaid() {
    if (!mermaidReady || !window.mermaid) return;
    const css = getComputedStyle(root);
    const v = (name) => css.getPropertyValue(name).trim();
    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: 'strict',
      theme: 'base',
      themeVariables: {
        darkMode: root.dataset.theme === 'dark',
        fontFamily: v('--font'),
        fontSize: '15px',
        background: v('--surface'),
        primaryColor: v('--accent-soft'),
        primaryTextColor: v('--text'),
        primaryBorderColor: v('--accent'),
        secondaryColor: v('--surface-2'),
        secondaryTextColor: v('--text'),
        secondaryBorderColor: v('--border'),
        tertiaryColor: v('--surface-2'),
        tertiaryTextColor: v('--text'),
        tertiaryBorderColor: v('--border'),
        lineColor: v('--muted'),
        textColor: v('--text'),
        clusterBkg: v('--surface-2'),
        clusterBorder: v('--border'),
        edgeLabelBackground: v('--surface'),
      },
    });
    const blocks = [...document.querySelectorAll('pre.mermaid')];
    blocks.forEach((block) => {
      block.removeAttribute('data-processed');
      block.classList.remove('mermaid-failed');
      block.textContent = block.dataset.src;
    });
    window.mermaid.run({ nodes: blocks }).catch(() => {
      blocks.filter((block) => !block.querySelector('svg')).forEach((block) => {
        block.textContent = block.dataset.src;
        block.classList.add('mermaid-failed');
      });
    });
  }

  /* ---------- Stepper: click through a flow one step at a time ---------- */

  function initSteppers() {
    document.querySelectorAll('[data-stepper]').forEach((el) => {
      const steps = [...el.querySelectorAll(':scope > .step')];
      if (!steps.length) return;
      let current = 0;

      const track = document.createElement('div');
      track.className = 'stepper-track';
      const panel = document.createElement('div');
      panel.className = 'stepper-panel';
      panel.setAttribute('aria-live', 'polite');
      steps.forEach((step) => panel.appendChild(step));

      const controls = document.createElement('div');
      controls.className = 'stepper-controls';
      controls.innerHTML = '<button class="btn btn-small" type="button">← Back</button><button class="btn btn-small btn-primary" type="button">Next step →</button><span></span>';
      const [back, next, count] = controls.children;

      const nodes = steps.map((step, i) => {
        const node = document.createElement('button');
        node.type = 'button';
        node.className = 'stepper-node';
        node.innerHTML = `<b>${i + 1}</b>${esc(step.dataset.label || '')}`;
        node.addEventListener('click', () => show(i));
        track.appendChild(node);
        return node;
      });

      function show(i) {
        current = i;
        steps.forEach((step, k) => step.classList.toggle('is-current', k === i));
        nodes.forEach((node, k) => {
          node.classList.toggle('is-current', k === i);
          node.classList.toggle('is-past', k < i);
        });
        back.disabled = i === 0;
        next.disabled = i === steps.length - 1;
        count.textContent = `Step ${i + 1} of ${steps.length}`;
      }

      back.addEventListener('click', () => show(current - 1));
      next.addEventListener('click', () => show(current + 1));
      el.classList.add('stepper');
      el.append(track, panel, controls);
      show(0);
    });
  }

  /* ---------- Tabs ---------- */

  function initTabs() {
    document.querySelectorAll('[data-tabs]').forEach((el) => {
      const panels = [...el.querySelectorAll(':scope > .tab-panel')];
      if (!panels.length) return;
      const list = document.createElement('div');
      list.className = 'tab-list';
      const buttons = panels.map((panel, i) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'btn btn-small';
        button.textContent = panel.dataset.label || `Tab ${i + 1}`;
        button.addEventListener('click', () => show(i));
        list.appendChild(button);
        return button;
      });
      function show(i) {
        panels.forEach((panel, k) => panel.classList.toggle('is-current', k === i));
        buttons.forEach((button, k) => button.classList.toggle('is-on', k === i));
      }
      el.classList.add('tabs');
      el.prepend(list);
      show(0);
    });
  }

  /* ---------- Start ---------- */

  window.DockerKT = { MODULES, store, esc, enhanceCode, setDone, doneList };

  document.addEventListener('DOMContentLoaded', () => {
    renderEyebrow();
    renderModuleCards();
    renderSidebar();
    renderPager();
    enhanceCode();
    initSteppers();
    initTabs();
    loadMermaid();
  });
})();
