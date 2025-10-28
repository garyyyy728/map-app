# 故障排除指南

## 🚨 常见问题及解决方案

---

### ❌ 问题 1: "User location is not supported for the API use"

**错误信息：**
```
400 FAILED_PRECONDITION
User location is not supported for the API use.
```

**原因：**
Google Gemini API 在某些地区（包括中国大陆）受到地理位置限制。

**✅ 解决方案：**

#### 方案 A: 使用代理服务器

1. **配置系统代理或 VPN**
   - 使用 VPN 连接到支持的地区（如美国、日本、新加坡等）
   - 或使用 HTTP/HTTPS 代理

2. **在代码中配置代理**

修改 `services/gemini_service.py`，在初始化 client 时添加代理配置：

```python
import os
import httpx
from google import genai

class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
        # 配置代理
        proxy_url = os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")
        
        if proxy_url:
            # 创建带代理的 httpx 客户端
            transport = httpx.HTTPTransport(proxy=proxy_url)
            http_client = httpx.Client(transport=transport)
            self.client = genai.Client(api_key=api_key, http_client=http_client)
        else:
            self.client = genai.Client(api_key=api_key)
```

3. **在 `.env` 文件中添加代理配置**

```env
GEMINI_API_KEY=your_api_key_here
HOST=0.0.0.0
PORT=8000
DEBUG=True

# 代理配置（根据实际情况填写）
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

#### 方案 B: 使用中转 API 服务

使用支持 Gemini API 的中转服务（第三方代理服务），这些服务在支持的地区运行并转发请求。

#### 方案 C: 部署到云服务器

将此后台服务部署到支持的地区的云服务器：
- AWS (美国、欧洲等地区)
- Google Cloud Platform
- Azure (非中国区)
- Vercel / Railway / Render 等

**使用 Docker 部署示例：**

```bash
# 在云服务器上
git clone your-repo
cd Gemini-API-Backend
docker-compose up -d
```

---

### ❌ 问题 2: API Key 无效

**错误信息：**
```
401 Unauthorized
Invalid API key
```

**解决方案：**

1. 检查 `.env` 文件中的 API Key 是否正确
2. 确认 API Key 没有多余的空格或换行
3. 访问 [Google AI Studio](https://ai.google.dev/) 重新生成 API Key
4. 确认 API Key 已启用并且没有过期

---

### ❌ 问题 3: 端口被占用

**错误信息：**
```
Error: Port 8000 is already in use
```

**解决方案：**

1. **修改端口**
   
   在 `.env` 文件中更改端口：
   ```env
   PORT=8080
   ```

2. **停止占用端口的进程**
   
   ```powershell
   # 查找占用 8000 端口的进程
   netstat -ano | findstr :8000
   
   # 停止进程（替换 PID）
   taskkill /PID <PID> /F
   ```

---

### ❌ 问题 4: 依赖安装失败

**错误信息：**
```
error: metadata-generation-failed
```

**解决方案：**

1. **更新 pip**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **使用预编译版本**
   ```bash
   pip install -r requirements.txt --prefer-binary
   ```

3. **安装 Visual Studio Build Tools**（Windows）
   
   如果某些包需要编译，下载并安装：
   https://visualstudio.microsoft.com/visual-cpp-build-tools/

---

### ❌ 问题 5: 图片分析失败

**错误信息：**
```
Invalid image format
```

**解决方案：**

1. 确保图片格式为 JPEG、PNG、WEBP 或 GIF
2. 确保图片大小不超过 20MB
3. 检查图片文件是否损坏

支持的格式：
- image/jpeg
- image/png  
- image/webp
- image/gif

---

### ❌ 问题 6: 请求超时

**错误信息：**
```
Request timeout
```

**解决方案：**

1. **增加超时时间**

修改 `services/gemini_service.py`：

```python
# 在 generate_text 方法中
response = self.client.models.generate_content(
    model=model,
    contents=prompt,
    config=config,
    timeout=60  # 增加到 60 秒
)
```

2. **减少 max_tokens**
   
   生成更少的内容可以减少响应时间

3. **检查网络连接**
   
   确保网络稳定且速度足够

---

### ❌ 问题 7: CORS 错误（前端调用）

**错误信息：**
```
Access-Control-Allow-Origin header is missing
```

**解决方案：**

修改 `main.py` 中的 CORS 配置：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-domain.com"],  # 添加您的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔍 调试技巧

### 1. 查看详细日志

在 `main.py` 中启用详细日志：

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 2. 测试 API Key

```python
from google import genai

client = genai.Client(api_key="your_api_key")
try:
    models = client.models.list()
    print("API Key 有效！可用模型：", [m.name for m in models])
except Exception as e:
    print(f"错误：{e}")
```

### 3. 使用交互式 API 文档

访问 http://localhost:8000/docs 进行交互式测试。

### 4. 检查服务器状态

```bash
# 健康检查
curl http://localhost:8000/health

# 查看可用模型
curl http://localhost:8000/api/gemini/models
```

---

## 📞 获取帮助

如果上述解决方案都不能解决您的问题：

1. **查看完整错误日志**
   - 检查终端输出
   - 查看服务器日志

2. **检查 Gemini API 状态**
   - 访问 [Google Cloud Status](https://status.cloud.google.com/)
   - 检查 API 配额和限制

3. **查阅官方文档**
   - [Gemini API 文档](https://ai.google.dev/gemini-api/docs)
   - [FastAPI 文档](https://fastapi.tiangolo.com/)

4. **常见问题 FAQ**
   - [Gemini API FAQ](https://ai.google.dev/gemini-api/docs/faq)

---

## ✅ 最佳实践

### 生产环境建议

1. **使用环境变量管理敏感信息**
   - 不要将 API Key 硬编码
   - 不要提交 `.env` 文件到 Git

2. **设置速率限制**
   - 避免超出 API 配额
   - 实现请求队列

3. **错误处理和重试**
   - 实现指数退避重试
   - 记录错误日志

4. **监控和告警**
   - 监控 API 使用情况
   - 设置配额告警

5. **安全性**
   - 使用 HTTPS
   - 实现认证机制
   - 验证用户输入

---

**大部分地理限制问题都可以通过使用 VPN 或代理来解决！** 🌍

