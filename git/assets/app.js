/* git learning path: optional, offline-first interactive enhancements. */
(function () {
  'use strict';
  const D = window.GIT_DATA;
  if (!D) return;
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => Array.from(root.querySelectorAll(s));
  const esc = (s) => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const KEY = 'git-learning-v1';
  const empty = () => ({version:1, done:[], answers:{}, labs:[], cards:{}, missions:[]});
  let storageOK = true;
  function normalize(raw) {
    if (!raw || raw.version !== 1 || !Array.isArray(raw.done) || !Array.isArray(raw.labs) || !Array.isArray(raw.missions) ||
        !raw.answers || typeof raw.answers !== 'object' || Array.isArray(raw.answers) ||
        !raw.cards || typeof raw.cards !== 'object' || Array.isArray(raw.cards)) throw new Error('Unrecognized progress format.');
    const clean = empty();
    clean.done = D.modules.map(m => m.id).filter(id => raw.done.includes(id));
    clean.labs = D.labSteps.filter(id => raw.labs.includes(id));
    clean.missions = D.exercises.filter(id => raw.missions.includes(id));
    D.questions.forEach(q => {
      if (Object.hasOwn(raw.answers, q.id) && Number.isInteger(raw.answers[q.id]) && raw.answers[q.id] >= 0 && raw.answers[q.id] < q.options.length) clean.answers[q.id] = raw.answers[q.id];
    });
    D.cards.forEach(c => {
      const item = Object.hasOwn(raw.cards, c.id) ? raw.cards[c.id] : null;
      if (item && Number.isInteger(item.streak) && item.streak >= 0 && item.streak <= 5 && Number.isFinite(item.due) && item.due >= 0 && item.due < 8640000000000000) clean.cards[c.id] = {streak:item.streak, due:item.due};
    });
    return clean;
  }
  let state = empty();
  try { const saved = localStorage.getItem(KEY); if (saved) state = normalize(JSON.parse(saved)); } catch (_) { /* Invalid or inaccessible storage must not break lessons. */ }
  function persist() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); }
    catch (_) { storageOK = false; }
    updateProgress();
  }
  function hasAnswer(q) { return Object.hasOwn(state.answers, q.id); }
  function correct(q) { return hasAnswer(q) && state.answers[q.id] === q.correct; }
  const title = id => (D.modules.find(m => m.id === id) || {title:id.replaceAll('-', ' ')}).title;
  window.GitLearning = {
    escape:esc,
    completeMission(id) { if (!state.missions.includes(id)) { state.missions.push(id); persist(); } },
    missionDone(id) { return state.missions.includes(id); }
  };
  document.documentElement.classList.add('js');
  let theme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  try { const saved = localStorage.getItem('git-learning-theme'); if (['dark','light'].includes(saved)) theme = saved; } catch (_) {}
  function applyTheme() {
    document.documentElement.dataset.theme = theme;
    const button = $('.theme-toggle');
    if (button) button.textContent = theme === 'dark' ? 'Light theme' : 'Dark theme';
  }
  applyTheme();
  $('.theme-toggle')?.addEventListener('click', () => {
    theme = theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('git-learning-theme', theme); } catch (_) {}
    applyTheme();
  });
  $('.mobile-menu')?.addEventListener('click', e => {
    const open = $('#sidebar').classList.toggle('is-open');
    e.currentTarget.setAttribute('aria-expanded', String(open));
  });
  const toc = document.createElement('ul');
  toc.className = 'toc';
  $$('main > section[id] > h2').forEach(h => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = '#' + h.parentElement.id;
    a.textContent = h.textContent;
    li.append(a); toc.append(li);
  });
  $('.modules .is-active')?.append(toc);

  function updateProgress() {
    const total = state.done.length;
    if ($('#course-meter')) $('#course-meter').value = total;
    if ($('#course-progress')) $('#course-progress').textContent = total + ' of ' + D.modules.length + ' lessons complete' + (storageOK ? '' : ' · changes saved for this visit only');
    $$('[data-lesson]').forEach((a, i) => {
      const done = state.done.includes(a.dataset.lesson);
      a.parentElement.classList.toggle('is-done', done);
      $('.num', a).textContent = done ? '✓' : i + 1;
    });
    if ($('#mark-done')) {
      const done = state.done.includes(document.body.dataset.module);
      $('#mark-done').textContent = done ? '✓ Completed · undo' : 'Mark lesson complete';
      $('#mark-done').setAttribute('aria-pressed', String(done));
    }
    if ($('#lab-progress')) {
      $('#lab-progress').textContent = state.labs.length + ' of ' + D.labSteps.length + ' steps checked by you';
      $('#lab-meter').max = D.labSteps.length;
      $('#lab-meter').value = state.labs.length;
    }
    if ($('#progress-summary')) $('#progress-summary').textContent = total + '/' + D.modules.length + ' lessons · ' + D.questions.filter(correct).length + '/' + D.questions.length + ' quiz answers correct · ' + state.labs.length + '/' + D.labSteps.length + ' lab steps · ' + state.missions.length + '/' + D.exercises.length + ' interactive exercises · ' + Object.keys(state.cards).length + '/' + D.cards.length + ' cards reviewed';
  }
  $('#mark-done')?.addEventListener('click', () => {
    const id = document.body.dataset.module;
    state.done = state.done.includes(id) ? state.done.filter(x => x !== id) : state.done.concat(id);
    persist();
  });
  $$('[data-lab]').forEach(box => {
    box.checked = state.labs.includes(box.dataset.lab);
    box.addEventListener('change', () => {
      state.labs = state.labs.filter(x => x !== box.dataset.lab);
      if (box.checked) state.labs.push(box.dataset.lab);
      persist();
    });
  });
  // Graceful clipboard fallback also works when served over plain local HTTP.
  $$('.snippet').forEach(snippet => {
    const button = document.createElement('button');
    button.className = 'btn btn-small copy-btn'; button.type = 'button'; button.textContent = 'Copy';
    button.setAttribute('aria-label', 'Copy this code block');
    $('.code-caption', snippet).append(button);
    button.addEventListener('click', async () => {
      const text = $('code', snippet).textContent;
      let copied = false;
      try { await navigator.clipboard.writeText(text); copied = true; } catch (_) {
        const field = document.createElement('textarea');
        field.value = text; field.style.position = 'fixed'; field.style.opacity = '0';
        document.body.append(field); field.select();
        try { copied = document.execCommand('copy'); } catch (_) {}
        field.remove(); button.focus();
      }
      button.textContent = copied ? 'Copied' : 'Select text to copy';
      setTimeout(() => { button.textContent = 'Copy'; }, 2200);
    });
  });
  function questionHTML(q, localAnswers, prefix) {
    const answered = Object.hasOwn(localAnswers, q.id);
    const selected = localAnswers[q.id];
    return '<form class="question" data-question="' + q.id + '"><fieldset><legend>' + esc(q.prompt) + '</legend>' +
      q.options.map((o,i) => '<label class="answer' + (answered && i === q.correct ? ' correct' : answered && i === selected ? ' incorrect' : '') + '"><input type="radio" name="' + prefix + '-' + q.id + '" value="' + i + '"' + (answered ? ' disabled' : '') + (i === selected ? ' checked' : '') + '><span>' + esc(o.text) + '</span></label>').join('') +
      '</fieldset>' + (!answered ? '<button class="btn btn-primary" type="submit">Check answer</button>' : '<p class="meta">Answer saved for this attempt.</p>') +
      '<div class="feedback" role="status" tabindex="-1">' + (answered ? '<b>' + (selected === q.correct ? 'Correct. ' : 'Not quite. ') + '</b>' + esc(q.options[selected].why) + (selected !== q.correct ? '<p><b>Correct answer: ' + esc(q.options[q.correct].text) + '</b><br>' + esc(q.options[q.correct].why) + '</p>' : '') + '<p><a href="' + q.topic + '.html">Review ' + esc(title(q.topic)) + ' →</a></p>' : '') + '</div></form>';
  }
  function bindQuestion(root, q, onAnswer) {
    const form = $('form[data-question]', root);
    form?.addEventListener('submit', e => {
      e.preventDefault();
      const selected = $('input:checked', form);
      if (!selected) { $('.feedback', form).textContent = 'Choose an answer first.'; return; }
      onAnswer(Number(selected.value));
    });
  }
  // Lesson checks are deliberate practice, separate from the scored quiz attempt.
  $$('[data-lesson-check]').forEach(root => {
    D.questions.filter(q => q.topic === root.dataset.lessonCheck).slice(0,2).forEach(q => {
      const card = document.createElement('div'); root.append(card);
      const answers = {};
      const draw = () => {
        card.innerHTML = questionHTML(q, answers, 'lesson');
        bindQuestion(card, q, value => { answers[q.id] = value; draw(); $('.feedback', card).focus(); });
      };
      draw();
    });
  });

  const quiz = $('#quiz');
  if (quiz) {
    const topics = [...new Set(D.questions.map(q => q.topic))];
    quiz.innerHTML = '<div class="filters"><label class="field">Topic<select id="quiz-topic"><option value="all">All ' + topics.length + ' topics</option>' + topics.map(t => '<option value="' + t + '">' + esc(title(t)) + '</option>').join('') + '</select></label><label class="field">Question set<select id="quiz-view"><option value="all">All questions</option><option value="unanswered">Unanswered</option><option value="missed">Missed questions</option></select></label></div><p id="quiz-score" role="status"></p><progress id="quiz-meter" max="' + D.questions.length + '" value="0" aria-label="Questions answered"></progress><p id="quiz-position" class="meta"></p><div id="quiz-card"></div><div class="actions"><button class="btn" id="quiz-prev">← Previous</button><button class="btn" id="quiz-next">Next →</button><button class="btn" id="quiz-retry">Retry missed</button><button class="btn" id="quiz-reset">Fresh attempt</button></div><div id="quiz-breakdown"></div>';
    let index = 0, retryIDs = null, deck = [];
    function getDeck() {
      const topic = $('#quiz-topic').value, view = $('#quiz-view').value;
      return D.questions.filter(q => (topic === 'all' || q.topic === topic) && (!retryIDs || retryIDs.includes(q.id)) &&
        (view === 'all' || view === 'unanswered' && !hasAnswer(q) || view === 'missed' && hasAnswer(q) && !correct(q)));
    }
    function draw(rebuild = true) {
      if (rebuild) deck = getDeck();
      index = Math.max(0, Math.min(index, deck.length - 1));
      const answered = D.questions.filter(hasAnswer).length, score = D.questions.filter(correct).length;
      $('#quiz-score').textContent = score + ' correct / ' + answered + ' answered · ' + (D.questions.length-answered) + ' remaining';
      $('#quiz-meter').value = answered;
      $('#quiz-position').textContent = deck.length ? 'Question ' + (index+1) + ' of ' + deck.length + (retryIDs ? ' · retrying missed questions' : '') : 'No questions in this set.';
      $('#quiz-prev').disabled = index === 0 || !deck.length;
      $('#quiz-next').disabled = index >= deck.length-1 || !deck.length;
      $('#quiz-retry').disabled = !D.questions.some(q => hasAnswer(q) && !correct(q) && ($('#quiz-topic').value === 'all' || q.topic === $('#quiz-topic').value));
      $('#quiz-breakdown').innerHTML = '<p class="meta">' + topics.map(t => '<a href="' + t + '.html">' + esc(title(t)) + '</a>: ' + D.questions.filter(q => q.topic === t && correct(q)).length + '/' + D.questions.filter(q => q.topic === t).length).join(' · ') + '</p>';
      if (!deck.length) { $('#quiz-card').innerHTML = '<p class="empty">Nothing here yet. Choose All questions, answer more questions, or retry a missed set.</p>'; return; }
      const q = deck[index];
      $('#quiz-card').innerHTML = questionHTML(q, state.answers, 'quiz');
      bindQuestion($('#quiz-card'), q, value => {
        state.answers[q.id] = value; persist();
        // Keep this deck stable while showing feedback, even in Unanswered view.
        draw(false); $('.feedback', $('#quiz-card')).focus();
      });
    }
    ['#quiz-topic','#quiz-view'].forEach(selector => $(selector).addEventListener('change', () => { index=0; retryIDs=null; draw(); }));
    $('#quiz-prev').addEventListener('click', () => { index--; draw(false); });
    $('#quiz-next').addEventListener('click', () => { index++; draw(false); });
    $('#quiz-retry').addEventListener('click', () => {
      retryIDs = D.questions.filter(q => hasAnswer(q) && !correct(q) && ($('#quiz-topic').value === 'all' || q.topic === $('#quiz-topic').value)).map(q => q.id);
      retryIDs.forEach(id => { delete state.answers[id]; });
      $('#quiz-view').value = 'all'; index=0; persist(); draw();
    });
    $('#quiz-reset').addEventListener('click', () => {
      if (!confirm('Clear this quiz attempt? Lesson, lab and flashcard progress will stay.')) return;
      state.answers={}; retryIDs=null; index=0; $('#quiz-view').value='all'; persist(); draw();
    });
    draw();
  }
  const issueSearch = $('#issue-search');
  if (issueSearch) {
    const filter = () => {
      const needle = issueSearch.value.trim().toLowerCase(), category = $('#issue-category').value;
      let count=0;
      $$('.issue').forEach(el => {
        el.hidden = !(el.textContent.toLowerCase().includes(needle) && (category === 'all' || el.dataset.category === category));
        if (!el.hidden) count++;
      });
      $('#issue-count').textContent = count + ' of ' + $$('.issue').length + ' cases';
      $('#issue-empty').hidden = count !== 0;
    };
    issueSearch.addEventListener('input', filter); $('#issue-category').addEventListener('change', filter);
    try {
      const hash = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (hash?.classList.contains('issue')) hash.open = true;
    } catch (_) { /* A malformed external hash must not interrupt the page. */ }
  }
  if ($('#command-search')) {
    const rows = $$('#command-table tbody tr');
    const filter = () => {
      const needle = $('#command-search').value.toLowerCase().trim();
      rows.forEach(row => { row.hidden = !row.textContent.toLowerCase().includes(needle); });
      const n = rows.filter(row => !row.hidden).length;
      $('#command-count').textContent = n + ' of ' + rows.length + ' commands';
      $('#command-empty').hidden = n !== 0;
    };
    $('#command-search').addEventListener('input', filter);
    $('#print-reference').addEventListener('click', () => window.print());
    filter();
  }

  let renderCards = () => {};
  if ($('#flashcards')) {
    const topics = [...new Set(D.cards.map(c => c.topic))];
    $('#flashcards').innerHTML = '<div class="filters"><label class="field">Card topic<select id="card-topic"><option value="all">All topics</option>' + topics.map(t => '<option value="' + t + '">' + esc(title(t)) + '</option>').join('') + '</select></label><label class="field">Review mode<select id="card-mode"><option value="due">Due + new cards</option><option value="all">All cards</option></select></label></div><p id="card-position" class="meta" role="status"></p><button class="flashcard" id="flashcard" aria-expanded="false"></button><div class="actions"><button class="btn" id="card-again" disabled>Again · review soon</button><button class="btn btn-primary" id="card-known" disabled>Know it</button><button class="btn" id="card-next">Skip →</button></div>';
    let index=0, revealed=false, deck=[];
    function getDeck() {
      return D.cards.filter(c => ($('#card-topic').value === 'all' || c.topic === $('#card-topic').value) &&
        ($('#card-mode').value === 'all' || !state.cards[c.id] || state.cards[c.id].due <= Date.now()));
    }
    renderCards = () => {
      deck=getDeck(); index=deck.length ? index % deck.length : 0; revealed=false;
      $('#card-again').disabled=true; $('#card-known').disabled=true;
      $('#card-next').disabled=!deck.length; $('#flashcard').disabled=!deck.length;
      $('#flashcard').setAttribute('aria-expanded','false');
      $('#card-position').textContent=deck.length ? 'Card ' + (index+1) + ' of ' + deck.length + ' in this review set' : 'No cards due in this topic. Switch to All cards for extra practice.';
      $('#flashcard').innerHTML = deck.length ? '<small>RECALL THE KEY OR COMMAND</small><strong>' + esc(deck[index].prompt) + '</strong><small>Click, Enter or Space to reveal</small>' : '<strong>You are caught up.</strong><small>Return tomorrow or review all cards.</small>';
    };
    $('#flashcard').addEventListener('click', () => {
      if (!deck.length) return;
      revealed=!revealed; $('#flashcard').setAttribute('aria-expanded',String(revealed));
      $('#card-again').disabled=!revealed; $('#card-known').disabled=!revealed;
      $('#flashcard').innerHTML = revealed ? '<small>' + esc(deck[index].prompt) + '</small><strong>' + esc(deck[index].answer).replaceAll('\n','<br>') + '</strong><small>' + esc(deck[index].why) + '</small>' : '<small>RECALL THE KEY OR COMMAND</small><strong>' + esc(deck[index].prompt) + '</strong><small>Click to reveal</small>';
    });
    const rate = known => {
      if (!revealed || !deck.length) return;
      const c=deck[index], old=state.cards[c.id] || {streak:0};
      const streak=known ? Math.min(old.streak+1,5) : 0;
      state.cards[c.id]={streak, due:known ? Date.now()+[1,3,7,14,30][streak-1]*86400000 : 0};
      if (!known || $('#card-mode').value === 'all') index++;
      persist(); renderCards();
    };
    $('#card-again').addEventListener('click',()=>rate(false));
    $('#card-known').addEventListener('click',()=>rate(true));
    $('#card-next').addEventListener('click',()=>{index++;renderCards();});
    ['#card-topic','#card-mode'].forEach(s=>$(s).addEventListener('change',()=>{index=0;renderCards();}));
    renderCards();
  }
  $('#export-progress')?.addEventListener('click', () => {
    const blob = new Blob([JSON.stringify({format:'git-learning-progress', exportedAt:new Date().toISOString(), progress:state},null,2)], {type:'application/json'});
    const url=URL.createObjectURL(blob), link=document.createElement('a');
    link.href=url; link.download='git-learning-progress.json'; document.body.append(link); link.click(); link.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
    $('#progress-message').textContent='Progress export prepared.';
  });
  $('#import-trigger')?.addEventListener('click', () => $('#import-progress').click());
  $('#import-progress')?.addEventListener('change', async e => {
    const file=e.target.files[0]; if (!file) return;
    try {
      if (file.size > 1000000) throw new Error('Choose a progress JSON file smaller than 1 MB.');
      const raw=JSON.parse(await file.text());
      if (raw.format !== 'git-learning-progress') throw new Error('This is not a git learning progress export.');
      const imported=normalize(raw.progress);
      if (!confirm('Replace current git learning progress with this backup?')) return;
      state=imported; persist(); renderCards();
      $('#progress-message').textContent='Progress imported.' + (storageOK ? '' : ' Browser storage is unavailable; export again before leaving.');
    } catch (error) { $('#progress-message').textContent='Import failed: ' + error.message; }
    finally { e.target.value=''; }
  });
  $('#reset-progress')?.addEventListener('click', () => {
    if (!confirm('Reset all git lesson, quiz, lab, mission and recall progress? Export a backup first if needed.')) return;
    state=empty(); persist(); renderCards(); $('#progress-message').textContent='Learning progress reset.';
  });
  // Probe availability once so the UI is honest when localStorage is denied.
  persist();
})();
