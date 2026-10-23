# SuperDry Capacity Agent — Agent Skill

Drive **all** of SuperDry Capacity Agent's functionality from Google Antigravity
or Gemini CLI (or your terminal) via chat: authenticate to Google Cloud, run
capacity advisories, and deploy GPU, TPU, or CPU capacity with a priority-based
strategy.

This folder is a self-contained **Agent Skill** (`SKILL.md` + a portable CLI). It
works with Google Antigravity and Gemini agents that support the `SKILL.md`
convention, and also works standalone as a plain CLI.

## Contents

```
skills/capacity-radar/
├── SKILL.md                     # Skill definition + agent instructions
├── README.md                    # This file
└── scripts/
    └── capacity_radar.py        # Portable CLI (auth, catalog, advise, deploy)
```

## Install (one line)

From Google Antigravity, point it at this repo/folder, e.g.:

```
Install the skill at https://github.com/bapimohanty-goog/SuperdryCapacityAgent (skills/capacity-radar)
```

Or copy the `skills/capacity-radar` folder into your agent's skills directory.

## Prerequisites

- Python 3.10+
- Google Cloud SDK (`gcloud`)
- SuperDry Capacity Agent backend dependencies:

  ```bash
  pip install -r backend/requirements.txt
  ```

- Authenticate once (Application Default Credentials):

  ```bash
  gcloud auth application-default login
  ```

## Use it directly (no agent)

```bash
# Auth + project check
python skills/capacity-radar/scripts/capacity_radar.py auth check --project my-project

# Discover chips / series / zones / VPC networks
python skills/capacity-radar/scripts/capacity_radar.py catalog chips
python skills/capacity-radar/scripts/capacity_radar.py catalog zones --machine-type a3-highgpu-8g
python skills/capacity-radar/scripts/capacity_radar.py catalog zones --machine-type c4-standard-16
python skills/capacity-radar/scripts/capacity_radar.py catalog networks --project my-project --region us-central1

# Advisories (safe / read-only)
python skills/capacity-radar/scripts/capacity_radar.py advise spot     --project my-project --machine-type a3-highgpu-8g --regions us-central1
python skills/capacity-radar/scripts/capacity_radar.py advise spot     --project my-project --machine-type c4-standard-16 --regions us-central1
python skills/capacity-radar/scripts/capacity_radar.py advise calendar --project my-project --machine-type a3-highgpu-8g --vm-count 4 --duration-days 7
python skills/capacity-radar/scripts/capacity_radar.py advise flex      --project my-project --machine-type a3-highgpu-8g --size 4 --max-run-hours 24 --regions us-central1

# Deploy (creates REAL, billable resources — requires --yes)
python skills/capacity-radar/scripts/capacity_radar.py deploy \
  --project my-project --machine-type a3-highgpu-8g --vm-count 2 \
  --priority spot:us-central1-b,us-east4-a \
  --priority dws_flex:us-central1-b \
  --yes

python skills/capacity-radar/scripts/capacity_radar.py deploy \
  --project my-project --machine-type c4-standard-16 --vm-count 4 \
  --priority on_demand:us-central1-a,us-central1-b \
  --priority spot:us-central1-a,us-central1-b \
  --yes
```

Every command prints JSON to stdout so agents can parse results and decide the
next step. `deploy` also streams live progress lines to stderr.

See **[SKILL.md](./SKILL.md)** for the full agent workflow and safety rules.

> Not an official Google product. `deploy` creates real GCP resources that cost
> money — always confirm the plan with the user first.
