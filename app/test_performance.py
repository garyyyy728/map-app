"""
性能测试脚本 - 测试AI分析速度
"""
import requests
import time
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"


def test_image_analysis_speed():
    """测试图片分析速度"""
    print("=" * 70)
    print("图片分析性能测试")
    print("=" * 70)
    print()
    
    # 查找测试图片
    test_images = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        test_images.extend(Path('.').glob(ext))
    
    if not test_images:
        print("❌ 未找到测试图片")
        print("请在项目目录下放置一张测试图片（.jpg/.jpeg/.png）")
        return
    
    test_image = test_images[0]
    file_size = os.path.getsize(test_image) / 1024  # KB
    
    print(f"📷 测试图片: {test_image.name}")
    print(f"📊 文件大小: {file_size:.2f} KB")
    
    if file_size > 1024:
        print(f"⚠️  警告: 图片较大（{file_size/1024:.2f} MB），建议压缩到 < 1MB")
    
    print()
    
    # 测试不同模型
    models = [
        ("gemini-2.0-flash-exp", "最快模型"),
        ("gemini-2.5-flash", "标准模型"),
    ]
    
    results = []
    
    for model, description in models:
        print(f"🧪 测试模型: {model} ({description})")
        print("-" * 70)
        
        try:
            # 准备请求
            with open(test_image, 'rb') as f:
                files = {'image': (test_image.name, f, 'image/jpeg')}
                data = {
                    'prompt': '简单描述这张图片',
                    'model': model
                }
                
                # 计时
                start_time = time.time()
                response = requests.post(
                    f"{BASE_URL}/api/gemini/analyze-image",
                    files=files,
                    data=data
                )
                end_time = time.time()
                
                elapsed = end_time - start_time
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"✅ 成功")
                        print(f"⏱️  耗时: {elapsed:.2f} 秒")
                        print(f"📝 分析结果: {result.get('analysis', '')[:100]}...")
                        results.append((model, elapsed, True))
                    else:
                        print(f"❌ 失败: {result.get('message')}")
                        results.append((model, elapsed, False))
                else:
                    print(f"❌ HTTP错误: {response.status_code}")
                    results.append((model, elapsed, False))
        
        except requests.exceptions.Timeout:
            print(f"❌ 超时")
            results.append((model, None, False))
        except requests.exceptions.ConnectionError:
            print(f"❌ 连接错误：请确保服务器正在运行")
            return
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            results.append((model, None, False))
        
        print()
        time.sleep(1)  # 避免请求过快
    
    # 显示总结
    print("=" * 70)
    print("性能测试总结")
    print("=" * 70)
    print()
    
    successful_results = [(m, t) for m, t, s in results if s and t is not None]
    
    if successful_results:
        print("✅ 成功的测试:")
        print()
        for model, elapsed in sorted(successful_results, key=lambda x: x[1]):
            print(f"  {model:30s} {elapsed:6.2f} 秒")
        
        fastest = min(successful_results, key=lambda x: x[1])
        print()
        print(f"🏆 最快: {fastest[0]} ({fastest[1]:.2f} 秒)")
        
        # 性能评级
        fastest_time = fastest[1]
        if fastest_time < 3:
            rating = "优秀 🌟🌟🌟"
        elif fastest_time < 5:
            rating = "良好 🌟🌟"
        elif fastest_time < 8:
            rating = "一般 🌟"
        else:
            rating = "较慢 ⚠️"
        
        print(f"📊 性能评级: {rating}")
    else:
        print("❌ 所有测试都失败了")
    
    print()
    print("=" * 70)


def test_text_generation_speed():
    """测试文本生成速度"""
    print()
    print("=" * 70)
    print("文本生成性能测试")
    print("=" * 70)
    print()
    
    prompts = [
        ("简单问题", "1+1等于几？"),
        ("中等问题", "请用一句话解释什么是人工智能"),
    ]
    
    for name, prompt in prompts:
        print(f"🧪 测试: {name}")
        print(f"📝 提示: {prompt}")
        print("-" * 70)
        
        try:
            data = {
                "prompt": prompt,
                "temperature": 0.7,
                "max_tokens": 100
            }
            
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/api/gemini/generate",
                json=data
            )
            end_time = time.time()
            
            elapsed = end_time - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"✅ 成功")
                    print(f"⏱️  耗时: {elapsed:.2f} 秒")
                    print(f"📝 回复: {result.get('text', '')[:100]}...")
                else:
                    print(f"❌ 失败: {result.get('message')}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
        
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
        
        print()


def main():
    """运行所有性能测试"""
    print()
    print("🚀 AI性能优化测试工具")
    print()
    
    # 检查服务器
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ 服务器未正常运行")
            print("请先启动服务器: python main.py")
            return
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
        print("请先启动服务器: python main.py")
        return
    except Exception as e:
        print(f"❌ 连接错误: {str(e)}")
        return
    
    print("✅ 服务器正常运行")
    print()
    
    # 运行测试
    test_image_analysis_speed()
    test_text_generation_speed()
    
    print()
    print("💡 优化建议:")
    print("  1. 如果速度仍然较慢，请检查网络和代理设置")
    print("  2. 压缩大图片可以显著提升速度")
    print("  3. 使用简洁的提示词")
    print("  4. 查看详细说明: AI分析速度优化说明.md")
    print()


if __name__ == "__main__":
    main()

