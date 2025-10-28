"""
SMG 街道圖片下載器 + Gemini 水浸分析
自動從澳門氣象局獲取實時街道圖片，並使用 Gemini API 分析水浸情況
"""
import requests
import time
import os
import base64
from datetime import datetime
from typing import Optional, Dict, List

# Gemini API 配置
# 建議使用環境變量: export GEMINI_API_KEY="your_key_here"
# 或者直接在此處設置（僅用於開發測試，生產環境請使用環境變量）
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBUU2MYPMqc9NHanRp68tRCJsUb5wWA1wU")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"

# 循環間隔設置
INTERVAL_MINUTES = 10

# SMG API 模板
API_URL_TEMPLATE = "https://cms.smg.gov.mo/zh_TW/api/imageseries/ftgmsCamera{group}"
BASE_HOST = "https://cms.smg.gov.mo"

# 地點代號列表
CAMERA_GROUPS = [
    "LTA", "LSP", "LSI", "LRR", "LPN", "LPM", "LPI", "LPH", "LPF",
    "LMM", "LIV", "LIL", "LHO", "LHK", "LCS", "LCL", "LCH", "LAO", "LMF",
]

# 中文名稱映射
LOCATION_NAMES = {
    "LMF": "花地瑪",
    "LSI": "內港北",
    "LPI": "內港",
    "LHK": "康公廟",
    "LPH": "司打口",
    "LPF": "內港南",
    "LPM": "下環街",
    "LIV": "青洲河邊馬路",
    "LMM": "紅街市",
    "LRR": "光復街",
    "LTA": "永樂戲院",
    "LHO": "菜園路",
    "LCH": "沙維斯街",
    "LAO": "柯維納馬路",
    "LIL": "益隆",
    "LCS": "松樹尾",
    "LPN": "黑橋街",
    "LCL": "聖方濟各堂",
    "LSP": "石排灣",
}

# 圖片保存文件夾
SAVE_DIR = "smg_images"
ANALYSIS_SAVE_DIR = "smg_analysis_results"


def mask_api_key(url: str) -> str:
    """
    遮蔽 URL 中的 API key 以避免記錄敏感信息
    
    Args:
        url: 包含 API key 的 URL
        
    Returns:
        遮蔽後的 URL
    """
    if "key=" in url:
        parts = url.split("key=")
        if len(parts) == 2:
            return parts[0] + "key=***MASKED***"
    return url


def ensure_directories():
    """確保必要的目錄存在"""
    os.makedirs(SAVE_DIR, exist_ok=True)
    os.makedirs(ANALYSIS_SAVE_DIR, exist_ok=True)


def get_image_url(group: str) -> Optional[str]:
    """
    從 SMG API 獲取最新圖片 URL
    
    Args:
        group: 地點代號 (如 "LMF", "LTA" 等)
        
    Returns:
        圖片完整 URL，如果失敗返回 None
    """
    try:
        api_url = API_URL_TEMPLATE.format(group=group)
        print(f"正在獲取 {group} ({LOCATION_NAMES.get(group, group)}) 的圖片 URL...")
        
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 從 API 響應中提取圖片路徑
        if data and isinstance(data, list) and len(data) > 0:
            image_path = data[0].get("path", "")
            if image_path:
                full_url = BASE_HOST + image_path
                print(f"✓ 獲取成功: {full_url}")
                return full_url
        
        print(f"✗ 未能從 API 響應中提取圖片 URL")
        return None
        
    except Exception as e:
        print(f"✗ 獲取 URL 失敗: {str(e)}")
        return None


def download_image(name: str, url: str) -> Optional[str]:
    """
    下載單張圖片並保存到指定文件夾
    
    Args:
        name: 圖片名稱（地點代號）
        url: 圖片 URL
        
    Returns:
        保存的圖片路徑，如果失敗返回 None
    """
    try:
        print(f"正在下載: {name} ({LOCATION_NAMES.get(name, name)}) ...")
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # 生成帶時間戳的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.jpg"
        filepath = os.path.join(SAVE_DIR, filename)
        
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        print(f"✓ 下載成功: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"✗ 下載失敗: {str(e)}")
        return None


def analyze_flood_with_gemini(image_path: str) -> Optional[Dict]:
    """
    使用 Gemini API 分析圖片中的水浸情況
    
    Args:
        image_path: 圖片文件路徑
        
    Returns:
        分析結果字典，包含分析文本和元數據
    """
    try:
        print(f"正在使用 Gemini 分析圖片: {image_path}")
        
        # 讀取圖片並轉換為 base64
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        
        # 構建請求數據
        request_data = {
            "contents": [
                {
                    "parts": [
                        {"text": "分析這張圖片裡面的水浸情況如何"},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_data
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 1024,
            }
        }
        
        # 發送請求到 Gemini API
        headers = {
            "Content-Type": "application/json",
        }
        
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        
        response = requests.post(
            url,
            json=request_data,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        
        # 提取分析結果
        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                analysis_text = candidate["content"]["parts"][0]["text"]
                
                print(f"✓ 分析完成")
                print(f"分析結果: {analysis_text[:100]}...")
                
                return {
                    "image_path": image_path,
                    "analysis": analysis_text,
                    "timestamp": datetime.now().isoformat(),
                    "success": True
                }
        
        print(f"✗ 未能從 API 響應中提取分析結果")
        return None
        
    except Exception as e:
        print(f"✗ Gemini 分析失敗: {str(e)}")
        return {
            "image_path": image_path,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "success": False
        }


def save_analysis_result(location: str, analysis_result: Dict):
    """
    保存分析結果到文本文件
    
    Args:
        location: 地點代號
        analysis_result: 分析結果字典
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{location}_{timestamp}_analysis.txt"
        filepath = os.path.join(ANALYSIS_SAVE_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"地點: {location} ({LOCATION_NAMES.get(location, location)})\n")
            f.write(f"時間: {analysis_result.get('timestamp', 'N/A')}\n")
            f.write(f"圖片路徑: {analysis_result.get('image_path', 'N/A')}\n")
            f.write(f"分析狀態: {'成功' if analysis_result.get('success') else '失敗'}\n")
            f.write("-" * 80 + "\n")
            
            if analysis_result.get('success'):
                f.write("水浸情況分析:\n")
                f.write(analysis_result.get('analysis', 'N/A'))
            else:
                f.write("錯誤信息:\n")
                f.write(analysis_result.get('error', 'N/A'))
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"✓ 分析結果已保存: {filepath}")
        
    except Exception as e:
        print(f"✗ 保存分析結果失敗: {str(e)}")


def process_single_location(group: str) -> bool:
    """
    處理單個地點：下載圖片並分析
    
    Args:
        group: 地點代號
        
    Returns:
        是否處理成功
    """
    print(f"\n{'='*60}")
    print(f"處理地點: {group} ({LOCATION_NAMES.get(group, group)})")
    print(f"{'='*60}")
    
    # 1. 獲取圖片 URL
    image_url = get_image_url(group)
    if not image_url:
        print(f"跳過 {group}: 無法獲取圖片 URL")
        return False
    
    # 2. 下載圖片
    image_path = download_image(group, image_url)
    if not image_path:
        print(f"跳過 {group}: 圖片下載失敗")
        return False
    
    # 3. 使用 Gemini 分析水浸情況
    analysis_result = analyze_flood_with_gemini(image_path)
    if not analysis_result:
        print(f"跳過 {group}: Gemini 分析失敗")
        return False
    
    # 4. 保存分析結果
    save_analysis_result(group, analysis_result)
    
    print(f"✓ {group} 處理完成")
    return True


def main():
    """主程序入口"""
    # 檢查 requests 庫
    try:
        import requests
    except ImportError:
        print("\n[錯誤] 'requests' 庫未安裝。")
        print("請在您的終端機運行: pip install requests")
        return
    
    # 檢查 API key 是否設置
    if not GEMINI_API_KEY or GEMINI_API_KEY == "":
        print("\n[錯誤] GEMINI_API_KEY 未設置。")
        print("請設置環境變量: export GEMINI_API_KEY='your_api_key'")
        print("或在腳本中直接設置 GEMINI_API_KEY 變量（僅用於開發測試）")
        return
    
    # 確保目錄存在
    ensure_directories()
    
    print("\n" + "=" * 80)
    print("SMG 街道圖片下載器 + Gemini 水浸分析")
    print("=" * 80)
    print(f"圖片保存目錄: {SAVE_DIR}")
    print(f"分析結果保存目錄: {ANALYSIS_SAVE_DIR}")
    print(f"循環間隔: {INTERVAL_MINUTES} 分鐘")
    print(f"地點數量: {len(CAMERA_GROUPS)}")
    print(f"Gemini API Key: {'已設置 (***' + GEMINI_API_KEY[-4:] + ')' if len(GEMINI_API_KEY) > 4 else '已設置'}")
    print("=" * 80 + "\n")
    
    cycle_count = 0
    
    while True:
        cycle_count += 1
        print(f"\n{'#'*80}")
        print(f"開始第 {cycle_count} 次循環")
        print(f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*80}\n")
        
        success_count = 0
        fail_count = 0
        
        # 處理每個地點
        for group in CAMERA_GROUPS:
            try:
                if process_single_location(group):
                    success_count += 1
                else:
                    fail_count += 1
                
                # 在處理地點之間稍作延遲，避免請求過快
                time.sleep(2)
                
            except Exception as e:
                print(f"✗ 處理 {group} 時發生錯誤: {str(e)}")
                fail_count += 1
        
        # 總結本次循環
        print(f"\n{'='*80}")
        print(f"第 {cycle_count} 次循環完成")
        print(f"成功: {success_count} 個地點")
        print(f"失敗: {fail_count} 個地點")
        print(f"下次循環時間: {INTERVAL_MINUTES} 分鐘後")
        print(f"{'='*80}\n")
        
        # 等待指定時間後進行下一次循環
        print(f"等待 {INTERVAL_MINUTES} 分鐘...")
        time.sleep(INTERVAL_MINUTES * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已被用戶中斷")
        print("感謝使用！")
    except Exception as e:
        print(f"\n\n程序發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
