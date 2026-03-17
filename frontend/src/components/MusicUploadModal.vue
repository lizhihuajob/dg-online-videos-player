<template>
  <div v-if="show" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <h3>上传音乐</h3>
        <button class="close-btn" @click="close">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <div class="modal-body">
        <div class="form-group">
          <label>选择分组（可选）</label>
          <select v-model="uploadGroupId" class="group-select">
            <option :value="null">不分组</option>
            <option v-for="group in groups" :key="group.id" :value="group.id">
              {{ group.name }}
            </option>
          </select>
        </div>

        <div
          class="upload-area"
          :class="{ 'drag-over': isDragOver }"
          @dragover.prevent="isDragOver = true"
          @dragleave.prevent="isDragOver = false"
          @drop.prevent="handleFileDrop"
          @click="fileInput?.click()"
        >
          <input
            ref="fileInput"
            type="file"
            accept="audio/*"
            hidden
            @change="handleFileSelect"
          >
          <div v-if="!selectedFile" class="upload-placeholder">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9 18V5l12-2v13"/>
              <circle cx="6" cy="18" r="3"/>
              <circle cx="18" cy="16" r="3"/>
            </svg>
            <p>点击或拖拽音乐文件到此处</p>
            <span>支持 MP3, WAV, FLAC 等格式</span>
          </div>
          <div v-else class="selected-file">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>
            <div class="file-info">
              <span class="file-name">{{ selectedFile.name }}</span>
              <span class="file-size">{{ formatSize(selectedFile.size) }}</span>
            </div>
            <button class="clear-file" @click.stop="selectedFile = null">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
        </div>

        <div v-if="uploadError" class="upload-error">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <span>{{ uploadError }}</span>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn secondary" @click="close">取消</button>
        <button
          class="btn primary"
          :disabled="!selectedFile || isUploading"
          @click="upload"
        >
          <span v-if="isUploading" class="btn-spinner"></span>
          <span v-else>开始上传</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  show: Boolean,
  groups: Array
})

const emit = defineEmits(['close', 'upload'])

const fileInput = ref(null)
const selectedFile = ref(null)
const uploadGroupId = ref(null)
const isDragOver = ref(false)
const isUploading = ref(false)
const uploadError = ref('')

function formatSize(bytes) {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function handleFileSelect(e) {
  const file = e.target.files[0]
  if (file) {
    if (!file.type.startsWith('audio/')) {
      uploadError.value = '请选择音乐文件'
      return
    }
    selectedFile.value = file
    uploadError.value = ''
  }
}

function handleFileDrop(e) {
  isDragOver.value = false
  const file = e.dataTransfer.files[0]
  if (file) {
    if (!file.type.startsWith('audio/')) {
      uploadError.value = '请拖拽音乐文件'
      return
    }
    selectedFile.value = file
    uploadError.value = ''
  }
}

async function upload() {
  if (!selectedFile.value) return
  
  isUploading.value = true
  uploadError.value = ''
  
  emit('upload', {
    file: selectedFile.value,
    groupId: uploadGroupId.value,
    onSuccess: () => {
      close()
    },
    onError: (error) => {
      uploadError.value = error
    },
    onFinally: () => {
      isUploading.value = false
    }
  })
}

function close() {
  selectedFile.value = null
  uploadGroupId.value = null
  uploadError.value = ''
  emit('close')
}
</script>

<style lang="scss" scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
  backdrop-filter: blur(4px);
}

.modal-card {
  width: 100%;
  max-width: 480px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);

  h3 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f8fafc;
    margin: 0;
  }

  .close-btn {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 8px;
    color: #64748b;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      color: #f8fafc;
    }

    svg {
      width: 16px;
      height: 16px;
    }
  }
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;

  label {
    display: block;
    margin-bottom: 8px;
    font-size: 0.9rem;
    color: #e2e8f0;
  }

  .group-select {
    width: 100%;
    padding: 12px 16px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 10px;
    color: #f8fafc;
    font-size: 0.95rem;
    outline: none;
    cursor: pointer;

    &:focus {
      border-color: rgba(99, 102, 241, 0.5);
    }

    option {
      background: #1e293b;
      color: #f8fafc;
    }
  }
}

.upload-area {
  border: 2px dashed rgba(99, 102, 241, 0.3);
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.25s ease;

  &:hover, &.drag-over {
    border-color: rgba(99, 102, 241, 0.5);
    background: rgba(99, 102, 241, 0.05);
  }

  .upload-placeholder {
    svg {
      width: 48px;
      height: 48px;
      color: #6366f1;
      margin-bottom: 16px;
    }

    p {
      color: #f8fafc;
      font-size: 0.95rem;
      margin-bottom: 8px;
    }

    span {
      color: #64748b;
      font-size: 0.85rem;
    }
  }

  .selected-file {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    background: rgba(99, 102, 241, 0.1);
    border-radius: 10px;

    svg {
      width: 32px;
      height: 32px;
      color: #6366f1;
      flex-shrink: 0;
    }

    .file-info {
      flex: 1;
      text-align: left;

      .file-name {
        display: block;
        color: #f8fafc;
        font-size: 0.95rem;
        margin-bottom: 4px;
      }

      .file-size {
        color: #64748b;
        font-size: 0.8rem;
      }
    }

    .clear-file {
      width: 28px;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(239, 68, 68, 0.1);
      border: none;
      border-radius: 6px;
      color: #ef4444;
      cursor: pointer;
      transition: all 0.2s ease;

      &:hover {
        background: rgba(239, 68, 68, 0.2);
      }

      svg {
        width: 16px;
        height: 16px;
      }
    }
  }
}

.upload-error {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding: 12px 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  color: #f87171;
  font-size: 0.9rem;

  svg {
    width: 18px;
    height: 18px;
    flex-shrink: 0;
  }
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
}

.btn {
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  &.secondary {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    color: #94a3b8;

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      border-color: rgba(99, 102, 241, 0.3);
      color: #f8fafc;
    }
  }

  &.primary {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border: none;
    color: white;
    box-shadow: 0 4px 15px -3px rgba(16, 185, 129, 0.4);

    &:hover:not(:disabled) {
      transform: translateY(-1px);
      box-shadow: 0 8px 25px -5px rgba(16, 185, 129, 0.5);
    }

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }

  .btn-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
