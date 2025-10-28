# SMG 街道圖片下載器 + Gemini 水浸分析

這是一個自動從澳門氣象局（SMG）獲取實時街道圖片，並使用 Google Gemini API 分析水浸情況的工具。

## 功能特點

- ✅ 自動從 SMG API 獲取 19 個地點的實時街道圖片
- ✅ 使用 Gemini 2.0 Flash 模型分析每張圖片的水浸情況
- ✅ 自動保存圖片和分析結果
- ✅ 循環執行，持續監控
- ✅ 完整的錯誤處理和日誌記錄

## 監控地點

包含以下 19 個澳門地點：

| 代號 | 中文名稱 | 代號 | 中文名稱 |
|------|---------|------|---------|
| LMF  | 花地瑪   | LSI  | 內港北   |
| LPI  | 內港     | LHK  | 康公廟   |
| LPH  | 司打口   | LPF  | 內港南   |
| LPM  | 下環街   | LIV  | 青洲河邊馬路 |
| LMM  | 紅街市   | LRR  | 光復街   |
| LTA  | 永樂戲院 | LHO  | 菜園路   |
| LCH  | 沙維斯街 | LAO  | 柯維納馬路 |
| LIL  | 益隆     | LCS  | 松樹尾   |
| LPN  | 黑橋街   | LCL  | 聖方濟各堂 |
| LSP  | 石排灣   |      |         |

## 安裝依賴

```bash
pip install requests
```

## 配置 API Key

**重要安全提示**：建議使用環境變量設置 API key，而不是直接寫在代碼中。

### 方法 1：使用環境變量（推薦）

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your_api_key_here"
python smg_image_downloader.py
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
python smg_image_downloader.py
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your_api_key_here
python smg_image_downloader.py
```

### 方法 2：直接在腳本中設置（僅用於開發測試）

在腳本開頭修改：
```python
GEMINI_API_KEY = "your_api_key_here"
```

**注意**：如果使用此方法，請確保不要將包含真實 API key 的代碼提交到公開的版本控制系統。

## 使用方法

### 基本使用

設置 API key 後，直接運行腳本：

```bash
python smg_image_downloader.py
```

### 配置選項

在腳本中可以修改以下配置：

```python
# 循環間隔（分鐘）
INTERVAL_MINUTES = 10

# 圖片保存目錄
SAVE_DIR = "smg_images"

# 分析結果保存目錄
ANALYSIS_SAVE_DIR = "smg_analysis_results"
```

## 工作流程

1. **獲取圖片 URL**：從 SMG API 獲取最新的街道圖片 URL
2. **下載圖片**：下載圖片到本地 `smg_images/` 目錄
3. **Gemini 分析**：將圖片上傳到 Gemini API 並使用固定提示詞分析
4. **保存結果**：將分析結果保存到 `smg_analysis_results/` 目錄
5. **循環執行**：等待指定時間後重複上述步驟

## 輸出文件

### 圖片文件

保存在 `smg_images/` 目錄，文件命名格式：

```
{地點代號}_{時間戳}.jpg
例如: LMF_20250128_143025.jpg
```

### 分析結果

保存在 `smg_analysis_results/` 目錄，文件命名格式：

```
{地點代號}_{時間戳}_analysis.txt
例如: LMF_20250128_143025_analysis.txt
```

分析結果文件內容示例：

```
地點: LMF (花地瑪)
時間: 2025-01-28T14:30:25
圖片路徑: smg_images/LMF_20250128_143025.jpg
分析狀態: 成功
--------------------------------------------------------------------------------
水浸情況分析:
根據圖片分析，這個地點目前沒有明顯的水浸跡象。街道乾燥，沒有積水...
================================================================================
```

## 提示詞

使用的固定提示詞為：

```
分析這張圖片裡面的水浸情況如何
```

Gemini API 會根據這個提示詞分析圖片中的水浸情況，包括：
- 是否有積水
- 積水程度
- 受影響區域
- 可能的風險等級

## API 說明

### SMG API

- **端點**：`https://cms.smg.gov.mo/zh_TW/api/imageseries/ftgmsCamera{group}`
- **方法**：GET
- **返回**：JSON 格式的圖片信息列表

### Gemini API

- **端點**：`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent`
- **方法**：POST
- **模型**：gemini-2.0-flash-exp
- **功能**：圖片理解和分析

## 錯誤處理

腳本包含完整的錯誤處理機制：

- ✅ API 請求超時處理
- ✅ 網絡錯誤重試
- ✅ 文件保存失敗處理
- ✅ 鍵盤中斷處理（Ctrl+C）
- ✅ 詳細的錯誤日誌輸出
- ✅ API key 遮蔽保護

## 安全注意事項

⚠️ **重要安全提示**：

1. **API 密鑰保護**：
   - ✅ 優先使用環境變量存儲 API key
   - ✅ 不要將包含真實 API key 的代碼提交到公開倉庫
   - ✅ 腳本已實現 API key 遮蔽功能，日誌中只顯示最後 4 位
   - ⚠️ 定期輪換 API key，特別是當懷疑已洩露時

2. **數據隱私**：
   - 下載的街道圖片可能包含個人隱私信息
   - 請遵守當地數據保護法規
   - 建議定期清理舊數據

3. **網絡安全**：
   - 使用 HTTPS 加密通信
   - 如在受限網絡環境，建議使用受信任的代理

## 其他注意事項

1. **請求頻率**：建議設置合理的循環間隔（10 分鐘以上），避免過度請求
2. **存儲空間**：長時間運行會累積大量圖片和分析結果，注意監控磁盤空間
3. **網絡連接**：需要穩定的網絡連接訪問 SMG 和 Gemini API

## 停止程序

按 `Ctrl+C` 可以安全地停止程序。

## 故障排除

### 問題：無法連接到 Gemini API

```
✗ Gemini 分析失敗: 400 FAILED_PRECONDITION
User location is not supported for the API use.
```

**解決方案**：如果您在中國大陸，需要配置代理才能訪問 Gemini API。

### 問題：requests 模塊未找到

```
[錯誤] 'requests' 庫未安裝。
```

**解決方案**：運行 `pip install requests` 安裝依賴。

### 問題：磁盤空間不足

**解決方案**：定期清理舊的圖片和分析結果文件。

## 授權

本項目使用的 API：
- SMG API：澳門氣象局公開 API
- Gemini API：Google AI 服務

## 貢獻

歡迎提交 Issue 和 Pull Request！
