"""
API 响应模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class BaseResponse(BaseModel):
    """基础响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field("", description="响应消息")


class GenerateTextResponse(BaseResponse):
    """文本生成响应"""
    text: Optional[str] = Field(None, description="生成的文本内容")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "生成成功",
                "text": "人工智能是一种模拟人类智能的计算机技术..."
            }
        }


class ChatResponse(BaseResponse):
    """对话响应"""
    reply: Optional[str] = Field(None, description="AI 回复内容")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "对话成功",
                "reply": "我可以帮助你回答问题、写作、翻译等任务。"
            }
        }


class ImageAnalyzeResponse(BaseResponse):
    """图片分析响应"""
    analysis: Optional[str] = Field(None, description="图片分析结果")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "分析成功",
                "analysis": "这张图片显示了一个美丽的日落场景..."
            }
        }


class ModelsListResponse(BaseResponse):
    """模型列表响应"""
    models: List[str] = Field(default_factory=list, description="可用模型列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "获取成功",
                "models": ["gemini-2.5-flash", "gemini-2.5-pro"]
            }
        }


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str = Field(..., description="服务状态")
    version: str = Field(..., description="API 版本")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0"
            }
        }

