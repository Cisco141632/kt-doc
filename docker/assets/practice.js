/* Docker learning path — exercise engine.
   Renders the exercises from exercises.js into every [data-exercises] element and checks the answers.
   Three kinds: "command" (type it), "blank" (fill the gaps in a file), "choice" (pick one). */
(function () {
  'use strict';

  const KT = window.DockerKT;
  const SOLVED_KEY = 'docker-kt-solved';
  const TYPE_LABELS = { command: 'Type the command', blank: 'Fill in the blank', choice: 'Scenario' };

  // Long and short spellings of the same option count as the same answer.
  const ALIASES = {
    '--detach': '-d', '--publish': '-p', '--all': '-a', '--follow': '-f', '--force': '-f', '--file': '-f',
    '--volume': '-v', '--volumes': '-v', '--env': '-e', '--tag': '-t', '--tty': '-t', '--interactive': '-i',
    '--memory': '-m', '--quiet': '-q',
  };

  /* ---------- Checking a typed command ---------- */

  // "docker run -dp 8080:80 --name=web nginx" → ["docker","run","-d","-p","8080:80","--name","web","nginx"]
  function tokens(command) {
    const list = String(command).trim()
      .replace(/^\$\s*/, '')
      .replace(/^sudo\s+/, '')
      .replace(/["']/g, '')
      .split(/\s+/)
      .filter(Boolean);
    if (list[0] === 'docker-compose') list.splice(0, 1, 'docker', 'compose');
    return list.flatMap((token) => {
      if (/^--[\w-]+=/.test(token)) {
        const cut = token.indexOf('=');
        return [token.slice(0, cut), token.slice(cut + 1)];
      }
      if (/^-[a-zA-Z]{2,}$/.test(token)) return token.slice(1).split('').map((letter) => '-' + letter);
      return [token];
    }).map((token) => ALIASES[token] || token);
  }

  // An answer is either an exact string, or { head, opts, tail }: the options in "opts" may be typed in any order.
  function matches(user, answer) {
    const typed = tokens(user);
    if (typeof answer === 'string') return typed.join(' ') === tokens(answer).join(' ');

    const head = tokens(answer.head);
    const tail = tokens(answer.tail || '');
    const groups = (answer.opts || []).map(tokens);
    const middleLength = groups.reduce((sum, group) => sum + group.length, 0);
    if (typed.length !== head.length + middleLength + tail.length) return false;
    if (typed.slice(0, head.length).join(' ') !== head.join(' ')) return false;
    if (typed.slice(typed.length - tail.length).join(' ') !== tail.join(' ')) return false;

    let rest = typed.slice(head.length, typed.length - tail.length);
    const unused = groups.slice();
    while (rest.length) {
      const found = unused.findIndex((group) => group.join(' ') === rest.slice(0, group.length).join(' '));
      if (found < 0) return false;
      rest = rest.slice(unused[found].length);
      unused.splice(found, 1);
    }
    return unused.length === 0;
  }

  function canonical(answer) {
    if (typeof answer === 'string') return answer;
    return [answer.head].concat(answer.opts || [], answer.tail || []).filter(Boolean).join(' ');
  }

  // Tells the learner which pieces are missing or not needed, without giving the whole answer away.
  function difference(user, answer) {
    const typed = tokens(user);
    const wanted = tokens(canonical(answer));
    const missing = wanted.slice();
    const extra = [];
    typed.forEach((token) => {
      const at = missing.indexOf(token);
      if (at >= 0) missing.splice(at, 1);
      else extra.push(token);
    });
    const code = (list) => list.map((token) => `<code>${KT.esc(token)}</code>`).join(' ');
    if (!missing.length && !extra.length) return 'You have all the right pieces, but the order is wrong. Options go before the image or container name.';
    const parts = [];
    if (missing.length && missing.length <= 3) parts.push(`Missing: ${code(missing)}`);
    else if (missing.length) parts.push(`${missing.length} pieces are missing`);
    if (extra.length && extra.length <= 3) parts.push(`Not expected: ${code(extra)}`);
    else if (extra.length) parts.push(`${extra.length} pieces are not expected`);
    return parts.join(' · ') + '.';
  }

  /* ---------- Solved state ---------- */

  function solvedList() { return KT.store.get(SOLVED_KEY, []); }

  function markSolved(id) {
    const list = solvedList();
    if (!list.includes(id)) {
      list.push(id);
      KT.store.set(SOLVED_KEY, list);
    }
  }

  /* ---------- Rendering one exercise ---------- */

  function moduleTitle(id) {
    const found = KT.MODULES.find((m) => m.id === id);
    return found ? found.title : '';
  }

  function buildExercise(ex, onSolved) {
    const card = document.createElement('div');
    card.className = 'exercise';
    card.dataset.module = ex.module;
    card.dataset.type = ex.type;
    card.innerHTML = `
      <div class="ex-head">
        <span class="badge info">${TYPE_LABELS[ex.type]}</span>
        <span>${KT.esc(moduleTitle(ex.module))}</span>
        <span class="badge ok" data-solved hidden>Solved</span>
      </div>
      <p class="ex-q">${ex.q}</p>
      <div data-body></div>
      <div class="ex-actions"></div>
      <div class="ex-feedback" aria-live="polite"></div>`;
    const body = card.querySelector('[data-body]');
    const actions = card.querySelector('.ex-actions');
    const feedback = card.querySelector('.ex-feedback');
    const solvedBadge = card.querySelector('[data-solved]');
    if (solvedList().includes(ex.id)) solvedBadge.hidden = false;

    function say(kind, html) {
      feedback.className = 'ex-feedback ' + kind;
      feedback.innerHTML = html;
      card.classList.toggle('is-correct', kind === 'ok');
      card.classList.toggle('is-wrong', kind === 'bad');
    }

    function correct(extraNote) {
      say('ok', `<b>Correct.</b> ${ex.why || ''}${extraNote || ''}`);
      solvedBadge.hidden = false;
      markSolved(ex.id);
      onSolved();
    }

    function addButton(label, onClick) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'btn btn-small';
      button.textContent = label;
      button.addEventListener('click', onClick);
      actions.appendChild(button);
    }

    if (ex.type === 'command') {
      const answers = [ex.answer].concat(ex.also || []);
      body.innerHTML = `
        <form class="ex-input">
          <label class="field"><span>$</span><input type="text" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" aria-label="Type your command" placeholder="type the command, then press Enter"></label>
          <button class="btn btn-primary" type="submit">Check</button>
        </form>`;
      const input = body.querySelector('input');
      body.querySelector('form').addEventListener('submit', (event) => {
        event.preventDefault();
        const typed = input.value;
        if (!typed.trim()) return say('hint', 'Type a command first.');
        if (answers.some((answer) => matches(typed, answer))) {
          const legacy = /^\s*(sudo\s+)?docker-compose\b/.test(typed);
          return correct(legacy ? ' <i>Note: <code>docker-compose</code> with a hyphen is the old tool. Today it is <code>docker compose</code> with a space.</i>' : '');
        }
        say('bad', `<b>Not yet.</b> ${difference(typed, ex.answer)}`);
      });
      addButton('Show answer', () => say('hint', `<b>Answer:</b> <code>${KT.esc(canonical(ex.answer))}</code><br>${ex.why || ''}`));
    }

    if (ex.type === 'blank') {
      const width = (blank) => Math.max(...blank.a.map((text) => text.length)) + 2;
      const html = KT.esc(ex.code).replace(/\[\[(\d+)\]\]/g, (all, n) =>
        `<input type="text" data-blank="${n}" size="${width(ex.blanks[n])}" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" aria-label="Blank ${Number(n) + 1}">`);
      body.innerHTML = `<pre class="ex-code">${html}</pre>`;
      const inputs = [...body.querySelectorAll('input')];
      const clean = (text, blank) => {
        const value = text.trim().replace(/\s+/g, ' ');
        return blank.ci ? value.toLowerCase() : value;
      };
      const check = () => {
        let right = 0;
        inputs.forEach((input) => {
          const blank = ex.blanks[input.dataset.blank];
          const ok = blank.a.some((accepted) => clean(accepted, blank) === clean(input.value, blank));
          input.classList.toggle('is-ok', ok);
          input.classList.toggle('is-bad', !ok);
          if (ok) right += 1;
        });
        if (right === inputs.length) correct();
        else say('bad', `<b>${right} of ${inputs.length} correct.</b> Fix the red ones and check again.`);
      };
      inputs.forEach((input) => input.addEventListener('keydown', (event) => { if (event.key === 'Enter') check(); }));
      addButton('Check', check);
      actions.lastChild.classList.add('btn-primary');
      addButton('Show answer', () => {
        inputs.forEach((input) => { input.value = ex.blanks[input.dataset.blank].a[0]; input.classList.remove('is-bad'); });
        say('hint', `<b>Filled in for you.</b> ${ex.why || ''}`);
      });
    }

    if (ex.type === 'choice') {
      body.innerHTML = `<div class="ex-options">${ex.options.map((option) => `<button type="button">${option}</button>`).join('')}</div>`;
      const buttons = [...body.querySelectorAll('button')];
      buttons.forEach((button, i) => button.addEventListener('click', () => {
        buttons.forEach((b) => { b.disabled = true; });
        buttons[ex.correct].classList.add('is-ok');
        if (i === ex.correct) return correct();
        button.classList.add('is-bad');
        say('bad', `<b>Not quite.</b> ${ex.why || ''}`);
        addButton('Try again', () => {
          buttons.forEach((b) => { b.disabled = false; b.classList.remove('is-ok', 'is-bad'); });
          say('', '');
          actions.lastChild.remove();
        });
      }));
    }

    if (ex.hint) {
      const hintButton = document.createElement('button');
      hintButton.type = 'button';
      hintButton.className = 'btn btn-small';
      hintButton.textContent = 'Hint';
      hintButton.addEventListener('click', () => say('hint', `<b>Hint:</b> ${ex.hint}`));
      actions.prepend(hintButton);
    }
    return card;
  }

  /* ---------- Rendering a list of exercises ---------- */

  function initContainer(box) {
    const wanted = box.dataset.exercises;
    const all = (window.DOCKER_EXERCISES || []).filter((ex) => wanted === 'all' || ex.module === wanted);
    if (!all.length) return;
    const isLab = wanted === 'all';
    let moduleFilter = 'all';
    let typeFilter = 'all';

    const filters = document.createElement('div');
    const list = document.createElement('div');
    const score = document.createElement('div');
    score.className = 'ex-score' + (isLab ? ' is-sticky' : '');
    box.append(filters, list, score);

    function renderScore() {
      const solved = solvedList();
      const count = all.filter((ex) => solved.includes(ex.id)).length;
      const pct = Math.round((count / all.length) * 100);
      score.innerHTML = `<b>${count} of ${all.length} solved</b><div class="progress-bar"><span style="width:${pct}%"></span></div>`;
      if (isLab) {
        const reset = document.createElement('button');
        reset.type = 'button';
        reset.className = 'btn btn-small';
        reset.textContent = 'Reset my progress';
        reset.addEventListener('click', () => {
          KT.store.set(SOLVED_KEY, []);
          renderList();
        });
        score.appendChild(reset);
        if (count === all.length) KT.setDone('practice', true);
      }
    }

    function renderList() {
      list.innerHTML = '';
      const shown = all.filter((ex) => (moduleFilter === 'all' || ex.module === moduleFilter) && (typeFilter === 'all' || ex.type === typeFilter));
      shown.forEach((ex) => list.appendChild(buildExercise(ex, renderScore)));
      if (!shown.length) list.innerHTML = '<p>No exercises match these filters.</p>';
      renderScore();
    }

    function renderFilters() {
      if (!isLab) return;
      const modules = [['all', 'All topics']].concat(KT.MODULES.filter((m) => all.some((ex) => ex.module === m.id)).map((m) => [m.id, m.title]));
      const types = [['all', 'All kinds']].concat(Object.keys(TYPE_LABELS).map((key) => [key, TYPE_LABELS[key]]));
      filters.innerHTML = '';
      [[modules, moduleFilter, (v) => { moduleFilter = v; }], [types, typeFilter, (v) => { typeFilter = v; }]].forEach(([options, current, pick]) => {
        const row = document.createElement('div');
        row.className = 'filter-row';
        options.forEach(([value, label]) => {
          const button = document.createElement('button');
          button.type = 'button';
          button.className = 'btn btn-small' + (value === current ? ' is-on' : '');
          button.textContent = label;
          button.addEventListener('click', () => { pick(value); renderFilters(); renderList(); });
          row.appendChild(button);
        });
        filters.appendChild(row);
      });
    }

    renderFilters();
    renderList();
  }

  // Exposed so the answer checker itself can be tested.
  window.DockerPractice = { matches, tokens, canonical };

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-exercises]').forEach(initContainer);
  });
})();
