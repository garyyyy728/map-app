#!/bin/bash
# SMG 水浸監控系統 - 快速啟動腳本

echo "============================================================"
echo "   SMG 水浸監控系統 - 快速啟動"
echo "============================================================"
echo ""

# 檢查 Python 是否安裝
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤: Python 3 未安裝"
    echo "請先安裝 Python 3.8 或更高版本"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"
echo ""

# 切換到腳本目錄
cd "$(dirname "$0")"

# 檢查並安裝依賴
echo "檢查依賴..."
if ! python3 -c "import requests" 2>/dev/null; then
    echo "正在安裝 requests..."
    pip3 install requests --user
fi

if ! python3 -c "import google.genai" 2>/dev/null; then
    echo "正在安裝 google-genai..."
    pip3 install google-genai --user
fi

echo "✅ 依賴檢查完成"
echo ""

# 創建必要的目錄
mkdir -p smg_images
mkdir -p flood_analysis

echo "✅ 目錄創建完成"
echo "   - 圖片保存: ./smg_images"
echo "   - 分析結果: ./flood_analysis"
echo ""

# 詢問使用哪個版本
echo "請選擇要運行的版本:"
echo "  1) 簡化版（推薦）- 獨立運行，無需 FastAPI 服務"
echo "  2) 完整版 - 需要 FastAPI 服務"
echo "  3) 僅測試 API 連接"
echo ""
read -p "請輸入選項 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "啟動簡化版監控系統..."
        echo "按 Ctrl+C 停止監控"
        echo ""
        python3 smg_flood_monitor_simple.py
        ;;
    2)
        echo ""
        echo "啟動完整版監控系統..."
        echo "注意: 請確保 FastAPI 服務已運行"
        echo "按 Ctrl+C 停止監控"
        echo ""
        python3 smg_flood_monitor.py
        ;;
    3)
        echo ""
        echo "運行 API 連接測試..."
        echo ""
        python3 test_smg_gemini.py
        ;;
    *)
        echo "無效的選項"
        exit 1
        ;;
esac
