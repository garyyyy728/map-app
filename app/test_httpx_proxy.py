"""
测试 httpx 代理配置的不同方法
"""
import httpx

proxy_url = "http://127.0.0.1:7890"

print("测试 httpx 代理配置...\n")

# 方法 1: 使用 proxy 参数（同步）
print("方法 1: httpx.Client(proxy=...)")
try:
    client = httpx.Client(proxy=proxy_url, timeout=10.0)
    response = client.get("https://www.google.com")
    print(f"✅ 成功！状态码: {response.status_code}")
    client.close()
except Exception as e:
    print(f"❌ 错误: {e}")

# 方法 2: 使用 mounts（高级配置）
print("\n方法 2: httpx.Client with mounts")
try:
    transport = httpx.HTTPTransport(proxy=proxy_url)
    client = httpx.Client(transport=transport, timeout=10.0)
    response = client.get("https://www.google.com")
    print(f"✅ 成功！状态码: {response.status_code}")
    client.close()
except Exception as e:
    print(f"❌ 错误: {e}")

# 方法 3: 异步客户端
print("\n方法 3: httpx.AsyncClient(proxy=...)")
try:
    import asyncio
    
    async def test_async():
        async with httpx.AsyncClient(proxy=proxy_url, timeout=10.0) as client:
            response = await client.get("https://www.google.com")
            return response.status_code
    
    status = asyncio.run(test_async())
    print(f"✅ 成功！状态码: {status}")
except Exception as e:
    print(f"❌ 错误: {e}")

