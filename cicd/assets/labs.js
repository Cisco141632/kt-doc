/* Small hands-on simulations used by the CI/CD course. */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    initPipelineBuilder();
    initReleaseMission();
  });

  function initPipelineBuilder() {
    const root = document.querySelector('[data-pipeline-builder]');
    if (!root) return;
    const buttons = [...root.querySelectorAll('[data-stage]')];
    const output = root.querySelector('[data-builder-output]');
    const order = ['lint', 'unit', 'build', 'scan', 'publish', 'staging', 'smoke', 'production'];
    const chosen = [];

    function paint(message, kind) {
      output.className = `ex-feedback ${kind || 'hint'}`;
      output.textContent = message;
    }

    buttons.forEach((button) => button.addEventListener('click', () => {
      const stage = button.dataset.stage;
      if (chosen.includes(stage)) return;
      const expected = order[chosen.length];
      if (stage !== expected) {
        paint(`That stage is useful, but not yet. Before “${button.textContent.trim()}”, choose the step that protects or produces its input.`, 'bad');
        return;
      }
      chosen.push(stage);
      button.classList.add('is-on');
      button.disabled = true;
      paint(chosen.length === order.length ? 'Pipeline complete: one tested image can now move safely from commit to production.' : `${chosen.length} of ${order.length} stages placed. Choose what should happen next.`, chosen.length === order.length ? 'ok' : 'hint');
    }));

    const reset = root.querySelector('[data-builder-reset]');
    if (reset) reset.addEventListener('click', () => {
      chosen.splice(0);
      buttons.forEach((button) => { button.disabled = false; button.classList.remove('is-on'); });
      paint('Start with the fastest feedback that can reject a bad change.', 'hint');
    });
  }

  function initReleaseMission() {
    const root = document.querySelector('[data-release-mission]');
    if (!root) return;
    const steps = [...root.querySelectorAll('[data-release-step]')];
    const output = root.querySelector('[data-release-output]');
    let current = 0;
    steps.forEach((button, index) => button.addEventListener('click', () => {
      if (index !== current) {
        output.className = 'ex-feedback bad';
        output.textContent = index < current ? 'That step is already complete.' : 'A required earlier check is still missing. Follow the evidence, not the deployment pressure.';
        return;
      }
      button.classList.add('is-on');
      button.disabled = true;
      current += 1;
      output.className = `ex-feedback ${current === steps.length ? 'ok' : 'hint'}`;
      output.textContent = current === steps.length ? 'Release complete. You preserved the image digest, verified health and kept a rollback target.' : `Evidence recorded. Continue with step ${current + 1}.`;
    }));
  }
})();
