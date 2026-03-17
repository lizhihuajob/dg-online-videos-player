# 视频音乐播放器

一个基于 Vue 3 + FastAPI 的在线视频和音乐播放器，支持视频管理、音乐管理、分组管理和播放记录功能。

## 功能特性

- 视频管理：支持上传、播放、删除视频文件，支持卡片/列表视图切换
- 音乐管理：支持上传、播放、删除音乐文件，支持卡片/列表视图切换
- 分组管理：支持创建视频和音乐分组，以表格形式展示
- 播放记录：记录播放历史
- 用户系统：支持用户注册、登录、头像上传和密码修改
- 响应式设计：适配桌面端和移动端

## 技术栈

### 前端
- Vue 3 + Composition API
- Vue Router
- Pinia (状态管理)
- SCSS (样式)
- xgplayer (视频播放器)

### 后端
- FastAPI
- SQLAlchemy (ORM)
- SQLite (数据库)
- JWT (认证)

## 默认账号信息

- 用户名: `admin`
- 密码: `123456`

## 快速开始

### 使用 Docker 运行

1. 克隆项目
```bash
git clone <repository-url>
cdg-online-videos-player-kimi
```

2. 使用 Docker Compose 启动
```bash
docker-compose up -d
```

3. 访问应用
- 前端: http://localhost:5173
- 后端 API: http://localhost:8000

### 开发环境搭建

#### 后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端

```bash
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

## 项目结构

```
.
├── backend/                 # 后端代码
│   ├── main.py             # FastAPI 主应用
│   ├── models.py           # 数据库模型
│   ├── schemas.py          # Pydantic 模型
│   ├── database.py         # 数据库配置
│   ├── auth.py             # 认证相关
│   └── requirements.txt    # Python 依赖
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── components/     # 组件
│   │   │   ├── music/      # 音乐相关组件
│   │   │   └── VideoPlayer.vue
│   │   ├── views/          # 页面视图
│   │   │   ├── Login.vue
│   │   │   ├── VideoManagement.vue
│   │   │   ├── MusicManagement.vue
│   │   │   ├── GroupManagement.vue
│   │   │   ├── PlayHistory.vue
│   │   │   └── Profile.vue
│   │   ├── stores/         # Pinia 状态管理
│   │   ├── router/         # 路由配置
│   │   └── styles/         # 全局样式
│   └── package.json
└── docker-compose.yml      # Docker 配置
```

## 最近更新

### 2024-03-17
1. 登录页面移除默认账号信息显示
2. 视频管理页面添加卡片/列表视图切换功能
3. 音乐管理页面添加卡片/列表视图切换功能
4. 分组管理页面改为表格形式展示
5. 播放记录页面移除在线视频和本地视频切换按钮
6. 优化个人中心UI布局为左右两栏模式
7. 拆分 MusicManagement.vue 为多个小组件

## API 文档

启动后端服务后，访问 http://localhost:8000/docs 查看完整的 API 文档 (Swagger UI)。

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT License
