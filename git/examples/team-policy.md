# Git and GitHub team policy worksheet

Adapt this example with the repository owners. This file is documentation; it does not configure GitHub.

## Record the agreement

- Repository and default branch:
- Release branch patterns and published tags:
- Policy owner and review date:
- Selected PR merge method:
- Required reviewers and domain owners:
- Required checks and trusted check sources:
- Supported Git version and development environment:
- Approved credential storage and automation owners:

## Everyday contributions

1. Start from an inspected, current base. Keep branches and PRs small enough to review.
2. Use focused commits and explain why a change is needed. Keep generated churn separate.
3. Inspect staged content and run relevant checks before pushing. Never commit credentials.
4. Describe the problem, final behavior, validation and material risks in the PR.
5. Treat approvals as applying to reviewed content; re-review substantive changes.
6. Resolve conflicts by checking both changes' intended behavior, then test the combined result.
7. Confirm the merged result and checks on the destination branch before deleting the feature branch.

## Shared history

- Main and release branches accept changes through the agreed PR workflow.
- Block ordinary force pushes and deletion on shared protected branches.
- Use revert for an incorrect shared change when appropriate; inspect dependencies and test.
- Rebase or amend unpublished work freely after saving a recovery point.
- Rewriting a published feature requires coordination with every collaborator.
- Inspect and record the exact expected remote tip. Preserve collaborators' commits.
- Use an explicit expected-value lease for an agreed rewrite. Stop and inspect if it fails.
- Never retry a failed lease with plain force as a reflex.
- Published release tags are stable. Coordinate any exceptional replacement.

## Server enforcement checklist

- Verify plan/visibility support and the effective organization policies.
- Target actual default/release names, testing patterns containing slashes.
- Set enforcement to Active when ready; a saved Disabled/Evaluate rule does not block updates.
- Require a PR, the agreed approval count, and the intended freshness behavior.
- Require appropriate code-owner review; validate CODEOWNERS from the PR base branch.
- Give owners the needed repository access. Protect ownership and workflow files.
- Require stable check names from intended sources, on the correct revision.
- Select merge methods compatible with linear-history rules, if enabled.
- Block force pushes and unintended deletion on shared branches.
- Specify a small bypass group, scope, incident logging and follow-up review.
- Check inherited and overlapping rules; do not infer effective policy from a single screen.

## Access and automation

- Use teams and the least sufficient role. Keep the administrator group small.
- Review direct, team, base-permission and outside-collaborator grants together.
- Give automation only the repositories and capabilities it needs.
- Set credential owners, expiration/review dates and a tested revocation route.
- Review deploy keys, app installations and service credentials during offboarding.
- Keep privileged workflows separate from execution of untrusted PR code.
- Set explicit workflow/job token permissions. Protect secrets and deployment environments.
- Rotate exposed credentials first, then follow the official history-removal procedure.

## Verify using an ordinary contributor in a safe repository

- A direct protected-branch push is rejected as intended.
- A PR with missing review or failing checks cannot merge.
- A new push triggers the intended review/check freshness requirements.
- CODEOWNERS requests the expected reviewers for sensitive paths.
- The approved integration method succeeds and records the expected commit history.
- The emergency bypass works only for the intended actors and scope.
- An underprivileged credential fails even when another access layer is sufficient.
- Document actual results and recheck after policy, plan or automation changes.

## When an incident happens

Record repository, branch, operation, status, intended outcome, relevant commit IDs,
exact redacted error, and whether other people pulled or pushed the history.
Preserve committed tips with rescue branches and copy important uncommitted content
before destructive recovery. Do not paste tokens or credential-bearing remote URLs.
Agree on recovery, validate the resulting tree and ancestry, and share the final
branch state with affected contributors.

References: [Git push](https://git-scm.com/docs/git-push),
[GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets),
[GitHub repository roles](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization).
