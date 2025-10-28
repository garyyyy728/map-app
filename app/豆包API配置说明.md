# 豆包大模型配置说明

## 一、获取 API Key

1. 访问火山引擎控制台：https://console.volcengine.com/ark
2. 登录/注册字节跳动账号
3. 进入"模型推理"服务
4. 创建 API Key 并保存

## 二、配置环境变量

1. 复制 `.env.example` 文件为 `.env`
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入你的 API Key：
   ```
   DOUBAO_API_KEY=你的API密钥
   ```

## 三、安装依赖

```bash
pip install -r requirements.txt
```

## 四、启动服务

```bash
python main.py
```

服务将在 http://localhost:8000 启动

## 五、访问文档

启动后可以访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 六、API 端点

所有 API 端点都已从 `/api/gemini/*` 更改为 `/api/doubao/*`：

- `POST /api/doubao/generate` - 文本生成
- `POST /api/doubao/chat` - 对话接口
- `POST /api/doubao/analyze-image` - 图片分析
- `GET /api/doubao/models` - 获取模型列表

## 七、可用模型

- `doubao-1.5-pro-32k` - 主力模型（32k上下文）
- `doubao-1.5-pro-256k` - 长文本模型（256k上下文）
- `doubao-lite-32k` - 轻量模型
- `doubao-vision-pro-32k` - 视觉模型（用于图片分析）

## 八、使用示例

### 文本生成
```bash
curl -X POST "http://localhost:8000/api/doubao/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "请用简单的语言解释什么是人工智能",
    "model": "doubao-1.5-pro-32k",
    "temperature": 0.7
  }'
```

### 对话
```bash
curl -X POST "http://localhost:8000/api/doubao/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "你好"}
    ],
    "temperature": 0.8
  }'
```

### 图片分析
```bash
curl -X POST "http://localhost:8000/api/doubao/analyze-image" \
  -F "image=@/path/to/image.jpg" \
  -F "prompt=描述这张图片"
```

## 九、注意事项

1. **API 密钥安全**：请妥善保管你的 API Key，不要提交到版本控制系统
2. **模型选择**：根据任务选择合适的模型
   - 日常对话：使用 `doubao-1.5-pro-32k`
   - 长文本处理：使用 `doubao-1.5-pro-256k`
   - 快速响应：使用 `doubao-lite-32k`
   - 图片分析：使用 `doubao-vision-pro-32k`
3. **费用控制**：注意 API 调用产生的费用
4. **代理设置**：如果网络无法直接访问，可以在 `.env` 中配置代理

## 十、常见问题

### Q: API Key 在哪里获取？
A: 登录火山引擎控制台，在"模型推理 - ARK"服务中创建。

### Q: 提示认证失败怎么办？
A: 检查 `.env` 文件中的 `DOUBAO_API_KEY` 是否正确配置。

### Q: 图片分析不支持怎么办？
A: 确保使用 `doubao-vision-pro-32k` 模型，这是专门的视觉模型。

### Q: 如何查看详细的错误日志？
A: 日志会输出到控制台，如果需要更详细的日志，可以在 `main.py` 中调整日志级别。

