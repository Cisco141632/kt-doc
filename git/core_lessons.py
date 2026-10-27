"""Git and GitHub explained with small actions and checks after each action."""
from lesson_parts import code, table, section, note, flow, graph, source, words, steps, compare, walk, three, filebox, ask, fixes


def add_core(lesson):
    lesson('foundations', 'Your file, staging, and HEAD', 35,
      'Use one small text file to see what Git saves. Learn HEAD, index, staging, and diff by watching the file change.',
      ['Make your first local project and commit.', 'Explain the three places using the actual text in a file.', 'Read each diff and predict what the next commit will save.'], [
      section('words', 'Start with these five meanings', words([
        ('Commit = a saved project version', 'You choose when Git saves a version. Each saved version has a message and an ID, such as <code>7ac19d2</code>. A commit stays on your computer until you send it elsewhere.'),
        ('Staging = choosing content for the next commit', 'Think of a tray marked “save these changes next.” <code>git add notes.txt</code> puts the file’s current content on that tray. Editing the file later does not change what is already on the tray.'),
        ('Index = Git’s name for that staging area', 'These are two names for the same thing. You do not need to learn two separate places. The index records the file versions you have chosen for the next commit.'),
        ('HEAD = where you are in saved history', 'HEAD tells Git which commit you are using. Usually it does this through your current branch. For example: <code>HEAD → main → commit A</code>. Before the first commit, main has no saved commit yet.'),
        ('Diff = a view of what changed', 'A diff compares two versions. A line starting with <code>-</code> was removed; a line starting with <code>+</code> was added. The command you choose decides which two versions Git compares.')
      ])),
      section('first-repository', 'Make a tiny practice project',
        '<p>A <b>terminal</b> is a window where you type commands. Run one step at a time. These examples use a Linux or macOS shell; on Windows, use Git Bash. A <b>repository</b> is your project plus its Git history.</p>' +
        steps([
          ('Check that Git is installed', 'Type the command and press Enter. If it is missing, install Git from <a href="https://git-scm.com/downloads">the official download page</a>, reopen your terminal, and try again. These lessons use Git 2.28 or later.', 'git --version', 'A version number, such as <code>git version 2.43.0</code>. Your number may differ.'),
          ('Make a new folder and go into it', '<code>mkdir</code> makes a folder. <code>cd</code> enters it. Choose a new name if this folder already exists.', 'mkdir git-notes-practice\ncd git-notes-practice', 'You are now inside your new, empty folder.'),
          ('Ask Git to keep history here', '<code>init</code> starts Git in this folder. <code>-b main</code> names your first branch main. Nothing is uploaded to GitHub.', 'git init -b main', 'Git reports that it created a repository. It also makes a hidden <code>.git</code> folder. Leave that folder alone.'),
          ('Set the name shown on your practice commits', 'These settings apply only to this project. Replace the example name and email with the ones you want on your commits. They label commits; they do not sign you into GitHub.', 'git config user.name "Your Name"\ngit config user.email "you@example.com"', 'Usually no output. <code>git config user.name</code> lets you check the saved name.'),
          ('Create one text file', '<code>printf</code> writes text. <code>></code> replaces the named file, so use it only for this new practice file.', "printf 'Hello\\n' > notes.txt", 'Open notes.txt in your editor. It contains one line: <code>Hello</code>.'),
          ('Ask Git what it sees', 'Status is a report about the current project. It does not save or discard anything.', 'git status', '<code>notes.txt</code> appears under “Untracked files.” This means Git has not yet chosen it for a commit.'),
          ('Choose this file for the next commit', 'This is the staging step. It chooses the content currently in notes.txt.', 'git add -- notes.txt', 'Run <code>git status</code>. The file is under “Changes to be committed.” The <code>--</code> separates options from file names.'),
          ('Look at what you are about to save', '<code>--staged</code> means “show the changes already chosen for the next commit.”', 'git diff --staged', 'The new line appears as <code>+Hello</code>. With no earlier commit, Git compares it with an empty starting point.'),
          ('Save the first version', '<code>-m</code> gives this saved version a short message.', 'git commit -m "Write my first note"', 'Git reports one new commit. <code>git log --oneline</code> shows its ID and message. <code>git status</code> reports a clean working tree: no changes to the tracked file are waiting.')
        ])),
      section('areas', 'Watch one file in three places',
        '<p>Start after the first commit above. Use the buttons to move one step at a time. Notice that the same file can have different content in each place.</p>' +
        walk('What happens if I edit again after git add?', [
          ('Start: Hello is saved', 'Your file, your chosen content, and your current commit all contain Hello. HEAD points through main to this commit.', three('Hello', 'Hello', 'Hello')),
          ('Edit Hello to Hi', 'Open notes.txt, change Hello to Hi, and save the file in your editor. Only your file changes. You have not made a Git commit.', three('Hi', 'Hello', 'Hello')),
          ('Run git add -- notes.txt', 'Git chooses Hi for the next commit. This chosen version is kept even if you edit the file again.', three('Hi', 'Hi', 'Hello')),
          ('Edit Hi to Good morning', 'Save the new text in your editor. You have two changes to compare: Hello → Hi is chosen; Hi → Good morning is still only in your file.', three('Good morning', 'Hi', 'Hello')),
          ('Run git commit -m "Use a short greeting"', 'Git saves Hi because Hi was chosen. HEAD now points through main to the new commit. Your file still says Good morning.', three('Good morning', 'Hi', 'Hi')),
          ('Run git add, then commit, to save Good morning too', 'Choose the newer text with git add -- notes.txt. Check git diff --staged, then commit it with a new message. Now all three places match again.', three('Good morning', 'Good morning', 'Good morning'))
        ]) + ask('At step 4, what will git commit save?', '<b>Hi.</b> That is what you chose at step 3. The later edit, Good morning, has not been chosen yet.')),
      section('diff', 'Which two versions does each diff compare?',
        '<p>At step 4 above, your file says Good morning, your staging area holds Hi, and HEAD still leads to Hello.</p>' +
        table(['Command', 'Compares', 'The change you see'], [
          ['<code>git diff</code>', 'Chosen content → your file', '<code>-Hi</code><br><code>+Good morning</code>'],
          ['<code>git diff --staged</code>', 'Current saved commit → chosen content', '<code>-Hello</code><br><code>+Hi</code>'],
          ['<code>git diff HEAD</code>', 'Current saved commit → your file', '<code>-Hello</code><br><code>+Good morning</code>']
        ]) + '<p>A plain diff does not show the contents of a new, untracked file. Start with <code>git status</code> to find it. In diff output, <code>---</code> and <code>+++</code> label the two files. A heading such as <code>@@ -1 +1 @@</code> gives the line numbers around the change.</p>' +
        code('git status --short', 'A shorter status report') +
        '<p>If you see <code>MM notes.txt</code>, the <b>first M</b> means the chosen content differs from the saved commit. The <b>second M</b> means your file differs from the chosen content. M means “modified.” <code>??</code> means untracked. You can always use the longer <code>git status</code> while learning.</p>'),
      section('inside', 'How Git keeps these versions',
        '<p>Inside <code>.git</code>, Git stores saved file content and the information needed to rebuild each saved project. Git calls a stored file’s content a <b>blob</b>. A <b>tree</b> records file names, folders, and which stored contents belong there. A commit points to the project tree, its earlier commit or commits, the name and time recorded, and the message.</p>' +
        '<p>A branch is a name that points to one commit. HEAD usually names the current branch. When you commit on main, main moves to the new commit, and HEAD still names main. These links let Git find your current saved files without copying the whole project for every branch.</p>' +
        flow([('HEAD', 'You are using main'), ('main', 'Points to saved commit B'), ('Commit B', 'Points to saved files and earlier commit A')]) +
        '<p><code>git add</code> stores the chosen file content and updates the index entries for it. <code>git commit</code> records a project version from those entries. Git gives stored objects IDs calculated from their contents. Changing a commit message or its earlier-commit link creates a different commit ID, even if the files are the same.</p>' +
        code('git show HEAD:notes.txt\ngit show :notes.txt', 'Read the saved file, then the staged file; these commands do not edit either one') +
        '<p><code>HEAD:notes.txt</code> means “notes.txt in the current commit.” <code>:notes.txt</code> means “notes.txt in the staging area.” These work after the file has been added; the HEAD form needs a first commit.</p>' +
        note('If you see “detached HEAD”', 'You are using a saved commit directly, rather than working through a branch name. To keep new work there, run <code>git switch -c keep-my-work</code> before switching away. Choose a branch name that does not already exist.')),
      section('problems', 'If the result is different', fixes([
        ['“Not a git repository”', '<code>pwd</code> shows your folder; <code>git status</code> checks it.', 'Use <code>cd</code> to enter git-notes-practice. Run status again.'],
        ['“Nothing to commit”', 'Read status. Did you change the file? Did you run add?', 'If there are changes you want to save, add that file, inspect <code>git diff --staged</code>, then commit.'],
        ['“Please tell me who you are”', '<code>git config user.name</code> and <code>git config user.email</code>.', 'Set the two local values from the setup steps, then retry the commit.'],
        ['“Why did my new edit stay out of the commit?”', 'Compare <code>git diff</code> with <code>git diff --staged</code>.', 'You edited after add. Add the file again only if you want the newer content in the next commit. Check the staged diff.'],
        ['“I chose the wrong file”', 'Read the staged diff before changing anything.', '<code>git restore --staged -- notes.txt</code> removes that file’s changes from the next commit after you have a first commit. Your edited file stays.']
      ]) + '<p>Try the same idea with buttons in the <a href="studio.html#snapshots">file, staging, and commit exercise</a>, then with real Git in <a href="practice.html#staging">lab 1</a>.</p>' + source(('Git add', 'https://git-scm.com/docs/git-add'), ('Git commit', 'https://git-scm.com/docs/git-commit'), ('Git diff', 'https://git-scm.com/docs/git-diff')))
    ], ['Your file is what you edit. Staging holds what you chose for the next commit.', 'Index means staging area. HEAD tells Git which saved commit you are using.', 'git diff shows changes still in your file; git diff --staged shows changes chosen for the next commit.'], 'foundations')

    lesson('daily-workflow', 'Save a change, one step at a time', 25,
      'Follow a small change from editing to a saved commit. Check exactly what will be included before you save it.',
      ['Read status before changing anything.', 'Save only the change you meant to save.', 'Keep temporary files and private settings out of new commits.'], [
      section('start', 'Begin in the right place',
        '<p>Use the practice project from the previous lesson. A <b>tracked file</b> is a file Git already knows about through staging or a commit. An <b>untracked file</b> has not been added yet.</p>' +
        steps([
          ('Read the current state', 'Status says which branch you are using and whether any changes are waiting.', 'git status', 'In a finished practice project, the branch is main and the working tree is clean.'),
          ('Make one small change', 'Open notes.txt. Add the line “I can save a change.” Save the file in your editor.', '', 'Status now lists notes.txt as modified, under “Changes not staged for commit.”'),
          ('Read what changed', 'Check that the added sentence is the change you meant to make.', 'git diff -- notes.txt', 'A <code>+</code> line shows the new sentence.'),
          ('Choose that file', 'Git chooses its current content for the next commit.', 'git add -- notes.txt', 'Status puts notes.txt under “Changes to be committed.”'),
          ('Read the chosen change', 'This is your last content check before saving the commit.', 'git diff --staged', 'Only the sentence you intended to add is included.'),
          ('Save with a useful message', 'Say what you changed. A message such as “Add a practice note” is more useful than “stuff.”', 'git commit -m "Add a practice note"', 'Git shows the new commit ID and the number of changed files.'),
          ('Check the saved result', '<code>show</code> displays the latest saved change. <code>--stat</code> gives a short file list.', 'git show --stat HEAD\ngit status', 'The new commit contains notes.txt. Status shows whether anything remains unsaved in Git.')
        ])),
      section('commit', 'What changes after add and commit?', compare(
        filebox('Before add', 'File: new sentence\nChosen: old text\nCommit: old text'),
        'add → check → commit',
        filebox('After commit', 'File: new sentence\nChosen: new sentence\nCommit: new sentence')) +
        '<p>If your file changes after add, stop and read both diffs. Commit saves the chosen content. It does not automatically choose your newest edit.</p>' +
        '<p>For two unrelated changes in the same file, <code>git add -p -- notes.txt</code> lets you choose small groups of changed lines. Git calls each group a <b>hunk</b>. Read each group and answer the prompt. If this feels difficult, make and save one small change at a time first.</p>' +
        ask('Does changing the commit message remove a file you chose by mistake?', 'No. The message describes the change. Use <code>git restore --staged -- filename</code> to remove a tracked file’s changes from the next commit, then check the staged diff.')),
      section('ignore', 'Tell Git which new files to leave out',
        '<p><code>.gitignore</code> is a text file listing new files Git should usually leave out. For example, a log file is a record of a program running. A local settings file may hold private passwords.</p>' +
        code('.env\n*.log\n.venv/', 'Example .gitignore file — edit this in your text editor') +
        '<p><code>.env</code> matches a file with that name. <code>*.log</code> matches names ending in .log. <code>.venv/</code> matches that folder. Save and commit .gitignore so teammates get the rules too.</p>' +
        '<p>These rules do not remove a file Git already tracks. To stop tracking an existing file while keeping your local copy, first inspect <code>git ls-files -- .env</code>, then use <code>git rm --cached -- .env</code> and commit the removal. Earlier commits still contain the old file. If it held a password or token, <a href="security-automation.html#secret">disable or replace that secret first</a>.</p>' +
        '<p><code>git check-ignore -v -- debug.log</code> tells you which rule ignores debug.log. Do not ignore files just because they are generated: your project may need dependency lockfiles, which record exact package versions.</p>'),
      section('handoff', 'When you work with a team',
        '<p>A <b>remote</b> is a saved name and address for another Git repository. A <b>push</b> sends your commits there. You will set this up in the next lesson. A commit by itself stays local.</p>' +
        flow([('Edit', 'Change one thing'), ('Check', 'Read git diff'), ('Choose', 'Run git add'), ('Check again', 'Read git diff --staged'), ('Commit', 'Save with a message')]) +
        '<p>For program changes, run the project’s tests before pushing. Tests are commands the project provides to check behavior; Git does not run them automatically. Before asking a teammate to review, say what changed and which checks you ran.</p>'),
      section('problems', 'If something goes wrong', fixes([
        ['Switching branches says it would overwrite your changes.', 'Read <code>git status</code> and both diffs.', 'Save useful work with a commit, or use the temporary-save steps in <a href="undo-recovery.html#stash">the stash lesson</a>. Then retry the switch.'],
        ['The commit includes unrelated changes.', 'Before committing, read <code>git diff --staged</code>.', 'Remove unwanted changes from staging with restore --staged, then check again. If already shared, make a new correction instead of silently changing shared history.'],
        ['Git says index.lock exists.', 'Another Git command or editor may still be running.', 'Let it finish. Remove the lock only after confirming it is left over from a stopped process. Run status afterward.']
      ]) + source(('Staging files', 'https://git-scm.com/docs/git-add'), ('Ignore rules', 'https://git-scm.com/docs/gitignore')))
    ], ['Read status, read the change, choose it, check it, then commit.', 'Saving a file in your editor and making a Git commit are separate actions.', 'Ignore rules only help with files that are not already tracked.'], 'daily-workflow')

    lesson('branches-remotes', 'Branches and sharing with GitHub', 35,
      'Try work on a branch, send commits to GitHub, and bring a teammate’s changes back. See why fetch, pull, and push do different jobs.',
      ['Explain a branch using a small history picture.', 'Connect a local project to the right GitHub repository.', 'Check new shared work before combining it with yours.'], [
      section('words', 'Names you will see', words([
        ('Branch', 'A name pointing to a saved commit. New commits move the name forward. You can work on a branch called add-title while main keeps the agreed project version.'),
        ('Remote and origin', 'A remote is the saved address of another repository. <code>origin</code> is the usual name for that address. It is a name you can choose, not another word for GitHub.'),
        ('origin/main', 'Your computer’s last known position of main on origin. It can be out of date. <code>git fetch origin</code> asks the other repository for updates.'),
        ('Upstream', 'The remote branch your local branch is set to follow. <code>git push -u</code> sets that link. The name upstream is also often used for the original project when someone works from their own GitHub copy, called a fork.')
      ])),
      section('branch', 'Try an idea away from main',
        steps([
          ('Start from saved work', 'In your practice project, finish or save any waiting changes first.', 'git status', 'A clean working tree means no tracked-file changes are waiting.'),
          ('Make and enter a branch', '<code>switch -c</code> creates a branch and makes it your current branch.', 'git switch -c add-title', 'Git reports that you switched to add-title. Both branches start at the same commit.'),
          ('Make a commit on the new branch', 'Edit notes.txt to add a title. Save it, then choose and commit the change.', 'git add -- notes.txt\ngit commit -m "Add a title"', 'add-title now points to a new commit. main stays at the earlier commit.'),
          ('Return to main and compare', 'Git changes your tracked files to match the branch you enter.', 'git switch main', 'The title is absent on main. <code>git switch add-title</code> brings it back. Neither saved version was deleted.')
        ]) + graph('Before:  A ← main, add-title\n\nAfter a commit on add-title:\nA ← main\n└── B ← add-title, HEAD', 'A and B mean saved commits. B remembers A as its earlier commit. A branch does not copy the entire folder.')),
      section('connect', 'Put the practice project on GitHub',
        '<p>You need a GitHub account and Git installed. To sign in from your terminal, follow <a href="https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git">GitHub’s credential setup steps</a>. A credential is the key or token that proves which account you are using. The GitHub website password is not used as the password for Git over HTTPS.</p>' +
        steps([
          ('Create the shared project on GitHub', 'On GitHub, choose New repository. Name it git-notes-practice. Choose the visibility you want. Since you already have local commits, leave README, license, and .gitignore creation off here.', '', 'GitHub shows an empty repository with a Code address. Public means other people can read the published files.'),
          ('Save that address in your local project', 'Copy the HTTPS or SSH address shown by GitHub. Replace REPOSITORY_URL below with it; do not type the placeholder or put a token in the address.', 'git remote add origin REPOSITORY_URL', 'Usually no output. <code>git remote -v</code> should show the intended owner and project name.'),
          ('Send main', 'Run this while main has the saved work you want to share. <code>-u</code> also links your local main to origin/main.', 'git push -u origin main', 'Refresh the GitHub page. It shows the commits and files sent from main.'),
          ('Send your idea branch too', 'The feature branch is separate from main on GitHub as well.', 'git switch add-title\ngit push -u origin add-title', 'GitHub lists add-title. Sending it does not combine it into main.')
        ]) +
        '<p>If the project already exists on GitHub, start by copying it instead: <code>git clone REPOSITORY_URL git-notes-copy</code>, then <code>cd git-notes-copy</code>. <b>Clone</b> means make a local copy with Git history. It also sets origin. Use a new destination folder.</p>'),
      section('three-refs', 'Your branch, your last check, and GitHub',
        walk('A teammate saves a new commit T on GitHub', [
          ('Before you check', 'Your local main and origin/main still say B. GitHub main has T. origin/main is a local note, so it does not update itself just because someone else pushed.', graph('Your computer: main → B     origin/main → B\nGitHub:       main → T     (T follows B)', 'You have not fetched T yet.')),
          ('Run git fetch origin', 'Git downloads new history and updates origin/main to T. Your main and your edited files stay as they were.', graph('Your computer: main → B     origin/main → T\nGitHub:       main → T', 'Fetch lets you inspect new work before using it.')),
          ('Use the new work', 'With a clean main at B, run git merge --ff-only origin/main. Because T continues from B, main can move to T.', graph('Your computer: main → T     origin/main → T\nGitHub:       main → T', 'Now your local main includes the teammate’s saved version.'))
        ])),
      section('fetch-pull', 'Choose the command for the job', table(['Command', 'What it does', 'What it leaves alone'], [
        ['<code>git fetch origin</code>', 'Download shared history and update your last-known positions.', 'Your current branch and working files.'],
        ['<code>git pull --ff-only</code>', 'Fetch, then move your branch forward only if no separate local commits need combining.', 'It refuses if both sides have new commits.'],
        ['<code>git pull --no-rebase</code>', 'Fetch, then combine using a merge.', 'It keeps existing commits; a new merge commit may be needed.'],
        ['<code>git pull --rebase</code>', 'Fetch, then make new versions of your local commits after the fetched work.', 'It does not send the result back; it may pause for conflicts.'],
        ['<code>git push</code>', 'Ask the other repository to accept your commits and update its branch.', 'It does not download and combine a teammate’s new work for you.']
      ]) + '<p>Plain <code>git pull</code> can behave differently with different settings. While learning, fetch, inspect, and choose the next step. <code>git branch -vv</code> shows branch links and ahead/behind counts based on your last fetch. <b>Ahead</b> means local-only commits; <b>behind</b> means commits seen on the remote side but missing from your branch.</p>'),
      section('push', 'If push or pull is rejected', fixes([
        ['Push says non-fast-forward.', 'Someone may have pushed first. Run <code>git fetch origin</code>, then <code>git log --graph --oneline --all</code>.', 'On a shared branch, inspect and merge the matching remote branch, test, then push normally. See <a href="troubleshooting.html#rejected-push">the full fix</a>.'],
        ['Pull --ff-only refuses.', 'Both sides have commits after their shared starting commit.', 'Use the <a href="merge.html">merge lesson</a>, or use rebase only when suitable for that branch. Do not force a push to fix a local pull.'],
        ['“No upstream branch.”', 'Read <code>git branch -vv</code> and <code>git remote -v</code>.', 'For add-title, use <code>git push -u origin add-title</code>. Check the destination first.'],
        ['Remote origin already exists.', 'Read <code>git remote -v</code>.', 'If it is correct, keep it. If it is wrong, use <code>git remote set-url origin REPOSITORY_URL</code> with the address you checked, then inspect again.']
      ])),
      section('cleanup', 'Remove old branch names carefully',
        '<p><code>git fetch --prune origin</code> removes your local records of remote branches that have been deleted. It does not delete a teammate’s live branch on GitHub. After your work is combined and checked, <code>git branch -d add-title</code> deletes your local branch name, with a check that its history is included in its upstream or the current branch. Switch away from that branch first.</p>' +
        '<p><code>-D</code> skips that history check. After a squash merge, the files may be included even though the original commits are not; inspect before deleting. <code>git push origin --delete add-title</code> deletes the server branch. Use that only after the team is finished with it.</p>' + source(('Branches', 'https://git-scm.com/docs/git-branch'), ('Fetch', 'https://git-scm.com/docs/git-fetch'), ('Pull', 'https://git-scm.com/docs/git-pull')))
    ], ['A branch is a name for a saved commit; HEAD tells Git which one you are using.', 'Fetch checks for shared updates. Pull fetches and uses them. Push sends your commits.', 'origin/main is your last-known position, so fetch before relying on it.'], 'branches-remotes')

    lesson('merge', 'Merge: put two sets of work together', 35,
      'See how Git uses the shared starting version to combine changes. Learn what to check when the merge finishes.',
      ['Explain a simple merge with before and after pictures.', 'Tell a branch move from a new merge commit.', 'Check the combined files and handle a refused merge.'], [
      section('idea', 'One project, two useful changes',
        '<p>Your settings file starts with timeout 10 and retries 1. Timeout is how long a request waits; retries is how many times it tries again. On main, you increase timeout to 20. On feature, your friend increases retries to 3. You want both changes.</p>' +
        words([('Base', 'The saved version both branches started from. It tells Git what each person changed.'), ('Parent', 'An earlier commit recorded by a commit. Most commits have one parent; a normal merge commit records two.'), ('Fast-forward', 'Git can move a branch name to an existing later commit when there is no separate work on that branch to combine.')]) +
        table(['Version', 'Timeout', 'Retries', 'What changed?'], [['Base B', '10', '1', 'Starting values.'], ['Main C', '20', '1', 'Only timeout changed.'], ['Feature D', '10', '3', 'Only retries changed.'], ['Merge M', '20', '3', 'Both changes kept.']]) +
        '<p>This is called a <b>three-way merge</b> because Git reads the base and the two branch versions. Reading only the last two files would not show who changed which value.</p>'),
      section('three-way', 'See a merge before and after',
        walk('Two branches made separate commits', [
          ('Before: both changes exist separately', 'C and D both follow B. Neither branch contains the other branch’s new commit.', graph('    C ← main\n   /\nA─B\n   \\\n    D ← feature', 'B is the shared starting commit.')),
          ('On main, run git merge feature', 'Git compares B → C and B → D. If it can combine the text, it builds the result. If it cannot, it pauses and asks you to choose the final content.', table(['File value', 'Final result'], [['timeout', '20'], ['retries', '3']])) ,
          ('After: main points to merge commit M', 'M records both C and D as parents. Existing commits do not change. Feature still points to D.', graph('    C──M ← main\n   /  /\nA─B  /\n   \\/\n    D ← feature', 'The links show that main now includes both saved histories.'))
        ])),
      section('perform', 'Try a real merge in lab 3',
        '<p>Create the <a href="practice.html#setup">practice folders</a> first. Open a terminal in its <code>03-three-way</code> folder. This setup already has the two changes.</p>' +
        steps([
          ('Read the starting state', 'Finish or save unrelated edits before merging.', 'git status\ngit log --graph --oneline --all', 'Main and feature have separate commits. The tracked files are clean.'),
          ('Find the starting commit', 'This prints the commit ID Git uses as their common starting point.', 'git merge-base main feature', 'One ID. In a complicated history there can be more than one suitable common base.'),
          ('Combine feature into your current branch', 'In this lab you are on main. If an editor opens for the merge message, save and close it.', 'git merge feature', 'Git reports a merge. If it reports conflicts, use the next lesson before continuing.'),
          ('Read both values and the history', 'Check content as well as the new commit links.', 'cat timeout.txt retries.txt\ngit show --no-patch --pretty="%h %p %s" HEAD', 'The values are 20 and 3. The line from show has the new ID, two parent IDs, and the message.')
        ]) + '<p>For a real program, also run tests covering both changes together. A merge can combine text successfully while combining behavior incorrectly, such as a renamed function whose callers still use its old name.</p>'),
      section('fast-forward', 'When no new merge commit is needed', compare(
        graph('A─B ← main\n   └─C─D ← feature', 'Main has no separate work after B.'),
        'On main: git merge --ff-only feature',
        graph('A─B─C─D ← main, feature', 'Only main’s position changes. No new commit is needed.')) +
        '<p><code>--ff-only</code> means “only do this if moving the branch name is enough.” A later date alone is not enough. The old main commit must be in the earlier history of feature.</p>'),
      section('modes', 'Three ways to keep the result', table(['Method', 'Saved result', 'What to remember'], [
        ['Normal merge', 'Keeps both histories; may fast-forward or add a two-parent commit.', '<code>--no-ff</code> asks for a merge commit even when a simple move would work.'],
        ['Squash', '<code>git merge --squash feature</code> chooses the combined changes. You inspect and commit them separately.', 'The new commit has one parent. It does not link the feature commits as a second parent.'],
        ['Rebase, then combine', 'Makes new copies of the feature changes after a newer base.', 'Commit IDs change. Read the rebase lesson before using this on work others have seen.']
      ]) + ask('Does a squash mean Git remembers feature as a merged parent?', 'No. It saves combined file changes in one new commit, with one parent. The files can match while the history links differ.')),
      section('problems', 'When the merge needs help', fixes([
        ['Merge paused with conflicts.', 'Run <code>git status</code>. It names the files needing a choice.', 'Edit the correct final content, add each resolved file, test, then run <code>git merge --continue</code>.'],
        ['You want to stop the merge.', 'Check that a merge is still in progress.', 'Use <code>git merge --abort</code>. Starting with unsaved unrelated changes can make an exact return harder.'],
        ['“Already up to date.”', 'Look at the branch names and <code>git log --graph --oneline --all</code>.', 'Git already has that branch’s commits in your current history. If a previous revert removed their effect, see the <a href="troubleshooting.html#reverted-merge">reverted merge example</a>.']
      ]) + source(('How merge works', 'https://git-scm.com/docs/git-merge'), ('Merge base', 'https://git-scm.com/docs/git-merge-base')))
    ], ['Merge uses the shared starting files to understand both changes.', 'Fast-forward moves a name; a normal two-sided merge adds a commit with two parents.', 'A successful text merge still needs a check of the final behavior.'], 'merge')

    lesson('conflicts', 'Fix a conflict, one file at a time', 40,
      'A conflict means Git needs your help choosing the final file. Read both changes, edit the result, and finish the right operation.',
      ['Read conflict markers and the original three versions.', 'Keep the needed changes from both people.', 'Check, continue, or stop a merge or rebase correctly.'], [
      section('first', 'First find out what paused',
        '<p>A <b>conflict</b> means Git could not choose some part of the combined result. Your saved commits are still there. It is common when two people edit the same lines differently. It can also happen when one deletes a file and another edits it.</p>' +
        code('git status', 'Start with this report') +
        '<p>Read whether it says merge, rebase, cherry-pick, or revert. Those operations have different finish and stop commands. List files needing a choice with <code>git diff --name-only --diff-filter=U</code>. Here U means unmerged: Git is waiting for you to resolve the file.</p>'),
      section('markers', 'Read the marks in the file',
        code('<<<<<<< HEAD\ntimeout = 20\n||||||| base\ntimeout = 10\n=======\ntimeout = 30\n>>>>>>> feature', 'Example text in a conflicted file — do not type this as commands') +
        '<p>In a merge done while on main, the first block is main’s value, 20. The base block shows the old value, 10. The last block is feature’s value, 30. You need to decide the correct value; Git cannot know the project’s rule.</p>' +
        '<p>The base block appears when you set <code>git config --local merge.conflictStyle diff3</code> before a new conflict. Some editors show only the first and last blocks. In all cases, remove the marks after writing the intended result.</p>' +
        words([('Ours and theirs during a merge', 'Ours means the branch you are on; theirs means the branch you are merging into it.'), ('Ours and theirs during a rebase', 'Ours means the new starting branch plus changes already copied onto it. Theirs means the original commit being copied now. The labels can feel reversed, so read the actual content.')]) +
        '<p>Git also keeps the conflict versions in numbered index entries. Run <code>git show :1:config.json</code> for the base, <code>git show :2:config.json</code> for ours, and <code>git show :3:config.json</code> for theirs. Some versions may be absent, for example when a file was newly added or deleted. <code>git ls-files -u</code> lists these entries.</p>'),
      section('resolve', 'Build one correct file',
        '<p>In lab 4, the team requires <b>timeout 20</b> from main and <b>retries 3</b> from feature. JSON is a settings format using named values inside braces. Neither whole branch has both required values.</p>' +
        compare(filebox('Two sides', 'Main:    timeout 20, retries 1\nFeature: timeout 30, retries 3'), 'Read the requirement and edit', filebox('Final config.json', '{"timeout": 20, "retries": 3}')) +
        steps([
          ('Read both changes and the rule', 'Use the file versions above, commit messages, and the task description. If two rules disagree, ask the people responsible for the change.', 'git status\ngit diff', 'You know what each side tried to change and what the final file should do.'),
          ('Edit and save the final file', 'In your editor, write one valid result. Remove conflict markers and duplicate settings.', '', 'config.json has timeout 20 and retries 3, with one of each key.'),
          ('Tell Git you resolved this file', 'Add chooses your edited result and replaces the unresolved entries for this file.', 'git add -- config.json', 'Status no longer lists config.json as unmerged.'),
          ('Check the chosen result', '<code>--cached</code> is another name for <code>--staged</code>. <code>--check</code> can catch leftover markers and whitespace errors, but cannot prove the settings are correct.', 'git diff --staged\ngit diff --staged --check\ngit diff --name-only --diff-filter=U', 'The chosen changes are intended. The unresolved-file command prints nothing after all files are fixed. Run the project tests too.'),
          ('Finish the merge', 'Use this only when status says a merge is in progress. For a rebase, use git rebase --continue instead.', 'git merge --continue', 'The merge completes. Read status and test the final files.')
        ]) + ask('Why can “Accept both” be wrong?', 'It can keep two incompatible values, duplicate a function, or make invalid JSON. Keep the required behavior, then check the file format.')),
      section('types', 'Other conflicts use the same careful process', table(['Conflict', 'What to decide', 'How to finish the file'], [
        ['Deleted on one side, edited on the other', 'Should the final project still have this file?', 'Use <code>git rm -- filename</code> for the intended deletion, or keep/edit the file and add it.'],
        ['Both sides added the same file name', 'Which combined contents should exist?', 'Read both complete files, create one result, and add it. A base version may not exist.'],
        ['File renamed differently', 'What should the final name be?', 'Check both names and code using them. Keep the intended paths and stage the changes. Git detects renames by comparing content.'],
        ['Image or other binary file', 'Which real file is the correct result?', 'Choose or rebuild it, open it in its program, then add it. Text markers may be unavailable.'],
        ['Dependency lockfile', 'Which package changes were intended?', 'Resolve the package list first, then rebuild the lockfile with the project’s required package-manager version. Review and test.'],
        ['Generated file', 'Which source input should produce it?', 'Resolve the input, generate the output again, and review it.'],
        ['No text conflict, but the program breaks', 'Did the combined changes make different assumptions?', 'Check the failing behavior and both changes. For example, a function rename and an old caller can merge cleanly but fail when run.']
      ])),
      section('abort', 'Finish or stop the operation named by status', table(['Operation', 'Continue after fixing and adding', 'Stop and return'], [
        ['Merge', '<code>git merge --continue</code>', '<code>git merge --abort</code>'],
        ['Rebase', '<code>git rebase --continue</code>', '<code>git rebase --abort</code>'],
        ['Cherry-pick', '<code>git cherry-pick --continue</code>', '<code>git cherry-pick --abort</code>'],
        ['Revert', '<code>git revert --continue</code>', '<code>git revert --abort</code>'],
        ['Stash apply or pop', 'Resolve, add, and decide when to commit.', 'There is no stash --abort. Preserve earlier edits before undoing the attempted application.']
      ]) + '<p><code>--skip</code> in a rebase or cherry-pick leaves out a commit’s change. Use it only when you have checked that the change is already present or should be dropped. A whole-file command such as <code>git restore --ours -- config.json</code> can drop useful content from the other side.</p>' +
        '<p>Try <a href="playground.html#conflict-lab">the conflict exercise</a> or <a href="practice.html#conflict">real lab 4</a>. If unsure, copy important edited files outside the project before doing more recovery work.</p>' + source(('Conflict versions', 'https://git-scm.com/docs/git-merge'), ('Rebase side names', 'https://git-scm.com/docs/git-rebase')))
    ], ['A conflict asks you to choose the correct final content.', 'Check whether you are merging or rebasing before using ours and theirs.', 'Edit, add, check, test, then use the matching continue command.'], 'conflicts')

    lesson('rebase', 'Rebase: put your changes after newer work', 40,
      'Follow each change as Git applies it again after a newer starting commit. See why commit IDs change and how to recover from a stopped rebase.',
      ['Predict which branch and commit IDs change.', 'Rebase a private practice branch with a way back.', 'Fix a paused step and check that no useful change was lost.'], [
      section('picture', 'Start with the reason',
        '<p>You made two commits on feature. Meanwhile main gained another commit. You want your feature changes to appear after that newer main. <b>Rebase</b> takes your selected changes and applies them again, one at a time, after a new starting commit.</p>' +
        walk('Same intended work, new commit IDs', [
          ('Before: work split after B', 'Main has C. Feature has D and E. Keep a backup name for the old feature before changing it.', graph('A─B─C ← main\n   └─D─E ← feature', 'D follows B, and E follows D.')),
          ('Apply the change from D after C', 'Git compares B with D to get D’s change, then tries that change after C. The new commit is D′. A conflict pauses this step.', graph('A─B─C─D′\n   └─D─E ← backup/feature', 'D′ has C as its parent, so it has a different ID from D.')),
          ('Apply E’s change next', 'E’s change is applied after D′, making E′. Feature moves to E′. Main stays at C.', graph('A─B─C─D′─E′ ← feature\n     ↑\n    main\nOld D─E remain through backup/feature.', 'A normal rebase changes the branch being rebased, not main.'))
        ]) + '<p>Git does not edit D and E in place. Parent links are part of each commit, so new parents mean new IDs. Git may leave out a change already present on the new base. Review the result rather than assuming the number of commits stays the same.</p>'),
      section('procedure', 'Try it on a private branch first',
        '<p>A <b>private branch</b> here means work you have not shared with others. If someone already uses the old commits, changing the branch history needs agreement. In a team project, fetch first and use the intended remote base such as origin/main.</p>' +
        steps([
          ('Start with saved, clean work', 'Read status. Save unrelated edits first. Switch to the branch whose changes you want to reapply.', 'git status\ngit switch feature', 'Feature is current and there are no waiting tracked-file changes.'),
          ('Keep the old feature under another name', 'Choose a new backup name. This keeps committed work, not uncommitted edits.', 'git branch backup/feature-before-rebase', 'Both names point to the old feature commit.'),
          ('Record the old starting point', 'Copy the printed ID into your notes. Later it will be OLD_BASE in the comparison command.', 'git merge-base feature main', 'The common starting commit ID, B in the picture.'),
          ('Reapply feature after main', 'This local practice uses main. In a shared project, use the fetched and checked base, often origin/main.', 'git rebase main', 'Git reports success, or pauses at a conflict with instructions.'),
          ('Check the result', 'Inspect commit order, final files, and the project’s tests. Replace OLD_BASE with the ID you recorded.', 'git log --graph --oneline --all\ngit range-diff OLD_BASE..backup/feature-before-rebase main..feature', 'Range-diff compares the old list of changes with the new list. Read changed or missing entries; it is a review aid, not proof the program still works.')
        ])),
      section('conflict', 'If rebase stops',
        steps([
          ('Read the current step', 'Rebase is applying one original commit at a time.', 'git status\ngit rebase --show-current-patch', 'You can see the change being applied now. A patch is the list of added and removed lines.'),
          ('Edit the intended combined file', 'During rebase, ours is the newer starting work plus changes already reapplied. Theirs is the original commit being applied now.', '', 'The final file keeps the required behavior from both sides.'),
          ('Choose the resolved file, check it, and test', 'Use the actual conflicted file name. This example uses config.json.', 'git add -- config.json\ngit diff --staged', 'The right result is chosen. Run tests before continuing.'),
          ('Continue with the next change', 'The next commit can conflict in the same file again. Check each stop on its own.', 'git rebase --continue', 'The next step runs, or the rebase finishes.')
        ]) + '<p>To return to the pre-rebase branch, use <code>git rebase --abort</code> while rebase is in progress. <code>--quit</code> stops managing the rebase but leaves the current files and commit position. <code>--skip</code> drops the current change from the copied list. These three commands do different jobs.</p>'),
      section('interactive', 'Change the list of commits deliberately',
        '<p><code>git rebase -i main</code> opens a list of commits not on main, oldest first. The <code>-i</code> means interactive: you edit what Git should do. Use this only with a clear starting point and backup.</p>' +
        table(['Word in the list', 'What Git does'], [['pick', 'Apply that commit’s change.'], ['reword', 'Apply it, but ask you to change its message.'], ['edit', 'Pause so you can change or split the commit.'], ['squash', 'Combine it with the previous kept commit and let you edit the message.'], ['fixup', 'Combine it with the previous kept commit, usually leaving out this message.'], ['drop', 'Leave that change out.']]) +
        '<p>Changing order can break a change that needs an earlier one. <code>git commit --fixup COMMIT</code> marks a small correction for a specific commit. <code>git rebase -i --autosquash BASE</code> can place that correction beside it. Replace COMMIT and BASE with checked IDs. Review the edited list before saving.</p>'),
      section('onto', 'Move only a chosen set of changes',
        code('git log old-base..feature\ngit rebase --onto new-base old-base feature', 'Advanced example — these three names must be real branches or checked commit IDs') +
        '<p>Read it as: “Take feature’s commits that are not in old-base, and apply them after new-base.” The first command lets you inspect that selected set. Choosing the wrong old-base can include unrelated work or leave out a needed change.</p>' +
        '<p>A normal rebase usually turns merge history into a single line. <code>--rebase-merges</code> tries to build the merge structure again. That needs extra review, including earlier conflict decisions.</p>'),
      section('problems', 'Check before sending the rewritten branch', fixes([
        ['A normal push is rejected after rebase.', 'Did you already send the old commits to that branch?', 'If yes, read <a href="force-push.html">the force-push lesson</a> and agree with anyone using it. A local rebase has not changed GitHub yet.'],
        ['A change seems missing.', 'Compare with backup/feature-before-rebase and the correct range-diff ranges.', 'Keep both versions while you inspect. A change may already be in the base, or a conflict decision may have dropped it.'],
        ['The same file conflicts again.', 'Use <code>git rebase --show-current-patch</code>.', 'You may be on a later commit. Resolve that commit’s change; do not skip it merely to finish.']
      ]) + source(('Rebase', 'https://git-scm.com/docs/git-rebase'), ('Compare old and new changes', 'https://git-scm.com/docs/git-range-diff')))
    ], ['Rebase applies selected changes again and usually makes new commit IDs.', 'Only the branch being rebased moves; main stays at its starting position.', 'Keep the old branch, check each conflict, compare the result, and agree before replacing shared history.'], 'rebase')

    lesson('force-push', 'When push is refused, and what force changes', 40,
      'Understand why Git refuses to replace shared commits. Learn the expected-ID check used by force-with-lease and what to do when it fails.',
      ['Explain what a force push replaces on the server.', 'Read the difference between a normal push and a lease.', 'Keep a teammate’s work when the remote changes.'], [
      section('effect', 'A push asks to move a branch name',
        '<p>A normal push can move the server branch forward when its current commit is included in your new history. If the proposed history leaves out that current commit, Git normally refuses. This helps protect work already shared.</p>' +
        compare(graph('Server: A─B─C─T ← feature\nYours:  A─B─C′  ← feature', 'You changed C into C′. Your teammate added T after C.'), 'Force asks the server to use your new position', graph('Server: A─B─C′ ← feature\nOld C─T are outside this branch’s history.', 'T is no longer included through feature. Other copies may still have it.')) +
        '<p>A <b>force push</b> asks the server to accept this replacement. It changes the server branch position. It does not immediately replace every teammate’s files or erase every old copy. GitHub permissions and branch rules can still block it.</p>'),
      section('compare', 'What each push checks', table(['Command choice', 'Check before accepting', 'What can still go wrong?'], [
        ['Normal push', 'The current server commit must normally be part of the proposed history.', 'You can still send the wrong file or use the wrong branch.'],
        ['<code>--force</code>', 'Asks to skip that history check. Server rules still apply.', 'A teammate’s work can fall out of the branch history.'],
        ['<code>--force-with-lease</code>', 'By default, server position must match your local last-known position.', 'An editor may fetch in the background and update that position before you read the new work.'],
        ['<code>--force-with-lease=refs/heads/feature:EXPECTED</code>', 'Server feature must still be exactly the commit ID you recorded as EXPECTED.', 'The check detects a changed server position. It does not check whether your replacement keeps all useful work.']
      ]) + '<p><b>Lease</b> here means “only replace the branch if it is still where I expect.” <code>refs/heads/feature</code> is the full Git name for the server branch feature. Never add <code>--force</code> to a lease command; force disables that protection.</p>'),
      section('race', 'Why the expected ID matters',
        walk('Your expected position is C', [
          ('You record C before a rewrite', 'You inspect the server work and agree to replace C. You keep the full ID as your expectation.', filebox('Positions', 'Expected: C\nServer: C\nYour replacement: C′')),
          ('A teammate sends T', 'The server moves to T. Your saved expectation stays C, even if another tool fetches T.', filebox('Positions', 'Expected: C\nServer: T\nYour replacement: C′')),
          ('Your explicit lease is rejected', 'The server sees T instead of C. It leaves T in place. Fetch and read the new work before deciding what should happen next.', filebox('Result', 'No replacement accepted.\nTeammate’s T remains on feature.'))
        ]) + ask('If I change EXPECTED to T, have I kept T’s changes?', 'No. You have only changed the value the server checks. Read and keep the teammate’s needed work before agreeing to replace T.')),
      section('sequence', 'An agreed rewrite, with checks between actions',
        '<p>Use this only on a branch whose users have agreed to rewrite it. Shared main and release branches usually need new corrective commits instead. These steps assume a real local feature and origin/feature, and a clean working tree.</p>' +
        steps([
          ('Fetch and inspect both sides', 'Read all server-only changes before rewriting.', 'git status\ngit fetch origin\ngit switch feature\ngit log --left-right --graph --oneline feature...origin/feature', 'You can explain which changes are local and which are on the server. Stop if any teammate work is not understood.'),
          ('Record and keep both old positions', '<code>expected</code> is a shell variable holding the full server commit ID seen in your fetch. Choose unused backup branch names.', 'expected=$(git rev-parse refs/remotes/origin/feature)\ngit branch backup/local-feature\ngit branch backup/server-feature "$expected"', 'Your local and server starting commits have backup names. Uncommitted files are not saved by these names.'),
          ('Make only the agreed change to history', 'For example, rebase feature onto a fetched main when that is the agreed task.', 'git rebase origin/main', 'Check the old/new change lists, final files, and tests. Resolve any paused steps before continuing.'),
          ('Send to the exact branch with the saved expectation', 'Read the destination. HEAD means your current commit; the part after the colon names the server branch to update.', 'git push --force-with-lease=refs/heads/feature:"$expected" origin HEAD:refs/heads/feature', 'The server accepts only if its feature branch still equals expected and access/rules allow the update. If it rejects, inspect the reason.')
        ])),
      section('rejection', 'When the lease is rejected',
        '<p>Stop and fetch. Read the new commits and agree how to keep both sets of useful work. Do not simply fetch, update expected, and send the same replacement again. That can remove the very work the rejection protected.</p>' +
        '<p>After an agreed rewrite, teammates should keep their old local position under a backup branch before moving only their own unpublished changes onto the new history. A broad merge of the old history can bring the replaced commits back. Choose the range carefully; the rebase and cherry-pick lessons explain the options.</p>'),
      section('recovery', 'If the wrong branch was already replaced',
        '<p>Pause more pushes on that branch and tell the people using it. Find the old commit in a backup branch, a teammate’s copy, or a local reflog. Inspect it and create a rescue branch before doing more changes. Compare it with the current server history so recovery does not remove new work added after the mistake.</p>' +
        '<p>A reflog is a local record of branch movements; it is not a lasting server backup. If the purpose was to remove a leaked token, disable that token first. A force push cannot remove it from every other copy.</p>' +
        '<p>Try the <a href="playground.html#push-lab">push picture exercise</a> and <a href="practice.html#lease">Alice and Bob’s local lab</a>.</p>' + source(('Git push and leases', 'https://git-scm.com/docs/git-push')))
    ], ['A force push replaces a server branch position; it can leave out shared work.', 'An explicit lease checks the exact server commit ID you chose.', 'A rejected lease means inspect new work before changing the expectation.'], 'force-push')

    lesson('undo-recovery', 'Undo a mistake and find saved work', 40,
      'Choose an undo command by what you want to keep. Learn how files, staging, commits, and shared history change in each case.',
      ['Undo staging without throwing away the edited file.', 'Undo a shared change with a new correction.', 'Find a lost commit and keep it under a rescue branch.'], [
      section('choose', 'First say what went wrong',
        '<p>“Undo” can mean several different things. Did you choose the wrong file for the next commit? Edit the wrong line? Save the wrong commit? Send it to others? Read <code>git status</code>, <code>git diff</code>, and <code>git diff --staged</code> first.</p>' +
        table(['What you need', 'Command', 'What changes'], [
          ['Remove a tracked file’s changes from the next commit, keep your edits.', '<code>git restore --staged -- notes.txt</code>', 'Staging returns to the current saved version. Your file stays edited.'],
          ['Throw away unstaged edits to a tracked file.', '<code>git restore -- notes.txt</code>', 'Your file is replaced by the staged version. Save any wanted edits elsewhere first.'],
          ['Undo a commit already shared with others.', '<code>git revert COMMIT</code>', 'Adds a new commit that reverses the selected change. Replace COMMIT with the checked ID.'],
          ['Change the last private commit.', '<code>git commit --amend</code>', 'Makes a replacement commit from staging and lets you edit its message. The ID changes.'],
          ['Move a private branch back but keep all chosen content and files.', '<code>git reset --soft TARGET</code>', 'Moves the branch. Staging and files stay. TARGET is the checked destination commit.'],
          ['Move a private branch back, keep files, remove changes from staging.', '<code>git reset --mixed TARGET</code>', 'Moves the branch and resets staging. Files stay.'],
          ['Make the branch and tracked files match a target.', '<code>git reset --hard TARGET</code>', 'Moves the branch, replaces staging and tracked files. It can discard edits and remove untracked files in the way.']
        ])),
      section('picture', 'Unstage and discard are different',
        walk('Start with three different contents', [
          ('Before: Hi is chosen, Good morning is in your file', 'Your current saved commit still contains Hello.', three('Good morning', 'Hi', 'Hello')),
          ('Unstage: git restore --staged -- notes.txt', 'The next commit no longer contains the change to Hi. Your file still contains Good morning.', three('Good morning', 'Hello', 'Hello')),
          ('If you now run git restore -- notes.txt', 'Your file is overwritten from staging, which now contains Hello. The uncommitted Good morning text is lost from this file.', three('Hello', 'Hello', 'Hello'))
        ]) + '<p>The last step is shown so you understand the effect. Do it only when you want to discard that edit. A backup branch keeps commits; it cannot keep text that was never committed.</p>'),
      section('revert', 'Undo shared work by adding a correction',
        compare(graph('A─B─C─D ← main', 'C made a bad change. D added useful separate work.'), 'git revert C', graph('A─B─C─D─R ← main', 'R reverses C’s change. C and D stay in history.')) +
        '<p>In a real command, replace C with its actual ID. Inspect it with <code>git show COMMIT</code> first. A revert can conflict if later work changed the same lines. Resolve, add, test, and use <code>git revert --continue</code>, or stop with <code>git revert --abort</code>.</p>' +
        '<p>Revert changes files in Git. It does not undo a database change, recall an email, or disable a leaked password. Handle those systems separately.</p>' +
        '<details class="reveal"><summary>More detail: undoing a merge commit</summary><p>A merge has two parents. <code>git show --no-patch --pretty=raw MERGE</code> lists them. <code>git revert -m 1 MERGE</code> means keep parent 1 as the main line and reverse the merge’s change relative to it. Check the parent choice first. The old merge links still exist, so merging the same old branch again may not bring back the reverted effect. A reviewed new fix or a revert of the revert may be needed.</p></details>'),
      section('reflog', 'Find a commit after a branch moved away',
        '<p><b>Reflog</b> is Git’s local list of movements: “main moved here after commit,” “HEAD moved there after reset.” It can help find committed work that a branch no longer points to.</p>' +
        steps([
          ('Read the movement list', 'Look for the time and message before your mistake.', 'git reflog --date=iso', 'A list of local events and commit IDs.'),
          ('Inspect the candidate', 'Replace OLD_TIP with the ID from the event you found.', 'git show OLD_TIP', 'The wanted files and changes are in this commit. Do not guess based only on its position in the list.'),
          ('Give it a name before doing more recovery', 'Choose an unused rescue name. This does not move main or overwrite files.', 'git branch rescue/my-work OLD_TIP', 'The saved work is reachable through rescue/my-work.'),
          ('Choose how to use the rescued work', 'Compare it with the current project. You may need one file, one commit, or the whole branch.', 'git log --graph --oneline --all', 'You have both versions available while deciding. Test after bringing back the wanted change.')
        ]) + '<p>Reflogs stay on the computer where the movements happened, can expire, and are not downloaded by a new clone. Git may eventually remove stored commits that no branch or retained record reaches. A file never added or committed is not something reflog can reliably recover. Check editor history or backups for that case.</p>'),
      section('stash', 'Put unfinished edits aside for a short time',
        '<p>A <b>stash</b> is a temporary saved set of edits. It can help when you need to switch tasks before making a commit. First inspect what you are saving.</p>' +
        steps([
          ('Save tracked and new files temporarily', '<code>-u</code> includes untracked files. Ignored files are still left out.', 'git stash push -u -m "Notes before urgent fix"', 'The chosen edits move into a stash entry. Read status to see what remains.'),
          ('Find and inspect the entry', 'Number 0 is the newest entry. Its position can change when you make more stashes.', "git stash list\ngit stash show -p 'stash@{0}'", 'You can read the saved change before applying it.'),
          ('Apply and keep the saved entry', 'Use apply so the saved entry remains while you check the result.', "git stash apply 'stash@{0}'", 'The edits return, or Git reports conflicts. Check and test before deciding to drop the entry.')
        ]) + '<p><code>git stash pop</code> applies and removes an entry only after a successful application; it normally keeps the entry on conflicts. There is no <code>git stash --abort</code>. Preserve any edits that existed before applying it before undoing the attempt. <code>git stash branch rescue/wip \'stash@{0}\'</code> can apply the edits around their original starting commit and removes that entry on success. Inspect carefully.</p>' +
        '<p><code>-a</code> also saves ignored files, which may include large local data. For work you want to keep longer, prefer a branch with commits.</p>'),
      section('guard', 'Before deleting or replacing content',
        '<p><code>git clean -nd</code> previews untracked files and folders that a clean could remove. It does not remove them. <code>-x</code> includes ignored files too, such as a local database or environment. Read every path before any actual deletion.</p>' +
        '<p>Reset used with a path is different from reset used with a target commit: <code>git reset HEAD -- notes.txt</code> changes staging for that path and does not move the branch. Use the clearer restore --staged form while learning.</p>' +
        '<p>Try <a href="practice.html#reflog">recovery lab 7</a>, <a href="practice.html#stash">stash lab 8</a>, and <a href="practice.html#revert">revert lab 12</a>.</p>' + source(('Restore', 'https://git-scm.com/docs/git-restore'), ('Reset', 'https://git-scm.com/docs/git-reset'), ('Revert', 'https://git-scm.com/docs/git-revert'), ('Reflog', 'https://git-scm.com/docs/git-reflog'), ('Stash', 'https://git-scm.com/docs/git-stash')))
    ], ['Unstage keeps your file edits; restore without --staged can replace them.', 'Revert adds a correction to shared history. Reset can move a branch and replace files.', 'Find a lost commit, inspect it, and create a rescue branch before more changes.'], 'undo-recovery')

    lesson('history', 'Find what changed and why something broke', 40,
      'Read saved changes, search a file’s history, and use a repeatable test to find when a bug first appeared.',
      ['Choose log, show, and diff for a specific question.', 'Read two-dot and three-dot comparisons.', 'Find a first bad commit with bisect and check the result.'], [
      section('graph', 'Ask one question at a time',
        words([('Log', 'A list of saved commits. With --graph, lines show which commits follow which.'), ('Show', 'Read a particular saved commit or file without replacing your current file.'), ('Regression', 'Something that worked before but fails now. You need a test that can tell the two results apart.')]) +
        steps([
          ('See a small history picture', '<code>--oneline</code> gives a short ID and message. <code>--decorate</code> shows names such as main. <code>--all</code> includes histories reached by local branch and other saved names.', 'git log --graph --oneline --decorate --all -20', 'Up to 20 commits with their links. Fetch first if you need current remote history.'),
          ('Read one change', 'Replace COMMIT with an ID from log.', 'git show COMMIT', 'The commit message and the added/removed lines.'),
          ('Read an old file without switching branches', 'Use a real file path in place of notes.txt if needed.', 'git show COMMIT:notes.txt', 'The file’s contents in that saved commit. Your current file is not changed.'),
          ('Search the history of a file', '<code>--follow</code> tries to follow earlier names of this one file.', 'git log --follow -- notes.txt', 'Commits that affected the file, including detected renames.')
        ]) + '<p>Commit links are more useful than sorting only by time. A commit can record an original author time and a later time when it was applied. <code>git log --first-parent --oneline main</code> follows the first parent at merges, useful for seeing how changes entered main.</p>'),
      section('ranges', 'Two dots and three dots: read them with the command',
        graph('    C ← main\n   /\nA─B\n   \\\n    D─E ← feature', 'B is the shared starting commit. Main has C; feature has D and E.') +
        table(['Command', 'Meaning here', 'Result'], [
          ['<code>git log main..feature</code>', 'Commits in feature’s history but not main’s history.', 'D and E.'],
          ['<code>git log main...feature</code>', 'Commits on either side but not in both histories.', 'C, D, and E.'],
          ['<code>git diff main..feature</code>', 'Compare the files at the two named commits.', 'C’s files → E’s files. Same as git diff main feature.'],
          ['<code>git diff main...feature</code>', 'Compare the shared starting files with feature’s files.', 'B’s files → E’s files. This shows feature’s changes since the split.']
        ]) + ask('Does git diff feature...main show the same change in reverse?', 'No. It compares the base B to main C. The branch after the three dots decides the ending version.')),
      section('search', 'Find the reason behind a line',
        code("git blame -L 1,10 -- notes.txt\ngit log -S 'timeout' -- config.json\ngit log -G 'timeout.*' -- config.json", 'Use files and line numbers that exist in your project') +
        '<p><b>Blame</b> is the Git command name for showing the commit that last changed each selected line. Use it to find the commit and read its reason. Formatting and moved lines can affect the result; it is not a measure of who caused a bug. <code>-w</code> can ignore whitespace when calculating blame.</p>' +
        '<p><code>-S</code> finds commits where the number of occurrences of a text changed. <code>-G</code> searches added and removed lines for a pattern. The pattern above means timeout followed by any text. Both need you to inspect the matching commits.</p>'),
      section('bisect', 'Let Git narrow down the first bad commit',
        '<p><b>Bisect</b> tests a commit near the middle of a known good-to-bad range, then keeps narrowing the range based on your answer. Start with a clean working tree because it changes the checked-out files.</p>' +
        walk('A test passes before C and fails from C onward', [
          ('Choose known results', 'A works and E fails. Keep the same test and setup when checking older commits.', graph('A ✓ ─ B ? ─ C ? ─ D ? ─ E ✕', 'The question marks need a test.')),
          ('Test a middle commit', 'Git chooses C. The test fails. Tell Git “bad.” The first failure is now between A and C.', graph('A ✓ ─ B ? ─ C ✕     D     E', 'The search range becomes smaller.')),
          ('Test B and inspect C', 'B passes, so C is the first bad commit in this example. Reproduce both B and C and read C’s change.', graph('A ✓ ─ B ✓ ─ C ✕', 'The test result and the patch should explain the failure.'))
        ]) +
        code('git bisect start\ngit bisect bad BAD_COMMIT\ngit bisect good GOOD_COMMIT', 'Replace the two placeholders with tested commit IDs') +
        '<p>Run your test at the revision Git selects. Say <code>git bisect good</code> if the behavior works, <code>git bisect bad</code> if this bug occurs, or <code>git bisect skip</code> if you cannot test that revision. Repeat until Git reports the first bad commit. Save the report with <code>git bisect log</code>. Finish with <code>git bisect reset</code> to return to your original branch.</p>' +
        '<p>For a reliable test script, <code>git bisect run ./test-regression.sh</code> automates the answers. Exit 0 means good, exit 125 means cannot test, and normal nonzero failures mean bad. Special error codes are described in the manual. A missing dependency is not proof this product bug happened.</p>'),
      section('rewrite', 'Compare changes after a rebase',
        '<p><code>git range-diff OLD_BASE..old-tip NEW_BASE..new-tip</code> compares two lists of commit changes. Replace the four names with checked starting points and endings. It helps spot a dropped change or a changed conflict resolution. Matching patches do not prove identical behavior; the new surrounding code matters too.</p>'),
      section('problems', 'When the history does not answer the question', fixes([
        ['Expected old commits are missing.', 'Run <code>git rev-parse --is-shallow-repository</code> and check which branches were fetched.', 'A shallow copy has limited earlier history. Fetch more depth or the missing branches before comparing.'],
        ['Bisect points to an unlikely commit.', 'Test that commit and its parent with the same setup. Read <code>git bisect log</code>.', 'Fix unreliable tests or mark untestable revisions as skip before repeating.'],
        ['A date suggests the wrong order.', 'Read the parent links in the graph.', 'Use the saved history links and actual changes to explain the result.']
      ]) + '<p>Try <a href="practice.html#bisect">the real bisect lab</a>.</p>' + source(('Log', 'https://git-scm.com/docs/git-log'), ('Diff', 'https://git-scm.com/docs/git-diff'), ('Blame', 'https://git-scm.com/docs/git-blame'), ('Bisect', 'https://git-scm.com/docs/git-bisect')))
    ], ['Ask a specific question, then choose the history command.', 'Log chooses commits; diff compares file versions. Dot notation depends on which command you use.', 'Bisect needs a reliable test, known starting results, and a final check of the reported commit.'], 'history')

    lesson('collaboration', 'Ask a teammate to review your change', 30,
      'Follow a change from your branch to a GitHub pull request, review, checks, and merge. Learn what each step proves.',
      ['Open a pull request with the correct two branches.', 'Update it after feedback and read test results.', 'Explain the merge choices shown by GitHub.'], [
      section('workflow', 'What is a pull request?',
        '<p>A <b>pull request</b>, often shortened to PR, is a page asking to put one branch’s changes into another branch. It shows the changed files, discussion, and test results. Opening it does not put the changes into main.</p>' +
        words([('Base branch', 'The branch you want to receive the changes, often main.'), ('Head branch', 'The branch holding the proposed changes, such as add-title. This GitHub label is different from the all-capitals Git name HEAD.'), ('Review', 'A person reads the change and may approve it or ask for fixes.'), ('Check', 'A reported result from an automated job, such as tests. A passing check only covers what that job actually tested.')]) +
        flow([('Branch', 'Make and save a change'), ('Push', 'Send the branch'), ('Pull request', 'Ask to combine it'), ('Review and checks', 'Read, test, fix'), ('Merge', 'Put it into the base') ])),
      section('open-pr', 'Open and finish a small pull request',
        steps([
          ('Send your idea branch', 'Use the add-title branch from the sharing lesson. Check its saved changes first.', 'git switch add-title\ngit push -u origin add-title', 'GitHub now has that branch.'),
          ('Choose the correct branches on GitHub', 'Open Pull requests → New pull request. Set base to main and compare/head to add-title.', '', 'Files changed shows just the title change you meant to propose.'),
          ('Explain the change', 'Use a clear title such as “Add a title to the notes.” In the description, say what was wrong, what changed, and how you checked it. Use Draft if it is still unfinished.', '', 'A reviewer can understand the change without reading your private chat.'),
          ('Read feedback and checks', 'Open the Files changed and Checks views. If a test fails, open that job and read the first useful error. Confirm it ran for your latest commit.', '', 'You know what needs fixing and what already passed.'),
          ('Make follow-up commits on the same branch', 'Edit, test, add, commit, and push. The existing PR updates automatically.', 'git push origin add-title', 'The new commit appears in the same PR. Rules may ask for fresh approval.'),
          ('Merge when the required work is complete', 'Use the method your team chose. Review approvals, required checks, and unresolved concerns before merging.', '', 'The PR says Merged. Main contains the accepted result.'),
          ('Update your local main', 'Start with saved work. Fetch the accepted result and move your clean main forward.', 'git fetch origin\ngit switch main\ngit merge --ff-only origin/main', 'Your local main contains the change. Start the next task from a fresh branch here.')
        ])),
      section('review', 'What happens to history when you merge?',
        compare(filebox('Before', 'main:    A─B\nfeature: A─B─C─D'), 'Choose the team’s merge method', filebox('After', 'Merge:  keep C and D with a merge link\nSquash: save one combined change S\nRebase: save new copies C′ and D′')) +
        table(['GitHub option', 'What main gets', 'What to watch'], [
          ['Create a merge commit', 'The branch commits and a commit linking both histories.', 'This needs a rule that allows merge commits.'],
          ['Squash and merge', 'One commit containing the combined changes.', 'The old feature commits are not parents of the squash commit.'],
          ['Rebase and merge', 'New copies of the branch commits in a single line.', 'GitHub makes new commit IDs and updates committer information.']
        ]) + '<p>After squash or rebase merge, start new work from updated main. Reusing the old branch can make the next PR show old commits or confusing comparisons.</p>' +
        ask('A reviewer approved, but a required test failed. Is review complete?', 'The human review and automated check are separate. Under a rule requiring that check, the failure must be fixed before a normal merge.')),
      section('fork', 'If you cannot push to the original project',
        '<p>A <b>fork</b> is your own GitHub copy of a project, where the project allows it. A clone is a local copy on your computer. Clone your fork, and keep origin pointing to it. Save the original project address under a name such as upstream.</p>' +
        code('git remote add upstream PARENT_REPOSITORY_URL\ngit fetch upstream\ngit switch -c my-fix upstream/main', 'Replace the URL with the original project address; use its actual default branch') +
        '<p>Make your commits, push my-fix to origin, then open a PR with the original project as base and your fork/my-fix as head. Proposing a PR does not give you permission to merge it.</p>'),
      section('ownership', 'How to make a review useful',
        '<p>Keep unrelated changes separate. Include screenshots for a visible change and test results for program changes. If you rewrote the PR branch, give reviewers a range-diff comparison so they can see what changed during the rewrite.</p>' +
        '<p>An <b>issue</b> tracks a task or problem. A <b>tag</b> names a saved version. A GitHub <b>release</b> adds notes and downloads around a tag. Merging, releasing, and deploying a running program are separate actions.</p>' +
        '<p>CODEOWNERS is a file telling GitHub which people or teams should review certain paths. Rules decide whether that approval is required. A <b>merge queue</b> tests several approved changes in the order they will enter main. Its workflows may need the <code>merge_group</code> event to report the required results.</p>'),
      section('problems', 'If the PR is blocked', fixes([
        ['Unexpected files appear.', 'Check base and head, then inspect the commits.', 'Correct the branch choice or separate unrelated work before asking for review.'],
        ['New push removed an approval.', 'Read the current review rule.', 'Ask an eligible reviewer to read the new changes. Explain what changed.'],
        ['PR says there are conflicts.', 'Fetch the current base and inspect the branches.', 'Use the team’s merge or rebase method, resolve, test, and push the result.'],
        ['Green check, but merge still blocked.', 'Read every requirement shown by GitHub.', 'A missing review, unresolved thread, old check, or branch rule may still need work.']
      ]) + source(('Create a PR', 'https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request'), ('GitHub merge methods', 'https://docs.github.com/en/pull-requests/reference/pull-request-merges')))
    ], ['A PR asks to combine a head branch into a base branch.', 'A push, an approval, a passing check, a merge, and a deployment are separate steps.', 'After merging, update main and start the next task on a fresh branch.'], 'collaboration')

    lesson('github-permissions', 'Who can read, push, and change settings?', 35,
      'Understand account access and tokens through a failed-push example. Check the missing permission without giving everyone admin access.',
      ['Tell account identity, project access, token access, and rules apart.', 'Choose the access a person or job actually needs.', 'Find why the website works while terminal Git fails.'], [
      section('layers', 'Why “I can open the page” is not enough',
        '<p>You can read a public project without being allowed to push changes to it. You may also be signed into one account in your browser and using another account’s key in your terminal.</p>' +
        words([('Authentication = proving who you are', 'A sign-in, SSH key, or token tells GitHub which person or app made the request.'), ('Authorization = deciding what you may do', 'GitHub checks whether that account or app can read, push, merge, or change settings.'), ('Token = a key with limits', 'A personal access token is a secret used instead of an account password for supported operations. It can allow only certain projects and actions. It cannot give its owner access they do not already have.')]) +
        flow([('Who are you?', 'Account, app, or key'), ('Can you use this project?', 'Project access'), ('Does this key allow the action?', 'Token permissions'), ('Do rules allow it now?', 'Review, tests, branch rules')]) +
        '<p>Organizations may add sign-in approval, allowed-network rules, or token approval. A private project can appear as “not found” when your terminal account lacks access.</p>'),
      section('roles', 'Pick a role for the work',
        table(['Role in an organization project', 'Common use', 'Limit to remember'], [
          ['Read', 'Read code and join discussions.', 'No direct code pushes.'],
          ['Triage', 'Help sort issues and PRs.', 'Does not give code-push access.'],
          ['Write', 'Push changes and merge when rules allow.', 'Does not give full settings control or automatic rule bypass.'],
          ['Maintain', 'Do more project upkeep.', 'Some sensitive settings remain restricted.'],
          ['Admin', 'Manage access and sensitive settings.', 'Organization rules and branch rules can still apply.']
        ]) + '<p>These are organization repository roles. Personal projects use an owner/collaborator model. Some plans support custom roles. A person may receive access directly, through teams, or through organization defaults; removing one grant may leave another.</p>'),
      section('example', 'A token cannot replace missing project access',
        walk('Maya needs to send a code change', [
          ('Before: Maya has Read', 'Her token asks for Contents: write, but her account only has Read on this project. GitHub refuses the push.', filebox('Checks', 'Account access: Read → cannot push\nToken: Contents write → still cannot add account access')),
          ('Give the account the needed role', 'An authorized owner grants Write for this task. The token also needs this repository selected and Contents: write.', filebox('Checks', 'Account access: Write\nToken: correct repo + Contents write')),
          ('Follow the branch rule too', 'If main requires PRs, Maya still cannot push directly to main. She can push a feature branch and open a PR.', filebox('Result', 'Feature push: allowed if other policies pass\nDirect main push: blocked by required PR'))
        ])),
      section('credentials', 'Use the right kind of key', table(['Method', 'What it is for', 'What to inspect'], [
        ['HTTPS with a credential manager or GitHub CLI', 'A person working from a terminal.', 'The account it is signed in as and the project it can reach. Store credentials in the supported secure store.'],
        ['SSH key', 'Git access using a registered public key.', 'Which private key your SSH agent chooses; register only its public part. Organization sign-in approval may also be needed.'],
        ['Fine-grained personal token', 'A user token limited to selected projects and actions.', 'Owner, repository selection, permissions, expiry, and required organization approval. Check current support limits.'],
        ['Classic personal token', 'An older token type needed for some uses.', 'Its broader scopes and organization restrictions; keep access as small as possible.'],
        ['GitHub App token', 'An installed service doing project work.', 'Which projects the installation can use, its actions, and when the token expires.'],
        ['Deploy key', 'An SSH key for one repository.', 'Read-only or write-enabled. Anyone holding its private key may keep that access until the key is removed.'],
        ['GITHUB_TOKEN', 'A built-in key for an Actions job.', 'Job/workflow permissions and the event that started the run.']
      ]) + '<p>Never paste a token into a remote URL, source file, screenshot, or chat. If you expose it, revoke or replace it. Git commit name/email settings label commits; they do not sign you in.</p>'),
      section('grant', 'Check access in a clear order',
        steps([
          ('Check the address', 'Confirm the owner and project, without printing any token.', 'git remote -v', 'The intended address is listed without secrets.'),
          ('Check which account your terminal uses', 'For HTTPS, use your credential manager or <code>gh auth status</code> if GitHub CLI is installed. For SSH, <code>ssh -T git@github.com</code> reports the recognized account; a successful GitHub greeting may still return a nonzero shell status.', '', 'The account is the one that has the project access.'),
          ('Check the project grant and key limits', 'Ask the project owner to check the needed role. For a fine-grained token, check the correct owner, selected repository, Contents permission, expiry, and approval.', '', 'Both the account and the key allow the intended action.'),
          ('Read the exact branch-rule error', 'A GH006 or GH013 message may say a PR, signature, review, or check is needed.', '', 'Use the required route. Increasing token access does not remove branch requirements.'),
          ('Verify the intended action', 'Test in a permitted practice project or branch.', 'git ls-remote origin', 'A read succeeds. This proves read access only; a permitted feature-branch push separately checks write access.')
        ])),
      section('diagnose', 'Common access failures', fixes([
        ['Repository not found', 'Owner/project spelling and terminal account.', 'Correct the address or account/project selection, then try a read again.'],
        ['Permission denied (publickey)', 'Chosen SSH key, loaded agent keys, and public-key registration.', 'Use the intended registered key and complete organization approval where needed. Never print the private key.'],
        ['403 / resource not accessible', 'Token expiry, selected project, permission, approval, and organization policies.', 'Change only the missing access needed for the task, then retry that action.'],
        ['Cannot update .github/workflows', 'Ordinary content-write access plus workflow-file permission.', 'Use the appropriate Workflows permission or classic workflow scope, then satisfy review rules.'],
        ['Person left, but a job still has access', 'Other teams, direct grants, deploy keys, apps, and saved tokens.', 'Remove or replace the credentials that should no longer work, then verify the old access fails.']
      ]) + source(('Repository roles', 'https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization'), ('Personal access tokens', 'https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens')))
    ], ['Check who the terminal signs in as before changing permissions.', 'An account role, a token’s limits, and a branch rule all matter.', 'Give the access needed for the task, then test what should succeed and what should stay blocked.'], 'github-permissions')

    lesson('rules', 'Team rules that GitHub can check', 35,
      'Turn “review before merge” into a working rule. Check the target branches, required tests, and exceptions with a small practice change.',
      ['Write a clear rule before changing settings.', 'Understand a ruleset and who can use an exception.', 'Find why a rule blocks too much or fails to block a direct push.'], [
      section('policy', 'Start with a rule people understand',
        '<p>Example: “To change main, open a PR, get one other person’s approval, and pass the tests. Do not force-push or delete main.” A <b>ruleset</b> is a saved group of GitHub rules for selected branches or tags. A <b>bypass</b> is an explicitly allowed exception for selected people, teams, or apps.</p>' +
        compare(filebox('Before', 'Anyone with suitable write access may push\nunless an existing rule blocks it.'), 'Require a PR, approval, and tests', filebox('After', 'Direct main push: blocked\nReviewed PR + passing tests: can merge\nNamed exceptions: follow their allowed route')) +
        '<p>Write the agreement in CONTRIBUTING or your team guide. Include who handles urgent fixes and how those fixes are reviewed afterward. Local Git hooks are scripts that help check changes on a computer; they can be missing or skipped, so shared enforcement belongs on the server.</p>'),
      section('configure', 'Set up and test a branch ruleset',
        steps([
          ('Choose a safe project and check availability', 'You need Admin or the appropriate custom rule-management access. Available settings depend on plan, visibility, and organization policy.', '', 'You can see the applicable Rulesets settings.'),
          ('Create a branch ruleset', 'Open repository Settings and find Rulesets. Choose the branch-ruleset option; menu grouping can vary.', '', 'You can name the rule and select its target branches.'),
          ('Check the matching branches and mode', 'Select the actual default branch, such as main. Active means enforce. Disabled does not enforce. Evaluate, where available, reports what would happen without blocking.', '', 'The displayed matching branches and enforcement mode are the ones you meant.'),
          ('Set the requirements and exceptions', 'Require the agreed PR reviews and named checks. Block force pushes and deletion if that is the policy. Give exceptions only to the intended accounts or apps.', '', 'The saved rule describes the team agreement.'),
          ('Test a normal contributor’s direct push', 'Use a harmless practice branch covered by the test rule. Use an account that has no exception.', '', 'The direct update is refused with the expected rule message.'),
          ('Test the approved route', 'Open a small PR. Observe missing review and failing-check blocks, then obtain review and pass the actual required checks.', '', 'The PR becomes mergeable when the intended requirements pass.')
        ]) + '<p>More than one ruleset and older branch protection can apply. Read the combined effective rules: one permissive rule does not cancel a stricter one. Testing only as an admin or bypass account can hide a problem that normal contributors will face.</p>'),
      section('choices', 'Read the effect of each setting', table(['Setting', 'What it means', 'Common surprise'], [
        ['Require linear history', 'Keep a single-parent line on the target branch.', 'Merge commits are rejected. Allow a compatible squash or rebase merge method.'],
        ['Require up-to-date branch', 'Test with the current base before combining.', 'New main changes may require fresh tests. A merge queue can help busy projects.'],
        ['Dismiss stale approval / latest-push approval', 'New changes may need a new person’s review.', 'An earlier approval can disappear or no longer count.'],
        ['Required check', 'Wait for a named result from the expected source.', 'A misspelled job name or skipped event can leave it pending forever.'],
        ['Restrict updates', 'Only allowed exceptions can update matched branches.', 'This is stricter than simply requiring PRs and can block normal merges.'],
        ['Signed commits', 'Require acceptable commit signatures.', 'People and bots need signing setup, including how the chosen merge method signs new commits.'],
        ['Branch pattern', 'Choose which names the rule covers.', 'A single * does not match across / in the documented GitHub matching. Inspect the actual matches.']
      ])),
      section('owners', 'Ask the right people to review',
        '<p><b>CODEOWNERS</b> is a text file mapping paths to reviewers. Use real teams with the required repository access. For example:</p>' +
        code('* @example-org/maintainers\n/src/auth/ @example-org/security\n/.github/ @example-org/platform\n/.github/CODEOWNERS @example-org/maintainers', 'Example .github/CODEOWNERS — replace these team names') +
        '<p>GitHub reads this file from the PR’s base branch. The last matching pattern wins. The file requests review; the rule requiring code-owner approval makes that review a merge condition. The file does not grant access. Check errors and requested reviewers on an actual small PR.</p>'),
      section('verify', 'If the rule behaves differently', fixes([
        ['Direct push is allowed unexpectedly.', 'Matching branch, Active mode, inherited rules, and bypass list.', 'Correct the actual mismatch, then retry as a normal writer.'],
        ['A required check never appears.', 'Exact check name, workflow event, path/branch filters, and trusted source.', 'Make the job report on the revision being evaluated. For a merge queue, check <code>merge_group</code>.'],
        ['A correct PR cannot merge.', 'Conflicting history requirements, Restrict updates, missing approval, or another ruleset.', 'Read the named blocker and fix the inconsistent setting or unmet requirement.'],
        ['CODEOWNERS asks nobody.', 'File location on the base branch, matching path, team visibility/access, and syntax errors.', 'Fix the example and check the requested reviewers again.']
      ]) + '<p>Use the <a href="examples/team-policy.md">team rule worksheet</a> to record the choices. Opening the worksheet changes no GitHub settings.</p>' + source(('About rulesets', 'https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets'), ('Available rules', 'https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets'), ('CODEOWNERS', 'https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners')))
    ], ['A rule needs the correct branch targets, enforcement mode, and exceptions.', 'CODEOWNERS chooses reviewers; a separate rule requires their approval.', 'Test both a blocked direct update and a successful approved PR as a normal contributor.'], 'rules')

    lesson('security-automation', 'Passwords, job access, and signed commits', 35,
      'See what to do if a secret enters Git, how GitHub Actions gets access, and what a verified signature actually tells you.',
      ['Respond to an exposed password or token in the right order.', 'Limit what an automated job can read or write.', 'Tell a signature from a test result or code review.'], [
      section('secret', 'If you commit a password or token',
        '<p>A <b>secret</b> is a password, private key, or token that gives access to something. Removing it in the next commit leaves the old value in earlier commits and possibly in other copies.</p>' +
        flow([('Disable or replace it', 'Revoke or rotate the exposed key'), ('Check its use', 'Look for unexpected access'), ('Clean the copies', 'Follow the provider’s process'), ('Prevent a repeat', 'Use safe settings and scanning')]) +
        compare(filebox('Before', 'Commit A contains token X.\nCommit B deletes the text.\nToken X may still work.'), 'Revoke token X at its provider', filebox('After', 'Token X no longer grants access.\nOld text may still exist in copies.\nUse a new secret only in a safe store.')) +
        '<p>Revoke means disable the old credential. Rotate means replace it with a new one and stop using the old one. Do this first, then follow the service’s incident process. Removing old history with a tool such as git-filter-repo changes commit IDs and affects teammates. Coordinate all affected branches, tags, forks, clones, and cached views using the official cleanup guide. A force push cannot promise to erase every copy.</p>'),
      section('workflow', 'What is GitHub Actions?',
        '<p>GitHub Actions runs jobs described in a workflow file under <code>.github/workflows/</code>. A job can test code, build a file, or publish a release. <b>GITHUB_TOKEN</b> is a built-in credential supplied for the job. Its permissions decide which GitHub actions the job may perform.</p>' +
        code('permissions:\n  contents: read\n\njobs:\n  test:\n    runs-on: ubuntu-latest\n    permissions:\n      contents: read\n    # Add reviewed checkout and test steps here.', 'Part of a workflow — this example is not a complete runnable workflow') +
        '<p><code>contents: read</code> allows reading repository content; it does not allow ordinary content writes. Grant write access only to a job that needs it. When you explicitly list permissions, unspecified permissions are generally none, except the basic repository information GitHub always permits. Organization settings and the event can reduce the effective access further.</p>' +
        '<p>For cloud access, a short-lived login using OIDC can avoid a long-lived cloud key. OIDC lets the cloud provider check the identity of a particular job before issuing limited access. Configure the accepted project, branch, and job context carefully.</p>'),
      section('trust', 'A test job can run someone else’s code',
        '<p>A contribution from a fork may change a build command, package install script, or test. Running it means running the contributor’s code. Normal fork PR jobs usually have restricted tokens and no ordinary repository secrets, though settings can change exceptions.</p>' +
        '<p><code>pull_request_target</code> runs in the trusted base project’s context. Checking out the contributor’s code and running its build there can expose secrets or write access. Keep untrusted tests apart from jobs that can publish or change protected resources.</p>' +
        table(['Input or step', 'Careful handling'], [['Third-party action', 'Pin to a reviewed full commit ID and review updates. A moving version label can later point to different code.'], ['PR title, branch name, or issue text', 'Treat it as data. Do not paste it directly into a shell script. Pass it through a safely defined environment variable and quote the variable.'], ['Artifact from another job', 'Check where it came from before a privileged job uses it. An artifact is a saved output file; it can contain unsafe content too.'], ['Workflow changes', 'Require suitable review because these files decide what code runs with access.']])),
      section('signing', 'What does “Verified” mean?',
        '<p>A <b>signature</b> links the exact commit or tag to a signing key. Verification checks that link under the service’s rules. Author name and email fields alone do not prove who made a change.</p>' +
        table(['Evidence', 'What it tells you', 'What it does not prove'], [['Verified signature', 'The object matches an accepted signing key under the verifier’s rules.', 'That the program is correct or safe.'], ['Passing check', 'A particular job reported success for a revision.', 'That every possible test passed.'], ['Approval', 'A reviewer accepted the change they reviewed.', 'That all automated checks passed or that no later change needs review.']]) +
        code('git log --show-signature -1\ngit verify-commit COMMIT\ngit verify-tag TAG', 'Use a real signed commit/tag and a configured verifier') +
        '<p>Rebase or amend creates new objects. An old signature cannot verify a different replacement commit; sign replacements when needed. Account two-factor sign-in, SSH access keys, and signing keys serve different jobs.</p>'),
      section('problems', 'If a job or signature check fails', fixes([
        ['Job cannot write.', 'Job permission, repository defaults, event restrictions, and branch rules.', 'Grant only its required action where permitted, then rerun for the intended revision.'],
        ['A fork PR job has no secret.', 'Which event and trust context started it?', 'Do not expose secrets simply to make an untrusted build run. Use a restricted test path.'],
        ['Signature cannot be verified.', 'Correct object ID, public signing key, account association, and verification setup.', 'Repair signing setup and verify again. Continue to require review and tests.']
      ]) + source(('Remove sensitive data', 'https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository'), ('Job token', 'https://docs.github.com/en/actions/tutorials/authenticate-with-github_token'), ('Secure Actions use', 'https://docs.github.com/en/actions/reference/security/secure-use'), ('Signatures', 'https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification')))
    ], ['Disable an exposed secret first; deleting the latest text is not enough.', 'Give each job only the access it needs, and keep untrusted code away from powerful credentials.', 'A signature, passing test, and human approval are different kinds of evidence.'], 'security-automation')

    lesson('advanced', 'More tools for real project problems', 40,
      'Copy one fix, work in a second folder, reuse a conflict fix, and understand projects with large files or limited history.',
      ['Choose cherry-pick or worktree for a specific task.', 'Understand what rerere and merge side options keep.', 'Diagnose missing submodule files, LFS content, and older history.'], [
      section('cherry', 'Copy one fix to another branch',
        '<p><b>Cherry-pick</b> applies one commit’s change to your current branch. Example: main has a bug fix and a later new feature. An older release needs only the fix.</p>' +
        compare(filebox('Before', 'main:    A─B─F─N\nrelease: A─R\nF = fix; N = unrelated feature'), 'On release: cherry-pick the ID for F', filebox('After', 'release: A─R─F′\nThe fix is copied. N is not.')) +
        steps([
          ('Inspect the source change', 'Replace COMMIT with the fix’s checked ID. Check whether it needs other earlier changes.', 'git show COMMIT', 'Only the wanted fix is selected, and its dependencies are understood.'),
          ('Use the destination branch', 'Start with saved work.', 'git switch release/maintenance', 'Status names the intended release branch.'),
          ('Apply and record the source', '<code>-x</code> adds the original commit ID to the new commit message.', 'git cherry-pick -x COMMIT', 'A new commit usually has a new ID because it has a different parent. Run the release tests.')
        ]) + '<p>For a conflict, edit, add, check, then <code>git cherry-pick --continue</code>; stop with <code>git cherry-pick --abort</code>. Copying a merge commit requires choosing a parent with <code>-m</code> and careful review. Do not use repeated cherry-picks to replace a clear shared-branch merge policy.</p>'),
      section('worktree', 'Keep unfinished work while opening a second task',
        '<p>A <b>worktree</b> gives the same repository another working folder. Each folder has its own files, staging area, and HEAD; commit storage and branch names are shared. It is useful for an urgent fix while the first folder has unfinished edits.</p>' +
        code('git worktree add ../project-hotfix -b hotfix main\ngit worktree list', 'Create a new folder and a new branch named hotfix') +
        '<p>Your original folder and edits stay. Work in project-hotfix for the urgent change. Each folder may need its own installed dependencies. Git usually prevents the same branch from being checked out in both folders. When the second folder is clean and finished, use <code>git worktree remove ../project-hotfix</code>. Inspect it before removing.</p>'),
      section('rerere', 'Remember a conflict fix, then check it',
        '<p><b>Rerere</b> is Git’s name for remembering a conflict resolution and trying it again when the same conflict returns. Enable it for a practice project with <code>git config --local rerere.enabled true</code>. Use <code>git rerere status</code> and <code>git rerere diff</code> to inspect.</p>' +
        '<p>A remembered answer can be wrong in a new context. Read and test the result. <code>rerere.autoupdate</code> also changes whether the result is staged automatically, so check that setting before relying on it.</p>' +
        table(['Merge option', 'What it keeps'], [['<code>git merge -X ours feature</code>', 'Favors your side for conflicting parts, while still taking nonconflicting changes from feature.'], ['<code>git merge -s ours feature</code>', 'Records feature as merged in the history, but keeps your entire current project tree and ignores feature’s file contents.']]) +
        '<p>These are different operations. Neither one decides the correct application behavior for you.</p>'),
      section('scale', 'When a project does not contain the files you expect', table(['Feature', 'Simple meaning', 'If it causes a problem'], [
        ['Submodule', 'A project records a particular commit from another repository.', 'Read .gitmodules and <code>git submodule status</code>. Follow the project’s init/update steps and check access. The referenced commit must be available in that other repository.'],
        ['Git LFS', 'Git stores a small pointer file; a separate service stores the large file.', 'If an image is only pointer text, check LFS installation, download, access, and quota. Do not replace the pointer with guessed content.'],
        ['Shallow clone', 'Only some recent history was downloaded.', 'Check <code>git rev-parse --is-shallow-repository</code>. Fetch more history or unshallow when needed for old changes or merge bases.'],
        ['Partial clone', 'Some stored file content is downloaded only when needed.', 'An old-file read may need network access. Check the missing-object error and connection.'],
        ['Sparse checkout', 'Only selected tracked folders appear in your working folder.', 'A missing path may be outside that selection. It has not necessarily been deleted from Git.'],
        ['Attributes', 'A .gitattributes file controls handling of selected paths.', 'Check line endings and diff/merge handling before a large formatting or normalization change.']
      ]) +
        code('* text=auto\n*.sh text eol=lf\n*.png binary', 'Small .gitattributes example — adapt it to the project’s existing policy') +
        '<p>LF and CRLF are two line-ending forms used by different systems. Changing them can make every line appear changed. Keep a whole-project normalization separate from a functional change. Do not run <code>git add --renormalize .</code> without reviewing the intended policy and resulting changes.</p>' +
        '<p>A case-only rename may be missed on a file system that treats Notes.txt and notes.txt as the same name. Use an intermediate name with <code>git mv</code>, then the intended spelling, and check the staged result.</p>'),
      section('release', 'Give a release commit a stable name',
        '<p>A <b>tag</b> names a particular saved version. An annotated tag also has a message and creator information. Use the team’s chosen release commit and version.</p>' +
        code('git tag -a v1.2.0 -m "Release 1.2.0"\ngit show v1.2.0\ngit push origin v1.2.0', 'Example release steps — inspect the current commit before tagging') +
        '<p>A normal branch push does not send every tag. Push the intended tag explicitly. Avoid moving a published release tag because others may already have used its old value. GitHub Releases adds notes and downloadable files around a tag; check that any published build came from the intended commit.</p>'),
      section('problems', 'Match the tool to the problem', fixes([
        ['Branch is already checked out elsewhere.', 'Read <code>git worktree list</code>.', 'Use that folder or another branch. Do not force two active folders to update the same branch.'],
        ['Unrelated histories error.', 'Check remote addresses and each history’s first commit.', 'You may have joined the wrong projects. Use --allow-unrelated-histories only for an intended, reviewed combination of independent projects.'],
        ['Copied fix fails on the old release.', 'Check the fix’s earlier dependencies and release tests.', 'Include the required supporting change deliberately, or adapt the fix to the older code.']
      ]) + '<p>Try <a href="practice.html#cherry">lab 10</a> and <a href="practice.html#worktree">lab 11</a>.</p>' + source(('Cherry-pick', 'https://git-scm.com/docs/git-cherry-pick'), ('Worktree', 'https://git-scm.com/docs/git-worktree'), ('Rerere', 'https://git-scm.com/docs/git-rerere'), ('Attributes', 'https://git-scm.com/docs/gitattributes')))
    ], ['Cherry-pick copies a selected change; worktree opens another working folder.', 'A reused conflict fix still needs review and tests.', 'Missing files can come from submodules, LFS, or a limited checkout; read the specific error before changing history.'], 'advanced')
