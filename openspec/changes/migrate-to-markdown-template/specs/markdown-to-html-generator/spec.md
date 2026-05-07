## ADDED Requirements

### Requirement: 讀取並解析 Markdown 內容
系統 MUST 能夠讀取 `journey.md` 檔案，並正確識別每日行程的標題、時間區段、事件標題、圖片連結與注意事項。

#### Scenario: 解析成功
- **WHEN** Python 生成腳本執行時
- **THEN** 系統將 `journey.md` 的內容依據天數 (`Day 1`, `Day 2` 等) 分段，並提取出所有關聯的事件資料物件。

### Requirement: 支援圖片語法轉換
系統 MUST 支援在行程事件的正上方，使用標準 Markdown 語法 `![alt](url)` 來宣告該事件的展示圖片。

#### Scenario: 存在圖片的行程事件
- **WHEN** 腳本遇到 `![...](url)` 緊接著 `- **時間 ｜ 標題**` 的格式
- **THEN** 系統產出包含 `<img src="url">` 的完整 `.card` HTML 結構。

#### Scenario: 無圖片的行程事件
- **WHEN** 腳本遇到行程事件但上方無圖片宣告
- **THEN** 系統產出不含圖片區塊的純文字卡片 (`.card.text-card` 或無 `.card-img-wrapper` 的卡片結構)。

### Requirement: 支援 Google Maps 連結轉換
系統 MUST 支援在單日行程區塊的尾端，讀取 `🗺️ [地圖標題](Google Maps 網址)` 語法並將其渲染為嵌入式地圖。

#### Scenario: 生成單日底部地圖
- **WHEN** 腳本解析到某天的內容尾端出現地圖標記語法
- **THEN** 系統在該天的 `.day-content` 結尾處，生成包含 `<iframe>` 的 `.map-link-container` 結構。

### Requirement: 套用模板並輸出 HTML
系統 MUST 將解析後的 HTML 內容字串，注入到 `template.html` 的預留位置，並輸出為 `index.html`。

#### Scenario: 輸出靜態網頁
- **WHEN** 所有天數的行程皆解析完畢
- **THEN** 系統覆寫並儲存 `index.html` 檔案，且檔案內容符合標準 HTML5 規範。
