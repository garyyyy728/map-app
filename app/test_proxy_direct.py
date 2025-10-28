"""
直接测试代理配置
"""
import os
import sys

# 设置代理环境变量
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

print("🔍 测试代理配置...")
print(f"HTTP_PROXY: {os.environ.get('HTTP_PROXY')}")
print(f"HTTPS_PROXY: {os.environ.get('HTTPS_PROXY')}")

try:
    from google import genai
    import httpx
    
    api_key = "AIzaSyAebsKqvJPLrt8FXZrYnRw28oLviH0jEtw"
    proxy_url = "http://127.0.0.1:7890"
    
    print("\n方法 1: 使用 httpx.Client 配置代理")
    try:
        http_client = httpx.Client(
            proxies={
                "http://": proxy_url,
                "https://": proxy_url,
            },
            timeout=httpx.Timeout(60.0),
        )
        print("✅ httpx.Client 创建成功")
        
        # 测试代理是否工作
        response = http_client.get("https://www.google.com")
        print(f"✅ 代理测试成功，状态码: {response.status_code}")
        
    except Exception as e:
        print(f"❌ httpx.Client 错误: {e}")
    
    print("\n方法 2: 使用环境变量创建 genai.Client")
    try:
        client = genai.Client(api_key=api_key)
        print("✅ genai.Client 创建成功（使用环境变量）")
        
        # 尝试列出模型
        models = client.models.list()
        model_names = [m.name for m in models]
        print(f"✅ 成功列出 {len(model_names)} 个模型")
        print(f"模型: {model_names[:3]}...")
        
    except Exception as e:
        print(f"❌ genai.Client 错误: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"❌ 导入错误: {e}")
    import traceback
    traceback.print_exc()

