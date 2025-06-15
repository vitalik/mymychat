<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="auth-title">Sign Up</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            class="form-control"
            required
            :disabled="isLoading"
          >
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            class="form-control"
            required
            :disabled="isLoading"
          >
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            class="form-control"
            required
            :disabled="isLoading"
          >
        </div>
        <button type="submit" class="btn btn-primary w-100" :disabled="isLoading">
          <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
          Sign Up
        </button>
      </form>
      <p class="auth-link">
        Already have an account? <NuxtLink to="/login">Sign in</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const api = useApi()
const router = useRouter()

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const isLoading = ref(false)

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    alert('Passwords do not match')
    return
  }
  
  isLoading.value = true
  try {
    const result = await api.register(email.value, password.value)
    if (result.token) {
      // Redirect to home page on successful registration
      await router.push('/')
    } else {
      // Handle registration error
      console.error('Registration failed:', result.error)
      alert(result.error || 'Registration failed')
    }
  } catch (error) {
    console.error('Registration error:', error)
    alert('An error occurred during registration')
  } finally {
    isLoading.value = false
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/scss/variables';

.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
  padding: 1rem;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  background: hsl(var(--background-hue), var(--background-saturation), calc(var(--background-lightness) + 5%));
  border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  border-radius: 0.5rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.auth-title {
  text-align: center;
  margin-bottom: 1.5rem;
  color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  font-size: 1.5rem;
  font-weight: 600;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid hsl(var(--border-hue), var(--border-saturation), var(--border-lightness));
  border-radius: 0.375rem;
  background: hsl(var(--background-hue), var(--background-saturation), var(--background-lightness));
  color: hsl(var(--foreground-hue), var(--foreground-saturation), var(--foreground-lightness));
  font-size: 0.875rem;
  
  &:focus {
    outline: none;
    border-color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    box-shadow: 0 0 0 2px hsl(var(--primary-hue), var(--primary-saturation), calc(var(--primary-lightness) + 20%));
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  
  &.btn-primary {
    background: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    color: white;
    
    &:hover:not(:disabled) {
      background: hsl(var(--primary-hue), var(--primary-saturation), calc(var(--primary-lightness) - 5%));
    }
    
    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }
  
  &.w-100 {
    width: 100%;
  }
}

.auth-link {
  text-align: center;
  margin-top: 1.5rem;
  color: hsl(var(--foreground-hue), var(--foreground-saturation), calc(var(--foreground-lightness) + 20%));
  font-size: 0.875rem;
  
  a {
    color: hsl(var(--primary-hue), var(--primary-saturation), var(--primary-lightness));
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
}
</style>