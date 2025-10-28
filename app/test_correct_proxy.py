"""
使用正确的参数测试代理配置
"""
import httpx
from google import genai

api_key = "AIzaSyAebsKqvJPLrt8FXZrYnRw28oLviH0jEtw"
proxy_url = "http://127.0.0.1:7890"

print("测试正确的代理配置方法...\n")

# 方法 1: 使用 httpx_client
print("方法 1: http_options={'httpx_client': ...}")
try:
    http_client = httpx.Client(
        proxy=proxy_url,
        timeout=httpx.Timeout(60.0),
    )
    
    client = genai.Client(
        api_key=api_key,
        http_options={'httpx_client': http_client}
    )
    
    print("✅ Client 创建成功")
    
    # 测试 API 调用
    models = client.models.list()
    model_names = [m.name for m in models]
    print(f"✅ 成功列出 {len(model_names)} 个模型")
    print(f"前5个模型: {model_names[:5]}")
    
    http_client.close()
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

# 方法 2: 使用 client_args 传递代理
print("\n方法 2: http_options={'client_args': {'proxy': ...}}")
try:
    client = genai.Client(
        api_key=api_key,
        http_options={
            'client_args': {
                'proxy': proxy_url
            }
        }
    )
    
    print("✅ Client 创建成功")
    
    # 测试 API 调用
    models = client.models.list()
    model_names = [m.name for m in models]
    print(f"✅ 成功列出 {len(model_names)} 个模型")
    print(f"前5个模型: {model_names[:5]}")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

