# CKICAS Drought Monitor

A Constitutional AI system for drought monitoring following Yama principles (Ahimsa, Satya, Asteya, Brahmacharya, Aparigraha).

## Features

- **Constitutional AI Framework**: Built on ethical AI principles
- **Drought Monitoring Dashboard**: Real-time drought monitoring interface
- **AI Chatbot Assistant**: Integrated Claude-powered assistant for system guidance
- **Modern Web Interface**: React-based dashboard with Tailwind CSS

## Architecture

- **Backend**: FastAPI (Python) with async support
- **Frontend**: React + Vite with Tailwind CSS
- **Database**: SQLite with SQLAlchemy
- **AI**: Anthropic Claude integration (demo mode available)

## Deployment

This project is configured for easy deployment on Render.

### Quick Deploy to Render

1. Fork or clone this repository to GitHub
2. Connect your GitHub account to Render
3. Create a new Web Service from this repository
4. Render will automatically detect the `render.yaml` configuration
5. Set environment variables if needed (ANTHROPIC_API_KEY for full AI features)

### Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (in separate terminal)
cd frontend
npm install
npm run dev
```

## Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key (optional - runs in demo mode without it)
- `PORT`: Automatically set by Render

## API Endpoints

- `GET /health` - Health check
- `GET /api/admin/health` - Admin health check
- `GET /api/admin/chat/health` - Chatbot health check
- `POST /api/admin/chat` - Chat with AI assistant

## License

This project follows Constitutional AI principles and is designed for ethical AI deployment.