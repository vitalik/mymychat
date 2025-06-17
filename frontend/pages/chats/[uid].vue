<template>
  <div class="chat-layout">
    <ChatSidebar 
      :chats="chats" 
      :activeChat="activeChat"
      @select-chat="selectChat"
      @new-chat="startNewChat"
    />
    <div class="chat-main">
      <div class="chat-container">
        <ChatConversation 
          v-if="activeChat"
          :chat="activeChat"
          @send-message="sendMessage"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { store } from '~/stores/chatStore'

const { $toast } = useNuxtApp()
const api = useApi()
const route = useRoute()
const router = useRouter()

// Use computed property for chats from store
const chats = computed(() => store.chats)
const activeChat = ref(null)
const eventSource = ref(null)
const lastPromptId = ref(null)

onMounted(() => {
  // Load chats from store (won't cause empty flash)
  store.loadChats()
  if (route.params.uid) {
    loadChat(route.params.uid)
  }
})

watch(() => route.params.uid, (newUid) => {
  if (newUid) {
    closeSSEConnection() // Close current connection before switching
    loadChat(newUid)
  } else {
    closeSSEConnection() // Close connection when leaving chat
  }
})

onUnmounted(() => {
  closeSSEConnection()
})


async function loadChat(uid) {
  try {
    const response = await api.getChat(uid)
    activeChat.value = response
    
    // Track the highest prompt ID for resume functionality
    updateLastPromptId()
    
    // Start SSE connection for real-time updates
    startSSEConnection(uid)
  } catch (error) {
    $toast.error('Failed to load chat')
    router.push('/')
  }
}

function updateLastPromptId() {
  if (activeChat.value?.prompts?.length > 0) {
    const maxId = Math.max(...activeChat.value.prompts.map(p => p.id))
    lastPromptId.value = maxId
  }
}

function startSSEConnection(uid) {
  // Close existing connection
  closeSSEConnection()
  
  try {
    const token = localStorage.getItem('auth_token')
    const url = `${api.baseURL}/chats/${uid}/stream?token=${encodeURIComponent(token)}`
    eventSource.value = new EventSource(url)
    
    eventSource.value.onopen = () => {
      console.log('SSE connection opened for chat:', uid)
    }
    
    eventSource.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        handleSSEMessage(data)
      } catch (error) {
        console.error('Error parsing SSE message:', error)
      }
    }
    
    eventSource.value.onerror = (error) => {
      console.error('SSE connection error:', error)
      // Attempt to reconnect after a delay
      setTimeout(() => {
        if (activeChat.value) {
          startSSEConnection(activeChat.value.uid)
        }
      }, 5000)
    }
  } catch (error) {
    console.error('Failed to create SSE connection:', error)
  }
}

function closeSSEConnection() {
  if (eventSource.value) {
    eventSource.value.close()
    eventSource.value = null
  }
}

function handleSSEMessage(data) {
  if (!activeChat.value) return
  
  if (data.type === 'connected') {
    console.log('Connected to chat stream:', data.chat_uid)
    return
  }
  
  if (data.type === 'chunk' && data.prompt_id) {
    updatePromptWithChunk(data.prompt_id, data.chunk)
  }
  
  if (data.type === 'status' && data.prompt_id) {
    updatePromptStatus(data.prompt_id, data.status)
  }
  
  // Check for new prompts if we receive a prompt_id higher than our last known
  if (data.prompt_id && data.prompt_id > lastPromptId.value) {
    refreshChatData()
  }
}

function updatePromptWithChunk(promptId, chunk) {
  const prompt = activeChat.value.prompts.find(p => p.id === promptId)
  if (prompt) {
    prompt.output_text = (prompt.output_text || '') + chunk
  }
}

function updatePromptStatus(promptId, status) {
  const prompt = activeChat.value.prompts.find(p => p.id === promptId)
  if (prompt) {
    prompt.status = status
  }
}

async function refreshChatData() {
  try {
    const response = await api.getChat(activeChat.value.uid)
    activeChat.value = response
    updateLastPromptId()
  } catch (error) {
    console.error('Failed to refresh chat data:', error)
  }
}

async function selectChat(chatUid) {
  router.push(`/chats/${chatUid}`)
}

function startNewChat() {
  router.push('/')
}

async function sendMessage(data) {
  try {
    // Handle both old string format and new object format
    const payload = typeof data === 'string' 
      ? { input_text: data, file_ids: [] }
      : { input_text: data.text, file_ids: data.fileIds || [] }
    
    await api.createPrompt(activeChat.value.uid, payload)
    // SSE will handle real-time updates, no need to manually reload
    
    // Refresh chats list in store (in background)
    store.loadChats()
  } catch (error) {
    $toast.error('Failed to send message')
  }
}
</script>

<style lang="scss" scoped>
.chat-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: hsl(var(--chat-bg-hue), var(--chat-bg-saturation), var(--chat-bg-lightness));
  transition: background-color 0.3s ease;
}

.chat-container {
  max-width: 1000px;
  width: 100%;
  margin: 0 auto;
  height: 100%;
}
</style>