# 快速开始指南

这个指南将帮助您在 5 分钟内启动并运行 Gemini API 后台服务。

## 第一步：获取 API Key

1. 访问 [Google AI Studio](https://ai.google.dev/gemini-api/docs)
2. 点击 "获取 API 密钥"
3. 登录您的 Google 账号
4. 创建或选择一个项目
5. 复制生成的 API Key

## 第二步：安装依赖

```bash
# 确保您已安装 Python 3.10 或更高版本
python --version

# 安装项目依赖
pip install -r requirements.txt
```

## 第三步：配置环境

### 方法 1: 使用配置脚本（推荐）

```bash
python env_setup.py
```

按照提示输入您的 API Key 和其他配置。

### 方法 2: 手动创建 .env 文件

创建一个名为 `.env` 的文件，内容如下：

```env
GEMINI_API_KEY=your_api_key_here
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

将 `your_api_key_here` 替换为您的实际 API Key。

## 第四步：启动服务器

```bash
python main.py
```

您应该看到类似这样的输出：

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 第五步：测试 API

### 方法 1: 访问交互式文档

在浏览器中打开 http://localhost:8000/docs

您将看到一个完整的 API 文档页面，可以直接在浏览器中测试所有接口。

### 方法 2: 使用测试脚本

打开新的终端窗口，运行：

```bash
python test_api.py
```

### 方法 3: 使用 curl

```bash
# 健康检查
curl http://localhost:8000/health

# 生成文本
curl -X POST http://localhost:8000/api/gemini/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "你好，介绍一下你自己", "temperature": 0.7}'
```

### 方法 4: 运行示例代码

```bash
python examples/example_usage.py
```

## 🎉 完成！

现在您已经成功启动了 Gemini API 后台服务！

## 下一步

- 📖 查看完整的 [API 文档](http://localhost:8000/docs)
- 📚 阅读 [README.md](README.md) 了解更多功能
- 💻 查看 [examples/example_usage.py](examples/example_usage.py) 学习如何使用
- 🐳 了解如何使用 Docker 部署

## 常见问题

### 1. 服务启动失败

**错误**: `ValueError: Gemini API key is required`

**解决**: 确保 `.env` 文件存在且包含有效的 `GEMINI_API_KEY`

### 2. API 调用失败

**错误**: API 返回 500 错误

**可能原因**:
- API Key 无效或过期
- 网络连接问题
- 超出 API 配额限制

**解决**:
- 检查 API Key 是否正确
- 确认网络可以访问 Google API
- 查看 [API 控制台](https://ai.google.dev/) 检查配额

### 3. 端口被占用

**错误**: `OSError: [Errno 48] Address already in use`

**解决**: 修改 `.env` 文件中的 `PORT` 值，或停止占用 8000 端口的其他程序

## 获取帮助

如果遇到问题，请：

1. 查看服务器日志输出
2. 检查 `.env` 文件配置
3. 阅读完整的 [README.md](README.md)
4. 提交 Issue 或联系技术支持

---

**准备好开始构建了吗？试试这些示例！** 🚀

