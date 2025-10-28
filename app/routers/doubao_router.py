"""
豆包 API 路由
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import Optional
import logging

from models import (
    GenerateTextRequest,
    GenerateTextResponse,
    ChatRequest,
    ChatResponse,
    ImageAnalyzeResponse,
    ModelsListResponse,
)
from services.doubao_service import DoubaoService
from dependencies import get_doubao_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/doubao",
    tags=["豆包 API"],
)


@router.post(
    "/generate",
    response_model=GenerateTextResponse,
    summary="生成文本",
    description="使用豆包模型生成文本内容"
)
async def generate_text(
    request: GenerateTextRequest,
    doubao_service: DoubaoService = Depends(get_doubao_service)
):
    """生成文本接口"""
    try:
        text = await doubao_service.generate_text(
            prompt=request.prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        
        return GenerateTextResponse(
            success=True,
            message="生成成功",
            text=text
        )
    
    except Exception as e:
        logger.error(f"Generate text error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="对话接口",
    description="与豆包模型进行多轮对话"
)
async def chat(
    request: ChatRequest,
    doubao_service: DoubaoService = Depends(get_doubao_service)
):
    """对话接口"""
    try:
        # 转换消息格式
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        reply = await doubao_service.chat(
            messages=messages,
            model=request.model,
            temperature=request.temperature,
        )
        
        return ChatResponse(
            success=True,
            message="对话成功",
            reply=reply
        )
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"对话失败: {str(e)}")


@router.post(
    "/analyze-image",
    response_model=ImageAnalyzeResponse,
    summary="分析图片",
    description="使用豆包视觉模型分析图片内容"
)
async def analyze_image(
    image: UploadFile = File(..., description="要分析的图片文件"),
    prompt: str = Form("描述这张图片", description="分析提示词"),
    model: Optional[str] = Form(None, description="模型名称"),
    doubao_service: DoubaoService = Depends(get_doubao_service)
):
    """分析图片接口"""
    try:
        # 读取图片数据
        image_data = await image.read()
        
        # 调用服务
        analysis = await doubao_service.analyze_image(
            image_data=image_data,
            prompt=prompt,
            model=model,
        )
        
        return ImageAnalyzeResponse(
            success=True,
            message="分析成功",
            analysis=analysis
        )
    
    except Exception as e:
        logger.error(f"Image analysis error: {str(e)}")
        # 返回 JSON 格式的错误响应，而不是抛出 HTTPException
        return ImageAnalyzeResponse(
            success=False,
            message=f"图片分析失败: {str(e)}",
            analysis=""
        )


@router.get(
    "/models",
    response_model=ModelsListResponse,
    summary="获取模型列表",
    description="获取可用的豆包模型列表"
)
async def list_models(
    doubao_service: DoubaoService = Depends(get_doubao_service)
):
    """获取模型列表"""
    try:
        models = doubao_service.list_models()
        
        return ModelsListResponse(
            success=True,
            message="获取成功",
            models=models
        )
    
    except Exception as e:
        logger.error(f"List models error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取模型列表失败: {str(e)}")

