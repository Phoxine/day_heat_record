# Quickstart: 每日熱量記錄 Web App

## Prerequisites

- Docker
- Docker Compose

## Environment

建立 `.env`，可從 `.env.example` 複製：

```bash
cp .env.example .env
```

必要設定：

```text
DJANGO_SECRET_KEY=dev-secret-key
DJANGO_DEBUG=1
POSTGRES_DB=day_heat_record
POSTGRES_USER=day_heat_record
POSTGRES_PASSWORD=day_heat_record
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

## Start Services

```bash
docker compose up --build
```

服務：

- `web`: Django app
- `db`: PostgreSQL

## Database Setup

```bash
docker compose exec web python manage.py migrate
```

## Run Tests

```bash
docker compose exec web python manage.py test
```

## Manual Verification

1. 開啟首頁。
2. 建立個人資料：名字、身高、體重、年齡。
3. 在今天的早餐、午餐、晚餐各新增一筆食物與熱量。
4. 確認每個餐別小計與當日總熱量正確。
5. 切換到另一個日期並新增記錄，確認不同日期資料不混合。
6. 修改與刪除餐點，確認小計與總計更新。
7. 前往統計頁，確認最近 7 天與最近 30 天統計正確。

## Verification Results

2026-05-06 已完成以下驗證：

- `docker compose build`：通過。
- `docker compose up -d db`：通過，PostgreSQL service 顯示 healthy。
- `docker compose up -d web`：通過，Django service 映射到 `http://localhost:8000`。
- `docker compose exec web python manage.py migrate`：通過，已套用 admin、auth、calories、contenttypes、sessions migrations。
- `docker compose exec web python manage.py test`：通過，14 個測試全部成功。
- `python3 -m py_compile ...`：通過，主要 Python 檔案語法檢查成功。
