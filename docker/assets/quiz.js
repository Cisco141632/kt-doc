/* Docker learning path — quizzes.
   In every question the FIRST option is the correct one. The options are shuffled when shown. */
(function () {
  'use strict';

  const KT = window.DockerKT;
  const BEST_KEY = 'docker-kt-quiz-best';
  const PASS = 80;
  const FINAL_SIZE = 15;

  const TESTS = [
    {
      id: 'basics', title: 'Test 1 · Basics', module: 'index',
      questions: [
        { q: 'What is the difference between an image and a container?',
          options: ['An image is a read-only package; a container is a running instance of it', 'An image is running; a container is stored on disk', 'They are two names for the same thing', 'An image is for Linux; a container is for Windows'],
          why: 'You build an image once and start as many containers from it as you like.' },
        { q: 'Why does a container start much faster than a virtual machine?',
          options: ['It shares the kernel of the host, so no operating system has to boot', 'It always runs on a faster disk', 'It skips all security checks', 'It keeps everything in memory'],
          why: 'A container is an isolated process on a kernel that is already running. A virtual machine boots a full guest operating system.' },
        { q: 'You run <code>docker run nginx:alpine</code> for the first time and Docker downloads something. From where?',
          options: ['From a registry, by default Docker Hub', 'From the nginx company website', 'From another container', 'From your Git repository'],
          why: 'A registry stores and shares images. Docker Hub is the default one.' },
        { q: 'You start two containers from one image and create a file in the first. What does the second container see?',
          options: ['Nothing. Each container has its own writable layer', 'The same file, because they share the image', 'An error, because the image is locked', 'The file, but read-only'],
          why: 'The image is shared and read-only. Changes go into a private layer of each container.' },
        { q: 'What is the <code>docker</code> command that you type in the terminal?',
          options: ['A client that sends requests to the Docker daemon, which does the work', 'The program that runs the containers itself', 'A virtual machine', 'A kind of image'],
          why: 'If the daemon is not running, the client can do nothing and reports "Cannot connect to the Docker daemon".' },
        { q: 'When does a container stop by itself?',
          options: ['When its main process ends', 'After 24 hours', 'When you close the terminal', 'When the image is updated'],
          why: 'A container lives exactly as long as its main process. That is why a crashed app means a stopped container.' },
        { q: 'In <code>nginx:alpine</code>, what is <code>alpine</code>?',
          options: ['The tag: a version or variant of the image', 'The registry', 'The name of the container', 'A command that runs inside'],
          why: 'The format is <code>repository:tag</code>. Without a tag, Docker uses <code>latest</code>.' },
      ],
    },
    {
      id: 'commands', title: 'Test 2 · Commands', module: 'commands',
      questions: [
        { q: 'A container was started with <code>-p 9000:3000</code>. Which address do you open in the browser?',
          options: ['<code>localhost:9000</code>', '<code>localhost:3000</code>', 'Either one', '<code>localhost:80</code>'],
          why: 'The order is <code>HOST:CONTAINER</code>. 9000 is the port on your machine.' },
        { q: 'After <code>docker stop web</code>, the command <code>docker ps</code> no longer lists the container. Is it gone?',
          options: ['No. It still exists and <code>docker ps -a</code> shows it', 'Yes, it was deleted', 'Yes, together with its image', 'It was paused, not stopped'],
          why: 'Stopping keeps the container and its files. Only <code>docker rm</code> deletes it.' },
        { q: 'What is the difference between <code>docker run</code> and <code>docker exec</code>?',
          options: ['<code>run</code> creates a new container; <code>exec</code> runs a command in one that is already running', '<code>exec</code> creates a new container; <code>run</code> uses an existing one', 'They do the same thing', '<code>exec</code> only works on images'],
          why: 'To look inside your running app you want <code>exec</code>. <code>run</code> would give you a second, separate container.' },
        { q: 'What does <code>--rm</code> do in <code>docker run --rm alpine date</code>?',
          options: ['Removes the container automatically when it exits', 'Removes the image after the run', 'Deletes all stopped containers', 'Runs the container without a network'],
          why: 'Without it, every one-off command leaves a stopped container behind.' },
        { q: 'The disk is almost full. Which command is safe to run first?',
          options: ['<code>docker system df</code>', '<code>docker system prune -a --volumes</code>', '<code>docker volume prune -a</code>', '<code>docker rm -f $(docker ps -aq)</code>'],
          why: '<code>docker system df</code> only shows usage. The other three delete things, including data that may be needed.' },
        { q: 'What happens with <code>docker run nginx:alpine -d</code>?',
          options: ['<code>-d</code> is handed to the container as its command; it does not run in the background', 'It runs in the background as usual', 'Docker ignores the <code>-d</code>', 'It downloads the image twice'],
          why: 'Options must come before the image name. Everything after the image name is the command for the container.' },
        { q: '<code>docker exec -it web bash</code> answers: <code>exec: "bash": executable file not found</code>. What now?',
          options: ['Use <code>sh</code> instead; small images such as Alpine have no bash', 'Restart the Docker daemon', 'The container is broken; rebuild it', 'Add <code>sudo</code>'],
          why: 'Alpine-based images include only <code>sh</code>.' },
        { q: 'Which command shows why a container that already stopped has failed?',
          options: ['<code>docker logs NAME</code>', '<code>docker stats</code>', '<code>docker images</code>', '<code>docker start NAME</code>'],
          why: 'Logs are kept for stopped containers until the container is removed.' },
      ],
    },
    {
      id: 'dockerfile', title: 'Test 3 · Dockerfile', module: 'dockerfile',
      questions: [
        { q: 'Why does a good Dockerfile copy <code>requirements.txt</code> and install dependencies <b>before</b> copying the rest of the code?',
          options: ['So the slow install layer stays cached when only the code changes', 'Because Docker requires alphabetical order', 'Because dependencies cannot be installed after the code is copied', 'To make the image larger'],
          why: 'A changed layer rebuilds every layer after it. Code changes often; the dependency list rarely.' },
        { q: 'The Dockerfile contains <code>EXPOSE 8000</code>. Can you reach the app from your browser now?',
          options: ['No. <code>EXPOSE</code> is only documentation; you still need <code>-p</code>', 'Yes, on port 8000', 'Yes, on any port', 'Only on Linux'],
          why: 'Publishing a port is always done when the container starts, with <code>-p</code> or <code>ports:</code> in Compose.' },
        { q: 'What is the difference between <code>RUN</code> and <code>CMD</code>?',
          options: ['<code>RUN</code> executes while the image is built; <code>CMD</code> executes when a container starts', '<code>CMD</code> executes while the image is built; <code>RUN</code> when a container starts', 'They are the same', '<code>RUN</code> is for Linux and <code>CMD</code> for Windows'],
          why: 'Install with <code>RUN</code>, start the app with <code>CMD</code>.' },
        { q: 'In a multi-stage build, why is <code>WORKDIR /app</code> written in <b>both</b> stages?',
          options: ['Every <code>FROM</code> starts a new, separate stage; settings from the earlier stage do not carry over', 'It creates a folder shared by both stages', 'Docker requires the same folder name in every stage', 'It compresses the final image'],
          why: 'A new stage begins from its own base image. Files cross over only through <code>COPY --from</code>.' },
        { q: 'What does <code>npm ci</code> do when <code>package-lock.json</code> is missing?',
          options: ['It fails with an error', 'It creates a new lock file', 'It runs <code>npm install</code> instead', 'It installs the newest versions'],
          why: '<code>npm ci</code> installs exactly what the lock file says. That is what makes builds repeatable.' },
        { q: 'What is the main benefit of a multi-stage build?',
          options: ['The final image contains only what is needed to run, so it is smaller and safer', 'The build uses less memory', 'The container starts in several steps', 'It allows two apps in one container'],
          why: 'Compilers and development dependencies stay in the first stage, which is thrown away.' },
        { q: 'What is the dot at the end of <code>docker build -t app:1.0 .</code>?',
          options: ['The build context: the folder whose files the build may use', 'The tag of the image', 'The end of the command, as in a sentence', 'The name of the Dockerfile'],
          why: '<code>COPY</code> can only copy files that are inside the build context.' },
        { q: 'Why add <code>USER appuser</code> to a Dockerfile?',
          options: ['So the app does not run as root, which limits the damage if it is attacked', 'It makes the image smaller', 'It is required for <code>CMD</code> to work', 'It makes the build faster'],
          why: 'Containers run as root unless the image says otherwise.' },
        { q: 'Which of these belongs in <code>.dockerignore</code>?',
          options: ['<code>.git</code>, <code>.env</code> and local folders such as <code>.venv</code> or <code>node_modules</code>', '<code>requirements.txt</code>', 'The main source file', 'The <code>CMD</code> instruction'],
          why: 'It keeps the build fast and keeps secrets out of the image.' },
        { q: 'Why is <code>CMD ["gunicorn", "app:app"]</code> preferred over <code>CMD gunicorn app:app</code>?',
          options: ['The app receives the stop signal directly and shuts down cleanly', 'The bracket form is faster to type', 'The other form is not allowed', 'The bracket form uses less disk'],
          why: 'Without brackets a shell starts the app and usually does not pass the signal on, so <code>docker stop</code> waits 10 seconds and then kills it.' },
      ],
    },
    {
      id: 'storage', title: 'Test 4 · Data & networking', module: 'storage-network',
      questions: [
        { q: 'A Postgres container runs without a volume. You remove it and start a new one. What about the data?',
          options: ['It is gone', 'It is restored automatically', 'It is kept in the image', 'It moved to Docker Hub'],
          why: 'Files written inside a container are deleted with the container.' },
        { q: 'Which storage should a production database use?',
          options: ['A named volume', 'No volume; the container is enough', 'A bind mount of the source code folder', 'The image itself'],
          why: 'A named volume is managed by Docker and survives the removal of containers.' },
        { q: 'What kind of storage is <code>-v "$(pwd)/src:/app/src"</code>?',
          options: ['A bind mount: a folder of your machine shown inside the container', 'A named volume', 'A copy made at build time', 'A network share'],
          why: 'A path on the left means bind mount. A plain name on the left means named volume.' },
        { q: 'An app in a container connects to <code>localhost:5432</code>. The database is in another container. Why does it fail?',
          options: ['Inside a container, <code>localhost</code> is that container itself', 'Port 5432 is forbidden in Docker', 'Databases cannot run in containers', 'The app needs the <code>-it</code> option'],
          why: 'Put both on one network and connect to the database by its container name.' },
        { q: 'Two containers are on the same network that you created. How does one reach the other?',
          options: ['By the container name, for example <code>db:5432</code>', 'Only by IP address', 'Through <code>localhost</code>', 'They cannot talk to each other'],
          why: 'Networks you create have built-in name lookup.' },
        { q: 'The database container has no <code>-p</code>. Can the app container on the same network still connect to it?',
          options: ['Yes. <code>-p</code> is only for access from your machine or from outside', 'No. Every connection needs <code>-p</code>', 'Only if both use the same image', 'Only on Docker Desktop'],
          why: 'Not publishing the database port is also the safer choice.' },
        { q: 'What changes with <code>-p 127.0.0.1:8080:80</code> compared to <code>-p 8080:80</code>?',
          options: ['The port is reachable only from the machine itself, not from other machines', 'The container gets a fixed IP address', 'The port inside the container changes', 'Nothing'],
          why: 'Without an address, the port listens on every network interface.' },
        { q: 'Does <code>docker stop</code> delete the files written inside a container?',
          options: ['No. They stay until the container is removed', 'Yes, immediately', 'Yes, after 10 seconds', 'Only on Linux'],
          why: 'Stop then start gives you the same container with the same files.' },
      ],
    },
    {
      id: 'compose', title: 'Test 5 · Compose', module: 'compose',
      questions: [
        { q: 'What is the difference between <code>docker compose down</code> and <code>docker compose down -v</code>?',
          options: ['<code>-v</code> also deletes the named volumes, and with them the data', '<code>-v</code> only prints more details', '<code>-v</code> keeps the containers', 'There is no difference'],
          why: '<code>down</code> alone keeps your database.' },
        { q: 'With <code>depends_on: [db]</code> (short form), what is guaranteed before <code>web</code> starts?',
          options: ['Only that the <code>db</code> container has been started', 'That the database accepts connections', 'That the database is backed up', 'Nothing at all'],
          why: 'To wait for "ready", add a <code>healthcheck</code> and <code>condition: service_healthy</code>.' },
        { q: 'In a Compose project, how does the <code>web</code> service reach the <code>db</code> service?',
          options: ['By the service name: <code>db:5432</code>', 'By <code>localhost:5432</code>', 'By the IP address of your machine', 'It needs <code>ports</code> on <code>db</code> first'],
          why: 'Compose puts all services of a project on one private network with name lookup.' },
        { q: 'You changed the code and ran <code>docker compose up -d</code>. The old version still runs. Why?',
          options: ['Compose reused the image it built before; you need <code>--build</code>', 'Compose needs a reboot', 'The code must be committed to Git first', 'The volume is full'],
          why: 'An image is a snapshot. A code change needs a new image.' },
        { q: 'Where should the database password of a Compose project live?',
          options: ['In a <code>.env</code> file that is not committed to Git', 'Directly in <code>compose.yaml</code>', 'In the Dockerfile as <code>ENV</code>', 'In the image name'],
          why: 'Commit a <code>.env.example</code> with placeholder values instead.' },
        { q: 'An old Compose file starts with <code>version: \'3.8\'</code>. What does current Compose do with it?',
          options: ['Ignores it and prints a warning that it is obsolete', 'Refuses to start', 'Uses it to choose the Docker version', 'Downloads version 3.8 of every image'],
          why: 'The line can simply be deleted.' },
        { q: '<code>web</code> has <code>ports: ["8000:8000"]</code>. <code>db</code> has no <code>ports</code>. Can a database tool on your laptop connect to <code>db</code>?',
          options: ['No. Without <code>ports</code> it is reachable only inside the project network', 'Yes, on port 5432', 'Yes, on port 8000', 'Yes, on any port'],
          why: 'If you need that during development, add <code>"127.0.0.1:5432:5432"</code> to <code>db</code>.' },
        { q: 'Which command checks <code>compose.yaml</code> and prints it with all variables filled in?',
          options: ['<code>docker compose config</code>', '<code>docker compose ps</code>', '<code>docker compose check</code>', '<code>docker compose logs</code>'],
          why: 'Use it whenever Compose complains about the file or a variable.' },
      ],
    },
    {
      id: 'real', title: 'Test 6 · Real-world issues', module: 'real-world',
      questions: [
        { q: '<code>docker ps -a</code> shows <code>Exited (137)</code>. What most likely happened?',
          options: ['The process was killed, often because it ran out of memory', 'The app finished normally', 'The image was not found', 'The port was busy'],
          why: '137 = 128 + signal 9 (kill). Check <code>State.OOMKilled</code> with <code>docker inspect</code>.' },
        { q: 'The disk is full, but <code>docker system df</code> shows little usage. What is a likely cause?',
          options: ['Container log files that grow forever because rotation is not configured', 'Too many networks', 'The Docker client is outdated', 'Too many image tags'],
          why: 'Set <code>max-size</code> and <code>max-file</code> for the <code>json-file</code> log driver.' },
        { q: 'You find a live API key in an image that was pushed to a registry. What is the first thing to do?',
          options: ['Change (rotate) the key, because it must be treated as leaked', 'Delete the line from the Dockerfile and rebuild', 'Make the image tag longer', 'Restart the container'],
          why: 'Removing it from the Dockerfile is needed too, but the old image and its copies still contain the key.' },
        { q: 'What is the risk of <code>FROM node:latest</code>?',
          options: ['The base changes over time, so the same Dockerfile gives different results', 'It is slower to download', 'It only works on Mondays', 'It cannot be used with Compose'],
          why: 'Pin a version, for example <code>node:24-alpine</code>.' },
        { q: 'The firewall (<code>ufw</code>) blocks port 5432, yet the database started with <code>-p 5432:5432</code> is reachable from the internet. Why?',
          options: ['Docker adds its own firewall rules, which are applied before those of ufw', 'ufw does not work with Postgres', 'Port 5432 can never be blocked', 'The container runs as root'],
          why: 'Publish on <code>127.0.0.1</code> only, or do not publish the port at all.' },
        { q: 'An image built on an Apple Silicon Mac fails on the server with <code>exec format error</code>. What is wrong?',
          options: ['It was built for ARM processors and the server has an Intel or AMD processor', 'The image is too large', 'The Dockerfile has a syntax error', 'The server has an older Docker version'],
          why: 'Build with <code>--platform linux/amd64</code>, or let CI build on the right processor type.' },
        { q: 'After a server reboot, Docker runs but all containers are stopped. What was missing?',
          options: ['A restart policy such as <code>--restart unless-stopped</code>', 'A larger disk', 'A newer image', 'A published port'],
          why: 'The default restart policy is <code>no</code>.' },
        { q: 'Every <code>docker stop</code> takes exactly ten seconds. What is the usual reason?',
          options: ['The app never receives the stop signal and is killed after the grace period', 'The image is very large', 'The network is slow', 'The disk is full'],
          why: 'Typical cause: <code>CMD</code> written without square brackets, so a shell sits between Docker and the app.' },
        { q: 'After adding <code>USER appuser</code>, the container fails with <code>Permission denied: \'/app/app.py\'</code>. What fixes it?',
          options: ['<code>COPY --chown=appuser:appuser . .</code>', 'Removing the <code>WORKDIR</code> line', 'Publishing more ports', 'Using a bigger base image'],
          why: '<code>COPY</code> makes root the owner and keeps the permissions from your machine, so the new user may not be allowed to read the files.' },
        { q: 'Is a named volume a backup of your database?',
          options: ['No. It disappears with <code>down -v</code>, a volume prune or a dead disk', 'Yes, Docker keeps copies', 'Yes, on Docker Hub', 'Only if it is larger than 1 GB'],
          why: 'A volume protects against removing a container, nothing more. Take real backups and store them elsewhere.' },
      ],
    },
  ];

  const root = document.getElementById('quiz');
  if (!root) return;

  function shuffle(list) {
    const copy = list.slice();
    for (let i = copy.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }

  function moduleOf(id) { return KT.MODULES.find((m) => m.id === id); }

  function bestScores() { return KT.store.get(BEST_KEY, {}); }

  function saveBest(testId, pct) {
    const best = bestScores();
    if (!(testId in best) || pct > best[testId]) {
      best[testId] = pct;
      KT.store.set(BEST_KEY, best);
    }
    if (TESTS.every((test) => (best[test.id] || 0) >= PASS)) KT.setDone('quiz', true);
  }

  function finalExam() {
    const all = TESTS.flatMap((test) => test.questions.map((question) => Object.assign({ module: test.module }, question)));
    return { id: 'final', title: 'Final exam · mixed', questions: shuffle(all).slice(0, FINAL_SIZE) };
  }

  /* ---------- Screens ---------- */

  function showMenu() {
    const best = bestScores();
    const badge = (id) => (id in best
      ? `<span class="badge ${best[id] >= PASS ? 'ok' : 'warn'}">Best: ${best[id]}%</span>`
      : '<span class="badge info">Not tried yet</span>');
    root.innerHTML = `
      <div class="cards">
        ${TESTS.map((test) => `
          <button class="card" type="button" data-test="${test.id}" style="text-align:left;cursor:pointer;font:inherit">
            <span class="tag">${test.questions.length} questions</span>
            <b>${KT.esc(test.title)}</b>
            <small>${badge(test.id)}</small>
          </button>`).join('')}
        <button class="card" type="button" data-test="final" style="text-align:left;cursor:pointer;font:inherit">
          <span class="tag">${FINAL_SIZE} random questions</span>
          <b>Final exam · mixed</b>
          <small>${badge('final')}</small>
        </button>
      </div>
      <p class="widget-note">Pass mark: ${PASS}%. Answers are shuffled every time, so you cannot learn positions by heart. Your best scores are saved in this browser only.</p>`;
    root.querySelectorAll('[data-test]').forEach((button) => button.addEventListener('click', () => {
      const id = button.dataset.test;
      start(id === 'final' ? finalExam() : TESTS.find((test) => test.id === id));
    }));
  }

  function start(test) {
    const questions = test.id === 'final' ? test.questions : shuffle(test.questions);
    const wrong = [];
    let index = 0;
    let score = 0;

    function showQuestion() {
      const question = questions[index];
      const correctText = question.options[0];
      const options = shuffle(question.options);
      const pct = Math.round((index / questions.length) * 100);
      root.innerHTML = `
        <div class="widget">
          <div class="widget-row" style="justify-content:space-between">
            <span class="widget-title" style="margin:0">${KT.esc(test.title)}</span>
            <span class="label">Question ${index + 1} of ${questions.length} · ${pct}%</span>
          </div>
          <div class="progress-bar" style="margin-bottom:16px"><span style="width:${pct}%"></span></div>
          <p class="ex-q" style="font-size:1.08rem">${question.q}</p>
          <div class="ex-options">${options.map((option) => `<button type="button">${option}</button>`).join('')}</div>
          <div class="ex-feedback" aria-live="polite"></div>
          <div class="ex-actions">
            <button class="btn btn-small" type="button" data-quit>Leave test</button>
            <button class="btn btn-primary" type="button" data-next hidden>${index + 1 === questions.length ? 'See my result' : 'Next question →'}</button>
          </div>
        </div>`;
      const buttons = [...root.querySelectorAll('.ex-options button')];
      const feedback = root.querySelector('.ex-feedback');
      const next = root.querySelector('[data-next]');

      buttons.forEach((button, i) => button.addEventListener('click', () => {
        buttons.forEach((b, k) => {
          b.disabled = true;
          if (options[k] === correctText) b.classList.add('is-ok');
        });
        if (options[i] === correctText) {
          score += 1;
          feedback.className = 'ex-feedback ok';
          feedback.innerHTML = `<b>Correct.</b> ${question.why}`;
        } else {
          button.classList.add('is-bad');
          wrong.push({ question, picked: options[i] });
          feedback.className = 'ex-feedback bad';
          feedback.innerHTML = `<b>Not quite.</b> ${question.why}`;
        }
        next.hidden = false;
        next.focus();
      }));
      next.addEventListener('click', () => {
        index += 1;
        if (index < questions.length) showQuestion();
        else showResult();
      });
      root.querySelector('[data-quit]').addEventListener('click', showMenu);
    }

    function showResult() {
      const pct = Math.round((score / questions.length) * 100);
      const passed = pct >= PASS;
      saveBest(test.id, pct);
      const review = wrong.map(({ question, picked }) => {
        const module = moduleOf(question.module || test.module);
        return `<div class="exercise is-wrong">
          <p class="ex-q">${question.q}</p>
          <p><span class="badge danger">Your answer</span> ${picked}</p>
          <p><span class="badge ok">Correct</span> ${question.options[0]}</p>
          <p>${question.why}${module ? ` <a href="${module.file}">Read again: ${KT.esc(module.title)}</a>` : ''}</p>
        </div>`;
      }).join('');
      root.innerHTML = `
        <div class="widget">
          <span class="widget-title">${KT.esc(test.title)} · result</span>
          <p style="font-size:1.6rem;font-weight:700;margin-bottom:4px">${score} of ${questions.length} correct · ${pct}%</p>
          <div class="progress-bar" style="margin-bottom:12px"><span style="width:${pct}%"></span></div>
          <p>${passed ? 'Passed. Well done.' : `Not passed yet. You need ${PASS}%. Read the explanations below and try again.`}</p>
          <div class="ex-actions">
            <button class="btn btn-primary" type="button" data-again>Try this test again</button>
            <button class="btn" type="button" data-menu>All tests</button>
          </div>
        </div>
        ${wrong.length ? `<h3>Questions to review</h3>${review}` : ''}`;
      root.querySelector('[data-again]').addEventListener('click', () => start(test.id === 'final' ? finalExam() : test));
      root.querySelector('[data-menu]').addEventListener('click', showMenu);
      root.scrollIntoView({ block: 'start' });
    }

    showQuestion();
  }

  showMenu();
})();
