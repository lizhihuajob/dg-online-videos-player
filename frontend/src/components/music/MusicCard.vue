<template>
  <div class="music-card">
    <div class="music-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M9 18V5l12-2v13"/>
        <circle cx="6" cy="18" r="3"/>
        <circle cx="18" cy="16" r="3"/>
      </svg>
    </div>
    <div class="music-info">
      <h3 class="music-name" :title="music.original_name">{{ music.original_name }}</h3>
      <div class="music-meta">
        <span class="meta-format">{{ music.format.toUpperCase() }}</span>
        <span class="meta-size">{{ formatSize(music.size) }}</span>
        <span v-if="groupName" class="meta-group">{{ groupName }}</span>
      </div>
      <p class="music-date">{{ formatDate(music.created_at) }}</p>
    </div>
    <div class="music-actions">
      <button class="action-btn edit" @click="$emit('edit', music)" title="修改名称">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
        </svg>
      </button>
      <button class="action-btn group" @click="$emit('change-group', music)" title="切换分组">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
        </svg>
      </button>
      <button class="action-btn play" @click="$emit('play', music)" title="播放">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="5 3 19 12 5 21 5 3"/>
        </svg>
      </button>
      <button class="action-btn delete" @click="$emit('delete', music)" title="删除">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="3 6 5 6 21 6"/>
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  music: {
    type: Object,
    required: true
  },
  groupName: {
    type: String,
    default: ''
  }
})

defineEmits(['edit', 'change-group', 'play', 'delete'])

function formatSize(bytes) {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' })
}
</script>

<style lang="scss" scoped>
.music-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-4px);
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: 0 12px 40px -10px rgba(99, 102, 241, 0.2);
  }
}

.music-icon {
  width: 60px;
  height: 60px;
  background: rgba(16, 185, 129, 0.15);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  svg {
    width: 30px;
    height: 30px;
    color: #10b981;
  }
}

.music-info {
  flex: 1;
  min-width: 0;

  .music-name {
    font-size: 1rem;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .music-meta {
    display: flex;
    gap: 8px;
    margin-bottom: 6px;
    flex-wrap: wrap;

    span {
      font-size: 0.75rem;
      padding: 2px 8px;
      border-radius: 4px;
      background: rgba(99, 102, 241, 0.1);
      color: #a5b4fc;
    }
  }

  .music-date {
    font-size: 0.8rem;
    color: #64748b;
  }
}

.music-actions {
  display: flex;
  gap: 8px;

  .action-btn {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 10px;
    color: #94a3b8;
    cursor: pointer;
    transition: all 0.2s ease;

    svg {
      width: 16px;
      height: 16px;
    }

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      border-color: rgba(99, 102, 241, 0.3);
    }

    &.edit:hover {
      color: #6366f1;
    }

    &.group:hover {
      color: #8b5cf6;
    }

    &.play:hover {
      color: #10b981;
    }

    &.delete:hover {
      color: #ef4444;
      border-color: rgba(239, 68, 68, 0.3);
    }
  }
}
</style>
