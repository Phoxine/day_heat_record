# UI Contracts: 每日熱量記錄 Web App

本 feature 不提供 public JSON API。外部使用者介面 contract 是 Django server-rendered
HTML routes 與表單行為。

## GET `/`

**目的**: App 入口。

**Behavior**:

- 若尚未建立 profile，顯示建立個人資料表單。
- 若已有 profile，導向今日的 `/records/<date>/`。

**States**:

- 空狀態：顯示建立資料表單與正體中文提示。
- 錯誤狀態：表單送出失敗時停留頁面並顯示欄位錯誤。

## GET/POST `/profile/`

**目的**: 建立或編輯個人資料。

**Form fields**:

- `name`
- `height_cm`
- `weight_kg`
- `age`

**Validation**:

- 名字不可空白。
- 身高、體重、年齡必須大於 0。

**Success**:

- 儲存後導向今日記錄頁。

## GET `/records/<date>/`

**目的**: 查看指定日期的三餐記錄。

**Date format**: `YYYY-MM-DD`

**Behavior**:

- 顯示日期切換控制。
- 顯示早餐、午餐、晚餐三個區塊。
- 每個區塊顯示食物項目、餐別小計與新增表單。
- 頁面顯示當日總熱量。
- 日期沒有任何餐點時，顯示可新增的空狀態。

## POST `/records/<date>/entries/`

**目的**: 新增指定日期的餐點項目。

**Form fields**:

- `meal_type`: `breakfast`、`lunch`、`dinner`
- `food_name`
- `calories`

**Validation**:

- 餐別必須是三餐之一。
- 食物名稱不可空白。
- 熱量必須大於 0。

**Success**:

- 回到同一日期記錄頁並顯示更新後小計與總計。

## POST `/entries/<entry_id>/edit/`

**目的**: 修改餐點項目。

**Form fields**:

- `food_name`
- `calories`

**Success**:

- 回到該餐點所屬日期記錄頁。

## POST `/entries/<entry_id>/delete/`

**目的**: 刪除餐點項目。

**Success**:

- 回到該餐點所屬日期記錄頁，並重新計算小計與總計。

## GET `/stats/`

**目的**: 查看統計資訊。

**Query parameters**:

- `period`: `7` 或 `30`，預設 `7`

**Behavior**:

- 顯示指定期間總熱量。
- 顯示平均每日熱量。
- 顯示記錄天數。
- 顯示早餐、午餐、晚餐熱量分布。
- 顯示每日總熱量列表。

**Empty State**:

- 沒有任何餐點記錄時，顯示空統計狀態與返回記錄頁的行動。

## UI Requirements

- 所有 label、button、validation message 與 empty state MUST 使用正體中文。
- 桌面與行動尺寸都 MUST 避免文字重疊、按鈕截斷與表格橫向溢出。
- 食物名稱過長時 MUST 換行或截斷並保留主要資訊可讀性。
