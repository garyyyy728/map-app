"""
图片分析使用示例
展示常见的应用场景
"""
import sys
import os

# 添加父目录到路径以便导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from image_analyzer import ImageAnalyzer


def example_1_basic_analysis():
    """示例 1: 基础图片分析"""
    print("\n" + "=" * 60)
    print("示例 1: 基础图片分析")
    print("=" * 60)
    
    analyzer = ImageAnalyzer()
    
    # 假设有一张照片
    # result = analyzer.analyze("photo.jpg")
    # print(result)
    
    print("""
代码示例:
    analyzer = ImageAnalyzer()
    result = analyzer.analyze("photo.jpg")
    print(result)

应用场景:
    - 为照片生成自动描述
    - 图片内容审核
    - 图片搜索索引
    """)


def example_2_ecommerce():
    """示例 2: 电商场景 - 商品分析"""
    print("\n" + "=" * 60)
    print("示例 2: 电商场景 - 商品识别和描述生成")
    print("=" * 60)
    
    print("""
代码示例:
    analyzer = ImageAnalyzer()
    
    # 识别商品
    description = analyzer.analyze(
        "product.jpg",
        "识别这个商品的品牌、型号、颜色和主要特征"
    )
    
    # 生成商品标题
    title = analyzer.generate_caption("product.jpg", style="专业")
    
    # 质量检查
    quality = analyzer.check_quality("product.jpg")
    
    print(f"商品描述: {description}")
    print(f"商品标题: {title}")
    print(f"图片质量: {quality}")

应用场景:
    - 自动生成商品描述
    - 商品质量检测
    - 商品分类
    - SKU 识别
    """)


def example_3_ocr():
    """示例 3: OCR 文字识别"""
    print("\n" + "=" * 60)
    print("示例 3: OCR 文字识别")
    print("=" * 60)
    
    print("""
代码示例:
    analyzer = ImageAnalyzer()
    
    # 提取发票文字
    invoice_text = analyzer.extract_text("invoice.jpg")
    
    # 提取名片信息
    card_info = analyzer.analyze(
        "business_card.jpg",
        "提取姓名、电话、邮箱、公司等信息，用 JSON 格式返回"
    )
    
    # 提取表格数据
    table_data = analyzer.analyze(
        "table.png",
        "提取表格中的所有数据，保持表格格式"
    )
    
    print(f"发票内容: {invoice_text}")
    print(f"名片信息: {card_info}")
    print(f"表格数据: {table_data}")

应用场景:
    - 发票识别和自动录入
    - 名片信息提取
    - 文档数字化
    - 表格数据提取
    """)


def example_4_content_moderation():
    """示例 4: 内容审核"""
    print("\n" + "=" * 60)
    print("示例 4: 内容审核")
    print("=" * 60)
    
    print("""
代码示例:
    analyzer = ImageAnalyzer()
    
    # 审核用户上传的图片
    def moderate_image(image_path):
        # 内容检测
        content_check = analyzer.analyze(
            image_path,
            "这张图片是否包含不适当、暴力、成人内容？请评估并说明理由"
        )
        
        # 分类
        category = analyzer.categorize(image_path)
        
        # 检测人脸
        faces = analyzer.detect_faces(image_path)
        
        return {
            "content_check": content_check,
            "category": category,
            "faces": faces
        }
    
    result = moderate_image("user_upload.jpg")
    print(result)

应用场景:
    - 社交媒体内容审核
    - UGC 平台图片过滤
    - 广告合规检查
    """)


def example_5_image_search():
    """示例 5: 图片搜索引擎"""
    print("\n" + "=" * 60)
    print("示例 5: 图片搜索引擎")
    print("=" * 60)
    
    print("""
代码示例:
    analyzer = ImageAnalyzer()
    import json
    
    # 为图片库建立索引
    def index_images(image_paths):
        index = {}
        
        for img_path in image_paths:
            # 生成描述
            description = analyzer.analyze(img_path)
            
            # 提取关键元素
            objects = analyzer.detect_objects(img_path)
            
            # 识别颜色
            colors = analyzer.identify_colors(img_path)
            
            # 分类
            category = analyzer.categorize(img_path)
            
            index[img_path] = {
                "description": description,
                "objects": objects,
                "colors": colors,
                "category": category
            }
        
        return index
    
    # 搜索图片
    def search_images(query, index):
        results = []
        for img_path, data in index.items():
            # 简单的关键词匹配（实际应用中可以用向量搜索）
            if query.lower() in data["description"].lower():
                results.append(img_path)
        return results
    
    # 使用示例
    image_list = ["img1.jpg", "img2.jpg", "img3.jpg"]
    image_index = index_images(image_list)
    
    # 搜索包含"猫"的图片
    cat_images = search_images("猫", image_index)
    print(f"找到 {len(cat_images)} 张包含猫的图片")

应用场景:
    - 图片库管理
    - 以图搜图
    - 智能相册
    - 素材管理系统
    """)


def example_6_social_media():
    """示例 6: 社交媒体 - 自动标题和标签"""
    print("\n" + "=" * 60)
    print("示例 6: 社交媒体 - 自动生成标题和标签")
    print("=" * 60)
    
    print("""
代码示例:
    analyzer = ImageAnalyzer()
    
    def generate_social_post(image_path):
        # 生成创意标题
        caption = analyzer.generate_caption(image_path, style="创意")
        
        # 分析场景
        scene = analyzer.describe_scene(image_path)
        
        # 识别主要元素
        objects = analyzer.detect_objects(image_path)
        
        # 生成标签（基于元素）
        tag_prompt = f"基于这些元素：{objects}，生成 5-10 个适合社交媒体的标签（#号开头）"
        tags = analyzer.analyze(image_path, tag_prompt)
        
        return {
            "caption": caption,
            "scene": scene,
            "tags": tags
        }
    
    post = generate_social_post("travel_photo.jpg")
    print(f"标题: {post['caption']}")
    print(f"场景: {post['scene']}")
    print(f"标签: {post['tags']}")

应用场景:
    - Instagram/微博自动发布
    - 旅游照片整理
    - 营销内容生成
    """)


def example_7_real_estate():
    """示例 7: 房地产 - 房源图片分析"""
    print("\n" + "=" * 60)
    print("示例 7: 房地产 - 房源图片分析")
    print("=" * 60)
    
    print("""
代码示例:
    analyzer = ImageAnalyzer()
    
    def analyze_property_image(image_path):
        # 识别房间类型
        room_type = analyzer.analyze(
            image_path,
            "这是什么房间？（客厅、卧室、厨房、卫生间等）"
        )
        
        # 分析装修风格
        style = analyzer.analyze(
            image_path,
            "描述这个房间的装修风格（现代、简约、欧式、中式等）"
        )
        
        # 评估状况
        condition = analyzer.analyze(
            image_path,
            "评估房间的新旧程度和维护状况"
        )
        
        # 识别家具和设施
        furniture = analyzer.detect_objects(image_path)
        
        return {
            "room_type": room_type,
            "style": style,
            "condition": condition,
            "furniture": furniture
        }
    
    # 批量分析房源图片
    property_images = [
        "living_room.jpg",
        "bedroom.jpg",
        "kitchen.jpg",
        "bathroom.jpg"
    ]
    
    property_analysis = {}
    for img in property_images:
        property_analysis[img] = analyze_property_image(img)

应用场景:
    - 房源自动标注
    - 房间类型识别
    - 装修风格分类
    - 房源质量评估
    """)


def example_8_education():
    """示例 8: 教育场景 - 作业批改辅助"""
    print("\n" + "=" * 60)
    print("示例 8: 教育场景 - 作业批改辅助")
    print("=" * 60)
    
    print("""
代码示例:
    analyzer = ImageAnalyzer()
    
    # 数学题目识别
    def analyze_math_homework(image_path):
        # 提取题目
        problem = analyzer.extract_text(image_path)
        
        # 识别公式和图形
        analysis = analyzer.analyze(
            image_path,
            "识别图片中的数学公式、图表和计算过程"
        )
        
        return {
            "text": problem,
            "analysis": analysis
        }
    
    # 图表题分析
    def analyze_chart_question(image_path):
        chart_analysis = analyzer.answer_question(
            image_path,
            "这个图表显示了什么？有什么趋势或规律？"
        )
        return chart_analysis
    
    homework = analyze_math_homework("homework.jpg")
    print(f"题目: {homework['text']}")
    print(f"分析: {homework['analysis']}")

应用场景:
    - 在线教育平台
    - 作业自动批改
    - 学习资料数字化
    - 图表题目分析
    """)


def example_9_batch_processing():
    """示例 9: 批量处理"""
    print("\n" + "=" * 60)
    print("示例 9: 批量处理图片")
    print("=" * 60)
    
    print("""
代码示例:
    analyzer = ImageAnalyzer()
    import os
    
    # 批量分析目录中的所有图片
    def analyze_directory(directory):
        results = []
        
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(directory, filename)
                
                try:
                    # 基础分析
                    description = analyzer.analyze(image_path)
                    
                    # 分类
                    category = analyzer.categorize(image_path)
                    
                    results.append({
                        "filename": filename,
                        "description": description,
                        "category": category,
                        "status": "success"
                    })
                except Exception as e:
                    results.append({
                        "filename": filename,
                        "error": str(e),
                        "status": "failed"
                    })
        
        return results
    
    # 使用批量分析方法（更高效）
    image_files = ["img1.jpg", "img2.jpg", "img3.jpg"]
    results = analyzer.batch_analyze(image_files, "描述这张图片")
    
    for img_path, result in results.items():
        if result["success"]:
            print(f"{img_path}: {result['analysis']}")
        else:
            print(f"{img_path}: 失败 - {result['error']}")

应用场景:
    - 大量图片批量处理
    - 图片库整理
    - 数据集标注
    """)


def example_10_advanced():
    """示例 10: 高级应用 - 组合多种分析"""
    print("\n" + "=" * 60)
    print("示例 10: 高级应用 - 综合分析报告")
    print("=" * 60)
    
    print("""
代码示例:
    analyzer = ImageAnalyzer()
    
    def generate_comprehensive_report(image_path):
        '''生成图片的综合分析报告'''
        
        report = {
            "image_path": image_path,
            "basic_info": {},
            "content_analysis": {},
            "technical_analysis": {},
            "recommendations": {}
        }
        
        # 基础信息
        report["basic_info"]["description"] = analyzer.analyze(image_path)
        report["basic_info"]["category"] = analyzer.categorize(image_path)
        
        # 内容分析
        report["content_analysis"]["objects"] = analyzer.detect_objects(image_path)
        report["content_analysis"]["scene"] = analyzer.describe_scene(image_path)
        report["content_analysis"]["text"] = analyzer.extract_text(image_path)
        
        # 技术分析
        report["technical_analysis"]["colors"] = analyzer.identify_colors(image_path)
        report["technical_analysis"]["composition"] = analyzer.analyze_composition(image_path)
        report["technical_analysis"]["quality"] = analyzer.check_quality(image_path)
        
        # 建议
        improvement = analyzer.analyze(
            image_path,
            "如果要改进这张图片，你有什么建议？（关于构图、光线、色彩等）"
        )
        report["recommendations"]["improvement"] = improvement
        
        # 生成多种风格的标题
        report["recommendations"]["captions"] = {
            "creative": analyzer.generate_caption(image_path, "创意"),
            "professional": analyzer.generate_caption(image_path, "专业"),
            "simple": analyzer.generate_caption(image_path, "简洁")
        }
        
        return report
    
    # 生成报告
    report = generate_comprehensive_report("photo.jpg")
    
    # 打印报告
    import json
    print(json.dumps(report, indent=2, ensure_ascii=False))

应用场景:
    - 专业摄影分析
    - 图片资产管理
    - 自动化报告生成
    - 质量控制系统
    """)


def main():
    """运行所有示例"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "📸 图片分析应用示例" + " " * 26 + "║")
    print("╚" + "=" * 68 + "╝")
    
    examples = [
        example_1_basic_analysis,
        example_2_ecommerce,
        example_3_ocr,
        example_4_content_moderation,
        example_5_image_search,
        example_6_social_media,
        example_7_real_estate,
        example_8_education,
        example_9_batch_processing,
        example_10_advanced,
    ]
    
    for i, example in enumerate(examples, 1):
        example()
        
        if i < len(examples):
            input("\n按 Enter 继续下一个示例...")
    
    print("\n" + "=" * 60)
    print("✅ 所有示例展示完毕！")
    print("=" * 60)
    print("\n提示：这些都是代码示例，要实际运行需要:")
    print("  1. 准备对应的图片文件")
    print("  2. 确保服务器已启动")
    print("  3. 根据需要修改代码\n")


if __name__ == "__main__":
    main()

