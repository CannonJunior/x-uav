# X-UAV: UAV Comparison Platform

Advanced web application for comparing unmanned aerial vehicles with graph-based visualization, mission-centric analysis, and variant-level comparisons.

## Key Features

- **Mission-Centric Comparison**: Analyze UAVs by mission type (ISR, Strike, EW, etc.)
- **Variant-Level Analysis**: Compare platform families and mission-specific configurations
- **Graph Visualization**: Interactive network visualization of UAV relationships
- **Agent-Native Architecture**: Ollama-powered LLM interface with MCP tools
- **Zero-Cost Deployment**: Runs entirely on localhost with open-source stack

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.11+ with `uv` (for local backend development)

### Running with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Access Points

- **Frontend**: http://localhost:7676
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ArangoDB UI**: http://localhost:8529 (username: root, password: development)

### Local Development

#### Backend

```bash
cd backend

# Install dependencies
uv pip install -e ".[dev]"

# Run development server
uv run uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## Project Structure

```
x-uav/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Configuration
│   │   ├── db/       # Database connections
│   │   ├── models/   # Data models
│   │   ├── schemas/  # Pydantic schemas
│   │   └── services/ # Business logic
│   └── pyproject.toml
├── frontend/          # Vue.js frontend
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── services/
│   │   └── assets/
│   └── package.json
├── docker/           # Docker configurations
├── data/             # Persistent data volumes
├── tests/            # Test suites
└── docs/             # Documentation

```

## Technology Stack

### Frontend
- Vue.js 3 with Composition API
- Vite build tool
- Cytoscape.js (graph visualization)
- ECharts (charts and data visualization)
- Axios (HTTP client)

### Backend
- FastAPI (Python web framework)
- Pydantic (data validation)
- SQLAlchemy (ORM for PostgreSQL)
- python-arango (ArangoDB client)

### Databases
- **ArangoDB**: Graph database for UAV relationships
- **PostgreSQL**: Relational data (users, alerts)
- **Redis**: Caching and real-time features

### AI/ML
- **Ollama**: Local LLM deployment
- **MCP**: Model Context Protocol for agent tools

## Development Roadmap

### Phase 1: Foundation ✅ (Current)
- [x] Project setup and Docker configuration
- [x] ArangoDB integration
- [x] FastAPI backend skeleton
- [x] Vue.js frontend skeleton
- [x] Basic health check endpoints

### Phase 2: Data Model and Ontology
- [ ] Complete JSON-LD schema
- [ ] Graph database schema implementation
- [ ] Data import pipeline
- [ ] Sample CCA platform data

### Phase 3: Core API and Search
- [ ] UAV CRUD endpoints
- [ ] Advanced search functionality
- [ ] Graph traversal endpoints
- [ ] API testing suite

### Phase 4: Frontend Comparison UI
- [ ] UAV listing and search
- [ ] Side-by-side comparison table
- [ ] Filtering and sorting
- [ ] Responsive design

### Phase 5: Graph Visualization
- [ ] Cytoscape.js integration
- [ ] Interactive graph exploration
- [ ] Layout algorithms
- [ ] Node/edge filtering

### Phase 6: Ollama and MCP Integration
- [ ] Ollama service setup
- [ ] MCP server implementation
- [ ] Chat interface
- [ ] Natural language queries

### Phase 7-10: Advanced Features
- See [PROJECT-PLAN.md](PROJECT-PLAN.md) for full roadmap

## Contributing

This is an open-source project. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Data Sources

All UAV data is sourced from publicly available information:
- The War Zone (www.twz.com)
- Wikipedia
- Government fact sheets and procurement documents
- Defense industry publications

## License

Open source - see LICENSE file for details.

## Acknowledgments

- Inspired by the need for comprehensive UAV comparison tools
- Built with modern web technologies and zero-cost principles
- Focuses on transparency and verifiable data sources

---

**Project Status**: Phase 1 Complete - Foundation Established

For detailed implementation plan, see [PROJECT-PLAN.md](PROJECT-PLAN.md)
