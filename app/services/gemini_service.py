"""
Gemini API 服务层
"""
from google import genai
from typing import Optional, List, Dict, Any
import logging
import os
import httpx

logger = logging.getLogger(__name__)


class GeminiService:
    """Gemini API 服务类"""
    
    def __init__(self, api_key: str, http_proxy: str = "", https_proxy: str = ""):
        """
        初始化 Gemini 服务
        
        Args:
            api_key: Gemini API 密钥
            http_proxy: HTTP 代理地址（可选）
            https_proxy: HTTPS 代理地址（可选）
        """
        if not api_key:
            raise ValueError("Gemini API key is required")
        
        # 设置代理环境变量（如果提供）
        if http_proxy:
            os.environ["HTTP_PROXY"] = http_proxy
            os.environ["http_proxy"] = http_proxy
            logger.info(f"设置 HTTP 代理: {http_proxy}")
        
        if https_proxy:
            os.environ["HTTPS_PROXY"] = https_proxy
            os.environ["https_proxy"] = https_proxy
            logger.info(f"设置 HTTPS 代理: {https_proxy}")
        
        # 初始化 Gemini 客户端，配置代理
        if http_proxy or https_proxy:
            # 构建代理配置
            proxy_url = https_proxy or http_proxy
            logger.info(f"使用代理配置 Gemini 客户端: {proxy_url}")
            
            # 方法 1: 使用 client_args 传递代理配置
            # 这会让 genai.Client 内部创建的 httpx 客户端使用代理
            self.client = genai.Client(
                api_key=api_key,
                http_options={
                    'client_args': {'proxy': proxy_url},
                    'async_client_args': {'proxy': proxy_url}
                }
            )
        else:
            self.client = genai.Client(api_key=api_key)
        
        # 使用更快的模型作为默认
        self.default_model = "gemini-2.0-flash-exp"
    
    async def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        生成文本
        
        Args:
            prompt: 输入提示词
            model: 模型名称（可选）
            temperature: 温度参数，控制随机性 (0-2)
            max_tokens: 最大生成词元数
            
        Returns:
            生成的文本内容
        """
        try:
            model_name = model or self.default_model
            
            config = {
                "temperature": temperature,
            }
            if max_tokens:
                config["max_output_tokens"] = max_tokens
            
            response = self.client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config,
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 1.0,
    ) -> str:
        """
        对话接口
        
        Args:
            messages: 对话历史，格式为 [{"role": "user", "content": "..."}, ...]
            model: 模型名称（可选）
            temperature: 温度参数
            
        Returns:
            AI 回复内容
        """
        try:
            model_name = model or self.default_model
            
            # 构建对话内容
            contents = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })
            
            config = {"temperature": temperature}
            
            response = self.client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            raise
    
    async def analyze_image(
        self,
        image_data: bytes,
        prompt: str = "描述这张图片",
        model: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> str:
        """
        分析图片
        
        Args:
            image_data: 图片的二进制数据
            prompt: 提示词
            model: 模型名称（可选）
            timeout: 请求超时时间（秒），默认使用客户端配置
            
        Returns:
            分析结果
        """
        try:
            # 优先使用快速模型进行图片分析
            model_name = model or "gemini-2.0-flash-exp"
            
            logger.info(f"开始图片分析，使用模型: {model_name}, 图片大小: {len(image_data)} bytes")
            
            # 使用 Gemini API 的图片理解功能
            # 添加配置以优化响应速度
            config = {
                "temperature": 0.4,  # 降低温度以获得更快、更一致的响应
            }
            
            response = self.client.models.generate_content(
                model=model_name,
                contents=[
                    prompt,
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_data
                        }
                    }
                ],
                config=config,
            )
            
            logger.info("图片分析完成")
            return response.text
            
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            raise
    
    def list_models(self) -> List[str]:
        """
        列出可用的模型
        
        Returns:
            模型名称列表
        """
        try:
            models = self.client.models.list()
            return [model.name for model in models]
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            # 返回默认的已知模型列表（按速度排序）
            return [
                "gemini-2.0-flash-exp",      # 最快（实验版）
                "gemini-2.5-flash",          # 快速
                "gemini-2.5-flash-lite",     # 轻量
                "gemini-2.5-pro",            # 强大但较慢
            ]

