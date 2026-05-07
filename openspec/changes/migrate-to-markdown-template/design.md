## Context

目前「富士山・地中海郵輪」旅遊行程網頁是一個純靜態的 `index.html` 檔案。所有的文案、排版結構、圖片連結與 Google Maps 導覽連結都以 Hardcoded 方式寫死在 HTML 原始碼中。這種做法在初次開發時速度快，但當未來需要新增景點、調整順序或更新照片時，必須手動尋找並修改對應的 HTML 標籤（如 `.card`, `.time-badge`, `.note` 等），容易因漏改標籤導致版面破圖，且非工程背景的使用者難以維護。

使用者希望將 `journey.md`（原始的 Markdown 行程規劃檔）作為唯一的事實來源 (Single Source of Truth)，透過加入簡單的圖片與地圖語法後，自動生成對應的 HTML 網頁。

## Goals / Non-Goals

**Goals:**
- 提供一個自動化方案，讀取 `journey.md` 並產出 `index.html`。
- 保留原有高質感的視覺設計與互動（Parallax, Sticky Nav, Accordion）。
- 將 `index.html` 內的共用 HTML 架構抽離為 `template.html`。
- 支援在 `journey.md` 內直接使用標準 Markdown 語法插入圖片 (`![alt](url)`) 與 Google Maps (`🗺️ [title](url)`)。

**Non-Goals:**
- 不建立複雜的後端伺服器 (Node.js/Django 等)，維持無伺服器 (Serverless) 的靜態託管架構。
- 不引入龐大的前端框架 (React/Vue/Angular) 來重構頁面。
- 不使用純前端 JS (如 `marked.js`) 在客戶端即時渲染（因為直接開啟 `.html` 檔案會有 CORS 或加載延遲問題，且不利於純靜態發布）。

## Decisions

1. **選擇 Python 作為靜態生成腳本 (Static Site Generation)**
   - **Rationale**: 使用者已擁有 Python 3.13 虛擬環境 (`.\.venv\Scripts\python`)。Python 的文本處理與正則表達式 (`re` 模組) 功能強大，適合解析客製化但結構固定的 Markdown 文件，不需額外安裝 Node.js 或其他工具。
   - **Alternatives**: 
     - *Client-side JS parsing (marked.js)*: 雖然免編譯，但在本地 `file://` 協議下存取外部 `.md` 檔案會遇到 CORS 阻擋，需依賴 local server，不符合無腦雙擊開啟的期待。
     - *Hugo/Jekyll 等成熟 SSG 框架*: 對於這個單頁式的小專案來說殺雞用牛刀，學習成本過高。

2. **採用正則表達式 (RegEx) 擷取 Markdown 區塊而非完整 AST 解析**
   - **Rationale**: 現有的 `journey.md` 有著極度規律的特殊排版格式（如 `- **14:00 - 15:30 ｜ ...**`）。直接針對這些特徵進行 RegEx 匹配與 HTML 替換，會比將 Markdown 轉為抽象語法樹 (AST) 後再處理來得輕量且容易客製化 HTML class (`.card`, `.time-badge` 等)。
   - **Alternatives**: *使用 `markdown` 或 `mistune` 函式庫*: 這些函式庫產出的是標準 HTML (`<ul>`, `<li>`, `<p>`)，要再轉換成目前高度客製化的 UI 卡片結構反而麻煩。

3. **樣板引擎選擇純字串替換 (String Substitution)**
   - **Rationale**: 由於只有一個頁面，不需要複雜的 `if/else` 樣板邏輯。將 `template.html` 內加入 `<!-- CONTENT_PLACEHOLDER -->`，Python 腳本生成內容後直接 `replace()` 即可。

## Risks / Trade-offs

- **[Risk] Markdown 格式嚴格性** → **Mitigation**: 使用者如果在 `journey.md` 裡打錯時間格式或縮排，可能會導致腳本解析失敗。腳本應實作簡單的 Error Handling，若解析不到預期格式，終端機需印出警告提示哪一行出錯。
- **[Trade-off] 缺乏即時預覽 (Hot Reload)** → **Mitigation**: 採用編譯式生成的缺點是每次修改 `.md` 都要手動執行腳本。可透過包裝一個簡單的 `watch` 腳本或 batch file 來改善這點，但初期先以手動執行 `python build.py` 為主，保持系統單純。
