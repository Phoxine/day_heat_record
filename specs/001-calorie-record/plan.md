# Implementation Plan: 每日熱量記錄 Web App

**Branch**: `001-calorie-record` | **Date**: 2026-05-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-calorie-record/spec.md`

## Summary

建立一個以 Django templates 呈現的單一使用者熱量記錄 Web App。使用者可建立
個人資料、依日期記錄早中晚餐食物與熱量，並查看最近 7 天與 30 天統計資訊。
前後端皆由 Django 處理，資料存取一律透過 Django ORM，PostgreSQL 與 web app
都由 `compose.yaml` 管理。

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: Django 5.2 LTS、psycopg、gunicorn  
**Storage**: PostgreSQL 16，由 Django ORM 存取  
**Testing**: Django `TestCase`、Django test client、containerized PostgreSQL 測試流程  
**Target Platform**: Docker Compose 管理的本機與部署一致化環境  
**Project Type**: 單一 Django server-rendered web application  
**Performance Goals**: 30 天內記錄的統計頁在一般本機環境 1 秒內可完成主要內容呈現  
**Constraints**: 所有 service MUST 在 Docker container 中執行；使用者可見文案 MUST 使用正體中文；MVP 不加入登入、多使用者或前端框架  
**Scale/Scope**: 單一使用者、個人熱量記錄 MVP；資料量以日常個人使用為準

## Constitution Check

*GATE: MUST pass before Phase 0 research. Re-check after Phase 1 design.*

- **正體中文**: PASS。規格、計畫、contracts、quickstart 與使用者可見 UI 文案
  均使用正體中文；API、套件、路徑、命令與識別字保留原文。
- **P1 MVP**: PASS。P1 可單獨交付：建立 profile、記錄今天三餐、顯示餐別小計
  與當日總熱量。P2/P3 不阻塞 P1。
- **可被測試**: PASS。每個使用者故事都有獨立驗證方式；model、form、view 與
  統計查詢均規劃自動化測試。
- **UI/UX 友善**: PASS。採用少量 server-rendered templates，明確定義空狀態、
  錯誤狀態、成功狀態與行動裝置可讀性。
- **避免過度設計**: PASS。不加入 SPA、REST API、多使用者登入、背景服務、
  食物資料庫或額外狀態管理。

## Project Structure

### Documentation (this feature)

```text
specs/001-calorie-record/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── ui-routes.md
└── tasks.md
```

### Source Code (repository root)

```text
.
├── compose.yaml
├── Dockerfile
├── .env.example
├── requirements.txt
├── app/
│   ├── manage.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── calories/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── migrations/
│   │   └── tests/
│   ├── templates/
│   │   ├── base.html
│   │   └── calories/
│   └── static/
│       └── calories/
└── specs/
```

**Structure Decision**: 使用單一 Django project 與單一 `calories` app。這符合 MVP
需求並避免拆分 frontend/backend 專案造成不必要複雜度。Django templates 是主要
UI contract；不建立 public JSON API。

## Complexity Tracking

無 constitution gate violations。Docker Compose 是使用者明確要求，且只包含
必要的 `web` 與 `db` services。

## Phase 0: Research

見 [research.md](./research.md)。所有技術 unknowns 已決策完成，無未決問題。

## Phase 1: Design & Contracts

見 [data-model.md](./data-model.md)、[contracts/ui-routes.md](./contracts/ui-routes.md)
與 [quickstart.md](./quickstart.md)。

## Post-Design Constitution Check

- **正體中文**: PASS。所有新增 planning artifacts 使用正體中文。
- **P1 MVP**: PASS。資料模型與 routes 先支援 P1，日期切換與統計為可獨立擴充。
- **可被測試**: PASS。data model、forms、views、statistics 都有明確測試切入點。
- **UI/UX 友善**: PASS。contracts 定義空狀態、錯誤訊息與響應式要求。
- **避免過度設計**: PASS。不引入非必要 service、API layer 或前端 build pipeline。
