# 📝 Snippets 管理アプリ（Django / FBV / Oracle Cloud）

コードスニペット・テキストプロンプト・画像プロンプトを
カテゴリ別に整理・検索・管理できる Django アプリです。

Function-Based Views（FBV）を採用し、認証・検索・カテゴリ管理・CRUD を実装しています。

本番環境は Oracle Cloud Infrastructure（OCI）上に構築し、
Nginx・Gunicorn・PostgreSQL・Let's Encrypt を利用した構成で運用しています。

---

## 🌐 公開URL

https://snippets.taku-archive.dev

---

## 🔑 テストユーザー

動作確認用のユーザーを用意しています。

- ユーザー名: testuser
- パスワード: testpass123

---

## 🛠 使用技術

### Backend

- Python 3.x
- Django 4.x
- Function-Based Views（FBV）
- PostgreSQL
- Context Processor
- CSRF Protection
- Django Authentication
- Session Management

### Frontend

- HTML
- CSS
- Bootstrap
- レスポンシブ対応

### Infrastructure

- Oracle Cloud Infrastructure (OCI)
- Ubuntu Server
- Nginx
- Gunicorn
- PostgreSQL
- Let's Encrypt
- systemd
- GitHub

### Development

- SQLite（開発環境）
- Git
- GitHub

---

## 📌 主な機能

### ✔ スニペット管理

- スニペット登録
- スニペット編集
- スニペット削除
- スニペット詳細表示
- ページネーション付き一覧表示

### ✔ 言語管理

- 言語作成
- 言語詳細表示
- サブカテゴリ管理
- サブカテゴリ追加

### ✔ テキストプロンプト管理

- Prompt 作成
- Prompt 編集
- Prompt 削除
- Prompt 詳細表示

### ✔ 画像プロンプト管理

- Image Prompt 作成
- Image Prompt 編集
- Image Prompt 削除
- 画像アップロード
- 画像表示

### ✔ 検索機能

- Site Search
- Snippet / Prompt / ImagePrompt 横断検索

### ✔ 認証機能

- ログイン
- ログアウト
- `@login_required`
- セッション管理

---

## 🚀 本番構成

```text
Browser
↓
Nginx
↓
Gunicorn
↓
Django
↓
PostgreSQL
```

### 本番環境で実施した内容

- Oracle Cloud 上へ Ubuntu サーバーを構築
- PostgreSQL を導入
- Nginx + Gunicorn 構成へ移行
- HTTPS (Let's Encrypt) 対応
- 独自ドメイン運用
- Static ファイル配信
- Media ファイル配信
- Gunicorn の systemd 自動起動設定

---

## 🎨 UI / デザイン

- シンプルで見やすいレイアウト
- カテゴリごとの整理
- CRUD 操作を直感的に行える画面構成
- 統一感を意識したデザイン

---

## 🧩 工夫した点

### Function Based Views を採用

クラスベースビューではなく FBV を採用し、
リクエストからレスポンスまでの流れを把握しやすい構成にしています。

### カテゴリ構造の整理

Language → Category → Prompt の構造を採用し、
管理しやすいデータ設計を行いました。

### Oracle Cloud へのデプロイ

Render から Oracle Cloud へ移行し、

- Ubuntu
- PostgreSQL
- Gunicorn
- Nginx
- HTTPS

を自分で構築しました。

### 実運用を意識した構成

- 本番DBにテストユーザーを用意
- HTTPS対応
- Mediaファイル管理
- Gunicorn自動起動
- 独自ドメイン運用

---

## 📁 ディレクトリ構成

```text
snippets/
├── migrations/
├── templates/snippets/
├── static/snippets/
├── models.py
├── views.py
├── urls.py
└── context_processors.py

config/
├── settings/
│   ├── base.py
│   ├── dev.py
│   └── prod.py
├── urls.py
├── wsgi.py
└── asgi.py

media/
staticfiles/

manage.py
requirements.txt
```

---

## 📚 今後の改善予定

- GitHub Actions による自動デプロイ
- PostgreSQL バックアップ自動化
- UI改善
- タグ機能追加
- API化

---

## 📄 ライセンス

MIT License
