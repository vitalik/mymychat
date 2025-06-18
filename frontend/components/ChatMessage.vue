<template>
  <div class="message" :class="[`message-${type}`, { 'message-loading': status === 'running' }]">
    <div class="message-avatar">
      <i v-if="type === 'user'" class="bi bi-person-fill"></i>
      <i v-else class="bi bi-robot"></i>
    </div>
    <div class="message-content">
      <div v-if="type === 'assistant' && status === 'queued'" class="status-indicator">
        <i class="bi bi-clock me-2"></i>
        <span>Waiting...</span>
      </div>
      <div v-else-if="type === 'assistant' && status === 'running'" class="message-text">
        <div v-if="message" v-html="renderedMessage" class="markdown-content"></div>
        <span v-else class="status-indicator">
          <div class="spinner-border spinner-border-sm me-2" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <span>Generating...</span>
        </span>
      </div>
      <div v-else-if="type === 'assistant' && !message" class="status-indicator">
        <i class="bi bi-exclamation-circle me-2"></i>
        <span>No response yet</span>
      </div>
      <div v-else class="message-text">
        <div v-if="type === 'assistant'" v-html="renderedMessage" class="markdown-content"></div>
        <div v-else>{{ message }}</div>
        <div v-if="files && files.length > 0" class="message-files">
          <div v-for="file in files" :key="file.id" class="file-attachment">
            <i class="bi bi-paperclip"></i>
            <span>{{ file.filename }}</span>
          </div>
        </div>
        <button 
          v-if="type === 'assistant' && message && status !== 'queued'"
          class="copy-button"
          @click="copyMessage"
          :title="copyStatus"
        >
          <i v-if="copyStatus === 'Copied!'" class="bi bi-check"></i>
          <i v-else class="bi bi-copy"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  message: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    required: true,
    validator: (value) => ['user', 'assistant'].includes(value)
  },
  status: {
    type: String,
    default: 'finished'
  },
  files: {
    type: Array,
    default: () => []
  }
})

const { renderMarkdown } = useMarkdown()
const copyStatus = ref('Copy to clipboard')

const renderedMessage = computed(() => {
  if (props.type === 'assistant' && props.message) {
    const options = props.status === 'running' ? { appendTypingIndicator: true } : {}
    return renderMarkdown(props.message, options)
  }
  return props.message
})

async function copyMessage() {
  try {
    await navigator.clipboard.writeText(props.message)
    copyStatus.value = 'Copied!'
    setTimeout(() => {
      copyStatus.value = 'Copy to clipboard'
    }, 2000)
  } catch (error) {
    console.error('Failed to copy message:', error)
    copyStatus.value = 'Failed to copy'
    setTimeout(() => {
      copyStatus.value = 'Copy to clipboard'
    }, 2000)
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/scss/variables';

.message {
  display: flex;
  gap: 0.375rem;  // More compact gap
  margin-bottom: 0.75rem;  // More compact margin
  
  &.message-user {
    flex-direction: row-reverse;
    justify-content: flex-start;
  }
}

.message-avatar {
  flex-shrink: 0;
  width: 2rem;  // Smaller avatar
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;  // Smaller icon
  
  .message-user & {
    background: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    color: white;
  }
  
  .message-assistant & {
    background: hsl(var(--secondary-hue), var(--secondary-saturation), var(--secondary-lightness));
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  }
}

.message-content {
  flex: 1;
  max-width: calc(100% - 2.75rem);  // Adjusted for smaller avatar
  position: relative;
  
  .message-user & {
    flex: 0 1 auto;
    max-width: 75%;
    background: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    color: white;
    padding: 0.45rem 0.6rem;  // More compact padding
    border-radius: 0.5rem 0.5rem 0.25rem 0.5rem;  // More compact border radius
    display: inline-block;
  }
  
  .message-assistant & {
    background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) + 5%));
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
    border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
    padding: 0.45rem 0.6rem;  // More compact padding
    border-radius: 0.5rem 0.5rem 0.5rem 0.25rem;  // More compact border radius
  }
  
  .message-loading & {
    background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) - 5%));
  }
}

.copy-button {
  display: inline-flex;
  align-items: center;
  margin-top: 0.5rem;
  background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) + 3%));
  border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  border-radius: 0.25rem;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  opacity: 0.7;
  transition: all 0.2s;
  font-size: 0.75rem;
  
  &:hover {
    opacity: 1;
    background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) + 5%));
  }
  
  i {
    font-size: 0.75rem;
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  }
}

.message-text {
  white-space: pre-wrap;
  line-height: 1.4;  // More compact line height
  word-wrap: break-word;
}

.status-indicator {
  color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) + 30%));
  font-style: italic;
  display: inline-flex;
  align-items: center;
  font-size: 0.875rem;  // Slightly smaller
  
  [data-theme="dark"] & {
    color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) - 30%));
  }
}

.typing-indicator {
  animation: blink 1s infinite;
  margin-left: 2px;
  opacity: 0.7;
}

// Typing indicator inside markdown content
.markdown-content :deep(.typing-indicator) {
  animation: blink 1s infinite;
  margin-left: 2px;
  opacity: 0.7;
  display: inline;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

// Markdown content styling
.markdown-content {
  :deep(h1), :deep(h2), :deep(h3), :deep(h4), :deep(h5), :deep(h6) {
    margin: 0.75rem 0 0.5rem 0;
    line-height: 1.3;
    font-weight: 600;
    
    &:first-child {
      margin-top: 0;
    }
  }
  
  :deep(h1) { font-size: 1.5rem; }
  :deep(h2) { font-size: 1.25rem; }
  :deep(h3) { font-size: 1.125rem; }
  :deep(h4) { font-size: 1rem; }
  :deep(h5) { font-size: 0.875rem; }
  :deep(h6) { font-size: 0.75rem; }
  
  :deep(p) {
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.4;
    
    & + p {
      margin-top: 0.5rem !important;
    }
  }
  
  :deep(ul), :deep(ol) {
    margin: 0 !important;
    padding: 0 !important;
    padding-left: 1.25rem !important;
    list-style-position: outside;
    
    & + p {
      margin-top: 0.5rem !important;
    }
    
    li {
      margin: 0 !important;
      padding: 0 !important;
      line-height: 0.8rem !important;
      
      & + li {
        margin-top: 0.25rem !important;
      }
      
      p {
        margin: 0 !important;
        padding: 0 !important;
        
        &:first-child {
          display: inline;
        }
      }
      
      ul, ol {
        margin-top: 0.25rem !important;
        margin-bottom: 0 !important;
      }
    }
  }
  
  :deep(blockquote) {
    margin: 0.75rem 0;
    padding: 0.5rem 0.75rem;
    border-left: 3px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
    background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) + 2%));
    font-style: italic;
    border-radius: 0 0.25rem 0.25rem 0;
  }
  
  :deep(code) {
    padding: 0.125rem 0.25rem;
    background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) - 3%));
    border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
    border-radius: 0.25rem;
    font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
    font-size: 0.875em;
  }
  
  :deep(pre) {
    margin: 0.75rem 0;
    padding: 0.75rem;
    background: #282c34 !important; // Atom One Dark background
    border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
    border-radius: 0.375rem;
    overflow-x: auto;
    line-height: 1.4;
    
    code {
      padding: 0;
      background: none !important;
      border: none;
      font-size: 0.875rem;
      color: #abb2bf !important; // Atom One Dark text color
      
      // Ensure highlight.js classes work
      &.hljs {
        background: none !important;
        padding: 0;
        display: block;
      }
      
      // Preserve highlighting colors
      * {
        background: none !important;
      }
    }
  }
  
  :deep(table) {
    width: 100%;
    margin: 0.75rem 0;
    border-collapse: collapse;
    border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
    border-radius: 0.375rem;
    overflow: hidden;
    
    th, td {
      padding: 0.375rem 0.5rem;
      border-bottom: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
      text-align: left;
      line-height: 1.4;
    }
    
    th {
      background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) - 3%));
      font-weight: 600;
    }
    
    tr:last-child td {
      border-bottom: none;
    }
  }
  
  :deep(a) {
    color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
  
  :deep(strong) {
    font-weight: 600;
  }
  
  :deep(em) {
    font-style: italic;
  }
  
  :deep(hr) {
    margin: 1rem 0;
    border: none;
    border-top: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  }
}

// Dark theme adjustments for markdown
[data-theme="dark"] {
  .markdown-content {
    :deep(blockquote) {
      background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) + 3%));
    }
    
    :deep(code) {
      background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) + 5%));
    }
    
    :deep(pre) {
      background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) + 3%));
    }
    
    :deep(th) {
      background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) + 5%));
    }
  }
}

.message-files {
  margin-top: 0.5rem;
}

.file-attachment {
  display: inline-flex;
  align-items: center;
  font-size: 0.875rem;
  color: hsl(var(--muted-foreground-hue), var(--muted-foreground-saturation), var(--muted-foreground-lightness));
  margin-right: 0.75rem;
  
  i {
    margin-right: 0.25rem;
  }
}
</style>