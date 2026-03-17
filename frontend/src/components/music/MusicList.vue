<template>
  <div class="music-list">
    <div class="list-header">
      <span class="col-name">音乐名称</span>
      <span class="col-format">格式</span>
      <span class="col-size">大小</span>
      <span class="col-group">分组</span>
      <span class="col-date">上传时间</span>
      <span class="col-actions">操作</span>
    </div>
    <div
      v-for="music in musicList"
      :key="music.id"
      class="list-item"
    >
      <div class="col-name">
        <div class="music-icon-small">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 18V5l12-2v13"/>
            <circle cx="6" cy="18" r="3"/>
            <circle cx="18" cy="16" r="3"/>
          </svg>
        </div>
        <span class="music-name-text" :title="music.original_name">{{ music.original_name }}</span>
      </div>
      <span class="col-format">{{ music.format.toUpperCase() }}</span>
      <span class="col-size">{{ formatSize(music.size) }}</span>
      <span class="col-group">{{ getGroupName(music.group_id) || '-' }}</span>
      <span class="col-date">{{ formatDate(music.created_at) }}</span>
      <div class="col-actions">
        <button class="action-btn-small edit" @click="$emit('edit', music)" title="修改名称">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
        </button>
        <button class="action-btn-small group" @click="$emit('change-group', music)" title="切换分组">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
          </svg>
        </button>
        <button class="action-btn-small play" @click="$emit('play', music)" title="播放">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5 3 19 12 5 21 5 3"/>
          </svg>
        </button>
        <button class="action-btn-small delete" @click="$emit('delete', music)" title="删除">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  musicList: {
    type: Array,
    required: true
  },
  getGroupName: {
    type: Function,
    required: true
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
.music-list {
  display: flex;
  flex-direction: column;
  gap: 1px;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(99, 102, 241, 0.15);

  .list-header {
    display: grid;
    grid-template-columns: 2fr 80px 100px 120px 120px 180px;
    gap: 16px;
    padding: 14px 20px;
    background: rgba(30, 41, 59, 0.8);
    font-size: 0.85rem;
    font-weight: 600;
    color: #94a3b8;

    @media (max-width: 1024px) {
      display: none;
    }
  }

  .list-item {
    display: grid;
    grid-template-columns: 2fr 80px 100px 120px 120px 180px;
    gap: 16px;
    padding: 12px 20px;
    background: rgba(30, 41, 59, 0.6);
    align-items: center;
    transition: all 0.2s ease;

    &:hover {
      background: rgba(30, 41, 59, 0.8);
    }

    @media (max-width: 1024px) {
      grid-template-columns: 1fr auto;
      gap: 12px;

      .col-name {
        grid-column: 1;
      }

      .col-actions {
        grid-column: 2;
      }

      .col-format, .col-size, .col-group, .col-date {
        display: none;
      }
    }
  }

  .col-name {
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 0;

    .music-icon-small {
      width: 40px;
      height: 40px;
      background: rgba(16, 185, 129, 0.15);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;

      svg {
        width: 20px;
        height: 20px;
        color: #10b981;
      }
    }

    .music-name-text {
      font-size: 0.9rem;
      color: #f8fafc;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }

  .col-format, .col-size, .col-group, .col-date {
    font-size: 0.85rem;
    color: #94a3b8;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .col-actions {
    display: flex;
    gap: 8px;
    justify-content: flex-end;

    .action-btn-small {
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(99, 102, 241, 0.15);
      border-radius: 8px;
      color: #94a3b8;
      cursor: pointer;
      transition: all 0.2s ease;

      svg {
        width: 14px;
        height: 14px;
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
}
</style>
