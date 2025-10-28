"""
环境设置辅助脚本
用于快速创建 .env 文件
"""
import os


def create_env_file():
    """创建 .env 文件"""
    
    print("=" * 50)
    print("Gemini API 后台服务 - 环境配置")
    print("=" * 50)
    print()
    
    # 检查是否已存在 .env 文件
    if os.path.exists(".env"):
        overwrite = input(".env 文件已存在，是否覆盖？(y/n): ").lower()
        if overwrite != 'y':
            print("取消创建")
            return
    
    # 获取 API Key
    print("\n请访问以下链接获取 Gemini API Key:")
    print("https://ai.google.dev/gemini-api/docs")
    print()
    api_key = input("请输入您的 Gemini API Key: ").strip()
    
    if not api_key:
        print("错误: API Key 不能为空")
        return
    
    # 获取其他配置
    print("\n服务器配置 (直接按 Enter 使用默认值):")
    host = input("主机地址 [0.0.0.0]: ").strip() or "0.0.0.0"
    port = input("端口号 [8000]: ").strip() or "8000"
    debug = input("调试模式 [True]: ").strip() or "True"
    
    # 创建 .env 文件内容
    env_content = f"""# Gemini API 配置
GEMINI_API_KEY={api_key}

# 服务器配置
HOST={host}
PORT={port}
DEBUG={debug}

# API 配置
API_TITLE=Gemini API 后台服务
API_VERSION=1.0.0
API_DESCRIPTION=基于 Google Gemini API 的后台服务
"""
    
    # 写入文件
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("\n" + "=" * 50)
    print("✓ .env 文件创建成功！")
    print("=" * 50)
    print("\n现在您可以运行服务器:")
    print("  python main.py")
    print("\n或使用 uvicorn:")
    print(f"  uvicorn main:app --host {host} --port {port} --reload")
    print()


if __name__ == "__main__":
    try:
        create_env_file()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n错误: {str(e)}")

