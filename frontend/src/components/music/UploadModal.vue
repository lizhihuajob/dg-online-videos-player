<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card glass" @click.stop>
      <div class="modal-header">
        <h3>上传音乐</h3>
        <button class="close-btn" @click="$emit('close')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <div class="upload-content">
        <div class="upload-area" @click="fileInput.click()">
          <input
            type="file"
            ref="fileInput"
            @change="handleFileSelect"
            accept="audio/*"
            hidden
          >
          <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          <p class="upload-text">点击选择音乐文件</p>
          <p class="upload-hint">支持 MP3, WAV, FLAC, AAC 等格式</p>
        </div>

        <div v-if="selectedFile" class="file-preview">
          <div class="file-info">
            <svg class="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 18V5l12-2v13"/>
              <circle cx="6" cy="18" r="3"/>
              <circle cx="18" cy="16" r="3"/>
            </svg>
            <div class="file-details">
              <p class="file-name">{{ selectedFile.name }}</p>
              <p class="file-size">{{ formatSize(selectedFile.size) }}</p>
            </div>
          </div>
          <button class="remove-btn" @click="selectedFile = null">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="form-group" v-if="selectedFile">
          <label>选择分组</label>
          <select v-model="selectedGroupId">
            <option :value="null">默认分组</option>
            <option v-for="group in groups" :key="group.id" :value="group.id">
              {{ group.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="modal-footer">
        <button class="modal-btn secondary" @click="$emit('close')">取消</button>
        <button
          class="modal-btn primary"
          :disabled="!selectedFile || isUploading"
          @click="upload"
        >
          <span v-if="isUploading" class="btn-spinner"></span>
          <span v-else>上传</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  groups: {
    type: Array,
    default: () => []
  },
  isUploading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'upload'])

const fileInput = ref(null)
const selectedFile = ref(null)
const selectedGroupId = ref(null)

function handleFileSelect(e) {
  const file = e.target.files[0]
  if (file) {
    selectedFile.value = file
  }
}

function formatSize(bytes) {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function upload() {
  if (!selectedFile.value) return
  emit('upload', {
    file: selectedFile.value,
    groupId: selectedGroupId.value
  })
}
</script>

<style lang="scss" scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  width: 90%;
  max-width: 480px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  border-radius: 20px;
  border: 1px solid rgba(99, 102, 241, 0.2);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.05) inset;
  overflow: hidden;

  &.glass {
    backdrop-filter: blur(16px);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);

  h3 {
    font-size: 1.2rem;
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
    background: transparent;
    border: none;
    color: #64748b;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.2s;

    &:hover {
      color: #f8fafc;
      background: rgba(255, 255, 255, 0.05);
    }

    svg {
      width: 18px;
      height: 18px;
    }
  }
}

.upload-content {
  padding: 24px;
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 40px 24px;
  background: rgba(99, 102, 241, 0.05);
  border: 2px dashed rgba(99, 102, 241, 0.3);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(99, 102, 241, 0.1);
    border-color: rgba(99, 102, 241, 0.5);
  }

  .upload-icon {
    width: 48px;
    height: 48px;
    color: #6366f1;
  }

  .upload-text {
    font-size: 1rem;
    color: #c7d2fe;
    font-weight: 500;
    margin: 0;
  }

  .upload-hint {
    font-size: 0.8rem;
    color: #64748b;
    margin: 0;
  }
}

.file-preview {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 12px;
  margin-top: 16px;

  .file-info {
    display: flex;
    align-items: center;
    gap: 12px;

    .file-icon {
      width: 40px;
      height: 40px;
      color: #10b981;
    }

    .file-details {
      .file-name {
        font-size: 0.95rem;
        color: #f8fafc;
        margin: 0 0 4px 0;
        font-weight: 500;
      }

      .file-size {
        font-size: 0.8rem;
        color: #64748b;
        margin: 0;
      }
    }
  }

  .remove-btn {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    color: #64748b;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.2s;

    &:hover {
      color: #ef4444;
      background: rgba(239, 68, 68, 0.1);
    }

    svg {
      width: 18px;
      height: 18px;
    }
  }
}

.form-group {
  margin-top: 20px;

  label {
    display: block;
    margin-bottom: 8px;
    font-size: 0.9rem;
    color: #94a3b8;
  }

  select {
    width: 100%;
    padding: 12px 14px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 10px;
    color: #f8fafc;
    font-size: 0.95rem;
    outline: none;
    transition: all 0.25s ease;

    &:focus {
      border-color: rgba(99, 102, 241, 0.5);
      background: rgba(15, 23, 42, 0.8);
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
  }
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid rgba(99, 102, 241, 0.1);

  .modal-btn {
    flex: 1;
    padding: 12px 20px;
    border-radius: 10px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.25s ease;

    &.secondary {
      background: rgba(51, 65, 85, 0.6);
      border: none;
      color: #94a3b8;

      &:hover {
        background: rgba(71, 85, 105, 0.8);
        color: #f8fafc;
      }
    }

    &.primary {
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      border: none;
      color: white;
      box-shadow: 0 4px 15px -3px rgba(16, 185, 129, 0.4);

      &:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px -4px rgba(16, 185, 129, 0.5);
      }

      &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
    }
  }
}

.btn-spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
