<template>
  <div class="chat-input-container">
    <div class="chat-input-wrapper">
      <div class="input-group">
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

function handleKeydown(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    handleSend()
  }
}

function handleSend() {
  if (message.value.trim()) {
    emit('send', message.value)
    message.value = ''
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
.chat-input-wrapper {
  max-width: 800px;
  margin: 0 auto;
  
  .input-group {
    display: flex;
    align-items: flex-end;
    gap: 0.75rem;
    background: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
    border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
    border-radius: 1.5rem;
    padding: 0.75rem 1rem;
    transition: all 0.3s ease;
    
    &:focus-within {
      border-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
      box-shadow: 0 0 0 0.2rem hsl(var(--primary-hue) var(--primary-saturation) var(--primary-lightness) / 0.1);
    }
    
    [data-theme="dark"] & {
      background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) + 5%));
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
}
</style>