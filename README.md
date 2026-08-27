# 📝 Snippets 管理アプリ（Django / FBV / Render）

コードスニペットをカテゴリ別に整理・検索・管理する Django アプリです。
Function-Based Views（FBV） を採用し、処理の流れを明確化しながら
認証・カテゴリフィルタ・CRUD・本番環境デプロイまで一通り実装しています。

本番環境は Render を使用し、Whitenoise による静的ファイル配信など
実運用を意識した構成にしています。

---

## 🌐 公開 URL
https://portfolio-snippets.onrender.com

---

## 🔑 テストユーザー
動作確認用のユーザーを用意しています。

- **ユーザー名：** testuser  
- **パスワード：** testpass123  

---

## 🛠 使用技術

### Backend
- Python 3.x  
- Django 4.x  
- Django Function-Based Views（FBV） list / detail / create / update / delete 
- Context Processor（カテゴリ一覧の共通化）
- CSRF / セッション管理（7日維持）
- @login_required による認証制御

### Frontend
- HTML / CSS
- シンプルな UI / カテゴリタグによる視認性向上

### Infrastructure
- Render（デプロイ）  
- SQLite（開発環境）
- Whitenoise（静的ファイル配信）

---

## 📌 機能一覧

### ✔  スニペット管理
- スニペットの登録（snippet_add /言語固定モード（pk） / サブカテゴリ固定モード（sub_pk）
- 一覧表示（snippets_list / ページネーション対応）
- 詳細表示（snippet_detail）
- 編集（snippet_edit / サブカテゴリ変更）
- 削除（snippet_delete / 削除確認ページ）

### ✔  言語管理
- 言語詳細（language_detail / AI 言語は Prompt / ImagePrompt に切替）
- 言語追加（language_add）
- サブカテゴリ詳細（subcategory_detail）
- サブカテゴリ追加（subcategory_add）

### ✔  検索機能
- サイト内検索（site_search / Snippet・Prompt・ImagePrompt を横断検索）

### ✔ 認証機能
- ログイン / ログアウト
- @login_required によるアクセス制御



---

## 🎨 UI / デザインのポイント
- シンプルで見やすいレイアウト  
- Todo の完了状態を色分けして視認性を向上  
- CRUD 操作を直感的に行える UI  
- ログイン画面も統一感のあるデザインに調整  

---

## 🧩 工夫した点
- クラスベースビューではなく FBV を採用し、処理の流れを明確に把握できる構成にしています。 
- 関数ビューに直接 @login_required を付与することで処理の見通しを良くしています。  
- Whitenoise を使用し、追加の CDN を使わずに高速配信を実現。   
- Render へのデプロイを通じて、本番環境での動作を確認  
- 本番 DB に **testuser** を作成し、企業がすぐに動作確認できるよう配慮  

---

## 📁 ディレクトリ構成（抜粋）

```
snippets/
  ├── migrations/
  ├── templates/snippets/
  ├── static/snippets/
  ├── models.py
  ├── views.py        # CRUD（FBV）
  ├── urls.py
  └── context_processors.py

config/
  ├── settings.py
  ├── urls.py
  └── wsgi.py

manage.py
requirements.txt
```

---

## 📄 ライセンス
このプロジェクトは MIT License のもとで公開しています。
