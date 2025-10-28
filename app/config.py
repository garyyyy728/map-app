"""
应用配置模块
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用设置"""
    
    # 豆包 API 配置
    doubao_api_key: str = ""
    doubao_base_url: str = "https://ark.cn-beijing.volces.com/api/v3"
    
    # Gemini API 配置
    gemini_api_key: str = ""
    
    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # API 配置
    api_title: str = "豆包 API 后台服务"
    api_version: str = "1.0.0"
    api_description: str = "基于火山引擎豆包大模型的后台服务"
    
    # CORS 配置
    cors_origins: list[str] = ["*"]
    
    # 代理配置（可选）
    http_proxy: str = ""
    https_proxy: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """获取配置实例（单例模式）"""
    return Settings()

