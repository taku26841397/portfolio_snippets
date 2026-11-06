# Oracle Cloud デプロイ手順

## SSH接続

```bash
ssh snippet
```

---

## Django更新

```bash
cd ~/apps/portfolio_snippets

git pull
```

---

## 仮想環境

```bash
source venv/bin/activate
```

---

## Pythonパッケージ追加時

```bash
pip install パッケージ名

pip freeze > requirements.txt
```

---

## PostgreSQL

接続

```bash
sudo -u postgres psql
```

終了

```sql
\q
```

---

## Gunicorn

状態確認

```bash
sudo systemctl status gunicorn
```

再起動

```bash
sudo systemctl restart gunicorn
```

### 使うタイミング

- settings.py変更
- Pythonコード変更
- ALLOWED_HOSTS変更
- MEDIA設定変更
- requirements変更

---

## Nginx

状態確認

```bash
sudo systemctl status nginx
```

設定確認

```bash
sudo nginx -t
```

再起動

```bash
sudo systemctl restart nginx
```

### 使うタイミング

- server_name変更
- SSL設定変更
- static設定変更
- media設定変更
- location設定変更

---

## Static

収集

```bash
python manage.py collectstatic
```

設定

```nginx
location /static/ {
    alias /home/ubuntu/apps/portfolio_snippets/staticfiles/;
}
```

---

## Media

Django

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

Nginx

```nginx
location /media/ {
    alias /home/ubuntu/apps/portfolio_snippets/media/;
}
```

---

## SSL

証明書確認

```bash
sudo certbot certificates
```

更新確認

```bash
sudo certbot renew --dry-run
```

---

## ドメイン

```text
snippets.taku-archive.dev
```

Aレコード

```text
151.145.74.184
```

---

## 本番URL

```text
https://snippets.taku-archive.dev
```

---

## トラブルシューティング

### CSSが表示されない

```bash
curl -I https://snippets.taku-archive.dev/static/admin/css/base.css
```

### 画像が表示されない

```bash
curl -I https://snippets.taku-archive.dev/media/xxxx.jpg
```

### Gunicornログ

```bash
sudo journalctl -u gunicorn -n 100
```

### Nginxログ

```bash
sudo tail -100 /var/log/nginx/error.log
```

---

## デプロイ後の定番コマンド

```bash
git pull

source venv/bin/activate

python manage.py collectstatic --noinput

sudo systemctl restart gunicorn
sudo systemctl restart nginx
```