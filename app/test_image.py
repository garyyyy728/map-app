"""
图片分析测试脚本
用于测试 Gemini API 的图片分析功能
"""
import requests
import sys
import os
from pathlib import Path


def test_image_analysis(image_path, prompt="详细描述这张图片"):
    """测试图片分析"""
    url = "http://localhost:8000/api/gemini/analyze-image"
    
    print(f"\n📸 分析图片: {image_path}")
    print(f"💬 提示词: {prompt}")
    print("-" * 60)
    
    try:
        # 检查文件是否存在
        if not os.path.exists(image_path):
            print(f"❌ 错误: 文件不存在 - {image_path}")
            return False
        
        # 检查文件大小
        file_size = os.path.getsize(image_path)
        file_size_mb = file_size / (1024 * 1024)
        print(f"📊 文件大小: {file_size_mb:.2f} MB")
        
        if file_size_mb > 10:
            print("⚠️  警告: 文件较大，可能需要较长时间处理")
        
        # 上传并分析
        with open(image_path, "rb") as f:
            files = {"image": f}
            data = {"prompt": prompt}
            
            print("⏳ 上传中...")
            response = requests.post(url, files=files, data=data, timeout=60)
            result = response.json()
            
            if result["success"]:
                print("\n✅ 分析成功!\n")
                print("=" * 60)
                print("📝 分析结果:")
                print("=" * 60)
                print(result['analysis'])
                print("=" * 60)
                return True
            else:
                print(f"\n❌ 分析失败: {result['message']}")
                return False
                
    except FileNotFoundError:
        print(f"❌ 错误: 文件不存在 - {image_path}")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 错误: 无法连接到服务器")
        print("   请确保:")
        print("   1. 服务器已启动 (python main.py)")
        print("   2. 服务运行在 http://localhost:8000")
        return False
    except requests.exceptions.Timeout:
        print("❌ 错误: 请求超时")
        print("   图片分析可能需要较长时间，请稍后重试")
        return False
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return False


def test_multiple_prompts(image_path):
    """使用多个提示词测试同一张图片"""
    prompts = [
        "详细描述这张图片",
        "列出图片中的所有物体",
        "提取图片中的所有文字（如果有）",
        "描述图片的颜色和构图",
        "这张图片可能在什么场景下拍摄？"
    ]
    
    print("\n" + "=" * 60)
    print("🔍 多角度分析模式")
    print("=" * 60)
    
    results = []
    for i, prompt in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] 分析中...")
        success = test_image_analysis(image_path, prompt)
        results.append(success)
        
        if i < len(prompts):
            print("\n" + "-" * 60)
    
    # 显示总结
    success_count = sum(results)
    print("\n" + "=" * 60)
    print(f"📊 分析完成: {success_count}/{len(prompts)} 成功")
    print("=" * 60)


def check_server():
    """检查服务器是否运行"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ 服务器运行正常")
            return True
        else:
            print(f"⚠️  服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
        print("\n请先启动服务器:")
        print("  python main.py")
        return False
    except Exception as e:
        print(f"❌ 检查服务器时出错: {str(e)}")
        return False


def print_usage():
    """打印使用说明"""
    print("""
╔════════════════════════════════════════════════════════════╗
║         Gemini 图片分析测试工具                            ║
╚════════════════════════════════════════════════════════════╝

📖 用法:

  1. 基础分析:
     python test_image.py <图片路径>
     
  2. 自定义提示词:
     python test_image.py <图片路径> "你的提示词"
     
  3. 多角度分析:
     python test_image.py <图片路径> --multi

📝 示例:

  python test_image.py photo.jpg
  python test_image.py photo.jpg "这张图片里有什么动物？"
  python test_image.py document.png "提取所有文字"
  python test_image.py landscape.jpg --multi

📋 支持的图片格式:
  - JPEG/JPG
  - PNG
  - GIF
  - WebP
  - BMP

⚠️  注意事项:
  1. 确保服务器已启动: python main.py
  2. 建议图片小于 4MB
  3. 如果在中国大陆，需要配置代理
    """)


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🚀 Gemini 图片分析测试工具")
    print("=" * 60)
    
    # 解析参数
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)
    
    image_path = sys.argv[1]
    
    # 检查服务器
    print("\n🔍 检查服务器状态...")
    if not check_server():
        sys.exit(1)
    
    # 多角度分析模式
    if len(sys.argv) > 2 and sys.argv[2] == "--multi":
        test_multiple_prompts(image_path)
    # 自定义提示词
    elif len(sys.argv) > 2:
        custom_prompt = sys.argv[2]
        test_image_analysis(image_path, custom_prompt)
    # 默认分析
    else:
        test_image_analysis(image_path)
    
    print("\n✨ 测试完成!\n")


if __name__ == "__main__":
    main()

