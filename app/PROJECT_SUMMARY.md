# SMG 水浸監控系統 - 項目總結

## 📋 項目概述

根據用戶需求，成功實現了一個自動化的澳門街道圖片監控與水浸分析系統。該系統從澳門氣象地球物理局（SMG）獲取實時街道圖片，並使用 Google Gemini AI 分析水浸情況。

## 🎯 完成的功能

### 1. 核心功能
- ✅ 從 19 個 SMG 攝像頭位置自動下載實時圖片
- ✅ 使用 Gemini AI 分析每張圖片的水浸情況
- ✅ 固定分析提示詞：「分析這張圖片裡面的水浸情況如何」
- ✅ 自動保存圖片和分析結果到本地
- ✅ 可配置的監控間隔（默認 10 分鐘）
- ✅ 支持循環監控和單次運行

### 2. 監控地點（19 個）
```
花地瑪 (LMF)          內港北 (LSI)         內港 (LPI)
康公廟 (LHK)          司打口 (LPH)         內港南 (LPF)
下環街 (LPM)          青洲河邊馬路 (LIV)    紅街市 (LMM)
光復街 (LRR)          永樂戲院 (LTA)       菜園路 (LHO)
沙維斯街 (LCH)        柯維納馬路 (LAO)     益隆 (LIL)
松樹尾 (LCS)          黑橋街 (LPN)         聖方濟各堂 (LCL)
石排灣 (LSP)
```

### 3. 技術實現

#### API 集成
- **SMG API**: `https://cms.smg.gov.mo/zh_TW/api/imageseries/ftgmsCamera{group}`
- **Gemini API**: Google Generative AI (gemini-2.0-flash-exp 模型)
- **API Key**: AIzaSyBUU2MYPMqc9NHanRp68tRCJsUb5wWA1wU

#### 架構設計
```
smg_flood_monitor_simple.py (推薦)
├── 獲取圖片 URL (從 SMG API)
├── 下載圖片 (保存到 smg_images/)
├── Gemini AI 分析 (REST API)
└── 保存結果 (保存到 flood_analysis/)

smg_flood_monitor.py (完整版)
├── 使用 FastAPI GeminiService
└── 更好的服務集成
```

## 📁 項目文件結構

```
app/
├── smg_flood_monitor.py           # 主監控腳本（FastAPI 集成）
├── smg_flood_monitor_simple.py    # 簡化版監控腳本（推薦使用）
├── test_smg_gemini.py             # API 連接測試腳本
├── examples_smg_usage.py          # 7 個使用範例
├── start_smg_monitor.sh           # 快速啟動腳本
├── SMG_FLOOD_MONITOR_README.md    # 詳細使用說明
│
├── config.py                      # 添加了 Gemini API 配置
├── dependencies.py                # 添加了 Gemini 服務依賴注入
├── main.py                        # 註冊了 Gemini 路由
├── requirements.txt               # 添加了 google-genai 依賴
└── .gitignore                     # 更新了排除規則
```

## 🚀 快速開始

### 方法 1: 使用快速啟動腳本（推薦）
```bash
cd app
chmod +x start_smg_monitor.sh
./start_smg_monitor.sh
```

### 方法 2: 直接運行簡化版
```bash
cd app
python smg_flood_monitor_simple.py
```

### 方法 3: 查看使用範例
```bash
cd app
python examples_smg_usage.py
```

## 📝 使用範例

### 範例 1: 基本使用
```python
from smg_flood_monitor_simple import process_all_cameras, ensure_directories

ensure_directories()
success_count = process_all_cameras()
print(f"成功處理 {success_count} 個地點")
```

### 範例 2: 監控特定地點
```python
from smg_flood_monitor_simple import (
    get_image_url, download_image, 
    analyze_flood_with_gemini, save_analysis_result
)

# 只監控花地瑪
group_code = "LMF"
url = get_image_url(group_code)
image_path = download_image(group_code, url)
analysis = analyze_flood_with_gemini(image_path)
save_analysis_result(group_code, image_path, analysis)
```

### 範例 3: 自定義提示詞
```python
# 在腳本中修改
FLOOD_ANALYSIS_PROMPT = "你的自定義提示詞"
```

## 📊 輸出文件

### 圖片文件
```
smg_images/
├── LMF_花地瑪_20241028_165530.jpg
├── LSI_內港北_20241028_165532.jpg
└── ...
```

### 分析結果
```
flood_analysis/
├── LMF_花地瑪_20241028_165530_分析.txt
├── LSI_內港北_20241028_165532_分析.txt
└── ...
```

分析結果文件內容：
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

## 🔧 配置選項

### 在腳本中可配置的參數：

```python
# 監控間隔（分鐘）
INTERVAL_MINUTES = 10

# Gemini API Key
GEMINI_API_KEY = "AIzaSyBUU2MYPMqc9NHanRp68tRCJsUb5wWA1wU"

# 保存目錄
SAVE_DIR = "smg_images"
ANALYSIS_DIR = "flood_analysis"

# 分析提示詞
FLOOD_ANALYSIS_PROMPT = "分析這張圖片裡面的水浸情況如何"

# 監控地點（可以自定義只監控特定地點）
CAMERA_GROUPS = ["LMF", "LPI", "LHK"]  # 或使用完整列表
```

## 🔌 與 FastAPI 服務集成

系統也集成到了 FastAPI 後端，可以通過 API 端點使用：

### 啟動 API 服務
```bash
python main.py
```

### API 端點
- `POST /api/gemini/analyze-image` - 分析上傳的圖片
- `POST /api/gemini/generate` - 生成文本
- `POST /api/gemini/chat` - 對話接口
- `GET /api/gemini/models` - 獲取可用模型列表

訪問 API 文檔：http://localhost:8000/docs

## 📦 依賴項

主要依賴已添加到 `requirements.txt`：
```
requests>=2.31.0        # HTTP 請求
google-genai>=1.0.0     # Gemini AI SDK
fastapi>=0.115.0        # Web 框架
uvicorn[standard]       # ASGI 服務器
python-dotenv>=1.0.0    # 環境變數管理
```

安裝：
```bash
pip install -r requirements.txt
```

## ⚙️ 系統要求

- Python 3.8+
- 網絡連接（訪問 cms.smg.gov.mo 和 Google AI API）
- 磁盤空間（用於保存圖片和分析結果）

## 🔐 安全性

- API Key 已內建在腳本中
- 建議在生產環境使用環境變數管理 API Key
- 添加了 `.gitignore` 防止提交敏感文件
- 輸出目錄不會被 git 追蹤

## 📖 文檔

完整文檔請參閱：
- `SMG_FLOOD_MONITOR_README.md` - 詳細使用指南
- `examples_smg_usage.py` - 7 個實用範例
- 腳本內的註釋和文檔字符串

## 🐛 故障排除

### 問題 1: 無法連接到 SMG API
**解決方案**: 檢查網絡連接，確保可以訪問 `https://cms.smg.gov.mo`

### 問題 2: Gemini API 錯誤
**解決方案**: 
- 檢查 API Key 是否正確
- 檢查 API 配額是否足夠
- 查看日誌了解詳細錯誤

### 問題 3: 圖片下載失敗
**解決方案**:
- 確認目錄有寫入權限
- 檢查磁盤空間

## 🎯 未來改進建議

1. **數據庫集成**: 將分析結果存入數據庫而不是文本文件
2. **Web 界面**: 添加 Web 界面查看實時監控結果
3. **告警系統**: 檢測到嚴重水浸時發送通知
4. **歷史對比**: 對比不同時間點的圖片
5. **統計報告**: 生成水浸趨勢統計報告
6. **多語言支持**: 支持繁體中文、簡體中文、英文等

## 👥 貢獻

本項目為澳門災情互助地圖系統的一部分，旨在提供實時災情監控功能。

## 📄 授權

請遵守 SMG API 和 Google Gemini API 的使用條款。

## 📞 技術支持

如有問題，請參考：
1. `SMG_FLOOD_MONITOR_README.md` 文檔
2. 運行 `python examples_smg_usage.py` 查看範例
3. 運行 `python test_smg_gemini.py` 測試 API 連接

---

**項目完成日期**: 2024-10-28  
**實現者**: GitHub Copilot Agent  
**倉庫**: garyyyy728/map-app
