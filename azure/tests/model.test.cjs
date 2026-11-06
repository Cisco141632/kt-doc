'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const M = require('../assets/model.js');

test('the three-part identity separates accounts, containers, and exact names', () => {
  let state = [];
  for (const [account, container] of [['demo', 'private'], ['delhi', 'private'], ['demo', 'export']]) {
    state = M.putBlob(state, { account, container, key: 'a/b.txt', content: account + container }).blobs;
  }
  assert.equal(state.length, 3);
  const updated = M.putBlob(state, { account: 'demo', container: 'private', key: 'a/b.txt', content: 'new' });
  assert.equal(updated.overwritten, true);
  assert.equal(updated.blobs.length, 3);
  assert.equal(updated.blobs[0].content, 'new');
  assert.equal(state[0].content, 'demoprivate', 'writing returns new state');
  assert.equal(updated.blobs[1].content, 'delhiprivate');
});

test('prefix listing is restricted to selected place and uses literal startsWith', () => {
  const state = ['cases/214/a', 'cases/2140/b', 'other/c'].map(key => ({ account: 'demo', container: 'private', key }));
  state.push({ account: 'delhi', container: 'private', key: 'cases/214/c' });
  assert.deepEqual(M.listBlobs(state, 'demo', 'private', 'cases/214/').map(x => x.key), ['cases/214/a']);
  assert.equal(M.listBlobs(state, 'demo', 'private', 'cases/214').length, 2);
  assert.equal(M.listBlobs(state, 'demo', 'export', '').length, 0);
});

test('routed key follows matching customer storage rather than deployment', () => {
  const result = M.routeKey('delhi/prod/media/case-artifacts/214/a.pdf');
  assert.equal(result.account, 'delhistore');
  assert.equal(result.reason, 'account-root');
});

test('deployment stage root takes precedence even if a customer claims it', () => {
  const config = M.copy(M.DEMO_CONFIG);
  config.accounts[0].root = config.deployment.root;
  const result = M.routeKey('crimeos-demo/demo/media/a', config);
  assert.equal(result.account, 'demostore');
  assert.equal(result.reason, 'deployment-root');
});

test('bare keys and unknown roots fall back to deployment without ownership repair', () => {
  for (const key of ['cases/214/a.txt', 'old-mh/prod/media/a', '', 'DELHI/prod/media/a']) {
    const result = M.routeKey(key);
    assert.equal(result.account, 'demostore');
    assert.equal(result.reason, 'fallback');
    assert.match(result.warning, /silent/);
  }
});

test('stage boundary prevents matching similarly named roots', () => {
  assert.equal(M.routeKey('delhi/production/media/a').reason, 'fallback');
  assert.equal(M.routeKey('delhi/prod').reason, 'fallback');
  assert.equal(M.routeKey('delhi/prod/media/a').reason, 'account-root');
});

test('different connections claiming the same root trigger logged-error fallback', () => {
  const config = M.copy(M.DEMO_CONFIG);
  config.accounts.push({ ...config.accounts[0], connectionId: 'different', account: 'other' });
  const result = M.routeKey('delhi/prod/media/a', config);
  assert.equal(result.reason, 'conflict');
  assert.equal(result.account, 'demostore');
  assert.match(result.warning, /error logged/);
});

test('duplicate root aliases to the same connection need not be ambiguous', () => {
  const config = M.copy(M.DEMO_CONFIG);
  config.accounts.push({ ...config.accounts[0] });
  assert.equal(M.routeKey('delhi/prod/media/a', config).reason, 'account-root');
});

test('owner helper replaces only the deployment media root and leaves bare/saved keys intact', () => {
  assert.equal(M.keyForOwner('crimeos-demo/demo/media/case_context_data/214.zip', 'delhi/prod'), 'delhi/prod/media/case_context_data/214.zip');
  assert.equal(M.keyForOwner('cases/214/a.txt', 'delhi/prod'), 'cases/214/a.txt');
  assert.equal(M.keyForOwner('crimeos-demo/demo/media-old/a', 'delhi/prod'), 'crimeos-demo/demo/media-old/a');
  assert.equal(M.keyForOwner('maha/prod/media/a', 'delhi/prod'), 'maha/prod/media/a');
});

test('saved URL reader ignores host/container/query and preserves only blob path', () => {
  assert.equal(M.keyFromSavedPath('https://oldstore.blob.core.windows.net/old-container/delhi/prod/media/a.pdf?sig=SIMULATION'), 'delhi/prod/media/a.pdf');
  assert.equal(M.keyFromSavedPath('cases/214/a.txt'), 'cases/214/a.txt');
  assert.equal(M.routeKey(M.keyFromSavedPath('https://oldstore.example/old-container/cases/214/a.txt')).account, 'demostore');
});

const grant = { grantedKey: 'delhi/prod/media/a', requestKey: 'delhi/prod/media/a', permissions: ['read'], operation: 'read', ttl: 300, elapsed: 299 };
test('SAS decision requires correct key, permission and unexpired interval', () => {
  assert.equal(M.sasDecision(grant).ok, true);
  assert.equal(M.sasDecision({ ...grant, requestKey: 'delhi/prod/media/b' }).status, 403);
  assert.equal(M.sasDecision({ ...grant, operation: 'write' }).ok, false);
  assert.equal(M.sasDecision({ ...grant, elapsed: 300 }).ok, false);
  assert.equal(M.sasDecision({ ...grant, elapsed: 301 }).ok, false);
  assert.equal(M.sasDecision({ ...grant, permissions: ['read', 'write'], operation: 'write' }).ok, true);
});

test('SAS time window rejects nonfinite and negative values', () => {
  for (const elapsed of [-1, Infinity, NaN]) assert.equal(M.sasDecision({ ...grant, elapsed }).ok, false);
  for (const ttl of [0, -1, Infinity, NaN]) assert.equal(M.sasDecision({ ...grant, ttl }).ok, false);
});

test('a saved original remains at its old-ID key and is never reconstructed from its pointer', () => {
  const found = M.pathDecision({ mode: 'saved', oldId: 214, newId: 9001, blobExists: true });
  assert.equal(found.ok, true);
  assert.match(found.readKey, /\/214\//);
  const missing = M.pathDecision({ mode: 'saved', blobExists: false });
  assert.equal(missing.state, 'missing');
  assert.equal(missing.ok, false);
});

test('bad current-ID validator rejects existing saved blob before storage request', () => {
  const result = M.pathDecision({ mode: 'saved', oldId: 214, newId: 9001, blobExists: true, validator: true });
  assert.equal(result.state, 'rejected');
  assert.match(result.reason, /before Azure/);
  assert.equal(M.pathDecision({ mode: 'saved', oldId: 214, newId: 214, blobExists: true, validator: true }).ok, true);
});

test('built bundle uses the current ID and supported application path can regenerate it', () => {
  const result = M.pathDecision({ mode: 'built', oldId: 214, newId: 9001, blobExists: false, validator: true });
  assert.equal(result.state, 'rebuilt');
  assert.match(result.readKey, /9001\.zip$/);
  assert.match(result.reason, /application behavior/);
});

test('migrating database text alone leaves saved PDF missing but allows bundle regeneration', () => {
  const result = M.migrationDecision({ dbCopied: true, blobsCopied: false, sameRoot: true, excludeBundle: true });
  assert.equal(result.savedOk, false);
  assert.equal(result.bundleOk, true);
  assert.match(result.savedKey, /\/214\//);
  assert.match(result.bundleKey, /9001\.zip$/);
});

test('saved migration needs matching root plus separately copied bytes; account copy does not fix a bare key', () => {
  assert.equal(M.migrationDecision({ blobsCopied: true }).savedOk, true);
  assert.equal(M.migrationDecision({ blobsCopied: true, sameRoot: false }).savedOk, false);
  const bare = M.migrationDecision({ blobsCopied: true, bareKey: true });
  assert.equal(bare.savedOk, false);
  assert.equal(bare.route, 'Demo deployment storage');
  assert.match(bare.reason, /separate copy/);
});

test('a changed destination root affects newly built bundle keys but leaves saved paths unchanged', () => {
  const result = M.migrationDecision({ blobsCopied: true, sameRoot: false });
  assert.match(result.savedKey, /^maha\/prod\/media\//);
  assert.match(result.bundleKey, /^mh-demo\/demo\/media\//);
  const destinationConfig = M.copy(M.DEMO_CONFIG);
  destinationConfig.accounts[1].root = 'mh-demo/demo/';
  assert.equal(M.routeKey(result.savedKey, destinationConfig).account, 'demostore');
  assert.equal(M.routeKey(result.bundleKey, destinationConfig).account, 'mahastore');
  assert.equal(result.bundleOk, true);
});

test('blob copy alone does not create migrated case and retained bundle metadata cannot promise rebuild', () => {
  const noRows = M.migrationDecision({ dbCopied: false, blobsCopied: true });
  assert.equal(noRows.savedOk, false);
  assert.equal(noRows.bundleOk, false);
  assert.equal(M.migrationDecision({ excludeBundle: false }).bundleOk, false);
  assert.match(M.migrationDecision({ idOffset: false }).bundleKey, /214\.zip$/);
});

test('journey preserves backend key authority and both database pointer fields', () => {
  assert.equal(M.JOURNEY.length, 9);
  assert.match(M.JOURNEY[1].action, /key_for_case/);
  assert.match(M.JOURNEY[3].database, /file_url/);
  assert.match(M.JOURNEY[6].key, /^delhi\/prod\/media\//);
  assert.equal(M.JOURNEY[6].key, M.JOURNEY[8].key);
  assert.match(M.JOURNEY[8].database, /extracted_text_key/);
});

test('debugging evidence distinguishes routing, absent bytes, 403 expiry and pre-storage ID guard', () => {
  assert.equal(new Set(M.DEBUG_CASES.map(value => value.cause)).size, 4);
  const expiry = M.DEBUG_CASES.find(value => value.id === 'expired');
  assert.match(expiry.evidence.access, /403/);
  assert.match(expiry.evidence.object, /exists/);
  assert.match(M.DEBUG_CASES.find(value => value.id === 'missing').evidence.access, /404/);
  assert.match(M.DEBUG_CASES.find(value => value.id === 'validator').evidence.access, /No Azure request/);
});
