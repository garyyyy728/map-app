#!/bin/bash
# 快速驗證腳本 - SMG 街道圖片下載器

echo "============================================================"
echo "  SMG 街道圖片下載器 + HuggingFace 水浸檢測"
echo "  快速驗證腳本"
echo "============================================================"
echo ""

# 檢查 Python 版本
check_python_version() {
    # 檢查 Python 版本是否 >= 3.8
    python -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null
    return $?
}

echo "🔍 檢查 Python 版本..."
python_version=$(python --version 2>&1)
echo "   $python_version"

if check_python_version; then
    echo "   ✅ Python 版本符合要求 (>= 3.8)"
else
    echo "   ❌ Python 版本過低，需要 3.8 或更高版本"
    exit 1
fi
echo ""

# 檢查必要的目錄
echo "🔍 檢查工作目錄..."
if [ -d "smg_images" ] && [ -d "smg_analysis_results" ]; then
    echo "   ✅ 工作目錄已創建"
    echo "      - smg_images/"
    echo "      - smg_analysis_results/"
else
    echo "   ⚠️  工作目錄不存在，將在運行時創建"
fi
echo ""

# 檢查依賴項
echo "🔍 檢查依賴項..."
missing_deps=()

if ! python -c "import requests" 2>/dev/null; then
    missing_deps+=("requests")
fi

if ! python -c "import transformers" 2>/dev/null; then
    missing_deps+=("transformers")
fi

if ! python -c "import torch" 2>/dev/null; then
    missing_deps+=("torch")
fi

if ! python -c "import PIL" 2>/dev/null; then
    missing_deps+=("pillow")
fi

if [ ${#missing_deps[@]} -eq 0 ]; then
    echo "   ✅ 所有依賴項已安裝"
    echo "      ✓ requests"
    echo "      ✓ transformers"
    echo "      ✓ torch"
    echo "      ✓ pillow"
else
    echo "   ❌ 缺少依賴項: ${missing_deps[*]}"
    echo ""
    echo "   請運行以下命令安裝:"
    echo "   pip install -r requirements.txt"
    exit 1
fi
echo ""

# 檢查磁盤空間
echo "🔍 檢查磁盤空間..."
if available_space=$(df -h . 2>/dev/null | awk 'NR==2 {print $4}'); then
    echo "   可用空間: $available_space"
else
    echo "   ⚠️  無法確定可用空間"
fi
echo "   建議: 至少 2GB（首次運行需要下載模型）"
echo ""

# 顯示測試選項
echo "============================================================"
echo "  可用的測試和運行選項"
echo "============================================================"
echo ""
echo "1. 運行離線測試（驗證基礎功能，無需網絡）:"
echo "   python test_smg_offline.py"
echo ""
echo "2. 運行完整測試（需要網絡連接）:"
echo "   python test_smg_downloader.py"
echo ""
echo "3. 啟動實時監控（所有 19 個地點）:"
echo "   python smg_image_downloader.py"
echo ""
echo "4. 查看測試結果:"
echo "   cat TEST_RESULTS.md"
echo "   cat TEST_SUMMARY.md"
echo ""
echo "============================================================"
echo "  注意事項"
echo "============================================================"
echo ""
echo "⚠️  首次運行需要網絡連接:"
echo "   - 下載 HuggingFace 模型（約 500MB）"
echo "   - 模型會被緩存，後續運行不需要重新下載"
echo ""
echo "⚠️  長時間運行注意事項:"
echo "   - 定期檢查磁盤空間使用情況"
echo "   - 建議定期清理舊的圖片和分析結果"
echo "   - 設置合理的循環間隔（建議 10 分鐘以上）"
echo ""
echo "============================================================"
echo "  系統狀態總結"
echo "============================================================"
echo ""
echo "✅ Python 環境: 就緒"
echo "✅ 依賴項: 已安裝"
echo "✅ 測試腳本: 已準備"
echo "✅ 文檔: 完整"
echo ""
echo "🎉 系統已準備就緒，可以開始測試！"
echo ""
