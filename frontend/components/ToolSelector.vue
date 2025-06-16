<template>
  <div class="tool-selector">
    <label class="form-label">
      <i class="bi bi-tools me-2"></i>Tools (Optional)
    </label>
    <div class="tools-grid">
      <div 
        v-for="(tool, key) in availableTools" 
        :key="key" 
        class="tool-item"
      >
        <label class="tool-checkbox">
          <input 
            type="checkbox" 
            :value="key"
            :checked="selectedTools.includes(key)"
            @change="toggleTool(key, $event.target.checked)"
          >
          <span class="checkmark"></span>
          <span class="tool-name">{{ tool.name }}</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const availableTools = ref({})
const selectedTools = ref([...props.modelValue])

onMounted(async () => {
  await loadTools()
})

async function loadTools() {
  try {
    const api = useApi()
    const response = await api.getTools()
    availableTools.value = response
  } catch (error) {
    console.error('Failed to load tools:', error)
  }
}

function toggleTool(toolKey, checked) {
  if (checked) {
    if (!selectedTools.value.includes(toolKey)) {
      selectedTools.value.push(toolKey)
    }
  } else {
    const index = selectedTools.value.indexOf(toolKey)
    if (index > -1) {
      selectedTools.value.splice(index, 1)
    }
  }
  emit('update:modelValue', selectedTools.value)
}
</script>

<style lang="scss" scoped>
.tool-selector {
  .form-label {
    font-weight: 600;
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
    margin-bottom: 0.5rem;
    display: block;
  }
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.tool-item {
  background: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
  border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  border-radius: 0.5rem;
  padding: 0.75rem;
  transition: border-color 0.2s ease, background-color 0.3s ease;

  &:hover {
    border-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
  }
}

.tool-checkbox {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin: 0;
  
  input[type="checkbox"] {
    display: none;
  }

  .checkmark {
    width: 18px;
    height: 18px;
    border: 2px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
    border-radius: 3px;
    margin-right: 0.75rem;
    position: relative;
    transition: all 0.2s ease;
    flex-shrink: 0;

    &::after {
      content: '';
      position: absolute;
      display: none;
      left: 5px;
      top: 2px;
      width: 5px;
      height: 8px;
      border: solid white;
      border-width: 0 2px 2px 0;
      transform: rotate(45deg);
    }
  }

  input[type="checkbox"]:checked + .checkmark {
    background-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    border-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));

    &::after {
      display: block;
    }
  }

  .tool-name {
    color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
    font-size: 0.9rem;
    line-height: 1.4;
  }
}
</style>