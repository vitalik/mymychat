<template>
  <div class="chat-input-container">
    <div class="chat-input-wrapper">
      <FileUpload ref="fileUploadRef" v-model="fileIds" />
      <div class="input-group">
        <button 
          class="btn btn-link attach-button" 
          @click="$refs.fileUploadRef.openFileDialog()"
          type="button"
          title="Attach files"
        >
          <i class="bi bi-paperclip"></i>
        </button>
        <textarea
          ref="textareaRef"
          v-model="message"
          class="form-control"
          placeholder="Type your message..."
          rows="1"
          @keydown="handleKeydown"
          @input="autoResize"
        ></textarea>
        <button 
          class="btn btn-primary send-button" 
          @click="handleSend"
          :disabled="!message.trim()"
          type="button"
        >
          <i class="bi bi-send-fill"></i>
          <span class="d-none d-sm-inline ms-2">Send</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const emit = defineEmits(['send'])

const message = ref('')
const textareaRef = ref(null)
const fileUploadRef = ref(null)
const fileIds = ref([])

function handleKeydown(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    handleSend()
  }
}

function handleSend() {
  if (message.value.trim() || fileIds.value.length > 0) {
    emit('send', { 
      text: message.value, 
      fileIds: fileIds.value 
    })
    message.value = ''
    fileIds.value = []
    nextTick(() => {
      autoResize()
    })
  }
}

function autoResize() {
  const textarea = textareaRef.value
  if (textarea) {
    textarea.style.height = 'auto'
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px'
  }
}
</script>

<style lang="scss" scoped>
.chat-input-container {
  padding: 1rem 2rem;
  background: hsl(var(--chat-bg-hue), var(--chat-bg-saturation), var(--chat-bg-lightness));
  transition: background-color 0.3s ease;
}

.chat-input-wrapper {
  max-width: 800px;
  margin: 0 auto;
  
  .input-group {
    display: flex;
    align-items: flex-end;
    gap: 0.5rem;
    background: hsl(var(--chat-bg-hue), var(--chat-bg-saturation), var(--chat-bg-lightness));
    border: none;
    border-radius: 1.5rem;
    padding: 0.75rem 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 0 0 1px hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
    
    &:focus-within {
      box-shadow: 0 0 0 2px hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    }
  }
  
  .form-control {
    flex: 1;
    border: none;
    outline: none;
    background: transparent;
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
    resize: none;
    min-height: 1.5rem;
    max-height: 120px;
    overflow-y: auto;
    padding: 0;
    
    &::placeholder {
      color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) + 40%));
      
      [data-theme="dark"] & {
        color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) - 40%));
      }
    }
    
    &:focus {
      box-shadow: none;
    }
  }
  
  .send-button {
    flex-shrink: 0;
    border: none;
    background: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    
    &:hover:not(:disabled) {
      background: hsl(var(--primary-hue), var(--primary-saturation), calc(var(--primary-lightness) - 5%));
      transform: translateY(-1px);
    }
    
    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    
    i {
      font-size: 0.875rem;
    }
  }
  
  .attach-button {
    flex-shrink: 0;
    border: none;
    background: none;
    color: hsl(var(--muted-foreground-hue), var(--muted-foreground-saturation), var(--muted-foreground-lightness));
    padding: 0.25rem;
    transition: color 0.2s ease;
    
    &:hover {
      color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
    }
    
    i {
      font-size: 1.25rem;
    }
  }
}
</style>