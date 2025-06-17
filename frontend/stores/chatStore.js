import { reactive } from 'vue'
import { useApi } from '~/composables/useApi'

export const store = reactive({
  chats: [],
  models: [],
  systemPrompts: [],
  tools: [],
  
  async loadChats() {
    try {
      const api = useApi()
      this.chats = await api.getChats()
    } catch (error) {
      console.error('Failed to load chats:', error)
    }
  },

  async loadModels() {
    try {
      const api = useApi()
      this.models = await api.getModels()
    } catch (error) {
      console.error('Failed to load models:', error)
    }
  },

  async loadSystemPrompts() {
    try {
      const api = useApi()
      this.systemPrompts = await api.getSystemPrompts()
    } catch (error) {
      console.error('Failed to load system prompts:', error)
    }
  },

  async loadTools() {
    try {
      const api = useApi()
      this.tools = await api.getTools()
    } catch (error) {
      console.error('Failed to load tools:', error)
    }
  },

  // Helper to load all data at once
  async loadAll() {
    await Promise.all([
      this.loadChats(),
      this.loadModels(),
      this.loadSystemPrompts(),
      this.loadTools()
    ])
  }
})