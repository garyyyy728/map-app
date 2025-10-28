"""
数据模型模块
"""
from .requests import (
    GenerateTextRequest,
    ChatMessage,
    ChatRequest,
    ImageAnalyzeRequest,
)
from .responses import (
    BaseResponse,
    GenerateTextResponse,
    ChatResponse,
    ImageAnalyzeResponse,
    ModelsListResponse,
    HealthResponse,
)

__all__ = [
    "GenerateTextRequest",
    "ChatMessage",
    "ChatRequest",
    "ImageAnalyzeRequest",
    "BaseResponse",
    "GenerateTextResponse",
    "ChatResponse",
    "ImageAnalyzeResponse",
    "ModelsListResponse",
    "HealthResponse",
]

