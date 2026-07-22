# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.2.0] - 2026-07-22

### Added

- GitHub Issue Forms (`bug_report.yml` / `feature_request.yml`) replacing the
  single generic issue template
- Milestones (`v0.1.0`, `v0.2.0`, `v0.3.0`) grouping issues by release phase
- A public GitHub Projects board tracking issue status
- This CHANGELOG
- README: architecture diagram, development flow diagram, and links to the
  auto-generated API reference (Swagger UI `/docs`, ReDoc `/redoc`)

### Changed

- Updated dependencies via Dependabot: `fastapi`, `pytest`, `httpx`,
  `pydantic`, `uvicorn`, and the `actions/checkout`, `actions/setup-python`,
  `softprops/action-gh-release` GitHub Actions

### Fixed

- Dependabot-created branches no longer fail `branch-name-check` (they are
  now exempt from the repo's branch naming policy, which they cannot follow)
- Replaced the deprecated `HTTP_422_UNPROCESSABLE_ENTITY` constant with
  `HTTP_422_UNPROCESSABLE_CONTENT`

## [0.1.0] - 2026-07-22

### Added

- Core TODO CRUD API: create, list, update status, delete
- Search, sort, and pagination on `GET /api/todos` (`q`, `status`, `sort`,
  `order`, `limit`, `offset`)
- CI workflows: test execution (pytest), lint (Ruff), branch name validation
- Dependabot configuration for weekly dependency updates
- A `Release` workflow that creates a GitHub Release with auto-generated
  notes when a `v*` tag is pushed
- README badges for CI status, license, and supported Python version
- Repository operating docs: `CONTRIBUTING.md`, `BRANCH_NAME_POLICY.md`,
  issue/PR templates, and a Claude Code `issue-pr-workflow` skill

### Changed

- Unified error response format across validation errors (422) and business
  errors (404, etc.) to `{"detail": <string>, "errors": <list|null>}`
- PRs now close their linked issue automatically via `Closes #<issue-number>`
- Consolidated branch naming rules into `BRANCH_NAME_POLICY.md` as the single
  source of truth

### Removed

- Unused `done` column from the `todos` table (completion state is derived
  from `status`)
