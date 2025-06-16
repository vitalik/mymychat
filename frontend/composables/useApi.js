class Api {
  constructor(baseURL) {
    this.baseURL = baseURL
  }

  getAuthHeaders() {
    const token = localStorage.getItem('auth_token')
    if (token) {
      return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    }
    return {
      'Content-Type': 'application/json'
    }
  }

  async settings() {
    const resp = await fetch(`${this.baseURL}/settings`, {
        method: 'GET',
        headers: this.getAuthHeaders(),
    })
    return await resp.json()
  }

  async getChats() {
    const resp = await fetch(`${this.baseURL}/chats`, {
        method: 'GET',
        headers: this.getAuthHeaders(),
    })
    return await resp.json()
  }

  async createChat(data) {
    const resp = await fetch(`${this.baseURL}/chats`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(data)
    })
    return await resp.json()
  }

  async getChat(uid) {
    const resp = await fetch(`${this.baseURL}/chats/${uid}`, {
        method: 'GET',
        headers: this.getAuthHeaders(),
    })
    return await resp.json()
  }

  async createPrompt(chatUid, data) {
    const resp = await fetch(`${this.baseURL}/chats/${chatUid}/prompts`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(data)
    })
    return await resp.json()
  }

  async getModels() {
    const resp = await fetch(`${this.baseURL}/models`, {
        method: 'GET',
        headers: this.getAuthHeaders(),
    })
    return await resp.json()
  }

  async login(email, password) {
    const resp = await fetch(`${this.baseURL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    const data = await resp.json()
    if (resp.ok) {
      localStorage.setItem('auth_token', data.token)
    }
    return data
  }

  async register(email, password) {
    const resp = await fetch(`${this.baseURL}/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    const data = await resp.json()
    if (resp.ok) {
      localStorage.setItem('auth_token', data.token)
    }
    return data
  }

  async checkAuth() {
    try {
      const resp = await fetch(`${this.baseURL}/auth/check`, {
          method: 'GET',
          headers: this.getAuthHeaders(),
      })
      if (resp.ok) {
        return await resp.json()
      }
      return null
    } catch (error) {
      return null
    }
  }

  async shareChat(chatUid) {
    const resp = await fetch(`${this.baseURL}/chats/${chatUid}/share`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
    })
    return await resp.json()
  }

  async getSharedChat(uid) {
    const resp = await fetch(`${this.baseURL}/chats/${uid}/shared`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    return await resp.json()
  }

  async getProfile() {
    const resp = await fetch(`${this.baseURL}/profile`, {
        method: 'GET',
        headers: this.getAuthHeaders(),
    })
    return await resp.json()
  }

  async updateProfile(data) {
    const resp = await fetch(`${this.baseURL}/profile`, {
        method: 'PATCH',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(data)
    })
    return await resp.json()
  }

  async getSystemPrompts() {
    const resp = await fetch(`${this.baseURL}/system-prompts`, {
        method: 'GET',
        headers: this.getAuthHeaders(),
    })
    return await resp.json()
  }

  async createSystemPrompt(data) {
    const resp = await fetch(`${this.baseURL}/system-prompts`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(data)
    })
    return await resp.json()
  }

  async updateSystemPrompt(id, data) {
    const resp = await fetch(`${this.baseURL}/system-prompts/${id}`, {
        method: 'PUT',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(data)
    })
    return await resp.json()
  }

  async deleteSystemPrompt(id) {
    const resp = await fetch(`${this.baseURL}/system-prompts/${id}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders(),
    })
    return await resp.json()
  }

  logout() {
    localStorage.removeItem('auth_token')
  }
}

const api = new Api('/api')

export const useApi = () => {
  return api
}
