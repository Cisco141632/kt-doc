"""Validate shipped pages, links, anchors, assessments and all seven lab types."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from course import LESSONS, GLOSSARY
from questions import QUESTIONS
from supplements import LABS


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = []
        self.links = []
        self.labs = []
        self.h1s = 0
        self.lang = None
        self.current = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        if tag == 'h1':
            self.h1s += 1
        if attrs.get('aria-current') == 'page':
            self.current += 1
        if 'data-lab' in attrs:
            self.labs.append(attrs['data-lab'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])


pages = {p.resolve(): Document(p) for p in ROOT.glob('*.html')}
assert len(pages) == 16, len(pages)
for path, doc in pages.items():
    assert doc.h1s == 1, (path, 'must have one main heading')
    assert doc.lang == 'en', path
    assert doc.current == 1, (path, 'must identify the active navigation link')
    assert len(doc.ids) == len(set(doc.ids)), (path, 'duplicate IDs')
    for link in doc.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if target.is_dir():
            target /= 'index.html'
        assert target.exists(), (path, link, 'missing local target')
        if url.fragment and target.suffix == '.html':
            target_doc = pages.get(target) or Document(target)
            assert unquote(url.fragment) in target_doc.ids, (path, link, 'missing anchor')

topics = {m['id'] for m in LESSONS}
assert len(topics) == len(LESSONS) == 11
assert len(QUESTIONS) >= 32
assert len({q['id'] for q in QUESTIONS}) == len(QUESTIONS)
assert set(Counter(q['topic'] for q in QUESTIONS)) == topics, 'every lesson needs assessment coverage'
for q in QUESTIONS:
    assert len(q['options']) >= 3 and 0 <= q['correct'] < len(q['options']), q['id']
    assert all(option['text'].strip() and option['why'].strip() for option in q['options']), q['id']
assert len(GLOSSARY) >= 18
assert len({g['term'].lower() for g in GLOSSARY}) == len(GLOSSARY)
expected_labs = {lab[0] for lab in LABS}
assert len(expected_labs) == 7
assert set(pages[(ROOT / 'practice.html').resolve()].labs) == expected_labs
assert set(lab for doc in pages.values() for lab in doc.labs) == expected_labs
payload = (ROOT / 'assets/data.js').read_text().split('window.AZURE_DATA = ', 1)[1]
data = json.loads(payload.rstrip().removesuffix(';'))
assert len(data['modules']) == len(pages)
assert set(data['lessonIds']) == topics
assert data['questions'] == QUESTIONS
assert set(data['labIds']) == expected_labs
home = (ROOT.parent / 'index.html').read_text()
assert 'href="azure/"' in home
print(f'PASS: {len(pages)} static pages; all local links and anchors; 11 lesson topics; {len(QUESTIONS)} explained questions; {len(GLOSSARY)} glossary terms; seven lab types; homepage integration.')
