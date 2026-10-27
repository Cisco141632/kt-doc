"""Small HTML helpers for plain-English Git lessons."""
from html import escape


def code(text, where="Type this in your terminal"):
    return '<div class="snippet"><div class="code-caption"><span>' + escape(where) + '</span></div><pre><code>' + escape(text.strip()) + '</code></pre></div>'


def table(headings, rows):
    return '<div class="table-wrap"><table><thead><tr>' + ''.join('<th scope="col">' + h + '</th>' for h in headings) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td class="wrap">' + c + '</td>' for c in row) + '</tr>' for row in rows) + '</tbody></table></div>'


def section(id, title, body):
    return '<section class="lesson-section" id="' + id + '"><h2>' + title + '</h2>' + body + '</section>'


def note(title, body, kind="tip"):
    return '<div class="callout ' + kind + '"><b class="callout-title">' + title + '</b><p>' + body + '</p></div>'


def flow(items):
    return '<div class="flow" role="group" aria-label="Steps in order">' + '<span aria-hidden="true">→</span>'.join('<div><b>' + a + '</b><small>' + b + '</small></div>' for a, b in items) + '</div>'


def graph(text, caption):
    return '<figure class="graph"><pre>' + escape(text.strip()) + '</pre><figcaption>' + caption + '</figcaption></figure>'


def source(*items):
    return '<p class="source-note">Read the full explanation: ' + ' · '.join('<a href="' + url + '">' + title + '</a>' for title, url in items) + '</p>'


def words(items):
    return '<div class="word-cards">' + ''.join('<details open><summary>' + escape(name) + '</summary><p>' + body + '</p></details>' for name, body in items) + '</div>'


def steps(items):
    """One action, its reason, and an observable result per step."""
    return '<ol class="small-steps">' + ''.join('<li><h3>' + title + '</h3><p>' + reason + '</p>' + (code(command) if command else '') + '<p class="expect"><b>What you should see:</b> ' + result + '</p></li>' for title, reason, command, result in items) + '</ol>'


def compare(before, action, after):
    return '<div class="before-after"><article><span class="state-label">Before</span>' + before + '</article><div class="change-arrow"><span aria-hidden="true">→</span><b>' + action + '</b></div><article><span class="state-label">After</span>' + after + '</article></div>'


def walk(title, frames):
    """All frames stay readable without JavaScript and when printed."""
    return '<div class="lesson-walk" data-walk><h3>' + title + '</h3><p class="meta">A picture to explore. These buttons do not run commands on your computer.</p><div class="walk-controls" hidden><button class="btn" type="button" data-walk-prev>← Back</button><span data-walk-count role="status"></span><button class="btn btn-primary" type="button" data-walk-next>Next step →</button><button class="btn" type="button" data-walk-reset>Start again</button></div><ol class="walk-frames">' + ''.join('<li class="walk-frame"><p class="eyebrow">Step ' + str(i + 1) + '</p><h4>' + label + '</h4><p>' + body + '</p><div class="walk-picture">' + picture + '</div></li>' for i, (label, body, picture) in enumerate(frames)) + '</ol></div>'


def filebox(label, text):
    return '<div class="file-box"><b>' + escape(label) + '</b><pre>' + escape(text) + '</pre></div>'


def three(file, ready, saved):
    return '<div class="three-places">' + filebox('1 · Your file', file) + filebox('2 · Chosen for the next commit', ready) + filebox('3 · Current saved commit', saved) + '</div>'


def ask(prompt, answer):
    return '<details class="reveal predict"><summary>Try to answer: ' + prompt + '</summary><p>' + answer + '</p></details>'


def fixes(rows):
    return table(['What happened?', 'What to check', 'What to do, then check'], rows)
