## 1. 樣板準備與抽取

- [x] 1.1 複製現有的 `index.html` 建立為 `template.html`。
- [x] 1.2 在 `template.html` 內清空 `<div class="container">` 裡的 hardcoded 行程內容，並替換為 `<!-- CONTENT_PLACEHOLDER -->` 標記。

## 2. 解析器與生成腳本開發

- [x] 2.1 建立 `program/build.py` 檔案作為主要生成腳本（依照專案目錄規範，放置於 program 資料夾，或者根目錄以方便執行）。
- [x] 2.2 實作正則表達式 (Regex) 解析 `journey.md` 中的「Day 標題」(`### 🗓️ Day X...`)，以建立對應的 `.day-section` 與 `.day-header`。
- [x] 2.3 實作 Regex 擷取行程事件（`- **時間區段 ｜ 標題**` 及其底下的子彈條列與 `**管家亮點**`）。
- [x] 2.4 實作 Regex 擷取圖片語法 (`![alt](url)`)，並在生成 HTML 時將其與緊接的行程事件封裝為 `.card`。
- [x] 2.5 實作 Regex 擷取地圖語法 (`🗺️ [標題](url)`)，產生底部的 `.map-link-container` 與 `<iframe>`。
- [x] 2.6 實作讀取 `template.html`，將生成的 HTML 字串替換進 placeholder 中，並覆寫 `index.html`。

## 3. 整合測試與發布

- [x] 3.1 編輯 `journey.md`，實際加入圖片連結與地圖連結語法以供測試。
- [x] 3.2 於終端機執行 `.\.venv\Scripts\python program/build.py` 產出最新版 `index.html`。
- [x] 3.3 驗證產出的 `index.html` 在 UI 呈現、手風琴折疊特效 (Accordion) 與視差滾動上是否與原版無異。
