#!/usr/bin/env python3
"""
图片分析 API 测试和诊断脚本
用于测试和诊断图片分析功能的问题
"""

import requests
import sys
import os
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

def print_section(title):
    """打印分节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def check_server():
    """检查服务器状态"""
    print_section("1. 检查服务器状态")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.ok:
            data = response.json()
            print(f"✅ 服务器在线")
            print(f"   状态: {data.get('status')}")
            print(f"   版本: {data.get('version')}")
            return True
        else:
            print(f"❌ 服务器响应异常: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到服务器 ({API_BASE_URL})")
        print(f"   请确保后端服务正在运行: python main.py")
        return False
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

def test_image_analysis_with_url():
    """测试使用在线图片的分析"""
    print_section("2. 测试图片分析 API（使用测试图片）")
    
    # 创建一个简单的测试图片（1x1 像素）
    import io
    from PIL import Image
    
    # 创建一个简单的红色图片
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    try:
        print("📤 发送测试请求...")
        
        files = {
            'image': ('test.png', img_bytes, 'image/png')
        }
        data = {
            'prompt': '这是什么颜色的图片？'
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/gemini/analyze-image",
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"📥 HTTP 状态码: {response.status_code}")
        
        try:
            result = response.json()
            print(f"\n响应内容:")
            print(f"  success: {result.get('success')}")
            print(f"  message: {result.get('message')}")
            
            if result.get('success'):
                print(f"\n✅ 分析成功!")
                print(f"\n分析结果:")
                print(f"  {result.get('analysis')}")
                return True
            else:
                print(f"\n❌ 分析失败!")
                print(f"\n错误信息:")
                print(f"  {result.get('message')}")
                
                # 检查是否是地理位置限制
                if 'User location is not supported' in result.get('message', ''):
                    print(f"\n💡 这是地理位置限制问题！")
                    print(f"   解决方案：")
                    print(f"   1. 启动代理工具（Clash、V2rayN 等）")
                    print(f"   2. 配置 .env 文件中的代理设置")
                    print(f"   3. 重启后端服务")
                    print(f"   详见: PROXY_SETUP.md")
                
                return False
                
        except ValueError:
            print(f"❌ 响应不是有效的 JSON:")
            print(response.text[:500])
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时（30秒）")
        return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_real_image(image_path):
    """测试使用真实图片"""
    print_section(f"3. 测试真实图片分析: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"❌ 图片文件不存在: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {
                'image': (os.path.basename(image_path), f, 'image/jpeg')
            }
            data = {
                'prompt': '详细描述这张图片'
            }
            
            print(f"📤 上传并分析图片...")
            response = requests.post(
                f"{API_BASE_URL}/api/gemini/analyze-image",
                files=files,
                data=data,
                timeout=60
            )
            
            result = response.json()
            
            if result.get('success'):
                print(f"✅ 分析成功!")
                print(f"\n分析结果:")
                print(f"{result.get('analysis')}")
                return True
            else:
                print(f"❌ 分析失败: {result.get('message')}")
                return False
                
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def print_help():
    """打印帮助信息"""
    print_section("诊断帮助")
    
    print("常见问题和解决方案:\n")
    
    print("1. ❌ 无法连接到服务器")
    print("   解决: 运行 python main.py 启动服务\n")
    
    print("2. ❌ User location is not supported")
    print("   解决: 配置代理（详见 PROXY_SETUP.md）")
    print("   - 启动代理工具")
    print("   - 编辑 .env 添加:")
    print("     HTTP_PROXY=http://127.0.0.1:7890")
    print("     HTTPS_PROXY=http://127.0.0.1:7890")
    print("   - 重启服务\n")
    
    print("3. ❌ API Key 无效")
    print("   解决: 检查 .env 中的 GEMINI_API_KEY\n")
    
    print("4. ❌ 分析超时")
    print("   解决: 检查网络连接，图片不要太大\n")
    
    print("查看完整文档:")
    print("  - 图片分析使用指南.md")
    print("  - TROUBLESHOOTING.md")
    print("  - 测试清单.md")

def main():
    """主函数"""
    print("\n🔍 Gemini 图片分析 API 诊断工具")
    print("="*60)
    
    # 检查依赖
    try:
        from PIL import Image
    except ImportError:
        print("\n⚠️  警告: 未安装 Pillow 库")
        print("   运行: pip install pillow")
        print("   继续使用基础测试...\n")
    
    # 1. 检查服务器
    if not check_server():
        print("\n❌ 服务器未运行，无法继续测试")
        print("\n请先启动服务器:")
        print("  python main.py")
        sys.exit(1)
    
    # 2. 测试 API
    try:
        success = test_image_analysis_with_url()
    except Exception as e:
        print(f"❌ 测试过程出错: {e}")
        success = False
    
    # 3. 如果提供了图片路径，测试真实图片
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        test_with_real_image(image_path)
    
    # 打印帮助
    if not success:
        print_help()
    
    # 总结
    print_section("测试总结")
    if success:
        print("✅ 所有测试通过！图片分析功能正常工作")
        print("\n可以使用以下方式分析图片:")
        print("  1. 网页界面: web_image_upload.html")
        print("  2. 命令行: python test_image.py your_image.jpg")
        print("  3. Python SDK: from image_analyzer import ImageAnalyzer")
    else:
        print("❌ 存在问题，请查看上面的错误信息和解决方案")
        print("\n需要帮助？查看:")
        print("  - TROUBLESHOOTING.md")
        print("  - 测试清单.md")

if __name__ == "__main__":
    main()

