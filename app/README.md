## 澳門災情互助地圖（免費技術棧）

核心功能：
- 地圖標記災情（水浸、火災等），即時共享
- 即時天氣（Open-Meteo）
- 後端資料庫與即時：Supabase（免費層）

使用到的免費 API/服務：
- 地圖瓦片：OpenStreetMap 標準瓦片（`https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`，請加上 attribution）
- 即時天氣：Open-Meteo（免金鑰）
- Realtime/資料庫：Supabase（免費層）

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
```

3. 建立資料庫表格（Supabase SQL Editor 貼上 `supabase/schema.sql`）

### 部署
- Netlify / Vercel 皆可（免費層）
- 於平台上設定環境變數 `VITE_SUPABASE_URL` 與 `VITE_SUPABASE_ANON_KEY`

### 後續可加功能（免費）：
- 匿名存在（Presence）即時分享位置（僅裝置級 UUID）
- 管理員隱藏/刪除不當標記（可用 Edge Function 或 Dashboard）
- 災情類型篩選、時間窗口顯示、熱度視覺化


