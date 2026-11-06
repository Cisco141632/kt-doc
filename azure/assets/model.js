/* Teaching model for the supplied 2026-11-06 CrimeOS guide. No Azure requests. */
(function (root, factory) {
  'use strict';
  const model = factory();
  if (typeof module === 'object' && module.exports) module.exports = model;
  if (root) root.AzureStorageModel = model;
})(typeof window !== 'undefined' ? window : null, function () {
  'use strict';
  const DEMO_CONFIG = Object.freeze({
    deployment: { root: 'crimeos-demo/demo/', account: 'demostore', container: 'private-files', name: 'Demo deployment', connectionId: 'deployment' },
    accounts: [
      { root: 'delhi/prod/', account: 'delhistore', container: 'private-files', name: 'Delhi customer', connectionId: 'delhi' },
      { root: 'maha/prod/', account: 'mahastore', container: 'private-files', name: 'MH customer', connectionId: 'maha' }
    ]
  });
  const copy = value => JSON.parse(JSON.stringify(value));
  function rootOf(value) { return String(value || '').replace(/\/+$/, '') + '/'; }
  function routeKey(key, config = DEMO_CONFIG) {
    key = String(key);
    const deployment = config.deployment;
    const steps = [];
    const finish = (target, reason, warning = '') => ({ ...target, key, reason, warning, steps });
    if (key.startsWith(rootOf(deployment.root))) {
      steps.push('1. The key starts with the deployment stage root. Deployment storage wins before customer lookup.');
      return finish(deployment, 'deployment-root');
    }
    steps.push('1. The deployment stage root does not match.');
    const matches = config.accounts.filter(account => key.startsWith(rootOf(account.root)));
    if (matches.length) {
      const distinctConnections = new Set(matches.map(account => account.connectionId || account.account));
      if (distinctConnections.size > 1) {
        steps.push('2. Conflicting customer mappings match this root. The guide says the backend logs an error.');
        steps.push('3. Fall back to the deployment connection.');
        return finish(deployment, 'conflict', 'Conflicting root: deployment fallback; error logged.');
      }
      steps.push('2. A customer prefix/stage root matches at the start of the key.');
      return finish(matches[0], 'account-root');
    }
    steps.push('2. No customer prefix/stage root matches.');
    steps.push('3. Silently use deployment storage. A customer owning the case does not repair a bare key.');
    return finish(deployment, 'fallback', 'Unmatched key: silent deployment fallback.');
  }
  function keyForOwner(legacyKey, ownerRoot, config = DEMO_CONFIG) {
    const media = rootOf(config.deployment.root) + 'media/';
    return String(legacyKey).startsWith(media) ? rootOf(ownerRoot) + 'media/' + String(legacyKey).slice(media.length) : String(legacyKey);
  }
  function keyFromSavedPath(path) {
    const text = String(path || '');
    if (!/^https?:\/\//i.test(text)) return text;
    const url = new URL(text);
    return url.pathname.replace(/^\//, '').split('/').slice(1).join('/');
  }
  function blobIdentity(account, container, key) { return JSON.stringify([account, container, key]); }
  function putBlob(blobs, blob) {
    const identity = blobIdentity(blob.account, blob.container, blob.key);
    const existing = blobs.findIndex(value => blobIdentity(value.account, value.container, value.key) === identity);
    const next = blobs.map(value => ({ ...value }));
    if (existing >= 0) next[existing] = { ...blob };
    else next.push({ ...blob });
    return { blobs: next, overwritten: existing >= 0 };
  }
  function listBlobs(blobs, account, container, prefix) {
    return blobs.filter(blob => blob.account === account && blob.container === container && blob.key.startsWith(prefix));
  }
  function sasDecision({ grantedKey, requestKey, permissions, operation, elapsed, ttl }) {
    if (!Number.isFinite(Number(ttl)) || Number(ttl) <= 0 || !Number.isFinite(Number(elapsed)) || Number(elapsed) < 0) return { ok: false, status: 403, reason: 'Invalid simulated time window.' };
    if (Number(elapsed) >= Number(ttl)) return { ok: false, status: 403, reason: 'The signed link has expired. Ask the backend for a new link; changing the URL expiry does not create a valid signature.' };
    if (grantedKey !== requestKey) return { ok: false, status: 403, reason: 'Wrong resource. This simulated grant covers one exact blob key, not another file or every file under a prefix.' };
    if (!permissions.includes(operation)) return { ok: false, status: 403, reason: 'Permission mismatch. A read grant does not authorize writing, and a write grant does not authorize reading.' };
    return { ok: true, status: operation === 'write' ? 201 : 200, reason: 'Resource, permission, and time window match. This is an access decision only; a real read also needs an existing blob.' };
  }
  function pathDecision({ mode = 'saved', oldId = 214, newId = 9001, blobExists = true, validator = false }) {
    const savedKey = `delhi/prod/media/case-artifacts/${oldId}/upload/complaint.pdf`;
    const builtKey = `delhi/prod/media/case_context_data/${newId}.zip`;
    const readKey = mode === 'saved' ? savedKey : builtKey;
    if (mode === 'saved' && validator && String(oldId) !== String(newId)) return { savedKey, builtKey, readKey, ok: false, state: 'rejected', reason: 'The application rejects an old-ID saved path because its guard rebuilds the expected prefix from the current ID. This happens before Azure is read.' };
    if (mode === 'saved') return { savedKey, builtKey, readKey, ok: blobExists, state: blobExists ? 'found' : 'missing', reason: blobExists ? 'Read the saved old-ID key exactly. An ID change alone does not rename an existing blob.' : 'The original PDF is missing at its saved key. A database row contains a pointer, not the PDF bytes; this saved file cannot be reconstructed from the pointer.' };
    return { savedKey, builtKey, readKey, ok: true, state: blobExists ? 'found' : 'rebuilt', reason: blobExists ? 'The bundle is read at the key built from the current ID.' : 'On the supported bundle rebuild path, the backend can generate a new ZIP from migrated case data at the current-ID key. Rebuilding is application behavior, not an Azure feature.' };
  }
  function migrationDecision({ dbCopied = true, blobsCopied = false, sameRoot = true, excludeBundle = true, bareKey = false, idOffset = true }) {
    const currentId = idOffset ? 9001 : 214;
    const savedKey = bareKey ? 'cases/214/ocr_results/a.txt' : 'maha/prod/media/case-artifacts/214/upload/complaint.pdf';
    const destinationRoot = sameRoot ? 'maha/prod/media' : 'mh-demo/demo/media';
    const bundleKey = `${destinationRoot}/case_context_data/${currentId}.zip`;
    if (!dbCopied) return { savedKey, bundleKey, saved: 'No migrated row', bundle: 'No migrated case to build from', savedOk: false, bundleOk: false, route: 'No read requested', reason: 'Copying blobs alone does not create case rows or saved pointers in the destination database.' };
    const savedOk = blobsCopied && sameRoot && !bareKey;
    return { savedKey, bundleKey, saved: savedOk ? 'Found at its unchanged saved key' : 'Missing in the selected destination storage', bundle: excludeBundle ? `Rebuild can be triggered under case ${currentId}` : 'Copied bundle metadata needs inspection; a rebuild is not guaranteed', savedOk, bundleOk: excludeBundle, route: bareKey || !sameRoot ? 'Demo deployment storage' : 'MH customer storage', reason: bareKey ? 'This lab copies blobs to customer storage. A bare OCR key still routes to destination deployment storage, so the copied customer blob is not found there. A separate copy to the selected deployment container would be needed.' : !sameRoot ? 'The destination root differs from the saved key. The saved key lookup misses and silently falls back to deployment storage, even if the PDF bytes were copied to customer storage. A newly built bundle uses the destination account’s new root instead.' : !blobsCopied ? 'keep_urls moves the saved text only. The PDF must be copied separately with the same key. The bundle can be regenerated when the migrated case has no CaseAIData row and the rebuild path runs.' : 'The saved PDF keeps its old-ID key. Separately copied bytes and matching root make it readable; the rebuilt bundle uses the current ID. No saved path is rewritten by keep_urls.' };
  }
  const JOURNEY = [
    { actor: 'Browser', title: 'Choose the original', action: 'The officer selects complaint.pdf for case 9001. Choosing a file does not upload it.', key: 'No storage key yet', database: 'No artifact row yet', objects: 'No uploaded blob yet' },
    { actor: 'Backend', title: 'Choose the key and grant upload', action: 'Resolve case ownership and call key_for_case. Sign a short-lived write link for the resulting original key.', key: 'delhi/prod/media/case-artifacts/9001/upload/complaint.pdf', database: 'No completed upload recorded yet', objects: 'Original upload not complete' },
    { actor: 'Browser → Azure', title: 'Upload directly', action: 'The browser writes PDF bytes directly to the customer blob using the backend-issued write link.', key: 'delhi/prod/media/case-artifacts/9001/upload/complaint.pdf', database: 'Upload completion still needs recording', objects: 'Original PDF exists in customer storage' },
    { actor: 'Backend → Database', title: 'Save the original pointer', action: 'Record the original URL in the CaseArtifact metadata. The database stores the address, not the PDF bytes.', key: 'delhi/prod/media/case-artifacts/9001/upload/complaint.pdf', database: 'CaseArtifact.meta_data.file_url = original URL', objects: 'Original PDF exists' },
    { actor: 'Backend → AI', title: 'Grant a read of the original', action: 'The backend supplies a signed read link for the original PDF. The AI receives no storage connection string.', key: 'delhi/prod/media/case-artifacts/9001/upload/complaint.pdf', database: 'Original file_url remains saved', objects: 'AI can read the original while the grant is valid' },
    { actor: 'AI → Backend', title: 'Request a derived write', action: 'After extracting text, the AI calls storage_grants with WRITE_DERIVED, case_id, run_id, and file_names. The backend authenticates and validates the request.', key: 'Backend has not granted the derived key yet', database: 'extracted_text_key not saved yet', objects: 'Original exists; derived text not uploaded' },
    { actor: 'Backend → AI', title: 'Grant the derived key', action: 'The backend decides the derived key under the same case owner and returns its write link and exact key.', key: 'delhi/prod/media/case-artifacts/9001/run-1/derived/complaint_pages_1-3.md', database: 'Derived key not saved until completion', objects: 'A grant authorizes a future write; it does not create the file' },
    { actor: 'AI → Azure → Backend', title: 'Write and report completion', action: 'The AI writes Markdown directly with the grant, then reports the backend-issued key. It does not invent a new key.', key: 'delhi/prod/media/case-artifacts/9001/run-1/derived/complaint_pages_1-3.md', database: 'Completion callback ready for persistence', objects: 'Original PDF and extracted Markdown exist' },
    { actor: 'Backend → Database', title: 'Save the derived pointer', action: 'Save the returned key as extracted_text_key. Later readers use this exact saved key, even if the case database ID changes.', key: 'delhi/prod/media/case-artifacts/9001/run-1/derived/complaint_pages_1-3.md', database: 'CaseArtifact.meta_data.extracted_text_key = returned key', objects: 'Both blobs stay in case-owner storage' }
  ];
  const DEBUG_CASES = [
    { id: 'route', title: 'OCR exists, but the app cannot read it', evidence: { path: 'Saved key: cases/214/ocr_results/a.txt (bare).', route: 'No prefix/stage matches. The reader selects Demo deployment storage.', object: 'The blob exists only in MH customer storage; it is absent from Demo deployment storage.', access: 'Fresh grant, correct read permission. Storage read returns 404 BlobNotFound.', validator: 'No current-ID guard runs on this path.' }, cause: 'route', explanation: 'The exact key is being read from the wrong storage account. A customer owning the case does not route a bare key. Inspect the routed destination before searching by file name.' },
    { id: 'missing', title: 'Migrated original PDF is missing', evidence: { path: 'Saved key: maha/prod/media/case-artifacts/214/upload/complaint.pdf.', route: 'MH root matches. The reader selects MH customer storage.', object: 'Destination container lacks this exact key. Database copied; PDF bytes were never copied.', access: 'Fresh read grant. Read returns 404 BlobNotFound.', validator: 'Saved old-ID key is accepted; no guard rejects it.' }, cause: 'missing', explanation: 'Routing is correct, but the PDF bytes are absent. Copying the database and keep_urls preserve only the pointer. A saved original is not rebuilt from its metadata.' },
    { id: 'expired', title: 'AI read fails after waiting', evidence: { path: 'Exact routed key matches the key in the grant.', route: 'Delhi customer root selects Delhi customer storage.', object: 'The blob exists at the selected storage account, container, and key.', access: 'Grant duration 300 seconds; AI starts at simulated second 301. Azure returns 403 authentication failure.', validator: 'No application guard rejects the key.' }, cause: 'expired', explanation: 'This is an authorization failure: the grant expired. Obtain a fresh scoped link from the backend. A 403 is not evidence that a blob is missing; 404 BlobNotFound is a different response.' },
    { id: 'validator', title: 'Original exists after the case ID changed', evidence: { path: 'Saved artifact key contains old case ID 214; the current database case ID is 9001.', route: 'Delhi root still selects the correct customer storage.', object: 'The original exists at its exact saved old-ID key.', access: 'No Azure request is made; the application rejects the path first.', validator: 'Application expects a prefix rebuilt with /9001/ and rejects the saved /214/ key.' }, cause: 'validator', explanation: 'The application guard is wrong for this saved-path read. Validate the stored association and read its saved key. Merely changing a database ID does not rename the blob, and this failure occurs before an Azure status exists.' }
  ];
  return { DEMO_CONFIG, copy, routeKey, keyForOwner, keyFromSavedPath, blobIdentity, putBlob, listBlobs, sasDecision, pathDecision, migrationDecision, JOURNEY, DEBUG_CASES };
});
