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
          <div class="user-area" v-if="currentUser">
            <div class="user-avatar" @click="goToProfile" title="个人中心">
              <img v-if="currentUser.avatar" :src="getAvatarUrl(currentUser.avatar)" alt="头像" class="avatar-image" />
              <span v-else class="avatar-text">{{ currentUser.username.charAt(0).toUpperCase() }}</span>
            </div>
            <span class="username" @click="goToProfile">{{ currentUser.username }}</span>
            <button class="logout-btn" @click="logout" title="退出登录">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>
              </svg>
            </button>
          </div>
          <button v-else class="login-btn" @click="showAuthModal = true" title="登录/注册">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </button>
        </div>
        
        <!-- Add Video Button -->
        <div class="add-video-section">
          <button class="add-video-btn" @click="showAddVideoModal = true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="16"/>
              <line x1="8" y1="12" x2="16" y2="12"/>
            </svg>
            <span>添加视频</span>
          </button>
        </div>

        <div class="history-sidebar-content">
          <!-- 在线视频历史 -->
          <div class="history-section">
            <div class="section-header" @click="toggleOnlineHistory">
              <div class="section-title-wrapper">
                <svg class="section-icon" :class="{ 'collapsed': !isOnlineHistoryOpen }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                  <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                </svg>
                <span class="section-title-text">在线视频</span>
                <span class="section-count" v-if="onlineHistory.length > 0">({{ onlineHistory.length }})</span>
              </div>
              <button v-if="onlineHistory.length > 0 && isOnlineHistoryOpen" class="clear-history" @click.stop="clearOnlineHistory">清除</button>
            </div>
            
            <div v-show="isOnlineHistoryOpen" class="history-list-wrapper">
              <div v-if="onlineHistory.length === 0" class="empty-history">
                <p>暂无在线播放记录</p>
              </div>
              
              <div class="history-sidebar-list">
                <div 
                  v-for="(item, index) in onlineHistory" 
                  :key="'online-' + item.id" 
                  class="history-sidebar-item"
                  :class="{ 'is-active': currentUrl === item.video_url }"
                  @dblclick="playOnlineHistoryItem(item)"
                  title="双击播放"
                >
                  <div class="item-info">
                    <div class="name-wrapper">
                      <span class="item-name">{{ item.video_name || item.video_url }}</span>
                    </div>
                    <span class="item-time">{{ formatTime(item.created_at) }}</span>
                  </div>
                  <div class="item-actions">
                    <button class="delete-item-btn" @click.stop="removeOnlineHistoryItem(item)" title="删除记录">
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
          </div>

          <!-- 本地视频历史 -->
          <div class="history-section">
            <div class="section-header" @click="toggleLocalHistory">
              <div class="section-title-wrapper">
                <svg class="section-icon" :class="{ 'collapsed': !isLocalHistoryOpen }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
                </svg>
                <span class="section-title-text">本地视频</span>
                <span class="section-count" v-if="localHistory.length > 0">({{ localHistory.length }})</span>
              </div>
              <button v-if="localHistory.length > 0 && isLocalHistoryOpen" class="clear-history" @click.stop="clearLocalHistory">清除</button>
            </div>
            
            <div v-show="isLocalHistoryOpen" class="history-list-wrapper">
              <div v-if="localHistory.length === 0" class="empty-history">
                <p>暂无本地播放记录</p>
              </div>
              
              <div class="history-sidebar-list">
                <div 
                  v-for="(item, index) in localHistory" 
                  :key="'local-' + (item.id || index)" 
                  class="history-sidebar-item is-local"
                  :class="{ 'is-active': currentUrl === item.url, 'is-expired': item.sid !== sessionId }"
                  @dblclick="playLocalHistoryItem(item, index)"
                  title="双击播放"
                >
                  <div class="item-info">
                    <div class="name-wrapper">
                      <span class="local-tag" :class="{ 'is-expired': item.sid !== sessionId }">
                        {{ item.sid === sessionId ? '本地' : '需重新上传' }}
                      </span>
                      <span class="item-name">{{ item.video_name || item.name }}</span>
                    </div>
                    <span class="item-time">{{ formatTime(item.timestamp || item.created_at) }}</span>
                  </div>
                  <div class="item-actions">
                    <button class="delete-item-btn" @click.stop="removeLocalHistoryItem(item, index)" title="删除记录">
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
          </div>
        </div>
        
        <div class="sidebar-footer">
          <p>双击播放，本地视频需重新选择文件</p>
        </div>
      </aside>

      <!-- Right Main Content -->
      <div class="main-content">
        <!-- Hidden file input for reupload -->
        <input 
          type="file" 
          ref="fileInput" 
          @change="handleFileSelect" 
          accept="video/*" 
          hidden
        >
        <!-- Main Player Section -->
        <main class="player-section">
          <div 
            class="player-card glass"
            @dragover.prevent="dragOver = true" 
            @dragleave.prevent="dragOver = false"
            @drop.prevent="handleDrop"
            :class="{ 'drag-active': dragOver }"
          >
            <div v-if="!currentUrl" class="placeholder" @click="showAddVideoModal = true">
              <svg class="placeholder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2">
                <path d="M20.2 6H3.8C2.8 6 2 6.8 2 7.8V16.2C2 17.2 2.8 18 3.8 18H20.2C21.2 18 22 17.2 22 16.2V7.8C22 6.8 21.2 6 20.2 6Z" />
                <path d="M2 11H22" />
                <path d="M7 6L10 11" />
                <path d="M12 6L15 11" />
                <path d="M17 6L20 11" />
              </svg>
              <p>点击添加视频或拖拽视频文件到此处</p>
            </div>
            <VideoPlayer 
              v-else 
              :url="currentUrl" 
              :format="currentFormat" 
              @error="handlePlayerError"
            />
          </div>
        </main>
      </div>
    </div>

    <!-- Auth Modal -->
    <div v-if="showAuthModal" class="modal-overlay" @click="showAuthModal = false">
      <div class="modal-card glass auth-modal" @click.stop>
        <div class="modal-header">
          <h3>{{ isLoginMode ? '登录' : '注册' }}</h3>
        </div>
        <div class="auth-form">
          <div class="form-group">
            <label>用户名</label>
            <input type="text" v-model="authForm.username" placeholder="请输入用户名">
          </div>
          <div class="form-group" v-if="!isLoginMode">
            <label>邮箱</label>
            <input type="email" v-model="authForm.email" placeholder="请输入邮箱">
          </div>
          <div class="form-group">
            <label>密码</label>
            <input type="password" v-model="authForm.password" placeholder="请输入密码">
          </div>
          <div class="auth-actions">
            <button class="modal-btn primary" @click="handleAuth">{{ isLoginMode ? '登录' : '注册' }}</button>
            <button class="mode-switch" @click="isLoginMode = !isLoginMode">
              {{ isLoginMode ? '没有账号？点击注册' : '已有账号？点击登录' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for errors -->
    <div v-if="showError" class="modal-overlay" @click="showError = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <h3>{{ errorTitle }}</h3>
        </div>
        <p>{{ errorMessage }}</p>
        <button class="modal-btn" @click="showError = false">确定</button>
      </div>
    </div>

    <!-- Modal for success messages -->
    <div v-if="showSuccess" class="modal-overlay" @click="showSuccess = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <svg class="success-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M9 12l2 2 4-4"/>
          </svg>
          <h3>{{ successTitle }}</h3>
        </div>
        <p>{{ successMessage }}</p>
        <button class="modal-btn" @click="showSuccess = false">确定</button>
      </div>
    </div>

    <!-- Add Video Modal -->
    <div v-if="showAddVideoModal" class="modal-overlay" @click="showAddVideoModal = false">
      <div class="modal-card glass add-video-modal" @click.stop>
        <div class="modal-header">
          <svg class="video-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
            <line x1="7" y1="2" x2="7" y2="22"/>
            <line x1="17" y1="2" x2="17" y2="22"/>
            <line x1="2" y1="12" x2="22" y2="12"/>
            <line x1="2" y1="7" x2="7" y2="7"/>
            <line x1="2" y1="17" x2="7" y2="17"/>
            <line x1="17" y1="17" x2="22" y2="17"/>
            <line x1="17" y1="7" x2="22" y2="7"/>
          </svg>
          <h3>添加视频</h3>
        </div>
        
        <!-- Tab Switch -->
        <div class="video-type-tabs">
          <button 
            class="tab-btn" 
            :class="{ active: videoType === 'online' }"
            @click="videoType = 'online'"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
              <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
            </svg>
            在线视频
          </button>
          <button 
            class="tab-btn" 
            :class="{ active: videoType === 'local' }"
            @click="videoType = 'local'"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
            </svg>
            本地视频
          </button>
        </div>

        <div class="add-video-form">
          <!-- Online Video Form -->
          <template v-if="videoType === 'online'">
            <div class="form-group">
              <label>视频地址</label>
              <input 
                type="text" 
                v-model="newVideoUrl" 
                placeholder="输入在线视频地址 (MP4, M3U8, RTMP...)"
                @keyup.enter="addVideoAndPlay"
              >
            </div>
            <div class="form-group">
              <label>视频名称（可选）</label>
              <input 
                type="text" 
                v-model="newVideoName" 
                placeholder="输入视频名称"
                @keyup.enter="addVideoAndPlay"
              >
            </div>
          </template>

          <!-- Local Video Form -->
          <template v-else>
            <div class="local-video-upload">
              <input 
                type="file" 
                ref="fileInput" 
                @change="handleModalFileSelect" 
                accept="video/*" 
                hidden
              >
              <div class="upload-area" @click="fileInput.click()">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                <p>点击选择本地视频文件</p>
                <span class="upload-hint">支持 MP4, WebM 等格式</span>
              </div>
              <div v-if="selectedLocalFile" class="selected-file">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10 9 9 9 8 9"/>
                </svg>
                <span class="file-name">{{ selectedLocalFile.name }}</span>
                <button class="clear-file" @click="selectedLocalFile = null">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
              <div class="upload-option" v-if="currentUser">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="uploadToServer" class="upload-checkbox">
                  <span class="checkbox-custom"></span>
                  上传到视频服务
                </label>
              </div>
            </div>
          </template>

          <div class="add-video-actions">
            <button class="modal-btn secondary" @click="closeAddVideoModal">取消</button>
            <button class="modal-btn primary" @click="addVideoAndPlay">确定</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import VideoPlayer from '@/components/VideoPlayer.vue'

const router = useRouter()
const API_BASE = 'http://localhost:8000'

const currentUrl = ref('')
const currentFormat = ref('mp4')
const inputUrl = ref('https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8')
const dragOver = ref(false)
const showError = ref(false)
const errorTitle = ref('播放失败')
const errorMessage = ref('')
const showSuccess = ref(false)
const successTitle = ref('操作成功')
const successMessage = ref('')
const onlineHistory = ref([])
const localHistory = ref([])
const sessionId = Math.random().toString(36).substring(7)
const pendingReuploadIndex = ref(-1)
const fileInput = ref(null)

// 折叠状态
const isOnlineHistoryOpen = ref(true)
const isLocalHistoryOpen = ref(true)

const showAuthModal = ref(false)
const isLoginMode = ref(true)
const authForm = ref({
  username: '',
  email: '',
  password: ''
})
const currentUser = ref(null)
const accessToken = ref(null)

// Add video modal
const showAddVideoModal = ref(false)
const videoType = ref('online') // 'online' or 'local'
const DEFAULT_VIDEO_URL = 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8'
const newVideoUrl = ref(DEFAULT_VIDEO_URL)
const newVideoName = ref('')
const selectedLocalFile = ref(null)
const uploadToServer = ref(false)

const isLoggedIn = computed(() => !!currentUser.value)

onMounted(() => {
  const token = localStorage.getItem('access_token')
  const user = localStorage.getItem('current_user')
  if (token && user) {
    accessToken.value = token
    currentUser.value = JSON.parse(user)
    loadHistoryFromBackend()
  }
})

const apiRequest = async (endpoint, options = {}) => {
  const headers = {
    ...options.headers
  }
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json'
  }
  if (accessToken.value) {
    headers['Authorization'] = `Bearer ${accessToken.value}`
  }
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  })
  return response
}

const handleAuth = async () => {
  try {
    let response
    if (isLoginMode.value) {
      const formData = new FormData()
      formData.append('username', authForm.value.username)
      formData.append('password', authForm.value.password)
      response = await apiRequest('/token', {
        method: 'POST',
        headers: {},
        body: formData
      })
    } else {
      response = await apiRequest('/register', {
        method: 'POST',
        body: JSON.stringify({
          username: authForm.value.username,
          email: authForm.value.email,
          password: authForm.value.password
        })
      })
    }
    
    if (response.ok) {
      const data = await response.json()
      if (isLoginMode.value) {
        accessToken.value = data.access_token
        currentUser.value = data.user
        localStorage.setItem('access_token', data.access_token)
        localStorage.setItem('current_user', JSON.stringify(data.user))
        showAuthModal.value = false
        authForm.value = { username: '', email: '', password: '' }
        await syncLocalHistoryToBackend()
        await loadHistoryFromBackend()
      } else {
        isLoginMode.value = true
        authForm.value = { username: '', email: '', password: '' }
        successTitle.value = '注册成功'
        successMessage.value = '注册成功，请登录'
        showSuccess.value = true
      }
    } else {
      const error = await response.json()
      errorTitle.value = isLoginMode.value ? '登录失败' : '注册失败'
      errorMessage.value = error.detail || '操作失败'
      showError.value = true
    }
  } catch (err) {
    errorTitle.value = isLoginMode.value ? '登录失败' : '注册失败'
    errorMessage.value = '网络错误'
    showError.value = true
  }
}

// 同步本地播放记录到后端
const syncLocalHistoryToBackend = async () => {
  // 同步在线视频历史
  const localOnlineHistory = onlineHistory.value.filter(item => item.id && String(item.id).startsWith('local_'))
  for (const item of localOnlineHistory) {
    try {
      await apiRequest('/history', {
        method: 'POST',
        body: JSON.stringify({
          video_url: item.video_url,
          video_name: item.video_name,
          video_format: item.video_format
        })
      })
    } catch (err) {
      console.error('Failed to sync online history to backend:', err)
    }
  }
}

const logout = () => {
  currentUser.value = null
  accessToken.value = null
  localStorage.removeItem('access_token')
  localStorage.removeItem('current_user')
  onlineHistory.value = []
  localHistory.value = []
}

const goToProfile = () => {
  router.push('/profile')
}

const getAvatarUrl = (avatar) => {
  if (!avatar) return null
  if (avatar.startsWith('http')) return avatar
  return `${API_BASE}${avatar}`
}

const loadOnlineHistoryFromBackend = async () => {
  if (!isLoggedIn.value) return
  try {
    const response = await apiRequest('/history')
    if (response.ok) {
      onlineHistory.value = await response.json()
    }
  } catch (err) {
    console.error('Failed to load online history:', err)
  }
}

const loadLocalHistoryFromBackend = async () => {
  if (!isLoggedIn.value) return
  try {
    const response = await apiRequest('/local-history')
    if (response.ok) {
      const backendLocalHistory = await response.json()
      // 合并后端本地历史与当前本地历史
      const currentLocalUrls = new Set(localHistory.value.map(item => item.url))
      backendLocalHistory.forEach(item => {
        if (!currentLocalUrls.has(item.url)) {
          localHistory.value.push({
            id: item.id,
            name: item.video_name,
            video_name: item.video_name,
            url: '', // 本地视频需要重新上传
            timestamp: new Date(item.created_at).getTime(),
            isLocal: true,
            sid: null, // 需要重新上传
            fileInfo: JSON.parse(item.file_info || '{}')
          })
        }
      })
      // 限制数量
      if (localHistory.value.length > 10) {
        localHistory.value = localHistory.value.slice(0, 10)
      }
    }
  } catch (err) {
    console.error('Failed to load local history:', err)
  }
}

const loadHistoryFromBackend = async () => {
  await loadOnlineHistoryFromBackend()
  await loadLocalHistoryFromBackend()
}

// 折叠/展开切换
const toggleOnlineHistory = () => {
  isOnlineHistoryOpen.value = !isOnlineHistoryOpen.value
}

const toggleLocalHistory = () => {
  isLocalHistoryOpen.value = !isLocalHistoryOpen.value
}

const addToHistory = async (url, name = '', fileInfo = null) => {
  const isLocal = url.startsWith('blob:')
  const displayName = name || url.split('/').pop().split('?')[0]
  const format = getFormat(url)

  if (isLocal) {
    // 本地视频历史
    const newItem = {
      url,
      name: displayName,
      video_name: displayName,
      timestamp: Date.now(),
      isLocal: true,
      sid: sessionId,
      fileInfo: fileInfo ? {
        name: fileInfo.name,
        size: fileInfo.size,
        type: fileInfo.type,
        lastModified: fileInfo.lastModified
      } : null
    }

    // 去重：移除同名本地视频
    localHistory.value = localHistory.value.filter(item => item.name !== displayName)
    localHistory.value.unshift(newItem)
    if (localHistory.value.length > 10) {
      localHistory.value = localHistory.value.slice(0, 10)
    }

    // 如果已登录，同步到后端
    if (isLoggedIn.value) {
      try {
        await apiRequest('/local-history', {
          method: 'POST',
          body: JSON.stringify({
            video_name: displayName,
            video_format: format,
            file_info: JSON.stringify(newItem.fileInfo)
          })
        })
      } catch (err) {
        console.error('Failed to save local history to backend:', err)
      }
    }
  } else {
    // 在线视频历史
    if (isLoggedIn.value) {
      try {
        const response = await apiRequest('/history', {
          method: 'POST',
          body: JSON.stringify({
            video_url: url,
            video_name: displayName,
            video_format: format
          })
        })
        if (response.ok) {
          await loadOnlineHistoryFromBackend()
        }
        
        // 记录播放日志
        await apiRequest('/play-logs', {
          method: 'POST',
          body: JSON.stringify({
            video_name: displayName,
            video_url: url,
            video_format: format
          })
        })
      } catch (err) {
        console.error('Failed to save online history:', err)
      }
    } else {
      // 未登录时，添加到本地在线视频历史
      const newItem = {
        id: 'local_' + Date.now(),
        video_url: url,
        video_name: displayName,
        video_format: format,
        created_at: new Date().toISOString()
      }

      // 去重：移除相同URL的在线视频
      onlineHistory.value = onlineHistory.value.filter(item => item.video_url !== url)
      onlineHistory.value.unshift(newItem)
      if (onlineHistory.value.length > 10) {
        onlineHistory.value = onlineHistory.value.slice(0, 10)
      }
    }
  }
}

// 在线视频历史操作
const clearOnlineHistory = async () => {
  if (isLoggedIn.value) {
    try {
      await apiRequest('/history', { method: 'DELETE' })
      onlineHistory.value = []
    } catch (err) {
      console.error('Failed to clear online history:', err)
    }
  } else {
    onlineHistory.value = []
  }
}

const removeOnlineHistoryItem = async (item) => {
  if (isLoggedIn.value && item.id) {
    try {
      await apiRequest(`/history/${item.id}`, { method: 'DELETE' })
      await loadOnlineHistoryFromBackend()
    } catch (err) {
      console.error('Failed to delete online history:', err)
    }
  } else {
    const index = onlineHistory.value.findIndex(h => h.video_url === item.video_url)
    if (index > -1) {
      onlineHistory.value.splice(index, 1)
    }
  }
}

const playOnlineHistoryItem = (item) => {
  inputUrl.value = item.video_url
  loadUrlVideo()
}

// 本地视频历史操作
const clearLocalHistory = async () => {
  if (isLoggedIn.value) {
    try {
      await apiRequest('/local-history', { method: 'DELETE' })
      localHistory.value = []
    } catch (err) {
      console.error('Failed to clear local history:', err)
    }
  } else {
    localHistory.value = []
  }
}

const removeLocalHistoryItem = async (item, index) => {
  if (isLoggedIn.value && item.id) {
    try {
      await apiRequest(`/local-history/${item.id}`, { method: 'DELETE' })
      // 从本地数组中移除
      localHistory.value.splice(index, 1)
    } catch (err) {
      console.error('Failed to delete local history:', err)
    }
  } else {
    localHistory.value.splice(index, 1)
  }
}

const playLocalHistoryItem = (item, index) => {
  if (item.sid !== sessionId) {
    pendingReuploadIndex.value = index
    fileInput.value.click()
    return
  }
  currentUrl.value = item.url
  currentFormat.value = item.name.split('.').pop().toLowerCase()
  addToHistory(item.url, item.name)
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const time = typeof timestamp === 'string' ? new Date(timestamp).getTime() : timestamp
  const now = Date.now()
  const diff = now - time
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return new Date(time).toLocaleDateString()
}

const handleFileSelect = (e) => {
  const file = e.target.files[0]
  if (file) {
    if (pendingReuploadIndex.value !== -1) {
      // 从历史记录重新上传，传入对应的历史记录项进行验证
      const historyItem = localHistory.value[pendingReuploadIndex.value]
      playFile(file, historyItem)
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

const playFile = (file, historyItem = null) => {
  // 如果提供了历史记录项，验证文件是否匹配
  if (historyItem && historyItem.fileInfo) {
    const info = historyItem.fileInfo
    const isMatch = file.name === info.name &&
                    file.size === info.size &&
                    file.lastModified === info.lastModified

    if (!isMatch) {
      showError.value = true
      errorMessage.value = '文件不匹配！请选择正确的视频文件。'
      return
    }
  }

  const url = URL.createObjectURL(file)
  currentUrl.value = url
  currentFormat.value = file.name.split('.').pop().toLowerCase()

  // 如果是从历史记录重新上传，更新原记录的 URL
  if (historyItem) {
    historyItem.url = url
    historyItem.sid = sessionId
    addToHistory(url, file.name, file)
  } else {
    addToHistory(url, file.name, file)
  }
}

const loadUrlVideo = () => {
  if (!inputUrl.value) return
  currentUrl.value = inputUrl.value
  currentFormat.value = getFormat(inputUrl.value)
  addToHistory(inputUrl.value)
}

const resetUrl = () => {
  inputUrl.value = 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8'
}

const getFormat = (url) => {
  if (url.startsWith('rtmp://')) {
    return 'rtmp'
  }
  const cleanUrl = url.split('?')[0].split('#')[0]
  const ext = cleanUrl.split('.').pop().toLowerCase()
  return ['mp4', 'webm', 'm3u8', 'flv'].includes(ext) ? ext : 'mp4'
}

const handlePlayerError = (err) => {
  if (currentUrl.value.startsWith('blob:')) {
    errorMessage.value = '本地视频加载失败。可能是链接已过期或文件已被移动，请重新上传。'
  } else {
    errorMessage.value = `无法播放该视频，请检查地址是否正确。(${err.message || '未知错误'})`
  }
  showError.value = true
}

const addVideoAndPlay = async () => {
  if (videoType.value === 'online') {
    // 在线视频
    if (!newVideoUrl.value.trim()) {
      errorMessage.value = '请输入视频地址'
      showError.value = true
      return
    }

    // 设置当前URL并播放
    currentUrl.value = newVideoUrl.value.trim()
    currentFormat.value = getFormat(currentUrl.value)

    // 添加到历史记录
    addToHistory(currentUrl.value, newVideoName.value.trim() || '')
  } else {
    // 本地视频
    if (!selectedLocalFile.value) {
      errorMessage.value = '请选择本地视频文件'
      showError.value = true
      return
    }

    if (uploadToServer.value && isLoggedIn.value) {
      try {
        const formData = new FormData()
        formData.append('file', selectedLocalFile.value)
        const response = await apiRequest('/upload', {
          method: 'POST',
          body: formData
        })
        if (response.ok) {
          const data = await response.json()
          const serverUrl = `${API_BASE}${data.url}`
          currentUrl.value = serverUrl
          currentFormat.value = data.format
          addToHistory(serverUrl, selectedLocalFile.value.name)
        } else {
          const error = await response.json()
          showError.value = true
          errorMessage.value = error.detail || '上传失败'
          return
        }
      } catch (err) {
        showError.value = true
        errorMessage.value = '上传失败'
        return
      }
    } else {
      // 播放本地文件，传入文件信息用于后续验证
      const url = URL.createObjectURL(selectedLocalFile.value)
      currentUrl.value = url
      currentFormat.value = selectedLocalFile.value.name.split('.').pop().toLowerCase()
      addToHistory(url, selectedLocalFile.value.name, selectedLocalFile.value)
    }
  }

  // 关闭弹窗并清空输入
  closeAddVideoModal()
}

const closeAddVideoModal = () => {
  showAddVideoModal.value = false
  newVideoUrl.value = DEFAULT_VIDEO_URL
  newVideoName.value = ''
  selectedLocalFile.value = null
  uploadToServer.value = false
  videoType.value = 'online'
}

const handleModalFileSelect = (e) => {
  const file = e.target.files[0]
  if (file) {
    selectedLocalFile.value = file
  }
}
</script>

<style lang="scss" scoped>
.main-container {
  min-height: 100vh;
  background: radial-gradient(ellipse at 20% 0%, #1a1a3e 0%, #0a0f1a 40%, #050810 100%);
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
  background: rgba(15, 23, 42, 0.7);
  border-right: 1px solid rgba(99, 102, 241, 0.12);
  transition: all 0.3s ease;
  flex-shrink: 0;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);

  .sidebar-header {
    padding: 20px 20px 16px;
    border-bottom: 1px solid rgba(99, 102, 241, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;

    .logo-mini {
      display: flex;
      align-items: center;
      gap: 10px;
      
      .logo-icon {
        width: 28px;
        height: 28px;
        color: #6366f1;
        filter: drop-shadow(0 0 8px rgba(99, 102, 241, 0.4));
      }

      span {
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #f8fafc 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }
    }

    .user-area {
      display: flex;
      align-items: center;
      gap: 8px;

      .user-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
        overflow: hidden;

        &:hover {
          transform: scale(1.1);
          box-shadow: 0 4px 15px rgba(99, 102, 241, 0.5);
        }

        .avatar-image {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .avatar-text {
          color: white;
          font-size: 0.9rem;
          font-weight: 600;
        }
      }

      .username {
        font-size: 0.9rem;
        color: #a5b4fc;
        cursor: pointer;
        transition: color 0.2s;

        &:hover {
          color: #f8fafc;
        }
      }

      .logout-btn {
        width: 28px;
        height: 28px;
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
          color: #ef4444;
          background: rgba(239, 68, 68, 0.1);
        }

        svg {
          width: 16px;
          height: 16px;
        }
      }
    }

    .login-btn {
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(99, 102, 241, 0.1);
      border: 1px solid rgba(99, 102, 241, 0.2);
      border-radius: 8px;
      color: #a5b4fc;
      cursor: pointer;
      transition: all 0.2s;

      &:hover {
        background: rgba(99, 102, 241, 0.2);
        border-color: #6366f1;
        color: #f8fafc;
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
    padding: 8px 0;

    &::-webkit-scrollbar {
      width: 4px;
    }
    &::-webkit-scrollbar-track {
      background: transparent;
    }
    &::-webkit-scrollbar-thumb {
      background: rgba(99, 102, 241, 0.2);
      border-radius: 2px;
    }

    .history-section {
      margin-bottom: 8px;
    }

    .section-header {
      padding: 12px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      transition: all 0.2s;
      border-radius: 0 8px 8px 0;
      margin: 0 8px;

      &:hover {
        background: rgba(99, 102, 241, 0.08);
      }

      .section-title-wrapper {
        display: flex;
        align-items: center;
        gap: 8px;

        .section-icon {
          width: 16px;
          height: 16px;
          color: #64748b;
          transition: transform 0.2s;

          &.collapsed {
            transform: rotate(-90deg);
          }
        }

        .section-title-text {
          font-size: 0.8rem;
          font-weight: 600;
          color: #94a3b8;
        }

        .section-count {
          font-size: 0.7rem;
          color: #64748b;
        }
      }

      .clear-history {
        background: transparent;
        border: none;
        color: #6366f1;
        font-size: 0.7rem;
        cursor: pointer;
        opacity: 0.7;
        transition: all 0.2s;
        &:hover { 
          opacity: 1; 
          color: #818cf8;
        }
      }
    }

    .history-list-wrapper {
      padding: 4px 0;
    }

    .empty-history {
      padding: 20px;
      text-align: center;
      color: #475569;
      font-size: 0.8rem;
    }

    .history-sidebar-list {
      display: flex;
      flex-direction: column;
    }

    .history-sidebar-item {
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      transition: all 0.25s ease;
      border-left: 3px solid transparent;
      margin: 0 8px;
      border-radius: 0 10px 10px 0;

      &:hover {
        background: rgba(99, 102, 241, 0.08);
        .play-indicator { opacity: 1; }
      }

      &.is-active {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.15) 0%, rgba(99, 102, 241, 0.05) 100%);
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
    }
  }

  .add-video-section {
    padding: 16px 20px;
    border-bottom: 1px solid rgba(99, 102, 241, 0.1);

    .add-video-btn {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 12px 16px;
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
      border: 1px solid rgba(99, 102, 241, 0.3);
      border-radius: 12px;
      color: #c7d2fe;
      font-size: 0.9rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.25) 100%);
        border-color: rgba(99, 102, 241, 0.5);
        color: #f8fafc;
        transform: translateY(-1px);
        box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.3);
      }

      &:active {
        transform: translateY(0);
      }

      svg {
        width: 20px;
        height: 20px;
      }
    }
  }
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 24px;
  overflow: hidden;
}

.top-controls-wrapper {
  width: 100%;
  max-width: 900px;
  margin-bottom: 20px;
}

.top-controls {
  display: flex;
  gap: 12px;
  align-items: center;
  width: 100%;

  .url-area {
    flex: 1;
  }

  .upload-area-mini {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0 18px;
    height: 48px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    color: #c7d2fe;
    white-space: nowrap;
    box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.2);

    &:hover {
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.2) 100%);
      border-color: rgba(99, 102, 241, 0.5);
      color: #f8fafc;
      transform: translateY(-2px);
      box-shadow: 0 8px 25px -5px rgba(99, 102, 241, 0.35);
    }

    .control-icon {
      width: 18px;
      height: 18px;
    }

    span {
      font-size: 0.85rem;
      font-weight: 500;
    }
  }
}

.player-section {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;

  .player-card {
    position: relative;
    width: 100%;
    height: 100%;
    background: linear-gradient(145deg, #0a0f1a 0%, #151b2e 100%);
    border-radius: 20px;
    border: 1px solid rgba(99, 102, 241, 0.12);
    box-shadow: 
      0 25px 50px -12px rgba(0, 0, 0, 0.8),
      0 0 0 1px rgba(255, 255, 255, 0.02) inset,
      0 0 100px rgba(99, 102, 241, 0.05) inset;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);

    &.drag-active {
      border-color: rgba(99, 102, 241, 0.6);
      transform: scale(1.008);
      box-shadow: 
        0 0 80px rgba(99, 102, 241, 0.2),
        0 25px 50px -12px rgba(0, 0, 0, 0.8),
        0 0 0 1px rgba(255, 255, 255, 0.05) inset;
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
    color: #475569;
    transition: all 0.4s ease;
    background: radial-gradient(circle at center, rgba(99, 102, 241, 0.08) 0%, transparent 70%);

    &:hover {
      color: #94a3b8;
      background: radial-gradient(circle at center, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
    }

    .placeholder-icon {
      width: 80px;
      height: 80px;
      margin-bottom: 24px;
      opacity: 0.4;
      transition: all 0.4s ease;
      color: #6366f1;
    }

    &:hover .placeholder-icon {
      opacity: 0.7;
      transform: scale(1.1);
      filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.4));
    }

    p {
      font-size: 1.1rem;
      letter-spacing: 0.5px;
      color: #64748b;
      font-weight: 500;
    }
  }
}

.url-area {
  .input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 12px;
    padding: 4px 4px 4px 16px;
    height: 48px;
    transition: all 0.3s ease;

    &:focus-within {
      border-color: rgba(99, 102, 241, 0.5);
      background: rgba(15, 23, 42, 0.9);
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1), 0 4px 20px -4px rgba(99, 102, 241, 0.2);
    }

    .input-icon {
      width: 18px;
      height: 18px;
      color: #6366f1;
      margin-right: 12px;
      opacity: 0.7;
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
        transition: color 0.2s;
      }

      &:focus::placeholder {
        color: #64748b;
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
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;

  svg {
    width: 18px;
    height: 18px;
  }

  &.play-btn {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    color: white;
    box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);

    &:hover {
      background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
      transform: scale(1.08);
      box-shadow: 0 6px 20px -4px rgba(99, 102, 241, 0.5);
    }

    &:active {
      transform: scale(0.98);
    }
  }

  &.clear-btn {
    background: transparent;
    color: #64748b;

    &:hover {
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.05);
    }
  }

  &.reset-btn {
    background: rgba(51, 65, 85, 0.6);
    color: #94a3b8;

    &:hover {
      background: rgba(71, 85, 105, 0.8);
      color: #f8fafc;
    }
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
  max-width: 380px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  padding: 28px;
  border-radius: 20px;
  border: 1px solid rgba(99, 102, 241, 0.2);
  text-align: center;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.05) inset;

  .modal-header {
    margin-bottom: 20px;
    
    .error-icon {
      width: 48px;
      height: 48px;
      color: #ef4444;
      margin: 0 auto 15px;
      filter: drop-shadow(0 0 10px rgba(239, 68, 68, 0.3));
    }

    .success-icon {
      width: 48px;
      height: 48px;
      color: #10b981;
      margin: 0 auto 15px;
      filter: drop-shadow(0 0 10px rgba(16, 185, 129, 0.3));
    }

    h3 {
      font-size: 1.25rem;
      margin: 0;
      font-weight: 600;
    }
  }

  p {
    color: #94a3b8;
    margin-bottom: 24px;
    line-height: 1.6;
    font-size: 0.95rem;
  }

  .modal-btn {
      width: 100%;
      padding: 12px;
      background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
      color: white;
      border: none;
      border-radius: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);

      &:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 20px -4px rgba(99, 102, 241, 0.5);
      }

      &:active {
        transform: translateY(0);
      }
    }

    &.auth-modal {
      max-width: 360px;
    }
  }

.auth-form {
  .form-group {
    margin-bottom: 16px;
    text-align: left;

    label {
      display: block;
      margin-bottom: 6px;
      font-size: 0.9rem;
      color: #94a3b8;
    }

    input {
      width: 100%;
      padding: 10px 12px;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      color: #f8fafc;
      font-size: 0.9rem;
      outline: none;
      transition: all 0.2s;

      &:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
      }
    }
  }

  .auth-actions {
    margin-top: 24px;
  }

  .mode-switch {
    width: 100%;
    background: transparent;
    border: none;
    color: #6366f1;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
    opacity: 0.8;

    &:hover {
      opacity: 1;
    }
  }
}

.add-video-modal {
  max-width: 420px;

  .video-icon {
    width: 48px;
    height: 48px;
    color: #6366f1;
    margin: 0 auto 15px;
    filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.3));
  }

  .video-type-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
    padding: 0 4px;

    .tab-btn {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 12px 16px;
      background: rgba(15, 23, 42, 0.5);
      border: 1px solid rgba(99, 102, 241, 0.15);
      border-radius: 10px;
      color: #94a3b8;
      font-size: 0.9rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.25s ease;

      svg {
        width: 18px;
        height: 18px;
      }

      &:hover {
        background: rgba(99, 102, 241, 0.1);
        border-color: rgba(99, 102, 241, 0.3);
        color: #c7d2fe;
      }

      &.active {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
        border-color: rgba(99, 102, 241, 0.4);
        color: #f8fafc;
      }
    }
  }

  .add-video-form {
    .form-group {
      margin-bottom: 16px;
      text-align: left;

      label {
        display: block;
        margin-bottom: 6px;
        font-size: 0.9rem;
        color: #94a3b8;
      }

      input {
        width: 100%;
        padding: 12px 14px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 10px;
        color: #f8fafc;
        font-size: 0.95rem;
        outline: none;
        transition: all 0.25s ease;

        &::placeholder {
          color: #475569;
        }

        &:focus {
          border-color: rgba(99, 102, 241, 0.5);
          background: rgba(15, 23, 42, 0.8);
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
      }
    }

    .local-video-upload {
      .upload-area {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 12px;
        padding: 32px 24px;
        background: rgba(15, 23, 42, 0.4);
        border: 2px dashed rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;

        &:hover {
          background: rgba(99, 102, 241, 0.1);
          border-color: rgba(99, 102, 241, 0.5);
        }

        svg {
          width: 40px;
          height: 40px;
          color: #6366f1;
        }

        p {
          color: #c7d2fe;
          font-size: 0.95rem;
          font-weight: 500;
          margin: 0;
        }

        .upload-hint {
          color: #64748b;
          font-size: 0.8rem;
        }
      }

      .selected-file {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 16px;
        padding: 12px 16px;
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 10px;

        svg {
          width: 20px;
          height: 20px;
          color: #6366f1;
          flex-shrink: 0;
        }

        .file-name {
          flex: 1;
          color: #e2e8f0;
          font-size: 0.9rem;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .clear-file {
          width: 24px;
          height: 24px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: transparent;
          border: none;
          color: #64748b;
          cursor: pointer;
          border-radius: 4px;
          transition: all 0.2s;

          &:hover {
            color: #ef4444;
            background: rgba(239, 68, 68, 0.1);
          }

          svg {
            width: 16px;
            height: 16px;
          }
        }
      }

      .upload-option {
        margin-top: 16px;
        padding: 12px 16px;
        background: rgba(99, 102, 241, 0.05);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 10px;

        .checkbox-label {
          display: flex;
          align-items: center;
          gap: 10px;
          cursor: pointer;
          color: #e2e8f0;
          font-size: 0.9rem;
          user-select: none;

          .upload-checkbox {
            display: none;
          }

          .checkbox-custom {
            width: 18px;
            height: 18px;
            border: 2px solid rgba(99, 102, 241, 0.4);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            background: rgba(15, 23, 42, 0.6);
            position: relative;

            &::after {
              content: '';
              width: 10px;
              height: 5px;
              border-left: 2px solid #f8fafc;
              border-bottom: 2px solid #f8fafc;
              transform: rotate(-45deg);
              opacity: 0;
              transition: opacity 0.2s ease;
              margin-bottom: 2px;
            }
          }

          .upload-checkbox:checked + .checkbox-custom {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            border-color: #6366f1;
            box-shadow: 0 0 8px rgba(99, 102, 241, 0.4);

            &::after {
              opacity: 1;
            }
          }

          &:hover .checkbox-custom {
            border-color: rgba(99, 102, 241, 0.6);
          }
        }
      }
    }

    .add-video-actions {
      display: flex;
      gap: 12px;
      margin-top: 24px;

      .modal-btn {
        flex: 1;
        min-height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;

        &.secondary {
          background: rgba(51, 65, 85, 0.6);
          box-shadow: none;

          &:hover {
            background: rgba(71, 85, 105, 0.8);
            transform: translateY(-1px);
          }
        }
      }
    }
  }
}
</style>
