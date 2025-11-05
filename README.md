# Agent Planner

An AI-powered project planning tool that transforms any project idea into a complete development roadmap with tasks, timelines, and technology recommendations.

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://agentplanner.web.app)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

Agent Planner uses a multi-agent AI system powered by Meta's Llama 3.3 70B to break down complex projects into actionable plans. Simply describe your project idea, and the system generates:

- Detailed task breakdowns
- Realistic timelines
- Task dependencies
- Technology stack recommendations
-  Implementation roadmap

**Try it live:** [agentplanner.web.app](https://agentplanner.web.app)

**Demo Video**

https://github.com/user-attachments/assets/5c19a127-adfb-4c29-92cd-aa526e017884

## Architecture

The system uses multiple specialized AI agents that work together:

- **Planner Agent**: Breaks down projects into tasks
- **Timeline Agent**: Estimates durations and schedules
- **Dependency Agent**: Identifies task relationships
- **Tech Stack Agent**: Recommends appropriate technologies
- **Formatter Agent**: Structures output for consistency

## Tech Stack

### Backend
- **FastAPI**: High-performance async API framework
- **SQLAlchemy**: ORM with async support for agent state management
- **LangChain**: Agent orchestration and LLM integration
- **Groq**: Fast inference with Llama 3.3 70B
- **Pydantic**: Data validation and settings management

### Frontend
- **React**: UI framework
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Styling

### Infrastructure
- **Google Cloud Run**: Containerized backend deployment
- **Firebase Hosting**: Frontend hosting
- **Docker**: Containerization

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- Groq API key ([Get one here](https://console.groq.com))

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional
EOF

# Run the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

## 📖 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints
```bash
POST /api/v1/projects/analyze
# Analyze a project description and generate a plan

GET /api/v1/projects/{project_id}
# Retrieve a saved project plan
```

## Example Usage
```bash
curl -X POST "http://localhost:8000/api/v1/projects/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Build a real-time chat application with user authentication",
    "timeline": "3 months",
    "team_size": 2
  }'
```

## Key Learnings

### Multi-Agent Orchestration
- Designed modular agents for specific reasoning tasks
- Implemented agent coordination for complex workflows
- Managed agent state and response synchronization

### Prompt Engineering
- Crafted prompts for consistent, structured outputs
- Handled LLM response variability
- Implemented retry logic for reliability

### Production Deployment
- Containerized applications with Docker
- Deployed to Cloud Run with proper health checks
- Implemented async patterns for scalability

## Challenges Overcome

1. **LangChain Version Conflicts**: Resolved cascading dependency conflicts across 15+ packages
2. **Cloud Run Port Issues**: Fixed containerization and port binding errors
3. **Model Deprecations**: Migrated from deprecated Groq models mid-project
4. **SQLAlchemy Async Patterns**: Implemented proper async ORM patterns
5. **Agent Desynchronization**: Fixed race conditions between timeline and planner agents
6. **Memory Leaks**: Resolved orchestrator memory issues causing crashes after ~50 requests
7. **Stateless Architecture**: Implemented temporary file storage for SQLite persistence
8. **Circular Dependencies**: Added detection to prevent infinite loops in dependency analysis

## Project Structure
```
agentplanner/
├── backend/
│   ├── app/
│   │   ├── agents/          # AI agent implementations
│   │   ├── api/             # API routes
│   │   ├── core/            # Configuration
│   │   ├── models/          # Database models
│   │   ├── services/        # Business logic
│   │   └── main.py          # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API client
│   │   └── types/           # TypeScript types
│   └── package.json
└── README.md
```

## Configuration

### Environment Variables

**Backend** (`backend/.env`):
```env
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional
DEBUG=True
```

**Frontend** (`frontend/.env`):
```env
REACT_APP_API_URL=http://localhost:8000
```

## Deployment

### Backend (Cloud Run)
```bash
cd backend

# Build and deploy
gcloud run deploy agentplanner \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Frontend (Firebase)
```bash
cd frontend

# Build
npm run build

# Deploy
firebase deploy
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built as part of an LLMs course project
- Powered by Meta's Llama 3.3 70B via Groq
- Inspired by the need for AI-assisted project planning

## Contact

Built by [Abhisek](https://github.com/abhisek-ai)

Project Link: [https://github.com/abhisek-ai/agent-planner](https://github.com/abhisek-ai/agent-planner)
