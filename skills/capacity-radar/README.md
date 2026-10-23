# SuperDry Capacity Agent — Agent Skill

Drive **all** of SuperDry Capacity Agent's functionality from Google Antigravity
or Gemini CLI via chat: authenticate to Google Cloud, run capacity advisories,
and deploy GPU, TPU, or CPU capacity with a priority-based strategy.

This folder is a self-contained **Agent Skill** (`SKILL.md` + a portable CLI). It
works with Google Antigravity and Gemini agents that support the `SKILL.md`
convention.

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

See **[SKILL.md](./SKILL.md)** for the full agent workflow and safety rules.

> Not an official Google product. `deploy` creates real GCP resources that cost
> money — always confirm the plan with the user first.
