"""
测试全局代理设置
"""
import os
import sys

# 方法 1: 在导入任何库之前设置环境变量
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["ALL_PROXY"] = "http://127.0.0.1:7890"

print("🔧 已设置全局代理环境变量")
print(f"HTTP_PROXY: {os.environ['HTTP_PROXY']}")
print(f"HTTPS_PROXY: {os.environ['HTTPS_PROXY']}\n")

# 方法 2: 尝试 monkey-patch httpx
try:
    import httpx
    
    # 保存原始的 Client 类
    _OriginalClient = httpx.Client
    _OriginalAsyncClient = httpx.AsyncClient
    
    # 创建包装类
    class ProxyClient(_OriginalClient):
        def __init__(self, *args, **kwargs):
            if 'proxy' not in kwargs:
                kwargs['proxy'] = "http://127.0.0.1:7890"
            super().__init__(*args, **kwargs)
    
    class ProxyAsyncClient(_OriginalAsyncClient):
        def __init__(self, *args, **kwargs):
            if 'proxy' not in kwargs:
                kwargs['proxy'] = "http://127.0.0.1:7890"
            super().__init__(*args, **kwargs)
    
    # 替换
    httpx.Client = ProxyClient
    httpx.AsyncClient = ProxyAsyncClient
    
    print("✅ 已 monkey-patch httpx.Client 和 httpx.AsyncClient\n")
    
except Exception as e:
    print(f"❌ Monkey-patch 失败: {e}\n")

# 现在导入 genai
from google import genai

api_key = "AIzaSyAebsKqvJPLrt8FXZrYnRw28oLviH0jEtw"

print("测试 genai.Client（使用全局代理）...\n")

try:
    client = genai.Client(api_key=api_key)
    print("✅ Client 创建成功")
    
    # 测试 API 调用
    print("正在列出模型...")
    models = client.models.list()
    model_names = [m.name for m in models]
    print(f"✅ 成功列出 {len(model_names)} 个模型")
    print(f"前5个模型: {model_names[:5]}")
    
except Exception as e:
    print(f"❌ 错误: {e}")

