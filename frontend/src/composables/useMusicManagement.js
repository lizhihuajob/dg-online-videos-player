import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export function useMusicManagement() {
  const authStore = useAuthStore()

  const musicList = ref([])
  const musicGroups = ref([])
  const isLoading = ref(false)
  const selectedGroupId = ref(null)
  const searchQuery = ref('')
  const viewMode = ref('card')

  const toastMessage = ref('')
  const toastType = ref('success')

  const showUploadModal = ref(false)
  const showEditModal = ref(false)
  const showChangeGroupModal = ref(false)
  const showDeleteModal = ref(false)
  const showPlayerModal = ref(false)

  const isUploading = ref(false)

  const musicToEdit = ref(null)
  const isEditing = ref(false)

  const musicToChangeGroup = ref(null)
  const isChangingGroup = ref(false)

  const musicToDelete = ref(null)
  const isDeleting = ref(false)

  const currentMusic = ref(null)

  const filteredMusic = computed(() => {
    if (!searchQuery.value.trim()) return musicList.value
    const query = searchQuery.value.toLowerCase()
    return musicList.value.filter(m => m.original_name.toLowerCase().includes(query))
  })

  onMounted(() => {
    loadMusic()
    loadGroups()
  })

  async function loadMusic() {
    isLoading.value = true
    try {
      const params = new URLSearchParams()
      params.append('file_type', 'music')
      if (selectedGroupId.value) {
        params.append('group_id', selectedGroupId.value)
      }
      const response = await authStore.apiRequest(`/videos?${params.toString()}`)
      if (response.ok) {
        musicList.value = await response.json()
      } else {
        showToast('加载音乐失败', 'error')
      }
    } catch (err) {
      showToast('网络错误', 'error')
    } finally {
      isLoading.value = false
    }
  }

  async function loadGroups() {
    try {
      const response = await authStore.apiRequest('/groups?group_type=music')
      if (response.ok) {
        musicGroups.value = await response.json()
      }
    } catch (err) {
      console.error('加载分组失败', err)
    }
  }

  function getGroupName(groupId) {
    const group = musicGroups.value.find(g => g.id === groupId)
    return group ? group.name : ''
  }

  function getMusicUrl(music) {
    return `${API_BASE}${music.url}`
  }

  function editMusic(music) {
    musicToEdit.value = music
    showEditModal.value = true
  }

  async function saveEdit(newName) {
    if (!newName || !musicToEdit.value) return

    isEditing.value = true
    try {
      const response = await authStore.apiRequest(`/videos/${musicToEdit.value.id}`, {
        method: 'PUT',
        body: JSON.stringify({ name: newName })
      })

      if (response.ok) {
        const updatedMusic = await response.json()
        const index = musicList.value.findIndex(m => m.id === updatedMusic.id)
        if (index !== -1) {
          musicList.value[index] = updatedMusic
        }
        closeEditModal()
        showToast('修改成功', 'success')
      } else {
        const error = await response.json()
        showToast(error.detail || '修改失败', 'error')
      }
    } catch (err) {
      showToast('网络错误', 'error')
    } finally {
      isEditing.value = false
    }
  }

  function closeEditModal() {
    showEditModal.value = false
    musicToEdit.value = null
  }

  function showChangeGroup(music) {
    musicToChangeGroup.value = music
    showChangeGroupModal.value = true
  }

  async function saveChangeGroup(groupId) {
    if (!musicToChangeGroup.value) return

    isChangingGroup.value = true
    try {
      const response = await authStore.apiRequest(`/videos/${musicToChangeGroup.value.id}`, {
        method: 'PUT',
        body: JSON.stringify({ group_id: groupId })
      })

      if (response.ok) {
        const updatedMusic = await response.json()
        const index = musicList.value.findIndex(m => m.id === updatedMusic.id)
        if (index !== -1) {
          musicList.value[index] = updatedMusic
        }
        closeChangeGroupModal()
        showToast('分组切换成功', 'success')
      } else {
        const error = await response.json()
        showToast(error.detail || '切换分组失败', 'error')
      }
    } catch (err) {
      showToast('网络错误', 'error')
    } finally {
      isChangingGroup.value = false
    }
  }

  function closeChangeGroupModal() {
    showChangeGroupModal.value = false
    musicToChangeGroup.value = null
  }

  function confirmDelete(music) {
    musicToDelete.value = music
    showDeleteModal.value = true
  }

  async function deleteMusic() {
    if (!musicToDelete.value) return

    isDeleting.value = true
    try {
      const response = await authStore.apiRequest(`/videos/${musicToDelete.value.id}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        musicList.value = musicList.value.filter(m => m.id !== musicToDelete.value.id)
        closeDeleteModal()
        showToast('删除成功', 'success')
      } else {
        const error = await response.json()
        showToast(error.detail || '删除失败', 'error')
      }
    } catch (err) {
      showToast('网络错误', 'error')
    } finally {
      isDeleting.value = false
    }
  }

  function closeDeleteModal() {
    showDeleteModal.value = false
    musicToDelete.value = null
  }

  function playMusic(music) {
    currentMusic.value = music
    showPlayerModal.value = true
  }

  function closePlayer() {
    showPlayerModal.value = false
    currentMusic.value = null
  }

  function showToast(message, type = 'success') {
    toastMessage.value = message
    toastType.value = type
    setTimeout(() => {
      toastMessage.value = ''
    }, 3000)
  }

  async function uploadMusic(file, groupId) {
    if (!file) return

    isUploading.value = true

    try {
      const formData = new FormData()
      formData.append('file', file)
      if (groupId) {
        formData.append('group_id', groupId)
      }

      const response = await authStore.apiRequest('/videos', {
        method: 'POST',
        body: formData,
        headers: {}
      })

      if (response.ok) {
        const newMusic = await response.json()
        musicList.value.unshift(newMusic)
        closeUploadModal()
        showToast('上传成功', 'success')
      } else {
        const error = await response.json()
        showToast(error.detail || '上传失败', 'error')
      }
    } catch (err) {
      showToast('网络错误', 'error')
    } finally {
      isUploading.value = false
    }
  }

  function closeUploadModal() {
    showUploadModal.value = false
  }

  return {
    musicList,
    musicGroups,
    isLoading,
    selectedGroupId,
    searchQuery,
    viewMode,
    filteredMusic,
    toastMessage,
    toastType,
    showUploadModal,
    showEditModal,
    showChangeGroupModal,
    showDeleteModal,
    showPlayerModal,
    isUploading,
    musicToEdit,
    isEditing,
    musicToChangeGroup,
    isChangingGroup,
    musicToDelete,
    isDeleting,
    currentMusic,
    loadMusic,
    loadGroups,
    getGroupName,
    getMusicUrl,
    editMusic,
    saveEdit,
    closeEditModal,
    showChangeGroup,
    saveChangeGroup,
    closeChangeGroupModal,
    confirmDelete,
    deleteMusic,
    closeDeleteModal,
    playMusic,
    closePlayer,
    showToast,
    uploadMusic,
    closeUploadModal
  }
}
