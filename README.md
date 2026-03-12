# 视频播放器

## 🛠 技术栈
- Frontend: Vue 3 + Vite + XGPlayer
- Styling: SCSS
- Container: Docker + Nginx

## 🚀 启动指南 (How to Run)
1. 确保 Docker Desktop 已启动。
2. 在根目录执行：`docker compose up --build`
3. 等待容器启动完成...

## 🔗 服务地址 (Services)
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## 📤 文件上传功能
本项目支持本地视频文件上传功能：

### 上传API
- **接口**: `POST /upload`
- **认证**: 需要 Bearer Token
- **请求体**: `multipart/form-data` 格式，字段名: `file`
- **支持格式**: MP4, WebM 等视频格式

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
- 🎬 支持多种视频格式（MP4, WebM）
- 📺 支持流媒体播放（HLS, DASH）
- 🎨 现代化 UI 设计，响应式布局
- ⚡ 流畅的交互体验
- 📋 视频列表与详情页
- 🔁 播放列表功能

## 🎨 设计亮点
- 渐变背景与现代卡片设计
- 优雅的过渡动画
- 完整的加载状态与错误处理
- 移动端优化的触摸交互
- 自适应视频播放器

---

## 🐳 Docker 镜像源配置 (Docker Registry Configuration)

### 推荐配置（基于实际项目验证）

#### 1. Docker 镜像源
**使用官方 Docker Hub 镜像**（已验证稳定可用）

```yaml
# docker-compose.yml 示例
services:
  frontend:
    build: ./frontend
    # Dockerfile 中使用：
    # - Node.js: node:20-alpine
    # - Nginx: nginx:alpine
```

#### 2. npm 依赖源
**使用淘宝镜像**（国内访问快）

在 `Dockerfile` 中添加：
```dockerfile
RUN npm config set registry https://registry.npmmirror.com
```

### 常用镜像推荐

| 技术栈 | 推荐镜像 | 说明 |
|--------|---------|------|
| Node.js | `node:20-alpine` | 前端构建 |
| Nginx | `nginx:alpine` | 前端生产环境 |

### 配置示例

#### Vue3 项目 Dockerfile
```dockerfile
# 构建阶段
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm config set registry https://registry.npmmirror.com
RUN npm ci
COPY . .
RUN npm run build

# 生产阶段
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 使用建议

1. ✅ **优先使用官方镜像**：稳定可靠，无需配置镜像代理
2. ✅ **使用 Alpine 版本**：镜像体积小，构建速度快
3. ✅ **配置 npm 淘宝源**：加速国内依赖下载
4. ✅ **多阶段构建**：减小最终镜像体积

### 常见问题

**Q: Docker 镜像拉取失败？**
A: 检查网络连接，确保 Docker Desktop 正常运行

**Q: npm install 很慢？**
A: 确保已配置淘宝镜像源：`npm config set registry https://registry.npmmirror.com`
