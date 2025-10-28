# SMG 圖片下載器 - 安全文檔

## 概述

本文檔描述 SMG 圖片下載器實施的安全措施和最佳實踐。

## 已實施的安全措施

### 1. API Key 保護

#### 環境變量支持
- ✅ 支持從環境變量 `GEMINI_API_KEY` 讀取 API key
- ✅ 優先使用環境變量，避免在代碼中硬編碼敏感信息
- ✅ 如未設置環境變量，會使用預設值（僅用於開發測試）

#### API Key 遮蔽
- ✅ 實現 `mask_api_key()` 函數，在日誌中遮蔽完整 API key
- ✅ 啟動時只顯示 API key 最後 4 位，格式：`***ABCD`
- ✅ 錯誤日誌中不會暴露完整 API key

#### 示例代碼
```python
# 從環境變量讀取，帶預設值
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "default_key_for_dev")

# 遮蔽 API key 函數
def mask_api_key(url: str) -> str:
    if "key=" in url:
        parts = url.split("key=")
        if len(parts) == 2:
            return parts[0] + "key=***MASKED***"
    return url
```

### 2. 數據保護

#### 本地存儲安全
- ✅ 圖片和分析結果保存在本地目錄
- ✅ 使用 `.gitignore` 排除敏感數據目錄：
  - `smg_images/` - 街道圖片
  - `smg_analysis_results/` - 分析結果
- ✅ 建議定期清理舊數據

#### 數據傳輸安全
- ✅ 所有 API 請求使用 HTTPS 加密
- ✅ SMG API: `https://cms.smg.gov.mo/...`
- ✅ Gemini API: `https://generativelanguage.googleapis.com/...`

### 3. 錯誤處理

#### 完善的異常處理
- ✅ 網絡請求超時處理（10-60秒）
- ✅ API 錯誤響應處理
- ✅ 文件操作異常處理
- ✅ 友好的錯誤信息，不暴露敏感細節

#### 日誌安全
- ✅ 錯誤日誌不包含完整 API key
- ✅ 敏感數據（API responses）僅記錄摘要

### 4. 輸入驗證

#### API Key 驗證
- ✅ 啟動時檢查 API key 是否設置
- ✅ 空 key 時提示用戶設置環境變量

#### 參數驗證
- ✅ 地點代號使用預定義列表，防止注入
- ✅ 文件路徑使用 `os.path.join()` 安全拼接

## 安全最佳實踐

### 對於開發者

1. **使用環境變量**
   ```bash
   # Linux/Mac
   export GEMINI_API_KEY="your_actual_key_here"
   
   # Windows PowerShell
   $env:GEMINI_API_KEY="your_actual_key_here"
   ```

2. **不要提交 API Key**
   - 在提交代碼前，確保 `.gitignore` 包含：
     ```
     .env
     .env.local
     smg_images/
     smg_analysis_results/
     ```

3. **定期輪換 API Key**
   - 建議每 3-6 個月輪換一次
   - 如懷疑 key 洩露，立即輪換

4. **限制 API Key 權限**
   - 在 Google Cloud Console 中限制 API key 使用範圍
   - 只啟用必要的 API（Gemini API）
   - 設置 IP 地址限制（如可能）

### 對於用戶

1. **保護下載的數據**
   - 街道圖片可能包含個人隱私信息
   - 不要公開分享未經審查的圖片
   - 遵守當地數據保護法規（如 GDPR、個資法）

2. **安全的網絡環境**
   - 使用受信任的網絡
   - 如在中國大陸，使用可靠的代理服務
   - 避免在公共 WiFi 上運行

3. **監控使用情況**
   - 定期檢查 API 使用量
   - 注意異常的請求模式
   - 在 Google Cloud Console 設置預算提醒

## CodeQL 安全掃描結果

### 已解決的問題

1. **Clear-text Storage of Sensitive Data**
   - ✅ 實施：使用環境變量存儲 API key
   - ✅ 實施：添加 API key 遮蔽功能
   - ✅ 實施：在 README 中強調安全最佳實踐

2. **Clear-text Logging of Sensitive Data**
   - ✅ 實施：日誌中只顯示 API key 最後 4 位
   - ✅ 實施：URL 中的 key 參數自動遮蔽

### 已評估的誤報

某些 CodeQL 告警將分析結果文本標記為"敏感數據（密碼）"，但實際上這些是：
- 來自 Gemini 的水浸分析文本
- 公開的街道圖片分析
- 不包含任何敏感或私密信息

這些是正常的業務數據，不是安全漏洞。

## 事件響應

### 如果 API Key 洩露

1. **立即行動**
   ```bash
   # 1. 停止運行腳本
   Ctrl+C
   
   # 2. 前往 Google Cloud Console
   # 3. 刪除洩露的 API key
   # 4. 創建新的 API key
   # 5. 更新環境變量
   export GEMINI_API_KEY="new_key_here"
   ```

2. **檢查影響**
   - 查看 API 使用日誌
   - 檢查是否有異常請求
   - 評估潛在的數據暴露

3. **預防措施**
   - 啟用 API key 使用限制
   - 設置更嚴格的 IP 限制
   - 考慮使用更安全的身份驗證方式

## 合規性

### 數據保護法規

本工具處理的數據可能受以下法規約束：

- **GDPR**（歐盟）: 如處理歐盟居民數據
- **個人資料保護法**（中國台灣）
- **個人資料保護法**（澳門）
- 其他當地數據保護法規

### 建議措施

1. **數據最小化**: 只下載和分析必要的圖片
2. **存儲期限**: 定期刪除舊數據（建議 30 天）
3. **訪問控制**: 限制對下載數據的訪問
4. **透明度**: 如公開使用結果，說明數據來源和處理方式

## 更新日誌

### v1.0 (2025-01-28)
- ✅ 初始實現
- ✅ API key 環境變量支持
- ✅ API key 遮蔽功能
- ✅ 完整的錯誤處理
- ✅ 安全文檔

## 聯繫方式

如發現安全問題，請通過以下方式報告：
- 創建 GitHub Issue（對於非敏感問題）
- 私下聯繫項目維護者（對於敏感漏洞）

## 許可證

請參閱主 README 文件的許可證部分。
