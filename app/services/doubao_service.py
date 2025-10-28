"""
豆包 API 服务层
"""
from openai import OpenAI
from typing import Optional, List, Dict, Any
import logging
import base64

logger = logging.getLogger(__name__)


class DoubaoService:
    """豆包 API 服务类"""
    
    def __init__(self, api_key: str, base_url: str, http_proxy: str = "", https_proxy: str = ""):
        """
        初始化豆包服务
        
        Args:
            api_key: 豆包 API 密钥
            base_url: API 基础地址
            http_proxy: HTTP 代理地址（可选）
            https_proxy: HTTPS 代理地址（可选）
        """
        if not api_key:
            raise ValueError("Doubao API key is required")
        
        # 配置代理
        proxy_config = None
        if http_proxy or https_proxy:
            proxy_url = https_proxy or http_proxy
            proxy_config = {
                "http://": proxy_url,
                "https://": proxy_url
            }
            logger.info(f"使用代理配置豆包客户端: {proxy_url}")
        
        # 初始化 OpenAI 客户端（豆包兼容 OpenAI 接口）
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            http_client=None if not proxy_config else None  # OpenAI SDK 会自动使用系统代理
        )
        
        # 使用豆包的默认模型
        self.default_model = "doubao-1.5-pro-32k"
    
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
            
            messages = [
                {"role": "user", "content": prompt}
            ]
            
            kwargs = {
                "model": model_name,
                "messages": messages,
                "temperature": temperature,
            }
            
            if max_tokens:
                kwargs["max_tokens"] = max_tokens
            
            response = self.client.chat.completions.create(**kwargs)
            
            return response.choices[0].message.content
            
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
            
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
            )
            
            return response.choices[0].message.content
            
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
            # 使用支持视觉的模型
            model_name = model or "doubao-vision-pro-32k"
            
            logger.info(f"开始图片分析，使用模型: {model_name}, 图片大小: {len(image_data)} bytes")
            
            # 将图片转换为 base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # 构建消息
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
            
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.4,
            )
            
            logger.info("图片分析完成")
            return response.choices[0].message.content
            
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
            # 豆包常用模型列表
            return [
                "doubao-1.5-pro-32k",           # 主力模型（32k上下文）
                "doubao-1.5-pro-256k",          # 长文本模型（256k上下文）
                "doubao-lite-32k",              # 轻量模型
                "doubao-vision-pro-32k",        # 视觉模型
            ]
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            return [
                "doubao-1.5-pro-32k",
                "doubao-vision-pro-32k",
            ]

