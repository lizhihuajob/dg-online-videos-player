# 视频播放器

## 📖 项目简介

本系统是一款基于 Web 技术构建的个人音视频管理平台，用户只需通过浏览器即可随时随地访问和管理自己的数字媒体资产，彻底打破设备与操作系统的壁垒。系统采用 B/S 架构，将多媒体文件集中存储于服务器或云存储中，通过直观的网页界面提供强大的管理、检索与播放功能，旨在为用户提供一个私有、安全且智能化的私人影音中心。

## 🛠 技术栈
- **Frontend**: Vue 3 + Vite + XGPlayer + Video.js
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Authentication**: JWT + bcrypt
- **Styling**: SCSS
- **Container**: Docker + Docker Compose + Nginx

## � 功能列表

### ✅ 已实现功能

#### 🔐 用户认证
- [x] 用户注册（用户名、邮箱、密码）
- [x] 用户登录（JWT Token 认证）
- [x] 退出登录
- [x] 个人信息查看
- [x] 修改个人信息（用户名、邮箱）
- [x] 修改密码（需验证当前密码）

#### 🎬 视频播放
- [x] 在线视频播放（MP4, WebM, HLS/M3U8, FLV, RTMP）
- [x] 本地视频文件播放
- [x] 拖拽上传本地视频
- [x] 视频文件上传至服务器
- [x] 播放进度控制
- [x] 音量控制
- [x] 全屏播放

#### 📜 播放历史
- [x] 在线视频播放历史记录
- [x] 本地视频播放历史记录
- [x] 播放历史列表展示
- [x] 双击播放历史记录
- [x] 删除单条播放历史
- [x] 清空全部播放历史
- [x] 历史记录本地存储（未登录状态）
- [x] 历史记录云端同步（登录状态）

#### 👤 个人中心
- [x] 个人资料展示
- [x] 编辑个人信息
- [x] 修改登录密码
- [x] 用户头像（首字母显示）

#### 🎨 界面功能
- [x] 响应式布局设计
- [x] 现代化 UI（渐变、毛玻璃效果）
- [x] 暗黑主题
- [x] 移动端适配
- [x] 播放列表侧边栏
- [x] 模态弹窗交互
- [x] 加载动画
- [x] 错误提示

#### 🛠 技术功能
- [x] RESTful API 设计
- [x] JWT 身份认证
- [x] 密码加密存储（bcrypt）
- [x] 数据库持久化（PostgreSQL）
- [x] 文件上传存储
- [x] 单元测试覆盖（45个测试用例）
- [x] Docker 容器化部署
- [x] 一键测试脚本

---

### 📝 TODO（待实现功能）

#### 🎬 视频播放增强
- [ ] 播放进度记忆（断点续播）
- [ ] 播放速度调节（0.5x - 2.0x）
- [ ] 画中画模式
- [ ] 循环播放/单曲循环
- [ ] 视频截图功能
- [ ] 字幕加载（SRT, VTT）
- [ ] 音轨切换
- [ ] 画质选择（多码率切换）

#### 📁 视频管理
- [ ] 视频分类/标签
- [ ] 视频搜索功能
- [ ] 视频收藏功能
- [ ] 视频评分/点赞
- [ ] 视频信息编辑（标题、描述、封面）
- [ ] 批量操作（批量删除、批量移动）
- [ ] 视频文件夹管理
- [ ] 回收站功能

#### 🔍 智能功能
- [ ] 视频缩略图生成
- [ ] 视频时长自动识别
- [ ] 视频格式自动转换
- [ ] 智能推荐算法
- [ ] 观看统计分析
- [ ] 热门视频排行

#### 👥 用户系统增强
- [ ] 用户头像上传
- [ ] 用户等级/积分系统
- [ ] 第三方登录（GitHub, Google）
- [ ] 邮箱验证
- [ ] 密码找回功能
- [ ] 多设备登录管理

#### 🔒 安全与隐私
- [ ] 视频访问权限控制（私有/公开）
- [ ] 分享链接生成（带过期时间）
- [ ] 播放密码保护
- [ ] IP 访问限制
- [ ] 操作日志记录

#### 📱 移动端优化
- [ ] 手势控制（滑动调节进度/音量）
- [ ] 竖屏全屏播放
- [ ] 后台音频播放
- [ ] 锁屏播放控制

#### 🌐 系统功能
- [ ] 多语言支持（i18n）
- [ ] 系统设置面板
- [ ] 主题切换（暗黑/明亮）
- [ ] 通知系统
- [ ] 数据备份/恢复
- [ ] 系统监控面板

#### ☁️ 云存储集成
- [ ] 阿里云 OSS 存储
- [ ] 腾讯云 COS 存储
- [ ] AWS S3 存储
- [ ] CDN 加速支持

---

## �📁 项目结构

```
dg-online-videos-player/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── auth.py         # JWT 认证
│   │   ├── database.py     # 数据库配置
│   │   ├── main.py         # API 路由
│   │   └── models.py       # 数据模型
│   ├── tests/              # 单元测试
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Vue3 前端
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── data/                   # 上传文件存储目录
├── docker-compose.yml      # Docker 编排配置
├── test.sh                 # 一键测试脚本
└── README.md
```

## 🚀 启动指南

### 环境要求
- Docker Desktop 20.10+
- Docker Compose 2.0+

### 快速启动
```bash
# 1. 克隆项目后进入根目录
cd dg-online-videos-player

# 2. 启动所有服务
docker compose up --build

# 3. 等待服务启动完成（约 30-60 秒）
```

### 停止服务
```bash
docker compose down

# 同时删除数据卷（谨慎使用）
docker compose down -v
```

## 🔗 服务地址
| 服务 | 地址 | 说明 |
|------|------|------|
| Frontend | http://localhost:3000 | Web 应用界面 |
| Backend API | http://localhost:8000 | RESTful API |
| API 文档 | http://localhost:8000/docs | Swagger UI |

## 🧪 测试

### 一键测试
项目根目录提供了 `test.sh` 脚本，可快速运行所有测试：

```bash
# 运行全部测试
./test.sh
```

### 手动运行测试
```bash
cd backend

# 使用内存数据库运行测试（推荐）
DATABASE_URL="sqlite:///:memory:" python3 -m pytest tests/ -v

# 或使用 SQLite 文件数据库
DATABASE_URL="sqlite:///./test.db" python3 -m pytest tests/ -v
```

### 测试覆盖范围

#### 🔐 认证模块 (`test_auth.py`)
- ✅ 密码哈希生成与验证
- ✅ 错误密码验证失败
- ✅ 相同密码生成不同哈希（盐值随机）
- ✅ 空密码处理
- ✅ JWT Token 创建与解析
- ✅ Token 过期时间设置
- ✅ Token 附加数据存储

#### 👤 用户认证 (`test_main.py`)
- ✅ 新用户注册
- ✅ 重复用户名/邮箱注册失败
- ✅ 登录成功/失败场景
- ✅ 获取当前用户信息
- ✅ 无效 Token 处理
- ✅ 未授权访问控制

#### 📝 用户信息管理
- ✅ 更新用户信息
- ✅ 更新为已存在用户名/邮箱失败
- ✅ 修改密码（验证当前密码）
- ✅ 错误当前密码修改失败

#### 📺 播放历史
- ✅ 添加播放历史
- ✅ 重复添加自动更新
- ✅ 获取播放历史列表
- ✅ 删除单条历史
- ✅ 删除不存在的历史（404）
- ✅ 清空全部历史

#### 💻 本地播放历史
- ✅ 添加本地视频历史
- ✅ 获取本地历史列表
- ✅ 删除本地历史
- ✅ 清空本地历史

#### 📤 视频上传
- ✅ 上传视频文件成功
- ✅ 上传不同格式视频（MP4, WebM, OGV, MOV）
- ✅ 上传非视频文件失败
- ✅ 上传图片文件失败
- ✅ 未授权上传失败

**测试结果**: 45 个测试用例全部通过

## 📤 文件上传功能

### 上传 API
- **接口**: `POST /upload`
- **认证**: 需要 Bearer Token
- **请求体**: `multipart/form-data`，字段名: `file`
- **支持格式**: MP4, WebM, FLV, HLS 等视频格式

### 存储说明
- 上传的视频文件存储在 `./data` 目录（Docker 卷挂载）
- 文件使用 UUID 重命名，避免冲突
- 访问路径: `/uploads/{uuid}.{ext}`

### 示例响应
```json
{
  "filename": "example.mp4",
  "url": "/uploads/f6306a24-861b-4354-af7c-7b71e9bd884c.mp4",
  "format": "mp4"
}
```

## ✨ 功能特性
- 📱 完美支持移动端 H5
- 🎬 支持多种视频格式（MP4, WebM, FLV）
- 📺 支持流媒体播放（HLS, DASH）
- 🎨 现代化 UI 设计，响应式布局
- ⚡ 流畅的交互体验
- 📋 视频列表与详情页
- 🔁 播放列表功能
- 👤 用户认证与播放历史

## 🎨 设计亮点
- 渐变背景与现代卡片设计
- 优雅的过渡动画
- 完整的加载状态与错误处理
- 移动端优化的触摸交互
- 自适应视频播放器

## 🐳 Docker 镜像说明

### 服务组成
| 服务 | 镜像 | 说明 |
|------|------|------|
| Frontend | `node:20-alpine` + `nginx:alpine` | Vue3 构建 + Nginx 服务 |
| Backend | Python 3.12 + FastAPI | RESTful API 服务 |
| Database | `postgres:16-alpine` | PostgreSQL 数据库 |

### 镜像源配置
- **Node.js**: 使用官方 `node:20-alpine` 镜像
- **npm**: 配置淘宝镜像加速 `https://registry.npmmirror.com`
- **Nginx**: 使用官方 `nginx:alpine` 镜像
- **PostgreSQL**: 使用官方 `postgres:16-alpine` 镜像

## 📝 API 接口概览

### 认证接口
- `POST /register` - 用户注册
- `POST /token` - 用户登录（获取 JWT）
- `GET /users/me` - 获取当前用户信息

### 播放历史
- `GET /play-history` - 获取播放历史
- `POST /play-history` - 添加播放记录
- `DELETE /play-history/{id}` - 删除单条记录
- `DELETE /play-history` - 清空播放历史

### 本地播放历史
- `GET /local-play-history` - 获取本地视频历史
- `POST /local-play-history` - 添加本地视频记录
- `DELETE /local-play-history/{id}` - 删除本地记录

### 视频上传
- `POST /upload` - 上传视频文件

## 🔧 开发环境配置

### 后端开发
```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端开发
```bash
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev

# 构建生产版本
npm run build
```

## ⚠️ 注意事项

1. **首次启动**: Docker 构建可能需要几分钟时间，请耐心等待
2. **数据持久化**: 上传的文件和数据库数据会保存在 Docker 卷中，重启后保留
3. **端口占用**: 确保 3000 和 8000 端口未被其他服务占用
4. **内存要求**: 建议分配至少 2GB 内存给 Docker

## 📄 许可证

MIT License
