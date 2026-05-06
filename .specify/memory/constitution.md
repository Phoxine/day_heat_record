<!--
Sync Impact Report
Version change: template -> 1.0.0
Modified principles:
- Placeholder Principle 1 -> I. 高品質可維護
- Placeholder Principle 2 -> II. 可被測試
- Placeholder Principle 3 -> III. UI/UX 友善
- Placeholder Principle 4 -> IV. MVP 優先
- Placeholder Principle 5 -> V. 簡潔而不過度設計
Added sections:
- 產品與技術限制
- 開發流程與品質門檻
Removed sections:
- 無
Templates requiring updates:
- ✅ updated .specify/templates/plan-template.md
- ✅ updated .specify/templates/spec-template.md
- ✅ updated .specify/templates/tasks-template.md
- ✅ updated .specify/templates/checklist-template.md
- ✅ updated AGENTS.md
- ✅ no update required: .specify/templates/commands/*.md not present in this repository
Follow-up TODOs:
- 無
-->
# Day Heat Record Constitution

## Core Principles

### I. 高品質可維護
所有交付 MUST 以清楚、可讀、可維護為最低標準。需求、規格、計畫、任務、
程式碼與使用者可見文字 MUST 使用正體中文，除非引用 API 名稱、程式識別字、
第三方專有名詞或錯誤訊息。實作 MUST 遵循既有專案慣例，避免無關重構與
未被需求證明的抽象化。

Rationale: MVP 仍然是產品基準；低品質的捷徑會讓後續驗證、修改與交付變慢。

### II. 可被測試
每個功能切片 MUST 定義可獨立驗證的使用者情境、驗收條件與成功指標。核心
商業邏輯、資料轉換、錯誤處理與使用者流程 MUST 有自動化測試或明確的手動
驗證步驟；若不加入自動化測試，計畫 MUST 說明風險與替代驗證方式。

Rationale: 可測試性是判斷功能是否完成的依據，而不是交付後才補上的活動。

### III. UI/UX 友善
任何使用者介面 MUST 優先支援主要任務的清楚完成：資訊階層明確、互動狀態
可理解、錯誤訊息可行動、行動裝置與桌面尺寸不重疊或截斷重要內容。UI 文案
MUST 使用自然的正體中文，避免把技術實作細節暴露給使用者。

Rationale: 好的 MVP 不只是功能存在，也必須讓目標使用者能可靠完成任務。

### IV. MVP 優先
規格與任務 MUST 先交付最小但可用、可展示、可驗證的 P1 使用者故事。P2/P3
範圍 MUST 不阻塞 P1 完成；若某項基礎建設會延後 MVP，計畫 MUST 明確說明
它是 P1 必要條件，並記錄較小替代方案為何不可行。

Rationale: 專案需要快速產生可驗證價值，避免用完整系統設計取代產品學習。

### V. 簡潔而不過度設計
實作 MUST 採用能滿足目前需求的最簡單可靠方案。新增框架、跨層抽象、複雜
狀態管理、設計系統或泛用化元件前，MUST 有明確需求、重複成本或風險理由。
Complexity Tracking MUST 記錄任何違反簡潔性的決策與被拒絕的較小方案。

Rationale: 過度設計會增加測試、維護與 UI 認知成本，降低 MVP 交付速度。

## 產品與技術限制

本專案的所有功能規格、計畫、任務、檢查清單與使用者可見介面 MUST 使用
正體中文。技術文件可保留必要的英文 API、套件、路徑與命令名稱，但說明文字
MUST 以正體中文撰寫。

規格 MUST 明確標示 MVP 邊界、非目標、假設與成功指標。任何 UI/UX 需求 MUST
包含目標使用者、主要任務、關鍵狀態、錯誤狀態與響應式行為。任何資料或邏輯
需求 MUST 包含可驗證的輸入、輸出、邊界條件與錯誤情境。

## 開發流程與品質門檻

每個 feature 的 plan.md MUST 在 Constitution Check 中確認：正體中文、P1 MVP、
可測試性、UI/UX 友善與避免過度設計。spec.md MUST 以可獨立測試的使用者故事
排序，並讓 P1 能單獨構成可展示 MVP。tasks.md MUST 依使用者故事分組，且每個
故事 MUST 有驗證任務或測試任務。

實作完成前 MUST 執行對應的測試、lint、型別檢查或手動驗證；若任一項無法執行，
交付摘要 MUST 說明原因、風險與替代檢查結果。任何新增複雜度 MUST 在 plan.md
的 Complexity Tracking 中記錄。

## Governance

本 constitution 優先於其他專案慣例。所有規格、計畫、任務、實作與 review MUST
檢查是否符合 Core Principles；若有例外，MUST 在對應文件中寫明理由、影響與
後續處理方式。

修訂 constitution MUST 更新版本、日期與 Sync Impact Report，並同步更新受影響
的模板與 runtime guidance。版本規則如下：

- MAJOR: 移除或重新定義既有原則，造成既有流程不相容。
- MINOR: 新增原則、治理章節或實質擴充品質門檻。
- PATCH: 澄清文字、修正錯字或不改變治理語意的調整。

Compliance review MUST 發生在 planning、tasks generation 與 implementation
完成前。任何未通過的門檻 MUST 在進入下一階段前修正，或以文件化例外處理。

**Version**: 1.0.0 | **Ratified**: 2026-05-06 | **Last Amended**: 2026-05-06
