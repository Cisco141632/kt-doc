"""Practice and lookup pages, using the same words as the lessons."""
from html import escape
from lesson_parts import section, code, note, table, steps, compare, filebox, flow
from reference_content import COMMANDS, GLOSSARY
from practice_content import ISSUES, LABS


def issues_html():
    return ''.join('<details class="issue" id="' + id + '" data-category="' + category + '"><summary><span class="chip">' + category + '</span> ' + escape(title) + '</summary><h3>Why it can happen</h3><p>' + escape(cause) + '</p><ol class="fix-steps"><li><h4>Check first</h4><p>' + escape(inspect) + '</p></li><li><h4>Fix the cause</h4><p>' + escape(fix) + '</p></li><li><h4>Check that it worked</h4><p>' + escape(verify) + '</p></li></ol><a href="' + topic + '.html">Read the lesson with pictures →</a></details>' for id, category, title, cause, inspect, fix, verify, topic in ISSUES)


def labs_html():
    output = ''
    for lab in LABS:
        actions = []
        for line in lab['commands'].splitlines():
            if line.startswith('#'):
                actions.append('<li class="lab-instruction"><p>' + escape(line.lstrip('# ')) + '</p></li>')
            elif line.strip():
                actions.append('<li>' + code(line) + '</li>')
        output += '<article class="lab" id="' + lab['id'] + '"><p class="eyebrow">Practice folder · ' + escape(lab['directory']) + '</p><h3>' + escape(lab['title']) + '</h3><p><b>Your goal:</b> ' + escape(lab['goal']) + '</p><p>Open a terminal in <code>YOUR_LAB_ROOT/' + escape(lab['directory']) + '</code>. YOUR_LAB_ROOT means the folder you chose in setup. Read one step, run it, and look at its result before going on.</p><ol class="lab-actions">' + ''.join(actions) + '</ol>'
        output += '<h4>Check the results yourself</h4>' + ''.join('<label class="lab-step"><input type="checkbox" data-lab="' + lab['id'] + '-' + str(i) + '">' + escape(step) + '</label>' for i, step in enumerate(lab['steps']))
        output += '<details class="reveal"><summary>Why does this happen?</summary><p>' + escape(lab['why']) + '</p></details><p class="expect"><b>Final check:</b> ' + escape(lab['verify']) + '</p><p><b>If your result differs:</b> ' + escape(lab['problem']) + '</p><a href="' + lab['topic'] + '.html">Read the related lesson →</a></article>'
    return output


def add_support(lesson):
    lesson('troubleshooting', 'Something went wrong: check and fix it', 35,
      'Find the message you see. Learn why it can happen, what to check first, how to fix it, and how to confirm the result.',
      ['Read the exact error before choosing a fix.', 'Keep useful files and commits while investigating.', 'Check that the fix kept both your work and your teammate’s work.'], [
      section('method', 'Start with these checks',
        '<p>“Rejected” can mean a history problem, a sign-in problem, or a branch rule. The right fix depends on the full message.</p>' + steps([
          ('Read the current state', 'Find the current branch and any paused operation.', 'git status', 'You know whether Git is waiting for a merge/rebase decision or just showing file changes.'),
          ('Read changes not yet saved in a commit', 'These commands only show differences; they do not replace files.', 'git diff\ngit diff --staged', 'You can separate edits in your files from content chosen for the next commit.'),
          ('Inspect branch links and saved history', 'This is a local view. Fetch when you need newer remote information.', 'git branch -vv\ngit log --graph --oneline --decorate --all -20', 'You can see branch names and the commits they currently point to.'),
          ('Choose the matching case below', 'If work seems lost, stop cleanup and preserve what you find.', '', 'The fix matches the cause. Check the stated final result afterward.')
        ]) + compare(filebox('Before', 'Push rejected\nReason: teammate pushed first\nBoth changes still need to be kept.'), 'Fetch → inspect → merge → test', filebox('After', 'Both changes included\nNormal push succeeds\nFinal files behave as intended.'))),
      section('cases', 'Find your error or symptom', '<div class="filters only-js"><label class="field">Search errors and fixes<input id="issue-search" type="search" placeholder="push rejected, HEAD, stash, access…"></label><label class="field">Group<select id="issue-category"><option value="all">All groups</option>' + ''.join('<option>' + c + '</option>' for c in sorted(set(i[1] for i in ISSUES))) + '</select></label></div><p class="meta" id="issue-count" aria-live="polite">30 problems with checks and fixes</p><div id="issues">' + issues_html() + '</div><p class="empty" id="issue-empty" hidden>No matching problem. Try “push”, “history”, or “access”.</p>'),
      section('handoff', 'Write down the fix', '<p>Record the branch, command, exact error without secrets, cause, fix, and final check. Include old/new commit IDs when history moved. For example: “Push was rejected because Bob sent T first. I fetched, checked T, merged it, ran the tests, and pushed normally. Both changes are now present.” Tell teammates the agreed final state of a shared branch.</p>')
    ], ['Read the error, then check files, history, access, or rules as needed.', 'Keep useful work before replacing or deleting anything.', 'Check the wanted files and behavior after the fix.'], 'troubleshooting')

    lesson('practice', 'Try 12 exercises with real Git', 75,
      'Create new practice folders and try each command in small steps. Some conflicts and rejected pushes are expected parts of the exercise.',
      ['Create practice projects without changing an existing project.', 'Read and run one action at a time.', 'Explain the result and check it in your terminal.'], [
      section('setup', 'Create a new practice area',
        '<p>You need Git 2.28 or later and Python 3. Check <code>git --version</code> and <code>python3 --version</code>. Setup creates small local repositories, including a shared local repository and Alice/Bob copies. It does not need a GitHub login or send anything online.</p>' + steps([
          ('Choose a new destination', 'Run from this learning-documents repository’s root folder. The destination must not exist. On a system without /tmp, choose another new local path.', 'python3 git/examples/create-labs.py /tmp/git-learning-first-run', 'Twelve exercise folders are created. Existing folders are refused, not replaced.'),
          ('Enter the first lab', 'Use the destination path you chose. Each exercise below names its folder.', 'cd /tmp/git-learning-first-run/01-staging', 'You are inside the first practice repository. Status shows changes prepared for this exercise.'),
          ('Run one line and read the result', 'Pause at comments asking you to edit or expect a conflict. Do not paste the whole exercise as one script.', '', 'You can explain each action before running the next line.')
        ]) + '<p>You can also <a href="examples/create-labs.py" download>download the setup script</a> and run it with a new local path. Examples use a Linux/macOS shell or Git Bash on Windows. The script gives these projects local identity settings and disables signing/hooks locally for consistent practice.</p>' + note('Check a box after observing the result', 'The page cannot read your project files. These boxes record what you checked yourself. Browser exercises let you try pictures first.') + '<p id="lab-progress" class="meta" aria-live="polite"></p><progress id="lab-meter" max="1" value="0" aria-label="Steps checked by you"></progress>'),
      section('labs', 'Follow each exercise', labs_html()),
      section('finish', 'Repeat with a fresh folder', '<p>Keep your practice folders to inspect later. To repeat from the beginning, run setup with another new destination. It will not reset an existing exercise. Only delete a practice folder after checking it holds no work you want to keep.</p><p>Explain the before and after without looking at the commands. A conflict or expected rejection can be the correct result of an exercise.</p>')
    ], ['Practise in new folders made for these exercises.', 'Run one action, inspect it, then move on.', 'Check the final files and history, not just a success message.'])

    lesson('playground', 'See what the commands change', 35,
      'Move through history pictures, fix a settings conflict, and find why a push or access check is refused.',
      ['Read branch names and earlier-commit links.', 'Keep two required values when fixing a conflict.', 'Explain why a push or access check succeeds or fails.'], [
      section('scope', 'How to read these pictures', '<p>Each circle is a saved commit. A, B, and C stand for real commit IDs. Lines link a commit to earlier commits. A label such as main tells you which commit the branch names. Earlier work is on the left; later work is on the right.</p><p>Buttons change these examples, not a real project or account. If a word is unfamiliar, open <a href="reference.html#glossary">the word list</a>.</p>'),
      section('history-explorer', '1 · Before and after each history command', '<p>Choose a story. Read the starting point, predict the next picture, then use Next step. Read what moved and what stayed.</p><div id="graph-explorer" class="visual-tool"></div><noscript><p>Read the pictures in <a href="merge.html">merge</a>, <a href="rebase.html">rebase</a>, and <a href="force-push.html">force push</a>.</p></noscript>'),
      section('conflict-lab', '2 · Keep the needed values from both sides', '<p>Timeout is a wait limit. Retries is how many times to try again. The requirement is timeout 20 and retries 3. JSON is the settings format below. Make one valid settings object with both values.</p><div id="conflict-tool" class="visual-tool"></div><noscript><p>Base: 10 / 1. Main: 20 / 1. Feature: 30 / 3. Final result: {"timeout":20,"retries":3}. Neither whole side has both values.</p></noscript>'),
      section('push-lab', '3 · A teammate pushes while you change history', '<p>Your replacement is C′. The old server commit was C. Your teammate may have added T. A lease checks whether the server is still at an expected commit, not whether your files keep every needed change.</p><div id="push-tool" class="visual-tool"></div><noscript><p>An explicit expected-C lease refuses if the server is now at T. Fetch and inspect T before deciding how to keep it.</p></noscript>'),
      section('access-lab', '4 · Find the missing access check', '<p>A role gives an account project access. A token is its limited secret key. A branch rule can still require a PR, reviews, and tests. Change one setting at a time.</p><div id="permission-tool" class="visual-tool"></div><noscript><p>Account access, token limits, and rules must all allow the action. Admin is not always an automatic exception.</p></noscript>')
    ], ['Branch labels name commits; lines show earlier history.', 'A conflict fix needs the right values as well as valid punctuation.', 'An expected-ID check and an access role each check only part of the action.'])

    from studio_content import add_studio
    add_studio(lesson, section, note, table)

    lesson('quiz', 'Check your understanding', 35,
      'Try 60 questions about files, saved changes, team work, and mistakes. Every choice includes a reason.',
      ['Predict what a command will do.', 'Learn from a wrong choice and try again.', 'Use a real exercise to check a difficult idea.'], [
      section('assessment', 'Try a few questions at a time', '<p>Choose one topic or all topics. Read the reason after answering. Retry missed lets you try difficult questions again. Fresh attempt clears only this quiz’s answers; other practice stays.</p><p>Short checks within lessons are separate from this full quiz. There is no countdown.</p><div id="quiz"></div><noscript><p>The question bank below works without JavaScript. JavaScript adds scoring and saves this attempt.</p></noscript><details class="reveal"><summary>Read or print all questions and answers</summary><div id="static-questions"></div></details>')
    ], ['Predict the change before choosing a command.', 'Read why a choice is right or wrong.', 'Try a real lab when you cannot yet explain the result.'])

    lesson('recap', 'Review what you learned', 20,
      'Try short command cards, choose your next practice step, and back up progress saved in this browser.',
      ['Recall a command by the job it does.', 'Review one difficult idea at a time.', 'Export or import your progress.'], [
      section('cards', 'Try answering before you turn the card', '<p>Say what the command changes and what to check first. Turn the card to compare. Know it schedules review after 1, 3, 7, 14, then 30 days for repeated correct reviews. Again keeps it ready to review. Choose All cards to practise any time.</p><p><a class="btn" href="studio.html#sprint">Try five questions →</a></p><div id="flashcards"></div><noscript><p>Cover the command column in the <a href="reference.html">reference table</a> and answer from the task column.</p></noscript>'),
      section('plan', 'Build up in small steps', table(['When ready', 'Try this', 'Explain afterward'], [
        ['First', '<a href="practice.html#staging">File and staging lab</a>', 'Why commit saves chosen text even after another edit.'],
        ['Next', '<a href="practice.html#fast-forward">Branch move</a> and <a href="practice.html#three-way">merge</a>', 'Why one moves a name and the other adds a two-parent commit.'],
        ['Then', '<a href="practice.html#conflict">Conflict</a> and <a href="practice.html#rebase">rebase</a>', 'Which values are needed and why ours/theirs depend on the operation.'],
        ['After that', '<a href="practice.html#lease">Push race</a> and <a href="practice.html#reflog">recovery</a>', 'Why a rejected lease keeps new shared work, and how a rescue name keeps a found commit.'],
        ['Later', '<a href="practice.html#bisect">Bug search</a>, <a href="practice.html#cherry">copy a fix</a>, <a href="practice.html#worktree">second folder</a>', 'How you checked the result instead of guessing.'],
        ['With a team', '<a href="collaboration.html">A small PR</a>, <a href="github-permissions.html">access</a>, and <a href="rules.html">rules</a>', 'Why push, approval, passing tests, and merge are separate.']
      ]) + '<p>Try 20–30 minutes when that suits you. Repeat difficult exercises in a new practice folder. You do not need to finish every topic in one sitting.</p>'),
      section('checks', 'Before changing shared history', '<ul class="checklist"><li>Read status. Confirm the project, branch, and remote.</li><li>Keep wanted edits and the old committed position.</li><li>Fetch and read the shared work you will affect.</li><li>Agree with anyone using the branch before replacing commits.</li><li>Check final files, history, and tests before sending the result.</li></ul>'),
      section('progress', 'Keep a copy of your progress', '<p>The browser stores completed lessons, answers, checked steps, exercises, and card-review times when storage is available. It cannot check work in actual repositories. Export before changing devices or clearing browser data.</p><p>Export makes a JSON text file of your progress. Import reads it and asks before replacing current progress.</p><div class="actions only-js"><button class="btn" id="export-progress">Export progress JSON</button><button class="btn" id="import-trigger">Import progress JSON</button><input id="import-progress" type="file" accept=".json,application/json" aria-label="Choose a Git learning backup" hidden><button class="btn" id="reset-progress">Reset learning progress</button></div><p id="progress-message" role="status"></p><p id="progress-summary"></p>')
    ], ['Explain what changes before naming the command.', 'Use mistakes to choose your next practice.', 'Export progress if you want to keep it elsewhere.'])

    lesson('reference', 'Find a command or a word', 20,
      'Look up a task and check what its command changes. Find plain meanings for Git words and links to the full manuals.',
      ['Choose a command by the result you need.', 'Look up an unfamiliar word.', 'Use official manuals for more options and version details.'], [
      section('commands', 'What do you want to do?', '<p>These are separate examples, not a script. Replace path, COMMIT, TARGET, and example branch names with the actual file or ID you checked. Read the related lesson before replacing files or shared commits.</p><div class="filters only-js"><label class="field">Find a task or command<input id="command-search" type="search" placeholder="staging, unstage, recover, push…"></label><button class="btn" id="print-reference">Print reference</button></div><p id="command-count" class="meta" aria-live="polite"></p><div id="command-table">' + table(['Your task', 'Command', 'What to remember'], [[escape(task), '<code>' + escape(cmd) + '</code>', escape(tip)] for topic, task, cmd, tip in COMMANDS]) + '</div><p class="empty" id="command-empty" hidden>No matching command. Try the problem-fixing page for an error message.</p>'),
      section('glossary', 'Words explained in plain English', '<p>Return when a word gets in the way. <a href="foundations.html#areas">HEAD, index, staging, and diff are shown with one file here.</a></p><dl class="glossary">' + ''.join('<dt>' + escape(name) + '</dt><dd>' + escape(body) + '</dd>' for name, body in GLOSSARY) + '</dl>'),
      section('sources', 'Official manuals for more detail', '<p>GitHub features depend on plan, visibility, organization settings, and Enterprise version. Git options depend on your installed version. Check <code>git --version</code> and <code>git help COMMAND</code> for your local manual. Sources reviewed in October 2026.</p><ul class="source-list">' + ''.join('<li><a href="' + url + '">' + title + '</a></li>' for title, url in [
        ('Pro Git book', 'https://git-scm.com/book/en/v2'), ('Git command manuals', 'https://git-scm.com/docs'),
        ('Git add: choosing content', 'https://git-scm.com/docs/git-add'), ('Git diff: comparing versions', 'https://git-scm.com/docs/git-diff'),
        ('Git merge', 'https://git-scm.com/docs/git-merge'), ('Git rebase', 'https://git-scm.com/docs/git-rebase'), ('Git push and leases', 'https://git-scm.com/docs/git-push'),
        ('Git restore', 'https://git-scm.com/docs/git-restore'), ('Git reset', 'https://git-scm.com/docs/git-reset'), ('Git revert', 'https://git-scm.com/docs/git-revert'), ('Git reflog', 'https://git-scm.com/docs/git-reflog'),
        ('Git bisect', 'https://git-scm.com/docs/git-bisect'), ('Git range-diff', 'https://git-scm.com/docs/git-range-diff'),
        ('GitHub PR merge choices', 'https://docs.github.com/en/pull-requests/reference/pull-request-merges'),
        ('GitHub repository roles', 'https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization'),
        ('GitHub tokens', 'https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens'),
        ('GitHub rulesets', 'https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets'),
        ('CODEOWNERS', 'https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners'),
        ('Actions job tokens', 'https://docs.github.com/en/actions/tutorials/authenticate-with-github_token'),
        ('Actions security', 'https://docs.github.com/en/actions/reference/security/secure-use'),
        ('Removing sensitive data', 'https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository')
      ]) + '</ul>')
    ], ['Choose by what should change and what must stay.', 'Learn a word through its example before its extra details.', 'Use the manual for a specific version or setting.'])
