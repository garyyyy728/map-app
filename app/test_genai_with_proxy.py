"""
测试 genai.Client 与 httpx 代理配置
"""
import os
import httpx
from google import genai

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

api_key = "AIzaSyAebsKqvJPLrt8FXZrYnRw28oLviH0jEtw"
proxy_url = "http://127.0.0.1:7890"

print("测试 genai.Client 代理配置...\n")

# 方法 1: 使用 http_options
print("方法 1: genai.Client(http_options={'client': httpx.Client(proxy=...)})")
try:
    http_client = httpx.Client(
        proxy=proxy_url,
        timeout=httpx.Timeout(60.0),
    )
    
    client = genai.Client(
        api_key=api_key,
        http_options={'client': http_client}
    )
    
    print("✅ Client 创建成功")
    
    # 测试 API 调用
    models = client.models.list()
    model_names = [m.name for m in models]
    print(f"✅ 成功列出 {len(model_names)} 个模型")
    print(f"前3个模型: {model_names[:3]}")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

# 方法 2: 只使用环境变量
print("\n方法 2: genai.Client() - 仅使用环境变量")
try:
    client = genai.Client(api_key=api_key)
    print("✅ Client 创建成功")
    
    # 测试 API 调用
    models = client.models.list()
    model_names = [m.name for m in models]
    print(f"✅ 成功列出 {len(model_names)} 个模型")
    
except Exception as e:
    print(f"❌ 错误: {e}")

