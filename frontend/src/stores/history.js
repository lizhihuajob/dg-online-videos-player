import { defineStore } from 'pinia'
import { api } from '@/api'
import { useUserStore } from './user'

export const useHistoryStore = defineStore('history', {
  state: () => ({
    history: [],
    sessionId: Math.random().toString(36).substring(7)
  }),

  actions: {
    async loadHistory() {
      const userStore = useUserStore()
      if (userStore.isLoggedIn) {
        try {
          const data = await api.getPlayHistory(userStore.token)
          this.history = data.map(item => ({
            id: item.id,
            url: item.video_url,
            name: item.video_name || item.video_url.split('/').pop().split('?')[0],
            timestamp: new Date(item.created_at).getTime(),
            isLocal: item.is_local,
            format: item.video_format,
            sid: item.is_local ? this.sessionId : null
          }))
        } catch (error) {
          console.error('加载播放记录失败:', error)
        }
      } else {
        const savedHistory = localStorage.getItem('video-history')
        if (savedHistory) {
          this.history = JSON.parse(savedHistory)
        }
      }
    },

    async addToHistory(url, name = '', format = 'mp4', isLocal = false) {
      const userStore = useUserStore()
      const displayName = name || url.split('/').pop().split('?')[0]
      
      const newItem = {
        url,
        name: displayName,
        timestamp: Date.now(),
        isLocal,
        sid: isLocal ? this.sessionId : null,
        format
      }

      this.history = this.history.filter(item => {
        if (isLocal && item.isLocal) {
          return item.name !== displayName
        }
        return item.url !== url
      })

      this.history.unshift(newItem)
      if (this.history.length > 10) {
        this.history = this.history.slice(0, 10)
      }

      if (userStore.isLoggedIn && !isLocal) {
        try {
          const data = await api.addPlayHistory(userStore.token, {
            video_url: url,
            video_name: displayName,
            video_format: format,
            is_local: isLocal
          })
          const index = this.history.findIndex(item => item.url === url)
          if (index !== -1) {
            this.history[index].id = data.id
          }
        } catch (error) {
          console.error('保存播放记录失败:', error)
        }
      }

      if (!userStore.isLoggedIn || isLocal) {
        localStorage.setItem('video-history', JSON.stringify(this.history))
      }
    },

    async removeHistoryItem(index) {
      const userStore = useUserStore()
      const item = this.history[index]
      
      if (userStore.isLoggedIn && item.id && !item.isLocal) {
        try {
          await api.deletePlayHistory(userStore.token, item.id)
        } catch (error) {
          console.error('删除播放记录失败:', error)
        }
      }
      
      this.history.splice(index, 1)
      
      if (!userStore.isLoggedIn || item.isLocal) {
        localStorage.setItem('video-history', JSON.stringify(this.history))
      }
    },

    async clearHistory() {
      const userStore = useUserStore()
      
      if (userStore.isLoggedIn) {
        try {
          await api.clearPlayHistory(userStore.token)
        } catch (error) {
          console.error('清除播放记录失败:', error)
        }
      }
      
      this.history = []
      localStorage.removeItem('video-history')
    }
  }
})
