"""Exercise all twelve authored labs against real, disposable, local Git repositories."""
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("fixtures",ROOT/"examples/create-labs.py")
fixtures=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)
fixtures.ENV["GIT_EDITOR"]="true"
fixtures.ENV["GIT_SEQUENCE_EDITOR"]="true"
run=fixtures.run

with tempfile.TemporaryDirectory(prefix="kt-git-labs-") as tmp:
    root=Path(tmp)/"new-labs"
    manifest=fixtures.create(root)
    try:
        fixtures.create(root)
    except FileExistsError:
        pass
    else:
        raise AssertionError("Existing lab directories must be refused")
    assert (root/"lab-manifest.json").exists()

    p=root/"01-staging"
    assert run(p,"status","--short").startswith("MM ")
    run(p,"commit","-m","Commit only staged content")
    assert "First edit" in run(p,"show","HEAD:notes.txt")
    assert "Second edit" not in run(p,"show","HEAD:notes.txt")
    assert "Second edit" in run(p,"diff")

    p=root/"02-fast-forward"
    tip=run(p,"rev-parse","feature")
    run(p,"merge","--ff-only","feature")
    assert run(p,"rev-parse","HEAD")==tip

    p=root/"03-three-way"
    run(p,"merge","--no-edit","feature")
    assert len(run(p,"rev-list","--parents","-n","1","HEAD").split())==3
    assert (p/"timeout.txt").read_text()=="20\n"
    assert (p/"retries.txt").read_text()=="3\n"

    p=root/"04-conflict"
    run(p,"merge","feature",expected=1)
    assert json.loads(run(p,"show",":1:config.json"))=={"timeout":10,"retries":1}
    assert json.loads(run(p,"show",":2:config.json"))=={"timeout":20,"retries":1}
    assert json.loads(run(p,"show",":3:config.json"))=={"timeout":30,"retries":3}
    fixtures.write(p,{"config.json":fixtures.config(20,3)})
    run(p,"add","config.json"); run(p,"diff","--cached","--check")
    run(p,"merge","--continue")
    assert run(p,"status","--porcelain")==""

    p=root/"05-rebase"
    old=run(p,"rev-parse","HEAD")
    run(p,"branch","backup/feature")
    run(p,"rebase","main",expected=1)
    assert json.loads(run(p,"show",":2:config.json"))["timeout"]==20
    assert json.loads(run(p,"show",":3:config.json"))["timeout"]==30
    fixtures.write(p,{"config.json":fixtures.config(20,3)})
    run(p,"add","config.json"); run(p,"rebase","--continue")
    assert run(p,"rev-parse","HEAD")!=old
    assert run(p,"rev-parse","backup/feature")==old
    assert (p/"notes.txt").exists()
    run(p,"merge-base","--is-ancestor","main","feature")

    p=root/"06-lease/alice"
    remote=root/"06-lease/remote.git"
    expected=manifest["labs"]["lease"]["expected"]
    bob=manifest["labs"]["lease"]["bob"]
    run(p,"push","origin","HEAD:refs/heads/feature",expected=1)
    run(p,"push","--force-with-lease","origin","HEAD:refs/heads/feature",expected=1)
    run(p,"fetch","origin")
    run(p,"push","--force-with-lease=refs/heads/feature:"+expected,"origin","HEAD:refs/heads/feature",expected=1)
    assert run(remote,"rev-parse","refs/heads/feature")==bob
    # Demonstrate the unsafe default-lease case only against this disposable bare remote.
    run(p,"push","--force-with-lease","origin","HEAD:refs/heads/feature")
    assert run(remote,"rev-parse","refs/heads/feature")==run(p,"rev-parse","HEAD")
    run(p,"merge-base","--is-ancestor",bob,"HEAD",expected=1)
    assert run(root/"06-lease/bob","rev-parse","HEAD")==bob

    p=root/"07-reflog"
    recovered=run(p,"rev-parse","HEAD@{1}")
    assert recovered==manifest["labs"]["reflog"]["old_tip"]
    run(p,"branch","rescue/recovered",recovered)
    assert "Important" in run(p,"show","rescue/recovered:valuable.txt")

    p=root/"08-stash"
    run(p,"stash","apply",expected=1)
    assert run(p,"stash","list")
    run(p,"restore","--source=HEAD","--staged","--worktree","--","config.json")
    run(p,"stash","branch","rescue/stashed","stash@{0}")
    assert json.loads((p/"config.json").read_text())=={"timeout":20,"retries":1}
    assert run(p,"stash","list")==""

    p=root/"09-bisect"
    run(p,"bisect","start","known-bad","known-good")
    run(p,"bisect","run","sh","-c",'test "$(cat value.txt)" = 0')
    assert run(p,"rev-parse","refs/bisect/bad")==manifest["labs"]["bisect"]["culprit"]
    run(p,"bisect","reset")
    assert run(p,"branch","--show-current")=="main"

    p=root/"10-cherry-pick"
    run(p,"cherry-pick","-x","fix-to-backport")
    assert (p/"bug.txt").read_text()=="fixed\n"
    assert not (p/"unrelated-feature.txt").exists()
    assert "cherry picked from commit" in run(p,"log","-1","--format=%B")

    p=root/"11-worktree"
    before=(p/"notes.txt").read_text()
    run(p,"worktree","add","../11-hotfix","-b","hotfix","main")
    assert (root/"11-hotfix/notes.txt").read_text()=="base notes\n"
    run(p,"worktree","remove","../11-hotfix")
    assert (p/"notes.txt").read_text()==before

    p=root/"12-revert"
    run(p,"revert","--no-edit","bad-change")
    assert (p/"flag.txt").read_text()=="off\n"
    assert (p/"docs.txt").exists()
    run(p,"merge-base","--is-ancestor","bad-change","HEAD")
    assert run(p,"status","--porcelain")==""
    print("PASS: all 12 real Git labs, conflict stages, recovery, existing-directory protection, and both lease outcomes on local remotes.")
