<template>
  <div class="model-selector">
    <button 
      class="btn btn-outline-secondary model-trigger"
      @click="toggleModal"
    >
      <i class="bi bi-cpu me-2"></i>
      <span v-if="selectedModel">{{ getModelDisplayName(selectedModel) }}</span>
      <span v-else>Choose Model</span>
      <i class="bi bi-chevron-down ms-2"></i>
    </button>

    <!-- Modal Backdrop -->
    <div 
      v-if="isOpen" 
      class="modal-backdrop"
      @click="closeModal"
    ></div>

    <!-- Modal -->
    <div v-if="isOpen" class="model-modal">
      <div class="modal-header">
        <h5><i class="bi bi-cpu me-2"></i>Select Model</h5>
        <button class="btn-close" @click="closeModal">
          <i class="bi bi-x"></i>
        </button>
      </div>

      <div class="modal-body">
        <!-- Search -->
        <div class="search-box mb-3">
          <i class="bi bi-search"></i>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search models..."
            class="form-control"
          >
        </div>

        <!-- Provider Tabs -->
        <div class="provider-tabs mb-3">
          <button
            v-for="provider in filteredProviders"
            :key="provider.provider"
            class="provider-tab"
            :class="{ active: activeProvider === provider.provider }"
            @click="activeProvider = provider.provider"
          >
            <i :class="getProviderIcon(provider.provider)" class="me-2"></i>
            {{ provider.provider }}
            <span class="badge">{{ provider.models.length }}</span>
          </button>
        </div>

        <!-- Models List -->
        <div class="models-list">
          <div v-if="activeProviderModels.length === 0" class="empty-state">
            <i class="bi bi-search opacity-50"></i>
            <p class="text-muted mt-2 mb-0">No models found</p>
          </div>
          
          <div
            v-for="model in activeProviderModels"
            :key="model.id"
            class="model-item"
            :class="{ selected: selectedModel === model.id }"
            @click="selectModel(model)"
          >
            <div class="model-info">
              <div class="model-name">{{ model.name }}</div>
              <div class="model-description">{{ model.description }}</div>
            </div>
            <div class="model-actions">
              <i v-if="selectedModel === model.id" class="bi bi-check-circle-fill text-success"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  modelValue: String,
  providers: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const searchQuery = ref('')
const activeProvider = ref('dummy')
const selectedModel = ref(props.modelValue)

const filteredProviders = computed(() => {
  if (!searchQuery.value) return props.providers
  
  return props.providers.map(provider => ({
    ...provider,
    models: provider.models.filter(model => 
      model.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      model.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })).filter(provider => provider.models.length > 0)
})

const activeProviderModels = computed(() => {
  const provider = filteredProviders.value.find(p => p.provider === activeProvider.value)
  if (!provider) return []
  
  // If searching, return all matching models; otherwise limit to 20
  return searchQuery.value ? provider.models : provider.models.slice(0, 20)
})

onMounted(() => {
  if (props.providers.length > 0) {
    activeProvider.value = props.providers[0].provider
  }
})

function toggleModal() {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    searchQuery.value = ''
  }
}

function closeModal() {
  isOpen.value = false
  searchQuery.value = ''
}

function selectModel(model) {
  selectedModel.value = model.id
  emit('update:modelValue', model.id)
  closeModal()
}

function getModelDisplayName(modelId) {
  for (const provider of props.providers) {
    const model = provider.models.find(m => m.id === modelId)
    if (model) return model.name
  }
  return modelId
}

function getProviderIcon(provider) {
  const icons = {
    dummy: 'bi bi-gear',
    openai: 'bi bi-robot',
    openrouter: 'bi bi-router'
  }
  return icons[provider] || 'bi bi-cpu'
}
</script>

<style lang="scss" scoped>
.model-selector {
  position: relative;
}

.model-trigger {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  text-align: left;
  border-radius: 0.75rem;
  border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  background-color: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
  color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  padding: 0.75rem;
  transition: border-color 0.2s ease, background-color 0.3s ease;
  
  &:hover {
    border-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
  }
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1050;
}

.model-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  background: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
  border-radius: 1rem;
  border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  z-index: 1051;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  
  h5 {
    margin: 0;
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  }
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: hsl(var(--muted-foreground-hue), var(--muted-foreground-saturation), var(--muted-foreground-lightness));
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  
  &:hover {
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
    background: hsl(var(--muted-hue), var(--muted-saturation), var(--muted-lightness));
  }
}

.modal-body {
  padding: 1.5rem;
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.search-box {
  position: relative;
  
  i {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: hsl(var(--muted-foreground-hue), var(--muted-foreground-saturation), var(--muted-foreground-lightness));
  }
  
  .form-control {
    padding-left: 2.5rem;
    border-radius: 0.5rem;
    border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
    background-color: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
    
    &:focus {
      border-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
      box-shadow: 0 0 0 0.2rem hsl(var(--primary-hue) var(--primary-saturation) var(--primary-lightness) / 0.1);
      outline: none;
    }
  }
}

.provider-tabs {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.provider-tab {
  background: none;
  border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  color: hsl(var(--muted-foreground-hue), var(--muted-foreground-saturation), var(--muted-foreground-lightness));
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  .badge {
    background: hsl(var(--muted-hue), var(--muted-saturation), var(--muted-lightness));
    color: hsl(var(--muted-foreground-hue), var(--muted-foreground-saturation), var(--muted-foreground-lightness));
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
  }
  
  &.active {
    background: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    color: white;
    border-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    
    .badge {
      background: rgba(255, 255, 255, 0.2);
      color: white;
    }
  }
  
  &:hover:not(.active) {
    border-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  }
}

.models-list {
  flex: 1;
  overflow-y: auto;
  margin: -0.5rem;
  padding: 0.5rem;
  
  .empty-state {
    text-align: center;
    padding: 3rem 1rem;
    
    i {
      font-size: 3rem;
      color: hsl(var(--muted-foreground-hue), var(--muted-foreground-saturation), var(--muted-foreground-lightness));
    }
  }
}

.model-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border: 1px solid transparent;
  
  &:hover {
    background: hsl(var(--muted-hue), var(--muted-saturation), var(--muted-lightness));
  }
  
  &.selected {
    background: hsl(var(--primary-hue) var(--primary-saturation) var(--primary-lightness) / 0.1);
    border-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
  }
}

.model-info {
  flex: 1;
  
  .model-name {
    font-weight: 600;
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
    margin-bottom: 0.25rem;
  }
  
  .model-description {
    color: hsl(var(--muted-foreground-hue), var(--muted-foreground-saturation), var(--muted-foreground-lightness));
    font-size: 0.875rem;
    line-height: 1.4;
  }
}

.model-actions {
  flex-shrink: 0;
  margin-left: 1rem;
  
  i {
    font-size: 1.2rem;
  }
}

@media (max-width: 768px) {
  .model-modal {
    width: 95%;
    max-height: 90vh;
  }
  
  .modal-header, .modal-body {
    padding: 1rem;
  }
}
</style>