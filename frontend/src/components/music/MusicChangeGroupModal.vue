<template>
  <BaseModal
    :show="show"
    title="切换分组"
    @close="onClose"
  >
    <div class="form-group">
      <label>选择分组</label>
      <select v-model="form.group_id" class="group-select">
        <option :value="0">取消分组</option>
        <option v-for="group in groups" :key="group.id" :value="group.id">
          {{ group.name }}
        </option>
      </select>
    </div>
    <template #footer>
      <button class="btn secondary" @click="onClose">取消</button>
      <button
        class="btn primary"
        :disabled="isLoading"
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
  groups: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'save'])

const form = ref({ group_id: 0 })

watch(() => props.music, (newMusic) => {
  if (newMusic) {
    form.value.group_id = newMusic.group_id || 0
  }
})

function onClose() {
  form.value.group_id = 0
  emit('close')
}

function handleSave() {
  emit('save', form.value.group_id)
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

  .group-select {
    width: 100%;
    padding: 12px 16px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 8px;
    color: #f8fafc;
    font-size: 0.95rem;
    outline: none;
    transition: all 0.25s ease;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
    background-size: 16px;

    &:focus {
      border-color: rgba(99, 102, 241, 0.5);
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
  }
}
</style>
