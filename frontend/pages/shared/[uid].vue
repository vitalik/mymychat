<template>
  <div class="shared-chat-layout">
    <div class="shared-chat-header">
      <div class="container">
        <h1 class="shared-title">{{ chat?.headline || 'Shared Chat' }}</h1>
        <p class="shared-description">This is a read-only view of a shared conversation.</p>
      </div>
    </div>
    
    <div class="shared-chat-content">
      <div class="container">
        <div v-if="loading" class="loading-state">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <span>Loading chat...</span>
        </div>
        
        <div v-else-if="error" class="error-state">
          <i class="bi bi-exclamation-circle"></i>
          <h3>Chat not found</h3>
          <p>This chat is either private or doesn't exist.</p>
        </div>
        
        <div v-else-if="chat" class="messages-container">
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
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

// This page doesn't require authentication
definePageMeta({
  layout: false
})

const api = useApi()
const route = useRoute()

const chat = ref(null)
const loading = ref(true)
const error = ref(false)

onMounted(async () => {
  try {
    const uid = route.params.uid
    const response = await api.getSharedChat(uid)
    chat.value = response
  } catch (err) {
    console.error('Failed to load shared chat:', err)
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
.shared-chat-layout {
  min-height: 100vh;
  background: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
}

.shared-chat-header {
  background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) + 3%));
  border-bottom: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  padding: 2rem 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 2rem;
}

.shared-title {
  color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.shared-description {
  color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) + 30%));
  margin: 0;
  font-size: 0.875rem;
}

.shared-chat-content {
  padding: 2rem 0;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) + 20%));
  
  .spinner-border {
    width: 2rem;
    height: 2rem;
    margin-bottom: 1rem;
    border: 0.2rem solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
    border-right-color: transparent;
    border-radius: 50%;
    animation: spinner-border 0.75s linear infinite;
  }
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  
  i {
    font-size: 3rem;
    color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) + 40%));
    margin-bottom: 1rem;
  }
  
  h3 {
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
    margin: 0 0 0.5rem 0;
    font-size: 1.25rem;
  }
  
  p {
    color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) + 20%));
    margin: 0;
  }
}

.messages-container {
  padding: 0;
}

.message-group {
  margin-bottom: 2rem;
}

@keyframes spinner-border {
  to {
    transform: rotate(360deg);
  }
}

.visually-hidden {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: -1px !important;
  overflow: hidden !important;
  clip: rect(0, 0, 0, 0) !important;
  white-space: nowrap !important;
  border: 0 !important;
}

// Dark theme adjustments
[data-theme="dark"] {
  .shared-description {
    color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) - 30%));
  }
  
  .loading-state {
    color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) - 20%));
  }
  
  .error-state {
    i {
      color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) - 40%));
    }
    
    p {
      color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) - 20%));
    }
  }
}
</style>