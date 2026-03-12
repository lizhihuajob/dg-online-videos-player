<template>
  <div class="main-container">
    <div class="app-layout">
      <!-- Left Sidebar: History -->
      <aside class="sidebar glass">
        <div class="sidebar-header">
          <div class="logo-mini">
            <svg class="logo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M10 8l6 4-6 4V8z" fill="currentColor"/>
            </svg>
            <span>Vision Player</span>
          </div>
        </div>
        
        <!-- User Section -->
        <div class="user-section">
          <div v-if="userStore.isLoggedIn" class="user-info">
            <div class="user-avatar">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <div class="user-details">
              <span class="username">{{ userStore.user?.username }}</span>
              <span class="user-status">已登录</span>
            </div>
            <button class="logout-btn" @click="handleLogout" title="退出登录">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                <polyline points="16 17 21 12 16 7"/>
                <line x1="21" y1="12" x2="9" y2="12"/>
              </svg>
            </button>
          </div>
          <button v-else class="login-btn" @click="showAuthModal = true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
              <polyline points="10 17 15 12 10 7"/>
              <line x1="15" y1="12" x2="3" y2="12"/>
            </svg>
            <span>登录 / 注册</span>
          </button>
        </div>
        
        <div class="history-sidebar-content">
          <div class="section-title">
            <span>播放历史</span>
            <button v-if="historyStore.history.length > 0" class="clear-history" @click="clearHistory">清除</button>
          </div>
          
          <div v-if="historyStore.history.length === 0" class="empty-history">
            <p>暂无播放记录</p>
          </div>
          
          <div class="history-sidebar-list">
            <div 
              v-for="(item, index) in historyStore.history" 
              :key="item.id || index" 
              class="history-sidebar-item"
              :class="{ 'is-active': currentUrl === item.url, 'is-local': item.isLocal }"
              @dblclick="playHistoryItem(item, index)"
              title="双击播放"
            >
              <div class="item-info">
                <div class="name-wrapper">
                  <span v-if="item.isLocal" class="local-tag" :class="{ 'is-expired': item.sid !== historyStore.sessionId }">
                    {{ item.sid === historyStore.sessionId ? '本地' : '已失效' }}
                  </span>
                  <span class="item-name">{{ item.name || item.url }}</span>
                </div>
                <span class="item-time">{{ formatTime(item.timestamp) }}</span>
              </div>
              <div class="item-actions">
                <button class="delete-item-btn" @click.stop="removeHistoryItem(index)" title="删除记录">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 6L6 18M6 6l12 12"/>
                  </svg>
                </button>
                <div class="play-indicator">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7z"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="sidebar-footer">
          <p>双击记录即可播放</p>
          <p v-if="!userStore.isLoggedIn" class="hint">登录后可同步播放记录</p>
        </div>
      </aside>

      <!-- Right Main Content -->
      <div class="main-content">
        <!-- Header -->
        <header class="header">
          <p class="subtitle">极简、强大的网页视频播放解决方案</p>
        </header>

        <!-- Top Controls Section -->
        <section class="top-controls-wrapper">
          <div class="top-controls">
            <!-- URL Input -->
            <div class="url-area">
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                  <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                </svg>
                <input 
                  type="text" 
                  v-model="inputUrl" 
                  placeholder="输入在线视频地址 (MP4, M3U8...)"
                  @keyup.enter="loadUrlVideo"
                >
                <div class="button-group">
                  <button v-if="inputUrl" class="action-btn clear-btn" @click="inputUrl = ''" title="清空">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <path d="M18 6L6 18M6 6l12 12"/>
                    </svg>
                  </button>
                  <button class="action-btn play-btn" @click="loadUrlVideo" title="播放">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <path d="M5 12h14M12 5l7 7-7 7"/>
                    </svg>
                  </button>
                  <button class="action-btn reset-btn" @click="resetUrl" title="重置默认">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <path d="M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Local Upload -->
            <div class="upload-area-mini" @click="fileInput.click()">
              <input type="file" ref="fileInput" @change="handleFileSelect" accept="video/*" hidden>
              <svg class="control-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
              </svg>
              <span>上传本地视频</span>
            </div>
          </div>
        </section>

        <!-- Main Player Section -->
        <main class="player-section">
          <div 
            class="player-card glass"
            @dragover.prevent="dragOver = true" 
            @dragleave.prevent="dragOver = false"
            @drop.prevent="handleDrop"
            :class="{ 'drag-active': dragOver }"
          >
            <div v-if="!currentUrl" class="placeholder" @click="fileInput.click()">
              <svg class="placeholder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2">
                <path d="M20.2 6H3.8C2.8 6 2 6.8 2 7.8V16.2C2 17.2 2.8 18 3.8 18H20.2C21.2 18 22 17.2 22 16.2V7.8C22 6.8 21.2 6 20.2 6Z" />
                <path d="M2 11H22" />
                <path d="M7 6L10 11" />
                <path d="M12 6L15 11" />
                <path d="M17 6L20 11" />
              </svg>
              <p>拖拽视频文件到此处或从上方添加</p>
            </div>
            <VideoPlayer 
              v-else 
              :url="currentUrl" 
              :format="currentFormat" 
              @error="handlePlayerError"
            />
          </div>
        </main>

        <!-- Footer -->
        <footer class="footer">
          <p>© 2024 Vision Player. Supports MP4, WebM, and HLS (M3U8).</p>
        </footer>
      </div>
    </div>

    <!-- Auth Modal -->
    <AuthModal v-if="showAuthModal" @close="showAuthModal = false" />

    <!-- Error Modal -->
    <div v-if="showError" class="modal-overlay" @click="showError = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <h3>播放失败</h3>
        </div>
        <p>{{ errorMessage }}</p>
        <button class="modal-btn" @click="showError = false">确定</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import VideoPlayer from '@/components/VideoPlayer.vue'
import AuthModal from '@/components/AuthModal.vue'
import { useUserStore } from '@/stores/user'
import { useHistoryStore } from '@/stores/history'

const userStore = useUserStore()
const historyStore = useHistoryStore()

const currentUrl = ref('')
const currentFormat = ref('mp4')
const inputUrl = ref('https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8')
const dragOver = ref(false)
const showError = ref(false)
const errorMessage = ref('')
const showAuthModal = ref(false)
const pendingReuploadIndex = ref(-1)
const fileInput = ref(null)

onMounted(async () => {
  userStore.init()
  await historyStore.loadHistory()
})

const handleLogout = () => {
  userStore.logout()
  historyStore.loadHistory()
}

const clearHistory = async () => {
  await historyStore.clearHistory()
}

const removeHistoryItem = async (index) => {
  await historyStore.removeHistoryItem(index)
}

const playHistoryItem = (item, index) => {
  if (item.isLocal) {
    if (item.sid !== historyStore.sessionId) {
      pendingReuploadIndex.value = index
      fileInput.value.click()
      return
    }
    currentUrl.value = item.url
    currentFormat.value = item.format || item.name.split('.').pop().toLowerCase()
    historyStore.addToHistory(item.url, item.name, currentFormat.value, true)
  } else {
    inputUrl.value = item.url
    loadUrlVideo()
  }
}

const formatTime = (timestamp) => {
  const now = Date.now()
  const diff = now - timestamp
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return new Date(timestamp).toLocaleDateString()
}

const handleFileSelect = (e) => {
  const file = e.target.files[0]
  if (file) {
    if (pendingReuploadIndex.value !== -1) {
      playFile(file)
      pendingReuploadIndex.value = -1
    } else {
      playFile(file)
    }
  }
}

const handleDrop = (e) => {
  dragOver.value = false
  const file = e.dataTransfer.files[0]
  if (file && file.type.startsWith('video/')) {
    playFile(file)
  }
}

const playFile = (file) => {
  const url = URL.createObjectURL(file)
  currentUrl.value = url
  currentFormat.value = file.name.split('.').pop().toLowerCase()
  historyStore.addToHistory(url, file.name, currentFormat.value, true)
}

const loadUrlVideo = () => {
  if (!inputUrl.value) return
  currentUrl.value = inputUrl.value
  currentFormat.value = getFormat(inputUrl.value)
  historyStore.addToHistory(inputUrl.value, '', currentFormat.value, false)
}

const resetUrl = () => {
  inputUrl.value = 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8'
}

const getFormat = (url) => {
  const cleanUrl = url.split('?')[0].split('#')[0]
  const ext = cleanUrl.split('.').pop().toLowerCase()
  return ['mp4', 'webm', 'm3u8'].includes(ext) ? ext : 'mp4'
}

const handlePlayerError = (err) => {
  if (currentUrl.value.startsWith('blob:')) {
    errorMessage.value = '本地视频加载失败。可能是链接已过期或文件已被移动，请重新上传。'
  } else {
    errorMessage.value = `无法播放该视频，请检查地址是否正确。(${err.message || '未知错误'})`
  }
  showError.value = true
}
</script>

<style lang="scss" scoped>
.main-container {
  min-height: 100vh;
  background: radial-gradient(circle at top center, #1e293b 0%, #080c14 100%);
  color: #f8fafc;
  overflow: hidden;
}

.app-layout {
  display: flex;
  height: 100vh;
  width: 100%;
}

.sidebar {
  width: 300px;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(15, 23, 42, 0.4);
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
  flex-shrink: 0;

  .sidebar-header {
    padding: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);

    .logo-mini {
      display: flex;
      align-items: center;
      gap: 10px;
      
      .logo-icon {
        width: 24px;
        height: 24px;
        color: #6366f1;
      }

      span {
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: -0.5px;
      }
    }
  }

  .user-section {
    padding: 16px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);

    .user-info {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px;
      background: rgba(99, 102, 241, 0.1);
      border-radius: 12px;
      border: 1px solid rgba(99, 102, 241, 0.2);

      .user-avatar {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;

        svg {
          width: 20px;
          height: 20px;
          color: white;
        }
      }

      .user-details {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 2px;

        .username {
          font-size: 0.9rem;
          font-weight: 600;
          color: #f8fafc;
        }

        .user-status {
          font-size: 0.75rem;
          color: #6366f1;
        }
      }

      .logout-btn {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: transparent;
        border: none;
        color: #64748b;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s;

        &:hover {
          background: rgba(239, 68, 68, 0.1);
          color: #ef4444;
        }

        svg {
          width: 18px;
          height: 18px;
        }
      }
    }

    .login-btn {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 12px;
      background: linear-gradient(135deg, #6366f1, #4f46e5);
      border: none;
      border-radius: 12px;
      color: white;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
      }

      svg {
        width: 18px;
        height: 18px;
      }
    }
  }

  .history-sidebar-content {
    flex: 1;
    overflow-y: auto;
    padding: 20px 0;

    &::-webkit-scrollbar {
      width: 4px;
    }
    &::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 2px;
    }

    .section-title {
      padding: 0 24px 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;

      span {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
      }

      .clear-history {
        background: transparent;
        border: none;
        color: #6366f1;
        font-size: 0.75rem;
        cursor: pointer;
        opacity: 0.7;
        &:hover { opacity: 1; }
      }
    }

    .empty-history {
      padding: 40px 24px;
      text-align: center;
      color: #475569;
      font-size: 0.9rem;
    }

    .history-sidebar-list {
      display: flex;
      flex-direction: column;
    }

    .history-sidebar-item {
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      transition: all 0.2s;
      border-left: 3px solid transparent;

      &:hover {
        background: rgba(255, 255, 255, 0.03);
        .play-indicator { opacity: 1; }
      }

      &.is-active {
        background: rgba(99, 102, 241, 0.05);
        border-left-color: #6366f1;
        .item-name { color: #f8fafc; }
      }

      .item-info {
        flex: 1;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 2px;
      }

      .name-wrapper {
        display: flex;
        align-items: center;
        gap: 6px;
        min-width: 0;
      }

      .local-tag {
        font-size: 10px;
        padding: 1px 4px;
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        border-radius: 4px;
        flex-shrink: 0;
        font-weight: 600;

        &.is-expired {
          background: rgba(244, 63, 94, 0.1);
          color: #fb7185;
        }
      }

      .item-name {
        font-size: 0.85rem;
        color: #94a3b8;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        transition: color 0.2s;
      }

      .item-time {
        font-size: 0.7rem;
        color: #475569;
      }

      .item-actions {
        display: flex;
        align-items: center;
        gap: 8px;
        opacity: 0;
        transition: opacity 0.2s;
      }

      .delete-item-btn {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: transparent;
        border: none;
        color: #64748b;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.2s;

        &:hover {
          background: rgba(239, 68, 68, 0.1);
          color: #ef4444;
        }

        svg {
          width: 14px;
          height: 14px;
        }
      }

      .play-indicator {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #6366f1;

        svg {
          width: 16px;
          height: 16px;
        }
      }

      &:hover {
        background: rgba(255, 255, 255, 0.03);
        .item-actions { opacity: 1; }
      }
    }
  }

  .sidebar-footer {
    padding: 15px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    
    p {
      font-size: 0.75rem;
      color: #475569;
      text-align: center;
      margin: 0;

      &.hint {
        margin-top: 4px;
        color: #6366f1;
      }
    }
  }
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 60px;
  overflow-y: auto;
}

.header {
  text-align: center;
  margin-bottom: 30px;

  .subtitle {
    font-size: 0.9rem;
    color: #64748b;
    font-weight: 300;
  }
}

.top-controls-wrapper {
  width: 100%;
  max-width: 1000px;
  margin-bottom: 24px;
}

.top-controls {
  display: flex;
  gap: 16px;
  align-items: center;
  width: 100%;

  .url-area {
    flex: 1;
  }

  .upload-area-mini {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0 20px;
    height: 50px;
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s;
    color: #a5b4fc;
    white-space: nowrap;

    &:hover {
      background: rgba(99, 102, 241, 0.2);
      border-color: #6366f1;
      color: #f8fafc;
      transform: translateY(-1px);
    }

    .control-icon {
      width: 18px;
      height: 18px;
    }

    span {
      font-size: 0.9rem;
      font-weight: 500;
    }
  }
}

.player-section {
  width: 100%;
  max-width: 1000px;
  margin-bottom: 30px;

  .player-card {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    background: #000;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 20px 50px -12px rgba(0, 0, 0, 0.8);
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);

    &.drag-active {
      border-color: #6366f1;
      transform: scale(1.005);
      box-shadow: 0 0 40px rgba(99, 102, 241, 0.2);
    }
  }

  .placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: #334155;
    transition: all 0.3s;

    &:hover {
      color: #64748b;
      background: rgba(255, 255, 255, 0.01);
    }

    .placeholder-icon {
      width: 60px;
      height: 60px;
      margin-bottom: 16px;
      opacity: 0.4;
    }

    p {
      font-size: 0.95rem;
      letter-spacing: 0.5px;
    }
  }
}

.url-area {
  .input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 4px 4px 4px 16px;
    height: 50px;
    transition: all 0.3s;

    &:focus-within {
      border-color: #6366f1;
      background: rgba(15, 23, 42, 0.8);
      box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
    }

    .input-icon {
      width: 18px;
      height: 18px;
      color: #475569;
      margin-right: 12px;
    }

    input {
      flex: 1;
      background: transparent;
      border: none;
      color: #f8fafc;
      font-size: 0.9rem;
      outline: none;
      padding: 8px 0;

      &::placeholder {
        color: #475569;
      }
    }
  }
}

.button-group {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;

  svg {
    width: 18px;
    height: 18px;
  }

  &.play-btn {
    background: #6366f1;
    color: white;

    &:hover {
      background: #4f46e5;
      transform: scale(1.05);
    }
  }

  &.clear-btn {
    background: transparent;
    color: #475569;

    &:hover {
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.05);
    }
  }

  &.reset-btn {
    background: #334155;
    color: #94a3b8;

    &:hover {
      background: #475569;
      color: #f8fafc;
    }
  }
}

.footer {
  text-align: center;
  margin-top: auto;
  padding: 20px 0;
  
  p {
    font-size: 0.8rem;
    color: #475569;
  }
}

.glass {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-card {
  width: 90%;
  max-width: 400px;
  background: rgba(30, 41, 59, 0.9);
  padding: 30px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;

  .modal-header {
    margin-bottom: 20px;
    
    .error-icon {
      width: 48px;
      height: 48px;
      color: #ef4444;
      margin: 0 auto 15px;
    }

    h3 {
      font-size: 1.25rem;
      margin: 0;
    }
  }

  p {
    color: #94a3b8;
    margin-bottom: 25px;
    line-height: 1.5;
  }

  .modal-btn {
    width: 100%;
    padding: 12px;
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;

    &:hover {
      background: #4f46e5;
    }
  }
}
</style>
