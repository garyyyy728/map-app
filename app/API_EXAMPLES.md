# API 使用示例

本文档提供了使用 Gemini API 后台服务的详细示例。

## 目录

- [文本生成](#文本生成)
- [多轮对话](#多轮对话)
- [图片分析](#图片分析)
- [获取模型列表](#获取模型列表)
- [Python 代码示例](#python-代码示例)
- [JavaScript 代码示例](#javascript-代码示例)
- [错误处理](#错误处理)

---

## 文本生成

### cURL 示例

```bash
curl -X POST http://localhost:8000/api/gemini/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "请解释什么是机器学习",
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| prompt | string | ✅ | 输入提示词 | - |
| model | string | ❌ | 模型名称 | gemini-2.5-flash |
| temperature | float | ❌ | 温度参数 (0-2) | 1.0 |
| max_tokens | int | ❌ | 最大生成词元数 | null |

### 响应示例

```json
{
  "success": true,
  "message": "生成成功",
  "text": "机器学习是人工智能的一个分支，它使计算机能够从数据中学习..."
}
```

---

## 多轮对话

### cURL 示例

```bash
curl -X POST http://localhost:8000/api/gemini/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "你好"},
      {"role": "assistant", "content": "你好！有什么我可以帮助你的吗？"},
      {"role": "user", "content": "介绍一下 Python"}
    ],
    "temperature": 0.8
  }'
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| messages | array | ✅ | 对话历史 | - |
| model | string | ❌ | 模型名称 | gemini-2.5-flash |
| temperature | float | ❌ | 温度参数 (0-2) | 1.0 |

### 消息格式

```json
{
  "role": "user",      // 或 "assistant"
  "content": "消息内容"
}
```

### 响应示例

```json
{
  "success": true,
  "message": "对话成功",
  "reply": "Python 是一种高级编程语言..."
}
```

---

## 图片分析

### cURL 示例

```bash
curl -X POST http://localhost:8000/api/gemini/analyze-image \
  -F "image=@/path/to/image.jpg" \
  -F "prompt=详细描述这张图片" \
  -F "model=gemini-2.5-flash"
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| image | file | ✅ | 图片文件 | - |
| prompt | string | ❌ | 分析提示词 | 描述这张图片 |
| model | string | ❌ | 模型名称 | gemini-2.5-flash |

### 响应示例

```json
{
  "success": true,
  "message": "分析成功",
  "analysis": "这张图片显示了一个美丽的海滩场景..."
}
```

---

## 获取模型列表

### cURL 示例

```bash
curl http://localhost:8000/api/gemini/models
```

### 响应示例

```json
{
  "success": true,
  "message": "获取成功",
  "models": [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro"
  ]
}
```

---

## Python 代码示例

### 基础文本生成

```python
import requests

url = "http://localhost:8000/api/gemini/generate"
payload = {
    "prompt": "写一个 Hello World 程序",
    "temperature": 0.5
}

response = requests.post(url, json=payload)
result = response.json()

if result["success"]:
    print(result["text"])
else:
    print(f"错误: {result['message']}")
```

### 多轮对话

```python
import requests

class GeminiChat:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.messages = []
    
    def send_message(self, message):
        self.messages.append({"role": "user", "content": message})
        
        response = requests.post(
            f"{self.base_url}/api/gemini/chat",
            json={
                "messages": self.messages,
                "temperature": 0.7
            }
        )
        
        result = response.json()
        if result["success"]:
            reply = result["reply"]
            self.messages.append({"role": "assistant", "content": reply})
            return reply
        else:
            return f"错误: {result['message']}"

# 使用示例
chat = GeminiChat()
print(chat.send_message("你好"))
print(chat.send_message("介绍一下 FastAPI"))
```

### 图片分析

```python
import requests

url = "http://localhost:8000/api/gemini/analyze-image"

with open("image.jpg", "rb") as f:
    files = {"image": f}
    data = {"prompt": "这张图片里有什么？"}
    
    response = requests.post(url, files=files, data=data)
    result = response.json()
    
    if result["success"]:
        print(result["analysis"])
```

---

## JavaScript 代码示例

### 使用 Fetch API

```javascript
// 文本生成
async function generateText(prompt) {
  const response = await fetch('http://localhost:8000/api/gemini/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      prompt: prompt,
      temperature: 0.7
    })
  });
  
  const result = await response.json();
  
  if (result.success) {
    console.log(result.text);
  } else {
    console.error(result.message);
  }
}

// 使用
generateText('介绍一下 JavaScript');
```

### 对话接口

```javascript
class GeminiChat {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
    this.messages = [];
  }
  
  async sendMessage(content) {
    this.messages.push({ role: 'user', content });
    
    const response = await fetch(`${this.baseUrl}/api/gemini/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: this.messages,
        temperature: 0.7
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      const reply = result.reply;
      this.messages.push({ role: 'assistant', content: reply });
      return reply;
    } else {
      throw new Error(result.message);
    }
  }
}

// 使用示例
const chat = new GeminiChat();
chat.sendMessage('你好').then(reply => console.log(reply));
```

### 图片分析

```javascript
async function analyzeImage(file) {
  const formData = new FormData();
  formData.append('image', file);
  formData.append('prompt', '描述这张图片');
  
  const response = await fetch('http://localhost:8000/api/gemini/analyze-image', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  
  if (result.success) {
    console.log(result.analysis);
  } else {
    console.error(result.message);
  }
}

// 使用（在浏览器中）
const input = document.querySelector('input[type="file"]');
input.addEventListener('change', (e) => {
  const file = e.target.files[0];
  analyzeImage(file);
});
```

---

## 错误处理

### 错误响应格式

```json
{
  "success": false,
  "message": "错误描述",
  "detail": "详细错误信息"
}
```

### 常见错误代码

| 状态码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未授权（API Key 无效） |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

### Python 错误处理示例

```python
import requests

try:
    response = requests.post(
        "http://localhost:8000/api/gemini/generate",
        json={"prompt": "Hello"},
        timeout=30
    )
    response.raise_for_status()  # 检查 HTTP 错误
    
    result = response.json()
    
    if result["success"]:
        print(result["text"])
    else:
        print(f"API 错误: {result['message']}")
        
except requests.exceptions.ConnectionError:
    print("无法连接到服务器")
except requests.exceptions.Timeout:
    print("请求超时")
except requests.exceptions.HTTPError as e:
    print(f"HTTP 错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

---

## 最佳实践

### 1. 温度参数选择

- **0.0 - 0.3**: 确定性输出，适合事实性问答
- **0.4 - 0.7**: 平衡创造性和准确性，适合大多数场景
- **0.8 - 1.5**: 更有创造性，适合创意写作
- **1.6 - 2.0**: 非常随机，适合头脑风暴

### 2. 提示词优化

```python
# ❌ 不好的提示词
"写一篇文章"

# ✅ 好的提示词
"写一篇 500 字的技术博客文章，介绍 Python 的异步编程，包括示例代码，面向中级开发者"
```

### 3. 对话上下文管理

```python
# 限制对话历史长度，避免超出上下文窗口
MAX_MESSAGES = 20

if len(messages) > MAX_MESSAGES:
    messages = messages[-MAX_MESSAGES:]
```

### 4. 错误重试

```python
import time

def retry_request(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i == max_retries - 1:
                raise
            time.sleep(2 ** i)  # 指数退避
```

---

## 完整示例应用

查看 `examples/example_usage.py` 获取更多完整的实用示例。

运行示例：

```bash
python examples/example_usage.py
```

---

**现在您已经了解如何使用所有 API 端点了！** 🎉

