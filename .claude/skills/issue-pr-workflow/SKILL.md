# Issue & PR Workflow Skill

## Purpose

Use this skill when creating a GitHub issue or opening a pull request for this
repository (`koki217/todo-api`) via Claude Code, so that issue bodies, branch
names, and PR bodies stay consistent with this repo's existing conventions.

Trigger on requests like "issueを作って", "〜のPRを作って", "この変更でPRを出して".

## Prerequisites

- `gh` CLI must be authenticated with access to `koki217/todo-api`. Verify with:
  ```bash
  gh auth status
  ```
- Run all commands from the repository root (`06_Practice/todo_api`), not the
  `AIX` root — `AIX` itself is not a git repository.
- Before creating a new issue, check for duplicates:
  ```bash
  gh issue list --repo koki217/todo-api
  ```

## Step 1 — Create the Issue

Follow the structure defined in `.github/ISSUE_TEMPLATE/` — use
`bug_report.yml`'s fields (Summary / Expected behavior / Actual behavior /
Steps to reproduce / environment info) for defects, or
`feature_request.yml`'s fields (Summary / Expected behavior / Additional
context) for new functionality. `gh issue create` doesn't render the YAML
form, so write the body as plain Markdown headings matching those field
names, and omit fields that don't apply rather than leaving placeholders.

Pick a label from the repo's existing set only if it clearly applies: `bug`,
`enhancement`, `documentation`, `question`, `good first issue`, `help wanted`,
`duplicate`, `invalid`, `wontfix`.

```bash
gh issue create --repo koki217/todo-api \
  --title "<title>" \
  --body "<body>" \
  --label "<label>"   # optional
```

Note the returned issue number — it drives the branch name in Step 2.

## Step 2 — Create the Branch

Branch names must follow the policy defined in
`.github/BRANCH_NAME_POLICY.md` (also enforced by CI via
`.github/workflows/branch-name-check.yml`). That file is the source of
truth for the exact format and allowed `type` values — read it before
naming the branch rather than relying on a summary here.

```bash
git switch main && git pull
git switch -c <type>/<issue-number>-<short-description>
```

Example: `feature/3-add-due-date-field`

## Step 3 — Implement the Change

Follow `CONTRIBUTING.md` and `.claude/CLAUDE.md`:

1. Start from the smallest testable change.
2. Add or update a test when behavior changes.
3. Keep route handlers, persistence logic, and schemas separated.
4. Run tests: `pytest -q`
5. Confirm the app still starts: `uvicorn todo_api.app:app --reload`
   (or `PYTHONPATH=src uvicorn todo_api.app:app --reload` if not installed
   editable)

Use `api-architect` for API/route design questions and `test-qa` for test
validation if the change is non-trivial.

## Step 4 — Create the Pull Request

1. Push the branch:
   ```bash
   git push -u origin <branch-name>
   ```
2. Write the PR body following `.github/PULL_REQUEST_TEMPLATE.md` (Summary /
   Related issue / Why / Changes / Validation checklist / Notes). Always link
   the issue with `Closes #<issue-number>` in the Related issue section so
   GitHub auto-closes the issue when the PR is merged into `main`. Only use a
   non-closing reference (e.g. `Related to #<issue-number>`) if the PR is
   partial work that should not close the issue on its own.
3. Open as a **draft** by default (matches existing repo practice):
   ```bash
   gh pr create --repo koki217/todo-api \
     --title "<title>" \
     --body "<body>" \
     --draft
   ```
4. Report the PR URL back to the user. Do not mark ready-for-review, request
   reviewers, or merge unless explicitly asked.

## Guardrails

- Never force-push, merge, or close issues/PRs without explicit user
  instruction — these are visible actions on a shared GitHub repo.
- Keep each issue/PR scoped to one small, reviewable change per
  `CONTRIBUTING.md`'s "Development Philosophy".
- If a request doesn't cleanly map to the branch naming policy (e.g. no
  clear issue number yet), create the issue first rather than guessing a
  branch name.
