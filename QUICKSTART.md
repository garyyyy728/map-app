# SMG 圖片下載器 - 快速開始指南

## 🚀 快速開始（2 步驟）

### 步驟 1: 安裝依賴

```bash
pip install requests transformers torch pillow
```

或使用 requirements.txt：

```bash
pip install -r requirements.txt
```

**注意**：首次運行時會自動下載 HuggingFace 模型（約 500MB），請確保網絡連接穩定。

### 步驟 2: 運行程序

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
水浸檢測結果: non-flooded
置信度: 95.23%

所有類別的概率:
  - non-flooded: 95.23%
  - flooded: 4.77%
================================================================================
```

## 💡 提示

- 首次運行會下載 HuggingFace 模型（約 500MB），請耐心等待
- 建議先用 `test_smg_downloader.py` 測試單個地點
- 如果有 GPU，推理速度會更快
- 長時間運行會累積大量文件，建議定期清理舊數據

## 📚 更多文檔

- **完整使用說明**: 查看 `SMG_DOWNLOADER_README.md`
- **代碼說明**: 查看 `smg_image_downloader.py` 中的註釋

## ❓ 常見問題

### Q: 首次運行很慢？
A: 第一次運行需要下載模型（約 500MB），請耐心等待

### Q: 無法連接到 SMG 網站？
A: 檢查網絡連接，SMG API 可能暫時不可用

### Q: 模型載入失敗？
A: 確保已安裝所有依賴：`pip install -r requirements.txt`

### Q: 如何只分析特定地點？
A: 在代碼中修改 `CAMERA_GROUPS` 列表，只保留需要的地點代號

## 🎉 完成！

現在您可以開始使用 SMG 圖片下載器了！
