# SMG 水浸監控系統使用說明

## 功能概述

這個系統會自動從澳門氣象地球物理局（SMG）的街道攝像頭獲取實時圖片，並使用 Gemini AI 分析水浸情況。

## 主要功能

1. **自動下載圖片**：從 19 個監控地點獲取實時街道圖片
2. **AI 水浸分析**：使用 Gemini AI 分析每張圖片的水浸情況
3. **結果保存**：保存圖片和分析結果到本地文件夾
4. **循環監控**：按設定間隔自動重複執行

## 監控地點

系統監控以下 19 個地點：

- 花地瑪 (LMF)
- 內港北 (LSI)
- 內港 (LPI)
- 康公廟 (LHK)
- 司打口 (LPH)
- 內港南 (LPF)
- 下環街 (LPM)
- 青洲河邊馬路 (LIV)
- 紅街市 (LMM)
- 光復街 (LRR)
- 永樂戲院 (LTA)
- 菜園路 (LHO)
- 沙維斯街 (LCH)
- 柯維納馬路 (LAO)
- 益隆 (LIL)
- 松樹尾 (LCS)
- 黑橋街 (LPN)
- 聖方濟各堂 (LCL)
- 石排灣 (LSP)

## 安裝依賴

```bash
cd /home/runner/work/map-app/map-app/app
pip install -r requirements.txt
```

主要依賴：
- `requests`: HTTP 請求庫
- `google-genai`: Google Gemini AI SDK
- 其他 FastAPI 相關依賴

## 配置

### 1. Gemini API Key

API Key 已經內建在腳本中：
```
AIzaSyBUU2MYPMqc9NHanRp68tRCJsUb5wWA1wU
```

如需更改，請編輯 `smg_flood_monitor.py` 中的 `GEMINI_API_KEY` 變數。

### 2. 環境變數（可選）

你也可以在 `.env` 文件中設置：
```
GEMINI_API_KEY=你的API密鑰
```

然後修改腳本讀取環境變數。

### 3. 監控間隔

在 `smg_flood_monitor.py` 中修改：
```python
INTERVAL_MINUTES = 10  # 修改為你想要的間隔時間（分鐘）
```

## 使用方法

### 啟動監控系統

```bash
cd /home/runner/work/map-app/map-app/app
python smg_flood_monitor.py
```

### 停止監控

按 `Ctrl+C` 停止監控系統。

## 輸出文件

### 1. 圖片文件

保存位置：`smg_images/` 目錄

文件命名格式：
```
{代號}_{中文名稱}_{時間戳}.jpg
```

例如：
```
LMF_花地瑪_20241028_165530.jpg
```

### 2. 分析結果

保存位置：`flood_analysis/` 目錄

文件命名格式：
```
{代號}_{中文名稱}_{時間戳}_分析.txt
```

文件內容包括：
- 地點信息
- 圖片文件名
- 分析時間
- 提示詞
- AI 分析結果

例如：
```
地点代号: LMF
地点名称: 花地瑪
图片文件: LMF_花地瑪_20241028_165530.jpg
分析时间: 2024-10-28 16:55:30
提示词: 分析這張圖片裡面的水浸情況如何

============================================================
分析结果:
============================================================

根據圖片顯示，目前該區域沒有明顯的水浸情況...
```

## API 整合

系統也支持通過 FastAPI 端點使用 Gemini 服務：

### 啟動 API 服務器

```bash
cd /home/runner/work/map-app/map-app/app
python main.py
```

訪問 API 文檔：`http://localhost:8000/docs`

### 可用端點

1. **分析圖片**: `POST /api/gemini/analyze-image`
   - 上傳圖片文件
   - 提供提示詞
   - 返回 AI 分析結果

2. **生成文本**: `POST /api/gemini/generate`
   - 發送文本提示
   - 返回生成的文本

3. **對話**: `POST /api/gemini/chat`
   - 多輪對話
   - 維護對話歷史

## 系統架構

```
smg_flood_monitor.py (主腳本)
    ├─ 獲取圖片 URL (從 SMG API)
    ├─ 下載圖片
    ├─ 使用 Gemini AI 分析
    └─ 保存結果

services/gemini_service.py (Gemini 服務層)
    └─ 處理 AI 請求

config.py (配置管理)
    └─ 管理 API 密鑰和設置
```

## 故障排除

### 1. 無法連接到 SMG API

檢查網絡連接，確保可以訪問：
```
https://cms.smg.gov.mo
```

### 2. Gemini API 錯誤

- 檢查 API Key 是否正確
- 檢查是否有足夠的 API 配額
- 查看日誌了解詳細錯誤信息

### 3. 圖片下載失敗

- 確認 `smg_images/` 目錄有寫入權限
- 檢查磁盤空間是否足夠

## 日誌

系統會在控制台輸出詳細的日誌信息：

```
2024-10-28 16:55:30 - INFO - 開始新一轮监控
2024-10-28 16:55:31 - INFO - [LMF] 獲取到圖片 URL
2024-10-28 16:55:32 - INFO - [LMF] ✅ 下載成功
2024-10-28 16:55:35 - INFO - ✅ 分析完成
```

## 注意事項

1. **API 限制**：注意 Gemini API 的使用限制和配額
2. **存儲空間**：定期清理舊的圖片和分析結果文件
3. **請求頻率**：避免過於頻繁的請求，建議最少 5 分鐘間隔
4. **隱私**：妥善保管 API Key，不要公開分享

## 自定義

### 修改分析提示詞

在 `smg_flood_monitor.py` 中：
```python
FLOOD_ANALYSIS_PROMPT = "你的自定義提示詞"
```

### 選擇特定地點

修改 `CAMERA_GROUPS` 列表，只保留你需要的地點代號：
```python
CAMERA_GROUPS = ["LMF", "LPI", "LHK"]  # 只監控這三個地點
```

### 更改保存目錄

```python
SAVE_DIR = "你的圖片目錄"
ANALYSIS_DIR = "你的分析結果目錄"
```

## 技術支持

如有問題，請檢查：
1. 日誌輸出
2. API 文檔：https://ai.google.dev/gemini-api/docs
3. SMG 官網：https://www.smg.gov.mo
