## MODIFIED Requirements

### Requirement: 系統基礎架構定義
系統 SHALL 從純靜態 HTML 檔案維護模式，轉型為基於 Python 的靜態網站生成器 (SSG) 模式。

#### Scenario: 專案核心文件組成變更
- **WHEN** 開發者檢視專案結構時
- **THEN** 專案的資料單一真相來源 (Source of Truth) 從 `index.html` 轉移至 `journey.md`，而 `index.html` 成為由 `build.py` 自動生成的編譯產物。
