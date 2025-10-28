"""
API 使用示例
演示如何使用 Gemini API 后台服务
"""
import requests
import json


# API 基础地址
BASE_URL = "http://localhost:8000"


def example_generate_text():
    """示例：生成文本"""
    print("=" * 60)
    print("示例 1: 文本生成")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/gemini/generate"
    payload = {
        "prompt": "写一首关于春天的短诗",
        "temperature": 0.9,
        "max_tokens": 200
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result["success"]:
        print(f"\n生成的内容:\n{result['text']}\n")
    else:
        print(f"错误: {result['message']}\n")


def example_chat():
    """示例：多轮对话"""
    print("=" * 60)
    print("示例 2: 多轮对话")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/gemini/chat"
    
    # 第一轮对话
    print("\n用户: 你好，我想学习 Python 编程")
    payload = {
        "messages": [
            {"role": "user", "content": "你好，我想学习 Python 编程"}
        ],
        "temperature": 0.7
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result["success"]:
        reply1 = result["reply"]
        print(f"AI: {reply1}\n")
        
        # 第二轮对话（带上下文）
        print("用户: 从哪里开始学习比较好？")
        payload = {
            "messages": [
                {"role": "user", "content": "你好，我想学习 Python 编程"},
                {"role": "assistant", "content": reply1},
                {"role": "user", "content": "从哪里开始学习比较好？"}
            ],
            "temperature": 0.7
        }
        
        response = requests.post(url, json=payload)
        result = response.json()
        
        if result["success"]:
            print(f"AI: {result['reply']}\n")


def example_list_models():
    """示例：获取可用模型"""
    print("=" * 60)
    print("示例 3: 获取可用模型")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/gemini/models"
    response = requests.get(url)
    result = response.json()
    
    if result["success"]:
        print("\n可用的模型:")
        for i, model in enumerate(result["models"], 1):
            print(f"  {i}. {model}")
        print()


def example_analyze_image():
    """示例：分析图片（需要先有图片文件）"""
    print("=" * 60)
    print("示例 4: 图片分析")
    print("=" * 60)
    
    # 注意：这个示例需要一个实际的图片文件
    image_path = "test_image.jpg"  # 替换为实际的图片路径
    
    try:
        url = f"{BASE_URL}/api/gemini/analyze-image"
        
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {'prompt': '详细描述这张图片的内容'}
            
            response = requests.post(url, files=files, data=data)
            result = response.json()
            
            if result["success"]:
                print(f"\n图片分析结果:\n{result['analysis']}\n")
            else:
                print(f"错误: {result['message']}\n")
                
    except FileNotFoundError:
        print(f"\n注意: 找不到图片文件 '{image_path}'")
        print("请将实际的图片文件路径传入，或跳过此示例。\n")


def example_with_different_models():
    """示例：使用不同的模型"""
    print("=" * 60)
    print("示例 5: 使用不同模型")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/gemini/generate"
    prompt = "用一句话解释量子计算"
    
    models = ["gemini-2.5-flash", "gemini-2.5-flash-lite"]
    
    for model in models:
        print(f"\n使用模型: {model}")
        payload = {
            "prompt": prompt,
            "model": model,
            "temperature": 0.5
        }
        
        response = requests.post(url, json=payload)
        result = response.json()
        
        if result["success"]:
            print(f"回答: {result['text']}")


def main():
    """运行所有示例"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "Gemini API 使用示例" + " " * 24 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    try:
        # 先检查服务是否可用
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("错误: 服务器未正常运行")
            return
        
        # 运行示例
        example_list_models()
        example_generate_text()
        example_chat()
        example_with_different_models()
        # example_analyze_image()  # 需要图片文件，默认注释掉
        
        print("=" * 60)
        print("✓ 所有示例运行完成")
        print("=" * 60)
        print()
        
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器")
        print("请确保服务器正在运行:")
        print("  python main.py")
        print()
    except Exception as e:
        print(f"错误: {str(e)}")


if __name__ == "__main__":
    main()

