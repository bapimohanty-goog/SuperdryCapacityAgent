# SuperDry Capacity Agent

**Priority-based GPU, TPU, and CPU capacity scanning and deployment tool for Google Cloud Platform.**

SuperDry Capacity Agent automates finding and securing compute capacity across Google Cloud zones for **all Compute Engine and Cloud TPU families** — including GPUs, TPUs, General Purpose CPUs, Compute-Optimized CPUs, Memory-Optimized CPUs, Storage-Optimized CPUs, and custom GCE machine types. It supports multiple consumption models — On-Demand Reservations, DWS Calendar, DWS Flex Start, and Spot VMs — and lets you define a priority-based strategy that tries each method in order until capacity is secured.

![Google Cloud](https://img.shields.io/badge/Google%20Cloud-GPU%20%2F%20TPU%20%2F%20CPU-4285F4?logo=google-cloud&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)

---

## Features

### Scan & Deploy
- **All Compute Categories Supported** — Choose from **370 preset configurations** across 6 categories (**GPU**, **TPU**, **General Purpose CPU**, **Compute-Optimized CPU**, **Memory-Optimized CPU**, **Storage-Optimized CPU**) or enter any **Custom / Search** GCE machine type (e.g., `n2-custom-8-32768`, `c3-standard-8-lssd`)
- **Priority-based scanning** — Define up to 4 priorities (e.g., try On-Demand first, then DWS Calendar, then Spot)
- **Multi-zone scanning** — Automatically tries all supported zones for the chosen machine type
- **Automatic hardware-aware provisioning** — Automatically configures `hyperdisk-balanced` + `GVNIC` for 4th-gen families (`C4`, `C4A`, `C4D`, `N4`, `H3`, `M4`, `X4`, `Z3`), `GVNIC` for 3rd-gen families (`C3`, `C3D`, `M3`), Arm64 OS images (`debian-12-arm64`) for Arm series (`C4A`, `T2A`), and `guestAccelerators` attachment for N1-attached GPUs (`T4`, `V100`)
- **Real-time progress** — WebSocket-based live updates with detailed step-by-step logs
- **Sequential or Parallel** execution modes
- **Custom naming** — Set resource name prefixes for reservations and VMs
- **Cancel anytime** — Cancel a running scan and the tool stops gracefully

### Consumption Models

| Model | Description | Supported Hardware |
|-------|-------------|--------------------|
| **On-Demand Reservation** | Reserve capacity at on-demand rates. Immediate if available. | All CPU families (General Purpose, Compute/Memory/Storage-Optimized, Custom GCE), plus A4X, A3 Edge/Mega/High, A2, G4, G2, and N1 (T4/V100) GPUs |
| **DWS Calendar Mode** | Book capacity for a specific time window as a future reservation. Uses DENSE deployment for multi-node GPU families. | A4, A3 Ultra/Mega/High/Edge GPUs; v6e, v5p, v5e TPUs |
| **DWS Flex Start** | Queue for capacity; retries until resources become available. For TPUs, uses Queued Resources with configurable max wait time. | A4X, A4, A3 GPUs; v6e, v5p, v5e TPUs |
| **Spot VMs** | Spare capacity at a discount. Can be preempted at any time. | All GPU, TPU, CPU, and Custom GCE families |

### Capacity Advisory

- **Spot VM Advisory** — Check spot capacity availability and preemption scores across regions and zones for any GPU or CPU machine type
- **DWS Calendar Advisory** — Query the Calendar Mode Advisory API to find optimal zones and time windows (supported on Calendar-eligible GPU/TPU families)
  - **Check Availability** — Query with your exact parameters (start date, flexibility, duration)
  - **Find Best Plan** — Queries at multiple VM count levels (100%, 75%, 50%, 25%, 1 VM) to show how to split capacity across multiple smaller reservations
- **DWS Flex Start Advisory** _(Preview — requires a whitelisted project)_ — For a chosen machine type, size, and region/zone, estimates how long a DWS Flex Start request would wait in the queue before capacity is granted. This capability is in Preview and is only available for allow-listed (whitelisted) projects; non-whitelisted projects receive `The service is not available for this project.`

---

## Supported Hardware

### GPU Families (11 Chips, 39 Configs)

| Family | GPU | Machine Types | DWS Calendar | DWS Flex | Spot | On-Demand |
|--------|-----|---------------|:------------:|:--------:|:----:|:---------:|
| A4X Max | NVIDIA GB300 | `a4x-maxgpu-4g-metal` | - | Yes | Yes | - |
| A4X | NVIDIA GB200 | `a4x-highgpu-4g` | - | Yes | Yes | Yes |
| A4 | NVIDIA B200 | `a4-highgpu-8g` | Yes (DENSE) | Yes | Yes | - |
| A3 Ultra | NVIDIA H200 | `a3-ultragpu-8g` | Yes (DENSE) | Yes | Yes | - |
| A3 Edge | NVIDIA H100 | `a3-edgegpu-8g` | Yes (DENSE) | Yes | Yes | Yes |
| A3 Mega | NVIDIA H100 | `a3-megagpu-8g` | Yes (DENSE) | Yes | Yes | Yes |
| A3 High | NVIDIA H100 | `a3-highgpu-{1,2,4,8}g` | Yes (DENSE) | Yes | Yes | Yes |
| A2 Ultra | NVIDIA A100 80GB | `a2-ultragpu-{1,2,4,8}g` | - | - | Yes | Yes |
| A2 Standard | NVIDIA A100 40GB | `a2-highgpu-{1,2,4,8}g` | - | - | Yes | Yes |
| G4 | NVIDIA RTX PRO 6000 | `g4-standard-{6..384}` | - | - | Yes | Yes |
| G2 | NVIDIA L4 | `g2-standard-{4..96}` | - | - | Yes | Yes |
| N1 + T4 | NVIDIA T4 | `n1-standard-{4,8,16,32,64,96}-t4-{1,2,4}g` | - | - | Yes | Yes |
| N1 + V100 | NVIDIA V100 | `n1-standard-{4,8,16,32,64,96}-v100-{1,2,4,8}g` | - | - | Yes | Yes |

### TPU Types (6 Generations, 12 Configs)

| Type | Machine Types | Zones | DWS Calendar | DWS Flex | Spot |
|------|---------------|-------|:------------:|:--------:|:----:|
| v6e (Trillium) | `v6e-{1,4,8}chip` | 9 zones | Yes | Yes | Yes |
| v5p | `v5p-8chip` | 3 zones | Yes | Yes | Yes |
| v5e | `v5e-{1,4,8}chip` | 5 zones | Yes | Yes | Yes |
| v4 | `v4-8chip` | 1 zone | - | - | Yes |
| v3 | `v3-8chip` | 3 zones | - | - | Yes |
| v2 | `v2-8chip` | 5 zones | - | - | Yes |

### General Purpose CPU Families (10 Series, 225 Configs)

| Series | Processor | Machine Types | Spot | On-Demand |
|--------|-----------|---------------|:----:|:---------:|
| **C4** | Intel Granite Rapids / Emerald Rapids | `c4-standard-{2..288}`, `c4-highcpu-{2..288}`, `c4-highmem-{2..288}` | Yes | Yes |
| **C4A** | Google Axion (Arm) | `c4a-standard-{1..72}`, `c4a-highcpu-{1..72}`, `c4a-highmem-{1..72}` | Yes | Yes |
| **C4D** | AMD EPYC Turin (5th Gen) | `c4d-standard-{2..384}`, `c4d-highcpu-{2..384}`, `c4d-highmem-{2..384}` | Yes | Yes |
| **N4** | Intel Emerald Rapids | `n4-standard-{2..80}`, `n4-highcpu-{2..80}`, `n4-highmem-{2..80}` | Yes | Yes |
| **N2** | Intel Ice Lake / Cascade Lake | `n2-standard-{2..128}`, `n2-highcpu-{2..96}`, `n2-highmem-{2..128}` | Yes | Yes |
| **N2D** | AMD EPYC Milan / Rome | `n2d-standard-{2..224}`, `n2d-highcpu-{2..224}`, `n2d-highmem-{2..96}` | Yes | Yes |
| **E2** | Cost-Optimized x86 | `e2-micro`, `e2-small`, `e2-medium`, `e2-standard-{2..32}`, `e2-highcpu-{2..32}`, `e2-highmem-{2..16}` | Yes | Yes |
| **T2D** | AMD EPYC Milan Scale-Out | `t2d-standard-{1..60}` | Yes | Yes |
| **T2A** | Ampere Altra (Arm) | `t2a-standard-{1..48}` | Yes | Yes |
| **N1** | Intel Skylake / Broadwell | `n1-standard-{1..96}`, `n1-highcpu-{2..96}`, `n1-highmem-{2..96}` | Yes | Yes |

### Compute-Optimized CPU Families (5 Series, 69 Configs)

| Series | Processor | Machine Types | Spot | On-Demand |
|--------|-----------|---------------|:----:|:---------:|
| **C3** | Intel Sapphire Rapids | `c3-standard-{4..192}`, `c3-highcpu-{4..192}`, `c3-highmem-{4..192}` | Yes | Yes |
| **C3D** | AMD EPYC Genoa (4th Gen) | `c3d-standard-{4..360}`, `c3d-highcpu-{4..360}`, `c3d-highmem-{4..360}` | Yes | Yes |
| **H3** | HPC Intel Sapphire Rapids | `h3-standard-88` | Yes | Yes |
| **C2** | Intel Cascade Lake | `c2-standard-{4,8,16,30,60}` | Yes | Yes |
| **C2D** | AMD EPYC Milan | `c2d-standard-{2..112}`, `c2d-highcpu-{2..112}`, `c2d-highmem-{2..112}` | Yes | Yes |

### Memory-Optimized CPU Families (5 Series, 23 Configs)

| Series | Processor | Machine Types | Spot | On-Demand |
|--------|-----------|---------------|:----:|:---------:|
| **M4** | Next-Gen Memory-Optimized | `m4-megamem-{28,56,112,224}`, `m4-ultramem-{56,112,224}` | Yes | Yes |
| **M3** | Intel Ice Lake | `m3-megamem-{64,128}`, `m3-ultramem-{32,64,128}` | Yes | Yes |
| **M2** | Intel Cascade Lake Ultramem | `m2-megamem-416`, `m2-hypermem-416`, `m2-ultramem-{208,416}` | Yes | Yes |
| **M1** | Intel Skylake | `m1-megamem-96`, `m1-ultramem-{40,80,160}` | Yes | Yes |
| **X4** | Extreme Memory (16–32 TB) | `x4-megamem-{960,1440,1920}-metal` | Yes | Yes |

### Storage-Optimized CPU Families (1 Series, 2 Configs)

| Series | Processor | Machine Types | Spot | On-Demand |
|--------|-----------|---------------|:----:|:---------:|
| **Z3** | Intel Sapphire Rapids + High-Density Titanium SSD | `z3-highmem-88`, `z3-highmem-176` | Yes | Yes |

### Custom / Arbitrary GCE Machine Types

Use the **Search / Custom** tab in the UI (or pass any GCE machine type string to the API/CLI) to scan or deploy any valid Google Cloud Compute Engine machine type not in the presets — such as custom vCPU/memory shapes (`n2-custom-8-32768`), local SSD variants (`c3-standard-8-lssd`), or shared-core shapes (`f1-micro`, `g1-small`).

---

## Two ways to use it

SuperDry Capacity Agent can be used **either** as a web app **or** as an **AI Agent Skill**
(drive everything from chat in an agent like Claude, Google Antigravity, etc.).

- **Web app** — run the FastAPI backend + React UI (see Quick Start below).
- **Agent Skill** — install the bundled skill so an AI agent can authenticate,
  run advisories, and deploy capacity through conversation. See
  **[Use as an Agent Skill](#use-as-an-agent-skill)**.

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm
- **Google Cloud SDK** (`gcloud`) installed and configured
- A GCP project with **Compute Engine API** enabled

### 1. Clone the Repository

```bash
git clone https://github.com/bapimohanty-goog/SuperdryCapacityAgent.git
cd SuperdryCapacityAgent
```

### 2. Authenticate with Google Cloud

```bash
# Login with your Google account (sets up Application Default Credentials)
gcloud auth application-default login

# Set your project (optional — you can also enter it in the UI)
gcloud config set project YOUR_PROJECT_ID
```

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies & Build

```bash
cd ../frontend
npm install
npm run build
```

### 5. Run the Application

```bash
cd ../backend
python main.py
```

The app will be available at **http://localhost:8000**

### Development Mode (Hot Reload)

For frontend development with hot reload:

```bash
# Terminal 1: Backend
cd backend && python main.py

# Terminal 2: Frontend dev server (proxied to backend)
cd frontend && npm run dev
```

Frontend dev server runs on http://localhost:3000 with API proxy to :8000.

---

## Architecture

```
SuperdryCapacityAgent/
├── backend/
│   ├── main.py              # FastAPI server — REST + WebSocket endpoints
│   ├── hunter.py            # Core scanning engine (GPU, TPU & CPU deployment)
│   ├── advisory.py          # DWS Calendar, Spot & Flex advisory API queries
│   ├── gpu_data.py          # Full machine type catalog (GPU/TPU/CPU), zone mappings, consumption support
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main app — auth drawer, tab navigation
│   │   └── components/
│   │       ├── AdvisoryPanel.jsx       # Calendar, Spot & DWS Flex advisory queries
│   │       ├── ScanningPanel.jsx       # Scan & Deploy configuration + live logs
│   │       └── MachineTypeSelector.jsx # Category → Chip/Series → Machine type picker + Custom GCE input
│   ├── vite.config.js       # Vite config with API proxy
│   └── package.json
└── README.md
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, FastAPI, WebSocket, httpx |
| Frontend | React 18, Material UI v5, Vite |
| Auth | Google Application Default Credentials (ADC) |
| APIs | Compute Engine REST API (v1), TPU API (v2), Spot Advisory (alpha) |

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/auth/check` | Verify GCP auth and project access |
| `POST` | `/api/auth/login` | Trigger `gcloud auth application-default login` |
| `GET` | `/api/machine-types` | List all 370 preset GPU/TPU/CPU machine types with zone info |
| `GET` | `/api/chip-groups` | Machine types grouped by category and chip/series for the selector |
| `GET` | `/api/machine-types/{type}/zones` | Zones and metadata for a preset or custom GCE machine type |
| `POST` | `/api/advisory/calendar` | Query DWS Calendar Advisory API |
| `POST` | `/api/advisory/calendar/splits` | Find best capacity split plan |
| `POST` | `/api/advisory/spot` | Query Spot VM Advisory API |
| `POST` | `/api/advisory/flex` | Query DWS Flex Start Capacity Advisory API (Preview — whitelisted projects) |
| `WS` | `/ws/scan` | WebSocket for real-time scan & deploy across GPU, TPU, and CPU types |

---

## Configuration

### Required GCP IAM Permissions

The authenticated user or service account needs:

| Role | Purpose |
|------|---------|
| `roles/compute.admin` | Create reservations, instances, future reservations |
| `roles/tpu.admin` | Create TPU nodes and queued resources (if using TPUs) |

### CORS Configuration

By default, the backend allows requests from `localhost:3000` and `localhost:5173` (Vite dev servers). To customize:

```bash
export CORS_ORIGINS="http://localhost:3000,https://your-domain.com"
```

### Changing the Port

Edit `backend/main.py`:

```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change 8000
```

---

## Usage Guide

### Setting Up a Scan

1. **Authenticate** — Click "Authenticate with Google" to open browser sign-in
2. **Connect** — Enter your GCP Project ID and click "Connect"
3. **Select machine type** — Pick a Category (**GPU**, **TPU**, **General Purpose**, **Compute-Opt**, **Memory-Opt**, **Storage-Opt**, or **Search / Custom**) → Chip / Series → Machine Type (or search/enter any custom GCE machine type)
4. **Set VM count** — Min and Max VMs (system tries max first, scales down to min)
5. **Add priorities** — Each priority specifies:
   - Consumption method (On-Demand, DWS Calendar, DWS Flex, Spot — automatically filtered to methods supported by the selected hardware)
   - Target zones (leave empty = try all available)
   - Retry rounds and interval
   - Optional resource name prefix
6. **Method-specific settings**:
   - **DWS Calendar**: Start/end times for the reservation window
   - **DWS Flex**: Max wait time and usage duration
7. Choose **Sequential** or **Parallel** execution
8. Click **Start Scan & Deploy**

### Using the Advisory Tab

#### Spot VM Advisory (All GPU & CPU Types)
1. Select any GPU or CPU machine type (or enter a custom GCE machine type)
2. Filter by regions (optional)
3. Click **Check Spot Availability** to view zone-by-zone preemption scores

#### DWS Calendar Advisory (Supported GPU & TPU Families)
1. Select a Calendar-eligible GPU/TPU machine type and enter VM count
2. Pick a start date and flexibility window (0-3 days)
3. Set duration in days
4. Click **Check Availability** to see zone recommendations, or click **Find Best Plan** to query at 100%, 75%, 50%, 25%, and 1 VM counts to plan split reservations

### Understanding Scan Results

| Status | Meaning |
|--------|---------|
| **Success** | Capacity secured. Logs show method, zone, and resource details. |
| **Failed** | All priorities exhausted. Try different zones, types, or methods. |
| **Cancelled** | You stopped the scan. Check GCP Console for partial resources. |

### DWS Calendar Behavior
Calendar future reservations use `reservationMode: CALENDAR` with DENSE deployment for multi-node GPU families (A3, A4). After submission, the tool polls until Google approves or rejects. Approval is typically within a minute for eligible projects.

### DWS Flex Behavior
- **GPUs**: Uses Compute Engine reservations with retry logic (no real queue — each attempt succeeds or fails immediately)
- **TPUs**: Uses the TPU Queued Resource API with actual server-side queuing

---

## Use as an Agent Skill

SuperDry Capacity Agent ships with a self-contained **AI Agent Skill** so any agent (e.g.
Claude, Google Antigravity, or other agentic IDEs) can drive **all** of the app's
functionality through chat — authenticate, run any advisory (Calendar / Spot /
DWS Flex, any chip/series/region/size), and configure + launch a priority-based
deployment — asking the user follow-up questions for any missing input, exactly
like the web UI.

The skill lives in **[`skills/capacity-radar/`](skills/capacity-radar/)** and is
built as a `SKILL.md` plus a portable CLI (`scripts/capacity_radar.py`) that
reuses the app's own backend, so results are identical to the UI.

### Install (one line)

Point your agent at this repo/skill folder, for example:

```
Install the skill at https://github.com/bapimohanty-goog/SuperdryCapacityAgent (skills/capacity-radar)
```

…or copy `skills/capacity-radar/` into your agent's skills directory.

### Prerequisites

```bash
pip install -r backend/requirements.txt      # backend deps the skill reuses
gcloud auth application-default login         # one-time auth (or use the skill's `auth login`)
```

### What the agent can do

- **Authenticate** — check ADC + project access; help the user log in if needed.
- **Discover** — list GPU/TPU/CPU chips & series, machine types, and supported zones.
- **Advise (safe / read-only)** — Spot, DWS Calendar (+ best-split plan), and
  DWS Flex Start (Preview / whitelisted) advisories for any machine type/region/size.
- **Deploy** — priority-based scan & deploy (sequential or parallel). This
  creates **real, billable** resources, so the skill requires explicit
  confirmation (`--yes`) before it will proceed.

### Run the CLI directly (no agent required)

```bash
# Auth + discovery
python skills/capacity-radar/scripts/capacity_radar.py auth check --project my-project
python skills/capacity-radar/scripts/capacity_radar.py catalog chips

# Advisories (GPU or CPU)
python skills/capacity-radar/scripts/capacity_radar.py advise spot --project my-project --machine-type a3-highgpu-8g --regions us-central1
python skills/capacity-radar/scripts/capacity_radar.py advise spot --project my-project --machine-type c4-standard-8 --regions us-central1
python skills/capacity-radar/scripts/capacity_radar.py advise flex --project my-project --machine-type a3-highgpu-8g --size 4 --max-run-hours 24 --regions us-central1

# Deploy (creates real resources — requires --yes)
python skills/capacity-radar/scripts/capacity_radar.py deploy \
  --project my-project --machine-type a3-highgpu-8g --vm-count 2 \
  --priority spot:us-central1-b,us-east4-a --priority dws_flex:us-central1-b --yes

python skills/capacity-radar/scripts/capacity_radar.py deploy \
  --project my-project --machine-type c4-standard-16 --vm-count 4 \
  --priority on_demand:us-central1-a,us-central1-b --priority spot:us-central1-a --yes
```

See **[`skills/capacity-radar/SKILL.md`](skills/capacity-radar/SKILL.md)** for the
full agent workflow, command reference, and safety rules.

---

## Deployment

### Docker

The repo ships a multi-stage `Dockerfile` (Node 20 builds the frontend, Python 3.12 serves it) listening on port 8080:

```bash
docker build -t superdry-capacity-agent .
docker run -p 8080:8080 \
  -e DEMO_MODE=false \
  -v ~/.config/gcloud:/root/.config/gcloud \
  superdry-capacity-agent
```

> Mount your `gcloud` config directory to pass ADC credentials to the container.

### Cloud Run — public hosted app (bring-your-own-credentials)

This reproduces the hosted web app exactly. The service runs as a **zero-permission** service account and never uses server-side credentials (`AUTH_MODE=user`): visitors paste their own access token (`gcloud auth print-access-token`, Cloud Shell works too) into the Authentication panel, so every scan and deploy runs under the visitor's own identity, project, and quota. That's what makes the URL safe to share publicly.

```bash
# One-time: create a service account and grant it NO roles
gcloud iam service-accounts create superdry-capacity-web

gcloud run deploy superdry-capacity-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --service-account superdry-capacity-web@YOUR_PROJECT.iam.gserviceaccount.com \
  --set-env-vars DEMO_MODE=false,AUTH_MODE=user \
  --memory 512Mi --cpu 1 --max-instances 2
```

### Cloud Run — private deployment (server credentials)

If the app is only for you or your team, you can instead give the service account real permissions (`roles/compute.admin`, plus `roles/tpu.admin` for TPUs) and skip the token-pasting flow:

```bash
gcloud run deploy superdry-capacity-agent \
  --source . \
  --region us-central1 \
  --no-allow-unauthenticated \
  --service-account SA_NAME@PROJECT.iam.gserviceaccount.com \
  --set-env-vars DEMO_MODE=false
```

> Never combine server credentials with `--allow-unauthenticated`: anyone on the internet could then create billable resources in your project.

### Environment variables

| Variable | Dockerfile default | Hosted app | Purpose |
|----------|-------------------|------------|---------|
| `DEMO_MODE` | `true` | `false` | When `true`, real deployments are disabled (safe demo). Set `false` for a working app. |
| `AUTH_MODE` | `local` | `user` | `user` = backend never uses its own credentials; every request must carry a visitor-supplied token. |
| `DEFAULT_PROJECT` | empty | empty | Optional project ID to pre-fill in the UI. |
| `OAUTH_CLIENT_ID` | unset | unset | Optional: enables a "Sign in with Google" button instead of token pasting (requires your own verified OAuth client). |

---

## Important Notes

- **Cost**: This tool creates real GCP resources (reservations, VMs, TPU nodes). Understand cost implications before deploying.
- **Cleanup**: If a scan is cancelled, check GCP Console for partially created resources that may still incur charges.
- **Quotas**: Ensure your project has sufficient quota for the machine types and zones you're targeting.
- **DWS Calendar**: Future reservations may require Google account team approval for DENSE deployment eligibility. If you get a "not available for this project" error, contact your account representative.
- **A4X Max & X4**: Bare metal instances — cannot use standard on-demand reservations.
- **Token Refresh**: ADC tokens are automatically refreshed every 50 minutes during long scans.

---

## Disclaimer

This is **not** an official Google product. There is no SLA, warranty, or guarantee of any kind. Use at your own risk.
