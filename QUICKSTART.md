# SMG 圖片下載器 - 快速開始指南

## 📋 您的 API Key

已提供的 Gemini API Key：`AIzaSyBUU2MYPMqc9NHanRp68tRCJsUb5wWA1wU`

## 🚀 快速開始（3 步驟）

### 步驟 1: 設置 API Key

**Linux/Mac:**
```bash
export GEMINI_API_KEY="AIzaSyBUU2MYPMqc9NHanRp68tRCJsUb5wWA1wU"
```

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY="AIzaSyBUU2MYPMqc9NHanRp68tRCJsUb5wWA1wU"
```

**Windows CMD:**
```cmd
set GEMINI_API_KEY=AIzaSyBUU2MYPMqc9NHanRp68tRCJsUb5wWA1wU
```

### 步驟 2: 安裝依賴

```bash
pip install requests
```

### 步驟 3: 運行程序

**測試運行（推薦先測試）:**
```bash
python test_smg_downloader.py
```

**正式運行:**
```bash
python smg_image_downloader.py
```

## 📁 輸出文件

程序會創建兩個目錄：

1. **`smg_images/`** - 存放下載的街道圖片
   - 格式：`{地點代號}_{時間戳}.jpg`
   - 例如：`LMF_20250128_143025.jpg`

2. **`smg_analysis_results/`** - 存放 Gemini 分析結果
   - 格式：`{地點代號}_{時間戳}_analysis.txt`
   - 例如：`LMF_20250128_143025_analysis.txt`

## 🎯 功能說明

程序會：
1. 每 10 分鐘循環一次（可在代碼中修改 `INTERVAL_MINUTES`）
2. 從 19 個澳門地點獲取實時街道圖片
3. 使用 Gemini API 分析每張圖片的水浸情況
4. 自動保存圖片和分析結果

## 🛑 停止程序

按 `Ctrl + C` 可以安全停止程序。

## ⚙️ 配置選項

在 `smg_image_downloader.py` 中可以修改：

```python
# 循環間隔（分鐘）
INTERVAL_MINUTES = 10  # 改為 5 則每 5 分鐘運行一次

# 圖片保存目錄
SAVE_DIR = "smg_images"  # 可改為其他目錄名

# 分析結果保存目錄
ANALYSIS_SAVE_DIR = "smg_analysis_results"  # 可改為其他目錄名
```

## 🔍 查看分析結果

分析結果文件示例：

```text
地點: LMF (花地瑪)
時間: 2025-01-28T14:30:25
圖片路徑: smg_images/LMF_20250128_143025.jpg
分析狀態: 成功
--------------------------------------------------------------------------------
水浸情況分析:
根據圖片分析，這個地點目前沒有明顯的水浸跡象。街道乾燥，沒有看到任何積水...
================================================================================
```

## 💡 提示

- 首次運行建議先用 `test_smg_downloader.py` 測試單個地點
- 如果在中國大陸，可能需要配置代理訪問 Gemini API
- 長時間運行會累積大量文件，建議定期清理舊數據

## 📚 更多文檔

- **完整使用說明**: 查看 `SMG_DOWNLOADER_README.md`
- **安全指南**: 查看 `SECURITY.md`
- **代碼說明**: 查看 `smg_image_downloader.py` 中的註釋

## ❓ 常見問題

### Q: 提示 API Key 未設置？
A: 確保已設置環境變量 `GEMINI_API_KEY`

### Q: 無法連接到 SMG 網站？
A: 檢查網絡連接，SMG API 可能暫時不可用

### Q: Gemini API 返回錯誤？
A: 檢查 API Key 是否正確，是否有使用額度

### Q: 如何只分析特定地點？
A: 在代碼中修改 `CAMERA_GROUPS` 列表，只保留需要的地點代號

## 🎉 完成！

現在您可以開始使用 SMG 圖片下載器了！
