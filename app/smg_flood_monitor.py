"""
SMG 街道图片监控与水浸分析系统
实时获取澳门气象地球物理局的街道摄像头图片，并使用 Gemini AI 分析水浸情况
"""
import requests
import time
import os
from datetime import datetime
from services.gemini_service import GeminiService
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

# API 模板 - 从 F12 开发者工具中找到的隐藏 API
API_URL_TEMPLATE = "https://cms.smg.gov.mo/zh_TW/api/imageseries/ftgmsCamera{group}"
BASE_HOST = "https://cms.smg.gov.mo"

# 所有地点的代号列表
CAMERA_GROUPS = [
    "LTA", "LSP", "LSI", "LRR", "LPN", "LPM", "LPI", "LPH", "LPF",
    "LMM", "LIV", "LIL", "LHO", "LHK", "LCS", "LCL", "LCH", "LAO", "LMF",
]

# 中文名称映射
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

# 图片保存文件夹
SAVE_DIR = "smg_images"

# 水浸分析结果保存文件夹
ANALYSIS_DIR = "flood_analysis"

# 固定的分析提示词
FLOOD_ANALYSIS_PROMPT = "分析這張圖片裡面的水浸情況如何"

# Gemini API Key
GEMINI_API_KEY = "AIzaSyBUU2MYPMqc9NHanRp68tRCJsUb5wWA1wU"

# ==================== 函数定义 ====================


def ensure_directories():
    """确保必要的目录存在"""
    os.makedirs(SAVE_DIR, exist_ok=True)
    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    logger.info(f"目录检查完成: {SAVE_DIR}, {ANALYSIS_DIR}")


def get_image_url(group_code):
    """
    通过 API 获取最新图片的 URL
    
    Args:
        group_code: 地点代号 (如 "LMF", "LTA", ...)
        
    Returns:
        图片 URL 或 None
    """
    api_url = API_URL_TEMPLATE.format(group=group_code)
    
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 从 API 响应中提取图片路径
        if isinstance(data, list) and len(data) > 0:
            # 获取最新的图片（第一个）
            latest_image = data[0]
            image_path = latest_image.get("path", "")
            
            if image_path:
                # 拼接完整 URL
                full_url = f"{BASE_HOST}{image_path}"
                logger.info(f"[{group_code}] 获取到图片 URL: {full_url}")
                return full_url
        
        logger.warning(f"[{group_code}] API 返回数据格式异常")
        return None
        
    except Exception as e:
        logger.error(f"[{group_code}] 获取图片 URL 失败: {e}")
        return None


def download_image(group_code, url):
    """
    下载图片并保存
    
    Args:
        group_code: 地点代号
        url: 图片 URL
        
    Returns:
        保存的文件路径或 None
    """
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
        
        file_size = os.path.getsize(filepath) / 1024  # KB
        logger.info(f"[{group_code}] ✅ 下载成功: {filename} ({file_size:.1f} KB)")
        
        return filepath
        
    except Exception as e:
        logger.error(f"[{group_code}] 下载失败: {e}")
        return None


def analyze_flood_with_gemini(image_path, gemini_service):
    """
    使用 Gemini AI 分析图片中的水浸情况
    
    Args:
        image_path: 图片文件路径
        gemini_service: GeminiService 实例
        
    Returns:
        分析结果文本或 None
    """
    try:
        logger.info(f"开始分析图片: {os.path.basename(image_path)}")
        
        # 读取图片数据
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # 使用 Gemini 分析（同步调用异步函数）
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        analysis = loop.run_until_complete(
            gemini_service.analyze_image(
                image_data=image_data,
                prompt=FLOOD_ANALYSIS_PROMPT,
                model="gemini-2.0-flash-exp"
            )
        )
        
        loop.close()
        
        logger.info(f"✅ 分析完成: {os.path.basename(image_path)}")
        return analysis
        
    except Exception as e:
        logger.error(f"❌ 分析失败: {e}")
        return None


def save_analysis_result(group_code, image_path, analysis):
    """
    保存分析结果到文件
    
    Args:
        group_code: 地点代号
        image_path: 图片路径
        analysis: 分析结果
    """
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


def process_all_cameras(gemini_service):
    """
    处理所有摄像头：下载图片并分析
    
    Args:
        gemini_service: GeminiService 实例
        
    Returns:
        成功处理的数量
    """
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
        analysis = analyze_flood_with_gemini(image_path, gemini_service)
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
    # 检查依赖
    try:
        import requests
    except ImportError:
        print("\n❌ 错误: 'requests' 库未安装")
        print("请运行: pip install requests")
        return
    
    # 确保目录存在
    ensure_directories()
    
    # 初始化 Gemini 服务
    logger.info("初始化 Gemini AI 服务...")
    try:
        gemini_service = GeminiService(api_key=GEMINI_API_KEY)
        logger.info("✅ Gemini 服务初始化成功")
    except Exception as e:
        logger.error(f"❌ Gemini 服务初始化失败: {e}")
        return
    
    # 启动监控循环
    logger.info(f"\n🚀 SMG 水浸监控系统启动")
    logger.info(f"监控间隔: {INTERVAL_MINUTES} 分钟")
    logger.info(f"监控地点: {len(CAMERA_GROUPS)} 个")
    logger.info(f"图片保存目录: {SAVE_DIR}")
    logger.info(f"分析结果目录: {ANALYSIS_DIR}")
    logger.info(f"\n按 Ctrl+C 停止监控\n")
    
    try:
        # 首次运行
        process_all_cameras(gemini_service)
        
        # 循环监控
        while True:
            next_run = datetime.now().timestamp() + (INTERVAL_MINUTES * 60)
            next_run_time = datetime.fromtimestamp(next_run).strftime('%Y-%m-%d %H:%M:%S')
            
            logger.info(f"\n⏰ 等待下一轮监控...")
            logger.info(f"下次运行时间: {next_run_time}")
            
            time.sleep(INTERVAL_MINUTES * 60)
            
            process_all_cameras(gemini_service)
            
    except KeyboardInterrupt:
        logger.info("\n\n👋 监控系统已停止")
    except Exception as e:
        logger.error(f"\n\n❌ 系统错误: {e}")


if __name__ == "__main__":
    main()
