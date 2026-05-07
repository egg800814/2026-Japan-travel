# 現狀規格書 (Project Baseline)

## 1. 系統架構概述 (System Architecture Overview)
本專案目前為一個純前端的靜態單頁/多頁式網站 (Static Single/Multi-Page Application)，主要用於展示「富士山・地中海郵輪 8天7夜」的專屬行程表。
- **核心技術**：純 HTML5 + CSS3 + 輕量 Vanilla JS。
- **部署模式**：靜態網頁託管 (Static Hosting)。
- **檔案結構**：
  - `index.html`：主行程表入口頁面（使用深色/高質感 Editorial Design 主題）。
  - `new.html`：行程表替代版本。
  - `journey.md` / `docs/design_proposal.md`：原始文案與設計提案規格。

## 2. 資料庫/資料表 Schema (Database Schema)
目前為**無資料庫架構 (Serverless / No Database)**。
所有的行程資料（時間、地點、描述、圖片 URL）均以 Hardcoded 形式直接寫入 HTML DOM 結構中。
若未來需要模組化與資料綁定，其核心資料結構 (Virtual JSON Schema) 預期如下：

- **`Trip` (總行程)**
  - `title`: string (行程主標題)
  - `description`: string (SEO 與摘要描述)
  - `days`: array of `Day`
- **`Day` (單日行程)**
  - `id`: string (錨點，例如：`day0`, `day1`)
  - `title`: string (例如："Day 1 抵達")
  - `theme`: string (外觀主題，例如：`info-theme`, `cruise-theme`)
  - `events`: array of `Event`
- **`Event` (單一景點/事件)**
  - `timeBadge`: string (時間區間，例如："14:00 - 15:30")
  - `title`: string (景點/事件標題)
  - `image_url`: string (展示圖片)
  - `notes`: array of objects (管家叮嚀，包含 `type`, `header`, `content`)
  - `map_link`: string (Google Maps 導航連結)

## 3. 核心 API 列表 (Core API List)
目前無後端 API，僅依賴第三方服務嵌入與資源引入：
1. **Google Maps Embed API**
   - 用途：於每個 Day 的行程末端嵌入互動式地圖 (`<iframe src="https://maps.google.com/maps?...">`)，提供當日路線概覽。
2. **Google Fonts API**
   - 用途：載入字體 `Noto Serif TC` (思源明體) 與 `Noto Sans TC` (思源黑體)，呈現高質感的排版與閱讀體驗。
3. **外部圖庫引用**
   - 用途：引用 Unsplash 等外部圖片連結作為情境示意與背景圖。

## 4. 重要的業務邏輯 (Important Business Logic)
系統目前的邏輯完全集中於前端介面互動，無複雜狀態管理：
- **視差滾動與進場動畫 (Parallax & Cinematic Reveal)**
  - 首屏 Hero 區塊透過 CSS `@keyframes cinematicFadeIn` 實現電影級淡入效果。
  - 英雄背景設定 `background-attachment: fixed` 實現捲動時的視差滾動 (Parallax Scrolling)。
- **行動優先導覽列 (Sticky Navigation)**
  - 行程切換導覽列 (`#mainNav`) 使用 `position: sticky` 吸附於螢幕頂部。
  - 支援手機端水平滑動 (Horizontal Scroll)，提供使用者在不同天數標籤 (`#day0` ~ `#day9`) 之間快速跳轉。
- **手風琴式折疊區塊 (Accordion Collapse)**
  - 各天行程透過 `.day-section` 與 `.day-header` 區分。
  - 綁定原生 `onclick="toggleSection(...)"` 事件，切換 `.day-content` 的 `collapsed` 狀態，並附帶平滑的 `slideDown` 動畫。
- **高轉換率設計機制 (FOMO & Premium UI)**
  - 依照 `design_proposal.md`，使用高對比度的色彩（如 `--accent-color: #C5A059`）。
  - 將一般行程轉化為「管家視角」與「限時限量」的文案提示 (`.note.calm` 等組件)，強化沉浸感與急迫感。
