## 澳門災情互助地圖（免費技術棧）

核心功能：
- 地圖標記災情（水浸、火災等），即時共享
- 即時天氣（Open-Meteo）
- 後端資料庫與即時：Supabase（免費層）
- **新增：SMG 街道圖片監控與 AI 水浸分析系統**

使用到的免費 API/服務：
- 地圖瓦片：OpenStreetMap 標準瓦片（`https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`，請加上 attribution）
- 即時天氣：Open-Meteo（免金鑰）
- Realtime/資料庫：Supabase（免費層）
- **SMG 街道圖片：澳門氣象地球物理局 API**
- **AI 分析：Google Gemini API**

### SMG 水浸監控系統

自動從澳門氣象地球物理局獲取 19 個地點的實時街道圖片，並使用 Gemini AI 分析水浸情況。

#### 快速開始
```bash
cd app
./start_smg_monitor.sh  # 或直接運行: python smg_flood_monitor_simple.py
```

詳細使用說明請參閱：
- `SMG_FLOOD_MONITOR_README.md` - 完整使用指南
- `PROJECT_SUMMARY.md` - 項目總結
- `examples_smg_usage.py` - 使用範例

監控地點包括：花地瑪、內港、康公廟、司打口、紅街市等 19 個澳門重點區域。

### 本地開發
1. Node.js LTS 安裝完成後，於專案根目錄：
```
npm install
npm run dev
```
瀏覽：`http://localhost:5173`

2. 環境變數
建立 `.env`，內容請參考 `ENV_EXAMPLE.txt`：
```
VITE_SUPABASE_URL=你的 Supabase 專案 URL
VITE_SUPABASE_ANON_KEY=你的 Supabase anon key
GEMINI_API_KEY=你的 Gemini API 密鑰（可選，已內建）
```

3. 建立資料庫表格（Supabase SQL Editor 貼上 `supabase/schema.sql`）

### 部署
- Netlify / Vercel 皆可（免費層）
- 於平台上設定環境變數 `VITE_SUPABASE_URL` 與 `VITE_SUPABASE_ANON_KEY`

### 後續可加功能（免費）：
- 匿名存在（Presence）即時分享位置（僅裝置級 UUID）
- 管理員隱藏/刪除不當標記（可用 Edge Function 或 Dashboard）
- 災情類型篩選、時間窗口顯示、熱度視覺化
- **SMG 監控數據整合到地圖界面**
- **歷史水浸數據分析與趨勢預測**


