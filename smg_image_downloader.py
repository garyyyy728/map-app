"""
SMG 街道圖片下載器 + Moondream 本地視覺模型水浸檢測
自動從澳門氣象局獲取實時街道圖片，並使用 Moondream 本地模型分析水浸情況
"""
import requests
import time
import os
import re
from datetime import datetime
from typing import Optional, Dict, List
from PIL import Image

# Moondream 模型配置
MODEL_NAME = "vikhyatk/moondream2"
model = None
tokenizer = None

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


def load_model():
    """
    載入 Moondream 本地視覺模型
    
    Returns:
        Tuple of (model, tokenizer) if successful, None otherwise
    """
    global model, tokenizer
    
    if model is not None and tokenizer is not None:
        return model, tokenizer
    
    try:
        print("正在載入 Moondream 本地視覺模型...")
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        # 載入 Moondream2 模型
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
            revision="2024-08-26"
        )
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        
        print(f"✓ 模型載入成功: {MODEL_NAME}")
        return model, tokenizer
        
    except Exception as e:
        print(f"✗ 模型載入失敗: {str(e)}")
        return None, None


def mask_api_key(url: str) -> str:
    """
    遮蔽 URL 中的 API key 以避免記錄敏感信息
    （保留此函數以維持向後兼容，但在新版本中不再使用）
    
    Args:
        url: 包含 API key 的 URL
        
    Returns:
        遮蔽後的 URL
    """
    if "key=" in url:
        # 使用正則表達式替換來遮蔽 key 參數，保留其他查詢參數
        return re.sub(r'key=[^&]*', 'key=***MASKED***', url)
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


def analyze_flood_with_model(image_path: str) -> Optional[Dict]:
    """
    使用 Moondream 本地視覺模型分析圖片中的水浸情況
    
    Args:
        image_path: 圖片文件路徑
        
    Returns:
        分析結果字典，包含分析文本和水浸判斷
    """
    try:
        print(f"正在使用 Moondream 模型分析圖片: {image_path}")
        
        # 載入模型（如果尚未載入）
        model_obj, tokenizer_obj = load_model()
        if model_obj is None or tokenizer_obj is None:
            return {
                "image_path": image_path,
                "error": "模型載入失敗",
                "timestamp": datetime.now().isoformat(),
                "success": False
            }
        
        # 載入圖片
        image = Image.open(image_path)
        
        # 使用 Moondream 進行圖片分析
        # 編碼圖片
        enc_image = model_obj.encode_image(image)
        
        # 詢問關於水浸的問題
        flood_question = "請仔細觀察這張圖片，描述是否有水浸（積水、淹水）的情況？如果有水浸，請描述水浸的程度（輕微、中等、嚴重）。"
        flood_analysis = model_obj.answer_question(enc_image, flood_question, tokenizer_obj)
        
        # 詢問詳細的場景描述
        scene_question = "請描述這張圖片中看到的場景，包括道路、建築物、天氣狀況等。"
        scene_description = model_obj.answer_question(enc_image, scene_question, tokenizer_obj)
        
        # 基於回答判斷是否有水浸
        flood_keywords = ["水浸", "積水", "淹水", "洪水", "水災", "flooding", "flooded", "water", "積"]
        analysis_lower = flood_analysis.lower()
        
        # 判斷是否提到水浸
        is_flooded = any(keyword in analysis_lower for keyword in flood_keywords)
        
        # 如果提到了沒有水浸的關鍵字，則判定為無水浸
        no_flood_keywords = ["沒有水浸", "無水浸", "no flooding", "no water", "乾燥", "沒有積水", "沒有淹水"]
        has_no_flood = any(keyword in analysis_lower for keyword in no_flood_keywords)
        
        if has_no_flood:
            is_flooded = False
        
        flood_status = "有水浸" if is_flooded else "無水浸"
        
        # 構建分析文本
        analysis_text = f"{'='*60}\n"
        analysis_text += f"水浸狀態: {flood_status}\n"
        analysis_text += f"{'='*60}\n\n"
        analysis_text += f"【水浸分析】\n{flood_analysis}\n\n"
        analysis_text += f"【場景描述】\n{scene_description}\n"
        
        print(f"✓ 分析完成")
        print(f"水浸狀態: {flood_status}")
        print(f"分析摘要: {flood_analysis[:100]}...")
        
        return {
            "image_path": image_path,
            "analysis": analysis_text,
            "flood_analysis": flood_analysis,
            "scene_description": scene_description,
            "is_flooded": is_flooded,
            "flood_status": flood_status,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
    except Exception as e:
        print(f"✗ 模型分析失敗: {str(e)}")
        import traceback
        traceback.print_exc()
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
            
            # 如果分析成功，顯示水浸狀態
            if analysis_result.get('success'):
                flood_status = analysis_result.get('flood_status', 'N/A')
                f.write(f"\n{'='*80}\n")
                f.write(f"【水浸狀態】: {flood_status}\n")
                f.write(f"{'='*80}\n")
            
            f.write("-" * 80 + "\n")
            
            if analysis_result.get('success'):
                f.write("詳細分析結果:\n")
                f.write(analysis_result.get('analysis', 'N/A'))
            else:
                f.write("錯誤信息:\n")
                f.write(analysis_result.get('error', 'N/A'))
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"✓ 分析結果已保存: {filepath}")
        
    except Exception as e:
        print(f"✗ 保存分析結果失敗: {str(e)}")


def process_single_location(group: str) -> Optional[Dict]:
    """
    處理單個地點：下載圖片並分析
    
    Args:
        group: 地點代號
        
    Returns:
        分析結果字典，如果失敗返回 None
    """
    print(f"\n{'='*60}")
    print(f"處理地點: {group} ({LOCATION_NAMES.get(group, group)})")
    print(f"{'='*60}")
    
    # 1. 獲取圖片 URL
    image_url = get_image_url(group)
    if not image_url:
        print(f"跳過 {group}: 無法獲取圖片 URL")
        return None
    
    # 2. 下載圖片
    image_path = download_image(group, image_url)
    if not image_path:
        print(f"跳過 {group}: 圖片下載失敗")
        return None
    
    # 3. 使用 HuggingFace 模型分析水浸情況
    analysis_result = analyze_flood_with_model(image_path)
    if not analysis_result:
        print(f"跳過 {group}: 模型分析失敗")
        return None
    
    # 4. 保存分析結果
    save_analysis_result(group, analysis_result)
    
    # 5. 顯示處理結果摘要
    if analysis_result.get('success'):
        flood_status = analysis_result.get('flood_status', 'N/A')
        flood_analysis = analysis_result.get('flood_analysis', 'N/A')
        
        print(f"\n{'*'*60}")
        print(f"處理完成摘要:")
        print(f"  地點: {group} ({LOCATION_NAMES.get(group, group)})")
        print(f"  水浸狀態: {flood_status}")
        print(f"  分析摘要: {flood_analysis[:80]}...")
        print(f"{'*'*60}\n")
    
    print(f"✓ {group} 處理完成")
    return analysis_result


def main():
    """主程序入口"""
    # 檢查必要的庫
    try:
        import requests
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from PIL import Image
    except ImportError as e:
        print(f"\n[錯誤] 缺少必要的庫: {e}")
        print("請安裝所需依賴:")
        print("  pip install requests transformers torch pillow")
        return
    
    # 確保目錄存在
    ensure_directories()
    
    # 預先載入模型
    print("\n正在初始化 Moondream 本地視覺模型...")
    model_obj, tokenizer_obj = load_model()
    if model_obj is None or tokenizer_obj is None:
        print("\n[錯誤] 無法載入 Moondream 模型")
        print("請確保已安裝 transformers 庫並且網絡連接正常")
        return
    
    print("\n" + "=" * 80)
    print("SMG 街道圖片下載器 + Moondream 本地視覺模型水浸檢測")
    print("=" * 80)
    print(f"圖片保存目錄: {SAVE_DIR}")
    print(f"分析結果保存目錄: {ANALYSIS_SAVE_DIR}")
    print(f"循環間隔: {INTERVAL_MINUTES} 分鐘")
    print(f"地點數量: {len(CAMERA_GROUPS)}")
    print(f"檢測模型: {MODEL_NAME}")
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
        flooded_locations = []  # 記錄有水浸的地點
        non_flooded_locations = []  # 記錄無水浸的地點
        
        # 處理每個地點
        for group in CAMERA_GROUPS:
            try:
                result = process_single_location(group)
                if result and result.get('success'):
                    success_count += 1
                    # 記錄水浸狀態
                    if result.get('is_flooded'):
                        flooded_locations.append({
                            'location': group,
                            'name': LOCATION_NAMES.get(group, group),
                            'analysis': result.get('flood_analysis', '')[:50]
                        })
                    else:
                        non_flooded_locations.append({
                            'location': group,
                            'name': LOCATION_NAMES.get(group, group)
                        })
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
        
        # 顯示水浸狀態摘要
        print(f"\n{'='*80}")
        print(f"水浸狀態摘要:")
        print(f"{'='*80}")
        
        if flooded_locations:
            print(f"\n⚠️  發現水浸地點 ({len(flooded_locations)} 個):")
            for loc in flooded_locations:
                print(f"  - {loc['location']} ({loc['name']}) - 分析: {loc['analysis']}...")
        else:
            print(f"\n✅ 沒有檢測到水浸地點")
        
        if non_flooded_locations:
            print(f"\n✓ 正常地點 ({len(non_flooded_locations)} 個):")
            for loc in non_flooded_locations:
                print(f"  - {loc['location']} ({loc['name']})")
        
        print(f"\n{'='*80}")
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
