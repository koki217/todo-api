# Branch Naming Policy

このリポジトリでは、ブランチ名は以下の形式に統一します。

`<type>/<issue-number>-<short-description>`

## ルール

- 小文字のみを使用する
- 単語の区切りは `-` を使う
- `type` は以下のいずれかにする
  - `feature`
  - `fix`
  - `docs`
  - `chore`
  - `refactor`
- `issue-number` は GitHub issue 番号を入れる
- `short-description` は短い説明を英語で記載する
- スペースや大文字、アンダースコアは使わない

## 例

- `feature/1-add-search-pagination`
- `fix/2-fix-status-update`
- `docs/3-update-readme`
- `chore/4-update-ci-config`
- `refactor/5-clean-api-structure`

## 例外

- Dependabot が自動生成するブランチ(`dependabot/pip/...`、
  `dependabot/github_actions/...`)はこの命名規則の対象外とする。
  Dependabot側でブランチ名を本ポリシーに合わせることはできないため、
  `.github/workflows/branch-name-check.yml` で `dependabot/` から始まる
  ブランチはチェック自体をスキップする。

## 目的

- PR のレビュー対象が把握しやすい
- issue 番号と branch を紐づけやすい
- GitHub 上での運用を一貫させる
