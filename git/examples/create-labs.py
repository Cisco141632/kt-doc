#!/usr/bin/env python3
"""Create fresh, local-only Git lab repositories. Never edits an existing directory."""
import argparse
import json
import os
import subprocess
from pathlib import Path

ENV = {k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0")

def run(repo, *args, expected=0):
    p = subprocess.run(["git", "-c", "core.hooksPath="+os.devnull, "-c", "init.templateDir=", *args],
        cwd=repo, env=ENV, text=True, capture_output=True)
    if p.returncode != expected:
        raise RuntimeError("git " + " ".join(args) + " failed: " + p.stderr)
    return p.stdout.strip()

def configure(repo):
    run(repo,"config","user.name","Git Learning")
    run(repo,"config","user.email","learner@example.invalid")
    run(repo,"config","commit.gpgsign","false")
    run(repo,"config","merge.conflictStyle","diff3")
    run(repo,"config","core.hooksPath",os.devnull)

def init(path, files):
    path.mkdir()
    run(path,"init","-b","main")
    configure(path)
    commit(path,files,"Initial snapshot")
    return path

def write(repo, files):
    for name, content in files.items():
        p=repo/name
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(content)

def commit(repo, files, message):
    write(repo,files)
    run(repo,"add","--all")
    run(repo,"commit","-m",message)
    return run(repo,"rev-parse","HEAD")

def config(timeout,retries):
    return json.dumps({"timeout":timeout,"retries":retries},indent=2)+"\n"

def divergent(path, extra=False):
    p=init(path,{"config.json":config(10,1)})
    run(p,"switch","-c","feature")
    commit(p,{"config.json":config(30,3)},"Change timeout and retry policy")
    if extra:
        commit(p,{"notes.txt":"Feature notes must survive.\n"},"Add feature notes")
    run(p,"switch","main")
    commit(p,{"config.json":config(20,1)},"Set approved timeout budget")
    if extra:
        run(p,"switch","feature")
    return p

def create(root):
    root=root.resolve()
    root.mkdir(parents=True,exist_ok=False)
    manifest={"root":str(root),"labs":{}}
    p=init(root/"01-staging",{"notes.txt":"Base note.\n"})
    write(p,{"notes.txt":"Base note.\nFirst edit.\n"})
    run(p,"add","notes.txt")
    write(p,{"notes.txt":"Base note.\nFirst edit.\nSecond edit.\n"})
    p=init(root/"02-fast-forward",{"base.txt":"base\n"})
    run(p,"switch","-c","feature")
    commit(p,{"feature.txt":"feature\n"},"Add feature")
    run(p,"switch","main")
    p=init(root/"03-three-way",{"timeout.txt":"10\n","retries.txt":"1\n"})
    run(p,"switch","-c","feature")
    commit(p,{"retries.txt":"3\n"},"Increase retries")
    run(p,"switch","main")
    commit(p,{"timeout.txt":"20\n"},"Increase timeout")
    divergent(root/"04-conflict")
    divergent(root/"05-rebase",extra=True)
    group=root/"06-lease"; group.mkdir()
    remote=group/"remote.git"; remote.mkdir()
    run(remote,"init","--bare","-b","main")
    seed=init(group/"seed",{"base.txt":"base\n"})
    run(seed,"remote","add","origin",str(remote))
    run(seed,"push","-u","origin","main")
    run(seed,"switch","-c","feature")
    old=commit(seed,{"feature.txt":"shared feature\n"},"Original feature")
    run(seed,"push","-u","origin","feature")
    (group/"expected-tip.txt").write_text(old+"\n")
    for who in ("alice","bob"):
        run(group,"clone",str(remote),who)
        configure(group/who)
        run(group/who,"switch","feature")
    run(group/"alice","commit","--amend","-m","Alice rewrites the feature message")
    bob=commit(group/"bob",{"bob.txt":"Teammate work must not disappear.\n"},"Bob adds work")
    run(group/"bob","push","origin","feature")
    manifest["labs"]["lease"]={"expected":old,"bob":bob}
    p=init(root/"07-reflog",{"base.txt":"base\n"})
    old=commit(p,{"valuable.txt":"Important recorded work.\n"},"Record valuable work")
    run(p,"reset","--hard","HEAD~1")
    manifest["labs"]["reflog"]={"old_tip":old}
    p=init(root/"08-stash",{"config.json":config(10,1)})
    write(p,{"config.json":config(20,1)})
    run(p,"stash","push","-m","WIP timeout")
    commit(p,{"config.json":config(30,1)},"Different timeout on branch")
    p=init(root/"09-bisect",{"value.txt":"0\n","notes.txt":"start\n"})
    run(p,"tag","known-good")
    commit(p,{"notes.txt":"before regression\n"},"Unrelated documentation")
    culprit=commit(p,{"value.txt":"1\n"},"Introduce regression")
    commit(p,{"notes.txt":"after regression\n"},"More documentation")
    commit(p,{"extra.txt":"extra\n"},"Add unrelated file")
    run(p,"tag","known-bad")
    manifest["labs"]["bisect"]={"culprit":culprit}
    p=init(root/"10-cherry-pick",{"bug.txt":"broken\n"})
    run(p,"switch","-c","feature")
    commit(p,{"bug.txt":"fixed\n"},"Fix the bug")
    run(p,"tag","fix-to-backport")
    commit(p,{"unrelated-feature.txt":"Do not backport this.\n"},"Add unrelated feature")
    run(p,"switch","main")
    commit(p,{"maintenance.txt":"maintenance branch\n"},"Maintenance note")
    p=init(root/"11-worktree",{"notes.txt":"base notes\n"})
    write(p,{"notes.txt":"base notes\nunfinished feature work\n"})
    p=init(root/"12-revert",{"flag.txt":"off\n"})
    commit(p,{"flag.txt":"on\n"},"Enable bad behavior")
    run(p,"tag","bad-change")
    commit(p,{"docs.txt":"Keep these later docs.\n"},"Improve documentation")
    (root/"lab-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    return manifest

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination",type=Path,help="A NEW directory; existing paths are refused.")
    args=parser.parse_args()
    try:
        create(args.destination)
    except FileExistsError:
        parser.exit(2,"Destination already exists. Choose another new directory; no existing lab is overwritten.\n")
    print("Created 12 local Git labs in "+str(args.destination.resolve()))
    print("No network remotes or credentials are used. Open practice.html for the steps.")
