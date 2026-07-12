# Deploy from GitHub to OCI OKE (no local laptop needed)

Everything runs in **GitHub Actions** — you only configure secrets in GitHub + OCI Console.

---

## Flow

```
git push to main
    → Build and Release (builds 6 images → ghcr.io)
    → Deploy to Kubernetes (connects to OKE → runs pods)
```

**No laptop, no local kubectl, no local OCI CLI required.**

---

## One-time setup (OCI Console + GitHub only)

### Step 1 — Create API key in OCI Console

1. OCI Console → **Profile icon** (top right) → **My profile**
2. Click **API keys** (left menu) → **Add API key**
3. Choose **Generate API key pair** → **Download private key**
4. Save the downloaded `.pem` file
5. Copy the configuration shown on screen — you need:
   - `user` → **OCI_USER_OCID**
   - `fingerprint` → **OCI_FINGERPRINT**
   - `tenancy` → **OCI_TENANCY_OCID**
   - `region` → **OCI_REGION** (`ap-mumbai-1`)

---

### Step 2 — Get Cluster OCID

1. OCI Console → **Developer Services → Kubernetes Clusters (OKE)**
2. Open **`buildmart-oke`**
3. Copy **Cluster ID** (OCID) → **OCI_CLUSTER_OCID**

Example: `ocid1.cluster.oc1.ap-mumbai-1.xxxxx`

---

### Step 3 — Add secrets to GitHub

Go to: https://github.com/sandeep8756/buildmart-backend/settings/secrets/actions

Click **New repository secret** for each:

| Secret name | Value | Where to get it |
|-------------|-------|-----------------|
| `OCI_TENANCY_OCID` | `ocid1.tenancy.oc1..` | API key config screen |
| `OCI_USER_OCID` | `ocid1.user.oc1..` | API key config screen |
| `OCI_FINGERPRINT` | `aa:bb:cc:...` | API key config screen |
| `OCI_API_KEY` | Full content of `.pem` file | Downloaded private key |
| `OCI_REGION` | `ap-mumbai-1` | Your Mumbai region |
| `OCI_CLUSTER_OCID` | `ocid1.cluster.oc1..` | buildmart-oke cluster page |

**For `OCI_API_KEY`:** Open the `.pem` file in a text editor and paste the entire content including:
```
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
```

---

### Step 4 — Make ghcr.io images public (one-time)

GitHub Actions pushes images to ghcr.io. OKE must pull them.

1. Go to https://github.com/users/sandeep8756/packages
2. Open each `buildmart-*` package
3. **Package settings → Change visibility → Public**

Do this for all 6 packages.

---

### Step 5 — Trigger deploy from GitHub

**Option A — Manual trigger:**
1. https://github.com/sandeep8756/buildmart-backend/actions
2. Click **Deploy to Kubernetes**
3. Click **Run workflow** → **Run workflow**

**Option B — Automatic:**
- Any push to `main` triggers build → then auto-deploys

---

## What GitHub Actions does automatically

1. Installs OCI CLI on cloud runner
2. Uses your API key secrets to authenticate
3. Generates kubeconfig for `buildmart-oke`
4. Installs NGINX Ingress Controller
5. Deploys 6 pods (3 Core + 3 BFF)
6. Shows Ingress IP in workflow summary

---

## After deploy — connect Vercel UI

1. Open the **Deploy to Kubernetes** workflow run
2. Check **Summary** for **Ingress IP** (e.g. `80.225.x.x`)
3. In Vercel → Environment Variables:

```
NEXT_PUBLIC_MATERIALS_BFF_URL=http://<INGRESS-IP>
NEXT_PUBLIC_WORKERS_BFF_URL=http://<INGRESS-IP>
NEXT_PUBLIC_DELIVERY_BFF_URL=http://<INGRESS-IP>
```

4. Redeploy UI on Vercel

**Test:**
```
curl http://<INGRESS-IP>/buildmart-materials-bff/materials_list_bff
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Deploy skipped | Add all 6 OCI secrets to GitHub |
| `ImagePullBackOff` | Make ghcr.io packages public |
| `Unauthorized` OCI | Check API key PEM is complete in secret |
| No Ingress IP | Wait 2-5 min, re-run workflow |
| Pods not ready | Check Actions logs → `kubectl get pods -n buildmart` output |

---

## No local commands needed

You never need to run on your laptop:
- ~~oci ce cluster create-kubeconfig~~
- ~~kubectl apply~~
- ~~docker build/push~~

All done by GitHub Actions when you push code or click **Run workflow**.
