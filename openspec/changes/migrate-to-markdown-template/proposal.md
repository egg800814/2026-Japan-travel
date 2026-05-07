## Why

目前行程網頁（`index.html`）是純靜態的 HTML 結構。當需要新增、修改或調整景點順序時，必須直接編輯繁雜的 HTML 與 CSS class 結構，不僅耗時且容易出錯。透過將靜態網頁轉型為「Markdown 驅動的樣板 (Template Driven)」，使用者未來只需在 `journey.md` 內以直覺的文本編輯，並能輕鬆加入圖片網址與單日地圖，即可自動生成完整的網頁，大幅降低維護成本。

## What Changes

- 將現有 `index.html` 內文抽離，轉化為僅包含骨架與樣式的樣板檔案（`template.html`）。
- 開發一支 Python 靜態生成腳本（`build.py`），執行時讀取 `journey.md` 並透過正則表達式解析各天行程、標題、時間與亮點叮嚀。
- 擴充 `journey.md` 語法約定：
  - **圖片插入**：在景點項目上方直接使用 Markdown 圖片語法 `![alt](url)`，腳本自動與下方內容封裝成單一卡片 (`.card`)。
  - **地圖插入**：在當日行程最後一行使用 `🗺️ [地圖標題](Google Maps 網址)` 語法，腳本自動轉換為嵌入式 iframe 區塊 (`.map-iframe`)。
- `index.html` 將成為腳本自動產出的檔案，不再人工編輯。

## Capabilities

### New Capabilities
- `markdown-to-html-generator`: 負責讀取 `journey.md` 文本，解析特定事件節點、圖片語法與地圖標記，並套用 `template.html` 產生靜態網頁。

### Modified Capabilities
- `project-baseline`: 專案從「純靜態網頁」轉型為「Python 腳本靜態網站生成架構」，規格需更新。

## Impact

- **核心檔案變更**：`index.html` 轉為編譯產物，新增 `template.html` 作為基底。
- **維護流程改變**：未來編輯行程的單一事實來源 (Single Source of Truth) 轉移至 `journey.md`。
- **系統相依**：需要 Python 3.13 執行環境 (`.\.venv\Scripts\python`) 來執行生成腳本，無伺服器端相依。
