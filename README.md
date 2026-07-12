# BuildMart Backend

FastAPI backend for **M&P – Buy Materials. Book Workers. Build Faster.**

Structured following the Observability platform model — **separate BFF microservices** under `bff/` (like `jio-hcmp-deeptrace-topology-bff`, `jio-hcmp-deeptrace-onboarding-bff`).

## Architecture

```
Frontend (buildmart UI)
        │
        ├──────────────────┬──────────────────┐
        ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ materials-bff   │ │ workers-bff     │ │ delivery-bff    │
│     :8101       │ │     :8102       │ │     :8103       │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ materials core  │ │ workers core    │ │ delivery core   │
│     :8001       │ │     :8002       │ │     :8003       │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## Project Structure

```
buildmart-backend/
├── bff/
│   ├── common/                         # Shared BFF code (like Observability/bff/common)
│   ├── buildmart-materials-bff/        # Separate BFF microservice
│   ├── buildmart-workers-bff/          # Separate BFF microservice
│   └── buildmart-delivery-bff/         # Separate BFF microservice
└── core/
    ├── common/                         # Shared core code
    ├── buildmart-materials/            # Core microservice
    ├── buildmart-workers/
    └── buildmart-delivery/
```

## Observability model mapping

| Observability | BuildMart |
|---------------|-----------|
| `bff/jio-hcmp-deeptrace-topology-bff` | `bff/buildmart-materials-bff` |
| `bff/jio-hcmp-deeptrace-onboarding-bff` | `bff/buildmart-workers-bff` |
| `bff/common/` | `bff/common/` |
| `core/jio-hcmp-deeptrace` | `core/buildmart-materials` (sibling cores) |

## Each BFF microservice structure

```
buildmart-materials-bff/
├── main.py                 # FastAPI app + router mount
├── start.sh                # Gunicorn + UvicornWorker
├── Dockerfile              # Merges bff/common at build
├── buildmart-materials-bff.yaml
├── utils/properties.py     # ip_port → core service
└── application/api/
    ├── v1.py               # Routes (_bff suffix)
    ├── service.py          # fetch_get/fetch_post to core
    └── schemas.py          # Pydantic models
```

## Quick Start

```bash
docker compose up --build
```

| Service | Port | Swagger |
|---------|------|---------|
| Materials BFF | 8101 | http://localhost:8101/docs |
| Workers BFF | 8102 | http://localhost:8102/docs |
| Delivery BFF | 8103 | http://localhost:8103/docs |
| Materials Core | 8001 | http://localhost:8001/docs |
| Workers Core | 8002 | http://localhost:8002/docs |
| Delivery Core | 8003 | http://localhost:8003/docs |

## BFF API Endpoints

| BFF Service | Endpoint |
|-------------|----------|
| materials-bff | `GET /buildmart-materials-bff/materials_list_bff` |
| materials-bff | `GET /buildmart-materials-bff/material_detail_bff/{id}` |
| workers-bff | `GET /buildmart-workers-bff/workers_list_bff` |
| workers-bff | `GET /buildmart-workers-bff/worker_detail_bff/{id}` |
| delivery-bff | `GET /buildmart-delivery-bff/delivery_options_bff` |
| delivery-bff | `POST /buildmart-delivery-bff/delivery_quote_bff` |

## Environment Variables

Each BFF uses `ip_port` to reach its core (same as Observability):

| BFF | `ip_port` default | Core |
|-----|-------------------|------|
| materials-bff | `localhost:8001` | buildmart-materials |
| workers-bff | `localhost:8002` | buildmart-workers |
| delivery-bff | `localhost:8003` | buildmart-delivery |

## Repos

| Repo | Purpose |
|------|---------|
| [buildmart](https://github.com/sandeep8756/buildmart) | Frontend UI |
| [buildmart-backend](https://github.com/sandeep8756/buildmart-backend) | BFF + Core APIs |

## License

MIT
