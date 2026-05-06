# Tasks: 每日熱量記錄 Web App

**Input**: Design documents from `specs/001-calorie-record/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ui-routes.md, quickstart.md

**Tests**: 本專案 constitution 要求每個使用者故事都可被測試，因此每個故事都包含
自動化測試或驗證任務。

**Organization**: 任務依使用者故事分組，確保 P1 可作為獨立 MVP 交付。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可平行執行，前提是不同檔案且不依賴未完成任務。
- **[Story]**: 使用者故事標籤，只用於 story phase。
- 每個任務都包含明確檔案路徑。

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 建立 Django + PostgreSQL + Docker Compose 的基本專案骨架。

- [ ] T001 建立 Django 專案與 app 目錄結構於 app/manage.py、app/config/、app/calories/、app/templates/、app/static/
- [ ] T002 建立 Python 相依清單於 requirements.txt，包含 Django 5.2 LTS、psycopg、gunicorn
- [ ] T003 建立 container image 定義於 Dockerfile
- [ ] T004 建立 Docker Compose services 於 compose.yaml，包含 web 與 db
- [ ] T005 建立環境變數範例於 .env.example
- [ ] T006 建立 Django settings、root urls、wsgi/asgi 於 app/config/settings.py、app/config/urls.py、app/config/wsgi.py、app/config/asgi.py
- [ ] T007 建立 calories app 設定與 URL 入口於 app/calories/apps.py、app/calories/urls.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 建立所有使用者故事共用的資料模型、forms、base layout 與基本測試架構。

**CRITICAL**: 完成本階段前不得開始使用者故事實作。

- [ ] T008 建立 UserProfile、DailyRecord、MealEntry models 與 validation 於 app/calories/models.py
- [ ] T009 建立 initial migration 於 app/calories/migrations/0001_initial.py
- [ ] T010 建立 Django admin 設定於 app/calories/admin.py
- [ ] T011 建立 ProfileForm 與 MealEntryForm 於 app/calories/forms.py
- [ ] T012 建立 base template 與共用導覽於 app/templates/base.html
- [ ] T013 建立共用 CSS 與響應式基礎樣式於 app/static/calories/styles.css
- [ ] T014 [P] 建立 model validation 測試於 app/calories/tests/test_models.py，僅涵蓋欄位驗證與唯一約束
- [ ] T015 [P] 建立 form validation 測試於 app/calories/tests/test_forms.py

**Checkpoint**: 資料模型、forms 與共用 UI 基礎完成，所有使用者故事可開始實作。

---

## Phase 3: User Story 1 - 建立資料並記錄當日三餐熱量 (Priority: P1) MVP

**Goal**: 使用者可建立個人資料，在今天的早餐、午餐、晚餐新增食物與熱量，並看到餐別小計與當日總熱量。

**Independent Test**: 從無資料狀態建立 profile，新增三筆分屬三餐的食物熱量，重新整理後確認資料仍可查看且總熱量正確。

### Tests / Verification for User Story 1

- [ ] T016 [P] [US1] 建立 profile 建立與首頁導向測試於 app/calories/tests/test_profile_views.py
- [ ] T017 [P] [US1] 建立今日記錄新增三餐、餐別小計 helper 與總熱量測試於 app/calories/tests/test_record_views.py

### Implementation for User Story 1

- [ ] T018 [US1] 實作首頁與 profile 建立/編輯 view 於 app/calories/views.py
- [ ] T019 [US1] 實作 profile route 與首頁 route 於 app/calories/urls.py、app/config/urls.py
- [ ] T020 [US1] 建立 profile form template 於 app/templates/calories/profile_form.html
- [ ] T021 [US1] 實作指定日期記錄頁 view、今日預設導向與餐點新增 view 於 app/calories/views.py
- [ ] T022 [US1] 實作記錄頁與餐點新增 routes 於 app/calories/urls.py
- [ ] T023 [US1] 建立三餐記錄 template 於 app/templates/calories/record_detail.html
- [ ] T024 [US1] 在 app/calories/models.py 加入餐別小計與當日總熱量 helper methods
- [ ] T025 [US1] 完成 P1 UI 文案、錯誤訊息、空狀態與成功狀態於 app/templates/calories/profile_form.html、app/templates/calories/record_detail.html

**Checkpoint**: P1 可獨立 demo：建立 profile、記錄今日三餐、查看餐別小計與當日總熱量。

---

## Phase 4: User Story 2 - 依日期查看與編輯飲食記錄 (Priority: P2)

**Goal**: 使用者可切換不同日期，並新增、修改、刪除該日期的餐點項目。

**Independent Test**: 建立兩個不同日期的記錄，確認資料不互相混合，並能修改與刪除單筆餐點。

### Tests / Verification for User Story 2

- [ ] T026 [P] [US2] 建立日期隔離與日期切換測試於 app/calories/tests/test_date_records.py
- [ ] T027 [P] [US2] 建立餐點修改與刪除測試於 app/calories/tests/test_entry_mutations.py

### Implementation for User Story 2

- [ ] T028 [US2] 實作日期切換處理與無記錄日期空狀態於 app/calories/views.py
- [ ] T029 [US2] 實作餐點編輯與刪除 views 於 app/calories/views.py
- [ ] T030 [US2] 實作餐點編輯與刪除 routes 於 app/calories/urls.py
- [ ] T031 [US2] 更新記錄頁 template 加入日期切換、編輯表單與刪除操作於 app/templates/calories/record_detail.html
- [ ] T032 [US2] 更新 record view validation message 與長食物名稱顯示行為於 app/templates/calories/record_detail.html、app/static/calories/styles.css

**Checkpoint**: P1 + P2 可獨立 demo：多日期記錄、不同日期資料隔離、餐點修改與刪除。

---

## Phase 5: User Story 3 - 查看熱量統計資訊 (Priority: P3)

**Goal**: 使用者可查看最近 7 天與 30 天總熱量、平均每日熱量、記錄天數、三餐分布與每日列表。

**Independent Test**: 建立至少 7 天記錄後進入統計頁，確認所有統計數字只包含指定期間資料。

### Tests / Verification for User Story 3

- [ ] T033 [P] [US3] 建立統計 aggregation 測試於 app/calories/tests/test_statistics.py，涵蓋總熱量、平均每日熱量、記錄天數、三餐分布、最高熱量日期與主要熱量來源餐別
- [ ] T034 [P] [US3] 建立統計頁 view 與空狀態測試於 app/calories/tests/test_stats_view.py

### Implementation for User Story 3

- [ ] T035 [US3] 實作統計查詢 helper function 於 app/calories/views.py
- [ ] T036 [US3] 實作 stats view 與 period 參數處理於 app/calories/views.py
- [ ] T037 [US3] 實作 stats route 於 app/calories/urls.py
- [ ] T038 [US3] 建立統計頁 template 於 app/templates/calories/stats.html，顯示總熱量、平均每日熱量、記錄天數、三餐分布、每日總熱量列表、最高熱量日期與主要熱量來源餐別
- [ ] T039 [US3] 更新導覽與統計頁樣式於 app/templates/base.html、app/static/calories/styles.css

**Checkpoint**: P1 + P2 + P3 完成，使用者可完成建立資料、記錄餐點、查看統計的完整流程。

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 完成交付前驗證、文件與容器化操作檢查。

- [ ] T040 [P] 補齊 quickstart 驗證結果與操作說明於 specs/001-calorie-record/quickstart.md
- [ ] T041 [P] 檢查所有 template 使用者可見文案為正體中文於 app/templates/base.html、app/templates/calories/
- [ ] T042 執行 containerized Django 測試 `docker compose exec web python manage.py test` 並修正失敗案例於 app/calories/tests/
- [ ] T043 執行 `docker compose up --build` 與 `docker compose exec web python manage.py migrate` 驗證於 compose.yaml、Dockerfile
- [ ] T044 驗證行動與桌面寬度下記錄頁、profile 頁、統計頁不重疊或截斷於 app/static/calories/styles.css
- [ ] T045 清理非 MVP 複雜度與未使用程式碼於 app/calories/、app/config/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 無依賴。
- **Foundational (Phase 2)**: 依賴 Setup 完成，阻塞所有使用者故事。
- **User Story 1 (Phase 3)**: 依賴 Foundational 完成，是 MVP。
- **User Story 2 (Phase 4)**: 依賴 US1 的記錄頁與餐點建立流程。
- **User Story 3 (Phase 5)**: 依賴 US1 的資料模型與餐點資料；可在 US2 後完成完整使用體驗。
- **Polish (Phase 6)**: 依賴所有目標故事完成。

### User Story Dependencies

- **US1**: P1 MVP，必須先完成。
- **US2**: 建立在 US1 的日期記錄頁與餐點項目上。
- **US3**: 建立在 US1/US2 累積的多日期資料上。

### Within Each User Story

- 測試先於實作。
- Forms/models/helper methods 先於 views。
- Views 先於 templates 的完整互動串接。
- Route 完成後再做 end-to-end view tests。

## Parallel Opportunities

- T014 與 T015 可平行。
- US1 測試 T016 與 T017 可平行。
- US2 測試 T026 與 T027 可平行。
- US3 測試 T033 與 T034 可平行。
- Polish 中 T040 與 T041 可平行。

## Parallel Example: User Story 1

```bash
Task: "T016 [P] [US1] 建立 profile 建立與首頁導向測試於 app/calories/tests/test_profile_views.py"
Task: "T017 [P] [US1] 建立今日記錄新增三餐與總熱量測試於 app/calories/tests/test_record_views.py"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. 完成 Phase 1 Setup。
2. 完成 Phase 2 Foundational。
3. 完成 Phase 3 US1。
4. 停下並驗證：建立 profile、記錄今日三餐、確認總熱量。

### Incremental Delivery

1. Setup + Foundational -> 可開始故事開發。
2. US1 -> MVP 可 demo。
3. US2 -> 支援多日期、修改、刪除。
4. US3 -> 支援統計頁。
5. Polish -> 完成容器與 UI 驗證。

## Notes

- 所有任務描述與 UI 文案一律使用正體中文；路徑、命令與 identifiers 可保留原文。
- 不新增 REST API、SPA、登入、多使用者或背景服務。
- 每個 story checkpoint 都必須可獨立測試與展示。
