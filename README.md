# BuildMart Backend

FastAPI backend for **M&P – Buy Materials. Book Workers. Build Faster.**

Structured following the Observability platform model (`jio-hcmp-deeptrace-bff` / `jio-hcmp-deeptrace`).

## Architecture

```
Frontend (buildmart UI)
        │
        ▼
┌─────────────────────────────────────────┐
│  bff/buildmart-bff          :8084       │
│  application/api_materials              │
│  application/api_workers                │
│  application/api_delivery               │
│  + bff/common (merged at Docker build)  │
└─────────────────────────────────────────┘
        │ fetch_get / fetch_post
        ▼
┌─────────────────────────────────────────┐
│  core/buildmart-materials   :8001       │
│  core/buildmart-workers     :8002       │
│  core/buildmart-delivery    :8003       │
│  + core/common (merged at Docker build) │
└─────────────────────────────────────────┘
```

## Project Structure

```
buildmart-backend/
├── bff/
│   ├── common/                    # Shared BFF code (like Observability/bff/common)
│   │   ├── middleware.py
│   │   ├── requirements.txt
│   │   └── utils/
│   └── buildmart-bff/             # Single BFF deployable (like jio-hcmp-deeptrace-bff)
│       ├── main.py
│       ├── start.sh
│       ├── Dockerfile
│       ├── buildmart-bff.yaml
│       ├── application/
│       │   ├── router.py
│       │   ├── api_materials/   # router → service → core
│       │   ├── api_workers/
│       │   └── api_delivery/
│       └── utils/properties.py
├── core/
│   ├── common/                    # Shared core code (like Observability/core/common)
│   ├── buildmart-materials/       # Core microservice
│   ├── buildmart-workers/
│   └── buildmart-delivery/
└── docker-compose.yml
```

## Per-service layering (Observability pattern)

```
v1.py / router.py     → HTTP routes + decorators
service.py            → Business logic
repository.py         → Data access (mock data for now)
schemas.py            → Pydantic models
main.py               → FastAPI app + router mounting
start.sh              → Gunicorn + UvicornWorker
Dockerfile            → Merges common/ at build time
```

## Quick Start

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| BFF Gateway | http://localhost:8084 |
| BFF Swagger | http://localhost:8084/docs |
| Materials Core | http://localhost:8001/buildmart-materials/health |
| Workers Core | http://localhost:8002/buildmart-workers/health |
| Delivery Core | http://localhost:8003/buildmart-delivery/health |

## BFF API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/buildmart-bff/materials_list_bff` | List materials |
| GET | `/buildmart-bff/material_detail_bff/{id}` | Material detail |
| GET | `/buildmart-bff/workers_list_bff` | List workers |
| GET | `/buildmart-bff/worker_detail_bff/{id}` | Worker detail |
| GET | `/buildmart-bff/delivery_options_bff` | Delivery options |
| POST | `/buildmart-bff/delivery_quote_bff` | Calculate delivery quote |
| GET | `/buildmart-bff/common/health` | BFF health check |

## Core API Endpoints

| Service | Endpoint |
|---------|----------|
| Materials | `/buildmart-materials/materials_list` |
| Workers | `/buildmart-workers/workers_list` |
| Delivery | `/buildmart-delivery/delivery_options` |

## Environment Variables (BFF)

| Variable | Default | Purpose |
|----------|---------|---------|
| `ip_port_materials` | `localhost:8001` | Materials core host:port |
| `ip_port_workers` | `localhost:8002` | Workers core host:port |
| `ip_port_delivery` | `localhost:8003` | Delivery core host:port |

## Repos

| Repo | Purpose |
|------|---------|
| [buildmart](https://github.com/sandeep8756/buildmart) | Frontend UI |
| [buildmart-backend](https://github.com/sandeep8756/buildmart-backend) | BFF + Core APIs |

## License

MIT
