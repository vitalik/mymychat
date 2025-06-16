# MyMyChat 💬

> A modern, feature-rich ChatGPT clone built for the [T3 Chat Cloneathon](https://cloneathon.t3.chat/) competition.

## 🚀 Live Demo

[Add your deployed URL here]


## ✨ Features
- [x] **🤖 Chat with Various LLMs** - Support for multiple language models and providers
- [x] **🎨 Syntax Highlighting** - Beautiful code formatting and highlighting
- [x] **🔄 Resumable Streams** - Continue generation after page refresh
- [x] **🔗 Chat Sharing** - Share conversations with others
- [x] **🔑 Bring Your Own Key** - Use your own API keys
- [x] **🔍 Web Search** - Integrate real-time web search
- [x] **📎 Attachment Support** - Allow users to upload files (images and pdfs)
- [ ] **🛠️ Custom tools** - Bring your own tools
- [ ] **🌳 Chat Branching** - Create alternative conversation paths
- [ ] **🖼️ Image Generation Support** - AI-powered image generation capabilities



## 🏃‍♂️ Quick Start

[ TODO ]


### Stack
- **Django / Django Ninja**
- **Redis**
- **Nuxt 3**
- **Vue 3**
- **Bootstrap 5**
- **Server-Sent Events**




## Development

### Prerequisites
- Python 3.12+
- Node.js 22+
- Redis server

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### Frontend Setup
```bash
cd frontend
npm install
```

### Running the Application
```bash
# Terminal 1: Backend API
cd backend
uvicorn asgi:application --reload

# Terminal 2: LLM Worker
cd backend
python manage.py worker_llm

# Terminal 3: Frontend
cd frontend
npm run dev
```

Visit `http://localhost:3000` to start chatting!

## 📱 Screenshots

[Add screenshots of your application here]



## 🤝 Contributing

This is a competition entry, but contributions and feedback are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

