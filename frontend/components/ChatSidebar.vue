<template>
  <div class="chat-sidebar">
    <div class="sidebar-header">
      <h5><i class="bi bi-chat-dots-fill me-2"></i>MyMyChat</h5>
      <div class="header-actions">
        <button class="btn btn-sm theme-toggle" @click="toggleTheme" :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'">
          <i :class="isDark ? 'bi bi-sun-fill' : 'bi bi-moon-fill'"></i>
        </button>
        <button class="btn btn-sm btn-primary ms-2" @click="$emit('new-chat')">
          <i class="bi bi-plus-lg"></i>
        </button>
      </div>
    </div>
    <div class="chat-list">
      <div 
        v-for="chat in chats" 
        :key="chat.uid"
        class="chat-item"
        :class="{ active: activeChat?.uid === chat.uid }"
        @click="$emit('select-chat', chat.uid)"
      >
        <div class="chat-icon">
          <i class="bi bi-chat-left-text"></i>
        </div>
        <div class="chat-content">
          <div class="chat-headline">{{ chat.headline }}</div>
        </div>
      </div>
      
      <div v-if="chats.length === 0" class="empty-state">
        <i class="bi bi-chat-square-dots opacity-50"></i>
        <p class="text-muted mt-2 mb-0">No chats yet</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject } from 'vue'

defineProps({
  chats: {
    type: Array,
    default: () => []
  },
  activeChat: {
    type: Object,
    default: null
  }
})

defineEmits(['select-chat', 'new-chat'])

// Theme functionality
const theme = inject('theme')
const { isDark, toggleTheme } = theme
</script>

<style lang="scss" scoped>
.sidebar-header {
  .header-actions {
    display: flex;
    align-items: center;
  }
  
  .theme-toggle {
    background: none;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: currentColor;
    padding: 0.375rem 0.5rem;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
    
    &:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.4);
    }
  }
}

.chat-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  
  .chat-icon {
    flex-shrink: 0;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0.5rem;
    background: rgba(255, 255, 255, 0.1);
    
    i {
      font-size: 0.875rem;
    }
  }
  
  .chat-content {
    flex: 1;
    min-width: 0;
  }
  
  &.active .chat-icon {
    background: rgba(255, 255, 255, 0.3);
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  text-align: center;
  
  i {
    font-size: 2rem;
  }
  
  p {
    font-size: 0.875rem;
  }
}
</style>