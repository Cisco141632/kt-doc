(function () {
  'use strict';

  const QUESTIONS = [
    { module: 'index.html', topic: 'CI/CD', q: 'Tests and packaging are automatic, but production needs human approval. What practice is this?', options: ['Continuous delivery', 'Continuous deployment', 'Manual integration', 'Infrastructure drift'], correct: 0, why: 'The release is always ready, but a deliberate approval remains before production.' },
    { module: 'foundations.html', topic: 'Pipeline', q: 'Lint and unit tests do not depend on each other. What is the best pipeline shape?', options: ['Run them in parallel', 'Run every job on one permanent runner', 'Deploy before either check', 'Combine them with production approval'], correct: 0, why: 'Parallel independent checks shorten the critical path while preserving evidence.' },
    { module: 'foundations.html', topic: 'Artifacts', q: 'A build job creates a binary needed by an isolated deploy job. What must happen?', options: ['Upload/download it as an artifact', 'Assume every runner shares a disk', 'Paste it into a log', 'Disable runner isolation'], correct: 0, why: 'Jobs are normally isolated. Explicit artifact transfer makes the dependency reproducible.' },
    { module: 'continuous-integration.html', topic: 'CI', q: 'A test fails one run in twenty without a code change. What is the correct response?', options: ['Assign ownership, diagnose it and quarantine only with a deadline', 'Retry forever and keep it required', 'Delete all tests', 'Ignore every CI failure'], correct: 0, why: 'Flaky gates destroy trust. They require a tracked repair, not silent acceptance.' },
    { module: 'continuous-integration.html', topic: 'Testing', q: 'Which check best detects an application/database schema incompatibility?', options: ['Integration test with the real database boundary', 'Formatter', 'Unit test with every dependency mocked', 'Markdown link checker'], correct: 0, why: 'The real integration boundary reveals behavior that a mock can conceal.' },
    { module: 'docker-artifacts.html', topic: 'Artifact', q: 'Staging passed image digest sha256:abc. What should production run?', options: ['The same sha256:abc digest', 'A newly rebuilt image from the same branch', 'Whatever latest points to', 'A developer laptop build'], correct: 0, why: 'Rebuilding changes the artifact. Promotion preserves the exact verified content.' },
    { module: 'docker-artifacts.html', topic: 'Identity', q: 'Why is latest a weak production deployment reference?', options: ['It can point to different content over time', 'Docker cannot pull it', 'It is always larger', 'It disables networking'], correct: 0, why: 'A movable tag makes audit and rollback ambiguous. Use an immutable tag and record the digest.' },
    { module: 'delivery-environments.html', topic: 'Delivery', q: 'When should a protected production job receive production secrets?', options: ['After its environment protection rules pass', 'During every pull request', 'Before code checkout', 'In the Dockerfile'], correct: 0, why: 'Delay privileged access until the job is authorized to deploy.' },
    { module: 'delivery-environments.html', topic: 'Database', q: 'Old and new application instances coexist during a rolling update. What must a migration support?', options: ['Both application versions during the overlap', 'Only the new version', 'Only a developer laptop', 'No application version'], correct: 0, why: 'Expand-and-contract changes keep both versions compatible until rollout and cleanup finish.' },
    { module: 'deployment-strategies.html', topic: 'Deployment', q: 'You want to expose 1% of traffic and compare new-version metrics. Which strategy fits?', options: ['Canary', 'Recreate', 'Nightly backup', 'Static analysis'], correct: 0, why: 'A canary limits initial exposure and uses version-specific evidence to decide progression.' },
    { module: 'deployment-strategies.html', topic: 'Rollback', q: 'Why can an application rollback still fail?', options: ['The old code may be incompatible with already changed data', 'The old image is always deleted by Docker', 'Rollback changes DNS permanently', 'Git does not retain commits'], correct: 0, why: 'Code rollback does not undo schema or data changes.' },
    { module: 'security.html', topic: 'Security', q: 'A production API key appears in Git history. What is the first response?', options: ['Revoke or rotate it', 'Only add the file to .gitignore', 'Rename the variable', 'Hide the current commit'], correct: 0, why: 'Any exposed credential must be treated as compromised; removing text cannot invalidate copies.' },
    { module: 'security.html', topic: 'Permissions', q: 'What should an untrusted fork pull request receive?', options: ['Read-only source access and no production secrets', 'Cloud administrator keys', 'Registry delete access', 'The production kubeconfig'], correct: 0, why: 'Pull-request code is executable input. Privileged credentials would create a direct compromise path.' },
    { module: 'iac-gitops.html', topic: 'GitOps', q: 'A manual cluster edit conflicts with Git. What will a reconciliation controller normally do?', options: ['Restore the declared Git state', 'Rewrite Git automatically in every case', 'Disable all deployments', 'Rebuild the application image'], correct: 0, why: 'GitOps controllers continuously work toward the declared desired state.' },
    { module: 'iac-gitops.html', topic: 'IaC', q: 'Why review an infrastructure plan?', options: ['It previews additions, changes and deletions before apply', 'It guarantees zero cloud cost', 'It replaces state', 'It encrypts every application secret'], correct: 0, why: 'A plan makes the proposed infrastructure difference reviewable before mutation.' },
    { module: 'observability.html', topic: 'Verification', q: 'The deployment command exited successfully. Is the release complete?', options: ['No; verify readiness, smoke behavior and version-specific health', 'Yes; exit code is all user evidence', 'Yes; if CPU is nonzero', 'No; rebuild the image first'], correct: 0, why: 'A platform accepting a change is not proof that users can complete critical work.' },
    { module: 'observability.html', topic: 'Telemetry', q: 'Why attach the image digest/version to logs and metrics?', options: ['To compare new and stable behavior', 'To reduce network latency automatically', 'To replace health checks', 'To hide errors'], correct: 0, why: 'Version dimensions connect production behavior to the exact release.' },
    { module: 'observability.html', topic: 'Performance', q: 'Which pair balances delivery throughput and stability?', options: ['Lead time and change failure rate', 'Lines of code and developer age', 'Image name and branch color', 'Number of meetings and tickets'], correct: 0, why: 'Delivery health combines speed measures with failure/recovery measures.' },
  ];

  const root = document.getElementById('quiz');
  if (!root || !window.CICDKT) return;
  let answered = 0;
  let correct = 0;

  function shuffle(items) {
    return items.map((item) => ({ item, key: Math.random() })).sort((a, b) => a.key - b.key).map(({ item }) => item);
  }

  const score = document.createElement('div');
  score.className = 'ex-score is-sticky';
  score.innerHTML = '<b>Score</b><span data-score>0 / 0 answered</span><div class="progress-bar"><span style="width:0%"></span></div>';
  root.appendChild(score);

  QUESTIONS.forEach((question, questionIndex) => {
    const exercise = document.createElement('article');
    exercise.className = 'exercise';
    const options = shuffle(question.options.map((label, originalIndex) => ({ label, originalIndex })));
    exercise.innerHTML = `<div class="ex-head"><span class="badge info">${question.topic}</span><span>Question ${questionIndex + 1} of ${QUESTIONS.length}</span></div>
      <p class="ex-q">${question.q}</p><div class="ex-options"></div><p class="ex-feedback"></p>`;
    const optionRoot = exercise.querySelector('.ex-options');
    const feedback = exercise.querySelector('.ex-feedback');
    options.forEach((option) => {
      const button = document.createElement('button'); button.type = 'button'; button.innerHTML = option.label;
      button.addEventListener('click', () => {
        if (exercise.dataset.answered) return;
        exercise.dataset.answered = 'true'; answered += 1;
        const isCorrect = option.originalIndex === question.correct;
        if (isCorrect) correct += 1;
        exercise.classList.add(isCorrect ? 'is-correct' : 'is-wrong');
        [...optionRoot.children].forEach((candidate) => { candidate.disabled = true; if (Number(candidate.dataset.index) === question.correct) candidate.classList.add('is-ok'); });
        if (!isCorrect) button.classList.add('is-bad');
        feedback.className = `ex-feedback ${isCorrect ? 'ok' : 'bad'}`;
        feedback.innerHTML = `<b>${isCorrect ? 'Correct.' : 'Review this.'}</b> ${question.why} <a href="${question.module}">Open the related lesson →</a>`;
        updateScore();
      });
      button.dataset.index = option.originalIndex; optionRoot.appendChild(button);
    });
    root.insertBefore(exercise, score);
  });

  const reset = document.createElement('button'); reset.type = 'button'; reset.className = 'btn btn-small'; reset.textContent = 'Restart quiz'; reset.addEventListener('click', () => window.location.reload());
  score.appendChild(reset);

  function updateScore() {
    const pct = answered ? Math.round((correct / answered) * 100) : 0;
    score.querySelector('[data-score]').textContent = `${correct} correct · ${answered} / ${QUESTIONS.length} answered`;
    score.querySelector('.progress-bar span').style.width = `${Math.round((answered / QUESTIONS.length) * 100)}%`;
    if (answered === QUESTIONS.length) {
      const finalPct = Math.round((correct / QUESTIONS.length) * 100);
      score.querySelector('[data-score]').textContent = `${correct} / ${QUESTIONS.length} · ${finalPct}% ${finalPct >= 80 ? '· Passed' : '· Review and retry'}`;
      if (finalPct >= 80) window.CICDKT.setDone('quiz', true);
    }
  }
})();
