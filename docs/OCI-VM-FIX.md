# Fix OCI Mumbai Free Tier — OKE Node Pool Failed

OKE node pool fails with `NODEPOOL_CREATE Failed` because **ARM (A1.Flex) capacity is full** in Mumbai free tier. This is an OCI infrastructure limit, not a code bug.

**Fix: Use an Always Free VM instead of OKE worker nodes.**

---

## Option A — VM + k3s (Kubernetes on VM)

### 1. Create VM in OCI Console

[OCI Console Mumbai](https://cloud.oracle.com/?region=ap-mumbai-1)

**Compute → Instances → Create instance**

| Setting | Value |
|---------|-------|
| Name | `buildmart-vm` |
| Image | Oracle Linux 8 |
| Shape | VM.Standard.A1.Flex |
| OCPUs | 1 |
| Memory | 6 GB |
| Public IP | Yes |
| SSH key | Add your public key |

If creation fails → try **different Availability Domain** or retry later.

### 2. Open firewall ports

**Networking → VCN → Security Lists → Default → Add Ingress Rules**

| Source CIDR | Port |
|-------------|------|
| 0.0.0.0/0 | 22 (SSH) |
| 0.0.0.0/0 | 80 |
| 0.0.0.0/0 | 443 |
| 0.0.0.0/0 | 8101 |
| 0.0.0.0/0 | 8102 |
| 0.0.0.0/0 | 8103 |

### 3. SSH and run setup

```bash
ssh opc@<VM-PUBLIC-IP>

curl -fsSL https://raw.githubusercontent.com/sandeep8756/buildmart-backend/main/scripts/setup-oci-vm-k3s.sh | bash
```

### 4. Vercel env vars

```
NEXT_PUBLIC_MATERIALS_BFF_URL=http://<VM-IP>
NEXT_PUBLIC_WORKERS_BFF_URL=http://<VM-IP>
NEXT_PUBLIC_DELIVERY_BFF_URL=http://<VM-IP>
```

---

## Option B — VM + Docker Compose (simplest)

```bash
ssh opc@<VM-PUBLIC-IP>

curl -fsSL https://raw.githubusercontent.com/sandeep8756/buildmart-backend/main/scripts/setup-oci-vm-compose.sh | bash
```

Vercel env (note port per BFF):

```
NEXT_PUBLIC_MATERIALS_BFF_URL=http://<VM-IP>:8101
NEXT_PUBLIC_WORKERS_BFF_URL=http://<VM-IP>:8102
NEXT_PUBLIC_DELIVERY_BFF_URL=http://<VM-IP>:8103
```

---

## Why OKE failed

| Work request | Cause |
|--------------|-------|
| NODEPOOL_CREATE | Out of host capacity (ARM A1.Flex) |
| NODEPOOL_UPDATE | Same |
| NODEPOOL_RECONCILE | Same |

**OKE control plane (`buildmart-oke`) is fine** — only worker nodes can't provision. Leave it or delete later; no charge for Basic cluster without nodes.

---

## Retry OKE later (optional)

When ARM capacity frees up in Mumbai:

1. Delete failed `pool1`
2. Add node pool: A1.Flex, **1 OCPU, 6 GB**, 1 node
3. Subnet: `oke-nodesubnet-quick-...-regional`
4. GitHub Actions deploy will work (secrets already set)

---

## What stays working

| Component | Status |
|-----------|--------|
| Oracle DB `buildmart` | Available |
| GitHub build/release | Auto on push |
| Vercel UI | Deployed |
| OKE cluster | Active (no workers) |
| **Fix** | VM + k3s or docker compose |
