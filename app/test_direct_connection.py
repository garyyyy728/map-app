"""
测试是否可以不使用代理直接访问 Gemini API
"""
import os
import sys

def test_direct_connection():
    """测试直接连接到 Gemini API"""
    print("🔍 测试网络连接...")
    print("-" * 50)
    
    # 临时移除代理环境变量
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
    original_values = {}
    
    for var in proxy_vars:
        original_values[var] = os.environ.get(var)
        if var in os.environ:
            del os.environ[var]
    
    try:
        from google import genai
        from config import get_settings
        
        settings = get_settings()
        
        if not settings.gemini_api_key:
            print("❌ 未找到 API Key")
            print("💡 请在 .env 文件中设置 GEMINI_API_KEY")
            return False
        
        print("✅ API Key 已配置")
        print("🌐 尝试直接连接到 Gemini API（不使用代理）...")
        
        # 创建不使用代理的客户端
        client = genai.Client(api_key=settings.gemini_api_key)
        
        # 尝试生成简单文本
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents="Hello, just testing!",
        )
        
        print("✅ 成功！您可以不使用代理直接访问 Gemini API")
        print(f"📝 测试响应: {response.text[:100]}...")
        print("\n" + "=" * 50)
        print("🎉 结论：您的网络环境可以直接使用，无需配置代理！")
        print("=" * 50)
        return True
        
    except Exception as e:
        error_msg = str(e).lower()
        print(f"❌ 连接失败: {str(e)}")
        print("\n" + "=" * 50)
        
        if "location" in error_msg or "region" in error_msg:
            print("🌍 地理位置限制")
            print("💡 您需要使用代理才能访问 Gemini API")
        elif "timeout" in error_msg or "connection" in error_msg:
            print("⏱️ 网络连接超时")
            print("💡 建议：")
            print("   1. 检查网络连接")
            print("   2. 或者使用代理访问")
        elif "api" in error_msg and "key" in error_msg:
            print("🔑 API Key 问题")
            print("💡 请检查 .env 中的 GEMINI_API_KEY 是否正确")
        else:
            print("❓ 其他错误")
            print("💡 建议配置代理后再试")
        
        print("=" * 50)
        return False
        
    finally:
        # 恢复原始代理设置
        for var, value in original_values.items():
            if value is not None:
                os.environ[var] = value


if __name__ == "__main__":
    print("=" * 50)
    print("   测试是否可以不使用代理访问 Gemini API")
    print("=" * 50)
    print()
    
    success = test_direct_connection()
    
    print()
    print("📚 更多信息：")
    print("   - 如果测试成功：直接运行 python main.py")
    print("   - 如果需要代理：查看 PROXY_SETUP.md")
    
    sys.exit(0 if success else 1)

