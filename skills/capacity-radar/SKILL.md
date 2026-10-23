---
name: capacity-radar
description: >-
  Find, advise on, and deploy Google Cloud GPU, TPU, and CPU capacity (across all
  Compute Engine machine families) from chat. Use this skill whenever the user
  wants to check GPU/TPU/CPU availability, get capacity advice, compare consumption
  models (On-Demand, DWS Calendar, DWS Flex Start, Spot), or actually deploy,
  reserve, or hunt for GPU, TPU, General Purpose CPU, Compute-Optimized,
  Memory-Optimized, Storage-Optimized, or Custom GCE capacity on Google Cloud (GCP).
  Triggers include: "find me H100s", "check spot availability for c4-standard-8",
  "reserve a3-highgpu-8g", "deploy N2 / C3 / M4 VMs", "how long to wait for DWS Flex",
  "hunt for GPUs", "get me TPUs", "provision compute capacity".
license: Not an official Google product. Use at your own risk.
---

# SuperDry Capacity Agent Skill

**SuperDry Capacity Agent** helps users **find and secure GPU, TPU, and CPU capacity across all Google Cloud Compute Engine families**.
This skill lets you (the agent) drive every capability of the SuperDry Capacity Agent app
through a single CLI, entirely via chat: authenticate, explore all 370 preset machine types
(plus any custom GCE shape), run capacity advisories, and deploy using a priority-based strategy.

## What this skill can do (tell the user!)

Many users won't know the full capability. Proactively offer these:

1. **Authentication** — verify the user is logged into Google Cloud (ADC) and has
   access to their project; if not, help them log in (opens a browser).
2. **Catalog / discovery across all Compute Engine & TPU families** — list 370 preset
   machine types across 6 categories (plus any custom GCE machine type), supported zones,
   and which consumption models each supports:
   - **GPU (11 chips, 39 configs)** — NVIDIA GB300 (`a4x-maxgpu-4g-metal`), GB200 (`a4x-highgpu-4g`), B200 (`a4-highgpu-8g`), H200 (`a3-ultragpu-8g`), H100 (`a3-edgegpu-8g`, `a3-megagpu-8g`, `a3-highgpu-{1,2,4,8}g`), A100 80GB (`a2-ultragpu-*`), A100 40GB (`a2-highgpu-*`), RTX PRO 6000 (`g4-standard-*`), L4 (`g2-standard-*`), T4 (`n1-standard-*-t4-*`), and V100 (`n1-standard-*-v100-*`).
   - **TPU (6 generations, 12 configs)** — `v6e` (Trillium), `v5p`, `v5e`, `v4`, `v3`, `v2`.
   - **General Purpose CPU (10 series, 225 configs)** — `C4`, `C4A` (Axion Arm), `C4D`, `N4`, `N2`, `N2D`, `E2`, `T2D`, `T2A` (Arm), `N1`.
   - **Compute-Optimized CPU (5 series, 69 configs)** — `C3`, `C3D`, `H3`, `C2`, `C2D`.
   - **Memory-Optimized CPU (5 series, 23 configs)** — `M4`, `M3`, `M2`, `M1`, `X4`.
   - **Storage-Optimized CPU (1 series, 2 configs)** — `Z3` (`z3-highmem-88`, `z3-highmem-176`).
   - **Custom / Arbitrary GCE Machine Types** — any valid GCE machine type string (e.g., `n2-custom-8-32768`, `c3-standard-8-lssd`).
3. **Capacity Advisories** (read-only, safe — no resources created):
   - **Spot VM Advisory** — availability + preemption risk per zone for any GPU or CPU machine type.
   - **DWS Calendar Advisory** — recommended zones/time-windows for Calendar-eligible GPU/TPU families; plus a "best plan" mode that splits a large request across VM-count levels.
   - **DWS Flex Start Advisory** _(Preview — requires a whitelisted project)_ — estimated wait time in the queue before Flex Start capacity is granted.
4. **Scan & Deploy** — a priority-based hunt that tries consumption methods in
   order (or in parallel) across zones until capacity is secured, with automatic
   hardware-aware provisioning (`hyperdisk-balanced` + `GVNIC` for 4th-gen series
   like `C4`/`C4A`/`C4D`/`N4`/`H3`/`M4`/`X4`/`Z3`, `GVNIC` for `C3`/`C3D`/`M3`,
   `debian-12-arm64` for Arm `C4A`/`T2A`, and `guestAccelerators` for `N1` GPUs).
   **This creates real, billable GCP resources** — always confirm with the user first.

## The one tool: `scripts/capacity_radar.py`

Everything is done by running this Python CLI. It reuses the app's own backend
modules, so results are identical to the web UI. Every command prints JSON to
stdout so you can parse it and decide the next step.

Run it with the repo's Python environment (see Setup). General shape:

```bash
python scripts/capacity_radar.py <group> <command> [flags...]
```

### Commands

| Command | Purpose |
|---|---|
| `auth check --project <ID>` | Check ADC auth + project access + Compute API status |
| `auth login` | Run `gcloud auth application-default login` (opens browser) |
| `catalog chips` | List all GPU, TPU, and CPU series grouped by category (`gpu`, `tpu`, `general_purpose`, `compute_optimized`, `memory_optimized`, `storage_optimized`) |
| `catalog machine-types` | Full list of all 370 preset machine types + consumption model support matrix |
| `catalog zones --machine-type <MT>` | Supported zones/regions for any preset or custom GCE machine type |
| `catalog networks --project <ID> [--region <R>]` | List VPC networks (+ regional subnetworks); flags whether a `default` VPC exists |
| `advise spot --project <ID> --machine-type <MT> [--regions r1,r2] [--zones z1,z2]` | Spot availability + preemption risk (all GPU & CPU types) |
| `advise calendar --project <ID> --machine-type <MT> --vm-count N --start-date YYYY-MM-DD --flexibility-days 0..3 --duration-days D [--regions/--zones]` | DWS Calendar availability (Calendar-supported GPU/TPU families) |
| `advise calendar-plan ... (same flags as calendar)` | DWS Calendar "best split" plan |
| `advise flex --project <ID> --machine-type <MT> --size N --max-run-hours H [--regions/--zones]` | DWS Flex Start wait-time advisory (Preview) |
| `deploy --project <ID> --machine-type <MT> --vm-count N --priority <spec> [--priority ...] [--parallel] [--yes]` | Priority-based scan & deploy across GPU, TPU, or CPU types (REAL resources) |

### `--priority` spec format (deploy)

Repeatable. `method[:zones][:max_retries][:retry_interval]`
- `method` = `on_demand` | `dws_calendar` | `dws_flex` | `spot`
  - **CPU families (`C4`, `N4`, `N2`, `E2`, `C3`, `M4`, `Z3`, Custom GCE, etc.)**: support `on_demand` and `spot`
  - **GPU families**: support `spot`, plus `on_demand` / `dws_calendar` / `dws_flex` depending on family
  - **TPU families**: support `spot`, plus `dws_calendar` / `dws_flex` on `v6e`, `v5p`, `v5e`
- `zones` = comma-separated (omit → all supported zones for the machine type)
- Examples: `spot:us-central1-b,us-east4-a` · `on_demand:us-central1-a,us-central1-b` · `dws_flex:us-central1-b:3:60`

Extra deploy flags: `--name-prefix`, `--flex-max-wait-hours`, `--flex-usage-hours`,
`--calendar-start`/`--calendar-end` (ISO datetime), `--calendar-duration-hours`,
`--network`, `--subnetwork`.

### Network / subnetwork selection (GPU, TPU & CPU)

All GCE VMs (GPU and CPU) and TPU nodes need a VPC network. By default Cloud TPU uses a VPC
literally named `default`; on projects without one, deploys fail with
`The value "default" provided for field "Network"/"Subnetwork" does not exist`.

- Leave `--network`/`--subnetwork` **empty** to auto-select: prefer a `default`
  VPC, else the first VPC that has a subnetwork in the target region.
- Run `catalog networks --project <ID> --region <R>` to list options and see
  `hasDefault`. If there is no usable network, create one:
  `gcloud compute networks create <name> --subnet-mode=auto` (or use the app UI's
  "Create new VPC" option), then pass `--network <name>`.

## How to behave (agent workflow)

Follow this loop and **ask follow-up questions whenever an input is missing** —
mirror how the app collects inputs. Never guess the project ID.

1. **Auth first.** Run `auth check --project <ID>`. If `authenticated` is false,
   offer to run `auth login` (tell them a browser will open). If the project is
   invalid or the Compute API is disabled, surface the `instructions` from the
   JSON and help them fix it.
2. **Clarify intent.** Ask what they want: *advice* (safe) or *deploy* (creates
   resources). Suggest capabilities they may not know about.
3. **Resolve the resource.** If they name a GPU, TPU, or CPU series loosely
   (e.g., "H100", "8x H100", "C4 16 vCPU", "N2 highmem", "Trillium TPU"),
   use `catalog chips` to map it to an exact machine type (e.g. `a3-highgpu-8g`,
   `c4-standard-16`, `n2-highmem-32`, `v6e-4chip`), or pass a valid custom GCE
   machine type directly (e.g. `n2-custom-8-32768`). Use `catalog zones` to
   confirm/suggest regions & zones. Ask for any missing inputs (VM count,
   region/zone, duration, size, dates).
4. **Run the advisory** the user wants and summarize results clearly (which
   zones have capacity, estimated waits, preemption risk). Note that CPU families
   support the **Spot VM Advisory** (`advise spot`), while **DWS Calendar** and
   **DWS Flex** advisories apply to supported GPU/TPU families. For DWS Flex, note
   it is Preview/whitelisted; if you get `The service is not available for this
   project.`, explain the project needs allow-listing.
5. **For deploy:** build the priority strategy from the conversation, show the
   plan, and **require explicit user confirmation**. Only then run `deploy`
   with `--yes`. Without `--yes`, the CLI returns `requiresConfirmation: true`
   and a `plan` object — present that plan and ask the user to confirm. Stream
   progress (deploy writes live events to stderr and a full `events` array in
   the final JSON).

### Safety rules

- **Deploy creates real, billable resources.** Always confirm the exact plan
  (project, machine type, count, methods, zones) with the user before using
  `--yes`.
- Advisories are read-only and safe to run freely.
- Never fabricate project IDs, zones, or results — always run the CLI and report
  what it returns.

## Setup (one time)

The skill needs the SuperDry Capacity Agent backend deps available to Python and the
gcloud SDK for auth.

```bash
# From the repo root:
pip install -r backend/requirements.txt
# Authenticate once (or use: python skills/capacity-radar/scripts/capacity_radar.py auth login)
gcloud auth application-default login
```

Then invoke the CLI from the repo root, e.g.:

```bash
python skills/capacity-radar/scripts/capacity_radar.py catalog chips
```

## Quick examples

```bash
# Check auth + project
python skills/capacity-radar/scripts/capacity_radar.py auth check --project my-project

# "Do you have H100s on spot in us-central1?"
python skills/capacity-radar/scripts/capacity_radar.py advise spot \
  --project my-project --machine-type a3-highgpu-8g --regions us-central1

# "Check Spot availability for C4 16-vCPU instances in us-central1 and us-east4"
python skills/capacity-radar/scripts/capacity_radar.py advise spot \
  --project my-project --machine-type c4-standard-16 --regions us-central1,us-east4

# "How long would I wait for 4x H100 on DWS Flex?"
python skills/capacity-radar/scripts/capacity_radar.py advise flex \
  --project my-project --machine-type a3-highgpu-8g --size 4 --max-run-hours 24 --regions us-central1

# "Hunt for 2x H100: try spot first, then DWS Flex" (after user confirms)
python skills/capacity-radar/scripts/capacity_radar.py deploy \
  --project my-project --machine-type a3-highgpu-8g --vm-count 2 \
  --priority spot:us-central1-b,us-east4-a \
  --priority dws_flex:us-central1-b \
  --yes

# "Deploy 4x C4 standard VMs: try On-Demand first, then Spot" (after user confirms)
python skills/capacity-radar/scripts/capacity_radar.py deploy \
  --project my-project --machine-type c4-standard-16 --vm-count 4 \
  --priority on_demand:us-central1-a,us-central1-b \
  --priority spot:us-central1-a,us-central1-b \
  --yes
```
