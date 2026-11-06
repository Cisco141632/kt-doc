/* Browser-only, deterministic storage lessons. No credentials or network calls. */
(function () {
  'use strict';
  const M = window.AzureStorageModel;
  if (!M) return;
  let counter = 0;
  const esc = value => String(value).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
  const option = (value, title) => `<option value="${esc(value)}">${esc(title)}</option>`;
  const button = (action, text, primary = false) => `<button class="btn${primary ? ' btn-primary' : ''}" type="button" data-action="${esc(action)}">${esc(text)}</button>`;
  const keyParts = key => {
    const parts = String(key).split('/');
    const rooted = parts[2] === 'media';
    return `<div class="key-parts" aria-label="Blob key segments">${parts.map((part, i) => `<span class="key-part"><small>${rooted && i < 3 ? ['prefix', 'stage', 'media'][i] : 'name segment'}</small><code>${esc(part || '∅')}</code></span>`).join('')}</div>`;
  };
  function complete(id, frame) {
    if (frame.dataset.completed) return;
    frame.dataset.completed = 'true';
    const message = frame.querySelector('[data-completion]');
    if (message) message.textContent = 'Experiment complete — you tested the key idea.';
    document.dispatchEvent(new CustomEvent('azure:lab-complete', { detail: { id } }));
  }
  function frame(el, type, title, intro, controls, output) {
    const uid = `azure-lab-${++counter}`;
    function field(name, title, control) {
      return `<label class="field" for="${uid}-${name}"><span>${esc(title)}</span>${control.replace('data-control=', `id="${uid}-${name}" data-control=`)}</label>`;
    }
    el.innerHTML = `<section class="lab" data-lab-kind="${type}" aria-labelledby="${uid}-title"><div class="lab-head"><span class="chip">Browser simulation · no Azure connection</span><h3 id="${uid}-title">${esc(title)}</h3><p>${esc(intro)}</p></div><div class="lab-controls">${controls(field)}</div><div class="lab-output" role="status" aria-live="polite" aria-atomic="true" data-output>${output || ''}</div><div class="actions">${button('reset', 'Reset experiment')}<span class="muted" data-completion></span></div></section>`;
    const node = el.firstElementChild;
    return { node, output: node.querySelector('[data-output]'), get: name => node.querySelector(`[data-control="${name}"]`), action: name => node.querySelector(`[data-action="${name}"]`) };
  }
  function text(name, value) { return `<input data-control="${name}" type="text" value="${esc(value)}" autocomplete="off" spellcheck="false">`; }
  function select(name, options) { return `<select data-control="${name}">${options.map(([value, title]) => option(value, title)).join('')}</select>`; }
  function number(name, value, min = 0, max = 99999) { return `<input data-control="${name}" type="number" value="${value}" min="${min}" max="${max}" step="1">`; }
  function check(name, checked = true) { return `<input data-control="${name}" type="checkbox"${checked ? ' checked' : ''}>`; }
  function listen(frame, render, types = ['input', 'change']) { types.forEach(type => frame.node.addEventListener(type, event => { if (event.target.matches('input,select')) render(); })); }

  function explorer(el) {
    let blobs = [
      { account: 'demostore', container: 'private-files', key: 'cases/214/a.txt', content: 'Demo original' },
      { account: 'delhistore', container: 'private-files', key: 'cases/214/a.txt', content: 'Delhi original' },
      { account: 'demostore', container: 'private-files', key: 'cases/2140/b.txt', content: 'Different case' }
    ];
    const initial = M.copy(blobs);
    let writes = 0;
    let last = 'Select a place, then write a blob twice. Try the same key in the other account or container.';
    const f = frame(el, 'explorer', 'Find a blob by three things', 'A storage account, a container, and an exact blob key together identify one object. Try prefix cases/214 with and without the final slash.', field => [
      field('account', 'Azure storage account', select('account', [['demostore', 'demostore'], ['delhistore', 'delhistore']])),
      field('container', 'Container', select('container', [['private-files', 'private-files'], ['exports', 'exports']])),
      field('key', 'Blob key — its full name', text('key', 'cases/214/a.txt')),
      field('content', 'Simulated file contents', text('content', 'My revised text')),
      field('prefix', 'List names beginning with', text('prefix', 'cases/214/')),
      button('write', 'Write this blob', true)
    ].join(''));
    function render() {
      const account = f.get('account').value, container = f.get('container').value, key = f.get('key').value;
      const list = M.listBlobs(blobs, account, container, f.get('prefix').value);
      const exact = blobs.find(blob => M.blobIdentity(blob.account, blob.container, blob.key) === M.blobIdentity(account, container, key));
      f.output.innerHTML = `<div class="storage-map"><div class="storage-node is-selected"><b>Account</b><code>${esc(account)}</code><div class="storage-node"><b>Container</b><code>${esc(container)}</code><div class="storage-node"><b>Exact key</b><code>${esc(key || '(empty)')}</code></div></div></div></div><p><b>Exact key contents:</b> ${exact ? esc(exact.content) : 'No blob at this account + container + key.'}</p><p><b>Prefix listing:</b> ${list.length} matching blob${list.length === 1 ? '' : 's'} in this container.</p>${list.length ? `<ul>${list.map(blob => `<li><code>${esc(blob.key)}</code> — ${esc(blob.content)}</li>`).join('')}</ul>` : '<p>No matching names. Listing does not search other accounts or containers.</p>'}<p class="lab-log">${esc(last)}</p><p class="muted">Slashes are part of a blob name in this flat-namespace model. A prefix is a string match, so cases/214 also matches cases/2140.</p>`;
    }
    listen(f, render);
    f.action('write').addEventListener('click', () => {
      const key = f.get('key').value;
      if (!key.trim()) { last = 'Enter a nonempty blob key before writing.'; render(); return; }
      const result = M.putBlob(blobs, { account: f.get('account').value, container: f.get('container').value, key, content: f.get('content').value });
      blobs = result.blobs;
      writes++;
      last = result.overwritten ? 'Overwritten: the existing blob at this exact identity now has the new contents. Other accounts and containers are unchanged.' : 'Created: this is a separate blob because no object existed at this exact identity.';
      render();
      if (writes >= 2) complete('explorer', f.node);
    });
    f.action('reset').addEventListener('click', () => { blobs = M.copy(initial); writes = 0; f.get('account').value = 'demostore'; f.get('container').value = 'private-files'; f.get('key').value = 'cases/214/a.txt'; f.get('content').value = 'My revised text'; f.get('prefix').value = 'cases/214/'; last = 'Experiment reset. Write twice and compare accounts.'; render(); });
    render();
  }

  function sas(el) {
    let sawSuccess = false, sawDenied = false;
    const f = frame(el, 'sas', 'Will this signed link allow the request?', 'Model one blob-scoped grant like the CrimeOS read and write links. The time control is simulated; no real SAS token is generated. All requests here use delhistore / private-files.', field => [
      field('grant-key', 'Blob key covered by the grant', text('grant-key', 'delhi/prod/media/complaint.pdf')),
      field('permissions', 'Granted permissions', select('permissions', [['read', 'Read only'], ['write', 'Write only'], ['read,write', 'Read and write (Azure can combine permissions)']])),
      field('ttl', 'Grant validity in seconds', select('ttl', [['300', '300 seconds — normal file'], ['900', '900 seconds — case bundle'] ])),
      field('request-key', 'Blob key the client requests', text('request-key', 'delhi/prod/media/complaint.pdf')),
      field('operation', 'Requested action', select('operation', [['read', 'Read'], ['write', 'Write']])),
      field('elapsed', 'Seconds elapsed since grant starts', number('elapsed', 0, 0, 1800)),
      button('test', 'Test this request', true)
    ].join(''), '<p>Predict the result, then test. Try a permitted read, then an expired grant or the wrong action.</p>');
    function test() {
      const result = M.sasDecision({ grantedKey: f.get('grant-key').value, requestKey: f.get('request-key').value, permissions: f.get('permissions').value.split(','), operation: f.get('operation').value, elapsed: Number(f.get('elapsed').value), ttl: Number(f.get('ttl').value) });
      f.output.innerHTML = `<div class="storage-node ${result.ok ? 'is-success' : 'is-error'}"><b>${result.ok ? 'Allowed' : 'Denied'} · simulated ${result.status}</b><p>${esc(result.reason)}</p></div><p>Grant covers <code>${esc(f.get('grant-key').value)}</code>; permission <b>${esc(f.get('permissions').value)}</b>; valid before simulated second <b>${esc(f.get('ttl').value)}</b>.</p><p class="muted">This models a narrow CrimeOS grant. Azure also supports container/account scope and other permissions; this lab does not implement every SAS option.</p>`;
      sawSuccess ||= result.ok;
      sawDenied ||= !result.ok;
      if (sawSuccess && sawDenied) complete('sas', f.node);
    }
    f.action('test').addEventListener('click', test);
    ['input', 'change'].forEach(type => f.node.addEventListener(type, event => { if (event.target.matches('input,select')) f.output.innerHTML = '<p>Settings changed. Predict the outcome, then choose “Test this request.”</p>'; }));
    f.action('reset').addEventListener('click', () => { f.get('grant-key').value = 'delhi/prod/media/complaint.pdf'; f.get('permissions').value = 'read'; f.get('ttl').value = '300'; f.get('request-key').value = 'delhi/prod/media/complaint.pdf'; f.get('operation').value = 'read'; f.get('elapsed').value = '0'; sawSuccess = false; sawDenied = false; f.output.innerHTML = '<p>Reset. Test an allowed request and a denied request to finish the experiment.</p>'; });
  }

  function routing(el) {
    const seen = new Set();
    const presets = { customer: 'delhi/prod/media/case-artifacts/214/a.pdf', bare: 'cases/214/ocr_results/a.txt', deployment: 'crimeos-demo/demo/media/case_context_data/214.zip', unknown: 'old-mh/prod/media/case-artifacts/214/a.pdf', boundary: 'delhi/production/media/a.pdf' };
    const f = frame(el, 'routing', 'Watch CrimeOS route a key', 'The routing decision uses the start of the key, not the URL host or the account of the person opening a case. Compare a customer key, a bare key, and a deployment key.', field => [
      field('preset', 'Choose an example', select('preset', [['customer', 'Customer-rooted key'], ['bare', 'Bare OCR key'], ['deployment', 'Deployment-rooted key'], ['unknown', 'Unknown old root'], ['boundary', 'Similar but different stage']])),
      field('key', 'Key to route', text('key', presets.customer)),
      field('prefix', 'Delhi customer storage_prefix', text('prefix', 'delhi')),
      field('stage', 'Delhi customer storage_stage', text('stage', 'prod')),
      field('config', 'Customer mapping', select('config', [['configured', 'Configured: Delhi → delhistore'], ['none', 'Customer storage not configured'], ['conflict', 'Two different connections claim Delhi root'], ['overlap', 'Customer claims deployment root']])),
      button('helper', 'Apply case-owner helper')
    ].join(''));
    let helperNote = '';
    function config() {
      const cfg = M.copy(M.DEMO_CONFIG);
      const root = `${f.get('prefix').value.replace(/\/+$/, '')}/${f.get('stage').value.replace(/^\/+|\/+$/g, '')}/`;
      cfg.accounts[0].root = root;
      if (f.get('config').value === 'none') cfg.accounts = [];
      if (f.get('config').value === 'conflict') cfg.accounts.push({ ...cfg.accounts[0], account: 'otherstore', name: 'Conflicting customer', connectionId: 'other' });
      if (f.get('config').value === 'overlap') cfg.accounts[0].root = cfg.deployment.root;
      return cfg;
    }
    function render() {
      const cfg = config();
      let key;
      try { key = M.keyFromSavedPath(f.get('key').value); }
      catch (_) { f.output.textContent = 'That saved URL could not be parsed. Enter a blob key or an HTTP(S) URL containing a container and blob path.'; return; }
      const result = M.routeKey(key, cfg);
      seen.add(result.reason);
      f.output.innerHTML = `<p><b>Selected storage:</b> <code>${esc(result.account)}</code> / <code>${esc(result.container)}</code></p><p><b>Reason:</b> ${esc({ 'account-root': 'Customer root matched', 'deployment-root': 'Deployment root matched first', fallback: 'No root matched — silent deployment fallback', conflict: 'Conflicting root mappings — deployment fallback' }[result.reason])}</p>${keyParts(key)}<ol>${result.steps.map(step => `<li class="route-step">${esc(step.replace(/^\d\. /, ''))}</li>`).join('')}</ol><div class="storage-map">${[cfg.deployment, ...cfg.accounts].map(target => `<div class="storage-node${target.account === result.account ? ' is-selected' : ''}"><b>${esc(target.name)}</b><code>${esc(target.account)}</code><small>Root: ${esc(target.root)}</small></div>`).join('')}</div>${helperNote ? `<p class="lab-log">${esc(helperNote)}</p>` : ''}<p class="muted">Mappings in the guide are cached for 60 seconds. This simulation applies changes immediately and does not model waiting or validate production configuration. A key is a blob name; it is not an Azure access key.</p>`;
      if (seen.has('account-root') && seen.has('fallback') && seen.has('deployment-root')) complete('routing', f.node);
    }
    f.get('preset').addEventListener('change', () => { f.get('key').value = presets[f.get('preset').value]; helperNote = ''; render(); });
    listen(f, render);
    f.action('helper').addEventListener('click', () => {
      const cfg = config();
      const before = f.get('key').value;
      const root = cfg.accounts[0] ? cfg.accounts[0].root : cfg.deployment.root;
      const after = M.keyForOwner(before, root, cfg);
      f.get('key').value = after;
      helperNote = before === after ? 'Unchanged. The helper replaces the deployment media root only. A bare key stays bare, and an already customer-rooted key stays as saved.' : `Helper replaced the deployment media root with the case owner root: ${after}`;
      render();
    });
    f.action('reset').addEventListener('click', () => { f.get('preset').value = 'customer'; f.get('key').value = presets.customer; f.get('prefix').value = 'delhi'; f.get('stage').value = 'prod'; f.get('config').value = 'configured'; helperNote = ''; seen.clear(); render(); });
    render();
  }

  function paths(el) {
    let sawSaved = false, sawBuilt = false;
    const f = frame(el, 'paths', 'Change a case ID without moving a file', 'Compare a saved original PDF pointer with a regenerable case bundle key. The object checkbox refers to the key currently selected for reading.', field => [
      field('mode', 'File behavior', select('mode', [['saved', 'Saved original PDF path'], ['built', 'Built case bundle path']])),
      field('old-id', 'Case ID when the file was saved', number('old-id', 214, 1, 999999)),
      field('new-id', 'Current database case ID', number('new-id', 9001, 1, 999999)),
      field('exists', 'Blob exists at the selected read key', check('exists')),
      field('validator', 'Guard wrongly expects current-ID prefix', check('validator', false))
    ].join(''));
    function render() {
      const oldId = Number(f.get('old-id').value), newId = Number(f.get('new-id').value);
      if (!Number.isInteger(oldId) || !Number.isInteger(newId) || oldId < 1 || newId < 1) { f.output.textContent = 'Enter positive whole case IDs.'; return; }
      const mode = f.get('mode').value;
      const result = M.pathDecision({ mode, oldId, newId, blobExists: f.get('exists').checked, validator: f.get('validator').checked });
      f.output.innerHTML = `<div class="lab-grid"><div class="storage-node"><b>Original saved pointer</b><code>${esc(result.savedKey)}</code><small>Stored in CaseArtifact metadata</small></div><div class="storage-node"><b>Bundle key built now</b><code>${esc(result.builtKey)}</code><small>Computed from current case ID</small></div></div><p><b>Read key:</b> <code>${esc(result.readKey)}</code></p><div class="storage-node ${result.ok ? 'is-success' : 'is-error'}"><b>${esc(result.state.toUpperCase())}</b><p>${esc(result.reason)}</p></div><p class="muted">The bad guard toggle applies to saved paths. Real ownership and access checks remain necessary; the lesson is to avoid assuming that every saved path contains the current database ID.</p>`;
      if (mode === 'saved' && result.state === 'missing') sawSaved = true;
      if (mode === 'built' && result.state === 'rebuilt') sawBuilt = true;
      if (sawSaved && sawBuilt) complete('paths', f.node);
    }
    listen(f, render);
    f.action('reset').addEventListener('click', () => { f.get('mode').value = 'saved'; f.get('old-id').value = '214'; f.get('new-id').value = '9001'; f.get('exists').checked = true; f.get('validator').checked = false; sawSaved = false; sawBuilt = false; render(); });
    render();
  }

  function journey(el) {
    let current = 0;
    const visited = new Set([0]);
    const f = frame(el, 'journey', 'Follow complaint.pdf through the system', 'Advance one action at a time. Watch who decides the key, who writes the bytes, and what the database records. Example names and IDs are fictional.', () => `${button('previous', '← Previous step')}${button('next', 'Next step →', true)}`);
    function render() {
      const step = M.JOURNEY[current];
      f.output.innerHTML = `<p class="eyebrow">Step ${current + 1} of ${M.JOURNEY.length} · ${esc(step.actor)}</p><h4>${esc(step.title)}</h4><p>${esc(step.action)}</p><div class="journey-steps" aria-label="PDF journey">${M.JOURNEY.map((value, i) => `<span class="journey-step${i === current ? ' is-active' : ''}"${i === current ? ' aria-current="step"' : ''}><b>${i + 1}</b> ${esc(value.title)}</span>`).join('')}</div><div class="lab-grid"><div class="storage-node"><b>Key in this action</b><code>${esc(step.key)}</code></div><div class="storage-node"><b>Database now</b><p>${esc(step.database)}</p></div><div class="storage-node"><b>Blob state now</b><p>${esc(step.objects)}</p></div></div><p class="muted">Throughout this sequence, storage credentials stay in the backend. Browser and AI use only scoped, temporary grants.</p>`;
      f.action('previous').disabled = current === 0;
      f.action('next').disabled = current === M.JOURNEY.length - 1;
      if (visited.size === M.JOURNEY.length) complete('journey', f.node);
    }
    f.action('previous').addEventListener('click', () => { current = Math.max(0, current - 1); visited.add(current); render(); });
    f.action('next').addEventListener('click', () => { current = Math.min(M.JOURNEY.length - 1, current + 1); visited.add(current); render(); });
    f.action('reset').addEventListener('click', () => { current = 0; visited.clear(); visited.add(0); render(); });
    render();
  }

  function migration(el) {
    let sawMissing = false, sawFound = false;
    const f = frame(el, 'migration', 'Move database rows and blobs separately', 'Model an MH-to-demo migration using keep_urls. A blob copy here targets MH customer storage with identical keys; deployment storage is a separate destination.', field => [
      field('database', 'Copy the case rows and saved path text', check('database')),
      field('blobs', 'Copy blob bytes to MH customer storage', check('blobs', false)),
      field('root', 'Destination MH account matches the saved root', check('root')),
      field('bundle', 'Exclude CaseAIData so bundle can rebuild', check('bundle')),
      field('offset', 'Apply ID offset: case 214 becomes 9001', check('offset')),
      field('bare', 'Use bare OCR saved key instead of routed PDF', check('bare', false))
    ].join(''));
    function render() {
      const result = M.migrationDecision({ dbCopied: f.get('database').checked, blobsCopied: f.get('blobs').checked, sameRoot: f.get('root').checked, excludeBundle: f.get('bundle').checked, idOffset: f.get('offset').checked, bareKey: f.get('bare').checked });
      f.output.innerHTML = `<div class="lab-grid"><div class="storage-node"><b>Saved pointer after keep_urls</b><code>${esc(result.savedKey)}</code><p>The old ID remains in this saved text.</p></div><div class="storage-node"><b>Bundle key for current case</b><code>${esc(result.bundleKey)}</code><p>Built by application code from the current ID.</p></div></div><p><b>Saved-file read routes to:</b> ${esc(result.route)}</p><div class="storage-map"><div class="storage-node ${result.savedOk ? 'is-success' : 'is-error'}"><b>Saved file</b><p>${esc(result.saved)}</p></div><div class="storage-node ${result.bundleOk ? 'is-success' : ''}"><b>Case bundle</b><p>${esc(result.bundle)}</p></div></div><p class="lab-log">${esc(result.reason)}</p><p class="muted">Rebuild happens when the backend's supported rebuild path runs. Migrating rows does not make Azure recreate a missing file. Copying an existing CaseAIData row needs a separate audit of its state and references.</p>`;
      if (f.get('database').checked) { sawMissing ||= !result.savedOk; sawFound ||= result.savedOk; }
      if (sawMissing && sawFound) complete('migration', f.node);
    }
    listen(f, render);
    f.action('reset').addEventListener('click', () => { f.get('database').checked = true; f.get('blobs').checked = false; f.get('root').checked = true; f.get('bundle').checked = true; f.get('offset').checked = true; f.get('bare').checked = false; sawMissing = false; sawFound = false; render(); });
    render();
  }

  function debugging(el) {
    const solved = new Set();
    let revealed = new Set(), feedback = '';
    const evidenceNames = { path: '1. Inspect saved path', route: '2. Trace storage routing', object: '3. Inspect exact blob location', access: '4. Inspect grant and response', validator: '5. Inspect application guard' };
    const f = frame(el, 'debugging', 'Diagnose a failed file read', 'Gather evidence before choosing a cause. A storage 403, a 404, and an application-side rejection need different investigations.', field => [
      field('scenario', 'Incident to investigate', select('scenario', M.DEBUG_CASES.map(value => [value.id, value.title]))),
      `<div class="actions">${Object.entries(evidenceNames).map(([key, title]) => button('evidence-' + key, title)).join('')}</div>`,
      field('diagnosis', 'Your diagnosis', select('diagnosis', [['', 'Choose after inspecting evidence'], ['route', 'Wrong selected storage account'], ['missing', 'Blob bytes were not copied'], ['expired', 'Signed link expired'], ['validator', 'Current-ID guard rejects saved path']])),
      button('diagnose', 'Check diagnosis', true)
    ].join(''));
    function incident() { return M.DEBUG_CASES.find(value => value.id === f.get('scenario').value); }
    function render() {
      const value = incident();
      f.output.innerHTML = `<h4>${esc(value.title)}</h4>${revealed.size ? `<ol class="lab-log">${Object.entries(evidenceNames).filter(([key]) => revealed.has(key)).map(([key, title]) => `<li><b>${esc(title.replace(/^\d\. /, ''))}:</b> ${esc(value.evidence[key])}</li>`).join('')}</ol>` : '<p>No evidence inspected yet. Start with the saved path and trace where it is read.</p>'}${feedback ? `<p class="feedback">${esc(feedback)}</p>` : ''}<p class="muted">Solved ${solved.size} of ${M.DEBUG_CASES.length} incidents. In real Azure, inspect the exact error code and request details; status alone is not a complete diagnosis.</p>`;
    }
    Object.keys(evidenceNames).forEach(key => f.action('evidence-' + key).addEventListener('click', () => { revealed.add(key); f.action('evidence-' + key).setAttribute('aria-pressed', 'true'); render(); }));
    function resetEvidence() { revealed = new Set(); feedback = ''; f.get('diagnosis').value = ''; Object.keys(evidenceNames).forEach(key => f.action('evidence-' + key).setAttribute('aria-pressed', 'false')); render(); }
    f.get('scenario').addEventListener('change', resetEvidence);
    f.action('diagnose').addEventListener('click', () => {
      const value = incident();
      if (revealed.size < 2) { feedback = 'Inspect at least two pieces of evidence before checking your diagnosis.'; render(); return; }
      if (!f.get('diagnosis').value) { feedback = 'Choose a diagnosis first.'; render(); return; }
      if (f.get('diagnosis').value === value.cause) { solved.add(value.id); feedback = 'Correct. ' + value.explanation; } else feedback = 'That cause does not fit all the evidence. ' + value.explanation;
      render();
      if (solved.size === M.DEBUG_CASES.length) complete('debugging', f.node);
    });
    f.action('reset').addEventListener('click', () => { solved.clear(); f.get('scenario').value = M.DEBUG_CASES[0].id; resetEvidence(); });
    resetEvidence();
  }

  const mounts = { explorer, sas, routing, paths, journey, migration, debugging };
  function mountAll(scope = document) {
    scope.querySelectorAll('[data-lab]').forEach(el => {
      if (el.dataset.labMounted || !mounts[el.dataset.lab]) return;
      el.dataset.labMounted = 'true';
      mounts[el.dataset.lab](el);
    });
  }
  window.AzureStorageLabs = { mountAll, types: Object.keys(mounts) };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => mountAll());
  else mountAll();
})();
