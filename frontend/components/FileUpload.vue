<template>
  <div class="file-upload">
    <input
      ref="fileInput"
      type="file"
      multiple
      @change="handleFileSelect"
      style="display: none"
    />
    
    <div 
      class="upload-area"
      @click="openFileDialog"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      @drop.prevent="handleDrop"
      :class="{ 'drag-over': isDragOver }"
    >
      <i class="bi bi-cloud-upload me-2"></i>
      <span v-if="!isDragOver">Click to upload files or drag & drop</span>
      <span v-else>Drop files here</span>
    </div>
    
    <div v-if="uploadedFiles.length > 0" class="file-list">
      <div 
        v-for="file in uploadedFiles" 
        :key="file.id" 
        class="file-item"
      >
        <span class="file-name">{{ file.filename }}</span>
        <button 
          class="btn-remove" 
          @click="removeFile(file.id)"
          type="button"
        >
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const fileInput = ref(null)
const uploadedFiles = ref([])
const isDragOver = ref(false)
const { $toast } = useNuxtApp()
const api = useApi()

function openFileDialog() {
  fileInput.value?.click()
}

async function handleFileSelect(event) {
  const files = event.target.files
  if (!files || files.length === 0) return

  await uploadFiles(files)
  
  // Clear input
  event.target.value = ''
}

async function uploadFiles(files) {
  for (const file of files) {
    try {
      const response = await api.uploadFile(file)
      uploadedFiles.value.push({
        id: response.id,
        filename: response.filename
      })
    } catch (error) {
      $toast.error(`Failed to upload ${file.name}`)
    }
  }
  
  // Update parent with file IDs
  updateFileIds()
}

function handleDragOver(event) {
  isDragOver.value = true
}

function handleDragLeave(event) {
  isDragOver.value = false
}

async function handleDrop(event) {
  isDragOver.value = false
  const files = event.dataTransfer?.files
  if (!files || files.length === 0) return
  
  await uploadFiles(files)
}

function removeFile(fileId) {
  uploadedFiles.value = uploadedFiles.value.filter(f => f.id !== fileId)
  updateFileIds()
}

function updateFileIds() {
  const fileIds = uploadedFiles.value.map(f => f.id)
  emit('update:modelValue', fileIds)
}

// Clear files when model value is reset
watch(() => props.modelValue, (newVal) => {
  if (newVal.length === 0) {
    uploadedFiles.value = []
  }
})

// Expose method to open file dialog
defineExpose({
  openFileDialog
})
</script>

<style lang="scss" scoped>
.upload-area {
  width: 100%;
  padding: 0.75rem;
  border: 2px dashed hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  border-radius: 0.5rem;
  background: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
  color: hsl(var(--muted-foreground-hue), var(--muted-foreground-saturation), var(--muted-foreground-lightness));
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  
  &:hover, &.drag-over {
    border-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
    background: hsl(var(--muted-hue), var(--muted-saturation), var(--muted-lightness));
  }
  
  &.drag-over {
    border-style: solid;
    background: hsl(var(--primary-hue) var(--primary-saturation) var(--primary-lightness) / 0.1);
  }
  
  i {
    font-size: 1.1rem;
  }
}

.file-list {
  margin-top: 0.5rem;
}

.file-item {
  display: inline-flex;
  align-items: center;
  background: hsl(var(--muted-hue), var(--muted-saturation), var(--muted-lightness));
  border-radius: 0.5rem;
  padding: 0.25rem 0.5rem;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
}

.file-name {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-remove {
  background: none;
  border: none;
  color: hsl(var(--muted-foreground-hue), var(--muted-foreground-saturation), var(--muted-foreground-lightness));
  cursor: pointer;
  padding: 0;
  margin-left: 0.5rem;
  display: flex;
  align-items: center;
  
  &:hover {
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  }
}
</style>