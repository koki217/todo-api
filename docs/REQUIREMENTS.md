# TODO API 要件整理

## 1. 目的

個人開発として、最小構成の TODO 管理 API を作成する。

- `POST` で TODO を保存する
- `GET` で TODO 一覧を取得する
- TODO の状態をより実務寄りに管理できるようにする

## 2. スコープ

### MVP

- TODO 作成
- TODO 一覧取得
- TODO 完了状態更新
- TODO 削除
- SQLite 永続化
- ローカル起動確認

### 拡張要件

- TODO に以下の項目を追加する
  - `title`
  - `detail`
  - `created_by`
  - `status`
  - `created_at`
  - `updated_at`
- `status` は次の 4 種類のみ許可する
  - `未着手`
  - `進行中`
  - `完了`
  - `保留`

### 非対象

- 認証
- ユーザー管理
- 外部サービス連携
- 高度な権限管理

## 3. データモデル

`TODO` は以下の属性を保持する。

- `id`: 自動採番される一意の識別子
- `title`: TODO の件名
- `detail`: TODO の詳細説明
- `created_by`: 起票者
- `status`: TODO の状態
- `done`: 完了判定（`status = 完了` の場合に `true`）
- `created_at`: 作成日時
- `updated_at`: 更新日時

## 4. API 仕様

### 4.1 TODO 作成

- `POST /api/todos`
- リクエストボディ
  - `title`: 必須
  - `detail`: 必須
  - `created_by`: 必須
  - `status`: 任意、既定値は `未着手`

### 4.2 TODO 一覧取得

- `GET /api/todos`
- 作成日時の新しい順で取得する

### 4.3 TODO ステータス更新

- `PATCH /api/todos/{todo_id}`
- リクエストボディ
  - `status`: 必須
- `status` には `未着手 / 進行中 / 完了 / 保留` のいずれかを指定する
- `done` フラグは API では扱わず、`status` の値で完了状態を表す

### 4.4 TODO 削除

- `DELETE /api/todos/{todo_id}`
- 削除成功時は `204 No Content` を返す

## 5. 受け入れ条件

1. `POST /api/todos` で TODO を保存できる
2. `GET /api/todos` で保存済みの TODO を取得できる
3. `PATCH /api/todos/{todo_id}` で `status` を更新できる
4. `status` と `detail` と `created_by` を含めた作成ができる
5. `status` は `未着手 / 進行中 / 完了 / 保留` のいずれかのみ許容される
6. `created_at` と `updated_at` が保持される
7. `pytest` が通る
8. README と設計書が揃っている
