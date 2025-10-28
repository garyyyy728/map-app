"""
检查 genai.Client 的参数和配置选项
"""
from google import genai
import inspect

print("=== genai.Client 初始化参数 ===")
print(inspect.signature(genai.Client.__init__))
print()

print("=== genai.Client 文档 ===")
print(genai.Client.__init__.__doc__)
print()

# 尝试查看 HttpOptions
try:
    from google.genai.client import HttpOptions
    print("=== HttpOptions 字段 ===")
    if hasattr(HttpOptions, 'model_fields'):
        for field_name, field_info in HttpOptions.model_fields.items():
            print(f"  - {field_name}: {field_info}")
except Exception as e:
    print(f"无法导入 HttpOptions: {e}")

# 查看 Client 类的所有属性
print("\n=== Client 的所有公开方法 ===")
for attr in dir(genai.Client):
    if not attr.startswith('_'):
        print(f"  - {attr}")

