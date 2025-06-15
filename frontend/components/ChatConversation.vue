<template>
  <div class="chat-conversation">
    <div class="messages-container">
      <div v-for="(prompt, index) in chat.prompts" :key="prompt.id" class="message-group">
        <ChatMessage 
          :message="prompt.input_text" 
          type="user" 
        />
        <ChatMessage 
          :message="prompt.output_text" 
          type="assistant"
          :status="prompt.status"
        />
      </div>
    </div>
    <div class="chat-actions">
      <button 
        class="btn btn-outline-secondary btn-sm"
        @click="shareChat"
        :disabled="isSharing"
      >
        <i class="bi bi-share me-2"></i>
        {{ isSharing ? 'Sharing...' : 'Share Chat' }}
      </button>
    </div>
    <ChatInput @send="handleSend" />
  </div>
</template>

<script setup>
import { nextTick, ref, watch } from 'vue'

const api = useApi()
const isSharing = ref(false)

const props = defineProps({
  chat: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['send-message'])

watch(() => props.chat.prompts, () => {
  nextTick(() => {
    scrollToBottom()
  })
}, { deep: true })

function handleSend(message) {
  emit('send-message', message)
}

function scrollToBottom() {
  const container = document.querySelector('.messages-container')
  if (container) {
    container.scrollTop = container.scrollHeight
  }
}

async function shareChat() {
  isSharing.value = true
  try {
    await api.shareChat(props.chat.uid)
    const shareUrl = `${window.location.origin}/shared/${props.chat.uid}`
    await navigator.clipboard.writeText(shareUrl)
    
    // Show success message (assuming toast is available)
    const { $toast } = useNuxtApp()
    $toast.success('Share link copied to clipboard!')
  } catch (error) {
    console.error('Failed to share chat:', error)
    const { $toast } = useNuxtApp()
    $toast.error('Failed to share chat')
  } finally {
    isSharing.value = false
  }
}
</script>

<style lang="scss" scoped>
.chat-conversation {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  background: hsl(var(--chat-bg-hue), var(--chat-bg-saturation), var(--chat-bg-lightness));
  transition: background-color 0.3s ease;
}

.message-group {
  margin-bottom: 2rem;
}

.chat-actions {
  padding: 1rem 2rem;
  border-top: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  background: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
  display: flex;
  justify-content: center;
}

.btn {
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  border: 1px solid;
  
  &.btn-outline-secondary {
    color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) + 20%));
    border-color: hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
    background: transparent;
    
    &:hover:not(:disabled) {
      background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) - 3%));
      border-color: hsl(var(--border-hue), var(--border-saturation), calc(var(--border-lightness) - 10%));
    }
    
    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }
  
  &.btn-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
  }
}
</style>