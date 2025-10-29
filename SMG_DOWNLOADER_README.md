# SMG 街道圖片下載器 + HuggingFace 水浸檢測

這是一個自動從澳門氣象局（SMG）獲取實時街道圖片，並使用 HuggingFace Transformers 模型分析水浸情況的工具。

## 功能特點

- ✅ 自動從 SMG API 獲取 19 個地點的實時街道圖片
- ✅ 使用 HuggingFace 預訓練模型 (Flood-Image-Detection) 檢測水浸
- ✅ 本地推理，無需 API Key
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
pip install requests transformers torch pillow
```

或使用 requirements.txt：

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

無需 API key，直接運行腳本：

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
## 分析結果

使用的 HuggingFace 模型：**prithivMLmods/Flood-Image-Detection**

模型會對圖片進行分類，輸出結果包括：
- 檢測類別（如：flooded, non-flooded 等）
- 置信度百分比
- 所有可能類別的概率分布

## API 說明

### SMG API

- **端點**：`https://cms.smg.gov.mo/zh_TW/api/imageseries/ftgmsCamera{group}`
- **方法**：GET
- **返回**：JSON 格式的圖片信息列表

### HuggingFace 模型

- **模型**：prithivMLmods/Flood-Image-Detection
- **類型**：Image Classification（圖片分類）
- **功能**：水浸檢測
- **推理**：本地推理，無需 API key

## 錯誤處理

腳本包含完整的錯誤處理機制：

- ✅ API 請求超時處理
- ✅ 網絡錯誤處理
- ✅ 模型載入失敗處理
- ✅ 文件保存失敗處理
- ✅ 鍵盤中斷處理（Ctrl+C）
- ✅ 詳細的錯誤日誌輸出

## 注意事項

⚠️ **重要提示**：

1. **系統要求**：
   - Python 3.8 或更高版本
   - 建議使用 GPU 以加快推理速度（可選）
   - 至少 2GB 可用磁盤空間（用於模型緩存）

2. **數據隱私**：
   - 下載的街道圖片可能包含個人隱私信息
   - 請遵守當地數據保護法規
   - 建議定期清理舊數據

3. **網絡連接**：
   - 首次運行需要下載模型（約 500MB）
   - 使用 HTTPS 加密通信
   - 需要穩定的網絡連接訪問 SMG API

## 其他注意事項

1. **請求頻率**：建議設置合理的循環間隔（10 分鐘以上），避免過度請求
2. **存儲空間**：長時間運行會累積大量圖片和分析結果，注意監控磁盤空間（模型緩存約 500MB）
3. **首次啟動**：第一次運行時會自動下載模型，可能需要幾分鐘時間

## 停止程序

按 `Ctrl+C` 可以安全地停止程序。

## 故障排除

### 問題：缺少依賴庫

```
[錯誤] 缺少必要的庫: No module named 'transformers'
```

**解決方案**：安裝所有依賴 `pip install -r requirements.txt`

### 問題：模型載入失敗

```
✗ 模型載入失敗: ...
```

**解決方案**：
1. 檢查網絡連接
2. 確保有足夠的磁盤空間（至少 2GB）
3. 嘗試手動下載模型：`python -c "from transformers import AutoModelForImageClassification; AutoModelForImageClassification.from_pretrained('prithivMLmods/Flood-Image-Detection')"`

**解決方案**：運行 `pip install requests` 安裝依賴。

### 問題：磁盤空間不足

**解決方案**：定期清理舊的圖片和分析結果文件。

## 授權

本項目使用的 API：
- SMG API：澳門氣象局公開 API
- Gemini API：Google AI 服務

## 貢獻

歡迎提交 Issue 和 Pull Request！
