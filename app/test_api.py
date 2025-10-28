"""
API 测试脚本
用于快速测试 Gemini API 后台服务
"""
import requests
import json


BASE_URL = "http://localhost:8000"


def test_health():
    """测试健康检查"""
    print("测试健康检查...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()


def test_generate_text():
    """测试文本生成"""
    print("测试文本生成...")
    data = {
        "prompt": "请用一句话介绍人工智能",
        "temperature": 0.7,
        "max_tokens": 100
    }
    response = requests.post(f"{BASE_URL}/api/gemini/generate", json=data)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"成功: {result.get('success')}")
    print(f"生成内容: {result.get('text')}")
    print()


def test_chat():
    """测试对话接口"""
    print("测试对话接口...")
    data = {
        "messages": [
            {"role": "user", "content": "你好，请介绍一下你自己"}
        ],
        "temperature": 0.8
    }
    response = requests.post(f"{BASE_URL}/api/gemini/chat", json=data)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"成功: {result.get('success')}")
    print(f"回复: {result.get('reply')}")
    print()


def test_list_models():
    """测试获取模型列表"""
    print("测试获取模型列表...")
    response = requests.get(f"{BASE_URL}/api/gemini/models")
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"成功: {result.get('success')}")
    print(f"可用模型: {result.get('models')}")
    print()


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Gemini API 后台服务测试")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_list_models()
        test_generate_text()
        test_chat()
        
        print("=" * 60)
        print("✓ 所有测试完成")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器")
        print("请确保服务器正在运行: python main.py")
    except Exception as e:
        print(f"错误: {str(e)}")


if __name__ == "__main__":
    main()

