# 项目结构说明

## 📁 目录结构

```
Gemini-API-Backend/
│
├── main.py                     # FastAPI 主应用入口
├── config.py                   # 应用配置管理（环境变量、设置）
├── dependencies.py             # FastAPI 依赖注入
├── requirements.txt            # Python 依赖包列表
├── .gitignore                 # Git 忽略文件配置
│
├── models/                     # 数据模型层
│   ├── __init__.py            # 模块初始化
│   ├── requests.py            # API 请求数据模型
│   └── responses.py           # API 响应数据模型
│
├── routers/                    # API 路由层
│   ├── __init__.py            # 模块初始化
│   └── gemini_router.py       # Gemini API 相关路由
│
├── services/                   # 业务逻辑层
│   ├── __init__.py            # 模块初始化
│   └── gemini_service.py      # Gemini API 服务封装
│
├── examples/                   # 示例代码
│   ├── __init__.py            # 模块初始化
│   └── example_usage.py       # API 使用示例
│
├── env_setup.py               # 环境配置辅助脚本
├── test_api.py                # API 测试脚本
│
├── Dockerfile                 # Docker 镜像构建文件
├── docker-compose.yml         # Docker Compose 配置
├── .dockerignore             # Docker 忽略文件配置
│
├── README.md                  # 项目完整文档
├── QUICKSTART.md             # 快速入门指南
└── PROJECT_STRUCTURE.md      # 项目结构说明（本文件）
```

## 🏗️ 架构设计

本项目采用经典的三层架构设计：

### 1. 路由层（Routers）

**职责**: 处理 HTTP 请求，定义 API 端点

- `routers/gemini_router.py`: 所有 Gemini 相关的 API 端点
  - `/api/gemini/generate` - 文本生成
  - `/api/gemini/chat` - 对话接口
  - `/api/gemini/analyze-image` - 图片分析
  - `/api/gemini/models` - 模型列表

### 2. 服务层（Services）

**职责**: 封装业务逻辑，与外部 API 交互

- `services/gemini_service.py`: Gemini API 的完整封装
  - `generate_text()` - 文本生成逻辑
  - `chat()` - 对话管理
  - `analyze_image()` - 图片分析
  - `list_models()` - 获取可用模型

### 3. 模型层（Models）

**职责**: 定义数据结构，验证输入输出

- `models/requests.py`: API 请求的数据模型
  - `GenerateTextRequest`
  - `ChatRequest`
  - `ImageAnalyzeRequest`

- `models/responses.py`: API 响应的数据模型
  - `GenerateTextResponse`
  - `ChatResponse`
  - `ImageAnalyzeResponse`
  - `ModelsListResponse`

## 🔄 数据流

```
客户端请求
    ↓
路由层（Router）
    ↓
数据验证（Pydantic Model）
    ↓
服务层（Service）
    ↓
Gemini API
    ↓
响应处理
    ↓
返回客户端
```

## 🔧 核心组件

### 配置管理 (`config.py`)

- 使用 Pydantic Settings 管理配置
- 支持从环境变量读取
- 单例模式确保配置一致性

### 依赖注入 (`dependencies.py`)

- FastAPI 依赖注入系统
- 服务实例的统一管理
- 便于测试和维护

### 主应用 (`main.py`)

- FastAPI 应用初始化
- 中间件配置（CORS）
- 全局异常处理
- 路由注册

## 📦 辅助工具

### 环境配置 (`env_setup.py`)

交互式创建 `.env` 文件，简化配置过程。

### 测试脚本 (`test_api.py`)

快速测试所有 API 端点，验证服务是否正常工作。

### 示例代码 (`examples/example_usage.py`)

展示如何在 Python 中调用 API，包含多个实用示例。

## 🐳 部署支持

### Docker 部署

- `Dockerfile`: 定义镜像构建过程
- `docker-compose.yml`: 快速启动服务
- `.dockerignore`: 优化镜像大小

## 🎯 设计原则

1. **关注点分离**: 路由、业务逻辑、数据模型分离
2. **单一职责**: 每个模块只负责一个功能
3. **依赖注入**: 解耦组件，便于测试
4. **类型安全**: 使用 Pydantic 进行数据验证
5. **错误处理**: 完善的异常处理机制
6. **可扩展性**: 易于添加新的 API 端点

## 🚀 扩展建议

### 添加新的 API 端点

1. 在 `models/requests.py` 中定义请求模型
2. 在 `models/responses.py` 中定义响应模型
3. 在 `services/gemini_service.py` 中实现业务逻辑
4. 在 `routers/gemini_router.py` 中添加路由
5. 更新文档和测试

### 添加数据库支持

1. 创建 `database/` 目录
2. 添加 SQLAlchemy 或其他 ORM
3. 创建数据模型和迁移
4. 在服务层集成数据库操作

### 添加认证授权

1. 创建 `auth/` 目录
2. 实现 JWT 或 OAuth2
3. 添加认证中间件
4. 保护需要认证的端点

### 添加缓存

1. 集成 Redis
2. 在服务层添加缓存逻辑
3. 实现缓存失效策略

## 📝 代码规范

- 遵循 PEP 8 规范
- 使用类型提示（Type Hints）
- 编写 Docstring 文档
- 保持函数简洁（单一职责）
- 使用有意义的变量名

## 🧪 测试建议

建议添加以下测试：

1. **单元测试**: 测试服务层的各个方法
2. **集成测试**: 测试 API 端点
3. **性能测试**: 测试并发处理能力
4. **安全测试**: 测试输入验证和错误处理

---

**这个项目结构清晰、易于理解和维护，适合作为生产环境的后台 API 服务！** ✨

