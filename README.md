# Ollama 聊天应用

基于 Ollama 的 Web 聊天应用，使用 Python FastAPI 和 Vue.js 构建。

## 功能特点

- 💬 支持多轮对话
- 🔄 多会话管理
- 🎯 实时响应
- ⚙️ 可调节的模型参数
- 🎨 现代化 UI 界面
- 📝 完整的聊天历史记录

## 技术栈

### 后端
- Python 3.8+
- FastAPI
- Ollama Python SDK
- Uvicorn
- Poetry（依赖管理）

### 前端
- Vue 3
- Element Plus
- Vite
- Axios

## 快速开始

### 前置要求

1. 安装 [Ollama](https://ollama.ai)
2. 安装 Python 3.8+
3. 安装 Node.js 16+
4. 安装 Poetry

### 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd ollama-chat
```

2. 安装后端依赖
```bash
cd backend
poetry install
```

3. 安装前端依赖
```bash
cd frontend
npm install
```

### 启动服务

1. 启动 Ollama 服务
```bash
ollama serve
```

2. 启动后端服务（新终端）
```bash
cd backend
poetry run python app.py
```

3. 启动前端服务（新终端）
```bash
cd frontend
npm run dev
```

4. 访问应用
打开浏览器访问 http://localhost:3000

## API 文档

启动后端服务后，可以通过以下地址访问 API 文档：
- Swagger UI：http://localhost:5001/docs
- ReDoc：http://localhost:5001/redoc

## 主要 API 端点

- POST `/api/chat` - 发送聊天消息
- GET `/api/conversations` - 获取会话列表
- GET `/api/history/{conversation_id}` - 获取指定会话的历史记录
- GET `/api/models` - 获取可用模型列表

## 模型参数配置

可以通过前端界面调整以下参数：
- 模型选择（如 llama2、codellama、mistral 等）
- Temperature（温度，控制输出的随机性）
- Top P（控制输出的多样性）
- Max Tokens（最大生成长度）

## 开发说明

### 后端开发
```bash
cd backend
poetry run python app.py
```

### 前端开发
```bash
cd frontend
npm run dev
```

### 代码格式化
```bash
# 后端
poetry run black .
poetry run isort .

# 前端
npm run lint
```

## 项目结构
```
ollama-chat/
├── backend/
│   ├── app.py           # FastAPI 应用
│   ├── pyproject.toml   # Poetry 配置
│   └── poetry.lock      # 依赖锁定文件
├── frontend/
│   ├── src/
│   │   ├── App.vue     # 主应用组件
│   │   └── main.js     # 入口文件
│   ├── package.json    # npm 配置
│   └── vite.config.js  # Vite 配置
└── README.md
```

## 注意事项

1. 确保 Ollama 服务正在运行
2. 默认端口：
   - 前端：3000
   - 后端：5001
   - Ollama：11434
3. 首次使用需要下载模型，可能需要一些时间

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交改动
4. 推送到分支
5. 提交 Pull Request

## 许可证

MIT License
