"""
FastAPI 主应用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from config import get_settings
from routers.doubao_router import router as doubao_router
from models import HealthResponse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# 获取配置
settings = get_settings()

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 健康检查端点
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["系统"],
    summary="健康检查",
    description="检查服务是否正常运行"
)
async def health_check():
    """健康检查"""
    return HealthResponse(
        status="healthy",
        version=settings.api_version
    )


# 根路径
@app.get(
    "/",
    tags=["系统"],
    summary="欢迎页面"
)
async def root():
    """根路径"""
    return {
        "message": f"欢迎使用 {settings.api_title}",
        "version": settings.api_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# 注册路由
app.include_router(doubao_router)


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "服务器内部错误",
            "detail": str(exc) if settings.debug else "请联系管理员"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting {settings.api_title} v{settings.api_version}")
    logger.info(f"Docs available at http://{settings.host}:{settings.port}/docs")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )

