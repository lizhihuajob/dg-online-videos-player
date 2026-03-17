<template>
  <BaseModal
    :show="show"
    title="修改音乐名称"
    @close="onClose"
  >
    <div class="form-group">
      <label>音乐名称</label>
      <input
        type="text"
        v-model="form.name"
        placeholder="请输入音乐名称"
      >
    </div>
    <template #footer>
      <button class="btn secondary" @click="onClose">取消</button>
      <button
        class="btn primary"
        :disabled="!form.name.trim() || isLoading"
        @click="handleSave"
      >
        <span v-if="isLoading" class="btn-spinner"></span>
        <span v-else>保存</span>
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, watch } from 'vue'
import BaseModal from '../BaseModal.vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  music: {
    type: Object,
    default: null
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'save'])

const form = ref({ name: '' })

watch(() => props.music, (newMusic) => {
  if (newMusic) {
    form.value.name = newMusic.original_name
  }
})

function onClose() {
  form.value.name = ''
  emit('close')
}

function handleSave() {
  if (form.value.name.trim()) {
    emit('save', form.value.name.trim())
  }
}
</script>

<style lang="scss" scoped>
.form-group {
  margin-bottom: 0;

  label {
    display: block;
    margin-bottom: 8px;
    color: #f8fafc;
    font-weight: 500;
  }

  input {
    width: 100%;
    padding: 12px 16px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 8px;
    color: #f8fafc;
    font-size: 0.95rem;
    outline: none;
    transition: all 0.25s ease;

    &:focus {
      border-color: rgba(99, 102, 241, 0.5);
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
  }
}
</style>
