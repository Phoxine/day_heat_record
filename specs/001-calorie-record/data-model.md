# Data Model: 每日熱量記錄 Web App

## UserProfile

代表單一使用者的基本資料。

**Fields**:

- `id`: primary key
- `name`: 字串，必填，去除前後空白後不可為空
- `height_cm`: 正整數，必填
- `weight_kg`: 正數，可支援小數，必填
- `age`: 正整數，必填
- `created_at`: 建立時間
- `updated_at`: 更新時間

**Validation**:

- `name` 不可空白。
- `height_cm`、`weight_kg`、`age` 必須大於 0。
- MVP 只允許一筆 active profile；若已有 profile，首頁導向記錄頁，profile 頁提供編輯。

## DailyRecord

代表某一日期的飲食記錄容器。

**Fields**:

- `id`: primary key
- `profile`: foreign key to `UserProfile`
- `date`: 日期，必填
- `created_at`: 建立時間
- `updated_at`: 更新時間

**Relationships**:

- 一個 `UserProfile` 有多個 `DailyRecord`。
- 一個 `DailyRecord` 有多個 `MealEntry`。

**Validation**:

- 同一個 `profile` 與 `date` 組合 MUST 唯一。
- 日期沒有記錄時，view 可建立空的 `DailyRecord` 或以空狀態呈現後在新增餐點時建立。

## MealEntry

代表使用者輸入的一筆食物與熱量。

**Fields**:

- `id`: primary key
- `daily_record`: foreign key to `DailyRecord`
- `meal_type`: choice，值為 `breakfast`、`lunch`、`dinner`
- `food_name`: 字串，必填，去除前後空白後不可為空
- `calories`: 正整數，必填
- `created_at`: 建立時間
- `updated_at`: 更新時間

**Validation**:

- `food_name` 不可空白。
- `calories` 必須大於 0。
- `meal_type` 只能是早餐、午餐、晚餐三者之一。

## Derived Values

以下值不建表，從 ORM 查詢或 model/helper method 計算：

- 餐別小計：單一 `DailyRecord` 中指定 `meal_type` 的 `calories` 加總。
- 當日總熱量：單一 `DailyRecord` 所有 `MealEntry.calories` 加總。
- 統計總熱量：指定日期區間內所有 `MealEntry.calories` 加總。
- 平均每日熱量：指定日期區間總熱量除以有記錄的日期數；沒有記錄時顯示 0。
- 三餐分布：指定日期區間內各 `meal_type` 小計與佔比。
- 每日總熱量列表：指定日期區間內依日期分組的熱量加總。

## State Transitions

- 未建立 profile -> 建立 profile -> 今日記錄頁。
- 無日期記錄 -> 新增第一筆 meal entry -> 日期有記錄。
- 日期有記錄 -> 修改或刪除 meal entry -> 重新計算小計與總計。
- 刪除某日期最後一筆 meal entry -> 日期呈現空餐點狀態，統計不將該日期列為有記錄日。
