# Calendar Takeover

![Calendar Interface](https://via.placeholder.com/800x400?text=Calendar+Takeover+Interface)

一个基于AI的智能日历管理系统，使用FastAPI后端和HTML/JS前端，集成DeepSeek AI实现自然语言事件创建。

## 📋 目录

- [项目概述](#项目概述)
- [功能特性](#功能特性)
- [系统架构](#系统架构)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [详细配置](#详细配置)
- [API文档](#api文档)
- [使用示例](#使用示例)
- [问题排查](#问题排查)
- [开发指南](#开发指南)

## 📝 项目概述

Calendar Takeover 是一个智能日历系统，允许用户通过自然语言与AI助手交互来添加和管理事件。系统提供直观的暗色主题界面，响应式设计，以及强大的自然语言处理能力。

本项目旨在简化日历管理体验，让用户能够通过类似于与助手对话的方式创建复杂的日程安排，无需使用繁琐的表单或复杂的时间选择器。

## ✨ 功能特性

- **🗓️ 暗色主题日历**：美观的暗色UI，支持月视图和日视图
- **🤖 AI智能助手**：支持通过自然语言添加、修改事件
- **📊 事件可视化**：在日历中直观显示事件，并提供详细信息查看
- **🔄 灵活导航**：轻松在月份间切换，跳转到今天
- **📱 响应式设计**：适配不同屏幕尺寸的设备
- **🚀 高性能**：前后端分离架构，提供流畅体验
- **🧩 可扩展性**：模块化设计，方便添加新功能

## 🏗️ 系统架构

该项目采用前后端分离的微服务架构：

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│             │       │             │       │             │
│  前端界面   │◄─────►│  主服务 API  │◄─────►│  DeepSeek   │
│ HTML/JS/CSS │       │   FastAPI   │       │     API     │
│             │       │             │       │             │
└─────────────┘       └──────┬──────┘       └─────────────┘
                             │
                      ┌──────▼──────┐
                      │             │
                      │  AI 聊天    │
                      │  微服务     │
                      │             │
                      └─────────────┘
```

1. **前端**：HTML/CSS/JavaScript实现的单页面应用
   - 渲染日历界面
   - 管理用户交互
   - 通过API与后端通信

2. **主后端**：处理日历事件和基础功能的FastAPI服务
   - 事件的CRUD操作
   - 数据存储和管理
   - 与前端通信

3. **AI聊天微服务**：专门处理自然语言处理的FastAPI服务
   - 接收聊天消息
   - 调用DeepSeek API解析用户意图
   - 将结构化事件数据返回给主服务

4. **DeepSeek AI**：提供强大的自然语言处理能力
   - 将用户自然语言转换为结构化数据
   - 支持多种时间表述和事件描述方式

## 🛠️ 技术栈

- **前端**：
  - HTML5、CSS3、JavaScript
  - 纯原生实现，无外部依赖
  - 响应式网格布局

- **后端**：
  - Python 3.8+
  - FastAPI 框架
  - Uvicorn ASGI服务器
  - HTTPX 异步HTTP客户端

- **AI服务**：
  - DeepSeek API
  - 自定义提示工程

- **存储**：
  - 当前版本：内存存储
  - 可扩展：支持数据库存储

## 🚀 快速开始

### 前提条件

- Python 3.8+
- DeepSeek API 密钥

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/yourusername/takeover.git
   cd takeover
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv takeover_env
   # Windows
   takeover_env\Scripts\activate
   # Linux/macOS
   source takeover_env/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install fastapi uvicorn httpx requests
   ```

4. **配置API密钥**
   在`config.py`中设置您的DeepSeek API密钥：
   ```python
   DEEPSEEK_API_KEY = "your-api-key-here"
   ```

5. **启动服务**
   ```bash
   # 使用run.py启动所有服务
   python run.py
   ```

6. **访问应用**
   在浏览器中打开 `calender.html` 文件


## ⚙️ 详细配置

### 配置文件说明

项目主要配置在 `config.py` 文件中：

```python
# DeepSeek API配置
DEEPSEEK_API_KEY = "your-api-key-here"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# 错误消息配置
ERROR_MESSAGES = {
    "parse_error": "抱歉，我无法理解您的输入...",
    "api_error": "抱歉，AI服务暂时不可用...",
    "validation_error": "请确保提供了事件的日期和标题..."
}

# AI提示模板
EVENT_PROMPT = '''
你是一个日历助手，请将用户输入转换为结构化的事件数据...
'''
```

### 服务端口配置

- **主服务**：默认端口 `8079`
- **AI聊天服务**：默认端口 `8181`

可通过命令行参数修改：

```bash
uvicorn server:app --host 127.0.0.1 --port <自定义端口>
```

### 前端配置

前端API端点配置在 `calender.html` 中：

```javascript
// API端点配置
const API_BASE = ''; // 默认为相对路径
// 如需修改为绝对路径，例如：
// const API_BASE = 'http://127.0.0.1:8079';
```

## 📚 API文档

### 主服务 API (端口 8079)

#### 获取事件

- **GET** `/api/events`
  - 获取所有事件
  - 返回：事件数组

- **GET** `/api/events?date=YYYY-MM-DD`
  - 获取特定日期的事件
  - 参数：`date` - ISO格式日期字符串
  - 返回：事件数组

- **GET** `/api/events?year=YYYY&month=MM`
  - 获取特定月份的事件
  - 参数：`year` - 年份, `month` - 月份(1-12)
  - 返回：事件数组

#### 调试端点

- **GET** `/debug`
  - 获取服务状态信息
  - 返回：调试信息对象

### AI聊天服务 API (端口 8181)

#### 聊天接口

- **POST** `/chat`
  - 处理用户聊天消息
  - 请求体：`{ "message": "用户消息" }`
  - 返回：
    ```json
    {
      "response": "AI回复消息",
      "event": { 
        "title": "事件标题",
        "date": "2024-01-01",
        "time_start": "15:00",
        "time_end": "16:00",
        "description": "事件描述"
      }
    }
    ```
  - 说明：当无法解析事件时，`event`字段为`null`

### 事件数据结构

```json
{
  "title": "事件标题",
  "date": "YYYY-MM-DD",
  "time_start": "HH:MM",
  "time_end": "HH:MM",
  "description": "事件描述"
}
```

## 🎯 使用示例

### 1. 通过AI助手添加事件

![添加事件](https://via.placeholder.com/800x400?text=添加事件)

1. 在左侧聊天框中输入：
   ```
   添加明天下午3点的团队会议
   ```
2. AI助手会解析您的意图，提取关键信息
3. 系统自动创建事件并在日历中显示

### 2. 查看日期详情

![日期详情](https://via.placeholder.com/800x400?text=日期详情)

1. 点击日历中的任何日期
2. 右侧栏会显示该日期的所有事件
3. 查看事件的详细信息，包括时间和描述

### 3. 月份导航

![月份导航](https://via.placeholder.com/800x400?text=月份导航)

1. 使用顶部的箭头按钮在月份间切换
2. 点击"Today"按钮快速跳转到当天

## 🔍 问题排查

### 常见问题

1. **AI服务无法连接**
   - 检查DeepSeek API密钥是否正确
   - 确认网络连接状态
   - 查看AI服务日志

2. **事件未显示在日历上**
   - 确认服务端口配置正确
   - 检查浏览器控制台是否有错误
   - 验证事件格式是否正确

3. **自然语言解析不准确**
   - 尝试使用更明确的语言描述事件
   - 检查EVENT_PROMPT模板是否配置正确
   - 考虑调整API参数降低temperature值

### 错误调试

项目包含两个测试脚本：

- `test_api.py`：全面测试DeepSeek API连接
- `simple_test.py`：简化的端到端测试

运行这些脚本以验证系统各组件的工作状态：

```bash
python test_api.py
python simple_test.py
```

### 日志记录

两个主要服务都包含详细的日志记录：

```bash
# 查看主服务日志
uvicorn server:app --log-level debug

# 查看AI服务日志
uvicorn chat_service:app --log-level debug
```

## 👨‍💻 开发指南

### 项目结构

```
e:\OneDrive\Gits\takeover\
│
├── calender.html        # 前端界面
├── server.py            # 主后端服务
├── chat_service.py      # AI聊天微服务
├── config.py            # 配置文件
├── test_api.py          # API测试脚本
└── simple_test.py       # 简化测试脚本
```

### 扩展事件存储

当前版本使用内存存储事件，可以扩展为使用数据库：

```python
# 在server.py中添加数据库支持
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./calendar.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 创建事件模型
class EventModel(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(String)
    time_start = Column(String, nullable=True)
    time_end = Column(String, nullable=True)
    description = Column(String, nullable=True)
```

### 添加新功能

扩展AI聊天功能以支持更多操作：

```python
# 在chat_service.py中添加更多意图处理
async def chat_with_ai(message: ChatMessage):
    user_message = message.message.lower()
    
    if any(keyword in user_message for keyword in ["添加", "创建", "安排"]):
        # 处理添加事件的逻辑
        return await handle_create_event(user_message)
    
    elif any(keyword in user_message for keyword in ["查找", "搜索", "显示"]):
        # 处理查找事件的逻辑
        return await handle_search_event(user_message)
    
    elif any(keyword in user_message for keyword in ["取消", "删除", "移除"]):
        # 处理删除事件的逻辑
        return await handle_delete_event(user_message)
        
    else:
        # 处理一般对话
        return {"response": "我是您的日历助手..."}
```

## 📜 许可证

此项目仅供学习和研究使用。

---

如有任何问题或建议，欢迎提交Issue或Pull Request。
