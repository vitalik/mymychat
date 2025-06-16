<template>
  <div class="chat-layout">
    <ChatSidebar 
      :chats="chats" 
      :activeChat="null"
      @select-chat="selectChat"
      @new-chat="startNewChat"
    />
    <div class="chat-main">
      <div class="chat-welcome">
        <h3>Welcome to MyMyChat</h3>
        <p>Start a new conversation</p>
        <div class="new-chat-form">
          <div class="model-selection mb-3">
            <label class="form-label">
              <i class="bi bi-cpu me-2"></i>Choose Model
            </label>
            <ModelSelector 
              v-model="selectedModel" 
              :providers="providers"
              @update:modelValue="saveSelectedModel"
            />
          </div>
          
          <div class="system-prompt-selection mb-3">
            <label for="system-prompt-select" class="form-label">
              <i class="bi bi-chat-quote me-2"></i>System Prompt (Optional)
            </label>
            <select 
              id="system-prompt-select"
              v-model="selectedSystemPrompt" 
              class="form-select"
            >
              <option value="">None</option>
              <option v-for="prompt in systemPrompts" :key="prompt.id" :value="prompt.text">
                {{ prompt.text.substring(0, 50) }}{{ prompt.text.length > 50 ? '...' : '' }}
              </option>
            </select>
          </div>
          
          <div class="tool-selection mb-3">
            <ToolSelector v-model="selectedTools" />
          </div>
          
          <div class="file-upload-section mb-3">
            <label class="form-label">
              <i class="bi bi-paperclip me-2"></i>Attachments (Optional)
            </label>
            <FileUpload v-model="selectedFileIds" />
          </div>
          
          <textarea
            v-model="newMessage"
            class="form-control"
            placeholder="Type your message to start a new chat..."
            rows="4"
            @keydown.enter.prevent="createNewChat"
          ></textarea>
          
          <button 
            class="btn btn-primary mt-3" 
            @click="createNewChat"
            :disabled="!newMessage.trim()"
          >
            <i class="bi bi-send-fill me-2"></i>Start Chat
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const { $toast } = useNuxtApp()
const api = useApi()
const router = useRouter()

const chats = ref([])
const newMessage = ref('')
const providers = ref([])
const systemPrompts = ref([])
const selectedModel = ref(localStorage.getItem('selectedModel') || 'dummy:dummy')
const selectedSystemPrompt = ref('')
const selectedTools = ref([])
const selectedFileIds = ref([])

onMounted(() => {
  loadChats()
  loadSystemPrompts()
  loadModels()
})

function saveSelectedModel() {
  localStorage.setItem('selectedModel', selectedModel.value)
}

async function loadChats() {
  try {
    const response = await api.getChats()
    chats.value = response
  } catch (error) {
    $toast.error('Failed to load chats')
  }
}

async function loadModels() {
  try {
    const response = await api.getModels()
    providers.value = response
    
    // Only set default if no saved model and current is still default
    if (selectedModel.value === 'dummy:dummy' && providers.value.length > 0 && providers.value[0].models.length > 0) {
      selectedModel.value = providers.value[0].models[0].id  
    }
  } catch (error) {
    $toast.error('Failed to load models')
  }
}

async function loadSystemPrompts() {
  try {
    const response = await api.getSystemPrompts()
    systemPrompts.value = response
  } catch (error) {
    $toast.error('Failed to load system prompts')
  }
}

async function selectChat(chatUid) {
  router.push(`/chats/${chatUid}`)
}

function startNewChat() {
  newMessage.value = ''
}

async function createNewChat() {
  if (!newMessage.value.trim() && selectedFileIds.value.length === 0) return
  
  try {
    const response = await api.createChat({
      input_text: newMessage.value,
      model: selectedModel.value,
      system_prompt: selectedSystemPrompt.value,
      tools: selectedTools.value,
      file_ids: selectedFileIds.value
    })
    router.push(`/chats/${response.uid}`)
  } catch (error) {
    $toast.error('Failed to create chat')
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

.chat-welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  padding: 2rem;
}

.chat-welcome h3 {
  margin-bottom: 1rem;
  color: #333;
}

.chat-welcome p {
  color: #666;
  margin-bottom: 2rem;
}

.new-chat-form {
  width: 100%;
  max-width: 600px;
}

.model-selection, .system-prompt-selection, .file-upload-section {
  text-align: left;
  
  .form-label {
    font-weight: 600;
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
    margin-bottom: 0.5rem;
    display: block;
  }
  
  .form-select {
    width: 100%;
    border-radius: 0.75rem;
    border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
    background-color: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
    padding: 0.75rem;
    transition: border-color 0.2s ease, background-color 0.3s ease;
    
    &:focus {
      outline: none;
      border-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
      box-shadow: 0 0 0 0.2rem hsl(var(--primary-hue) var(--primary-saturation) var(--primary-lightness) / 0.1);
    }
  }
}

.new-chat-form textarea {
  width: 100%;
  border-radius: 0.75rem;
  border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  background-color: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
  color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  padding: 1rem;
  transition: border-color 0.2s ease, background-color 0.3s ease;
}

.new-chat-form textarea:focus {
  outline: none;
  border-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
  box-shadow: 0 0 0 0.2rem hsl(var(--primary-hue) var(--primary-saturation) var(--primary-lightness) / 0.1);
}

.new-chat-form button {
  padding: 0.75rem 2rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}
</style>
