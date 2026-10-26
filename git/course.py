"""Original Git/GitHub curriculum. Regenerate HTML with python3 git/build.py."""
from html import escape

def code(text, where="Shell example — read the context before running"):
    return '<div class="snippet"><div class="code-caption"><span>' + escape(where) + '</span></div><pre><code>' + escape(text.strip()) + '</code></pre></div>'

def table(headings, rows):
    return '<div class="table-wrap"><table><thead><tr>' + ''.join('<th scope="col">' + h + '</th>' for h in headings) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td class="wrap">' + c + '</td>' for c in row) + '</tr>' for row in rows) + '</tbody></table></div>'

def note(title, body, kind="tip"):
    return '<div class="callout ' + kind + '"><b class="callout-title">' + title + '</b><p>' + body + '</p></div>'

def flow(items):
    return '<div class="flow" role="group" aria-label="Process diagram">' + '<span aria-hidden="true">→</span>'.join('<div><b>' + a + '</b><small>' + b + '</small></div>' for a,b in items) + '</div>'

def graph(text, caption):
    return '<figure class="graph"><pre>' + escape(text.strip()) + '</pre><figcaption>' + caption + '</figcaption></figure>'

def source(*items):
    return '<p class="source-note">Read more: ' + ' · '.join('<a href="' + url + '">' + title + '</a>' for title,url in items) + '</p>'

def section(id, title, body):
    return '<section class="lesson-section" id="' + id + '"><h2>' + title + '</h2>' + body + '</section>'

LESSONS = []
def lesson(id, title, minutes, description, objectives, sections, recap, topic=None):
    LESSONS.append(dict(id=id,title=title,minutes=minutes,description=description,objectives=objectives,sections=sections,recap=recap,topic=topic))

lesson("index", "Git, explained one picture at a time.", 15,
 "Start with a school project and discover what Git does, why it matters, and how GitHub helps people work together. Build confidence with pictures, hands-on practice and short recall sessions.",
 ["Explain Git and GitHub in different terms.", "Choose a learning route and practise in disposable repositories.", "Know the questions to ask before changing shared history."], [
section("why", "Start with a familiar problem",
 """<p>You are making a school project. Yesterday it was correct; today you accidentally deleted a useful paragraph. A friend has a different copy. Which version should you keep, and how can you combine your work? Git helps you keep a clear history of recorded versions. Start with the illustrated beginner lesson, then build up to real development problems.</p>
 <p><strong>Git</strong> is a distributed version-control system. It keeps a history of project versions you deliberately record on your computer. <strong>GitHub</strong> hosts repositories and adds pull requests, code review, issues, permissions, rules, automation and collaboration. A local commit is not automatically uploaded, reviewed, approved or deployed.</p>""" +
 flow([("Edit", "Make a useful change"),("Select", "Choose what you want to record"),("Record", "Save a project snapshot"),("Share", "Send it to a remote repository"),("Review", "Compare and discuss the change")]) +
 note("The five questions", "Which repository and branch am I on? Is the work committed or uncommitted? Is this history already shared? Which local or remote reference will move? What evidence and recovery point do I have?")),
section("routes", "Choose your route",
 """<div class="stat-grid"><div class="stat"><strong>23</strong><span>learning modules</span></div><div class="stat"><strong>60</strong><span>explained quiz questions</span></div><div class="stat"><strong>12</strong><span>real Git labs</span></div><div class="stat"><strong>30</strong><span>troubleshooting cases</span></div></div>""" +
 table(["Need", "Route"],[
 ["New to Git", '<a href="why-git.html">What is Git? A school-project story</a> → foundations → daily workflow → branches → merge → conflicts.'],
 ["Rebase or rejected push today", '<a href="rebase.html">Rebase</a> → <a href="force-push.html">force push and leases</a> → <a href="undo-recovery.html">recovery</a>.'],
 ["Investigate a regression", '<a href="history.html">History, blame and bisect</a>, then the disposable incident lab.'],
 ["Set team standards", '<a href="collaboration.html">Pull requests</a> → <a href="github-permissions.html">permissions</a> → <a href="rules.html">repository rules</a>.'],
 ["Learn visually", '<a href="studio.html">Play the five-station Practice Studio</a>, then <a href="playground.html">Step through the graph, resolve a conflict and simulate push/permission decisions</a>.'],
 ["Refresh quickly", '<a href="recap.html">Recall cards</a> and the <a href="reference.html">searchable reference</a>.']]) +
 """<p>Plan several short study sessions. Read, predict, inspect a real repository, then explain the result. The first pass takes roughly 12–16 hours with practice; deeper team exercises take longer. Every module ends with a concise recap.</p><div class="actions"><a class="btn btn-primary" href="why-git.html">Start with the school-project story →</a><a class="btn" href="studio.html">Try the Practice Studio →</a><a class="btn" href="playground.html">Open visual lab</a></div>"""),
section("scope", "How to use these documents",
 """<p>Core commands use modern Git, including <code>switch</code> and <code>restore</code> (Git 2.23+). Labs also use <code>git init -b</code> (2.28+). Check <code>git --version</code> and the installed manual. GitHub capabilities depend on repository visibility, plan, organization policy and GitHub Enterprise version. Official sources are linked near the relevant explanations and collected in the reference.</p>
 <p>The browser exercises are simulations: they do not access or modify any repository. The real labs use newly created local repositories and local bare remotes, so no GitHub account or access token is needed. Do not run a destructive practice command in a work repository.</p>
 <p>Command placeholders such as <code>COMMIT</code>, <code>OLD_BASE</code> and <code>feature</code> must be replaced with inspected values in your real project. Examples use POSIX shell syntax; use Git Bash or WSL on Windows for those snippets. There are no real credentials in these documents.</p>
 <p>This is a complete practical learning path, not a claim to list every Git plumbing flag or every GitHub product. Advanced topics point to their primary manuals. Learning progress is local to this browser and can be exported on the recap page.</p>"""),
section("curriculum", "The full learning path", '<div class="cards" data-course-cards></div>')
], ["Git records snapshots and ancestry; GitHub adds collaboration and policy.", "Inspect state and shared ownership before changing history.", "Practise risky operations only in a disposable repository."])

from beginner_content import add_beginner
add_beginner(lesson, section, table, note)

lesson("foundations", "Snapshots, the index, HEAD & objects", 25,
 "Understand what Git stores, what a branch actually is, and why staged and unstaged changes are different.",
 ["Distinguish the working tree, index and commits.", "Explain commit IDs, parents, branches, tags and HEAD.", "Configure identity without confusing it with authentication."], [
section("first-repository", "Start with a clone or a new local repository",
 """<p>For an existing project, copy its approved HTTPS or SSH clone URL from GitHub’s <strong>Code</strong> menu. Replace <code>APPROVED_REPOSITORY_URL</code> below; never insert a token into the URL. Cloning creates a local repository, downloads available history, configures a remote normally named origin, and checks out a branch. It does not copy another developer’s uncommitted files.</p>""" +
 code("git clone APPROVED_REPOSITORY_URL project\ncd project\ngit status\ngit remote -v", "Existing project — choose an unused destination directory") +
 """<p>For a genuinely new project, start in a fresh directory instead. <code>git init</code> creates local Git metadata; it neither creates a GitHub repository nor uploads files. Keep the two starting routes separate.</p>""" +
 code("mkdir my-first-git-project\ncd my-first-git-project\ngit init -b main\n# Set repository-local identity if needed:\ngit config user.name 'Your Name'\ngit config user.email 'your-approved-address@example.com'\nprintf 'A small first project.\\n' > README.md\ngit add -- README.md\ngit diff --staged\ngit commit -m 'Describe the project'\ngit log --oneline", "New local project — use a fresh directory") +
 """<p>To publish that new repository, first create the intended empty GitHub repository with the correct owner and visibility. If you already created its files locally, avoid independently initializing a second README/history on GitHub. Add the inspected remote with <code>git remote add origin APPROVED_REPOSITORY_URL</code>, verify <code>git remote -v</code>, then <code>git push -u origin main</code> when its access and rules permit. For a repository that already has history, clone and integrate that history instead of reflexively forcing an unrelated branch over it.</p>
 <p>The hidden <code>.git</code> directory contains the ordinary repository’s metadata and objects. Do not delete or edit it to “fix” a confusing status. Git does not track empty directories, and a newly created file is untracked until you add it.</p>""" +
 source(("Clone","https://git-scm.com/docs/git-clone"),("Initialize","https://git-scm.com/docs/git-init"))),
section("areas", "Three places where your content can exist",
 flow([("Working tree", "Files currently on disk"),("Index / staging area", "The snapshot prepared for the next commit"),("Local history", "Commits stored in the object database")]) +
 """<p>Editing changes your working tree. <code>git add</code> records the selected content in the index. <code>git commit</code> creates a commit from the index. If you edit a file again after staging it, the staged version and the current file can differ. A clean working tree means it matches the index and current commit for tracked paths; it does not mean every file on disk is tracked.</p>""" +
 code("git status --short\ngit diff\ngit diff --staged\ngit ls-files") +
 table(["Observation", "Meaning"],[
 ["<code>git diff</code>", "Working tree compared with index: unstaged changes."],
 ["<code>git diff --staged</code>", "Index compared with HEAD: what the next ordinary commit would include."],
 ["<code>git diff HEAD</code>", "Working-tree tracked content compared with the current commit; does not include untracked file contents."],
 ["<code>?? file</code>", "Untracked file; it is not in a commit merely because it exists in the directory."],
 ["<code>MM file</code>", "The file has both staged changes and additional unstaged changes."]])),
section("objects", "A commit is a snapshot with history",
 """<p>A blob stores file content, a tree maps names to blobs or other trees, and a commit points to a tree plus its parent commit(s), author/committer metadata and message. Git identifies objects by a content-derived object ID. Reusing file content reuses objects; a commit need not store another full copy of every unchanged file.</p>
 <p>A normal commit has one parent, a root commit has none, and a merge commit usually has two. Changing content, parents, metadata or the message changes the commit object and normally its ID. Rebase and amend create replacement commits; they do not edit an existing immutable commit in place.</p>""" +
 graph("A ── B ── C  ← main\n          ↑\n      parent of C", "Lines express ancestry, not elapsed time. A branch is a movable reference to a commit.") +
 code("git show --no-patch --pretty=raw HEAD\ngit cat-file -p HEAD\ngit ls-tree HEAD") +
 """<p>Most repositories you encounter use SHA-1 object IDs; Git also supports SHA-256 repository formats. Do not build tooling that assumes all identifiers are exactly 40 characters. Short prefixes are convenient only when unambiguous in that repository.</p>"""),
section("refs", "HEAD, branches and tags",
 """<p>On a branch, HEAD normally names a branch reference such as <code>refs/heads/main</code>. A new commit moves that branch forward. A branch is not a separate directory or a complete copied project. Switching branches updates the index and working tree; Git may refuse if doing so would overwrite local changes.</p>
 <p>Detached HEAD points directly to a commit, often when inspecting a tag or bisecting. You can commit there, but create a branch to retain new work before switching away. A tag normally marks a release point. Annotated tags have their own metadata and can be signed; lightweight tags are simple references. Tags can technically be moved, but published release tags should be treated as stable.</p>""" +
 code("git branch --show-current\ngit symbolic-ref --short HEAD\n# If you deliberately created useful commits while detached:\ngit switch -c rescue/detached-work") +
 """<p>The symbolic-ref command returns a nonzero status when HEAD is detached. That is an observation, not necessarily a broken repository.</p>"""),
section("setup", "Install, identify and inspect",
 code("git --version\ngit config --global user.name 'Your Name'\ngit config --global user.email 'your-approved-address@example.com'\ngit config --show-origin --get user.email\ngit config --show-origin --get-regexp '^(user|pull|push|merge)\\.'") +
 """<p>Use your operating system’s supported installer or package manager. Configure an approved work or GitHub noreply email if appropriate. <code>user.name</code> and <code>user.email</code> are commit metadata; they do not authenticate you or grant GitHub permissions. Repository-local settings can override global settings. Inspect origin and scope when an unexpected identity is used.</p>""" +
 source(("Git object model","https://git-scm.com/book/en/v2/Git-Internals-Git-Objects"),("Git configuration","https://git-scm.com/docs/git-config")))
], ["add selects content; commit records the index.", "Branches move; existing commit objects do not change.", "Author identity, cryptographic signatures and GitHub authentication are different."], "foundations")

lesson("daily-workflow", "A reliable daily development loop", 25,
 "Move from an issue to a coherent commit, with intentional staging, useful messages and a reviewable diff.",
 ["Stage only intended changes and verify the commit.", "Keep generated files, secrets and unrelated edits out.", "Choose a clean starting point for integration."], [
section("start", "Start by establishing context",
 code("git rev-parse --show-toplevel\ngit status\ngit branch --show-current\ngit remote -v\ngit fetch origin\ngit log --oneline --decorate -8") +
 """<p>Check that you are inside the intended clone, on the intended branch, talking to the expected remote. Remote URLs should not contain tokens. Fetch updates your knowledge of the remote without merging into your current branch. Inspect uncommitted work before switching or integrating.</p>
 <p>On a clean working tree, a common feature start is <code>git switch main</code>, <code>git merge --ff-only origin/main</code>, then <code>git switch -c feature/login-timeout</code>. If fast-forward fails, inspect divergence; do not make the failure disappear with a hard reset.</p>"""),
section("commit", "Build one reviewable change",
 code("git diff -- src/login.py\ngit add -p -- src/login.py\ngit diff --staged\ngit diff --staged --check\n# Run the project’s relevant tests here.\ngit commit -m 'Handle expired login challenges'\ngit show --stat HEAD\ngit status") +
 """<p>Partial staging lets you separate unrelated changes within one file. The patch shown by <code>git diff --staged</code> is the proposed snapshot. Review it for missing files, debug output, accidental formatting, credentials and generated artifacts. A commit should answer one understandable question, not merely capture everything that happened since lunch.</p>
 <p>A useful message describes behavior and why it changed. Use a short summary and, for a complex change, a body explaining the problem, constraints and tradeoff. Follow the team’s conventions; a naming scheme cannot replace a coherent diff.</p>""" +
 note("Staged content can be stale", "After staging, later edits are not automatically included. Recheck both git diff and git diff --staged before committing. Avoid a broad git add . when other work is mixed into the directory.", "warn")),
section("ignore", "Ignore rules are not deletion or secret protection",
 code("# .gitignore example\n.env\n.venv/\n__pycache__/\n*.log", "Repository ignore patterns — adapt to your project") +
 """<p><code>.gitignore</code> affects untracked-file discovery; it does not remove a file already tracked in history. For a tracked file that should stay on disk but leave the next snapshot, inspect and use <code>git rm --cached -- path</code>, then commit that removal. Old commits still contain the file. Use <code>git check-ignore -v -- path</code> to locate the matching ignore rule.</p>
 <p>Track a sanitized example configuration rather than an actual secret. Lockfiles are often intentionally tracked for reproducibility; do not ignore them reflexively. Large binaries may need Git LFS or artifact storage, not repeated ordinary Git snapshots.</p>"""),
section("handoff", "Before pushing and asking for review",
 """<ol class="checklist"><li>Read the exact diff and confirm the branch and remote.</li><li>Run relevant tests, checks and a build where required.</li><li>Confirm the base branch is appropriate and no private data is included.</li><li>Push the feature branch with an explicit upstream.</li><li>Open a pull request that explains the problem, behavior, validation and rollout implications.</li></ol>""" +
 code("git push -u origin feature/login-timeout") +
 """<p>A successful push only means the server accepted the update. It does not prove CI passed or the change was merged. Read the pull request checks and review comments. Save local work with a commit, a reviewed stash, or a separate worktree before taking on a different urgent task.</p>""" +
 source(("Staging","https://git-scm.com/docs/git-add"),("Ignore rules","https://git-scm.com/docs/gitignore"),("Commit","https://git-scm.com/docs/git-commit")))
], ["Inspect before staging; inspect staged content before committing.", "One commit should have one coherent purpose.", "Ignore rules neither untrack existing files nor remove secrets from history."], "daily-workflow")

lesson("branches-remotes", "Branches, remotes, fetch, pull & push", 30,
 "Separate your branch, your cached view of the remote and the actual server branch.",
 ["Explain local branches, remote-tracking references and upstreams.", "Recognize fast-forward and divergence.", "Choose integration explicitly after fetching."], [
section("three-refs", "Three references that people confuse",
 table(["Name", "Where it lives", "When it changes"],[
 ["<code>feature</code>", "Your local branch, refs/heads/feature", "When you commit, merge, rebase or deliberately move it."],
 ["<code>origin/feature</code>", "A local remote-tracking reference", "Normally updated by fetch, and sometimes by successful pushes; it can be stale."],
 ["<code>feature</code> on origin", "The actual branch on the server", "When an authorized update is accepted there."]]) +
 graph("Your clone                           Remote repository\nfeature ──────► L                    feature ──────► R\norigin/feature ► K\n\nK = last observed tip; it may differ from R.", "origin is a configured remote name, not a special server type. Upstream is a tracking relationship.") +
 code("git branch -vv\ngit remote -v\ngit fetch origin\ngit log --oneline --left-right HEAD...origin/feature") +
 """<p>Ahead/behind counts describe ancestry against the local tracking reference, not a live request to GitHub. Fetch first when you need current information. A fork is a hosted repository relationship; a clone is your local copy. A fork workflow commonly names your fork <code>origin</code> and the parent project <code>upstream</code>, but those names are conventions.</p>"""),
section("fetch-pull", "Fetch gathers; integration changes your branch",
 flow([("Fetch", "Download reachable objects and update tracking refs"),("Inspect", "Compare ancestry and intended changes"),("Integrate", "Fast-forward, merge or rebase deliberately")]) +
 table(["Command", "Effect"],[
 ["<code>git fetch origin</code>", "Updates remote-tracking information according to refspecs; does not merge into the checked-out branch."],
 ["<code>git pull --ff-only</code>", "Fetches, then requires a fast-forward integration; refuses divergent history."],
 ["<code>git pull --rebase</code>", "Fetches and rebases local work onto the selected upstream; may replay commits and stop for conflicts."],
 ["<code>git pull --no-rebase</code>", "Fetches and uses merge-based integration; may fast-forward or make a merge commit."]]) +
 """<p>Do not assume every developer’s plain <code>git pull</code> behaves the same: version, branch config and user settings matter. A cautious learning default is <code>git config --local pull.ff only</code>; if it refuses, inspect and choose an explicit operation. Teams may deliberately standardize on another policy.</p>"""),
section("push", "Why an ordinary push is rejected",
 graph("Before: A ── B ── C  remote feature\n                 └── D  local feature\n\nC is not an ancestor of D. Updating C → D is not a fast-forward.", "The rejection protects the remote branch’s ancestry. It does not mean you lack authentication.") +
 """<p>When a teammate has pushed C and your local work is D, fetch, inspect and integrate the teammate’s change using the team’s merge or rebase policy. A normal push can then advance to a descendant that includes the shared work. If you intentionally rewrote your own published branch, use the separate force-push procedure after coordination.</p>
 <p>Set the tracking relationship with <code>git push -u origin feature</code>, or inspect and set an upstream explicitly using <code>git branch --set-upstream-to=origin/feature feature</code>. Verify the branch exists. Never use force merely to repair a missing upstream or an authentication failure.</p>"""),
section("cleanup", "Pruning is not deleting teammates’ server branches",
 code("git fetch --prune origin\ngit branch --merged main\ngit branch -d feature/completed") +
 """<p>Pruning removes stale local remote-tracking references covered by the fetch refspec; normal branch pruning does not delete live server branches. Deleting a local branch with <code>-d</code> includes a merge-safety check, although “merged” depends on the tracked upstream or current branch. <code>-D</code> bypasses that check. <code>git push origin --delete branch</code> deletes a remote branch and requires an intentional team decision.</p>
 <p>Before deleting, confirm the work is integrated as intended, especially after squash merges: patch content may be integrated even though the original commits are not ancestors of main.</p>""" +
 source(("Fetch","https://git-scm.com/docs/git-fetch"),("Pull","https://git-scm.com/docs/git-pull"),("Branch tracking","https://git-scm.com/docs/git-branch")))
], ["origin/feature is a local observation, not the live server branch.", "Fetch first, then choose integration deliberately.", "A non-fast-forward rejection is a history question, not an invitation to force."], "branches-remotes")

lesson("merge", "Merge and the three-way comparison", 35,
 "See how Git combines two lines of development and why the common ancestor matters.",
 ["Distinguish fast-forward, merge commit and squash.", "Explain base, ours and theirs during a merge.", "Understand what an automatic merge does not guarantee."], [
section("fast-forward", "Fast-forward moves a pointer",
 graph("Before:\nA ── B           main\n      └── C ── D feature\n\nAfter git switch main; git merge --ff-only feature:\nA ── B ── C ── D main, feature", "B is an ancestor of D, so main can move forward without creating a merge commit.") +
 """<p>The diagram draws a separate line for feature only to show the label; C’s parent is B. A fast-forward does not combine independent edits because there is no divergent main-side work to combine. <code>--ff-only</code> fails if moving the pointer would not be enough.</p>"""),
section("three-way", "A three-way merge uses three snapshots",
 graph("       C  ← main (ours)\n      / \\\nA ── B   M  ← resulting main\n      \\ /\n       D  ← feature (theirs)\n\nB = merge base; M has parents C and D.", "Git compares what changed from B to C and from B to D, then builds a combined tree.") +
 table(["Snapshot", "timeout", "retries", "Interpretation"],[
 ["Base B","10","1","Common starting point."],
 ["Ours C","20","1","Main changed timeout."],
 ["Theirs D","10","3","Feature changed retries."],
 ["Combined M","20","3","Independent edits can be combined."]]) +
 """<p>Comparing only the two tips would not tell you which side changed each value. The base supplies that context. Git can usually combine independent edits; overlapping changes with incompatible textual resolutions may cause conflicts. Two branches changing the same file does not necessarily conflict, and two branches changing different files can still introduce a semantic bug.</p>
 <p>For a single merge base, inspect it with <code>git merge-base main feature</code>. In more complex criss-cross histories, there may be multiple best bases; the merge strategy may synthesize a base tree. The three-snapshot mental model remains useful, but the base need not be one simple hand-picked commit.</p>"""),
section("modes", "Choose the history you want to record",
 table(["Method", "New history shape", "Use and tradeoff"],[
 ["Fast-forward", "Moves the receiving branch to an existing descendant.", "Simple when no divergence; no merge boundary is recorded."],
 ["<code>git merge --no-ff feature</code>", "A merge commit with two parents, even when fast-forward is possible.", "Records integration ancestry; more graph structure."],
 ["<code>git merge --squash feature</code>, then commit", "Prepares a combined change; the later commit has one parent.", "One integration commit, but no parent link to the feature tip; repeated integration from a long-lived branch needs care."],
 ["Rebase, then fast-forward", "Replays commits onto a new base, then moves a ref.", "Linear history with rewritten identities; coordination is needed if old identities were shared."]]) +
 """<p>During a normal merge, existing commits stay unchanged. A merge commit records both parent lines, and its tree can include manual conflict-resolution changes that were in neither parent. A squash is not a record that all source commits became ancestors. That difference affects future merges, history analysis and branch-deletion checks.</p>"""),
section("perform", "Perform and verify a merge",
 code("git status\ngit fetch origin\ngit switch feature\ngit branch backup/feature-before-merge\ngit merge origin/main\n# If conflicts occur, follow the conflicts module before continuing.\ngit log --graph --oneline --decorate -12\ngit diff HEAD^1 HEAD\n# Run relevant tests before pushing.") +
 """<p>Use a unique backup-branch name; it protects the current committed tip, not uncommitted files. A backup branch does not replace checking a clean working tree. If you need to stop an in-progress merge, <code>git merge --abort</code> attempts to restore the pre-merge state. Starting with unrelated dirty work makes restoration harder and can prevent exact recovery.</p>
 <p>Automatic textual success means Git found a mechanically mergeable result. Verify API compatibility, imports, database assumptions and generated artifacts. Run tests that exercise the interaction between both changes, not just each branch independently.</p>""" +
 source(("Git merge","https://git-scm.com/docs/git-merge"),("Merge bases","https://git-scm.com/docs/git-merge-base")))
], ["Fast-forward moves a reference; a true merge combines divergent histories.", "Three-way means base + current side + incoming side.", "A conflict-free merge can still contain a functional bug."], "merge")

lesson("conflicts", "Resolve conflicts without losing intent", 45,
 "Follow a repeatable conflict-resolution procedure and learn what the editor’s buttons actually choose.",
 ["Identify the operation and conflict stages.", "Build the intended combined result and validate it.", "Handle text, delete/modify, rename, binary and generated-file conflicts."], [
section("first", "Stop and identify the operation",
 code("git status\ngit diff --name-only --diff-filter=U\ngit ls-files -u\ngit diff") +
 """<p>A conflict means the operation paused because Git could not finish some decisions automatically. It does not mean your repository is corrupted. First read whether this is a merge, rebase, cherry-pick, revert or stash application. Their continue and abort commands are different.</p>
 <p>List all unresolved paths, then read each branch’s intent: issue, commit message, surrounding code and tests. If two changes encode incompatible requirements, talk to the owners. A merge tool can edit text; it cannot decide which business behavior is correct.</p>"""),
section("markers", "Read all three versions",
 code("""<<<<<<< HEAD
timeout = 20
||||||| base
timeout = 10
=======
timeout = 30
>>>>>>> feature""", "Example diff3 conflict markers — not a shell command") +
 """<p>The marker labels depend on the operation. For a normal merge, HEAD/current is your checked-out branch and incoming is the branch being merged. <code>git config --local merge.conflictStyle diff3</code> includes the base in newly produced conflict markers. <code>zdiff3</code> is another useful style on supported Git versions.</p>""" +
 code("git show :1:settings.txt\ngit show :2:settings.txt\ngit show :3:settings.txt", "Inspect unmerged index stages for this path") +
 """<p>Stage 1 is the base, 2 is ours and 3 is theirs. Some stages are absent for add/add or delete/modify conflicts. During a rebase, ours is the new base plus already replayed commits; theirs is the commit currently being replayed. Do not equate ours with “my original feature branch” in every operation.</p>
 <p>“Accept current,” “Accept incoming,” and “Accept both” usually choose text mechanically. Accepting both may duplicate functions, create invalid JSON or combine two mutually exclusive values. Inspect the labels and construct the intended final content.</p>"""),
section("resolve", "The resolution loop",
 flow([("Understand", "Read base, both changes and requirements"),("Edit", "Produce one correct final result"),("Stage", "Mark each resolved path with add or rm"),("Validate", "Inspect the staged diff and test behavior"),("Continue", "Use the operation-specific command")]) +
 code("git add -- settings.txt\ngit diff --cached\ngit diff --cached --check\ngit diff --name-only --diff-filter=U\n# Run the relevant tests, then use ONE matching operation:\n# git merge --continue\n# git rebase --continue\n# git cherry-pick --continue\n# git revert --continue") +
 """<p>Staging says “this is my resolution,” not “this is correct.” Removing conflict markers is only one check. The unresolved-path list must be empty before continuing, and the staged diff must preserve the intended changes. A rebase can stop again at the next replayed commit; resolve each stop in context.</p>""" +
 note("Be precise with ours/theirs shortcuts", "git restore --ours -- path or --theirs chooses an entire side from the unmerged index for that path. It can discard useful changes from the other side. During rebase the labels are particularly easy to misread. Prefer manual intent-based editing when both changes matter.", "warn")),
section("types", "Conflicts beyond a few lines",
 table(["Type", "A careful resolution"],[
 ["Delete/modify", "Decide whether deletion or continued existence matches the feature. Use git rm for the intended deletion, or restore/edit and git add the retained file."],
 ["Add/add", "Both sides introduced the path. Compare complete contents and build one valid file; there may be no base stage."],
 ["Rename/rename or rename/delete", "Inspect old/new paths and callers. Decide the final name and update references; Git rename detection is inferred from content."],
 ["Binary", "A text merge is not available. Choose or regenerate a known correct artifact, verify it in its application and stage it."],
 ["Lockfile", "Resolve source manifests, use the project’s pinned package-manager version to regenerate the lockfile as documented, inspect and test. Do not blindly choose one side or delete the lockfile."],
 ["Generated code", "Resolve source-of-truth inputs, regenerate consistently, review the generated diff and test."],
 ["Whitespace / line endings", "Check .gitattributes and normalization policy. Avoid mixing a mass normalization with a functional conflict fix."],
 ["Semantic conflict", "Text merged cleanly but APIs or assumptions disagree. Only review and behavioral tests reveal it."]])),
section("abort", "Know how to stop safely",
 table(["Operation", "Stop / recover"],[
 ["Merge in progress", "<code>git merge --abort</code>."],
 ["Rebase in progress", "<code>git rebase --abort</code>; --quit has different semantics and leaves current state."],
 ["Cherry-pick / revert", "<code>git cherry-pick --abort</code> or <code>git revert --abort</code>."],
 ["Stash apply/pop conflict", "There is no git stash --abort. Preserve existing work, inspect status and the retained stash, then restore only the intended tracked paths or use a clean worktree."],
 ["Need to skip a rebase/cherry-pick step", "--skip drops that commit’s replay from the sequence. Use only when you have verified the change is already present or deliberately unnecessary."]]) +
 """<p>Do not respond to conflict fatigue with <code>reset --hard</code>. Copy important uncommitted files outside the repository if necessary, record the operation state, and prefer the matching abort command. Reuse resolutions with <code>rerere</code> only after understanding and reviewing what it reapplies.</p>""" +
 source(("Conflict stages and markers","https://git-scm.com/docs/git-merge"),("Restore side selection","https://git-scm.com/docs/git-restore"),("Rebase side reversal","https://git-scm.com/docs/git-rebase")))
], ["Identify the operation before interpreting current/incoming.", "Resolve intended behavior, not just the visible markers.", "Inspect the staged result, test, then continue or abort deliberately."], "conflicts")

lesson("rebase", "Rebase: replay changes onto a new base", 40,
 "Understand which commits are recreated, how conflicts are replayed, and what collaborators see after a rewrite.",
 ["Predict commit IDs and parent changes after rebase.", "Perform and inspect a private-branch rebase.", "Use interactive rebase and --onto with a recovery point."], [
section("picture", "What actually changes",
 graph("Before:\nA ── B ── C       main\n      └── D ── E  feature\n\nAfter rebasing feature onto main:\nA ── B ── C ── D′ ── E′  feature\n          ↑\n         main\n\nD and E are not edited. D′ and E′ are new commits.", "Each replay applies a commit’s change in a new parent context. That creates new identities.") +
 """<p>Rebase selects commits not already integrated into the target history and replays their changes onto a new base. In the simple case D and E become D′ and E′. The resulting files may look familiar, but different parents or metadata mean different commit IDs. Git may skip changes already upstream or handle newly empty commits according to its options.</p>
 <p>Rebase does not move main merely because you rebased onto it. It moves the branch you are rebasing. Ordinary rebase generally flattens merge structure; <code>--rebase-merges</code> attempts to recreate it and requires extra review. Do not treat every history shape as the simple two-commit example.</p>"""),
section("procedure", "A private branch rebase you can inspect",
 code("git status\ngit fetch origin\ngit switch feature\n# Choose a fresh backup name and start from a clean working tree.\ngit branch backup/feature-before-rebase\ngit merge-base feature origin/main\n# Record that output as OLD_BASE for the later comparison.\ngit rebase origin/main\ngit log --graph --oneline --decorate -15\ngit range-diff OLD_BASE..backup/feature-before-rebase origin/main..feature") +
 """<p>The backup retains the old committed tip. Record the old merge base before rewriting, because comparing the wrong ranges can hide a dropped patch. <code>range-diff</code> helps map the old patch series to the new one; it is a review aid, not a proof that behavior is identical. Inspect meaningful differences and run tests.</p>
 <p>If the branch was never pushed, an ordinary push publishes the new history. If its old IDs are already on the server, a normal push will usually be rejected as non-fast-forward. That is when the force-push lesson and your team’s shared-history policy matter.</p>"""),
section("conflict", "Why the same file can conflict more than once",
 """<p>Rebase works through individual commits. A resolution while replaying D can be followed by another conflict when replaying E. During each pause, the new base and successfully replayed commits are the “ours” side. The original commit currently being replayed is “theirs.” Read the content, not just the editor’s button names.</p>""" +
 code("git status\ngit rebase --show-current-patch\n# Edit and test the intended combined result.\ngit add -- path/to/resolved-file\ngit rebase --continue\n# To return to the original branch state instead:\n# git rebase --abort") +
 """<p><code>--skip</code> omits the current replayed change; it is not a generic “fix this conflict” operation. <code>--abort</code> restores the pre-rebase branch state when possible. <code>--quit</code> stops rebase bookkeeping while leaving HEAD, index and working-tree state where they are. Those choices have different consequences.</p>"""),
section("interactive", "Clean up a private patch series",
 code("git rebase -i origin/main", "Interactive rebase — review every todo action before saving") +
 table(["Action", "Effect"],[
 ["pick", "Replay the commit."],["reword","Replay but edit its message."],["edit","Pause to amend or split a change; continue when ready."],
 ["squash","Combine with the previous picked commit and edit the message."],["fixup","Combine while discarding this commit’s message by default."],
 ["drop","Omit the change from the replayed series. This is a deliberate content decision."]]) +
 """<p>The todo list normally runs oldest first. Reordering can break dependencies; combining commits can hide useful review boundaries. <code>git commit --fixup COMMIT</code> with <code>git rebase -i --autosquash BASE</code> helps organize review fixes. Review the resulting patch series rather than assuming a prettier graph means better code.</p>"""),
section("onto", "Move a specific range with --onto",
 graph("A ── B ── C        old-base\n           └─ D ─ E feature\nA ── X ── Y        new-base\n\n git rebase --onto new-base old-base feature\n\nA ── X ── Y ── D′ ── E′ feature", "Only the feature-side range after old-base is replayed onto new-base.") +
 """<p>This is useful for retargeting dependent work after a base branch changes, but the boundary is easy to choose incorrectly. Inspect <code>git log old-base..feature</code> first. A wrong boundary can replay unrelated changes or omit required ones. For shared branches, agree on the migration and keep old tips available to collaborators.</p>""" +
 source(("Rebase manual","https://git-scm.com/docs/git-rebase"),("Compare patch series","https://git-scm.com/docs/git-range-diff")))
], ["Rebase recreates selected commits and changes their IDs.", "Conflicts happen per replay; ours is the new-base side.", "Review ranges and coordinate before rewriting published history."], "rebase")

lesson("force-push", "Force push, leases & shared-history safety", 45,
 "Learn exactly what a force push replaces, why teammates can lose reachability, and what a lease does and does not protect.",
 ["Distinguish normal push, --force and an explicit lease.", "Inspect and preserve history before a permitted rewrite.", "Respond safely to a rejected lease or accidental rewrite."], [
section("effect", "Force push moves a server reference",
 graph("Remote before:\nA ── B ── C ── T  feature   (T is a teammate’s commit)\n      └── C′      your rewritten local feature\n\nForce update feature to C′:\nA ── B ── C′      remote feature\n      └── C ── T  no longer reachable from that branch", "The old objects may still exist in other references, clones or server storage, but the branch no longer leads to them.") +
 """<p>A force push requests a non-fast-forward reference update. The server may accept it only if permissions, rules and hooks allow it. It does not physically erase every old commit everywhere, and it does not overwrite another developer’s working files immediately. Their clone still has its own state; a later fetch shows the changed server reference and may leave their branch diverged.</p>
 <p>The danger is replacing a shared branch tip without retaining commits people expected to remain in that branch’s history. The server’s acceptance is not a semantic approval. Force pushing is not a way to fix authentication, choose a remote, resolve a source conflict or make failing tests pass.</p>"""),
section("compare", "Three push behaviors",
 table(["Push mode", "What it checks", "Remaining risk"],[
 ["Ordinary push", "The remote branch tip must normally be an ancestor of the proposed tip.", "You still need the correct destination and correct content."],
 ["<code>--force</code>", "Asks to bypass normal ancestry protection for the pushed refs; server rules still apply.", "Can replace commits you have not incorporated. It also disables lease protection if combined with it."],
 ["<code>--force-with-lease</code>", "Checks the remote tip against your local tracking expectation by default.", "An automatic/background fetch can advance that expectation without you reviewing the new commits."],
 ["Explicit <code>--force-with-lease=refs/heads/feature:EXPECTED</code>", "Requires that exact remote reference to still equal the pinned object ID.", "Protects against concurrent tip changes, not against deleting known commits or publishing bad content."]]) +
 """<p>Do not combine <code>--force</code> with a lease. A lease does not grant permission and does not override protected-branch rules. Pin the expected value before rewriting so you know precisely which remote state you are agreeing to replace.</p>"""),
section("sequence", "A deliberate, coordinated rewrite procedure",
 """<p>Use this only on a branch where rewriting is permitted and collaborators have agreed. These are separate steps to inspect, not an unattended paste-and-run script. Start with a clean working tree, fetch, and understand every remote-only commit before proceeding.</p>""" +
 code("""git status
git fetch origin
git switch feature
git log --left-right --graph --oneline feature...origin/feature
# Stop if remote work is not understood and preserved.
expected=$(git rev-parse refs/remotes/origin/feature)
git branch backup/feature-before-rewrite
git branch backup/remote-feature-before-rewrite "$expected"
# Perform the agreed rewrite, for example:
git rebase origin/main
# Inspect range-diff, final diff and run tests before this push:
git push --force-with-lease=refs/heads/feature:"$expected" origin HEAD:refs/heads/feature""") +
 """<p>The explicit destination prevents a vague default from selecting the wrong branch. Backup names must be unused and protect only committed history. If the remote already contains work absent locally, integrate or deliberately account for it first; pinning its ID does not preserve its content by itself.</p>"""),
section("rejection", "If the lease is rejected",
 flow([("Stop", "Someone changed the expected remote tip"),("Fetch and inspect", "Find the new commits and their owner"),("Preserve intent", "Integrate or coordinate the replacement"),("Review again", "Tests, graph and a new intentional expectation")]) +
 """<p>Do not blindly fetch, refresh the expected ID and retry the same destructive update. That merely teaches the lease to accept a state you still have not preserved. Inspect what changed and agree on how both lines of work should survive.</p>
 <p>For teammates affected by an intentional rewrite, fetch, preserve their local tip under a new branch, then move only their unpublished work onto the agreed new base. This may require a carefully bounded rebase or selected cherry-picks. A broad pull/merge can reintroduce the old history. A hard reset can discard local work.</p>"""),
section("recovery", "If the wrong branch was force-pushed",
 """<p>Stop further updates, communicate the incident, and locate the old tip in a colleague’s clone, a local reflog, a backup reference or other retained evidence. Create a rescue branch at that old commit before doing anything else. Compare old and current server history; another force update can otherwise erase legitimate work added after the incident.</p>
 <p>Restoring the old tip is a coordinated server change, subject to policy. A local reflog is not a durable remote backup. If the goal is secret removal, revoke the credential first and follow the dedicated repository-cleanup procedure; a force push cannot clean everybody’s clones or caches.</p>""" +
 source(("Push and lease semantics","https://git-scm.com/docs/git-push"),("GitHub protected branches","https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches")))
], ["Force updates a reference; it is not secure erasure.", "An explicit lease checks an exact expected tip, not correctness.", "A rejected lease means inspect new work, not weaken the protection."], "force-push")

lesson("undo-recovery", "Undo, reset, revert & recover", 40,
 "Choose an undo operation based on what must move and whether other people already depend on the history.",
 ["Distinguish restore, reset, revert, amend and clean.", "Recover a committed tip using reflog and a rescue branch.", "Understand what Git cannot recover reliably."], [
section("choose", "Match the tool to the layer",
 table(["Intent", "Tool", "What changes"],[
 ["Unstage a tracked path", "<code>git restore --staged -- path</code>", "Index is restored from HEAD by default; working files remain."],
 ["Discard unstaged tracked edits", "<code>git restore -- path</code>", "Working file is overwritten from the index. Save needed edits first."],
 ["Undo a public change with new history", "<code>git revert COMMIT</code>", "Creates a new inverse change; existing commits remain reachable."],
 ["Replace the last private commit", "<code>git commit --amend</code>", "Creates a replacement commit; ID changes."],
 ["Move current branch tip, retain index and files", "<code>git reset --soft TARGET</code>", "HEAD/current branch changes; staged and working content stay."],
 ["Move tip and reset index, retain files", "<code>git reset --mixed TARGET</code>", "Default reset mode; changes become unstaged."],
 ["Move tip and overwrite tracked state", "<code>git reset --hard TARGET</code>", "Tracked index/working content is reset; obstructing untracked paths can also be removed."],
 ["Remove untracked files", "<code>git clean</code>", "Separate destructive operation. Preview with -n; ignored files need extra flags."]]) +
 """<p>Path-limited reset has different semantics from commit-level reset: <code>git reset HEAD -- path</code> adjusts the index, not the branch. Avoid reasoning about every reset as the same operation. A backup branch protects commits, not unsaved file contents.</p>"""),
section("revert", "Revert shared work without rewriting ancestry",
 graph("A ── B ── C ── R  main\n          bad   inverse change\n\nC remains in history. R records the correction.", "Revert can conflict when later work changed the same area. Test the final behavior.") +
 code("git show COMMIT\ngit revert COMMIT\n# Resolve conflicts if necessary, then:\n# git revert --continue\n# Or stop with git revert --abort") +
 """<p>Revert applies the inverse of a selected change in the current context. It does not automatically roll back database changes, deployments, deleted external data or leaked credentials. A rollback plan must cover those systems separately.</p>
 <p>For a merge commit, inspect its parents with <code>git show --no-patch --pretty=raw MERGE</code>. <code>git revert -m 1 MERGE</code> chooses parent 1 as the mainline; do not assume that is always the intended parent. The original merge ancestry remains recorded, so merging the same branch again may not reintroduce the reverted changes. Plan new commits or a reviewed revert of the revert as appropriate.</p>"""),
section("reflog", "Recover by creating a new reference first",
 code("git reflog --date=iso\ngit show OLD_TIP\ngit branch rescue/before-mistake OLD_TIP\ngit log --graph --oneline --decorate --all -25") +
 """<p>Reflogs record local reference movements such as commits, resets and rebases. Find the event and inspect its commit rather than guessing <code>HEAD@{1}</code>; later commands may have changed that numbering. Create a rescue branch so the commit remains reachable, then decide how to integrate it.</p>
 <p>Reflogs are local and expire. A new clone does not download your old local reflog. Garbage collection can eventually remove unreachable objects. Some committed work may be recoverable if objects still exist; discarded untracked or never-staged file content generally is not a Git recovery promise. Editor history, filesystem snapshots and backups may be needed.</p>"""),
section("stash", "Stash is temporary storage, not a backup system",
 code("git stash push -u -m 'WIP before urgent fix'\ngit stash list\ngit stash show -p 'stash@{0}'\ngit stash apply 'stash@{0}'\n# Inspect and test before deliberately dropping a successfully applied stash.") +
 """<p>Ordinary stash captures tracked changes. <code>-u</code> includes untracked files; <code>-a</code> also includes ignored files and needs extra care. <code>apply</code> keeps the stash; <code>pop</code> drops it only after a successful application and normally keeps it when conflicts occur. Applying onto changed code can conflict.</p>
 <p>A stash apply conflict has no stash-specific abort command. Protect any pre-existing uncommitted work before cleaning the attempted application. Consider <code>git stash branch rescue/wip 'stash@{0}'</code> to apply around its original base; it can remove the stash on successful application, so inspect the result. For long-lived work, prefer a named branch and coherent commits.</p>"""),
section("guard", "Before discarding anything",
 """<ol class="checklist"><li>Inspect status, both diffs, untracked and ignored files relevant to the task.</li><li>Identify exactly what is committed, staged, unstaged and outside Git.</li><li>Save important files or make a suitable commit/stash before a destructive change.</li><li>Preview clean with <code>git clean -nd</code>; adding <code>-x</code> also targets ignored files such as local databases and environments.</li><li>Use explicit paths and targets, then verify the remaining state.</li></ol>""" +
 source(("Reset","https://git-scm.com/docs/git-reset"),("Restore","https://git-scm.com/docs/git-restore"),("Revert","https://git-scm.com/docs/git-revert"),("Reflog","https://git-scm.com/docs/git-reflog"),("Stash","https://git-scm.com/docs/git-stash")))
], ["Public correction usually calls for revert; private rewriting is a separate choice.", "A rescue branch protects a discovered committed tip before further operations.", "Reflog cannot promise recovery of never-recorded content."], "undo-recovery")

lesson("history", "Trace history, explain changes & find regressions", 40,
 "Turn commit history into evidence with log, diff, show, blame, range-diff and bisect.",
 ["Read ancestry rather than relying on timestamps.", "Find when and why code changed.", "Use a reliable test to locate a regression."], [
section("graph", "Start with the shape and the question",
 code("git log --graph --oneline --decorate --all -30\ngit log --first-parent --oneline main\ngit show --stat COMMIT\ngit show COMMIT -- path/to/file\ngit show COMMIT:path/to/file") +
 """<p><code>--all</code> walks commits reachable from local refs; it does not mean all commits ever created or everything still on the server. Fetch when remote history matters. <code>--first-parent</code> follows the integration line and is useful for release history when merges are preserved. Author and committer dates can differ and do not replace parent relationships.</p>
 <p>Ask a specific question: “What introduced this timeout?”, “Which feature landed in this release?”, “Was this patch preserved after rebase?” Different commands provide different evidence. Start with a small relevant range instead of reading thousands of unrelated commits.</p>"""),
section("ranges", "Two dots and three dots depend on the command",
 table(["Expression", "For git log", "For git diff"],[
 ["<code>A..B</code>", "Commits reachable from B but not from A.", "Compare endpoint trees A and B, like git diff A B."],
 ["<code>A...B</code>", "Commits reachable from either side but not both (symmetric difference).", "Compare the merge base with B: what the B side changed since the common base. This is asymmetric."],
 ["<code>HEAD^1</code> / <code>HEAD^2</code>", "First / second parent of HEAD; second requires a merge commit.", "Use those revisions to compare chosen parents or snapshots."],
 ["<code>HEAD~3</code>", "Follow the first-parent chain three times.", "A revision selector, not “three commits in date order.”"]]) +
 code("git log --left-right --oneline main...feature\ngit diff main...feature\ngit log --oneline origin/main..HEAD") +
 """<p>A pull-request diff commonly focuses on head-side changes since a merge base. A direct tip-to-tip diff answers another question. Always say which comparison you mean when discussing “the diff.”</p>"""),
section("find", "Find the change behind a line",
 code("git log --follow -- path/to/file\ngit log -p -- path/to/file\ngit log -S 'timeout_seconds' --all -- path/to/file\ngit log -G 'timeout.*=' --all -- path/to/file\ngit blame -L 20,45 -- path/to/file\ngit show COMMIT") +
 """<p><code>--follow</code> follows one file across detected renames; rename tracking is heuristic, not a stored rename event. <code>-S</code> finds changes to the number of occurrences of a string. <code>-G</code> finds patches whose added/removed lines match a regular expression.</p>
 <p>Blame shows the last modifying commit for lines in the selected revision. Use it to find context and read the whole commit, its parent and linked review. It is not a measure of responsibility or code quality: formatting, generated changes and moves can change attribution. <code>-w</code> can ignore whitespace in the blame calculation when that helps.</p>"""),
section("bisect", "Find the first bad commit with a repeatable test",
 flow([("Known good", "A revision where the behavior works"),("Known bad", "A revision where it fails"),("Test midpoint", "Classify good, bad or untestable"),("Narrow range", "Repeat until a culprit is identified")]) +
 code("git status\ngit bisect start\ngit bisect bad BAD_COMMIT\ngit bisect good GOOD_COMMIT\n# Test the checked-out revision and say git bisect good or bad.\n# Or automate with a verified test script:\ngit bisect run ./test-regression.sh\ngit bisect log\ngit bisect reset") +
 """<p>A clean working tree protects unrelated work while bisect checks out revisions. The test must detect the same regression across the range. Exit 0 means good; exit 125 means skip because this revision cannot be tested; ordinary nonzero test failures mark bad (the manual documents special statuses). A missing dependency is not proof the product regression exists there.</p>
 <p>A nonmonotonic or flaky test can mislead bisect. Reproduce the identified commit and its parent, read the patch, and check environmental changes. End with <code>git bisect reset</code> to return to the original checkout.</p>"""),
section("rewrite", "Audit a rewritten patch series",
 code("git range-diff OLD_BASE..backup/feature NEW_BASE..feature\ngit log --cherry-mark --left-right --oneline old-tip...new-tip") +
 """<p>Patch equivalence can help recognize changes that have new IDs after rebase or cherry-pick. It is not identical to ancestry or functional equivalence. <code>range-diff</code> compares patch series and helps reviewers inspect conflict-resolution edits, missing patches and unexpected reordering. Use the correct base boundaries and read unmatched entries.</p>""" +
 source(("Log and ranges","https://git-scm.com/docs/git-log"),("Diff","https://git-scm.com/docs/git-diff"),("Blame","https://git-scm.com/docs/git-blame"),("Bisect","https://git-scm.com/docs/git-bisect"),("Range-diff","https://git-scm.com/docs/git-range-diff")))
], ["Ancestry, date order, patch equivalence and content equality are different.", "log A...B is symmetric; diff A...B compares the base to B.", "A reproducible test turns bisect into evidence."], "history")

lesson("collaboration", "GitHub pull requests & team integration", 30,
 "Connect local Git habits to reviews, checks, merge methods and clear collaboration.",
 ["Understand repositories, forks, pull requests and review roles.", "Choose a consistent integration method.", "Write a useful handoff and improve practical skills."], [
section("workflow", "From issue to reviewed integration",
 flow([("Issue / plan", "Agree on scope and acceptance"),("Feature branch", "Small coherent commits"),("Pull request", "Head branch proposes changes to a base"),("Review + checks", "People inspect intent; automation tests it"),("Merge + observe", "Integrate, verify and clean up")]) +
 """<p>A pull request is a discussion and proposed integration between a head branch and a base branch. Opening one does not merge it. A draft signals that feedback is welcome but review is not yet ready. A fork lets a contributor propose changes without direct write access to the parent repository, subject to visibility and forking policies.</p>
 <p>Issues track work; branches hold references; pull requests review changes; releases describe published versions. A Git tag and a GitHub release are related but separate objects. GitHub Actions can run checks or deployments, but merging alone does not guarantee a deployment happened.</p>"""),
section("open-pr", "Open, update and finish a pull request",
 """<ol class="checklist"><li>Fetch the intended base. With a clean working tree, create your feature branch from the inspected base, for example <code>git switch -c feature/login-fix origin/main</code>.</li><li>Make a focused change, test it, inspect staged content and commit. Push with <code>git push -u origin feature/login-fix</code>.</li><li>On GitHub, use the proposed Compare &amp; pull request link, or Pull requests → New pull request. Verify both <strong>base repository/branch</strong> and <strong>head repository/branch</strong>.</li><li>Read Files changed and Commits before creating the PR. Select Draft if the work is still in progress. Add the problem, resulting behavior and validation, then request appropriate reviewers.</li><li>Push follow-up commits to the same head branch to update the PR. Inspect checks, resolve review threads with evidence, and obtain fresh review when required.</li><li>Resolve any base-branch conflicts using the team’s merge/rebase policy. Re-test the result and follow the published-history rules if a rewrite is involved.</li><li>Merge using the approved method once required gates pass. Fetch the result locally, update your clean main with <code>git merge --ff-only origin/main</code>, and verify before cleaning up the completed feature branch.</li></ol>""" +
 note("Fork contribution", "If you cannot push to the parent project, create a permitted fork, clone your fork, and add the inspected parent URL as a remote named upstream. Fetch upstream, branch from upstream/main (or the actual base), push your feature to origin, and open a PR with the parent as base and your fork as head. Permission to propose a PR is different from permission to merge it.") +
 code("git remote add upstream APPROVED_PARENT_URL\ngit fetch upstream\ngit switch -c feature/contribution upstream/main\n# Edit, test, stage and commit, then:\ngit push -u origin feature/contribution", "Fork workflow — assumes origin is your fork and main is the intended parent base") +
 """<p>GitHub’s <strong>Files changed</strong>, commit pages, and file History/Blame views complement local investigation. Preserve an exact commit link when discussing evidence: a branch URL can show different content after the branch moves. GitHub Actions shows job logs and the tested commit; a green check on a different revision is not proof that the latest change passed.</p>""" +
 source(("Create a pull request","https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request"))),
section("review", "Give the reviewer useful evidence",
 """<p>Describe the concrete problem and resulting behavior. Include the relevant tests, screenshots for UI changes, migrations, compatibility effects and a rollback plan when appropriate. Keep unrelated cleanup separate. A good review asks whether the change fulfills its requirements, handles failures and remains maintainable.</p>
 <p>Respond to comments with the implemented result or your reasoning. Do not mark unresolved behavioral concerns as solved merely to enable the merge button. New commits can invalidate approvals under team rules. Required checks may run against a commit or proposed merge result; inspect which revision was tested.</p>""" +
 table(["Merge option", "What reaches the base branch", "Team consideration"],[
 ["Create a merge commit", "Retains branch ancestry with a merge boundary.", "Useful when individual commits and the integration event matter."],
 ["Squash and merge", "One combined commit with a single parent.", "Good for one feature per PR; old feature commits are not ancestors of the squash commit."],
 ["Rebase and merge", "Linear replay of the commits onto the base.", "GitHub creates new commit IDs and updates committer information; do not equate it with every local fast-forward scenario."]]) +
 """<p>After a squash or GitHub rebase merge, start new work from updated main instead of extending the old feature branch indefinitely. Otherwise later PRs can contain surprising comparisons or require careful retargeting. The best merge method is the one your team can review, audit and recover consistently.</p>"""),
section("ownership", "Rules are part of the workflow",
 """<p>Agree who may rewrite a feature branch, who reviews sensitive code, how emergency fixes proceed, and what “done” means. Preserve shared main/release history and use reviewed corrective commits. If a contributor needs to rewrite a published personal PR branch, notify reviewers and retain enough evidence to compare the patch series.</p>
 <p>CODEOWNERS can request domain reviewers; enforcement requires a corresponding rule. A maintainer or bot’s permission is not an automatic bypass of all applicable controls. A merge queue, where available, tests integration combinations under busy traffic; required workflows need the appropriate merge-group trigger to provide checks for queue commits.</p>"""),
section("skills", "A practical skill ladder",
 table(["Stage", "Practise", "Evidence you understand it"],[
 ["Foundation", "Status, staged diff, commit, branch and fetch.", "Predict exactly what a commit will include."],
 ["Integration", "Fast-forward, three-way merge and one conflict.", "Explain base/ours/theirs and preserve both intended changes."],
 ["History", "Log ranges, blame, bisect and range-diff.", "Find a regression and show why the chosen commit is relevant."],
 ["Recovery", "Reflog, rescue branch, revert and private rebase.", "Recover a disposable mistake without overwriting unrelated work."],
 ["Collaboration", "Two-clone push races, PR review and code ownership.", "Explain why a rejected lease protects a teammate’s update."],
 ["Governance", "Least privilege, branch rules and trusted automation.", "Demonstrate that a non-bypass account is blocked and an approved PR can merge."]]) +
 """<p>Practise a short incident, then explain the graph before and after without looking at the commands. Review one real PR’s history with a teammate. Prefer small frequent changes, early integration, testable commits and a shared glossary over memorizing a long alias list.</p>""" +
 source(("Pull request merges","https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges"),("Code owners","https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners")))
], ["A PR proposes an integration; approval, checks, merge and deployment are distinct.", "Choose one understandable team merge policy.", "Skill comes from predicting and verifying state changes."], "collaboration")

lesson("github-permissions", "GitHub identity, roles & permissions", 40,
 "Understand who you authenticate as, which repository actions that identity can perform, and why a powerful token cannot grant missing access.",
 ["Distinguish authentication, authorization and branch policy.", "Choose the least repository role and credential scope for a task.", "Diagnose access failures without escalating everything to admin."], [
section("layers", "An operation passes several independent gates",
 flow([("Identity", "Which person, app or deploy key?"),("Resource access", "Can that identity reach this repo?"),("Credential scope", "Does this credential allow this operation?"),("Organization policy", "Approval, SSO, network and token restrictions"),("Branch rules", "PR, review, checks, signatures, bypass")]) +
 """<p>Authentication proves which identity is making a request. Authorization determines what that identity may do. Branch and repository rules add conditions to otherwise authorized changes. A valid token can still receive a rejection because its repository selection, permission scope or applicable policy does not allow the action.</p>
 <p>Public visibility generally permits reading published code without becoming a collaborator. It does not permit direct pushes. A private repository may appear as “not found” when the current credential lacks access. Internal visibility is an enterprise concept, not a synonym for private.</p>"""),
section("roles", "Organization repository roles",
 table(["Role", "Typical responsibility", "Important limit"],[
 ["Read", "Read code and participate in discussion/review.", "No direct code pushes."],
 ["Triage", "Manage issue/PR triage without code-writing privileges.", "Does not grant push access."],
 ["Write", "Contribute code, review and merge when rules permit.", "Not full administration or automatic rule bypass."],
 ["Maintain", "Broader repository maintenance.", "Sensitive administration is still restricted."],
 ["Admin", "Manage access and sensitive repository settings.", "Organization constraints and applicable rules still matter."]]) +
 """<p>This table describes organization-owned repositories. Personal repositories use their own owner/collaborator model. Custom roles may exist on eligible plans. An organization owner has broader organization responsibilities; a billing role is not a generic code-write role.</p>
 <p>Audit effective access from direct grants, teams and organization base permissions. Removing one team membership may not remove access granted elsewhere. Prefer team-based grants, a small admin group, appropriate base access and periodic review of outside collaborators.</p>""" +
 source(("Organization repository roles and full capability matrix","https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization"))),
section("credentials", "Choose the credential for the job",
 table(["Credential", "Typical use", "What to inspect"],[
 ["HTTPS + supported credential manager / GitHub CLI login", "Interactive developer access.", "Current account and secure credential storage; avoid credentials in remote URLs."],
 ["Personal SSH key", "Git transport as your account.", "Public key registration, agent identity and any organization SSO authorization."],
 ["Fine-grained PAT", "Scoped user automation where supported.", "Resource owner, selected repositories, permissions, expiry and required approval."],
 ["Classic PAT", "Workflows not supported by fine-grained tokens.", "Broader scopes, organization restrictions and SSO authorization; minimize exposure."],
 ["GitHub App installation token", "Installed integrations and service automation.", "Installation repository selection, app permissions and token lifetime."],
 ["Deploy key", "SSH access scoped to one repository.", "Read-only versus write-enabled; private-key holders may retain access independently of employee membership."],
 ["GITHUB_TOKEN", "A workflow job’s built-in GitHub credential.", "Workflow/job permissions, event trust and organization/repository settings."]]) +
 """<p>A PAT cannot make its owner more privileged than the owner already is. Fine-grained tokens add restrictions on top of that identity. Check current support limitations before choosing them for outside-collaborator or other specialized scenarios. Human offboarding also needs review of deploy keys, apps and automation credentials.</p>""" +
 source(("Personal access token controls and limitations","https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens"),("SSH authentication","https://docs.github.com/en/authentication/connecting-to-github-with-ssh"))),
section("grant", "A deliberate access-grant procedure",
 """<ol class="checklist"><li>Identify the specific repository, environment and operation: read, push a feature branch, triage, administer, or deploy.</li><li>Grant the least role through an appropriate team or scoped collaborator invitation. Check existing base and inherited access.</li><li>Choose a supported credential mechanism. For a fine-grained token, choose the correct resource owner and selected repositories.</li><li>Grant the operation’s required permission. Ordinary Git writes need suitable Contents access; modifying workflow files can require Workflows permission (or the classic workflow scope).</li><li>Set a suitable expiration and complete organization approval/SSO requirements where applicable.</li><li>Test an allowed operation and an intentionally denied operation using a non-admin account.</li><li>Record an owner, review date and revocation path for automation credentials.</li></ol>
 <p>Do not copy a PAT into shell history, source code, a remote URL, screenshots or chat. Prefer a supported secure credential store. If a credential is exposed, revoke or rotate it promptly; deleting its visible text is not sufficient.</p>"""),
section("diagnose", "A permission failure is a clue, not a reason for admin",
 table(["Symptom", "Inspect first"],[
 ["Authentication failed / Permission denied (publickey)", "Credential validity, transport, selected SSH key and which account it authenticates."],
 ["Repository not found", "Owner/repo spelling, account identity, private-repo access, selected token repositories."],
 ["403 / resource not accessible", "Token permission, app installation access, organization approval/SSO/IP rules and endpoint requirements."],
 ["Push blocked with GH013/GH006 or policy detail", "The named repository/branch rule, required PR/checks/signatures and bypass eligibility."],
 ["Cannot update .github/workflows", "Workflow-specific credential permission as well as Contents write and branch rules."],
 ["UI can view repo but terminal cannot", "The browser session and terminal credential may represent different identities."]]) +
 """<p>Read the server’s specific error. A missing credential permission is different from a branch rule intentionally blocking direct pushes. The visual permission lab lets you vary these gates without changing any actual account.</p>""")
], ["Identity, repository role, credential scope and rules are distinct gates.", "A token restricts the owner’s access; it does not create extra authority.", "Grant the narrowest access and verify both allowed and denied actions."], "github-permissions")

lesson("rules", "Set team rules and enforce them", 40,
 "Turn team expectations into repository controls that can be tested, explained and maintained.",
 ["Define a practical branch and review policy.", "Create and verify a ruleset with intentional bypass behavior.", "Avoid configurations that block every legitimate merge or silently allow direct updates."], [
section("policy", "Write the human agreement first",
 table(["Area", "Example baseline", "Why it matters"],[
 ["main and release branches", "Changes arrive through reviewed PRs; no ordinary force pushes or deletion.", "Keeps shared history and release references dependable."],
 ["Reviews", "Require an appropriate reviewer count and domain review for sensitive paths.", "Distributes knowledge and checks intent."],
 ["Checks", "Require named, relevant CI checks for the exact revision/integration being merged.", "Prevents a green result for the wrong work from being mistaken for validation."],
 ["Merge method", "Choose squash, rebase or merge commit consistently with history rules.", "Makes debugging and recovery predictable."],
 ["Feature history", "Rewriting only with branch-owner coordination; explicit lease for published rewrites.", "Protects collaborators’ unreviewed work."],
 ["Emergency changes", "A small named bypass group, recorded reason, rapid follow-up review.", "Makes an exception accountable instead of routine."],
 ["Secrets and automation", "Least-privilege credentials, no secrets in Git, trusted workflows for privileged actions.", "Limits the impact of mistakes and untrusted contributions."]]) +
 """<p>These are a sample team policy, not Git defaults. Store the agreed expectations in CONTRIBUTING or an equivalent handbook. Local aliases and hooks can help developers, but enforcement of a shared branch belongs on the server because local hooks can be absent or bypassed.</p>"""),
section("configure", "Configure a branch ruleset on GitHub",
 """<ol class="checklist"><li>Use a repository where you have admin or an applicable custom rule-management permission. Confirm the feature is available for its visibility and plan.</li><li>Open repository <strong>Settings</strong>, locate <strong>Rulesets</strong>, and choose a new branch ruleset. Interface grouping may vary.</li><li>Name the policy, choose its enforcement status and target the actual default/release branches. Inspect the matching branches.</li><li>Specify bypass actors and whether bypass is restricted to pull requests, where supported. Avoid a broad, undocumented escape route.</li><li>Choose PR requirements, review/check requirements, blocked force pushes and protected deletion as your policy requires.</li><li>Save, inspect the effective rules, and test with an ordinary contributor rather than only an admin/bypass account.</li></ol>
 <p>Rulesets can overlap with other rulesets and existing branch protection. Applicable restrictions are evaluated together; a permissive rule does not necessarily cancel a stricter one. Active rules enforce; disabled rules do not. Evaluation modes, where offered, report impact without enforcing. Confirm the actual mode rather than assuming a saved policy is blocking updates.</p>""" +
 source(("Create a repository ruleset","https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository"),("Layering and availability","https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets"))),
section("choices", "Settings with easy-to-miss consequences",
 table(["Setting", "Consequence to think through"],[
 ["Require linear history", "Merge commits are disallowed on the target; allow squash/rebase integration methods instead."],
 ["Require branch to be up to date", "A base-branch update can require integration and fresh checks; consider a merge queue for busy repositories where available."],
 ["Dismiss stale approvals / require latest-push approval", "New changes can require fresh human review; understand whose approval counts."],
 ["Require code-owner review", "Needs valid owners with appropriate access and a matching CODEOWNERS file on the PR base branch."],
 ["Restrict updates", "Can block updates except for bypass actors; it is not merely another name for requiring PRs."],
 ["Required checks", "Choose stable, unambiguous job/check names and appropriate trusted sources. A check that never runs can leave merges pending."],
 ["Require signed commits", "Onboard developers and bots, and check the selected merge workflow’s signature behavior."],
 ["Branch patterns", "Pattern syntax is not a shell glob copied blindly: a single * does not cross / in GitHub’s fnmatch matching. Verify actual branch matches."]]) +
 source(("Available rules and their semantics","https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets"))),
section("owners", "CODEOWNERS routes review; it does not grant access",
 code("""# Example only: replace these with real teams that have repository access.
* @example-org/maintainers
/src/auth/ @example-org/security
/.github/ @example-org/platform
/.github/CODEOWNERS @example-org/maintainers""", "Example .github/CODEOWNERS — not installed by this course") +
 """<p>GitHub uses the CODEOWNERS file from the pull request’s base branch. Later matching patterns take precedence, so order matters. Valid owners need the necessary repository access. The file requests ownership review; required code-owner approval must be enabled through the relevant rule. Ownership is not filesystem protection and does not make someone an administrator.</p>
 <p>Protect changes to the ownership file and workflow definitions themselves. Check GitHub’s displayed errors and requested reviewers with a sample PR rather than trusting that a text file is syntactically correct.</p>""" +
 source(("CODEOWNERS matching and enforcement","https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners"))),
section("verify", "Test the policy as a product feature",
 """<ol class="checklist"><li>Attempt a direct update to the protected test branch as an ordinary contributor; verify the intended rejection.</li><li>Open a small PR and observe required reviews, checks and ownership requests.</li><li>Push another change and confirm the approval/check freshness behavior.</li><li>Make a required check fail, then pass, and confirm the merge gate follows the correct revision.</li><li>Test the documented emergency path in a safe repository and record who can use it.</li><li>Review inherited organization rules, service-account access and policy drift periodically.</li></ol>
 <p>The course includes an <a href="examples/team-policy.md">adaptable policy checklist</a>. It is a planning document; no GitHub settings are changed by opening it.</p>""")
], ["Write the team agreement, then enforce and test it.", "Ruleset mode, branch targets and bypass actors are part of the policy.", "Local hooks and CODEOWNERS alone do not enforce every required rule."], "rules")

lesson("security-automation", "Secrets, signatures & GitHub automation", 35,
 "Keep credentials out of history, separate trusted automation from untrusted contributions, and understand what verification proves.",
 ["Respond correctly to a committed secret.", "Scope workflow tokens and protect privileged execution.", "Distinguish signed commits, successful tests and trustworthy code."], [
section("secret", "A secret in Git requires credential action",
 flow([("Revoke / rotate", "Invalidate the exposed credential"),("Assess", "Identify usage, scope and exposure"),("Coordinate cleanup", "History, refs, forks, clones and caches"),("Prevent repeat", "Templates, scanning and secure stores")]) +
 """<p>Deleting a secret from the latest file does not remove it from earlier commits. Even rewriting and force-pushing history cannot erase copies in other clones, forks, pull-request references or caches. Revoke or rotate first; then follow the provider’s incident process and GitHub’s sensitive-data removal guidance.</p>
 <p>History cleanup with tools such as git-filter-repo changes commit IDs and disrupts collaborators. Plan repository backups that do not expose the secret further, coordinate replacement references and downstream clones, and involve GitHub Support where the documented cleanup process requires it. Do not promise that a single reset or force push makes a leaked token safe.</p>""" +
 source(("GitHub sensitive-data removal procedure","https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository"))),
section("workflow", "Workflow permissions belong to the job",
 code("""# Excerpt from a GitHub Actions workflow, not a complete workflow.
permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    # Add reviewed checkout and test steps here.""", "Least-privilege workflow excerpt") +
 """<p><code>GITHUB_TOKEN</code> is provided for workflow jobs. Its effective permissions depend on repository/organization defaults, explicit workflow or job declarations, and event context. Specify only the permissions needed by each job. Giving the whole workflow write access because one release job needs it widens exposure unnecessarily.</p>
 <p>When explicitly declaring permissions, unspecified permissions are generally set to none, with the documented metadata exception. A job that needs issue comments, package publishing or deployments should receive only the corresponding access. Prefer short-lived app or OIDC-based cloud credentials where appropriate rather than a long-lived human PAT stored as a broad automation secret.</p>""" +
 source(("GITHUB_TOKEN authentication and permissions","https://docs.github.com/en/actions/tutorials/authenticate-with-github_token"),("Workflow syntax","https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax"))),
section("trust", "Do not execute untrusted code with privileged credentials",
 """<p>Fork pull requests are untrusted input. Normal fork-PR workflows usually have restricted tokens and no ordinary repository secrets; repository settings can affect exceptions. <code>pull_request_target</code> runs in a trusted base-repository context. Fetching or checking out the contributor’s code and then running its tests/install scripts there can expose secrets or write access.</p>
 <p>A build step, dependency install, configuration file or downloaded artifact can execute code. The risk is not limited to an obvious shell command in the PR. Keep untrusted validation separate from privileged release or labeling operations, and validate data passed between them. Follow current Actions event policies and security guidance rather than relying on an old template.</p>
 <p>Pin third-party actions to reviewed full commit IDs and use a controlled update process. Treat PR titles, branch names and issue bodies as data; do not splice them directly into shell scripts. Use expression-safe environment passing and quoted shell variables. Protect workflow changes with appropriate review.</p>""" +
 source(("Secure use of Actions","https://docs.github.com/en/actions/reference/security/secure-use"),("pull_request_target trust boundaries","https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target"))),
section("signing", "What a signature proves—and what it does not",
 """<p>A signed commit or tag binds an object to a signing key and allows verification according to the verifier’s trust rules. The author name/email fields alone are not proof of authorship. GitHub’s verification display depends on its supported signature types, identity association and policy.</p>
 <p>A verified signature does not prove the code is correct, reviewed, malware-free or approved for deployment. Keep tests and human review. Rebase/amend changes objects, so an old signature cannot remain valid for a different replacement commit; sign replacements if the policy requires it.</p>""" +
 code("git log --show-signature -1\ngit verify-commit COMMIT\ngit verify-tag TAG", "Inspection — requires a signed object and correctly configured verification") +
 """<p>Onboard signing keys and recovery/revocation procedures before enforcing signing across a team. Account 2FA, SSH authentication keys, signing keys and token scopes are related controls but serve different purposes.</p>""" +
 source(("Commit signature verification","https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification")))
], ["Rotate exposed credentials before considering history cleanup.", "Untrusted code must not inherit privileged workflow secrets or write tokens.", "A valid signature is evidence about an object and key, not proof of correctness."], "security-automation")

lesson("advanced", "Advanced workflows you will encounter", 35,
 "Recognize the tools for moving selected changes, parallel work, large repositories and repeated conflict resolution.",
 ["Choose cherry-pick, worktree, tags and rerere deliberately.", "Understand submodules, LFS, shallow clones and sparse checkouts.", "Know which advanced operations need extra coordination."], [
section("cherry", "Cherry-pick one change, not a whole branch",
 code("git show COMMIT\ngit switch release/maintenance\ngit cherry-pick -x COMMIT\n# Resolve and stage conflicts, then git cherry-pick --continue.\n# Or git cherry-pick --abort to stop.") +
 """<p>Cherry-pick applies a selected commit’s change to the current branch and generally creates a new commit ID. <code>-x</code> records the source commit reference for traceability. Verify dependencies: a fix may rely on earlier refactoring, a schema change or a test helper absent from the release branch.</p>
 <p>Cherry-picking a merge commit requires a chosen mainline and careful interpretation. Repeatedly cherry-picking a whole development stream creates duplicated patch identities and confusing ancestry. Use it for focused backports with tests rather than as a substitute for an integration policy.</p>"""),
section("worktree", "Parallel checkouts without a stash shuffle",
 code("git worktree add ../project-hotfix -b hotfix/login origin/main\ngit worktree list\n# Work, commit and review in the separate directory.\n# After it is clean and no longer needed:\ngit worktree remove ../project-hotfix") +
 """<p>Linked worktrees share one repository’s object database and references while having separate working directories and index/HEAD state. They are useful for an urgent fix while a feature checkout is dirty. Git normally prevents checking out the same branch in two worktrees to avoid competing updates.</p>
 <p>Each directory may need its own dependencies, build outputs and environment. Remove a worktree through Git when possible; do not assume deleting a directory also cleans its metadata. Inspect <code>worktree list</code> when branch deletion or checkout reports that a branch is in use.</p>"""),
section("rerere", "Reuse a resolution, then verify it",
 code("git config --local rerere.enabled true\ngit rerere status\ngit rerere diff") +
 """<p>Rerere records how a conflict was resolved and can reuse that resolution when a similar conflict reappears. This helps repeated integrations and rebases, but it can repeat a bad decision too. Inspect the result, decide when it should be staged, and run tests. <code>rerere.autoupdate</code> changes whether the index is updated automatically; understand that extra behavior before enabling it.</p>
 <p><code>git merge -X ours</code> favors our side for conflicting hunks while retaining nonconflicting changes from the other side. <code>git merge -s ours</code> records ancestry while keeping the current tree and ignoring the other tree’s content. They are very different. Neither should be a habitual way to avoid understanding conflicts.</p>"""),
section("scale", "Repository size and dependency boundaries",
 table(["Feature", "What it does", "Common pitfall"],[
 ["Submodule", "The parent records a commit ID for another repository plus configuration.", "Changing parent pointers does not automatically publish the submodule commit. Use documented initialization/update steps and ensure the referenced commit is reachable."],
 ["Git LFS", "Git records pointers while large objects are stored separately.", "A clone may have pointer text if LFS objects were not fetched; access and quota are separate concerns."],
 ["Shallow clone", "Downloads limited history depth.", "Blame, merge-base and range operations may lack needed ancestors; fetch deeper or unshallow when appropriate."],
 ["Partial clone", "Defers some objects until needed.", "Some operations need network access to retrieve missing objects."],
 ["Sparse checkout", "Limits which tracked paths appear in a working directory.", "Hidden paths are not deleted from the repository; tooling must handle the selected view."],
 ["Attributes", "Define line endings, merge/diff handling and other path behavior.", "Mass renormalization can create noisy diffs; coordinate and separate it from functional changes."]]) +
 code("* text=auto\n*.sh text eol=lf\n*.png binary", "Small .gitattributes example — adapt and review before normalizing existing files") +
 """<p>For a repository with existing line-ending policy, do not introduce <code>git add --renormalize .</code> casually. Preview, review the full diff and coordinate platform/tool behavior. Case-only filename changes can also require special care on case-insensitive filesystems.</p>"""),
section("release", "Release references and maintenance",
 code("git tag -a v1.2.0 -m 'Release 1.2.0'\ngit show v1.2.0\ngit push origin v1.2.0", "Example release workflow — use only the team-approved version and release commit") +
 """<p>Tags are not sent by every ordinary branch push; push the intended release tag explicitly. Avoid moving published tags: build systems and people may have cached the old value. A GitHub release adds release notes and assets around a tag; it does not itself prove that an artifact was built from that exact commit.</p>
 <p>For large history cleanup, use supported dedicated tooling and a coordinated migration. For an “unrelated histories” error, first check repository identity and remote selection; <code>--allow-unrelated-histories</code> is for an intentional combination of independent projects, not a routine push fix.</p>""" +
 source(("Cherry-pick","https://git-scm.com/docs/git-cherry-pick"),("Worktrees","https://git-scm.com/docs/git-worktree"),("Rerere","https://git-scm.com/docs/git-rerere"),("Submodules","https://git-scm.com/docs/git-submodule"),("Attributes","https://git-scm.com/docs/gitattributes")))
], ["Cherry-pick moves a selected patch; worktree gives another checkout.", "Reused resolutions still need review and testing.", "Large-repo and dependency features introduce their own fetch and ownership boundaries."], "advanced")

from practice_content import ISSUES, LABS

def issues_html():
    return ''.join('<details class="issue" id="' + id + '" data-category="' + category + '"><summary><span class="chip">' + category + '</span> ' + escape(title) + '</summary><h3>Likely cause</h3><p>' + escape(cause) + '</p><h3>Gather evidence</h3><p>' + escape(inspect) + '</p><h3>Resolve deliberately</h3><p>' + escape(fix) + '</p><h3>Verify the outcome</h3><p>' + escape(verify) + '</p><a href="' + topic + '.html">Review the related lesson →</a></details>' for id,category,title,cause,inspect,fix,verify,topic in ISSUES)

def labs_html():
    output=''
    for lab in LABS:
        output+='<article class="lab" id="' + lab['id'] + '"><p class="eyebrow">Disposable local repository · ' + lab['directory'] + '</p><h3>' + lab['title'] + '</h3><p><b>Outcome:</b> ' + lab['goal'] + '</p><p>After creating the fixtures, open a terminal in <code>YOUR_LAB_ROOT/' + lab['directory'] + '</code>. Read every comment before running the next command.</p>' + code(lab['commands'], 'Real Git lab — expected failures are part of the exercise')
        output+='<h4>Observe and check off yourself</h4>' + ''.join('<label class="lab-step"><input type="checkbox" data-lab="' + lab['id'] + '-' + str(i) + '">' + step + '</label>' for i,step in enumerate(lab['steps']))
        output+='<details class="reveal"><summary>Explain why this happens</summary><div><p>' + lab['why'] + '</p></div></details><p><b>Verify:</b> ' + lab['verify'] + '</p><p><b>If something differs:</b> ' + lab['problem'] + '</p><a href="' + lab['topic'] + '.html">Revisit the concept →</a></article>'
    return output

COMMANDS=[
("daily-workflow","Inspect repository state","git status","Read the operation in progress, branch and all change categories."),
("foundations","See unstaged changes","git diff","Working tree compared with index; untracked file contents are not shown."),
("foundations","Review the next commit","git diff --staged","Index compared with HEAD."),
("daily-workflow","Stage selected hunks","git add -p -- path","Read each hunk; later edits are not automatically restaged."),
("daily-workflow","Record a coherent change","git commit -m 'Describe behavior'","The commit records the index, not every file on disk."),
("branches-remotes","Start a feature branch","git switch -c feature/name","Check the starting commit and working tree first."),
("branches-remotes","Refresh remote knowledge","git fetch origin","Does not integrate remote changes into your current branch."),
("branches-remotes","Require fast-forward pull","git pull --ff-only","Refusal means inspect divergence, not remove the guard."),
("branches-remotes","Inspect tracking relationships","git branch -vv","Ahead/behind compares local tracking refs; fetch for current evidence."),
("branches-remotes","Push and set upstream","git push -u origin feature","Confirm the intended branch and remote."),
("history","Read the commit graph","git log --graph --oneline --decorate --all","Walks reachable local refs, not every historical object everywhere."),
("merge","Find a common merge base","git merge-base main feature","Complex histories can have more than one best base."),
("merge","Fast-forward only","git merge --ff-only feature","Current tip must be an ancestor of the incoming tip."),
("merge","Record a merge boundary","git merge --no-ff feature","Creates a merge commit when integration is needed."),
("merge","Prepare a squash integration","git merge --squash feature","Review and commit separately; source ancestry is not a merge parent."),
("conflicts","List unresolved paths","git diff --name-only --diff-filter=U","An empty result is necessary but not a correctness proof."),
("conflicts","Inspect unmerged index stages","git ls-files -u","Stages may be absent for add/add or delete/modify cases."),
("conflicts","Read the base version","git show :1:path","Stage 1 is the common-base content where present."),
("conflicts","Read the ours version","git show :2:path","During rebase this is the new-base/rebased-so-far side."),
("conflicts","Read the theirs version","git show :3:path","During rebase this is the original commit being replayed."),
("conflicts","Continue a resolved merge","git merge --continue","Stage the intended result and test before continuing."),
("conflicts","Abort a merge in progress","git merge --abort","Unrelated dirty work can complicate exact restoration."),
("rebase","Replay a feature onto main","git rebase origin/main","Work on a clean branch and keep a recovery reference."),
("rebase","See the current replayed patch","git rebase --show-current-patch","Useful when a rebase stops at a conflict."),
("rebase","Continue a resolved rebase step","git rebase --continue","Later commits may conflict again."),
("rebase","Restore the pre-rebase branch state","git rebase --abort","Different from --quit, which leaves the current state."),
("history","Compare old and new patch series","git range-diff OLD_BASE..old-tip NEW_BASE..new-tip","Use correct boundaries; inspect unmatched and changed patches."),
("force-push","Pin a lease to an expected remote tip","git push --force-with-lease=refs/heads/feature:EXPECTED origin HEAD:refs/heads/feature","Replace EXPECTED with the reviewed full ID. Server rules still apply."),
("force-push","Push to an explicit branch destination","git push origin HEAD:refs/heads/feature","Explicit destination reduces ambiguity; it does not validate content."),
("undo-recovery","Find local reference movements","git reflog --date=iso","Local and expiring, not a server-wide durable backup."),
("undo-recovery","Protect a recovered committed tip","git branch rescue/work COMMIT","Inspect the commit first; a branch does not save uncommitted files."),
("undo-recovery","Undo a public change with new history","git revert COMMIT","An inverse patch can conflict and needs tests."),
("undo-recovery","Move tip while retaining index and files","git reset --soft TARGET","Private-history operation; current branch/HEAD moves."),
("undo-recovery","Move tip and reset index, retain files","git reset --mixed TARGET","Changes become unstaged. Path-form reset has different semantics."),
("undo-recovery","Overwrite tracked state at a target","git reset --hard TARGET","Destructive; preserve important work and inspect the exact target."),
("undo-recovery","Unstage a path","git restore --staged -- path","Keeps working-file edits while restoring index content from HEAD."),
("undo-recovery","Discard unstaged tracked edits","git restore -- path","Overwrites the working file from the index. Save needed edits first."),
("undo-recovery","Stash including untracked files","git stash push -u -m 'Explain WIP'","Ignored files are not included by -u."),
("undo-recovery","Inspect a saved stash","git stash show -p 'stash@{0}'","Confirm which entry it is before applying or dropping it."),
("history","Follow a file through detected renames","git log --follow -- path","One path; rename following is heuristic."),
("history","Find a line’s last modifying commit","git blame -L 20,40 -- path","Read the commit and surrounding context rather than assigning blame."),
("history","Search for an occurrence-count change","git log -S 'text' -- path","Use -G for regex matches in added/removed patch lines."),
("history","Automate a regression search","git bisect run ./test-regression.sh","0 is good; 125 skips untestable revisions. End with bisect reset."),
("advanced","Backport one reviewed change","git cherry-pick -x COMMIT","New context normally creates a new ID; verify dependencies."),
("advanced","Create a parallel checkout","git worktree add ../hotfix -b hotfix main","Separate files/index; shared objects and refs."),
("advanced","Create an annotated release tag","git tag -a v1.2.0 -m 'Release 1.2.0'","Coordinate the version and push the intended tag explicitly."),
("daily-workflow","Find which ignore rule matched","git check-ignore -v -- path","Ignore rules do not automatically untrack existing files."),
("foundations","Find where a config value came from","git config --show-origin --get user.email","Repository-local settings may override global settings."),
]

lesson("troubleshooting","The development incident clinic",40,
 "Thirty common Git and GitHub problems, organized by symptom, evidence, correction and a result you can verify.",
 ["Classify history, working-tree, conflict, access and policy failures.", "Use targeted recovery rather than broad destructive commands.", "Document the cause and verified outcome."],[
section("method","Start with evidence",
 flow([("Context","Repo, branch, remote, operation"),("State","Tracked, staged, unstaged, untracked"),("History","Local graph and fetched remote graph"),("Access","Identity, credential and rule response"),("Correction","Smallest action that preserves intent")]) +
 code("git status\ngit branch -vv\ngit log --graph --oneline --decorate --all -20\ngit diff\ngit diff --staged") +
 """<p>For a remote problem, record the exact server error with credentials redacted. For local data loss, stop and preserve evidence before cleanup. An error message is not a complete diagnosis: “rejected” can mean ancestry, access or policy.</p>"""),
section("cases","Find your symptom",
 '<div class="filters only-js"><label class="field">Search symptoms and fixes<input id="issue-search" type="search" placeholder="force, stash, permissions, conflict…"></label><label class="field">Category<select id="issue-category"><option value="all">All categories</option>' +
 ''.join('<option>' + c + '</option>' for c in sorted(set(i[1] for i in ISSUES))) +
 '</select></label></div><p class="meta" id="issue-count" aria-live="polite">30 troubleshooting cases</p><div id="issues">' + issues_html() + '</div><p class="empty" id="issue-empty" hidden>No matching cases. Try “push”, “history” or “access”.</p>'),
section("handoff","Write the useful incident handoff",
 """<p>Record the repository and branch, operation attempted, relevant old/new IDs, the observed failure, what was preserved, the correction and how you verified it. Include downstream impact on teammates, CI or releases. Avoid including tokens, private keys or unnecessarily sensitive code.</p>
 <p>When the same issue repeats, improve the workflow: smaller changes, clearer branch ownership, better checks, stable formatting policy, documented credential setup, or an enforced server rule. A rescue command solves one incident; a better development habit reduces the next one.</p>""")
],["Read the exact failure and inspect the relevant layer.","Preserve recoverable work before changing more state.","Verify the outcome and improve the process that caused the incident."],"troubleshooting")

lesson("practice","Twelve real Git labs",75,
 "Practise staging, integration, conflicts, leases and recovery in disposable repositories, with expected failures and concrete verification.",
 ["Create local-only fixtures without touching an existing repository.", "Complete twelve exercises and explain their state changes.", "Distinguish observed terminal results from self-reported checklist progress."],[
section("setup","Create a fresh practice area",
 """<p>You need Python 3 and Git 2.28+ for the fixture builder. Run it from the documentation repository root, choosing a <strong>new</strong> destination directory. The builder refuses to overwrite an existing directory. It creates local repositories and one local bare remote; no network credentials or GitHub access are used.</p>""" +
 code("python3 git/examples/create-labs.py /tmp/git-learning-first-run") +
 """<p>Alternatively download <a href="examples/create-labs.py" download>create-labs.py</a> and run it with a new destination path. Each lab below names its subdirectory. Commands contain intentional failure points and editor steps: do not paste an entire lab as an unattended script.</p>
 <p>The builder uses local learner identity and isolates inherited Git configuration during setup. Normal commands you run afterward still have your environment; if signing, hooks or editors change behavior, inspect configuration rather than altering your global settings unnecessarily. The generated repos configure signing off and hooks disabled locally for reproducible practice.</p>""" +
 note("Learning checklist, not automatic machine verification","Check a box only after observing the result in your terminal. The site cannot read your filesystem. Browser exercises on the next page are separate, explicitly limited simulations.") +
 '<p id="lab-progress" class="meta" aria-live="polite"></p><progress id="lab-meter" max="1" value="0" aria-label="Self-reported lab steps"></progress>'),
section("labs","Observe, predict, execute, verify",labs_html()),
section("finish","Finish without losing work",
 """<p>The repositories live only under your chosen lab root, including the local bare remote and both Alice/Bob clones. Keep the directory if you want to inspect later. To start over, create a different new directory; the builder will not reset an existing exercise in place.</p>
 <p>Before deleting a lab root through your normal file manager, confirm it contains only disposable work you created for this course. Never copy the lab’s reset/restore cleanup into an unrelated work repository. The full exercises take several hours; the module estimate covers a first guided pass.</p>""")
],["Use a fresh local fixture for every risky experiment.","An expected rejection or conflict is evidence, not a failed lesson.","Explain the graph and content after each operation."])

lesson("playground","Visual history and decision labs",35,
 "Step through history changes, resolve a three-way conflict, simulate a lease race and diagnose a permissions gate.",
 ["Predict merge, rebase, squash, revert, reset and fetch effects.", "Resolve combined intent instead of accepting a whole side.", "Explain why a push or a permission decision is accepted or rejected."],[
section("scope","A model you can inspect",
 """<p>These tools are simulations. They do not run Git, access a repository, authenticate to GitHub or change server settings. Labels such as A, B and C stand for commit IDs; actual objects have content-derived IDs. The model intentionally focuses on a few important rules. Use the real labs and full manuals for command behavior.</p>"""),
section("history-explorer","1 · Step through the commit graph",
 '<div id="graph-explorer" class="visual-tool"></div><noscript><p>Read the static before-and-after graphs in <a href="merge.html">merge</a>, <a href="rebase.html">rebase</a> and <a href="force-push.html">force push</a>.</p></noscript>'),
section("conflict-lab","2 · Resolve a three-way conflict",
 '<div id="conflict-tool" class="visual-tool"></div><noscript><p>Base: timeout 10 / retries 1. Main: 20 / 1. Feature: 30 / 3. Requirement: preserve timeout 20 and retries 3. Resolve to one valid JSON object and explain why neither entire side suffices.</p></noscript>'),
section("push-lab","3 · Simulate a remote update race",
 '<div id="push-tool" class="visual-tool"></div><noscript><p>The old remote tip is C; a teammate may advance it to T. Your rewritten tip is C′. Normal push rejects the rewrite. An explicit expected-C lease rejects when the live remote is T. A default tracking-based lease can be weakened if a background fetch updates your expectation to T.</p></noscript>'),
section("access-lab","4 · Diagnose the permission gates",
 '<div id="permission-tool" class="visual-tool"></div><noscript><p>A valid identity, repository access, a suitable scoped credential and satisfied applicable rules are separate requirements. Admin alone is not an automatic bypass. Review the <a href="github-permissions.html">permissions lesson</a>.</p></noscript>')
],["Changing a graph label can change reachability without erasing every object.","A valid resolution preserves the stated requirements, not just syntax.","A lease and a repository role each solve only part of a larger decision."])

from studio_content import add_studio
add_studio(lesson, section, note, table)

lesson("quiz","Scenario quiz: explain the result",35,
 "Sixty questions across fifteen topics test Git behavior, recovery, collaboration and GitHub controls, with an explanation for every choice.",
 ["Predict effects before memorizing commands.", "Review missed scenarios and revisit their source lesson.", "Distinguish current-attempt scores from practical proficiency."],[
section("assessment","Test your understanding",
 """<p>Each submitted choice stays in your current attempt until you retry missed questions or start fresh. Use topic filters for focused practice. In-lesson checks are separate practice and do not silently answer this quiz for you.</p><div id="quiz"></div><noscript><p>JavaScript adds grading and saved attempts. The complete readable question bank is below.</p></noscript><details class="reveal"><summary>Open the complete question bank for reading or printing</summary><div id="static-questions"></div></details>""")
],["Explain why a command fits the state before running it.","A high score is not a substitute for observing a real lab.","Revisit the source lesson behind every uncertain answer."])

lesson("recap","Recall cards and a skill-building plan",20,
 "Recall the right tool for the situation, review weak areas and preserve your browser-local learning progress.",
 ["Recall high-value commands and their boundaries.", "Follow a practical progression from staging to team governance.", "Back up or reset local learning data."],[
section("cards","Retrieve before revealing",
 """<p><a class="btn" href="studio.html#sprint">Start a five-minute recall round →</a></p><p>Say the command and its main risk before revealing the answer. “Know it” schedules the card for 1, 3, 7, 14 and 30 days after successive successful reviews. “Again” returns it to immediate review. Due + new cards focuses the session; All cards is available any time.</p><div id="flashcards"></div><noscript><p>Cover the command column in the <a href="reference.html">reference sheet</a> and test yourself from the task names.</p></noscript>"""),
section("plan","A two-week practice plan",
 table(["Days","Focus","Proof of progress"],[
 ["1–2","Snapshots, staging and clean commits.","Explain MM and predict staged content in lab 1."],
 ["3–4","Branches, fetch and three-way merge.","Draw the graph and explain the merge base in labs 2–3."],
 ["5–6","Conflicts and rebase.","Resolve the required 20/3 result and explain reversed sides in labs 4–5."],
 ["7","Force push and leases.","Explain why Bob’s newer tip causes rejection in lab 6."],
 ["8–9","Recovery and stash.","Recover without guessing or overwriting unrelated work in labs 7–8."],
 ["10–11","History search and selective integration.","Identify the regression and backport only the fix in labs 9–10."],
 ["12","Parallel work and public correction.","Complete worktree/revert labs without losing independent changes."],
 ["13–14","Permissions, rules and a peer walkthrough.","Describe least access, verify an allowed/denied operation in a safe repo, and review a real PR’s history."]]) +
 """<p>Spend 20–30 minutes per practice session and revisit weak topics. Say what HEAD, the index, working tree and server reference will look like before each operation. Ask a teammate to explain a different solution and compare the tradeoffs.</p>"""),
section("checks","Before integrating or rewriting",
 """<ul class="checklist"><li>Confirm repository, branch, remote and target reference.</li><li>Inspect staged, unstaged and untracked work; preserve what matters.</li><li>Fetch and inspect divergence; identify the merge base and source commits.</li><li>Know who depends on the branch and which server rules apply.</li><li>Keep an appropriate committed recovery tip and separate backups for uncommitted files.</li><li>Choose merge, rebase, revert or a lease based on the actual intent.</li><li>Review the resulting graph, content and tests, then communicate the outcome.</li></ul>"""),
section("progress","Keep your learning progress",
 """<p>Lesson completion, lab observations, quiz answers, interactive exercise completion and recall schedules are stored on this browser when storage is available. Export before switching devices or clearing data. These records are learning aids, not proof that a real repository was inspected.</p><div class="actions only-js"><button class="btn" id="export-progress">Export progress JSON</button><button class="btn" id="import-trigger">Import progress JSON</button><input id="import-progress" type="file" accept=".json,application/json" aria-label="Choose a Git learning backup" hidden><button class="btn" id="reset-progress">Reset learning progress</button></div><p id="progress-message" role="status"></p><p id="progress-summary"></p>""")
],["Retrieve, predict, observe and explain.","Recovery, collaboration and permissions are skills to practise, not just read.","Back up browser-local progress if you want to retain it."])

lesson("reference","Commands, glossary & trusted references",20,
 "Find the command by intent, understand its scope and continue into official Git and GitHub documentation.",
 ["Use the command sheet without ignoring context.", "Keep common terms distinct.", "Check version- and plan-specific details in primary sources."],[
section("commands","Task → command → consequence",
 """<p>Replace uppercase placeholders and example branch/path names with inspected values. Commands are examples, not a sequence to run. Destructive operations are included so you can recognize their scope, not as default recovery advice.</p><div class="filters only-js"><label class="field">Find a task, command or risk<input id="command-search" type="search" placeholder="lease, recover, staged, conflict…"></label><button class="btn" id="print-reference">Print reference</button></div><p id="command-count" class="meta" aria-live="polite"></p>""" +
 '<div id="command-table">' + table(["Task","Command","Remember"],[[escape(task),'<code>'+escape(cmd)+'</code>',escape(tip)] for topic,task,cmd,tip in COMMANDS]) + '</div><p class="empty" id="command-empty" hidden>No matching command. Try the incident clinic for a symptom.</p>'),
section("glossary","Terms that are easy to confuse",
 '<dl class="glossary">' + ''.join('<dt>'+a+'</dt><dd>'+b+'</dd>' for a,b in [
 ("Commit","An immutable snapshot reference plus parents, metadata and message."),
 ("Branch","A movable reference to a commit; not a copied directory."),
 ("HEAD","The current checkout reference, usually symbolic to a branch, sometimes directly to a commit."),
 ("Index","The staged snapshot and, during conflicts, unmerged entries."),
 ("Working tree","Files currently checked out on disk."),
 ("Remote","A named configuration for another repository’s URL and fetch/push behavior."),
 ("Remote-tracking reference","Your local cached observation of a remote ref, such as origin/main."),
 ("Upstream","A configured tracking relationship; also a conventional name for a fork’s parent remote."),
 ("Merge base","A best common ancestor used to understand divergence; complex histories may have several."),
 ("Fast-forward","Moving a ref to a descendant without needing a new merge commit."),
 ("Three-way merge","Combining changes using a base and two side snapshots."),
 ("Rebase","Replaying selected changes onto another base, normally creating replacement commits."),
 ("Lease","An expected-value condition on a remote ref update, not a content-preservation guarantee."),
 ("Revert","A new inverse change that preserves prior ancestry."),
 ("Reset","A family of operations that can move a tip and/or adjust index/working state, depending on mode and path form."),
 ("Reflog","A local record of ref movements, with expiration and retention limits."),
 ("Pull request","A hosted proposal to integrate one branch’s work into another with discussion and review."),
 ("Authentication","Establishing the identity making the request."),
 ("Authorization","Determining which operations that identity and credential may perform."),
 ("Ruleset","A set of server-side repository/branch/tag constraints with targets, enforcement and bypass behavior."),
 ("CODEOWNERS","A path-to-owner review-routing file; required enforcement is configured separately."),
 ("Signature","Cryptographic evidence about an object and signing key; not a code-quality guarantee.")
 ]) + '</dl>'),
section("sources","Start with these primary references",
 """<p>References were reviewed in October 2026. Git commands vary with version; GitHub features vary with plan, visibility, organization policy and Enterprise version. Use your installed <code>git help COMMAND</code> for local behavior.</p>
 <ul class="source-list">
 <li><a href="https://git-scm.com/book/en/v2">Pro Git, the official online book</a> — the best continuous companion for fundamentals, branching and internals.</li>
 <li><a href="https://git-scm.com/docs">Git command reference</a> — complete command options, edge cases and version histories.</li>
 <li><a href="https://git-scm.com/docs/git-merge">git merge</a>, <a href="https://git-scm.com/docs/git-rebase">git rebase</a>, <a href="https://git-scm.com/docs/git-push">git push</a> — integration and lease semantics.</li>
 <li><a href="https://git-scm.com/docs/git-reflog">git reflog</a>, <a href="https://git-scm.com/docs/git-reset">git reset</a>, <a href="https://git-scm.com/docs/git-revert">git revert</a> — recovery and undo boundaries.</li>
 <li><a href="https://git-scm.com/docs/git-bisect">git bisect</a> and <a href="https://git-scm.com/docs/git-range-diff">git range-diff</a> — regression investigation and patch-series review.</li>
 <li><a href="https://docs.github.com/en/pull-requests/reference/pull-request-merges">GitHub pull request merge methods</a> — platform-specific integration behavior.</li>
 <li><a href="https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization">GitHub organization repository roles</a> — full capability matrix.</li>
 <li><a href="https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens">GitHub access tokens</a> — scopes, selection, approval and current support limits.</li>
 <li><a href="https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets">Rulesets</a>, <a href="https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository">creation steps</a>, <a href="https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets">rule semantics</a> — targets, enforcement and plan availability.</li>
 <li><a href="https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners">CODEOWNERS</a> — matching, ownership and review requirements.</li>
 <li><a href="https://docs.github.com/en/actions/tutorials/authenticate-with-github_token">GITHUB_TOKEN permissions</a> and <a href="https://docs.github.com/en/actions/reference/security/secure-use">secure use of Actions</a> — automation trust boundaries.</li>
 <li><a href="https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository">Removing sensitive data</a> — revocation, cleanup limitations and coordinated recovery.</li>
 </ul><p>These original lessons synthesize practical workflows; the linked manuals are the source of complete version-specific flags and platform behavior. Start with Pro Git for a continuous narrative, then use the command manual for a precise edge case.</p>""")
],["Choose commands by intent and state, not by how often you have seen them.","Official references resolve version- and policy-specific details.","A strong workflow preserves evidence, shared intent and a recovery path."])
