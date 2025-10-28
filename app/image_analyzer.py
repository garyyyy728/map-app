"""
完整的图片分析器类
支持多种分析场景
"""
import requests
from typing import Optional
import os


class ImageAnalyzer:
    """Gemini 图片分析器"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        初始化图片分析器
        
        Args:
            base_url: API 服务器地址
        """
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/gemini/analyze-image"
    
    def analyze(
        self, 
        image_path: str, 
        prompt: str = "描述这张图片",
        model: Optional[str] = None,
        timeout: int = 60
    ) -> str:
        """
        分析图片
        
        Args:
            image_path: 图片文件路径
            prompt: 分析提示词
            model: 使用的模型（可选）
            timeout: 超时时间（秒）
            
        Returns:
            分析结果文本
            
        Raises:
            FileNotFoundError: 文件不存在
            Exception: 其他错误
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        
        with open(image_path, "rb") as f:
            files = {"image": f}
            data = {"prompt": prompt}
            
            if model:
                data["model"] = model
            
            response = requests.post(
                self.endpoint, 
                files=files, 
                data=data,
                timeout=timeout
            )
            
            result = response.json()
            
            if result["success"]:
                return result["analysis"]
            else:
                raise Exception(f"分析失败: {result['message']}")
    
    def detect_objects(self, image_path: str) -> str:
        """
        检测图片中的物体
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            物体列表描述
        """
        return self.analyze(
            image_path, 
            "请列出这张图片中的所有物体和元素，用列表形式呈现"
        )
    
    def describe_scene(self, image_path: str) -> str:
        """
        详细描述场景
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            场景描述
        """
        return self.analyze(
            image_path,
            "详细描述这张图片的场景，包括环境、氛围、光线、颜色等细节"
        )
    
    def extract_text(self, image_path: str) -> str:
        """
        提取图片中的文字（OCR）
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            提取的文字内容
        """
        return self.analyze(
            image_path,
            "提取图片中的所有文字内容，保持原有格式和布局"
        )
    
    def analyze_emotion(self, image_path: str) -> str:
        """
        分析情感和表情
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            情感分析结果
        """
        return self.analyze(
            image_path,
            "分析图片中人物的情感、表情和肢体语言，描述他们可能的心理状态"
        )
    
    def identify_colors(self, image_path: str) -> str:
        """
        识别主要颜色
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            颜色分析结果
        """
        return self.analyze(
            image_path,
            "分析图片的主要颜色、色调和配色方案"
        )
    
    def analyze_composition(self, image_path: str) -> str:
        """
        分析构图
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            构图分析结果
        """
        return self.analyze(
            image_path,
            "分析图片的构图、布局、对称性和视觉重点"
        )
    
    def answer_question(self, image_path: str, question: str) -> str:
        """
        回答关于图片的问题
        
        Args:
            image_path: 图片文件路径
            question: 问题
            
        Returns:
            回答
        """
        return self.analyze(image_path, question)
    
    def compare_with_description(self, image_path: str, description: str) -> str:
        """
        将图片与描述进行对比
        
        Args:
            image_path: 图片文件路径
            description: 预期描述
            
        Returns:
            对比结果
        """
        prompt = f"这张图片是否符合以下描述？请详细说明：{description}"
        return self.analyze(image_path, prompt)
    
    def generate_caption(self, image_path: str, style: str = "简洁") -> str:
        """
        生成图片标题
        
        Args:
            image_path: 图片文件路径
            style: 标题风格（简洁/详细/创意/专业）
            
        Returns:
            图片标题
        """
        prompts = {
            "简洁": "用一句话简洁地描述这张图片，适合作为标题",
            "详细": "生成一个详细的图片标题，包含主要元素和场景",
            "创意": "为这张图片创作一个富有创意和诗意的标题",
            "专业": "以专业摄影的角度为这张图片写一个标题"
        }
        
        prompt = prompts.get(style, prompts["简洁"])
        return self.analyze(image_path, prompt)
    
    def check_quality(self, image_path: str) -> str:
        """
        评估图片质量
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            质量评估结果
        """
        return self.analyze(
            image_path,
            "评估这张图片的质量，包括清晰度、光线、构图等方面"
        )
    
    def detect_faces(self, image_path: str) -> str:
        """
        检测人脸
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            人脸检测结果
        """
        return self.analyze(
            image_path,
            "检测图片中有多少个人脸，并描述每个人的大致特征（年龄、性别、表情等）"
        )
    
    def categorize(self, image_path: str) -> str:
        """
        分类图片
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            图片分类
        """
        return self.analyze(
            image_path,
            "对这张图片进行分类，并说明它最适合哪个类别（如：风景、人物、动物、建筑、食物等）"
        )
    
    def batch_analyze(self, image_paths: list, prompt: str = "描述这张图片") -> dict:
        """
        批量分析多张图片
        
        Args:
            image_paths: 图片路径列表
            prompt: 分析提示词
            
        Returns:
            {图片路径: 分析结果} 的字典
        """
        results = {}
        
        for image_path in image_paths:
            try:
                result = self.analyze(image_path, prompt)
                results[image_path] = {
                    "success": True,
                    "analysis": result
                }
            except Exception as e:
                results[image_path] = {
                    "success": False,
                    "error": str(e)
                }
        
        return results


# 使用示例
if __name__ == "__main__":
    import sys
    
    # 创建分析器实例
    analyzer = ImageAnalyzer()
    
    if len(sys.argv) < 2:
        print("""
╔════════════════════════════════════════════════════════════╗
║           ImageAnalyzer 使用示例                           ║
╚════════════════════════════════════════════════════════════╝

📖 Python 代码示例:

from image_analyzer import ImageAnalyzer

analyzer = ImageAnalyzer()

# 基础分析
result = analyzer.analyze("photo.jpg")
print(result)

# 物体检测
objects = analyzer.detect_objects("street.jpg")
print(objects)

# 场景描述
scene = analyzer.describe_scene("landscape.jpg")
print(scene)

# 文字提取（OCR）
text = analyzer.extract_text("document.png")
print(text)

# 情感分析
emotion = analyzer.analyze_emotion("portrait.jpg")
print(emotion)

# 颜色分析
colors = analyzer.identify_colors("painting.jpg")
print(colors)

# 问答
answer = analyzer.answer_question("chart.png", "这个图表显示了什么趋势？")
print(answer)

# 生成标题
caption = analyzer.generate_caption("photo.jpg", style="创意")
print(caption)

# 批量分析
images = ["img1.jpg", "img2.jpg", "img3.jpg"]
results = analyzer.batch_analyze(images)
print(results)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💻 命令行测试:
  python image_analyzer.py <图片路径>

示例:
  python image_analyzer.py photo.jpg
        """)
        sys.exit(0)
    
    image_path = sys.argv[1]
    
    print("\n" + "=" * 60)
    print("🎨 ImageAnalyzer 完整演示")
    print("=" * 60)
    
    try:
        # 1. 基础分析
        print("\n[1] 基础分析:")
        print("-" * 60)
        result = analyzer.analyze(image_path)
        print(result)
        
        # 2. 物体检测
        print("\n[2] 物体检测:")
        print("-" * 60)
        objects = analyzer.detect_objects(image_path)
        print(objects)
        
        # 3. 场景描述
        print("\n[3] 场景描述:")
        print("-" * 60)
        scene = analyzer.describe_scene(image_path)
        print(scene)
        
        # 4. 颜色分析
        print("\n[4] 颜色分析:")
        print("-" * 60)
        colors = analyzer.identify_colors(image_path)
        print(colors)
        
        # 5. 生成标题
        print("\n[5] 创意标题:")
        print("-" * 60)
        caption = analyzer.generate_caption(image_path, style="创意")
        print(caption)
        
        # 6. 图片分类
        print("\n[6] 图片分类:")
        print("-" * 60)
        category = analyzer.categorize(image_path)
        print(category)
        
        print("\n" + "=" * 60)
        print("✅ 演示完成!")
        print("=" * 60 + "\n")
        
    except FileNotFoundError as e:
        print(f"\n❌ 错误: {e}\n")
    except requests.exceptions.ConnectionError:
        print("\n❌ 错误: 无法连接到服务器")
        print("请确保服务器已启动: python main.py\n")
    except Exception as e:
        print(f"\n❌ 错误: {e}\n")

