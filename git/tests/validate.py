"""Check shipped HTML, local links, curriculum coverage and Git learning content."""
import json
import sys
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
assert len(pages) == 21
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
assert len(QUESTIONS) == 60
assert set(Counter(q["topic"] for q in QUESTIONS).values()) == {4}
assert len(COMMANDS) == 48 and len(LABS) == 12 and len(ISSUES) == 30
assert len({s for lab in LABS for s in [lab["id"]]}) == 12
data=json.loads((ROOT/"assets/data.js").read_text().split("window.GIT_DATA = ",1)[1].removesuffix(";\n"))
assert data["questions"]==QUESTIONS
assert {m["id"] for m in data["modules"]}=={p["id"] for p in LESSONS}
assert len(data["cards"])==48 and data["exercises"]==[0,1,2]
assert set(data["labSteps"])=={lab["id"]+"-"+str(i) for lab in LABS for i in range(len(lab["steps"]))}
for path in ROOT.rglob("*"):
    if path.is_file() and "__pycache__" not in path.parts:
        for number,line in enumerate(path.read_text().splitlines(),1):
            assert line.rstrip()==line,(path,number,"trailing whitespace")
print("PASS: 21 static pages, local links/anchors, unique IDs, 60 questions across 15 topics.")
