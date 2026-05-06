# 每日熱量記錄 Web App

這是一個使用 Django 建立的每日熱量記錄 Web App。使用者可以建立個人資料，
依日期記錄早餐、午餐、晚餐吃了什麼與攝取熱量，並在統計頁查看近期熱量趨勢。

## 技術概要

- Backend / Frontend: Django 5.2 LTS + Django templates
- Database: PostgreSQL 16
- Data access: Django ORM
- Runtime: Docker Compose
- Services:
  - `web`: Django app
  - `db`: PostgreSQL

## 環境需求

- Docker
- Docker Compose

## 初次設定

建立本機 `.env`：

```bash
cp .env.example .env
```

`.env.example` 內已提供可供本機開發使用的預設值：

```text
DJANGO_SECRET_KEY=dev-secret-key
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
POSTGRES_DB=day_heat_record
POSTGRES_USER=day_heat_record
POSTGRES_PASSWORD=day_heat_record
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

## 啟動服務

建置並啟動所有 service：

```bash
docker compose up --build
```

背景啟動：

```bash
docker compose up -d --build
```

啟動後開啟：

```text
http://localhost:8000
```

查看 service 狀態：

```bash
docker compose ps
```

停止服務：

```bash
docker compose down
```

## 資料庫 migrate

啟動服務後執行：

```bash
docker compose exec web python manage.py migrate
```

## 執行測試

```bash
docker compose exec web python manage.py test
```

目前測試涵蓋：

- 使用者資料與餐點資料 validation
- profile 建立與首頁導向
- 今日三餐記錄與總熱量計算
- 不同日期資料隔離
- 餐點修改與刪除
- 統計 aggregation 與統計頁空狀態

## 常用開發指令

建立 migration：

```bash
docker compose exec web python manage.py makemigrations
```

進入 Django shell：

```bash
docker compose exec web python manage.py shell
```

建立 admin 使用者：

```bash
docker compose exec web python manage.py createsuperuser
```

查看 logs：

```bash
docker compose logs -f web
docker compose logs -f db
```

## 專案結構

```text
.
├── app/
│   ├── config/                 # Django project settings / urls / wsgi / asgi
│   ├── calories/               # 熱量記錄 app
│   ├── templates/              # Django templates
│   └── static/                 # CSS
├── specs/001-calorie-record/   # Spec Kit 規格、計畫、任務與 quickstart
├── compose.yaml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## MVP 範圍

已實作：

- 單一使用者個人資料
- 依日期記錄早餐、午餐、晚餐
- 新增、修改、刪除餐點
- 餐別小計與當日總熱量
- 最近 7 天與 30 天統計
- 最高熱量日期與主要熱量來源餐別

暫不包含：

- 多使用者登入
- 雲端同步
- 食物資料庫
- 自動熱量估算
- 營養素分析
