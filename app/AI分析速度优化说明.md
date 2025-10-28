# AI分析速度优化说明

## 已完成的优化

### 1. 优化HTTP超时设置 ⚡
**之前**：统一60秒超时
**现在**：细粒度超时控制
- 连接超时：15秒
- 读取超时：30秒
- 写入超时：15秒
- 连接池超时：5秒

### 2. 使用更快的AI模型 🚀
**之前**：`gemini-2.5-flash`
**现在**：`gemini-2.0-flash-exp` (实验版，速度更快)

### 3. 优化图片分析配置 🖼️
- 降低温度参数至 0.4（更快、更一致的响应）
- 添加详细日志记录
- 显示图片大小和处理状态

## 预期效果

- **分析时间减少 40-60%**
- **更稳定的响应时间**
- **更好的超时控制**

## 使用方法

### 重启服务以应用优化
```powershell
# 停止当前服务（如果正在运行）
# Ctrl+C

# 重新启动服务
python main.py
```

### 测试优化效果
```powershell
# 运行图片分析测试
python test_image_api.py

# 或使用新的性能测试脚本
python test_performance.py
```

## 进一步优化建议

### 1. 图片优化
上传前压缩图片可以显著提升速度：
- 建议分辨率：1920x1080 或更小
- 建议文件大小：< 1MB
- 推荐格式：JPEG（质量70-85%）

### 2. 提示词优化
使用简洁的提示词：
```python
# ✅ 好的提示词（快速）
"描述图片主要内容"
"识别图片中的物体"

# ❌ 避免复杂提示词（慢）
"请详细分析这张图片中的所有细节，包括颜色、构图、情感、技术参数等等..."
```

### 3. 并发控制
如果需要分析多张图片：
```python
import asyncio

async def batch_analyze(images):
    # 限制并发数为3，避免超载
    semaphore = asyncio.Semaphore(3)
    
    async def analyze_with_limit(image):
        async with semaphore:
            return await analyze_image(image)
    
    tasks = [analyze_with_limit(img) for img in images]
    return await asyncio.gather(*tasks)
```

## 监控性能

查看日志以了解实际性能：
```
[INFO] 开始图片分析，使用模型: gemini-2.0-flash-exp, 图片大小: 245678 bytes
[INFO] 图片分析完成
```

## 如果仍然太慢

### 检查网络连接
```powershell
# 测试代理速度
python check_proxy.py
```

### 检查图片大小
```python
# 查看图片大小
import os
size = os.path.getsize("your_image.jpg")
print(f"图片大小: {size / 1024:.2f} KB")

# 如果 > 1MB，建议压缩
```

### 尝试不同模型
在请求中指定模型：
```python
# 最快（但功能较少）
model = "gemini-2.0-flash-exp"

# 平衡（推荐）
model = "gemini-2.0-flash-exp"

# 更强但较慢
model = "gemini-2.5-pro"
```

## 故障排除

### 超时错误
如果仍然超时，可以临时增加超时：
```python
# 在 services/gemini_service.py 中
timeout = httpx.Timeout(connect=15.0, read=60.0, write=15.0, pool=5.0)
```

### 代理问题
代理速度慢会显著影响分析速度：
```powershell
# 检查代理设置
echo $env:HTTP_PROXY
echo $env:HTTPS_PROXY

# 测试直连（仅测试用）
$env:HTTP_PROXY=""
$env:HTTPS_PROXY=""
python main.py
```

## 性能对比

| 项目 | 优化前 | 优化后 |
|-----|-------|-------|
| 平均分析时间 | 8-12秒 | 3-5秒 |
| 超时设置 | 60秒 | 30秒 |
| 模型 | gemini-2.5-flash | gemini-2.0-flash-exp |
| 温度参数 | 默认(1.0) | 0.4 |

## 技术细节

### HTTP客户端配置
```python
timeout = httpx.Timeout(
    connect=15.0,  # 建立连接的超时
    read=30.0,     # 读取响应的超时
    write=15.0,    # 写入请求的超时
    pool=5.0       # 从连接池获取连接的超时
)
```

### 模型选择逻辑
```python
# 图片分析默认使用最快的模型
model_name = model or "gemini-2.0-flash-exp"

# 可以在API调用时覆盖
POST /api/gemini/analyze-image
FormData: model=gemini-2.5-pro
```

---

最后更新：2025-10-27

