"""
SMG 街道图片监控与水浸分析系统（简化版）
直接使用 Gemini API，无需 FastAPI 服务
"""
import requests
import time
import os
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ==================== 配置区域 ====================

# 循环间隔（分钟）
INTERVAL_MINUTES = 10

# API 模板
API_URL_TEMPLATE = "https://cms.smg.gov.mo/zh_TW/api/imageseries/ftgmsCamera{group}"
BASE_HOST = "https://cms.smg.gov.mo"

# 所有地点的代号列表
CAMERA_GROUPS = [
    "LTA", "LSP", "LSI", "LRR", "LPN", "LPM", "LPI", "LPH", "LPF",
    "LMM", "LIV", "LIL", "LHO", "LHK", "LCS", "LCL", "LCH", "LAO", "LMF",
]

# 中文名称映射
LOCATION_NAMES = {
    "LMF": "花地瑪", "LSI": "內港北", "LPI": "內港", "LHK": "康公廟",
    "LPH": "司打口", "LPF": "內港南", "LPM": "下環街", "LIV": "青洲河邊馬路",
    "LMM": "紅街市", "LRR": "光復街", "LTA": "永樂戲院", "LHO": "菜園路",
    "LCH": "沙維斯街", "LAO": "柯維納馬路", "LIL": "益隆", "LCS": "松樹尾",
    "LPN": "黑橋街", "LCL": "聖方濟各堂", "LSP": "石排灣",
}

# 保存目录
SAVE_DIR = "smg_images"
ANALYSIS_DIR = "flood_analysis"

# 固定的分析提示词
FLOOD_ANALYSIS_PROMPT = "分析這張圖片裡面的水浸情況如何"

# Gemini API 配置
GEMINI_API_KEY = "AIzaSyBUU2MYPMqc9NHanRp68tRCJsUb5wWA1wU"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"

# ==================== 函数定义 ====================


def ensure_directories():
    """确保必要的目录存在"""
    os.makedirs(SAVE_DIR, exist_ok=True)
    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    logger.info(f"目录检查完成: {SAVE_DIR}, {ANALYSIS_DIR}")


def get_image_url(group_code):
    """获取最新图片的 URL"""
    api_url = API_URL_TEMPLATE.format(group=group_code)
    
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            latest_image = data[0]
            image_path = latest_image.get("path", "")
            
            if image_path:
                full_url = f"{BASE_HOST}{image_path}"
                logger.info(f"[{group_code}] 获取到图片 URL: {full_url}")
                return full_url
        
        logger.warning(f"[{group_code}] API 返回数据格式异常")
        return None
        
    except Exception as e:
        logger.error(f"[{group_code}] 获取图片 URL 失败: {e}")
        return None


def download_image(group_code, url):
    """下载图片并保存"""
    try:
        location_name = LOCATION_NAMES.get(group_code, group_code)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{group_code}_{location_name}_{timestamp}.jpg"
        filepath = os.path.join(SAVE_DIR, filename)
        
        logger.info(f"[{group_code}] 开始下载图片...")
        
        response = requests.get(url, timeout=15, stream=True)
        response.raise_for_status()
        
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(filepath) / 1024
        logger.info(f"[{group_code}] ✅ 下载成功: {filename} ({file_size:.1f} KB)")
        
        return filepath
        
    except Exception as e:
        logger.error(f"[{group_code}] 下载失败: {e}")
        return None


def analyze_flood_with_gemini(image_path):
    """使用 Gemini API 分析图片中的水浸情况"""
    try:
        logger.info(f"开始分析图片: {os.path.basename(image_path)}")
        
        # 读取图片并转换为 base64
        import base64
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # 构建请求
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": FLOOD_ANALYSIS_PROMPT},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_data
                        }
                    }
                ]
            }]
        }
        
        # 发送请求
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        
        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                text = candidate["content"]["parts"][0].get("text", "")
                logger.info(f"✅ 分析完成: {os.path.basename(image_path)}")
                return text
        
        logger.warning(f"分析响应格式异常: {result}")
        return None
        
    except Exception as e:
        logger.error(f"❌ 分析失败: {e}")
        return None


def save_analysis_result(group_code, image_path, analysis):
    """保存分析结果到文件"""
    try:
        location_name = LOCATION_NAMES.get(group_code, group_code)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{group_code}_{location_name}_{timestamp}_分析.txt"
        filepath = os.path.join(ANALYSIS_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"地点代号: {group_code}\n")
            f.write(f"地点名称: {location_name}\n")
            f.write(f"图片文件: {os.path.basename(image_path)}\n")
            f.write(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"提示词: {FLOOD_ANALYSIS_PROMPT}\n")
            f.write(f"\n{'='*60}\n")
            f.write(f"分析结果:\n")
            f.write(f"{'='*60}\n\n")
            f.write(analysis)
        
        logger.info(f"✅ 分析结果已保存: {filename}")
        
    except Exception as e:
        logger.error(f"❌ 保存分析结果失败: {e}")


def process_all_cameras():
    """处理所有摄像头：下载图片并分析"""
    logger.info(f"\n{'='*60}")
    logger.info(f"开始新一轮监控 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"{'='*60}\n")
    
    success_count = 0
    
    for group_code in CAMERA_GROUPS:
        location_name = LOCATION_NAMES.get(group_code, group_code)
        logger.info(f"\n处理地点: {location_name} ({group_code})")
        logger.info("-" * 40)
        
        # 1. 获取图片 URL
        image_url = get_image_url(group_code)
        if not image_url:
            logger.warning(f"[{group_code}] 跳过：无法获取图片 URL")
            continue
        
        # 2. 下载图片
        image_path = download_image(group_code, image_url)
        if not image_path:
            logger.warning(f"[{group_code}] 跳过：图片下载失败")
            continue
        
        # 3. 使用 Gemini 分析水浸情况
        analysis = analyze_flood_with_gemini(image_path)
        if not analysis:
            logger.warning(f"[{group_code}] 跳过：AI 分析失败")
            continue
        
        # 4. 保存分析结果
        save_analysis_result(group_code, image_path, analysis)
        
        success_count += 1
        
        # 短暂延迟，避免请求过快
        time.sleep(2)
    
    logger.info(f"\n{'='*60}")
    logger.info(f"本轮监控完成: 成功处理 {success_count}/{len(CAMERA_GROUPS)} 个地点")
    logger.info(f"{'='*60}\n")
    
    return success_count


def main():
    """主程序入口"""
    # 确保目录存在
    ensure_directories()
    
    logger.info(f"\n🚀 SMG 水浸监控系统启动（简化版）")
    logger.info(f"监控间隔: {INTERVAL_MINUTES} 分钟")
    logger.info(f"监控地点: {len(CAMERA_GROUPS)} 个")
    logger.info(f"图片保存目录: {SAVE_DIR}")
    logger.info(f"分析结果目录: {ANALYSIS_DIR}")
    logger.info(f"\n按 Ctrl+C 停止监控\n")
    
    try:
        # 首次运行
        process_all_cameras()
        
        # 循环监控
        while True:
            next_run = datetime.now().timestamp() + (INTERVAL_MINUTES * 60)
            next_run_time = datetime.fromtimestamp(next_run).strftime('%Y-%m-%d %H:%M:%S')
            
            logger.info(f"\n⏰ 等待下一轮监控...")
            logger.info(f"下次运行时间: {next_run_time}")
            
            time.sleep(INTERVAL_MINUTES * 60)
            
            process_all_cameras()
            
    except KeyboardInterrupt:
        logger.info("\n\n👋 监控系统已停止")
    except Exception as e:
        logger.error(f"\n\n❌ 系统错误: {e}")


if __name__ == "__main__":
    main()
