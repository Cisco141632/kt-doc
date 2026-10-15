(function () {
  'use strict';

  const MODULES = [
    { id: 'start', file: 'index.html', title: 'Start here', level: 'Beginner', mins: 10, desc: 'Understand the path and take a small starting check.' },
    { id: 'sentences', file: 'sentence-basics.html', title: 'Build full sentences', level: 'Beginner', mins: 25, desc: 'Subject, verb, object, capital letters and full stops.' },
    { id: 'daily', file: 'daily-words.html', title: 'Daily words & sentences', level: 'Beginner', mins: 30, desc: 'High-frequency words for home, travel, food and routines.' },
    { id: 'workplace', file: 'workplace.html', title: 'Workplace English', level: 'Elementary', mins: 35, desc: 'Meetings, tasks, updates, requests and professional messages.' },
    { id: 'grammar', file: 'grammar.html', title: 'Grammar that you use', level: 'Elementary', mins: 30, desc: 'Present, past and future without memorising long rules.' },
    { id: 'questions', file: 'questions-conversation.html', title: 'Questions & conversation', level: 'Elementary', mins: 25, desc: 'Ask, answer, clarify and keep a conversation moving.' },
    { id: 'vocabulary', file: 'vocabulary-recall.html', title: 'Vocabulary recall', level: 'Intermediate', mins: 20, desc: 'Picture flashcards and spaced confidence practice.' },
    { id: 'spelling', file: 'spelling.html', title: 'Spelling & listening', level: 'Intermediate', mins: 20, desc: 'Listen, type, notice patterns and correct mistakes.' },
    { id: 'advanced', file: 'advanced.html', title: 'Clear advanced English', level: 'Advanced', mins: 35, desc: 'Passive voice, conditionals, connectors and professional tone.' },
    { id: 'practice', file: 'practice.html', title: 'Daily practice', level: 'All levels', mins: 20, desc: 'A repeatable daily routine with real writing prompts.' },
    { id: 'quiz', file: 'quiz.html', title: 'Mixed recall test', level: 'All levels', mins: 20, desc: 'Test sentence building, words, grammar and workplace English.' },
    { id: 'reference', file: 'reference.html', title: 'Quick reference', level: 'All levels', mins: 10, desc: 'Patterns, common words, corrections and a learning checklist.' }
  ];

  const VOCAB = [
    { word: 'home', image: 'home.svg', group: 'daily', meaning: 'the place where you live', sentence: 'I am going home now.' },
    { word: 'water', image: 'water.svg', group: 'daily', meaning: 'a drink that your body needs', sentence: 'Could I have some water?' },
    { word: 'meal', image: 'meal.svg', group: 'daily', meaning: 'food eaten at one time', sentence: 'We had a good meal.' },
    { word: 'bus', image: 'bus.svg', group: 'daily', meaning: 'a large road vehicle for passengers', sentence: 'I take the bus to work.' },
    { word: 'phone', image: 'phone.svg', group: 'daily', meaning: 'a device used to call or message', sentence: 'My phone is charging.' },
    { word: 'time', image: 'clock.svg', group: 'daily', meaning: 'what a clock shows', sentence: 'What time will you arrive?' },
    { word: 'book', image: 'book.svg', group: 'daily', meaning: 'pages of writing or pictures', sentence: 'I read a book every evening.' },
    { word: 'coffee', image: 'coffee.svg', group: 'daily', meaning: 'a hot drink made from roasted beans', sentence: 'I would like a coffee, please.' },
    { word: 'laptop', image: 'laptop.svg', group: 'workplace', meaning: 'a portable computer', sentence: 'My laptop needs an update.' },
    { word: 'calendar', image: 'calendar.svg', group: 'workplace', meaning: 'a tool for dates and appointments', sentence: 'I added the meeting to my calendar.' },
    { word: 'email', image: 'email.svg', group: 'workplace', meaning: 'a message sent electronically', sentence: 'I will send you an email.' },
    { word: 'task', image: 'briefcase.svg', group: 'workplace', meaning: 'a piece of work to complete', sentence: 'I completed the task.' },
    { word: 'document', image: 'document.svg', group: 'workplace', meaning: 'a written file with information', sentence: 'Please review this document.' },
    { word: 'message', image: 'message.svg', group: 'workplace', meaning: 'information sent to another person', sentence: 'I received your message.' },
    { word: 'team', image: 'team.svg', group: 'workplace', meaning: 'people who work together', sentence: 'Our team meets every morning.' },
    { word: 'complete', image: 'complete.svg', group: 'workplace', meaning: 'to finish all parts of something', sentence: 'I will complete it today.' },
    { word: 'issue', image: 'bug.svg', group: 'workplace', meaning: 'a problem that needs attention', sentence: 'We found an issue in the application.' },
    { word: 'release', image: 'release.svg', group: 'workplace', meaning: 'a version made available to users', sentence: 'The release is ready for testing.' }
  ];

  const QUIZ = [
    { q: 'Choose the complete sentence.', options: ['Need help with task.', 'I need help with this task.', 'I needing help this task.'], answer: 1, why: 'A complete basic sentence needs a subject (I), a verb (need), and the rest of the idea.' },
    { q: 'You are doing the task now. Which is correct?', options: ['I work on the task now.', 'I am working on the task now.', 'I working on task now.'], answer: 1, why: 'Use am/is/are + verb-ing for an action happening now.' },
    { q: 'Which question asks for clarification politely?', options: ['Explain again.', 'What you mean?', 'Could you please explain that again?'], answer: 2, why: 'Could you please…? is a clear, polite request pattern.' },
    { q: 'What does “It is being fixed” mean?', options: ['Someone is fixing it now.', 'It was fixed yesterday.', 'Nobody will fix it.'], answer: 0, why: 'Is being + past participle describes an action happening to something now.' },
    { q: 'Choose the correct past sentence.', options: ['I complete it yesterday.', 'I completed it yesterday.', 'I am completed it yesterday.'], answer: 1, why: 'Completed is the past form, and yesterday signals past time.' },
    { q: 'Choose the best workplace update.', options: ['Issue there. Fixing.', 'The issue is being fixed. I will share an update by 3 PM.', 'Problem maybe done soon.'], answer: 1, why: 'It states the status and gives a clear next update time.' },
    { q: 'Which spelling is correct?', options: ['recieve', 'receeve', 'receive'], answer: 2, why: 'The correct spelling is receive.' },
    { q: 'Choose the correct question.', options: ['Did you completed the task?', 'Did you complete the task?', 'You did complete the task?'], answer: 1, why: 'After did, use the base verb: complete.' },
    { q: 'Which sentence sounds professional and direct?', options: ['Send file fast.', 'Could you send the file by 2 PM, please?', 'Why file not sent?'], answer: 1, why: 'It is polite and includes a specific deadline.' },
    { q: 'Choose the correct conditional.', options: ['If the test fails, we will not deploy.', 'If the test will fail, we not deploy.', 'If test fail, no deploy.'], answer: 0, why: 'Use if + present simple, then will + base verb for a real future possibility.' }
  ];

  const KEYS = { theme: 'english-path-theme', done: 'english-path-done', recall: 'english-path-recall', daily: 'english-path-daily' };
  const root = document.documentElement;
  root.classList.add('js');
  const favicon = document.createElement('link');
  favicon.rel = 'icon';
  favicon.href = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='9' fill='%233559c7'/%3E%3Ctext x='16' y='21' text-anchor='middle' font-family='Arial' font-size='12' font-weight='700' fill='white'%3EEN%3C/text%3E%3C/svg%3E";
  document.head.appendChild(favicon);
  const store = {
    get(key, fallback) { try { const value = localStorage.getItem(key); return value === null ? fallback : JSON.parse(value); } catch (_) { return fallback; } },
    set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch (_) { /* progress is optional */ } }
  };
  const esc = (value) => String(value).replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
  const normalize = (value) => String(value).toLowerCase().replace(/[’']/g, '').replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();
  const activeId = () => document.body.dataset.module || 'start';
  const doneList = () => store.get(KEYS.done, []).filter((id) => MODULES.some((module) => module.id === id));

  function setTheme(value) {
    root.dataset.theme = value;
    store.set(KEYS.theme, value);
  }
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  setTheme(store.get(KEYS.theme, prefersDark ? 'dark' : 'light'));

  function shell() {
    const side = document.getElementById('sidebar');
    if (!side) return;
    const done = doneList();
    const items = MODULES.map((module, index) => `<li class="${module.id === activeId() ? 'active' : ''} ${done.includes(module.id) ? 'done' : ''}"><a href="${module.file}"${module.id === activeId() ? ' aria-current="page"' : ''}><span class="num">${done.includes(module.id) ? '✓' : index + 1}</span><span>${esc(module.title)}</span><small>${esc(module.level)}</small></a></li>`).join('');
    const percent = Math.round(done.length / MODULES.length * 100);
    side.innerHTML = `<a class="brand" href="index.html"><span class="brand-mark">EN</span><span>English Recall Path<small>Understand · remember · use</small></span></a><div><div class="progress-copy"><span>${done.length} of ${MODULES.length} complete</span><span>${percent}%</span></div><div class="progress-track" role="progressbar" aria-label="Course progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${percent}"><span style="width:${percent}%"></span></div></div><nav aria-label="Course modules"><ol class="modules">${items}</ol></nav><div class="side-actions"><a class="btn small" href="../index.html">All paths</a><button class="btn small" type="button" data-theme>${root.dataset.theme === 'dark' ? 'Light' : 'Dark'}</button></div>`;
    side.querySelector('[data-theme]').addEventListener('click', () => { setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'); shell(); });

    const mobile = document.querySelector('.mobile-menu') || document.createElement('div');
    mobile.className = 'mobile-menu';
    mobile.innerHTML = '<b>English Recall Path</b><button class="btn small" type="button" aria-expanded="false">Modules</button>';
    if (!mobile.parentNode) document.body.prepend(mobile);
    mobile.querySelector('button').addEventListener('click', (event) => {
      const open = side.classList.toggle('open');
      event.currentTarget.setAttribute('aria-expanded', String(open));
    });
  }

  function pageMeta() {
    const module = MODULES.find((item) => item.id === activeId());
    const head = document.querySelector('.page-head');
    if (module && head && !head.querySelector('.eyebrow')) {
      const note = document.createElement('p');
      note.className = 'eyebrow';
      note.textContent = `${module.level} · about ${module.mins} minutes`;
      head.prepend(note);
    }
    const target = document.querySelector('[data-module-cards]');
    if (target) target.innerHTML = MODULES.slice(1).map((item, index) => `<a class="card" href="${item.file}"><span class="tag">${esc(item.level)} · Step ${index + 1}</span><b>${esc(item.title)}</b><small>${esc(item.desc)}</small></a>`).join('');
  }

  function pager() {
    const main = document.querySelector('main');
    const index = MODULES.findIndex((item) => item.id === activeId());
    if (!main || index < 0) return;
    const footer = document.createElement('footer');
    footer.className = 'pager';
    const previous = MODULES[index - 1];
    const next = MODULES[index + 1];
    const done = doneList().includes(activeId());
    footer.innerHTML = `${previous ? `<a class="btn" href="${previous.file}">← ${esc(previous.title)}</a>` : ''}<span class="push"></span><button class="btn ${done ? 'primary' : ''}" type="button" data-done>${done ? '✓ Completed' : 'Mark complete'}</button>${next ? `<a class="btn primary" href="${next.file}">${esc(next.title)} →</a>` : ''}`;
    footer.querySelector('[data-done]').addEventListener('click', () => {
      const values = doneList().filter((id) => id !== activeId());
      if (!done) values.push(activeId());
      store.set(KEYS.done, values);
      location.reload();
    });
    const credits = document.createElement('p');
    credits.className = 'credits';
    credits.innerHTML = 'Recall pictures: <a href="https://openmoji.org/" target="_blank" rel="noreferrer">OpenMoji</a>, CC BY-SA 4.0.';
    main.append(footer, credits);
  }

  function speak(text) {
    if (!('speechSynthesis' in window)) return false;
    speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = .82;
    speechSynthesis.speak(utterance);
    return true;
  }

  function speechButtons() {
    document.querySelectorAll('[data-speak]').forEach((button) => button.addEventListener('click', () => {
      const text = button.dataset.speak || button.closest('[data-speech-text]')?.dataset.speechText || '';
      if (!speak(text)) button.textContent = 'Speech is not supported in this browser';
    }));
  }

  function answerChecks() {
    document.querySelectorAll('[data-answer]').forEach((form) => {
      form.addEventListener('submit', (event) => {
        event.preventDefault();
        const input = form.querySelector('input, textarea');
        const feedback = form.querySelector('.feedback');
        const accepted = form.dataset.answer.split('|').map(normalize);
        const value = normalize(input.value);
        const correct = accepted.includes(value);
        feedback.className = `feedback ${correct ? 'ok' : 'bad'}`;
        if (correct) feedback.innerHTML = `<b>Correct.</b> ${esc(form.dataset.success || 'Say it aloud once more.')}`;
        else feedback.innerHTML = `<b>Try again.</b> ${esc(form.dataset.hint || 'Check the word order, verb, capital letter, and full stop.')} <button class="btn small" type="button" data-show-answer>Show answer</button>`;
        const show = feedback.querySelector('[data-show-answer]');
        if (show) show.addEventListener('click', () => { feedback.innerHTML = `<b>Model answer:</b> ${esc(form.dataset.model || form.dataset.answer.split('|')[0])}. Now hide it and type it again.`; });
      });
    });
  }

  function sentenceBuilders() {
    document.querySelectorAll('[data-sentence-builder]').forEach((builder) => {
      const output = builder.querySelector('.sentence-line');
      const chips = [...builder.querySelectorAll('[data-word]')];
      const feedback = builder.querySelector('.feedback');
      const chosen = [];
      const render = () => { output.textContent = chosen.map((item) => item.dataset.word).join(' '); };
      chips.forEach((chip) => chip.addEventListener('click', () => { chosen.push(chip); chip.disabled = true; render(); }));
      builder.querySelector('[data-undo]').addEventListener('click', () => { const chip = chosen.pop(); if (chip) chip.disabled = false; render(); feedback.textContent = ''; });
      builder.querySelector('[data-clear]').addEventListener('click', () => { chosen.splice(0).forEach((chip) => { chip.disabled = false; }); render(); feedback.textContent = ''; });
      builder.querySelector('[data-check-sentence]').addEventListener('click', () => {
        const correct = normalize(output.textContent) === normalize(builder.dataset.target);
        feedback.className = `feedback ${correct ? 'ok' : 'bad'}`;
        feedback.innerHTML = correct ? '<b>Correct.</b> Read your complete sentence aloud.' : `<b>Not yet.</b> Start with the person or thing doing the action. Target: ${esc(builder.dataset.target)}`;
      });
    });
  }

  function pictureGrids() {
    document.querySelectorAll('[data-picture-group]').forEach((target) => {
      const words = VOCAB.filter((item) => target.dataset.pictureGroup === 'all' || item.group === target.dataset.pictureGroup);
      target.innerHTML = words.map((item) => `<article class="picture-word"><img src="assets/images/${item.image}" alt=""><b>${esc(item.word)}</b><small>${esc(item.meaning)}</small><button class="btn small" type="button" data-speak="${esc(item.word)}. ${esc(item.sentence)}">🔊 Hear it</button></article>`).join('');
    });
  }

  function vocabDecks() {
    document.querySelectorAll('[data-vocab-deck]').forEach((target) => {
      const group = target.dataset.vocabDeck;
      let words = VOCAB.filter((item) => group === 'all' || item.group === group);
      let current = 0;
      let revealed = false;
      const progress = store.get(KEYS.recall, {});
      words = words.sort((a, b) => (progress[a.word] || 0) - (progress[b.word] || 0));
      function draw() {
        const item = words[current % words.length];
        target.innerHTML = `<div class="flashcard"><span class="tag">Picture recall</span><img src="assets/images/${item.image}" alt="Picture clue for the word"><p class="prompt">What is this word? Say it before you reveal it.</p>${revealed ? `<div class="answer"><strong>${esc(item.word)}</strong><span>${esc(item.meaning)}</span><p>“${esc(item.sentence)}”</p></div><button class="btn small" type="button" data-say>🔊 Hear word and sentence</button><div class="rating" aria-label="Rate your recall"><button class="btn danger" data-rate="0">Again</button><button class="btn" data-rate="1">Hard</button><button class="btn primary" data-rate="2">I knew it</button></div>` : '<button class="btn primary" type="button" data-reveal>Reveal answer</button>'}<p class="deck-status">Card ${current + 1} of ${words.length} · ratings are saved on this device</p></div>`;
        target.querySelector('[data-reveal]')?.addEventListener('click', () => { revealed = true; draw(); });
        target.querySelector('[data-say]')?.addEventListener('click', () => speak(`${item.word}. ${item.sentence}`));
        target.querySelectorAll('[data-rate]').forEach((button) => button.addEventListener('click', () => {
          progress[item.word] = Number(button.dataset.rate);
          store.set(KEYS.recall, progress);
          current = (current + 1) % words.length;
          revealed = false;
          draw();
        }));
      }
      draw();
    });
  }

  function spellingTrainer() {
    document.querySelectorAll('[data-spelling]').forEach((target) => {
      const group = target.dataset.spelling;
      const words = VOCAB.filter((item) => group === 'all' || item.group === group);
      let current = 0;
      let hints = 0;
      function draw() {
        const item = words[current % words.length];
        const clue = item.word.split('').map((letter, index) => index < hints ? letter : '_').join(' ');
        target.innerHTML = `<div class="spelling-stage"><span class="tag">Listen and spell</span><img src="assets/images/${item.image}" alt="Picture clue"><div><button class="btn" type="button" data-listen>🔊 Listen</button> <button class="btn" type="button" data-hint>One-letter hint</button></div><div class="letter-hint">${esc(clue)}</div><form class="answer-row"><label class="sr-only" for="spell-word">Type the word</label><input id="spell-word" autocomplete="off" spellcheck="false" placeholder="Type the word you hear"><button class="btn primary">Check spelling</button></form><p class="feedback" aria-live="polite"></p></div>`;
        const input = target.querySelector('input');
        const feedback = target.querySelector('.feedback');
        target.querySelector('[data-listen]').addEventListener('click', () => speak(item.word));
        target.querySelector('[data-hint]').addEventListener('click', () => { hints = Math.min(item.word.length, hints + 1); draw(); });
        target.querySelector('form').addEventListener('submit', (event) => {
          event.preventDefault();
          if (normalize(input.value) === item.word) {
            feedback.className = 'feedback ok';
            feedback.innerHTML = `<b>Correct: ${esc(item.word)}.</b> ${esc(item.sentence)} <button class="btn small primary" type="button" data-next>Next word →</button>`;
            feedback.querySelector('[data-next]').addEventListener('click', () => { current = (current + 1) % words.length; hints = 0; draw(); });
          } else {
            feedback.className = 'feedback bad';
            feedback.innerHTML = `<b>Not yet.</b> You typed “${esc(input.value)}”. Listen slowly and try again.`;
          }
        });
      }
      draw();
    });
  }

  function matchGames() {
    document.querySelectorAll('[data-match]').forEach((target) => {
      const words = VOCAB.filter((item) => item.group === target.dataset.match).slice(0, 6);
      const cards = words.flatMap((item) => [{ key: item.word, type: 'image', value: item.image }, { key: item.word, type: 'word', value: item.word }]).sort(() => Math.random() - .5);
      let selected = null;
      let matches = 0;
      target.innerHTML = `<div class="match-grid">${cards.map((card, index) => `<button class="match-card" type="button" data-index="${index}" data-key="${esc(card.key)}">${card.type === 'image' ? `<img src="assets/images/${card.value}" alt="Picture to match">` : esc(card.value)}</button>`).join('')}</div><p class="feedback" aria-live="polite">Match each picture with its English word.</p>`;
      const feedback = target.querySelector('.feedback');
      target.querySelectorAll('.match-card').forEach((card) => card.addEventListener('click', () => {
        if (card.classList.contains('matched')) return;
        if (!selected) { selected = card; card.classList.add('selected'); return; }
        if (selected === card) { card.classList.remove('selected'); selected = null; return; }
        if (selected.dataset.key === card.dataset.key) {
          selected.classList.remove('selected'); selected.classList.add('matched'); card.classList.add('matched');
          matches += 1; feedback.className = 'feedback ok'; feedback.textContent = matches === words.length ? 'Excellent—every pair is correct.' : `Correct: ${card.dataset.key}. ${matches} of ${words.length} pairs.`;
        } else {
          selected.classList.remove('selected'); feedback.className = 'feedback bad'; feedback.textContent = 'Those do not match. Look carefully and try again.';
        }
        selected = null;
      }));
    });
  }

  function dailyPlan() {
    const target = document.querySelector('[data-daily-plan]');
    if (!target) return;
    const today = new Date().toISOString().slice(0, 10);
    const saved = store.get(KEYS.daily, {});
    const record = saved[today] || [];
    const tasks = [
      ['Recall 5 words', 'Look at a picture, say the word, then spell it.'],
      ['Build 3 sentences', 'Use: I + verb + the rest of the idea.'],
      ['Listen and repeat', 'Use the speaker buttons and copy the rhythm.'],
      ['Write one work update', 'Status + problem + next action + time.'],
      ['Review yesterday’s mistakes', 'Correct each mistake and write the sentence again.']
    ];
    const render = () => {
      target.innerHTML = `<div class="streak"><strong>${record.length}/5</strong> activities completed today</div><div class="daily-list">${tasks.map((task, index) => `<label class="daily-item ${record.includes(index) ? 'done' : ''}"><input type="checkbox" data-task="${index}" ${record.includes(index) ? 'checked' : ''}><span><b>${task[0]}</b><small>${task[1]}</small></span></label>`).join('')}</div>`;
      target.querySelectorAll('[data-task]').forEach((checkbox) => checkbox.addEventListener('change', () => {
        const index = Number(checkbox.dataset.task);
        const position = record.indexOf(index);
        if (checkbox.checked && position < 0) record.push(index);
        if (!checkbox.checked && position >= 0) record.splice(position, 1);
        saved[today] = record;
        store.set(KEYS.daily, saved);
        render();
      }));
    };
    render();
  }

  function quiz() {
    const target = document.querySelector('[data-quiz]');
    if (!target) return;
    let current = 0;
    let score = 0;
    let answered = false;
    function draw() {
      if (current >= QUIZ.length) {
        const percent = Math.round(score / QUIZ.length * 100);
        target.innerHTML = `<div class="practice-box"><span class="tag">Result</span><div class="score-ring">${percent}%</div><h2>${percent >= 80 ? 'Strong recall' : percent >= 60 ? 'Good start—review and retry' : 'Keep practising—this is how recall grows'}</h2><p>You answered ${score} of ${QUIZ.length} correctly.</p><button class="btn primary" type="button" data-restart>Try again</button></div>`;
        target.querySelector('[data-restart]').addEventListener('click', () => { current = 0; score = 0; answered = false; draw(); });
        return;
      }
      const item = QUIZ[current];
      target.innerHTML = `<div class="practice-box"><p class="quiz-progress">Question ${current + 1} of ${QUIZ.length} · Score ${score}</p><h2>${esc(item.q)}</h2><div>${item.options.map((option, index) => `<button class="quiz-option" type="button" data-option="${index}">${esc(option)}</button>`).join('')}</div><p class="feedback" aria-live="polite"></p></div>`;
      target.querySelectorAll('[data-option]').forEach((button) => button.addEventListener('click', () => {
        if (answered) return;
        answered = true;
        const picked = Number(button.dataset.option);
        const correct = picked === item.answer;
        if (correct) score += 1;
        button.classList.add(correct ? 'correct' : 'wrong');
        target.querySelectorAll('[data-option]')[item.answer].classList.add('correct');
        const feedback = target.querySelector('.feedback');
        feedback.className = `feedback ${correct ? 'ok' : 'bad'}`;
        feedback.innerHTML = `<b>${correct ? 'Correct.' : 'Not quite.'}</b> ${esc(item.why)} <button class="btn small primary" type="button" data-next>Next →</button>`;
        feedback.querySelector('[data-next]').addEventListener('click', () => { current += 1; answered = false; draw(); });
      }));
    }
    draw();
  }

  document.addEventListener('DOMContentLoaded', () => {
    shell(); pageMeta(); pictureGrids(); speechButtons(); answerChecks(); sentenceBuilders(); vocabDecks(); spellingTrainer(); matchGames(); dailyPlan(); quiz(); pager();
  });
})();
