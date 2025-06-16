<template>
  <div class="settings-layout">
    <div class="settings-container">
      <div class="settings-header">
        <h2><i class="bi bi-gear-fill me-2"></i>Settings</h2>
        <nuxt-link to="/" class="btn btn-outline-secondary">
          <i class="bi bi-arrow-left me-2"></i>Back to Chat
        </nuxt-link>
      </div>

      <div class="settings-content">
        <!-- API Keys Section -->
        <div class="settings-section">
          <h4><i class="bi bi-key-fill me-2"></i>API Keys</h4>
          <p class="text-muted">Configure your API keys to use different AI providers.</p>
          
          <div class="api-keys-form">
            <div class="mb-3">
              <label for="openai-key" class="form-label">
                <i class="bi bi-openai me-2"></i>OpenAI API Key
              </label>
              <div class="input-group">
                <input
                  id="openai-key"
                  v-model="apiKeys.openai_key"
                  type="password"
                  class="form-control"
                  placeholder="sk-..."
                >
                <button 
                  class="btn btn-outline-secondary"
                  type="button"
                  @click="toggleKeyVisibility('openai')"
                >
                  <i :class="showKeys.openai ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
              <div class="form-text">
                <span v-if="profile.openai_key_set" class="text-success">
                  <i class="bi bi-check-circle me-1"></i>API key configured
                </span>
                <span v-else class="text-muted">No API key configured</span>
              </div>
            </div>

            <div class="mb-3">
              <label for="openrouter-key" class="form-label">
                <i class="bi bi-router me-2"></i>OpenRouter API Key
              </label>
              <div class="input-group">
                <input
                  id="openrouter-key"
                  v-model="apiKeys.openrouter_key"
                  type="password"
                  class="form-control"
                  placeholder="sk-or-..."
                >
                <button 
                  class="btn btn-outline-secondary"
                  type="button"
                  @click="toggleKeyVisibility('openrouter')"
                >
                  <i :class="showKeys.openrouter ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
              <div class="form-text">
                <span v-if="profile.openrouter_key_set" class="text-success">
                  <i class="bi bi-check-circle me-1"></i>API key configured
                </span>
                <span v-else class="text-muted">No API key configured</span>
              </div>
            </div>

            <button 
              class="btn btn-primary"
              @click="saveApiKeys"
              :disabled="isSaving"
            >
              <i class="bi bi-save me-2"></i>
              {{ isSaving ? 'Saving...' : 'Save API Keys' }}
            </button>
          </div>
        </div>

        <!-- System Prompts Section -->
        <div class="settings-section">
          <h4><i class="bi bi-chat-quote-fill me-2"></i>System Prompts</h4>
          <p class="text-muted">Create reusable system prompts for your conversations.</p>
          
          <div class="system-prompts-form">
            <div class="mb-3">
              <label for="new-prompt" class="form-label">New System Prompt</label>
              <textarea
                id="new-prompt"
                v-model="newPromptText"
                class="form-control"
                rows="3"
                placeholder="Enter your system prompt..."
              ></textarea>
            </div>
            
            <button 
              class="btn btn-success mb-4"
              @click="createSystemPrompt"
              :disabled="!newPromptText.trim() || isCreating"
            >
              <i class="bi bi-plus-lg me-2"></i>
              {{ isCreating ? 'Creating...' : 'Create Prompt' }}
            </button>

            <div class="system-prompts-list">
              <div v-if="systemPrompts.length === 0" class="empty-state">
                <i class="bi bi-chat-quote opacity-50"></i>
                <p class="text-muted mt-2 mb-0">No system prompts yet</p>
              </div>
              
              <div 
                v-for="prompt in systemPrompts" 
                :key="prompt.id"
                class="prompt-item"
              >
                <div v-if="editingPrompt === prompt.id" class="prompt-edit">
                  <textarea
                    v-model="editText"
                    class="form-control mb-2"
                    rows="3"
                  ></textarea>
                  <div class="prompt-actions">
                    <button 
                      class="btn btn-sm btn-success me-2"
                      @click="savePrompt(prompt.id)"
                      :disabled="isUpdating"
                    >
                      <i class="bi bi-check"></i>
                    </button>
                    <button 
                      class="btn btn-sm btn-secondary"
                      @click="cancelEdit"
                    >
                      <i class="bi bi-x"></i>
                    </button>
                  </div>
                </div>
                
                <div v-else class="prompt-view">
                  <div class="prompt-text">{{ prompt.text }}</div>
                  <div class="prompt-meta">
                    <small class="text-muted">{{ formatDate(prompt.created_at) }}</small>
                  </div>
                  <div class="prompt-actions">
                    <button 
                      class="btn btn-sm btn-outline-primary me-2"
                      @click="startEdit(prompt)"
                    >
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button 
                      class="btn btn-sm btn-outline-danger"
                      @click="deletePrompt(prompt.id)"
                      :disabled="isDeleting"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const { $toast } = useNuxtApp()
const api = useApi()

// API Keys
const profile = ref({
  openai_key_set: false,
  openrouter_key_set: false
})
const apiKeys = ref({
  openai_key: '',
  openrouter_key: ''
})
const showKeys = ref({
  openai: false,
  openrouter: false
})
const isSaving = ref(false)

// System Prompts
const systemPrompts = ref([])
const newPromptText = ref('')
const editingPrompt = ref(null)
const editText = ref('')
const isCreating = ref(false)
const isUpdating = ref(false)
const isDeleting = ref(false)

onMounted(() => {
  loadProfile()
  loadSystemPrompts()
})

async function loadProfile() {
  try {
    const response = await api.getProfile()
    profile.value = response
  } catch (error) {
    $toast.error('Failed to load profile')
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

async function saveApiKeys() {
  isSaving.value = true
  try {
    const response = await api.updateProfile(apiKeys.value)
    profile.value = response
    $toast.success('API keys saved successfully')
  } catch (error) {
    $toast.error('Failed to save API keys')
  } finally {
    isSaving.value = false
  }
}

function toggleKeyVisibility(provider) {
  showKeys.value[provider] = !showKeys.value[provider]
  const input = document.getElementById(`${provider}-key`)
  input.type = showKeys.value[provider] ? 'text' : 'password'
}

async function createSystemPrompt() {
  if (!newPromptText.value.trim()) return
  
  isCreating.value = true
  try {
    const response = await api.createSystemPrompt({ text: newPromptText.value })
    systemPrompts.value.unshift(response)
    newPromptText.value = ''
    $toast.success('System prompt created')
  } catch (error) {
    $toast.error('Failed to create system prompt')
  } finally {
    isCreating.value = false
  }
}

function startEdit(prompt) {
  editingPrompt.value = prompt.id
  editText.value = prompt.text
}

function cancelEdit() {
  editingPrompt.value = null
  editText.value = ''
}

async function savePrompt(id) {
  isUpdating.value = true
  try {
    const response = await api.updateSystemPrompt(id, { text: editText.value })
    const index = systemPrompts.value.findIndex(p => p.id === id)
    if (index !== -1) {
      systemPrompts.value[index] = response
    }
    editingPrompt.value = null
    editText.value = ''
    $toast.success('System prompt updated')
  } catch (error) {
    $toast.error('Failed to update system prompt')
  } finally {
    isUpdating.value = false
  }
}

async function deletePrompt(id) {
  if (!confirm('Are you sure you want to delete this system prompt?')) return
  
  isDeleting.value = true
  try {
    await api.deleteSystemPrompt(id)
    systemPrompts.value = systemPrompts.value.filter(p => p.id !== id)
    $toast.success('System prompt deleted')
  } catch (error) {
    $toast.error('Failed to delete system prompt')
  } finally {
    isDeleting.value = false
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString()
}
</script>

<style lang="scss" scoped>
.settings-layout {
  min-height: 100vh;
  background: hsl(var(--chat-bg-hue), var(--chat-bg-saturation), var(--chat-bg-lightness));
  padding: 2rem 1rem;
}

.settings-container {
  max-width: 800px;
  margin: 0 auto;
}

.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  
  h2 {
    margin: 0;
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  }
}

.settings-content {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.settings-section {
  background: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
  border-radius: 1rem;
  padding: 2rem;
  border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  
  h4 {
    margin-bottom: 0.5rem;
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  }
  
  > p {
    margin-bottom: 1.5rem;
  }
}

.api-keys-form, .system-prompts-form {
  .form-label {
    font-weight: 600;
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  }
  
  .form-control {
    border-radius: 0.5rem;
    border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
    background-color: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
    
    &:focus {
      border-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
      box-shadow: 0 0 0 0.2rem hsl(var(--primary-hue) var(--primary-saturation) var(--primary-lightness) / 0.1);
    }
  }
}

.system-prompts-list {
  .empty-state {
    text-align: center;
    padding: 3rem 1rem;
    
    i {
      font-size: 3rem;
      color: hsl(var(--muted-foreground-hue), var(--muted-foreground-saturation), var(--muted-foreground-lightness));
    }
  }
}

.prompt-item {
  background: hsl(var(--muted-hue), var(--muted-saturation), var(--muted-lightness));
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 1rem;
  border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  
  &:last-child {
    margin-bottom: 0;
  }
}

.prompt-view {
  .prompt-text {
    white-space: pre-wrap;
    margin-bottom: 1rem;
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  }
  
  .prompt-meta {
    margin-bottom: 1rem;
  }
  
  .prompt-actions {
    display: flex;
    gap: 0.5rem;
  }
}

.prompt-edit {
  .prompt-actions {
    display: flex;
    gap: 0.5rem;
  }
}

@media (max-width: 768px) {
  .settings-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .settings-section {
    padding: 1.5rem;
  }
}
</style>