"""
直接测试 Gemini API 端点
"""
import httpx

api_key = "AIzaSyAebsKqvJPLrt8FXZrYnRw28oLviH0jEtw"
proxy_url = "http://127.0.0.1:7890"

# Gemini API 端点
base_url = "https://generativelanguage.googleapis.com"
endpoint = f"{base_url}/v1beta/models?key={api_key}"

print("测试直接访问 Gemini API 端点...\n")

# 测试 1: 不使用代理
print("测试 1: 不使用代理")
try:
    client = httpx.Client(timeout=10.0)
    response = client.get(endpoint)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print("✅ 成功（不需要代理）")
    else:
        print(f"响应: {response.text[:200]}")
    client.close()
except Exception as e:
    print(f"❌ 错误: {e}")

# 测试 2: 使用代理
print("\n测试 2: 使用代理")
try:
    client = httpx.Client(proxy=proxy_url, timeout=10.0)
    response = client.get(endpoint)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if 'models' in data:
            print(f"✅ 成功！找到 {len(data['models'])} 个模型")
            if data['models']:
                print(f"第一个模型: {data['models'][0]['name']}")
    else:
        print(f"响应: {response.text[:500]}")
    client.close()
except Exception as e:
    print(f"❌ 错误: {e}")

# 测试 3: 测试代理是否能访问 Google
print("\n测试 3: 代理访问 Google")
try:
    client = httpx.Client(proxy=proxy_url, timeout=10.0)
    response = client.get("https://www.google.com")
    print(f"✅ 代理可以访问 Google，状态码: {response.status_code}")
    client.close()
except Exception as e:
    print(f"❌ 错误: {e}")

