<template>
  <div>
    <div v-if="isLoading" class="loading-screen">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <NuxtPage v-else />
  </div>
</template>

<script setup>
// Theme management
import { ref, onMounted, provide, readonly } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const api = useApi()
const router = useRouter()
const route = useRoute()

const isDark = ref(false)
const isLoading = ref(true)
const isAuthenticated = ref(false)

onMounted(async () => {
  // Check for saved theme preference or default to light mode
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    isDark.value = savedTheme === 'dark'
  } else {
    // Check system preference
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  applyTheme()

  // Check authentication status
  await checkAuthentication()
  
  isLoading.value = false
})

async function checkAuthentication() {
  const authPages = ['/login', '/register']
  const isAuthPage = authPages.includes(route.path)
  
  try {
    const authResult = await api.checkAuth()
    isAuthenticated.value = !!authResult
    
    if (isAuthenticated.value && isAuthPage) {
      // Redirect authenticated users away from auth pages
      await router.push('/')
    } else if (!isAuthenticated.value && !isAuthPage) {
      // Redirect unauthenticated users to login
      await router.push('/login')
    }
  } catch (error) {
    isAuthenticated.value = false
    if (!isAuthPage) {
      await router.push('/login')
    }
  }
}

function applyTheme() {
  document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

function toggleTheme() {
  isDark.value = !isDark.value
  applyTheme()
}

// Provide theme functions globally
provide('theme', {
  isDark: readonly(isDark),
  toggleTheme
})

// Provide auth state globally
provide('auth', {
  isAuthenticated: readonly(isAuthenticated),
  checkAuthentication
})
</script>

<style lang="scss">
@import '~/assets/scss/main.scss';

.loading-screen {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
}

.spinner-border {
  width: 3rem;
  height: 3rem;
  border: 0.25rem solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  border-right-color: transparent;
  border-radius: 50%;
  animation: spinner-border 0.75s linear infinite;
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
</style>
