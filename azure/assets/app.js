/* Browser-local learning state and accessible course interactions. No network calls. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const data = window.AZURE_DATA;
  if (!data) return;
  const KEY = 'azure-storage-learning-v1';
  const THEME = 'azure-storage-learning-theme';
  const lessonIds = new Set(data.lessonIds);
  const labIds = new Set(data.labIds);
  const questionMap = new Map(data.questions.map(q => [q.id, q]));
  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c]));
  const blank = () => ({version: 1, done: [], labs: [], answers: {}});
  let storageUnavailable = false;
  function normalize(value) {
    if (!value || value.version !== 1 || !Array.isArray(value.done) || !Array.isArray(value.labs) || !value.answers || typeof value.answers !== 'object' || Array.isArray(value.answers)) throw new Error('This is not an Azure Storage course progress file (version 1).');
    const result = blank();
    result.done = [...new Set(value.done.filter(x => lessonIds.has(x)))];
    result.labs = [...new Set(value.labs.filter(x => labIds.has(x)))];
    for (const [id, answer] of Object.entries(value.answers)) {
      const q = questionMap.get(id);
      if (q && Number.isInteger(answer) && answer >= 0 && answer < q.options.length) result.answers[id] = answer;
    }
    return result;
  }
  function read() {
    try {
      const raw = localStorage.getItem(KEY);
      return raw ? normalize(JSON.parse(raw)) : blank();
    } catch {
      storageUnavailable = true;
      return blank();
    }
  }
  let state = read();
  function warning() {
    if (!storageUnavailable) return;
    const target = $('#storage-status');
    if (target) {
      target.hidden = false;
      target.textContent = 'Progress could not be loaded or saved in this browser. You can keep learning during this visit; export a backup before leaving.';
    }
  }
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); }
    catch { storageUnavailable = true; warning(); }
    updateProgress();
  }
  function updateProgress() {
    const done = new Set(state.done);
    if ($('#course-meter')) $('#course-meter').value = done.size;
    if ($('#course-progress')) $('#course-progress').textContent = `${done.size} of ${data.lessonIds.length} lessons complete`;
    $$('[data-nav-item]').forEach(item => item.classList.toggle('is-done', done.has(item.dataset.navItem)));
    const current = document.body.dataset.module;
    const mark = $('#mark-done');
    if (mark) {
      mark.textContent = done.has(current) ? 'Lesson complete ✓ · Undo' : 'Mark lesson complete';
      mark.setAttribute('aria-pressed', String(done.has(current)));
    }
    const resume = $('#resume-course');
    if (resume) {
      const next = data.lessonIds.find(id => !done.has(id));
      resume.href = next ? next + '.html' : 'quiz.html';
      resume.textContent = next ? (done.size ? 'Continue lesson ' : 'Start lesson ') + String(data.lessonIds.indexOf(next) + 1).padStart(2, '0') + ' →' : 'All lessons complete · Try the quiz →';
    }
    if ($('#lab-progress')) $('#lab-progress').textContent = `${state.labs.length} of ${data.labIds.length} lab milestones explored`;
    $$('[data-lab-badge]').forEach(badge => {
      const complete = state.labs.includes(badge.dataset.labBadge);
      badge.textContent = complete ? 'Milestone explored ✓' : 'Ready to explore';
      badge.classList.toggle('is-success', complete);
    });
  }
  function initialize() {
    warning();
    try {
      const storedTheme = localStorage.getItem(THEME);
      if (storedTheme === 'dark' || storedTheme === 'light') document.documentElement.dataset.theme = storedTheme;
      else if (window.matchMedia('(prefers-color-scheme: dark)').matches) document.documentElement.dataset.theme = 'dark';
    } catch { /* Reading does not require storage. */ }
    $('.theme-toggle')?.addEventListener('click', () => {
      const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = theme;
      try { localStorage.setItem(THEME, theme); } catch { /* Theme still changes for this visit. */ }
    });
    $('#menu-toggle')?.addEventListener('click', event => {
      const expanded = event.currentTarget.getAttribute('aria-expanded') !== 'true';
      event.currentTarget.setAttribute('aria-expanded', String(expanded));
      $('#sidebar').classList.toggle('is-open', expanded);
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && $('#menu-toggle')?.getAttribute('aria-expanded') === 'true') {
        $('#menu-toggle').click();
        $('#menu-toggle').focus();
      }
    });
    $('#nav-search')?.addEventListener('input', event => {
      const search = event.currentTarget.value.trim().toLowerCase();
      let count = 0;
      $$('[data-nav-item]').forEach(item => {
        item.hidden = !(item.dataset.navItem + ' ' + item.textContent).toLowerCase().includes(search);
        if (!item.hidden) count++;
      });
      $('#nav-empty').hidden = count > 0;
    });
    $('#mark-done')?.addEventListener('click', () => {
      const id = document.body.dataset.module;
      if (!lessonIds.has(id)) return;
      state.done = state.done.includes(id) ? state.done.filter(x => x !== id) : [...state.done, id];
      save();
    });
    document.addEventListener('azure:lab-complete', event => {
      const id = event.detail?.id;
      if (labIds.has(id) && !state.labs.includes(id)) {
        state.labs.push(id);
        save();
      }
    });
    $('#glossary-search')?.addEventListener('input', event => {
      const text = event.currentTarget.value.toLowerCase().trim();
      let count = 0;
      $$('[data-glossary]').forEach(entry => {
        entry.hidden = !entry.textContent.toLowerCase().includes(text);
        if (!entry.hidden) count++;
      });
      $('#glossary-count').textContent = `${count} matching term${count === 1 ? '' : 's'}`;
      $('#glossary-empty').hidden = count > 0;
    });
    initializeQuiz();
    initializeLessonChecks();
    initializeBackups();
    initializeCodeCopy();
    updateProgress();
  }

  function questionHTML(q, namespace, answer) {
    const answered = Number.isInteger(answer);
    return `<div class="question"><form><fieldset><legend>${escape(q.prompt)}</legend>${q.options.map((option, i) => `<label class="answer${answered && i === q.correct ? ' correct' : answered && i === answer ? ' incorrect' : ''}"><input type="radio" name="${namespace}" value="${i}"${answer === i ? ' checked' : ''}${answered ? ' disabled' : ''}><span>${escape(option.text)}</span></label>`).join('')}</fieldset><div class="actions"><button class="btn btn-primary" type="submit"${answered ? ' disabled' : ''}>Check answer</button>${answered ? '<button class="btn" type="button" data-retry>Try again</button>' : ''}<a href="${q.topic}.html">Review lesson</a></div><p class="feedback" role="status" aria-live="polite">${answered ? answerFeedback(q, answer) : ''}</p></form></div>`;
  }
  function answerFeedback(q, answer) {
    return `<strong>${answer === q.correct ? 'Correct.' : 'Not quite.'}</strong> ${escape(q.options[answer].why)}${answer !== q.correct ? '<br><strong>Best answer:</strong> ' + escape(q.options[q.correct].text) + ' ' + escape(q.options[q.correct].why) : ''}`;
  }
  function bindQuestion(container, q, render) {
    container.querySelector('form').addEventListener('submit', event => {
      event.preventDefault();
      if (Number.isInteger(state.answers[q.id])) return;
      const chosen = container.querySelector('input:checked');
      if (!chosen) {
        container.querySelector('.feedback').textContent = 'Choose an answer before checking.';
        return;
      }
      state.answers[q.id] = Number(chosen.value);
      save();
      render();
      container.querySelector('[data-retry]')?.focus({preventScroll: true});
    });
    container.querySelector('[data-retry]')?.addEventListener('click', () => {
      delete state.answers[q.id];
      save();
      render();
      container.querySelector('input')?.focus({preventScroll: true});
    });
  }
  function initializeLessonChecks() {
    $$('[data-lesson-check]').forEach((mount, sectionIndex) => {
      const qs = data.questions.filter(q => q.topic === mount.dataset.lessonCheck).slice(0, 2);
      qs.forEach((q, i) => {
        const container = document.createElement('div');
        mount.append(container);
        const render = () => {
          container.innerHTML = questionHTML(q, `lesson-${sectionIndex}-${i}`, state.answers[q.id]);
          bindQuestion(container, q, render);
        };
        render();
      });
    });
  }
  function initializeQuiz() {
    if (!$('#quiz-app')) return;
    let pool = [];
    let position = 0;
    function selectPool() {
      const topic = $('#quiz-topic').value;
      const mode = $('#quiz-mode').value;
      pool = data.questions.filter(q => (topic === 'all' || q.topic === topic) && (mode === 'all' || (mode === 'unanswered' ? !Number.isInteger(state.answers[q.id]) : Number.isInteger(state.answers[q.id]) && state.answers[q.id] !== q.correct)));
      position = 0;
      render();
    }
    function render() {
      const filtered = data.questions.filter(q => $('#quiz-topic').value === 'all' || q.topic === $('#quiz-topic').value);
      const answered = filtered.filter(q => Number.isInteger(state.answers[q.id]));
      const correct = answered.filter(q => state.answers[q.id] === q.correct).length;
      $('#quiz-score').textContent = `${correct} correct / ${answered.length} answered · ${filtered.length} questions in this topic`;
      $('#quiz-prev').disabled = position === 0 || !pool.length;
      $('#quiz-next').disabled = position >= pool.length - 1;
      const mount = $('#quiz-card');
      if (!pool.length) {
        mount.innerHTML = '<p class="empty">No questions in this set. Choose All questions or another topic.</p>';
        $('#quiz-position').textContent = '0 questions in this set';
        return;
      }
      const q = pool[position];
      $('#quiz-position').textContent = `Question ${position + 1} of ${pool.length} in this set`;
      mount.innerHTML = questionHTML(q, 'quiz-answer', state.answers[q.id]);
      bindQuestion(mount, q, render);
    }
    $('#quiz-topic').addEventListener('change', selectPool);
    $('#quiz-mode').addEventListener('change', selectPool);
    $('#quiz-prev').addEventListener('click', () => { if (position > 0) { position--; render(); } });
    $('#quiz-next').addEventListener('click', () => { if (position + 1 < pool.length) { position++; render(); } });
    selectPool();
  }
  function initializeBackups() {
    const status = message => { if ($('#progress-status')) $('#progress-status').textContent = message; };
    $('#export-progress')?.addEventListener('click', () => {
      const blob = new Blob([JSON.stringify({...state, course: 'azure-storage', exportedAt: new Date().toISOString()}, null, 2)], {type: 'application/json'});
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'azure-storage-progress.json';
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      status('Exported your current progress. Keep the JSON file to restore it later.');
    });
    $('#import-progress')?.addEventListener('change', async event => {
      const input = event.currentTarget;
      const file = input.files?.[0];
      if (!file) return;
      try {
        if (file.size > 256 * 1024) throw new Error('Progress files must be smaller than 256 KB.');
        const value = JSON.parse(await file.text());
        if (value.course !== 'azure-storage') throw new Error('Choose an Azure Storage progress export.');
        state = normalize(value);
        save();
        status('Imported progress. Lesson, lab and quiz records have been restored.');
      } catch (error) { status('Import failed: ' + error.message); }
      input.value = '';
    });
    $('#reset-progress')?.addEventListener('click', () => {
      if (!window.confirm('Reset Azure Storage lesson completion, lab milestones and quiz answers?')) return;
      state = blank();
      save();
      status('Learning progress reset for this course.');
    });
  }
  function initializeCodeCopy() {
    $$('.snippet').forEach(snippet => {
      const code = snippet.querySelector('pre code') || snippet.querySelector('pre');
      if (!code) return;
      let caption = snippet.querySelector('.code-caption');
      if (!caption) {
        caption = document.createElement('div');
        caption.className = 'code-caption';
        snippet.prepend(caption);
      }
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'btn btn-small';
      button.textContent = 'Copy example';
      button.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(code.textContent);
          button.textContent = 'Copied ✓';
        } catch { button.textContent = 'Select the example to copy'; }
        setTimeout(() => { button.textContent = 'Copy example'; }, 2500);
      });
      caption.append(button);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, {once: true});
  else initialize();
})();
