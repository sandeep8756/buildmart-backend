# BuildMart Backend

FastAPI microservices backend for **M&P – Buy Materials. Book Workers. Build Faster.**

## Architecture

```
Frontend (Next.js)
       │
       ▼
┌──────────────────────────────────────────────┐
│  BFF Layer                                   │
│  ├── gateway          :8080  (API Gateway)   │
│  ├── materials-bff    :8101                  │
│  ├── workers-bff      :8102                  │
│  └── delivery-bff     :8103                  │
└──────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│  Core Layer                                  │
│  ├── materials-service  :8001                │
│  ├── workers-service    :8002                │
│  └── delivery-service   :8003                │
└──────────────────────────────────────────────┘
```

## Project Structure

```
buildmart-backend/
├── bff/
│   ├── gateway/           # Single API entry point
│   ├── materials-bff/     # UI-optimized materials API
│   ├── workers-bff/       # UI-optimized workers API
│   └── delivery-bff/      # UI-optimized delivery API
├── core/
│   ├── materials-service/ # Materials business logic
│   ├── workers-service/   # Workers business logic
│   └── delivery-service/  # Delivery business logic
├── shared/                # Shared Pydantic models
└── docker-compose.yml
```

## Quick Start (Docker)

```bash
docker compose up --build
```

API Gateway: http://localhost:8080  
Swagger docs: http://localhost:8080/docs

## Quick Start (Local)

Run each service in a separate terminal:

```bash
# Core services
cd core/materials-service && pip install -r requirements.txt && uvicorn main:app --port 8001 --reload
cd core/workers-service  && pip install -r requirements.txt && uvicorn main:app --port 8002 --reload
cd core/delivery-service && pip install -r requirements.txt && uvicorn main:app --port 8003 --reload

# BFF services
cd bff/materials-bff && pip install -r requirements.txt && uvicorn main:app --port 8101 --reload
cd bff/workers-bff   && pip install -r requirements.txt && uvicorn main:app --port 8102 --reload
cd bff/delivery-bff  && pip install -r requirements.txt && uvicorn main:app --port 8103 --reload

# Gateway
cd bff/gateway && pip install -r requirements.txt && uvicorn main:app --port 8080 --reload
```

## API Endpoints (via Gateway)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/materials` | List materials (filter: category, search) |
| GET | `/api/v1/materials/{id}` | Get material by ID |
| GET | `/api/v1/workers` | List workers (filter: category, search, available) |
| GET | `/api/v1/workers/{id}` | Get worker by ID |
| GET | `/api/v1/delivery` | List delivery options |
| POST | `/api/v1/delivery/quote` | Calculate delivery price |
| GET | `/health` | Gateway + BFF health check |

## Example Requests

```bash
# List materials
curl http://localhost:8080/api/v1/materials

# Search workers
curl "http://localhost:8080/api/v1/workers?category=plumber&available=true"

# Delivery quote
curl -X POST http://localhost:8080/api/v1/delivery/quote \
  -H "Content-Type: application/json" \
  -d '{"optionId": "d1", "distanceKm": 10}'
```

## Tech Stack

- Python 3.11
- FastAPI
- Uvicorn
- HTTPX (BFF → Core communication)
- Docker & Docker Compose

## Repos

| Repo | Purpose |
|------|---------|
| [buildmart](https://github.com/sandeep8756/buildmart) | Frontend (Next.js UI) |
| [buildmart-backend](https://github.com/sandeep8756/buildmart-backend) | Backend (BFF + Core) |

## License

MIT
