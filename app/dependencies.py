"""
FastAPI 依赖注入
"""
from functools import lru_cache
from services.doubao_service import DoubaoService
from config import get_settings


@lru_cache()
def get_doubao_service() -> DoubaoService:
    """
    获取豆包服务实例（单例模式）
    
    Returns:
        DoubaoService 实例
    """
    settings = get_settings()
    return DoubaoService(
        api_key=settings.doubao_api_key,
        base_url=settings.doubao_base_url,
        http_proxy=settings.http_proxy,
        https_proxy=settings.https_proxy
    )

