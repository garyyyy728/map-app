"""
豆包 API 测试脚本
用于验证豆包 API 配置是否正确
"""
import asyncio
import os
from dotenv import load_dotenv
from services.doubao_service import DoubaoService

# 加载环境变量
load_dotenv()


async def test_generate_text():
    """测试文本生成"""
    print("\n" + "="*60)
    print("测试 1: 文本生成")
    print("="*60)
    
    try:
        service = DoubaoService(
            api_key=os.getenv("DOUBAO_API_KEY"),
            base_url=os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
        )
        
        prompt = "用一句话介绍什么是人工智能"
        print(f"\n提示词: {prompt}")
        
        result = await service.generate_text(
            prompt=prompt,
            temperature=0.7
        )
        
        print(f"\n✅ 生成成功！")
        print(f"回复: {result}")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        return False


async def test_chat():
    """测试对话"""
    print("\n" + "="*60)
    print("测试 2: 多轮对话")
    print("="*60)
    
    try:
        service = DoubaoService(
            api_key=os.getenv("DOUBAO_API_KEY"),
            base_url=os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
        )
        
        messages = [
            {"role": "user", "content": "你好，请用一句话介绍自己"},
        ]
        
        print(f"\n用户: {messages[0]['content']}")
        
        result = await service.chat(
            messages=messages,
            temperature=0.8
        )
        
        print(f"\n✅ 对话成功！")
        print(f"助手: {result}")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        return False


def test_list_models():
    """测试获取模型列表"""
    print("\n" + "="*60)
    print("测试 3: 获取模型列表")
    print("="*60)
    
    try:
        service = DoubaoService(
            api_key=os.getenv("DOUBAO_API_KEY"),
            base_url=os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
        )
        
        models = service.list_models()
        
        print(f"\n✅ 获取成功！")
        print(f"可用模型:")
        for model in models:
            print(f"  - {model}")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        return False


async def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("🚀 豆包 API 配置测试")
    print("="*60)
    
    # 检查环境变量
    api_key = os.getenv("DOUBAO_API_KEY")
    base_url = os.getenv("DOUBAO_BASE_URL")
    
    print("\n📋 配置信息:")
    print(f"  API Key: {'已配置' if api_key else '❌ 未配置'}")
    print(f"  Base URL: {base_url or '使用默认值'}")
    
    if not api_key:
        print("\n❌ 错误: 未配置 DOUBAO_API_KEY")
        print("请在 .env 文件中配置你的 API Key")
        print("参考 env_example.txt 文件")
        return
    
    # 运行测试
    results = []
    
    # 测试 1: 文本生成
    results.append(await test_generate_text())
    
    # 测试 2: 对话
    results.append(await test_chat())
    
    # 测试 3: 模型列表
    results.append(test_list_models())
    
    # 输出总结
    print("\n" + "="*60)
    print("📊 测试总结")
    print("="*60)
    
    total = len(results)
    passed = sum(results)
    
    print(f"\n总测试数: {total}")
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {total - passed}")
    
    if passed == total:
        print("\n🎉 所有测试通过！豆包 API 配置正确。")
        print("现在可以启动服务了: python main.py")
    else:
        print("\n⚠️ 部分测试失败，请检查配置和网络连接。")
        print("\n常见问题:")
        print("1. 检查 DOUBAO_API_KEY 是否正确")
        print("2. 检查网络是否可以访问火山引擎服务")
        print("3. 如需代理，请在 .env 中配置 HTTP_PROXY 和 HTTPS_PROXY")
        print("4. 查看详细错误信息以定位问题")


if __name__ == "__main__":
    asyncio.run(main())

