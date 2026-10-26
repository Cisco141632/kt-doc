const assert = require('node:assert/strict');
const {test} = require('node:test');
const {scenes,resolveConflict,simulatePush,evaluatePermission} = require('../assets/visuals.js');

test('every illustrated parent exists and points to an earlier commit', () => {
  assert.equal(scenes.length,8);
  for(const scene of scenes) for(const step of scene.steps) {
    assert.equal(new Set(step.nodes.map(n=>n.id)).size,step.nodes.length);
    for(const n of step.nodes) for(const id of n.parents) {
      const parent=step.nodes.find(p=>p.id===id);
      assert.ok(parent,scene.id+': missing parent '+id);
      assert.ok(parent.x<n.x,scene.id+': parent must precede child');
    }
  }
});
test('resolution requires valid JSON and both business requirements', () => {
  for(const text of ['<<<<<<< HEAD','null','[]','{"timeout":20,"retries":1}','{"timeout":30,"retries":3}','{"timeout":20,"retries":3,"timeout":20}']) assert.equal(resolveConflict(text).ok,false,text);
  assert.equal(resolveConflict('{"retries":3,"timeout":20}').ok,true);
});
test('a background fetch weakens a default lease but not the pinned expectation', () => {
  assert.equal(simulatePush({mode:'normal',remote:'C'}).allowed,false);
  assert.equal(simulatePush({mode:'lease',remote:'T',tracking:'C'}).allowed,false);
  assert.equal(simulatePush({mode:'lease',remote:'T',tracking:'T'}).lost,true);
  assert.equal(simulatePush({mode:'explicit',remote:'T',tracking:'T',expected:'C'}).allowed,false);
  assert.equal(simulatePush({mode:'explicit',remote:'C',expected:'C'}).allowed,true);
  assert.equal(simulatePush({mode:'force',remote:'T'}).lost,true);
  for(const mode of ['force','lease','explicit']) assert.equal(simulatePush({mode,remote:'C',protectedBranch:true}).allowed,false);
});
test('access requires every capability gate and applicable rule; admin is not bypass', () => {
  const good={role:'write',scope:'write',identity:true,selected:true,approved:true,action:'merge',approvals:2,checks:true,requirePR:true,bypass:false};
  assert.equal(evaluatePermission(good).allowed,true);
  for(const patch of [{role:'read'},{role:'triage'},{scope:'read'},{scope:'none'},{identity:false},{selected:false},{approved:false},{approvals:1},{checks:false},{action:'direct'}]) assert.equal(evaluatePermission({...good,...patch}).allowed,false);
  assert.equal(evaluatePermission({...good,role:'admin',action:'direct'}).allowed,false);
  assert.equal(evaluatePermission({...good,action:'direct',bypass:true}).allowed,true);
  assert.equal(evaluatePermission({...good,identity:false,bypass:true}).allowed,false);
  assert.equal(evaluatePermission({...good,action:'feature',approvals:0,checks:false}).allowed,true);
});
