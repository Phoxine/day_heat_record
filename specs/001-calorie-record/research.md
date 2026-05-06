# Research: 每日熱量記錄 Web App

## Decision: Django 5.2 LTS + Python 3.12

**Rationale**: Django 5.2 LTS 提供長期支援與成熟的 forms、templates、ORM、testing
工具，適合快速交付 server-rendered MVP。Python 3.12 是穩定且常見的 container
runtime 選擇。

**Alternatives considered**:

- Django 6.x：較新但對 MVP 無明確收益，且可能增加相依版本風險。
- FastAPI + frontend framework：需要額外 API 與前端狀態管理，對本需求過度設計。

## Decision: Django templates 作為前端與後端整合界面

**Rationale**: 使用者需求是表單、日期切換、餐點 CRUD 與統計頁，Django templates
可直接支援，不需要 SPA。server-rendered HTML 也能讓表單驗證錯誤與空狀態保持
簡單、可測試。

**Alternatives considered**:

- React/Vue SPA：會新增 build pipeline、API contract 與前端狀態管理，不符合 MVP。
- HTMX：可改善局部互動，但不是 MVP 必要條件，先不加入。

## Decision: PostgreSQL 16 + Django ORM

**Rationale**: 使用者明確要求 PostgreSQL 與 Django ORM。PostgreSQL 16 是穩定且
常用的 container image 版本，足以支援唯一約束、日期查詢與統計 aggregation。

**Alternatives considered**:

- SQLite：較簡單但不符合使用者指定的 PostgreSQL。
- 直接 SQL：目前查詢可由 ORM 表達，直接 SQL 會降低可維護性。

## Decision: Docker Compose 管理 `web` 與 `db`

**Rationale**: 使用者要求所有 service 都在 container 運行。MVP 只需要 Django
web app 與 PostgreSQL database，因此 compose 只納入 `web` 與 `db`，並用
environment variables 管理資料庫連線。

**Alternatives considered**:

- 加入 Nginx：本地 MVP 與 planning 階段不需要。
- 加入 Redis/Celery：沒有背景工作需求。

## Decision: 單一使用者 profile，暫不加入登入

**Rationale**: 規格明確將多人帳號登入列為 MVP 範圍外。使用單一 profile 可降低
資料模型與 UI 複雜度，仍能完整驗證核心熱量記錄流程。

**Alternatives considered**:

- Django auth：會引入註冊、登入、session、權限與多使用者資料隔離，超出 MVP。

## Decision: 統計摘要即時計算，不建立統計表

**Rationale**: 個人使用資料量小，透過 ORM aggregation 計算最近 7 天與 30 天統計
即可。避免建立同步任務或衍生資料表造成一致性問題。

**Alternatives considered**:

- Materialized statistics table：需要額外同步邏輯，對 MVP 過度設計。
