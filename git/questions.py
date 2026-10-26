"""Scenario questions; every option includes a reason."""
QUESTIONS=[]
def q(topic,prompt,right,wrong1,wrong2):
    choices=[right,wrong1,wrong2]
    shift=len(QUESTIONS)%3
    choices=choices[shift:]+choices[:shift]
    QUESTIONS.append(dict(id="q"+str(len(QUESTIONS)+1),topic=topic,prompt=prompt,
        options=[dict(text=t,why=w) for t,w in choices],correct=(3-shift)%3))

q("foundations","You stage version A of a file, edit it to B, then run ordinary git commit. What is recorded?",
 ("Version A from the index","Commit records the staged snapshot. Later unstaged edits remain in the working tree."),
 ("Version B because it is on disk","The working file is not automatically restaged at commit time."),
 ("Both versions as two commits","One commit is created from one index snapshot; Git does not invent a second commit."))
q("foundations","What is a branch in Git?",
 ("A movable reference to a commit","Its tip moves as commits are recorded or references are deliberately updated."),
 ("An independent full copy of all project files","Branches share objects; a separate working directory is a different concept."),
 ("A permanently fixed label","Published tags are conventionally stable; a branch is designed to move."))
q("foundations","You amend only the commit message. Why does the commit ID change?",
 ("The message is part of the commit object","Amend creates a replacement object, even if its tree content is unchanged."),
 ("Git renames the original object in place","Existing content-addressed objects are not edited in place."),
 ("The server must have changed the files","Amend is local and does not require a server."))
q("foundations","Setting user.email to a teammate’s GitHub address gives you what?",
 ("Commit metadata, not their repository permissions","Authentication and authorization are independent of author-name/email fields."),
 ("Their GitHub write permission","A metadata string cannot authenticate as that account."),
 ("A verified cryptographic signature","A signature requires a signing key and verification, not merely an email field."))

q("daily-workflow","What should you inspect to review the next ordinary commit’s content?",
 ("git diff --staged","It compares the index with HEAD, showing the staged changes."),
 ("Only git diff","That normally shows unstaged changes, which may differ from the proposed commit."),
 ("Only the latest remote commit","Remote history does not reveal your local staged snapshot."))
q("daily-workflow","A tracked .env file was added to .gitignore. Why does Git still show modifications?",
 ("Ignore rules do not untrack existing paths","Remove it from tracking deliberately and handle any historically exposed credentials separately."),
 ("The ignore file must always be global","Repository ignore rules work for eligible untracked files; scope is not the issue."),
 ("A force push is required for ignore rules","Force push moves a remote reference; it does not change tracked-file semantics."))
q("daily-workflow","Your working directory mixes an urgent fix with an unrelated experiment. What is a useful next step?",
 ("Stage selected paths/hunks and inspect the staged diff","A coherent commit lets the reviewer and future debugger understand one change."),
 ("Stage everything because commits are always harmless","Broad staging can publish unintended code, files or secrets."),
 ("Hide the experiment by changing the commit message","The message cannot remove unwanted content from the index."))
q("daily-workflow","A switch would overwrite your uncommitted work. What should you do first?",
 ("Preserve and inspect the work, or use another worktree","Commit, reviewed stash or a separate checkout avoids losing the original edits."),
 ("Use reset --hard immediately","That can discard the very work Git is protecting."),
 ("Delete the branch you are switching to","Deleting a branch does not safely resolve the working-tree conflict."))

q("branches-remotes","origin/feature says you are up to date. Does that guarantee the live server has no new commits?",
 ("No; the remote-tracking ref may be stale","Fetch before using it as current evidence of the server’s state."),
 ("Yes; it is a live network pointer","It is a local reference updated by operations such as fetch."),
 ("Yes, if the branch has an upstream","Upstream configuration names a comparison target; it does not continuously query the server."))
q("branches-remotes","What does git fetch normally do to your checked-out branch?",
 ("It updates remote information without integrating into that branch","It retrieves objects and updates refs according to fetch configuration."),
 ("It automatically rebases your local commits","Rebase is a separate integration step or configured pull behavior."),
 ("It discards all unstaged files","Fetch does not normally overwrite the checked-out working files."))
q("branches-remotes","Why might git pull --ff-only refuse after fetching?",
 ("The branches diverged and cannot be integrated only by moving the tip","Inspect and choose merge or rebase deliberately."),
 ("The only solution is a force push","A rejected local integration does not authorize replacing remote history."),
 ("The repository must be recloned","Divergence is ordinary Git state, not evidence of corruption."))
q("branches-remotes","What does normal git fetch --prune remove?",
 ("Stale local tracking refs covered by the fetch refspec","It cleans your cached view of deleted remote refs; tag behavior needs separate configuration awareness."),
 ("Every teammate’s inactive branch on the server","Pruning tracking refs is not a server-branch deletion command."),
 ("Your uncommitted source changes","Those belong to the working tree and index, not stale tracking refs."))

q("merge","When is a fast-forward possible?",
 ("The current target tip is an ancestor of the incoming tip","The branch can move to the descendant without creating a merge commit."),
 ("The incoming branch has a later timestamp","Ancestry, not date order, determines fast-forward eligibility."),
 ("Both branches have the same name","Names do not prove an ancestry relationship."))
q("merge","Which three snapshots matter in a simple three-way merge?",
 ("Common base, current side and incoming side","The base explains what each side changed independently."),
 ("Working tree, remote URL and GitHub account","Those are useful context, but not the three snapshots in the merge algorithm."),
 ("The three most recent commits by date","Date ordering is not how the common ancestor and tips are selected."))
q("merge","A merge reports no conflicts. What have you learned?",
 ("Git found a textual combination, but behavior still needs testing","Different files or nonoverlapping edits can introduce semantic incompatibility."),
 ("The combined application must be correct","Automatic textual integration is not an application proof."),
 ("Both branches’ tests were automatically run","Git merge does not automatically supply your project’s test strategy."))
q("merge","After a squash commit, are the original feature commits necessarily ancestors of main?",
 ("No; the squash records combined content with a different parent relationship","The source branch ancestry is not preserved as a merge parent."),
 ("Yes, because all their lines are present","Content inclusion and commit reachability are different."),
 ("Only if you delete the feature branch","Deleting a reference does not change existing commit parents."))

q("conflicts","During rebase, which side is normally called ours?",
 ("The new base plus commits already replayed","The original commit currently being replayed is the theirs side."),
 ("Always your original feature tip","That shortcut is wrong during a rebase and can discard the intended changes."),
 ("Always the live GitHub branch","These labels describe local operation state, not a live server query."))
q("conflicts","Your editor offers Accept both for conflicting JSON values. What should you do?",
 ("Construct one valid result that satisfies both intended requirements","Concatenation can create invalid JSON or duplicate contradictory keys."),
 ("Always accept both because it cannot lose information","Keeping text does not ensure valid structure or correct behavior."),
 ("Choose the side with the newest timestamp","Intent and context, not timestamps, determine the resolution."))
q("conflicts","What does git add do to a manually resolved conflict?",
 ("Records your chosen resolution in the index","It marks the path resolved; you must still review and test it."),
 ("Proves the application now works","Staging does not perform behavioral verification."),
 ("Automatically resumes every paused operation","Merge, rebase, cherry-pick and revert have operation-specific continuation."))
q("conflicts","A delete/modify conflict appears. What is the correct general response?",
 ("Decide whether the final design needs the file, then stage deletion or retained content","A delete/modify conflict is a product decision, not merely a marker cleanup."),
 ("Always retain the file to avoid losing any lines","That can undo an intentional deletion and leave obsolete behavior."),
 ("Always delete it because deletion has priority","Git needs your resolution precisely because the intent is not mechanically settled."))

q("rebase","Rebasing feature onto main changes which branch in the normal workflow?",
 ("The feature branch being replayed","Main supplies the new base; rebase does not automatically move main."),
 ("Main always moves to feature","That is a different integration operation."),
 ("Every remote copy of feature immediately","Rebase is local until a separate server update is performed."))
q("rebase","A rebase stops on a conflict in the second commit. What does --skip do?",
 ("Omits that commit’s replayed change","Use it only when the change is verified redundant or deliberately unwanted."),
 ("Automatically combines both sides correctly","Skip avoids applying a commit; it does not solve its intent."),
 ("Keeps the same patch but ignores the error message","Dropping a replay is a real history/content decision."))
q("rebase","Why keep a backup tip and use range-diff after a rebase?",
 ("To compare the old and new patch series and inspect changed or omitted work","This supports review and recovery, but tests are still needed."),
 ("To preserve the old commit IDs on the rebased branch","New parents require new objects; the backup retains the old line separately."),
 ("To make force-pushing shared main automatically safe","A backup does not grant permission or protect every collaborator."))
q("rebase","What is a key difference between rebase --abort and --quit?",
 ("Abort attempts to restore the pre-rebase state; quit leaves the current state","Choose based on the actual operation and desired recovery."),
 ("They always do exactly the same thing","The distinction matters when HEAD/index/working files are mid-replay."),
 ("Quit publishes the partial history to GitHub","Neither command inherently pushes to a remote."))

q("force-push","What does an accepted force push principally change?",
 ("The targeted remote reference","Old objects may remain elsewhere, but the branch may stop reaching teammates’ commits."),
 ("Every clone’s working directory immediately","Clones retain their own state until separate local operations occur."),
 ("All old object copies everywhere","Force push is not global erasure or a secret-revocation mechanism."))
q("force-push","Why is an explicit --force-with-lease=ref:EXPECTED useful?",
 ("It requires the live remote tip to match the pinned object ID","It detects concurrent tip changes regardless of a later tracking-ref update."),
 ("It proves every known teammate change is preserved","A lease checks identity, not whether your proposed tree/history retains intended content."),
 ("It bypasses GitHub rules and permissions","Server authorization and rules still apply."))
q("force-push","Your editor fetched a teammate’s new commit in the background. What can happen with a default lease?",
 ("Its tracking-based expectation may advance without your review","An unqualified lease can accept replacing that newly observed tip; pin the reviewed expectation."),
 ("It automatically rebases your local work onto the teammate’s commit","Fetch updates tracking information, not your branch’s content."),
 ("It becomes stricter than every explicit lease","Its safety depends on what the tracking ref now represents."))
q("force-push","An explicit lease was rejected. What should you do?",
 ("Inspect the new remote commits and account for them before retrying","Refreshing the expected ID without preserving work defeats the reason for the rejection."),
 ("Add --force to keep the lease but silence the error","Force disables the lease protection rather than preserving it."),
 ("Assume the new remote commit is disposable","Only collaboration and content inspection establish that."))

q("undo-recovery","Which operation usually undoes a public bad change while preserving shared ancestry?",
 ("git revert","It records a new inverse change; resolve conflicts and test the resulting behavior."),
 ("reset --hard followed by force push","That rewrites the shared reference and can disrupt collaborators."),
 ("Deleting the local branch name","A local reference deletion does not correct published behavior."))
q("undo-recovery","You found a missing committed tip in reflog. What is a useful first recovery action?",
 ("Inspect it and create a rescue branch at that ID","A named reference protects the candidate before more state changes."),
 ("Immediately reset every branch to HEAD@{1}","The entry may not be the right one, and broad movement can damage other work."),
 ("Run garbage collection to remove ambiguity","Unreachable-object cleanup can reduce recovery options."))
q("undo-recovery","Can reflog reliably recover a never-tracked file removed by a cleanup command?",
 ("No; Git may never have recorded its contents","Use external backups or editor/filesystem recovery where available."),
 ("Yes, reflog stores every working-tree byte","Reflog records ref movements, not continuous filesystem snapshots."),
 ("Yes, if the filename existed in .gitignore","Ignore rules do not store file contents."))
q("undo-recovery","A stash application conflicts. Which statement is correct?",
 ("The stash can remain, and there is no stash --abort command","Preserve pre-existing work and resolve or recover deliberately."),
 ("All conflicts mean the stash was permanently deleted","A failed pop/application normally retains the saved entry."),
 ("reset --hard is always safe here","There may be unrelated uncommitted work that must be preserved first."))

q("history","How does git diff A...B differ from git log A...B?",
 ("Diff compares merge-base to B; log selects the symmetric difference","Dot syntax must be interpreted in the command’s context."),
 ("Both show exactly the same unordered set of files","Log selects commits; diff compares snapshots."),
 ("Diff always compares B back to A","The three-dot comparison is based on the merge base and is asymmetric."))
q("history","A blame entry names a developer. What does it establish?",
 ("The selected line’s last modifying commit under that blame calculation","Read the commit and context; formatting and moves can affect attribution."),
 ("Who caused every present-day bug involving that line","Responsibility and current behavior require more evidence."),
 ("Who originally designed the entire subsystem","Blame is line-oriented history, not an architecture ownership record."))
q("history","A bisect revision cannot build because a historical dependency is unavailable. How should it be classified?",
 ("As untestable when appropriate, using skip/exit 125","Do not confuse an environment failure with the regression you are searching for."),
 ("Always bad","That can identify an irrelevant commit as the regression source."),
 ("Always good","Lack of a test result does not establish correct behavior."))
q("history","What question does git log -S 'text' help answer?",
 ("Which changes altered the occurrence count of that text?","Use -G for matching added/removed lines by regex; inspect the relevant path/range."),
 ("Which commits have signed metadata?","Signature inspection uses different commands/options."),
 ("Which remote has the fastest connection?","This is a history search, not a transport measurement."))

q("collaboration","A pull request is approved but a required test failed. Is it ready to merge?",
 ("Not under a policy requiring that check to pass","Human review and automated checks are independent evidence."),
 ("Yes; one approval bypasses all checks","Approvals do not automatically override repository rules."),
 ("Yes; Git has already merged it when the PR opened","Opening a PR proposes changes; it does not itself integrate them."))
q("collaboration","After squash-merging a feature, where should ordinary new work usually start?",
 ("From the updated base branch on a new feature branch","The old feature IDs were not preserved as main’s ancestors; endless reuse can complicate later comparisons."),
 ("Always continue the old feature branch without inspecting main","That can carry old ancestry into future PRs."),
 ("From a detached release tag without a branch","That may lose a convenient reference to new work and use the wrong base."))
q("collaboration","What is a good reason to include range-diff after rewriting a PR branch?",
 ("It helps reviewers compare the old and new patch series","Reviewers can focus on conflict resolutions, omissions and changes introduced during the rewrite."),
 ("It prevents anyone from requesting more review","A comparison is evidence, not an override of review policy."),
 ("It guarantees unchanged runtime behavior","Patch comparison still needs contextual review and tests."))
q("collaboration","Which practice most improves practical Git skill?",
 ("Predict state changes, execute in a disposable repo, then verify the graph and content","This builds a transferable mental model rather than a fragile command memory."),
 ("Memorize destructive aliases without reading their expansion","That hides important scope and side effects."),
 ("Avoid ever reading a diff because CI covers everything","CI cannot replace review of intent, secrets and unintended changes."))

q("github-permissions","A Read-only user creates a PAT with broad requested scopes. Can it give them repository Write access?",
 ("No; a user token cannot exceed the owner’s access","Scopes further constrain identity capabilities; they do not grant missing repository roles."),
 ("Yes; token scope always overrides the account role","Authorization layers do not work that way."),
 ("Only if the author email matches an admin","Commit metadata does not grant access."))
q("github-permissions","Who normally needs code push capability without full sensitive administration?",
 ("A contributor with Write access, subject to rules","Grant only the task’s needed repository role and credential permissions."),
 ("Everyone must be an organization owner","That greatly exceeds normal contribution needs."),
 ("Triage grants the same code-writing capability","Triage manages collaboration items without ordinary push privilege."))
q("github-permissions","The browser can view a private repo but terminal Git says not found. What should you check?",
 ("Whether the terminal credential is the same identity and has that repo selected","Browser sessions and CLI/SSH credentials can represent different accounts."),
 ("Whether you should force push","Force changes history rules, not private-repository visibility."),
 ("Whether setting user.name to the repo owner fixes it","Author metadata is not authentication."))
q("github-permissions","Removing an employee from a team is enough to revoke every automation credential they possessed. True?",
 ("No; review other grants, deploy keys and app/automation access too","Effective access and standalone credentials may have additional ownership/lifecycle paths."),
 ("Yes; team membership is the only access source","Direct, base and other team grants can remain."),
 ("Yes; every deploy key automatically belongs to that team member","Deploy keys are repository credentials, not simply a reflection of current team membership."))

q("rules","A CODEOWNERS file exists. Are code-owner approvals automatically required to merge?",
 ("No; enable the relevant required-review policy too","The file routes ownership; enforcement is a separate repository rule."),
 ("Yes; the file is a universal merge lock","Ownership declarations alone do not enforce every review requirement."),
 ("Only if every owner has Admin","Appropriate code-owner access is needed, but universal admin is not the solution."))
q("rules","You require linear history but allow only merge-commit integration. What is wrong?",
 ("The policies conflict; allow a compatible squash or rebase method","Linear history rejects merge commits on the protected target."),
 ("Linear history means newest timestamps first","It is about parent/merge structure, not display order."),
 ("Nothing; a merge commit always has one parent","A usual merge commit has two parents."))
q("rules","Why test rules using a non-bypass contributor?",
 ("An admin or configured bypass actor may not experience the intended restrictions","A saved setting is not proof that normal contributors are gated correctly."),
 ("Only read-only accounts can see rule outcomes","Ordinary writers are the relevant test for contribution restrictions."),
 ("Bypass actors never affect enforcement behavior","Bypass is precisely an explicit exception that needs review."))
q("rules","A required check is forever pending for merge-queue commits. What is a plausible cause?",
 ("The workflow does not report the required check for the merge-group event","Inspect exact event, job/check name and trusted source."),
 ("Every pending check should be removed from the ruleset immediately","Removing the gate without diagnosis can weaken intended protection."),
 ("The branch must always be force-pushed","History replacement does not fix an absent workflow event."))

q("security-automation","A token was committed and then deleted in a later commit. What is the first security action?",
 ("Revoke or rotate the exposed token","Old commits and external copies may still contain it; visibility cleanup does not invalidate credentials."),
 ("Assume it is safe because HEAD no longer contains it","History and copied data outlive the latest file state."),
 ("Force push and keep using the same token","A force update cannot guarantee removal from every copy."))
q("security-automation","What is dangerous about checking out fork PR code in a privileged pull_request_target job and running its build?",
 ("Untrusted code can execute with the trusted job’s secrets or write capability","Build/install/configuration steps can run attacker-controlled behavior."),
 ("The commit graph becomes automatically circular","The security issue is execution trust, not graph structure."),
 ("It only changes the appearance of the review page","It can affect repository and external-service access."))
q("security-automation","What does a verified commit signature establish?",
 ("Evidence about the object and a signing key under the verifier’s policy","It does not replace review or prove functional correctness."),
 ("All required tests passed","Test results are separate evidence."),
 ("The code can never contain a vulnerability","A valid signer can still make mistakes or sign harmful code."))
q("security-automation","Only the release job needs package publishing. How should workflow permissions be designed?",
 ("Grant that capability narrowly to the job that needs it","Minimize credentials available to other jobs, especially untrusted validation."),
 ("Give every job all write permissions","That increases impact without serving the test jobs’ needs."),
 ("Put a human admin PAT in every step","A broad long-lived human credential is usually unnecessary and risky."))

q("advanced","A cherry-picked commit has a new ID. Is that unexpected?",
 ("No; applying the patch in another parent context creates a new commit","Inspect dependencies and test the new context."),
 ("Yes; cherry-pick always moves the original object without changing parents","The operation normally creates a replacement application of the change."),
 ("Yes; it proves the file content was corrupted","Object identity depends on more than file content."))
q("advanced","What does a linked worktree provide?",
 ("Another working directory/index while sharing repository objects and refs","It is useful for parallel tasks without overwriting the first checkout’s files."),
 ("A separate GitHub organization","A worktree is a local Git structure."),
 ("A security sandbox for running untrusted code","It does not isolate permissions or execution privileges."))
q("advanced","Why review a rerere-reused resolution?",
 ("It may repeat an incorrect or contextually outdated decision","Reusing text is not a correctness proof."),
 ("Because rerere can never reproduce any previous result","Reuse is its purpose; contextual correctness is the remaining question."),
 ("Because it always force-pushes automatically","Rerere does not inherently publish repository changes."))
q("advanced","How does merge -s ours differ from merge -X ours?",
 ("-s ours keeps our tree while recording ancestry; -X ours favors ours in conflicting hunks","The latter can still incorporate the other side’s nonconflicting changes."),
 ("They are interchangeable spellings","Their different effects can silently discard intended work."),
 ("Both guarantee a valid combined application","Neither strategy replaces an intent-based review and tests."))

q("troubleshooting","Git reports index.lock exists. What is the correct first response?",
 ("Check whether an active Git process is using the repository","Only a confirmed stale lock should be removed; concurrent writers can corrupt intended state."),
 ("Delete every lock file immediately","The lock may be protecting an active operation."),
 ("Force push to release the lock","A remote update does not resolve a local index writer."))
q("troubleshooting","A clean merge made the application fail. What kind of problem may this be?",
 ("A semantic conflict","The text combined mechanically while assumptions or interfaces became incompatible."),
 ("Proof that every conflict must have visible markers","Markers only represent unresolved textual decisions."),
 ("A reason to accept ours for every future merge","That discards changes and avoids rather than fixes the underlying issue."))
q("troubleshooting","After reverting a merge, merging the same old branch does not restore its change. Why?",
 ("The original merge ancestry remains recorded","Revert changed content; plan new corrective commits or a reviewed revert of the revert."),
 ("Revert erased the entire source branch everywhere","It creates an inverse change, not global deletion."),
 ("Git ignored every future commit automatically","New descendants and their differences can still be integrated; the old ancestry explains the specific result."))
q("troubleshooting","Your clone lacks history needed for merge-base analysis. What should you inspect?",
 ("Whether it is shallow and whether the necessary refs/ancestors were fetched","Fetch appropriate depth/refs before interpreting an incomplete graph."),
 ("Whether the terminal theme is correct","Appearance does not affect available objects."),
 ("Whether a hard reset can manufacture missing ancestors","Moving a reference does not download absent history."))
