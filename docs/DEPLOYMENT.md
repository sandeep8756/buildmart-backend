# M&P Backend — Kubernetes Deployment

Deploy BFF + Core microservices to a **personal** Kubernetes cluster.

**Automated:** Push to `main` triggers GitHub Actions → build 6 images → push to `ghcr.io` → optional K8s deploy.

> Do **not** use office `kube_config_sitazure.yaml`. Use your own cluster kubeconfig.

---

## GitHub Actions (automatic build & release)

Every push to `main` on `sandeep8756/buildmart-backend`:

1. **Build and Release** workflow builds all 6 microservices
2. Pushes images to `ghcr.io/sandeep8756/<service>:latest` and `:sha`
3. **Deploy to Kubernetes** runs after (if `KUBE_CONFIG_DATA` secret is set)

**View runs:** GitHub repo → **Actions** tab

**Images published:**
```
ghcr.io/sandeep8756/buildmart-materials
ghcr.io/sandeep8756/buildmart-workers
ghcr.io/sandeep8756/buildmart-delivery
ghcr.io/sandeep8756/buildmart-materials-bff
ghcr.io/sandeep8756/buildmart-workers-bff
ghcr.io/sandeep8756/buildmart-delivery-bff
```

### Enable auto-deploy to K8s (one-time)

**Deploy from GitHub only — no local laptop needed.**

Add these secrets in **Settings → Secrets → Actions**:

| Secret | Value |
|--------|-------|
| `OCI_TENANCY_OCID` | From OCI API key config |
| `OCI_USER_OCID` | From OCI API key config |
| `OCI_FINGERPRINT` | From OCI API key config |
| `OCI_API_KEY` | Private key `.pem` file content |
| `OCI_REGION` | `ap-mumbai-1` |
| `OCI_CLUSTER_OCID` | `buildmart-oke` cluster ID |

Full guide: [docs/GITHUB-OCI-DEPLOY.md](docs/GITHUB-OCI-DEPLOY.md)

Then: **Actions → Deploy to Kubernetes → Run workflow**

---

## Architecture in K8s

```
Internet
   │
   ▼
Ingress (HTTPS)  api.yourdomain.com
   │
   ├── /buildmart-materials-bff  →  materials-bff pod  →  materials core pod
   ├── /buildmart-workers-bff    →  workers-bff pod    →  workers core pod
   └── /buildmart-delivery-bff   →  delivery-bff pod   →  delivery core pod

Core pods: ClusterIP only (not exposed to internet)
BFF pods:  exposed via Ingress
```

| Microservice | Image | K8s Service | Port | Public? |
|--------------|-------|-------------|------|---------|
| buildmart-materials | `REGISTRY/buildmart-materials:TAG` | buildmart-materials | 8001 | No |
| buildmart-workers | `REGISTRY/buildmart-workers:TAG` | buildmart-workers | 8002 | No |
| buildmart-delivery | `REGISTRY/buildmart-delivery:TAG` | buildmart-delivery | 8003 | No |
| buildmart-materials-bff | `REGISTRY/buildmart-materials-bff:TAG` | buildmart-materials-bff | 8101 | Yes (Ingress) |
| buildmart-workers-bff | `REGISTRY/buildmart-workers-bff:TAG` | buildmart-workers-bff | 8102 | Yes (Ingress) |
| buildmart-delivery-bff | `REGISTRY/buildmart-delivery-bff:TAG` | buildmart-delivery-bff | 8103 | Yes (Ingress) |

---

## Prerequisites

1. **Personal K8s cluster** (pick one):
   - [Minikube](https://minikube.sigs.k8s.io/) (local dev)
   - [kind](https://kind.sigs.k8s.io/) (local dev)
   - DigitalOcean Kubernetes / Linode LKE / Civo (cheap cloud)
   - Personal Azure/AWS account (not office cluster)

2. **kubectl** configured:
   ```bash
   kubectl cluster-info
   ```

3. **Docker** installed

4. **Container registry** (free options):
   - GitHub Container Registry: `ghcr.io/sandeep8756`
   - Docker Hub: `docker.io/sandeep8756`

5. **NGINX Ingress Controller** on cluster:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.3/deploy/static/provider/cloud/deploy.yaml
   ```

---

## Step 1 — Build microservices (Docker images)

Builds all 6 images from their Dockerfiles (merges `common/` at build time).

```bash
cd buildmart-backend

# Default: ghcr.io/sandeep8756, tag latest
./scripts/build-images.sh

# Or with custom registry/tag
REGISTRY=ghcr.io/sandeep8756 TAG=v1.0.0 ./scripts/build-images.sh
```

**What happens:**
```
core/buildmart-materials/Dockerfile   →  ghcr.io/sandeep8756/buildmart-materials:TAG
core/buildmart-workers/Dockerfile     →  ghcr.io/sandeep8756/buildmart-workers:TAG
core/buildmart-delivery/Dockerfile    →  ghcr.io/sandeep8756/buildmart-delivery:TAG
bff/buildmart-materials-bff/Dockerfile → ghcr.io/sandeep8756/buildmart-materials-bff:TAG
bff/buildmart-workers-bff/Dockerfile   → ghcr.io/sandeep8756/buildmart-workers-bff:TAG
bff/buildmart-delivery-bff/Dockerfile  → ghcr.io/sandeep8756/buildmart-delivery-bff:TAG
```

---

## Step 2 — Release (push images to registry)

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u sandeep8756 --password-stdin

# Push all 6 images
./scripts/push-images.sh

# Or with tag
REGISTRY=ghcr.io/sandeep8756 TAG=v1.0.0 ./scripts/push-images.sh
```

---

## Step 3 — Deploy pods to Kubernetes

Deploy order: **namespace → Core pods → BFF pods → Ingress**

```bash
# Set your API hostname (Ingress host)
export REGISTRY=ghcr.io/sandeep8756
export TAG=v1.0.0
export API_HOST=api.yourdomain.com

# Use YOUR personal kubeconfig (not office)
export KUBECONFIG=~/.kube/config

./scripts/deploy-k8s.sh
```

**What happens:**
1. Renders manifests with your `REGISTRY`, `TAG`, `API_HOST`
2. Creates namespace `buildmart`
3. Starts 3 **Core** Deployments + ClusterIP Services (internal)
4. Starts 3 **BFF** Deployments + ClusterIP Services
5. BFF env `ip_port` points to Core K8s DNS (`buildmart-materials:8001`, etc.)
6. Applies Ingress for public HTTPS BFF access

**Verify pods:**
```bash
kubectl get pods -n buildmart
kubectl logs -n buildmart deployment/buildmart-materials-bff
```

**Expected pods (6 running):**
```
buildmart-materials-xxxxx
buildmart-workers-xxxxx
buildmart-delivery-xxxxx
buildmart-materials-bff-xxxxx
buildmart-workers-bff-xxxxx
buildmart-delivery-bff-xxxxx
```

---

## One-command pipeline

```bash
export REGISTRY=ghcr.io/sandeep8756
export TAG=v1.0.0
export API_HOST=api.yourdomain.com
export KUBECONFIG=~/.kube/config

./scripts/release-k8s.sh
```

---

## Connect Vercel UI to K8s BFF

After Ingress is live, set in **Vercel → Settings → Environment Variables**:

```
NEXT_PUBLIC_MATERIALS_BFF_URL=https://api.yourdomain.com
NEXT_PUBLIC_WORKERS_BFF_URL=https://api.yourdomain.com
NEXT_PUBLIC_DELIVERY_BFF_URL=https://api.yourdomain.com
```

Redeploy UI on Vercel.

**Test BFF:**
```bash
curl https://api.yourdomain.com/buildmart-materials-bff/materials_list_bff
curl https://api.yourdomain.com/buildmart-workers-bff/workers_list_bff
curl https://api.yourdomain.com/buildmart-delivery-bff/delivery_options_bff
```

---

## K8s manifest layout

```
k8s/
├── namespace.yaml
├── ingress.yaml              # Public BFF entry (HTTPS)
├── core/
│   ├── buildmart-materials.yaml   # Deployment + ClusterIP Service
│   ├── buildmart-workers.yaml
│   └── buildmart-delivery.yaml
└── bff/
    ├── buildmart-materials-bff.yaml
    ├── buildmart-workers-bff.yaml
    └── buildmart-delivery-bff.yaml
```

Rendered output goes to `k8s/generated/` (gitignored).

---

## Local K8s dev (Minikube)

```bash
minikube start
minikube addons enable ingress

export REGISTRY=ghcr.io/sandeep8756
export TAG=dev
export API_HOST=buildmart.local

./scripts/build-images.sh
# For minikube, load images locally instead of push:
minikube image load ghcr.io/sandeep8756/buildmart-materials:dev
minikube image load ghcr.io/sandeep8756/buildmart-workers:dev
minikube image load ghcr.io/sandeep8756/buildmart-delivery:dev
minikube image load ghcr.io/sandeep8756/buildmart-materials-bff:dev
minikube image load ghcr.io/sandeep8756/buildmart-workers-bff:dev
minikube image load ghcr.io/sandeep8756/buildmart-delivery-bff:dev

./scripts/deploy-k8s.sh

# Add to /etc/hosts: <minikube-ip> buildmart.local
minikube ip
```

---

## Rollout / upgrade

```bash
# Build + push new version
TAG=v1.0.1 ./scripts/build-images.sh
TAG=v1.0.1 ./scripts/push-images.sh

# Rolling update (K8s replaces pods automatically)
TAG=v1.0.1 ./scripts/deploy-k8s.sh

# Watch rollout
kubectl rollout status deployment/buildmart-materials-bff -n buildmart
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ImagePullBackOff` | Run `docker push` and check registry login |
| BFF can't reach Core | Verify Core pods running; `ip_port` uses K8s service name |
| Ingress 404 | Check NGINX ingress controller is installed |
| UI mixed content | Use `https://` BFF URLs in Vercel env |
| Wrong cluster | Check `KUBECONFIG` — use personal, not office |

```bash
kubectl describe pod -n buildmart <pod-name>
kubectl logs -n buildmart deployment/buildmart-materials-bff
kubectl get ingress -n buildmart
```
