# TODO API 設計書（詳細版）

## 1. エンドポイント

- `POST /api/todos`
- `GET /api/todos`
- `PATCH /api/todos/{id}`
- `DELETE /api/todos/{id}`

## 2. DB

SQLite の `todos` テーブルを利用し、以下のカラムを予定する。

- `id`
- `title`
- `detail`
- `created_by`
- `status`
- `created_at`
- `updated_at`

## 2.1. GET /api/todos クエリパラメータ

- `q`: `title` / `detail` の部分一致検索
- `status`: ステータスの完全一致フィルタ
- `sort`: `id` / `title` / `created_at` / `updated_at`（デフォルト `created_at`）
- `order`: `asc` / `desc`（デフォルト `desc`）
- `limit`: 1〜100（デフォルト `100`）
- `offset`: 0以上（デフォルト `0`）

## 3. レスポンス方針

- JSON を返す
- エラー時は `detail` を返す
- ステータスコードを明示する
- `done` フラグは使わず、`status` の値で完了状態を表す
