"""Check shipped HTML, local links, curriculum coverage and tmux examples."""
import os
import subprocess
import sys
import tempfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from course import LESSONS, COMMANDS
from questions import QUESTIONS
from practice_content import LABS, ISSUES

class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = []
        self.links = []
        self.h1s = 0
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1s += 1
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append(attrs[attr])

pages = {p.resolve(): Document(p) for p in ROOT.glob("*.html")}
assert len(pages) == 18
for path, doc in pages.items():
    assert doc.h1s == 1, path
    assert len(doc.ids) == len(set(doc.ids)), (path, "duplicate IDs")
    for link in doc.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if target.is_dir():
            target /= "index.html"
        assert target.exists(), (path, link)
        if url.fragment and target.suffix == ".html":
            target_doc = pages.get(target) or Document(target)
            assert unquote(url.fragment) in target_doc.ids, (path, link, "missing anchor")
assert len(QUESTIONS) == 48
assert set(Counter(q["topic"] for q in QUESTIONS).values()) == {4}
assert len(COMMANDS) == 42 and len(LABS) == 8 and len(ISSUES) == 24
assert len({s for lab in LABS for s in [lab["id"]]}) == 8
print("PASS: 18 static pages, local links/anchors, unique IDs, 48 questions across 12 topics.")

if "--tmux" in sys.argv:
    socket = "kt-doc-validation-" + str(os.getpid())
    env = {k:v for k,v in os.environ.items() if k != "TMUX"}
    def tmux(*args, check=True):
        return subprocess.run(["tmux", "-L", socket, *args], text=True, capture_output=True, check=check, env=env)
    try:
        pane = tmux("-f", str(ROOT/"examples/tmux.conf"), "new-session", "-d", "-P", "-F", "#{pane_id}", "-s", "verify", "-n", "editor", "-x", "120", "-y", "40").stdout.strip()
        assert pane.startswith("%")
        assert tmux("show-options", "-gv", "mouse").stdout.strip() == "on"
        assert tmux("show-window-options", "-gv", "mode-keys").stdout.strip() == "vi"
        assert tmux("show-options", "-gv", "base-index").stdout.strip() == "1"
        tmux("source-file", str(ROOT/"examples/tmux.conf"))
        tmux("split-window", "-h", "-t", pane, "-c", str(ROOT))
        tmux("split-window", "-v", "-t", pane)
        tmux("select-layout", "-t", "verify:editor", "tiled")
        assert len(tmux("list-panes", "-t", "verify:editor").stdout.splitlines()) == 3
        tmux("resize-pane", "-Z", "-t", pane)
        assert tmux("display-message", "-p", "-t", pane, "#{window_zoomed_flag}").stdout.strip() == "1"
        tmux("resize-pane", "-Z", "-t", pane)
        tmux("set-buffer", "kt-doc clipboard test")
        assert tmux("show-buffer").stdout == "kt-doc clipboard test"
        tmux("capture-pane", "-p", "-S", "-200", "-t", pane)
        tmux("new-session", "-d", "-s", "keep")
        tmux("kill-session", "-t", "=verify")
        assert tmux("has-session", "-t", "=keep").returncode == 0
        # Exercise the actual launcher, replacing only the socket name to protect real labs.
        with tempfile.TemporaryDirectory(prefix="kt-doc-launcher-") as directory:
            script = Path(directory)/"workspace.sh"
            script.write_text((ROOT/"examples/workspace.sh").read_text().replace("kt-tmux", socket))
            args = ["sh", str(script), directory]
            first = subprocess.run(args, stdin=subprocess.DEVNULL, capture_output=True, env=env)
            # The attach step cannot open a TTY in this test; the detached setup must still be complete.
            before = tmux("list-panes", "-s", "-t", "kt-project", "-F", "#{pane_id}").stdout
            assert len(before.splitlines()) == 3
            assert len(tmux("list-windows", "-t", "kt-project").stdout.splitlines()) == 2
            second = subprocess.run(args, stdin=subprocess.DEVNULL, capture_output=True, env=env)
            after = tmux("list-panes", "-s", "-t", "kt-project", "-F", "#{pane_id}").stdout
            assert before == after, "launcher duplicated or replaced panes"
        print("PASS: real tmux config, splits, layouts, zoom, buffers, scoped cleanup and sequential launcher reuse.")
    finally:
        tmux("kill-server", check=False)
