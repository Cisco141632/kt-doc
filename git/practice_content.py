"""Problems and real exercises, with checks and final results."""
ISSUES = [('rejected-push',
  'remote',
  'Push rejected: non-fast-forward',
  'The server has work your proposed branch history does not include, or you changed commits already shared.',
  'Run git fetch origin, then git log --left-right --graph --oneline HEAD...origin/feature for the relevant '
  'branch.',
  'Read and combine the needed teammate changes, test, then push normally. For an agreed history '
  'replacement, follow the exact-ID lease lesson.',
  'Both sets of needed changes are present. The server accepts the intended update.',
  'force-push'),
 ('lease-rejected',
  'remote',
  'Force-with-lease rejected',
  'The server branch is no longer at the commit ID you expected.',
  'Fetch and compare the new last server commit with your saved expected ID.',
  'Read the new commits and agree how to keep them. Do not merely change the expected ID and repeat the same '
  'replacement.',
  'The final files keep both people’s needed work, and the shared history matches the agreement.',
  'force-push'),
 ('wrong-branch',
  'workflow',
  'I committed on the wrong branch',
  'You saved a commit while using a different branch from the one you intended.',
  'Read git status, git branch --show-current, and git show HEAD. Check whether you already pushed it.',
  'First keep the commit with git branch rescue/my-change. Then plan a private reset or a shared-history '
  'revert for the original branch.',
  'The wanted commit has a branch name and no shared work was silently replaced.',
  'undo-recovery'),
 ('detached',
  'workflow',
  'Detached HEAD',
  'HEAD points directly to a saved commit instead of naming a branch.',
  'Read git status and git log -1. Check whether you made useful new commits here.',
  'Before switching away, run git switch -c keep-my-work with an unused branch name.',
  'You are on the new branch and the needed commits are still available.',
  'foundations'),
 ('lost-reset',
  'recovery',
  'A reset or rebase made commits disappear',
  'The branch moved away from old commits. Those commits may still be stored locally.',
  'Read git reflog --date=iso. Use git show on a possible old ID to check its contents.',
  'Give the correct found commit a rescue branch name, then compare before bringing work back.',
  'The wanted saved work is available and checked. Reflog cannot promise recovery of never-stored file text.',
  'undo-recovery'),
 ('dirty-switch',
  'workflow',
  'Local changes would be overwritten',
  'Switching or merging would replace edits still in your files.',
  'Read status, git diff, git diff --staged, and any new files.',
  'Keep wanted work with a commit or a checked stash, or use a second worktree folder. Then retry.',
  'Your original edits are kept, and you understand the new starting state.',
  'daily-workflow'),
 ('unmerged',
  'conflicts',
  'You have unmerged paths',
  'An operation paused because some files still need your conflict choice.',
  'Read git status to identify the operation. Use git diff --name-only --diff-filter=U to list files.',
  'Edit the intended final files, add them, read the staged diff, test, and use the matching continue '
  'command.',
  'No unresolved files remain and the correct operation finishes.',
  'conflicts'),
 ('ours-theirs',
  'conflicts',
  'Accept current kept the wrong code',
  'The editor labels were read without checking which operation was running.',
  'Read status. Read the base and versions 2/3. During rebase, ours is the new starting work plus changes '
  'already applied.',
  'Write the result required by both changes. Do not blindly choose a whole side again.',
  'The staged file has the correct values and the combined behavior passes its tests.',
  'conflicts'),
 ('repeated-conflict',
  'conflicts',
  'Rebase conflicts again in the same file',
  'More than one commit in the rebase changes the same file.',
  'Run git rebase --show-current-patch to see the change being applied at this stop.',
  'Resolve this step’s needed change, add, check, test, and continue. Skip only a change checked as already '
  'present or unwanted.',
  'Rebase finishes and a comparison with the backup shows no accidental missing change.',
  'rebase'),
 ('stash-conflict',
  'recovery',
  'Stash pop left conflicts and still lists the stash',
  'Applying the saved edits did not finish cleanly, so the stash was kept.',
  'Read status, git stash list, and git stash show. Keep any edits that existed before applying it.',
  'Resolve and check the combined edits, or undo only the attempted application after saving earlier work. '
  'There is no stash --abort.',
  'The wanted edits are present. Drop a saved entry only after checking the result.',
  'undo-recovery'),
 ('ignored-tracked',
  'files',
  'A file in .gitignore still changes in Git',
  'Git already tracks the file. Ignore rules do not remove tracked files.',
  'Use git ls-files -- path for the actual file, and git check-ignore -v -- path where appropriate.',
  'If the file should leave tracking but stay on disk, review git rm --cached -- path and commit the '
  'removal. Handle any old secret separately.',
  'The file is no longer tracked in the new commit; required safe example settings remain.',
  'daily-workflow'),
 ('secret',
  'security',
  'A token was committed',
  'The password or token may still be in old commits or other copies.',
  'Find the credential owner, allowed actions, and signs of use without sharing its value further.',
  'Disable or replace it first. Then follow the provider’s incident steps and the GitHub old-history cleanup '
  'guide.',
  'The old credential no longer works. Record the cleanup and how you will avoid repeating it.',
  'security-automation'),
 ('no-upstream',
  'remote',
  'Current branch has no upstream',
  'Your local branch has no saved remote branch to follow.',
  'Read git branch -vv and git remote -v. Confirm the intended branch and address.',
  'For a new feature branch, use git push -u origin feature with the actual branch name. For an existing '
  'branch, set the intended tracking link.',
  'git branch -vv shows the expected remote branch. No force push is needed.',
  'branches-remotes'),
 ('not-found',
  'access',
  'Repository not found',
  'The address may be wrong or your terminal account may lack access to a private project.',
  'Check owner/project spelling, terminal account, token project selection, and organization access.',
  'Correct the address or account, or obtain the needed project grant through its owner.',
  'A read succeeds as the intended account, using a remote URL without a secret.',
  'github-permissions'),
 ('publickey',
  'access',
  'Permission denied (publickey)',
  'SSH selected a key GitHub does not recognize or does not allow for this project.',
  'Check the selected key, SSH agent, registered public key, and any required organization approval. Never '
  'print the private key.',
  'Load/register the intended key and complete required approval, or use the approved HTTPS login setup.',
  'GitHub recognizes the intended account; separately check that account’s repository access.',
  'github-permissions'),
 ('403',
  'access',
  '403 or resource not accessible',
  'The account, credential, or organization rules do not allow the action.',
  'Read the full response. Check expiry, selected project, required token permission, approval, sign-in, and '
  'network restrictions.',
  'Change only the missing access that the task needs, or complete the required approval.',
  'The intended operation succeeds while unrelated access remains limited.',
  'github-permissions'),
 ('protected',
  'rules',
  'GH013 / GH006 or protected-branch rejection',
  'A server rule is intentionally blocking this branch update.',
  'Read the GH013/GH006 message and the applicable branch rules.',
  'Use the required PR, reviews, tests, or documented emergency exception. Do not remove a rule just to '
  'silence the error.',
  'An approved change succeeds and an ordinary direct update remains blocked.',
  'rules'),
 ('workflow-scope',
  'access',
  'Cannot push a workflow-file change',
  'Changing workflow files can need a separate credential permission as well as ordinary content-write '
  'access.',
  'Read the exact error, token type, Workflows permission or classic workflow scope, and branch rules.',
  'Obtain only the required credential permission, then follow review rules.',
  'The intended workflow change succeeds without giving unrelated admin access.',
  'github-permissions'),
 ('pending-check',
  'rules',
  'A required check stays pending',
  'GitHub expects a named result that no job is reporting for this revision.',
  'Compare the exact check name/source with actual job names, events, branch/path filters, and merge_group '
  'where needed.',
  'Correct the job trigger or required check name so the intended job reports for the change being '
  'evaluated.',
  'The matching result appears on that revision and the merge condition responds to it.',
  'rules'),
 ('stale-review',
  'rules',
  'Approval vanished after another push',
  'The rules require fresh approval after the new changes.',
  'Read the latest commits and applicable review setting.',
  'Ask an eligible reviewer to read the new work. Explain what changed, using range-diff when helpful.',
  'The current version has the required fresh approval.',
  'collaboration'),
 ('line-endings',
  'files',
  'Every line appears changed',
  'A formatter or LF/CRLF line-ending conversion may have touched the whole file.',
  'Check .gitattributes, formatting settings, and a diff ignoring whitespace when helpful.',
  'Follow the team’s line-ending policy. Keep large formatting/conversion changes separate from a behavior '
  'fix.',
  'The remaining changes are intended and the file works on supported systems.',
  'advanced'),
 ('case-rename',
  'files',
  'A case-only rename is missing',
  'The file system may treat Notes.txt and notes.txt as the same name.',
  'Use git ls-files to see tracked spelling. Check the intended new file name and imports.',
  'Use git mv through an intermediate name, then the intended spelling. Read the staged rename.',
  'A clean checkout has the correct names and callers/imports on supported systems.',
  'advanced'),
 ('lockfile',
  'conflicts',
  'Package lockfile conflict',
  'Both changes affected dependency versions, or different tool versions generated the file.',
  'Read the package-list changes and required package-manager version.',
  'Resolve the package lists first, regenerate the lockfile as the project directs, then read and test the '
  'result.',
  'Installation keeps both intended dependency changes and uses the expected exact versions.',
  'conflicts'),
 ('unrelated',
  'remote',
  'Refusing to merge unrelated histories',
  'The two histories have no shared starting commit, perhaps because the wrong projects were selected.',
  'Check remote addresses and the first commits on both sides.',
  'Correct a mistaken address or clone. Use --allow-unrelated-histories only for an intended, reviewed '
  'combination of independent projects.',
  'The final history contains the projects you meant to combine.',
  'advanced'),
 ('shallow',
  'history',
  'History or merge-base seems missing',
  'Your copy may include only recent history or may be missing a needed branch.',
  'Read git rev-parse --is-shallow-repository and the fetched branch configuration.',
  'Fetch the missing branch or deeper history, or unshallow when appropriate. Then repeat the comparison.',
  'The required earlier commits exist locally and the history comparison is meaningful.',
  'history'),
 ('bisect-flaky',
  'history',
  'Bisect identifies an implausible commit',
  'The test may vary between runs or may classify a setup failure as the product bug.',
  'Test the reported commit and its parent with the same setup; read git bisect log.',
  'Make the test reliable. Skip revisions that truly cannot be tested, then repeat with known good/bad '
  'results.',
  'The reported commit’s change explains a repeatable transition from working to failing.',
  'history'),
 ('reverted-merge',
  'recovery',
  'Merging again does not restore reverted work',
  'Revert changed the files but kept the old merge links in history.',
  'Read the original merge, its revert, and later changes.',
  'Plan a new correction or a reviewed revert of the revert. The same old merge alone may not restore the '
  'effect.',
  'The desired behavior returns while later useful work stays.',
  'undo-recovery'),
 ('index-lock',
  'workflow',
  'index.lock exists',
  'Another Git process may be writing, or a stopped process may have left the lock behind.',
  'Check running Git commands, open commit editors, and repository activity.',
  'Let active operations finish. Remove only a confirmed leftover lock when no process uses it; then read '
  'status.',
  'Git works normally without two processes writing at once or losing staging state.',
  'daily-workflow'),
 ('submodule',
  'files',
  'Submodule path is empty or points to the wrong version',
  'The parent records another repository’s commit, which may not be initialized, downloaded, or accessible.',
  'Read .gitmodules and git submodule status. Check access and whether that specific commit was pushed.',
  'Follow the project’s init/update steps. Make the referenced commit available in the correct repository.',
  'The parent checks out with the intended available submodule version.',
  'advanced'),
 ('lfs',
  'files',
  'A large file is only pointer text',
  'Git has the small pointer text but the separate large-file content was not downloaded.',
  'Check Git LFS installation, download results, access, and quota.',
  'Follow the project’s LFS setup/download steps. Do not replace pointer text with guessed content.',
  'The application opens the expected real file and Git keeps the correct pointer.',
  'advanced')]

LABS = [{'id': 'staging',
  'directory': '01-staging',
  'title': '1 · See the staged snapshot',
  'topic': 'daily-workflow',
  'goal': 'Prove that staged content can differ from the file currently on disk.',
  'commands': 'git status --short\n'
              'git diff\n'
              'git diff --staged\n'
              'git show :notes.txt\n'
              "git commit -m 'Record the first edit'\n"
              'git show HEAD:notes.txt\n'
              'git diff',
  'steps': ['I identify MM and explain its two columns.',
            'I predict which edit the commit will include.',
            'I confirm the second edit remains unstaged after the commit.'],
  'why': 'The practice setup staged the first edit, then changed the working file again. Commit records the '
         'staging area, not every byte currently on disk.',
  'verify': 'HEAD contains the first edit; git diff still shows the second edit.',
  'problem': 'If you ran git add again, you changed the experiment. Create a fresh practice setup root to '
             'repeat it.'},
 {'id': 'fast-forward',
  'directory': '02-fast-forward',
  'title': '2 · Fast-forward without a merge commit',
  'topic': 'merge',
  'goal': 'Move main to the existing later feature commit and count its parents.',
  'commands': 'git log --graph --oneline --all\n'
              'git merge --ff-only feature\n'
              "git show --no-patch --pretty='%h %p %s' HEAD",
  'steps': ['I identify main as an earlier commit of feature.',
            'I fast-forward and confirm main and feature point to the same commit.',
            'I confirm the last commit has one parent and no extra merge commit was made.'],
  'why': 'Feature continues from main. Moving main’s name to the existing commit is enough.',
  'verify': 'git rev-parse main and git rev-parse feature match.',
  'problem': 'If ff-only fails, check separate new commits on both sides instead of removing the guard.'},
 {'id': 'three-way',
  'directory': '03-three-way',
  'title': '3 · Combine independent changes',
  'topic': 'merge',
  'goal': 'Combine a timeout change on main and a retry change on feature.',
  'commands': 'git merge-base main feature\n'
              'git log --graph --oneline --all\n'
              'git merge feature\n'
              "git show --no-patch --pretty='%h %p %s' HEAD\n"
              'cat timeout.txt retries.txt',
  'steps': ['I identify the common base and both branch tips.',
            'I explain the base-to-each-side changes before merging.',
            'I confirm two parents and both intended values after the merge.'],
  'why': 'The two branches changed different parts of the snapshot. A new two-parent commit records the '
         'combination.',
  'verify': 'timeout.txt is 20 and retries.txt is 3; the merge has two parents.',
  'problem': 'A textually clean merge still needs a behavioral test in a real application.'},
 {'id': 'conflict',
  'directory': '04-conflict',
  'title': '4 · Resolve a real three-way conflict',
  'topic': 'conflicts',
  'goal': 'Keep the approved timeout budget of 20 and feature’s retry count of 3.',
  'commands': 'git merge feature\n'
              '# The conflict is expected. Read status and all stages:\n'
              'git status\n'
              'git show :1:config.json\n'
              'git show :2:config.json\n'
              'git show :3:config.json\n'
              '# Edit config.json to valid JSON with timeout 20 and retries 3.\n'
              'git add -- config.json\n'
              'git diff --cached\n'
              'git diff --cached --check\n'
              'git merge --continue',
  'steps': ['I check base, ours and theirs.',
            'I produce one valid JSON object that keeps the stated requirements.',
            'I stage, check, continue and confirm a two-parent merge.'],
  'why': 'Choosing either entire side loses one requirement. Accepting both may create invalid or duplicate '
         'configuration.',
  'verify': 'config.json parses to timeout=20, retries=3 and no unresolved paths remain.',
  'problem': 'Do not run continue before editing/staging. git merge --abort is the matching way to stop this '
             'operation.'},
 {'id': 'rebase',
  'directory': '05-rebase',
  'title': '5 · Rebase and interpret the reversed sides',
  'topic': 'rebase',
  'goal': 'Apply two feature changes again after main, fixing the configuration conflict when it pauses.',
  'commands': 'git branch backup/feature-before-rebase\n'
              'git rebase main\n'
              '# Conflict expected: ours is main plus already replayed work.\n'
              'git status\n'
              'git rebase --show-current-patch\n'
              'git show :2:config.json\n'
              'git show :3:config.json\n'
              '# Resolve config.json to timeout 20, retries 3, then:\n'
              'git add -- config.json\n'
              'git rebase --continue\n'
              'git log --graph --oneline --all',
  'steps': ['I give the old feature commit a backup branch name.',
            'I identify ours/theirs by reading the file contents and the change being applied.',
            'I finish both commits, verify new IDs and keep the feature notes.'],
  'why': 'The new parents create replacement commits. The second feature change should survive even after '
         'resolving the first conflict.',
  'verify': 'main is an earlier commit of feature, notes.txt exists, config has 20/3, and the backup keeps '
            'old IDs.',
  'problem': 'Rebase may stop more than once. Do not skip a change just to reach the end.'},
 {'id': 'lease',
  'directory': '06-lease/alice',
  'title': '6 · A teammate races your rewrite',
  'topic': 'force-push',
  'goal': 'See a normal push and an exact-ID lease refused by a shared local repository.',
  'commands': 'expected=$(cat ../expected-tip.txt)\n'
              'git log --graph --oneline --all\n'
              'git push origin feature\n'
              '# Non-fast-forward rejection is expected.\n'
              'git push --force-with-lease=refs/heads/feature:"$expected" origin HEAD:refs/heads/feature\n'
              '# Lease rejection is expected. Inspect the teammate’s update:\n'
              'git fetch origin\n'
              'git log --left-right --oneline feature...origin/feature\n'
              'git show origin/feature:bob.txt',
  'steps': ['I find Alice’s replacement commit and the saved expected server ID.',
            'I observe that the stale explicit lease is rejected.',
            'I fetch and read Bob’s change before choosing how to combine the work.'],
  'why': 'The practice setup already includes a later push by Bob. Fetching updates origin/feature but does '
         'not change the saved exact expected variable.',
  'verify': 'The remote still contains bob.txt after both rejected pushes.',
  'problem': 'Do not replace the explicit lease with --force. Default leases after background fetch are '
             'explored in the browser tool.'},
 {'id': 'reflog',
  'directory': '07-reflog',
  'title': '7 · Recover a lost last saved commit',
  'topic': 'undo-recovery',
  'goal': 'Find the commit lost by an intended practice setup reset and name it safely.',
  'commands': 'git log --oneline\n'
              'git reflog --date=iso\n'
              "# Find the commit named 'Record valuable work'; inspect its ID.\n"
              'git show OLD_TIP\n'
              'git branch rescue/valuable-work OLD_TIP\n'
              'git show rescue/valuable-work:valuable.txt',
  'steps': ['I locate the reset and preceding valuable commit in reflog.',
            'I check the candidate before creating a rescue branch.',
            'I confirm the valuable file is available through a saved name again without moving main.'],
  'why': 'The old commit still exists locally and the reflog helps locate it. A rescue reference protects it '
         'before further operations.',
  'verify': 'The rescue branch contains valuable.txt; main remains at its current saved commit.',
  'problem': 'OLD_TIP is a placeholder. Do not assume HEAD@{1} after doing other operations.'},
 {'id': 'stash',
  'directory': '08-stash',
  'title': '8 · Handle a stash-application conflict',
  'topic': 'undo-recovery',
  'goal': 'See a stash kept after conflicts and recover the edits around their original starting point.',
  'commands': 'git status\n'
              'git stash list\n'
              "git stash apply 'stash@{0}'\n"
              '# Conflict expected. The fixture was clean before apply.\n'
              'git status\n'
              "git stash show -p 'stash@{0}'\n"
              '# ONLY for this fixture with no pre-existing edits: discard this attempted application.\n'
              'git restore --source=HEAD --staged --worktree -- config.json\n'
              "git stash branch rescue/stashed-work 'stash@{0}'\n"
              'git diff',
  'steps': ['I confirm the stash remains after a conflict.',
            'I distinguish a failed application from loss of the saved change.',
            'I recover on a new branch at the stash’s base and check the dirty result.'],
  'why': 'There is no stash --abort. This lab starts with clean files, so the shown targeted restore removes '
         'only this attempted application.',
  'verify': 'The rescue branch contains the intended stashed edit in its working files.',
  'problem': 'Never use the targeted restore recipe on pre-existing unsaved work without preserving it.'},
 {'id': 'bisect',
  'directory': '09-bisect',
  'title': '9 · Find a bug that appeared after working before with bisect',
  'topic': 'history',
  'goal': 'Find the commit where a file changes from the working value to the failing value.',
  'commands': 'git bisect start\n'
              'git bisect bad known-bad\n'
              'git bisect good known-good\n'
              'git bisect run sh -c \'test "$(cat value.txt)" = 0\'\n'
              'git bisect log\n'
              'git show --stat refs/bisect/bad\n'
              'git bisect reset',
  'steps': ['I understand why the test returns 0 for good and nonzero for bad.',
            'I check the identified commit and its parent.',
            'I end the bisect session and return to the original branch.'],
  'why': 'The test gives the same answer each time, so Git can keep narrowing the good-to-bad range.',
  'verify': "The first bad commit is 'Introduce regression'; its parent still contains 0. Regression means a "
            'bug that appeared after the project previously worked.',
  'problem': 'Do not mark a missing command or a setup failure as proof of the product bug.'},
 {'id': 'cherry',
  'directory': '10-cherry-pick',
  'title': '10 · Backport only the fix',
  'topic': 'advanced',
  'goal': 'Apply one bug fix without copying a later unrelated feature change.',
  'commands': 'git show fix-to-backport\n'
              'git cherry-pick -x fix-to-backport\n'
              'git log -1 --format=full\n'
              'cat bug.txt\n'
              'git ls-tree --name-only HEAD',
  'steps': ['I check the selected change and its dependencies.',
            'I apply the fix to the maintenance branch with a note of the original commit ID.',
            'I confirm the fix exists and the unrelated feature file does not.'],
  'why': 'Cherry-pick moves a patch into the current context, not all commits after a branch point.',
  'verify': 'bug.txt contains fixed; unrelated-feature.txt is absent.',
  'problem': 'A conflict or missing dependency requires a fix based on both needed changes, not blindly '
             'accepting one side.'},
 {'id': 'worktree',
  'directory': '11-worktree',
  'title': '11 · Work on a hotfix without disturbing a feature',
  'topic': 'advanced',
  'goal': 'Use a second checkout while the first has a deliberate uncommitted edit.',
  'commands': 'git status\n'
              'git worktree add ../11-hotfix -b hotfix main\n'
              'git worktree list\n'
              '# Inspect the hotfix directory; the original dirty file remains unchanged.\n'
              'git -C ../11-hotfix status\n'
              'git worktree remove ../11-hotfix\n'
              'git status',
  'steps': ['I observe the dirty change in the original directory.',
            'I create an independent clean checkout and check both contexts.',
            'I remove the clean worktree and verify the original edit remains.'],
  'why': 'Worktrees share stored commits and branch names, but keep separate files, staging, and HEAD.',
  'verify': 'The original notes.txt edit is still present after the hotfix worktree is removed.',
  'problem': 'Commit or save work in the second directory before removing a dirty worktree; do not force '
             'removal casually.'},
 {'id': 'revert',
  'directory': '12-revert',
  'title': '12 · Undo a shared change with new history',
  'topic': 'undo-recovery',
  'goal': 'Revert a bad feature flag while preserving a later documentation change.',
  'commands': 'git show bad-change\n'
              'git revert bad-change\n'
              'git log --graph --oneline --decorate\n'
              'cat flag.txt docs.txt\n'
              'git merge-base --is-ancestor bad-change HEAD',
  'steps': ['I identify the bad change and the later independent work.',
            'I create a revert commit rather than moving the branch backward.',
            'I verify the flag is off, docs remain and the bad commit is still an earlier commit.'],
  'why': 'A revert records a corrective inverse change in new history. It does not remove the old commit or '
         'undo unrelated later work.',
  'verify': 'flag.txt is off, docs.txt remains, and the command checking that the bad commit is still '
            'earlier in history succeeds.',
  'problem': 'If later edits overlap, resolve the revert conflict and use revert --continue or --abort.'}]
