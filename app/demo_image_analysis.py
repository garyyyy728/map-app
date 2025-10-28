"""
图片分析功能完整演示脚本
展示所有可用的分析方法
"""
import sys
import os
from image_analyzer import ImageAnalyzer
import requests


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_result(method_name, result):
    """打印结果"""
    print(f"📌 {method_name}:")
    print("-" * 70)
    print(result)
    print()


def check_server():
    """检查服务器状态"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ 服务器状态: 正常")
            return True
        else:
            print(f"⚠️  服务器响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到服务器: {e}")
        print("\n请先启动服务器:")
        print("  python main.py\n")
        return False


def demo_all_features(image_path):
    """演示所有功能"""
    
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "🎨 图片分析完整演示" + " " * 28 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # 检查服务器
    print_section("🔍 系统检查")
    if not check_server():
        return
    
    # 检查文件
    if not os.path.exists(image_path):
        print(f"❌ 错误: 文件不存在 - {image_path}\n")
        print("请提供一个有效的图片路径，例如:")
        print("  python demo_image_analysis.py photo.jpg\n")
        return
    
    file_size = os.path.getsize(image_path) / 1024 / 1024
    print(f"✅ 图片文件: {image_path}")
    print(f"✅ 文件大小: {file_size:.2f} MB")
    
    # 创建分析器
    analyzer = ImageAnalyzer()
    
    try:
        # 1. 基础分析
        print_section("1️⃣  基础分析")
        result = analyzer.analyze(image_path, "详细描述这张图片")
        print_result("基础分析", result)
        
        # 2. 物体检测
        print_section("2️⃣  物体检测")
        result = analyzer.detect_objects(image_path)
        print_result("检测到的物体", result)
        
        # 3. 场景描述
        print_section("3️⃣  场景描述")
        result = analyzer.describe_scene(image_path)
        print_result("场景详情", result)
        
        # 4. 文字提取
        print_section("4️⃣  文字提取 (OCR)")
        result = analyzer.extract_text(image_path)
        print_result("提取的文字", result if result and result.strip() else "（图片中没有检测到文字）")
        
        # 5. 颜色分析
        print_section("5️⃣  颜色分析")
        result = analyzer.identify_colors(image_path)
        print_result("颜色信息", result)
        
        # 6. 构图分析
        print_section("6️⃣  构图分析")
        result = analyzer.analyze_composition(image_path)
        print_result("构图评估", result)
        
        # 7. 生成标题
        print_section("7️⃣  生成标题")
        
        styles = ["简洁", "详细", "创意", "专业"]
        for style in styles:
            result = analyzer.generate_caption(image_path, style=style)
            print_result(f"标题 - {style}风格", result)
        
        # 8. 图片分类
        print_section("8️⃣  图片分类")
        result = analyzer.categorize(image_path)
        print_result("分类结果", result)
        
        # 9. 质量评估
        print_section("9️⃣  质量评估")
        result = analyzer.check_quality(image_path)
        print_result("质量分析", result)
        
        # 10. 情感分析（如果有人物）
        print_section("🔟 情感分析")
        result = analyzer.analyze_emotion(image_path)
        print_result("情感识别", result)
        
        # 11. 人脸检测
        print_section("1️⃣1️⃣  人脸检测")
        result = analyzer.detect_faces(image_path)
        print_result("人脸信息", result)
        
        # 12. 自定义问答
        print_section("1️⃣2️⃣  图片问答")
        
        questions = [
            "这张图片的主要焦点是什么？",
            "图片是在什么时间拍摄的？（白天/晚上/黄昏等）",
            "图片传达了什么样的氛围或情绪？",
            "如果要改进这张图片，你有什么建议？"
        ]
        
        for i, question in enumerate(questions, 1):
            result = analyzer.answer_question(image_path, question)
            print_result(f"问题 {i}: {question}", result)
        
        # 完成
        print("\n" + "╔" + "=" * 68 + "╗")
        print("║" + " " * 25 + "✨ 演示完成！" + " " * 30 + "║")
        print("╚" + "=" * 68 + "╝\n")
        
        print("📊 演示总结:")
        print("  ✅ 共执行了 20+ 种不同的分析")
        print("  ✅ 展示了所有主要功能")
        print("  ✅ 包含多种应用场景\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 错误: 无法连接到服务器")
        print("请确保服务器已启动: python main.py\n")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}\n")


def demo_quick(image_path):
    """快速演示（只展示主要功能）"""
    
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 22 + "🚀 快速演示模式" + " " * 30 + "║")
    print("╚" + "=" * 68 + "╝")
    
    if not check_server():
        return
    
    if not os.path.exists(image_path):
        print(f"\n❌ 文件不存在: {image_path}\n")
        return
    
    analyzer = ImageAnalyzer()
    
    try:
        print_section("核心功能演示")
        
        # 1. 基础描述
        print("⏳ [1/5] 基础描述...")
        result = analyzer.analyze(image_path)
        print_result("图片描述", result)
        
        # 2. 物体检测
        print("⏳ [2/5] 物体检测...")
        result = analyzer.detect_objects(image_path)
        print_result("物体列表", result)
        
        # 3. 颜色分析
        print("⏳ [3/5] 颜色分析...")
        result = analyzer.identify_colors(image_path)
        print_result("颜色信息", result)
        
        # 4. 生成标题
        print("⏳ [4/5] 生成标题...")
        result = analyzer.generate_caption(image_path, "创意")
        print_result("创意标题", result)
        
        # 5. 图片分类
        print("⏳ [5/5] 图片分类...")
        result = analyzer.categorize(image_path)
        print_result("类别", result)
        
        print("\n✅ 快速演示完成！\n")
        print("提示: 使用 --full 参数查看完整演示\n")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}\n")


def print_usage():
    """打印使用说明"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                  图片分析功能完整演示                              ║
╚════════════════════════════════════════════════════════════════════╝

📖 用法:

  完整演示（所有功能）:
    python demo_image_analysis.py <图片路径> --full
    
  快速演示（核心功能）:
    python demo_image_analysis.py <图片路径>

📝 示例:

  python demo_image_analysis.py photo.jpg
  python demo_image_analysis.py landscape.jpg --full
  python demo_image_analysis.py portrait.png --full

📋 演示内容:

  快速模式（5 项）:
    ✓ 基础描述
    ✓ 物体检测
    ✓ 颜色分析
    ✓ 生成标题
    ✓ 图片分类
  
  完整模式（20+ 项）:
    ✓ 基础分析
    ✓ 物体检测
    ✓ 场景描述
    ✓ 文字提取 (OCR)
    ✓ 颜色分析
    ✓ 构图分析
    ✓ 生成标题（4种风格）
    ✓ 图片分类
    ✓ 质量评估
    ✓ 情感分析
    ✓ 人脸检测
    ✓ 图片问答（4个问题）

⚙️  前提条件:
  
  1. 确保服务器已启动:
     python main.py
     
  2. 如果在中国大陆，需配置代理
     详见 PROXY_SETUP.md

💡 提示:

  - 首次运行建议使用快速模式
  - 完整模式会进行 20+ 次 API 调用，需要较长时间
  - 建议使用多样化的图片进行测试（风景、人物、文档等）
    """)


def main():
    """主函数"""
    
    # 解析参数
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)
    
    image_path = sys.argv[1]
    
    # 检查是否为完整模式
    full_mode = "--full" in sys.argv
    
    if full_mode:
        demo_all_features(image_path)
    else:
        demo_quick(image_path)


if __name__ == "__main__":
    main()

