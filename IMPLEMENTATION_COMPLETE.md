# 🎉 SMG 圖片下載器 + Gemini 水浸分析 - 實施完成！

## ✅ 您的需求已完成

根據您的需求，我已經創建了一個完整的解決方案，可以：

1. ✅ 自動從澳門氣象局（SMG）下載 19 個地點的實時街道圖片
2. ✅ 使用您提供的 Gemini API Key 分析每張圖片
3. ✅ 使用固定提示詞：「分析這張圖片裡面的水浸情況如何」
4. ✅ 自動保存圖片和分析結果

## 📦 已創建的文件

### 主要文件
1. **`smg_image_downloader.py`** - 主程序
   - 自動下載圖片
   - 調用 Gemini API 分析
   - 保存結果
   - 循環執行

2. **`test_smg_downloader.py`** - 測試腳本
   - 用於測試單個地點
   - 驗證功能是否正常

### 文檔文件
3. **`QUICKSTART.md`** - 快速開始指南 ⭐ **從這裡開始！**
   - 包含您的 API Key 設置說明
   - 3 步驟快速開始

4. **`SMG_DOWNLOADER_README.md`** - 完整使用說明
   - 詳細功能介紹
   - 配置選項
   - 故障排除

5. **`SECURITY.md`** - 安全指南
   - API Key 保護
   - 安全最佳實踐

6. **`.gitignore`** - Git 配置
   - 排除圖片和敏感數據

## 🚀 立即開始使用

### 第一步：設置 API Key

您提供的 API Key：`AIzaSyBUU2MYPMqc9NHanRp68tRCJsUb5wWA1wU`

**在終端運行：**

**Mac/Linux:**
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

### 第二步：安裝依賴

```bash
pip install requests
```

### 第三步：運行程序

**測試運行（推薦）：**
```bash
python test_smg_downloader.py
```

**正式運行：**
```bash
python smg_image_downloader.py
```

## 📊 程序運行流程

```
開始
  ↓
檢查 API Key
  ↓
循環（每 10 分鐘）
  ↓
├─ 地點 1 (LTA - 永樂戲院)
│   ├─ 從 SMG API 獲取圖片 URL
│   ├─ 下載圖片 → smg_images/LTA_20250128_143025.jpg
│   ├─ 上傳到 Gemini API
│   ├─ 使用提示詞：「分析這張圖片裡面的水浸情況如何」
│   └─ 保存結果 → smg_analysis_results/LTA_20250128_143025_analysis.txt
│
├─ 地點 2 (LSP - 石排灣)
│   └─ ...（同樣流程）
│
├─ ...（共 19 個地點）
│
└─ 等待 10 分鐘後重複
```

## 📁 輸出示例

### 圖片文件
```
smg_images/
├── LMF_20250128_143025.jpg  (花地瑪)
├── LTA_20250128_143028.jpg  (永樂戲院)
├── LSP_20250128_143031.jpg  (石排灣)
└── ...
```

### 分析結果文件
```
smg_analysis_results/
├── LMF_20250128_143025_analysis.txt
├── LTA_20250128_143028_analysis.txt
└── ...
```

### 分析結果示例內容
```text
地點: LMF (花地瑪)
時間: 2025-01-28T14:30:25
圖片路徑: smg_images/LMF_20250128_143025.jpg
分析狀態: 成功
--------------------------------------------------------------------------------
水浸情況分析:
根據圖片顯示，該地點目前沒有明顯的水浸跡象。街道相對乾燥，沒有看到積水或
水位上升的情況。車輛和行人正常通行，道路狀況良好...
================================================================================
```

## 🎯 監控的 19 個地點

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

## ⚙️ 自定義配置

如果需要修改，在 `smg_image_downloader.py` 中：

```python
# 修改循環間隔（分鐘）
INTERVAL_MINUTES = 10  # 改為 5 則每 5 分鐘一次

# 修改保存目錄
SAVE_DIR = "smg_images"
ANALYSIS_SAVE_DIR = "smg_analysis_results"

# 只監控特定地點（修改這個列表）
CAMERA_GROUPS = [
    "LTA",  # 永樂戲院
    "LMF",  # 花地瑪
    # 註釋掉不需要的地點
]
```

## 🛑 停止程序

按 `Ctrl + C` 即可安全停止。

## 🔒 安全特性

- ✅ API Key 使用環境變量，不直接寫在代碼中
- ✅ 日誌中 API Key 自動遮蔽（只顯示最後 4 位）
- ✅ 所有通信使用 HTTPS 加密
- ✅ 完整的錯誤處理

## 📚 更多信息

- **快速開始**: 查看 `QUICKSTART.md`
- **完整文檔**: 查看 `SMG_DOWNLOADER_README.md`
- **安全指南**: 查看 `SECURITY.md`

## ❓ 常見問題

### Q: 無法連接 Gemini API？
A: 如果您在中國大陸，可能需要配置代理。

### Q: 提示 API Key 未設置？
A: 確保已在當前終端設置環境變量 `GEMINI_API_KEY`。

### Q: 想要修改分析提示詞？
A: 在 `smg_image_downloader.py` 的 `analyze_flood_with_gemini` 函數中，
   找到這行：`{"text": "分析這張圖片裡面的水浸情況如何"}`，
   修改為您想要的提示詞。

### Q: 如何只分析一次，不循環？
A: 使用測試腳本：`python test_smg_downloader.py`

## 🎊 完成！

您的 SMG 圖片下載器已經準備就緒！

**下一步：**
1. 設置環境變量 `GEMINI_API_KEY`
2. 運行 `python test_smg_downloader.py` 測試
3. 運行 `python smg_image_downloader.py` 開始監控

如有任何問題，請查看文檔或創建 GitHub Issue。

祝使用愉快！🚀
