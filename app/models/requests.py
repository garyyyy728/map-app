"""
API 请求模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class GenerateTextRequest(BaseModel):
    """文本生成请求"""
    prompt: str = Field(..., description="输入提示词", min_length=1)
    model: Optional[str] = Field(None, description="模型名称，默认使用 doubao-1.5-pro-32k")
    temperature: float = Field(1.0, description="温度参数，控制随机性 (0-2)", ge=0, le=2)
    max_tokens: Optional[int] = Field(None, description="最大生成词元数", gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "请用简单的语言解释什么是人工智能",
                "model": "doubao-1.5-pro-32k",
                "temperature": 0.7,
                "max_tokens": 1000
            }
        }


class ChatMessage(BaseModel):
    """聊天消息"""
    role: str = Field(..., description="消息角色：user 或 assistant")
    content: str = Field(..., description="消息内容", min_length=1)


class ChatRequest(BaseModel):
    """对话请求"""
    messages: List[ChatMessage] = Field(..., description="对话历史", min_length=1)
    model: Optional[str] = Field(None, description="模型名称")
    temperature: float = Field(1.0, description="温度参数 (0-2)", ge=0, le=2)
    
    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {"role": "user", "content": "你好，请介绍一下自己"},
                    {"role": "assistant", "content": "你好！我是基于豆包大模型的 AI 助手。"},
                    {"role": "user", "content": "你能做什么？"}
                ],
                "temperature": 0.8
            }
        }


class ImageAnalyzeRequest(BaseModel):
    """图片分析请求"""
    prompt: str = Field("描述这张图片", description="分析提示词")
    model: Optional[str] = Field(None, description="模型名称")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "详细描述这张图片中的内容",
                "model": "doubao-vision-pro-32k"
            }
        }

