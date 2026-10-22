"""
Compute type, GPU, TPU, and CPU machine family, zone, and consumption model
mappings for Google Cloud Platform.
"""

import re

# ── Standard GCP Compute Zones (used for CPU series & custom machine types) ──
COMMON_CPU_ZONES = [
    # US
    "us-central1-a", "us-central1-b", "us-central1-c", "us-central1-f",
    "us-east1-b", "us-east1-c", "us-east1-d",
    "us-east4-a", "us-east4-b", "us-east4-c",
    "us-east5-a", "us-east5-b", "us-east5-c",
    "us-south1-a", "us-south1-b", "us-south1-c",
    "us-west1-a", "us-west1-b", "us-west1-c",
    "us-west2-a", "us-west2-b", "us-west2-c",
    "us-west3-a", "us-west3-b", "us-west3-c",
    "us-west4-a", "us-west4-b", "us-west4-c",
    # Americas
    "northamerica-northeast1-a", "northamerica-northeast1-b", "northamerica-northeast1-c",
    "northamerica-northeast2-a", "northamerica-northeast2-b", "northamerica-northeast2-c",
    "southamerica-east1-a", "southamerica-east1-b", "southamerica-east1-c",
    "southamerica-west1-a", "southamerica-west1-b", "southamerica-west1-c",
    # Europe
    "europe-central2-a", "europe-central2-b", "europe-central2-c",
    "europe-north1-a", "europe-north1-b", "europe-north1-c",
    "europe-southwest1-a", "europe-southwest1-b", "europe-southwest1-c",
    "europe-west1-b", "europe-west1-c", "europe-west1-d",
    "europe-west2-a", "europe-west2-b", "europe-west2-c",
    "europe-west3-a", "europe-west3-b", "europe-west3-c",
    "europe-west4-a", "europe-west4-b", "europe-west4-c",
    "europe-west6-a", "europe-west6-b", "europe-west6-c",
    "europe-west8-a", "europe-west8-b", "europe-west8-c",
    "europe-west9-a", "europe-west9-b", "europe-west9-c",
    # Middle East
    "me-central1-a", "me-central1-b", "me-central1-c",
    "me-central2-a", "me-central2-b", "me-central2-c",
    "me-west1-a", "me-west1-b", "me-west1-c",
    # Asia & Australia
    "asia-east1-a", "asia-east1-b", "asia-east1-c",
    "asia-east2-a", "asia-east2-b", "asia-east2-c",
    "asia-northeast1-a", "asia-northeast1-b", "asia-northeast1-c",
    "asia-northeast2-a", "asia-northeast2-b", "asia-northeast2-c",
    "asia-northeast3-a", "asia-northeast3-b", "asia-northeast3-c",
    "asia-south1-a", "asia-south1-b", "asia-south1-c",
    "asia-south2-a", "asia-south2-b", "asia-south2-c",
    "asia-southeast1-a", "asia-southeast1-b", "asia-southeast1-c",
    "asia-southeast2-a", "asia-southeast2-b", "asia-southeast2-c",
    "australia-southeast1-a", "australia-southeast1-b", "australia-southeast1-c",
    "australia-southeast2-a", "australia-southeast2-b", "australia-southeast2-c",
]

# Machine type to GPU/CPU details mapping
MACHINE_TYPES = {
    # ── GPU: Accelerator-Optimized & Guest-Accelerator VMs ──────────────────
    # A4X Max (GB300)
    "a4x-maxgpu-4g": {
        "gpu": "NVIDIA GB300",
        "chip": "GB300",
        "gpu_count": 4,
        "family": "A4X Max",
        "category": "GPU",
    },
    # A4X (GB200)
    "a4x-highgpu-4g": {
        "gpu": "NVIDIA GB200",
        "chip": "GB200",
        "gpu_count": 4,
        "family": "A4X",
        "category": "GPU",
    },
    # A4 (B200)
    "a4-highgpu-8g": {
        "gpu": "NVIDIA B200",
        "chip": "B200",
        "gpu_count": 8,
        "family": "A4",
        "category": "GPU",
    },
    # A3 Ultra (H200)
    "a3-ultragpu-8g": {
        "gpu": "NVIDIA H200 141GB",
        "chip": "H200",
        "gpu_count": 8,
        "family": "A3 Ultra",
        "category": "GPU",
    },
    # A3 Mega (H100)
    "a3-megagpu-8g": {
        "gpu": "NVIDIA H100 Mega 80GB",
        "chip": "H100",
        "gpu_count": 8,
        "family": "A3 Mega",
        "category": "GPU",
    },
    # A3 High (H100)
    "a3-highgpu-1g": {
        "gpu": "NVIDIA H100 80GB",
        "chip": "H100",
        "gpu_count": 1,
        "family": "A3 High",
        "category": "GPU",
    },
    "a3-highgpu-2g": {
        "gpu": "NVIDIA H100 80GB",
        "chip": "H100",
        "gpu_count": 2,
        "family": "A3 High",
        "category": "GPU",
    },
    "a3-highgpu-4g": {
        "gpu": "NVIDIA H100 80GB",
        "chip": "H100",
        "gpu_count": 4,
        "family": "A3 High",
        "category": "GPU",
    },
    "a3-highgpu-8g": {
        "gpu": "NVIDIA H100 80GB",
        "chip": "H100",
        "gpu_count": 8,
        "family": "A3 High",
        "category": "GPU",
    },
    # A3 Edge (H100)
    "a3-edgegpu-8g": {
        "gpu": "NVIDIA H100 80GB",
        "chip": "H100",
        "gpu_count": 8,
        "family": "A3 Edge",
        "category": "GPU",
    },
    # A2 Ultra (A100 80GB)
    "a2-ultragpu-1g": {
        "gpu": "NVIDIA A100 80GB",
        "chip": "A100 80GB",
        "gpu_count": 1,
        "family": "A2 Ultra",
        "category": "GPU",
        "accelerator_type": "nvidia-a100-80gb",
    },
    "a2-ultragpu-2g": {
        "gpu": "NVIDIA A100 80GB",
        "chip": "A100 80GB",
        "gpu_count": 2,
        "family": "A2 Ultra",
        "category": "GPU",
        "accelerator_type": "nvidia-a100-80gb",
    },
    "a2-ultragpu-4g": {
        "gpu": "NVIDIA A100 80GB",
        "chip": "A100 80GB",
        "gpu_count": 4,
        "family": "A2 Ultra",
        "category": "GPU",
        "accelerator_type": "nvidia-a100-80gb",
    },
    "a2-ultragpu-8g": {
        "gpu": "NVIDIA A100 80GB",
        "chip": "A100 80GB",
        "gpu_count": 8,
        "family": "A2 Ultra",
        "category": "GPU",
        "accelerator_type": "nvidia-a100-80gb",
    },
    # A2 Standard (A100 40GB)
    "a2-highgpu-1g": {
        "gpu": "NVIDIA A100 40GB",
        "chip": "A100 40GB",
        "gpu_count": 1,
        "family": "A2 Standard",
        "category": "GPU",
        "accelerator_type": "nvidia-tesla-a100",
    },
    "a2-highgpu-2g": {
        "gpu": "NVIDIA A100 40GB",
        "chip": "A100 40GB",
        "gpu_count": 2,
        "family": "A2 Standard",
        "category": "GPU",
        "accelerator_type": "nvidia-tesla-a100",
    },
    "a2-highgpu-4g": {
        "gpu": "NVIDIA A100 40GB",
        "chip": "A100 40GB",
        "gpu_count": 4,
        "family": "A2 Standard",
        "category": "GPU",
        "accelerator_type": "nvidia-tesla-a100",
    },
    "a2-highgpu-8g": {
        "gpu": "NVIDIA A100 40GB",
        "chip": "A100 40GB",
        "gpu_count": 8,
        "family": "A2 Standard",
        "category": "GPU",
        "accelerator_type": "nvidia-tesla-a100",
    },
    "a2-megagpu-16g": {
        "gpu": "NVIDIA A100 40GB",
        "chip": "A100 40GB",
        "gpu_count": 16,
        "family": "A2 Mega",
        "category": "GPU",
        "accelerator_type": "nvidia-tesla-a100",
    },
    # G4 (RTX PRO 6000)
    "g4-standard-48": {
        "gpu": "NVIDIA RTX PRO 6000",
        "chip": "RTX PRO 6000",
        "gpu_count": 1,
        "family": "G4",
        "category": "GPU",
    },
    "g4-standard-96": {
        "gpu": "NVIDIA RTX PRO 6000",
        "chip": "RTX PRO 6000",
        "gpu_count": 2,
        "family": "G4",
        "category": "GPU",
    },
    "g4-standard-192": {
        "gpu": "NVIDIA RTX PRO 6000",
        "chip": "RTX PRO 6000",
        "gpu_count": 4,
        "family": "G4",
        "category": "GPU",
    },
    "g4-standard-384": {
        "gpu": "NVIDIA RTX PRO 6000",
        "chip": "RTX PRO 6000",
        "gpu_count": 8,
        "family": "G4",
        "category": "GPU",
    },
    # G2 (L4)
    "g2-standard-4": {
        "gpu": "NVIDIA L4",
        "chip": "L4",
        "gpu_count": 1,
        "family": "G2",
        "category": "GPU",
        "accelerator_type": "nvidia-l4",
    },
    "g2-standard-8": {
        "gpu": "NVIDIA L4",
        "chip": "L4",
        "gpu_count": 1,
        "family": "G2",
        "category": "GPU",
        "accelerator_type": "nvidia-l4",
    },
    "g2-standard-12": {
        "gpu": "NVIDIA L4",
        "chip": "L4",
        "gpu_count": 1,
        "family": "G2",
        "category": "GPU",
        "accelerator_type": "nvidia-l4",
    },
    "g2-standard-16": {
        "gpu": "NVIDIA L4",
        "chip": "L4",
        "gpu_count": 1,
        "family": "G2",
        "category": "GPU",
        "accelerator_type": "nvidia-l4",
    },
    "g2-standard-24": {
        "gpu": "NVIDIA L4",
        "chip": "L4",
        "gpu_count": 2,
        "family": "G2",
        "category": "GPU",
        "accelerator_type": "nvidia-l4",
    },
    "g2-standard-32": {
        "gpu": "NVIDIA L4",
        "chip": "L4",
        "gpu_count": 1,
        "family": "G2",
        "category": "GPU",
        "accelerator_type": "nvidia-l4",
    },
    "g2-standard-48": {
        "gpu": "NVIDIA L4",
        "chip": "L4",
        "gpu_count": 4,
        "family": "G2",
        "category": "GPU",
        "accelerator_type": "nvidia-l4",
    },
    "g2-standard-96": {
        "gpu": "NVIDIA L4",
        "chip": "L4",
        "gpu_count": 8,
        "family": "G2",
        "category": "GPU",
        "accelerator_type": "nvidia-l4",
    },
    # N1 + T4 — guest accelerator GPUs
    "n1-standard-4-t4": {
        "gpu": "NVIDIA T4",
        "chip": "T4",
        "gpu_count": 1,
        "vcpus": 4,
        "memory_gb": 15,
        "family": "N1 (T4)",
        "category": "GPU",
        "accelerator_type": "nvidia-tesla-t4",
        "gce_machine_type": "n1-standard-4",
    },
    "n1-standard-8-t4": {
        "gpu": "NVIDIA T4",
        "chip": "T4",
        "gpu_count": 1,
        "vcpus": 8,
        "memory_gb": 30,
        "family": "N1 (T4)",
        "category": "GPU",
        "accelerator_type": "nvidia-tesla-t4",
        "gce_machine_type": "n1-standard-8",
    },
    "n1-standard-16-t4": {
        "gpu": "NVIDIA T4",
        "chip": "T4",
        "gpu_count": 2,
        "vcpus": 16,
        "memory_gb": 60,
        "family": "N1 (T4)",
        "category": "GPU",
        "accelerator_type": "nvidia-tesla-t4",
        "gce_machine_type": "n1-standard-16",
    },
    "n1-standard-32-t4": {
        "gpu": "NVIDIA T4",
        "chip": "T4",
        "gpu_count": 4,
        "vcpus": 32,
        "memory_gb": 120,
        "family": "N1 (T4)",
        "category": "GPU",
        "accelerator_type": "nvidia-tesla-t4",
        "gce_machine_type": "n1-standard-32",
    },
    # N1 + V100 — guest accelerator GPUs
    "n1-standard-4-v100": {
        "gpu": "NVIDIA V100 16GB",
        "chip": "V100",
        "gpu_count": 1,
        "vcpus": 4,
        "memory_gb": 15,
        "family": "N1 (V100)",
        "category": "GPU",
        "accelerator_type": "nvidia-tesla-v100",
        "gce_machine_type": "n1-standard-4",
    },
    "n1-standard-8-v100": {
        "gpu": "NVIDIA V100 16GB",
        "chip": "V100",
        "gpu_count": 2,
        "vcpus": 8,
        "memory_gb": 30,
        "family": "N1 (V100)",
        "category": "GPU",
        "accelerator_type": "nvidia-tesla-v100",
        "gce_machine_type": "n1-standard-8",
    },
    "n1-standard-16-v100": {
        "gpu": "NVIDIA V100 16GB",
        "chip": "V100",
        "gpu_count": 4,
        "vcpus": 16,
        "memory_gb": 60,
        "family": "N1 (V100)",
        "category": "GPU",
        "accelerator_type": "nvidia-tesla-v100",
        "gce_machine_type": "n1-standard-16",
    },
    "n1-standard-64-v100": {
        "gpu": "NVIDIA V100 16GB",
        "chip": "V100",
        "gpu_count": 8,
        "vcpus": 64,
        "memory_gb": 240,
        "family": "N1 (V100)",
        "category": "GPU",
        "accelerator_type": "nvidia-tesla-v100",
        "gce_machine_type": "n1-standard-64",
    },
}


# ── Programmatic CPU Machine Series Definitions ─────────────────────────────
# Format: (series_chip, family_label, category, processor_desc, subfamilies)
# subfamilies is a list of (subfamily_prefix, vcpu_counts, ram_per_vcpu_gb)
_CPU_SERIES_SPECS = [
    # General Purpose
    (
        "C4", "C4", "General Purpose", "Intel Xeon 5th/6th Gen (Emerald/Granite Rapids)",
        [
            ("c4-standard", [2, 4, 8, 16, 32, 48, 96, 144, 192, 288], 3.75),
            ("c4-highcpu",  [2, 4, 8, 16, 32, 48, 96, 144, 192, 288], 2.0),
            ("c4-highmem",  [2, 4, 8, 16, 32, 48, 96, 144, 192, 288], 7.75),
        ],
    ),
    (
        "C4A", "C4A", "General Purpose", "Google Axion Arm (Neoverse V2)",
        [
            ("c4a-standard", [1, 2, 4, 8, 16, 32, 48, 64, 72], 4.0),
            ("c4a-highcpu",  [1, 2, 4, 8, 16, 32, 48, 64, 72], 2.0),
            ("c4a-highmem",  [1, 2, 4, 8, 16, 32, 48, 64, 72], 8.0),
        ],
    ),
    (
        "C4D", "C4D", "General Purpose", "AMD EPYC 5th Gen (Turin)",
        [
            ("c4d-standard", [2, 4, 8, 16, 32, 48, 64, 96, 192, 384], 4.0),
            ("c4d-highcpu",  [2, 4, 8, 16, 32, 48, 64, 96, 192, 384], 2.0),
            ("c4d-highmem",  [2, 4, 8, 16, 32, 48, 64, 96, 192, 384], 8.0),
        ],
    ),
    (
        "N4", "N4", "General Purpose", "Intel Xeon 5th Gen (Emerald Rapids)",
        [
            ("n4-standard", [2, 4, 8, 16, 32, 48, 64, 80], 4.0),
            ("n4-highcpu",  [2, 4, 8, 16, 32, 48, 64, 80], 2.0),
            ("n4-highmem",  [2, 4, 8, 16, 32, 48, 64, 80], 8.0),
        ],
    ),
    (
        "N2", "N2", "General Purpose", "Intel Xeon (Ice Lake / Cascade Lake)",
        [
            ("n2-standard", [2, 4, 8, 16, 32, 48, 64, 80, 96, 128], 4.0),
            ("n2-highcpu",  [2, 4, 8, 16, 32, 48, 64, 80, 96], 1.0),
            ("n2-highmem",  [2, 4, 8, 16, 32, 48, 64, 80, 96, 128], 8.0),
        ],
    ),
    (
        "N2D", "N2D", "General Purpose", "AMD EPYC (Milan / Rome)",
        [
            ("n2d-standard", [2, 4, 8, 16, 32, 48, 64, 80, 96, 128, 224], 4.0),
            ("n2d-highcpu",  [2, 4, 8, 16, 32, 48, 64, 80, 96, 128, 224], 1.0),
            ("n2d-highmem",  [2, 4, 8, 16, 32, 48, 64, 80, 96], 8.0),
        ],
    ),
    (
        "E2", "E2", "General Purpose", "Cost-Optimized General Purpose",
        [
            ("e2-standard", [2, 4, 8, 16, 32], 4.0),
            ("e2-highcpu",  [2, 4, 8, 16, 32], 1.0),
            ("e2-highmem",  [2, 4, 8, 16], 8.0),
        ],
    ),
    (
        "T2D", "T2D", "General Purpose", "Tau AMD EPYC (Milan Scale-Out)",
        [
            ("t2d-standard", [1, 2, 4, 8, 16, 32, 48, 60], 4.0),
        ],
    ),
    (
        "T2A", "T2A", "General Purpose", "Tau Ampere Altra Arm",
        [
            ("t2a-standard", [1, 2, 4, 8, 16, 32, 48], 4.0),
        ],
    ),
    (
        "N1", "N1", "General Purpose", "Intel Xeon (Skylake / Broadwell)",
        [
            ("n1-standard", [1, 2, 4, 8, 16, 32, 64, 96], 3.75),
            ("n1-highcpu",  [2, 4, 8, 16, 32, 64, 96], 0.9),
            ("n1-highmem",  [2, 4, 8, 16, 32, 64, 96], 6.5),
        ],
    ),
    # Compute-Optimized
    (
        "C3", "C3", "Compute-Optimized", "Intel Xeon 4th Gen (Sapphire Rapids)",
        [
            ("c3-standard", [4, 8, 22, 44, 88, 176], 4.0),
            ("c3-highcpu",  [4, 8, 22, 44, 88, 176], 2.0),
            ("c3-highmem",  [4, 8, 22, 44, 88, 176], 8.0),
        ],
    ),
    (
        "C3D", "C3D", "Compute-Optimized", "AMD EPYC 4th Gen (Genoa)",
        [
            ("c3d-standard", [4, 8, 16, 30, 60, 90, 180, 360], 4.0),
            ("c3d-highcpu",  [4, 8, 16, 30, 60, 90, 180, 360], 2.0),
            ("c3d-highmem",  [4, 8, 16, 30, 60, 90, 180, 360], 8.0),
        ],
    ),
    (
        "H3", "H3", "Compute-Optimized", "HPC-Optimized Intel Xeon (Sapphire Rapids)",
        [
            ("h3-standard", [88], 4.0),
        ],
    ),
    (
        "C2", "C2", "Compute-Optimized", "Intel Xeon (Cascade Lake Compute-Optimized)",
        [
            ("c2-standard", [4, 8, 16, 30, 60], 4.0),
        ],
    ),
    (
        "C2D", "C2D", "Compute-Optimized", "AMD EPYC (Milan Compute-Optimized)",
        [
            ("c2d-standard", [2, 4, 8, 16, 32, 56, 112], 4.0),
            ("c2d-highcpu",  [2, 4, 8, 16, 32, 56, 112], 2.0),
            ("c2d-highmem",  [2, 4, 8, 16, 32, 56, 112], 8.0),
        ],
    ),
    # Memory-Optimized
    (
        "M4", "M4", "Memory-Optimized", "Intel Xeon 5th Gen Memory-Optimized",
        [
            ("m4-megamem",  [28, 56, 112, 224], 13.3),
            ("m4-ultramem", [56, 112, 224], 26.6),
        ],
    ),
    (
        "M3", "M3", "Memory-Optimized", "Intel Xeon (Ice Lake Memory-Optimized)",
        [
            ("m3-megamem",  [64, 128], 15.25),
            ("m3-ultramem", [32, 64, 128], 30.5),
        ],
    ),
    (
        "M2", "M2", "Memory-Optimized", "Intel Xeon (Cascade Lake Ultra-Memory)",
        [
            ("m2-ultramem", [208, 416], 28.3),
            ("m2-megamem",  [416], 14.1),
            ("m2-hypermem", [416], 21.2),
        ],
    ),
    (
        "M1", "M1", "Memory-Optimized", "Intel Xeon (Skylake Memory-Optimized)",
        [
            ("m1-megamem",  [96], 14.9),
            ("m1-ultramem", [40, 80, 160], 24.0),
        ],
    ),
    (
        "X4", "X4", "Memory-Optimized", "Intel Xeon 4th Gen Extreme Memory (16–32 TB)",
        [
            ("x4-megamem", [960, 1440, 1920], 17.0),
        ],
    ),
    # Storage-Optimized
    (
        "Z3", "Z3", "Storage-Optimized", "Intel Xeon 4th Gen + Titanium SSD Storage-Optimized",
        [
            ("z3-highmem", [88, 176], 8.0),
        ],
    ),
]

# Shared-core E2 types
for _mt, _vcpus, _mem in [
    ("e2-micro", 2, 1),
    ("e2-small", 2, 2),
    ("e2-medium", 2, 4),
]:
    MACHINE_TYPES[_mt] = {
        "gpu": "Cost-Optimized General Purpose",
        "chip": "E2",
        "gpu_count": 0,
        "vcpus": _vcpus,
        "memory_gb": _mem,
        "family": "E2",
        "category": "General Purpose",
    }

for _chip, _family, _category, _desc, _subfamilies in _CPU_SERIES_SPECS:
    for _prefix, _counts, _ram_ratio in _subfamilies:
        for _vcpu in _counts:
            _mt_name = f"{_prefix}-{_vcpu}"
            _mem_gb = round(_vcpu * _ram_ratio, 1)
            if _mem_gb == int(_mem_gb):
                _mem_gb = int(_mem_gb)
            MACHINE_TYPES[_mt_name] = {
                "gpu": _desc,
                "chip": _chip,
                "gpu_count": 0,
                "vcpus": _vcpu,
                "memory_gb": _mem_gb,
                "family": _family,
                "category": _category,
            }


# GPU & CPU family to supported zones mapping
GPU_ZONES = {
    "A4X Max (GB300)": [
        "us-central1-b", "us-east4-b", "us-east5-c"
    ],
    "A4X (GB200)": [
        "us-central1-a"
    ],
    "A4 (B200)": [
        "asia-northeast1-b", "asia-southeast1-b", "europe-west4-b",
        "us-central1-b", "us-east1-b", "us-east4-b", "us-south1-b",
        "us-west2-c", "us-west3-b", "us-west3-c"
    ],
    "A3 Ultra (H200)": [
        "asia-south1-b", "asia-south2-c", "europe-west1-b", "europe-west4-a",
        "us-central1-b", "us-east1-d", "us-east4-b", "us-east5-a",
        "us-south1-b", "us-west1-c"
    ],
    "A3 Edge (H100)": [
        "asia-east1-a", "asia-east1-b", "asia-east1-c",
        "asia-northeast1-b", "asia-southeast1-a", "asia-southeast1-b",
        "europe-west1-b", "europe-west1-c", "europe-west4-a", "europe-west4-b",
        "me-west1-b",
        "us-central1-a", "us-central1-b", "us-central1-c",
        "us-east1-b", "us-east1-c", "us-east4-a", "us-east4-b",
        "us-west1-a", "us-west1-b"
    ],
    "A3 Mega (H100)": [
        "asia-east1-c", "asia-northeast1-b", "asia-southeast1-b",
        "asia-southeast1-c", "australia-southeast1-c", "europe-west1-b",
        "europe-west1-c", "europe-west4-b", "europe-west4-c",
        "us-central1-a", "us-central1-b", "us-central1-c",
        "us-east4-a", "us-east4-b", "us-east4-c", "us-east5-a",
        "us-west1-a", "us-west1-b", "us-west4-a"
    ],
    "A3 High (H100)": [
        "asia-east1-c", "asia-northeast1-b", "asia-southeast1-b",
        "asia-southeast1-c", "europe-west1-b", "europe-west1-c",
        "europe-west4-c", "us-central1-a", "us-central1-c",
        "us-east4-a", "us-east4-b", "us-east5-a",
        "us-west1-a", "us-west1-b", "us-west4-a"
    ],
    "A2 Ultra (A100 80GB)": [
        "asia-southeast1-c", "europe-west4-a", "us-central1-a",
        "us-central1-c", "us-east4-c", "us-east5-a"
    ],
    "A2 Standard (A100 40GB)": [
        "asia-northeast1-a", "asia-northeast1-c", "asia-northeast3-b",
        "asia-southeast1-b", "asia-southeast1-c", "europe-west4-a",
        "europe-west4-b", "me-west1-a", "me-west1-c",
        "us-central1-a", "us-central1-b", "us-central1-c", "us-central1-f",
        "us-east1-b", "us-west1-b", "us-west3-b", "us-west4-b"
    ],
    "G4 (RTX PRO 6000)": [
        "asia-south2-c", "asia-southeast1-b", "asia-southeast1-c",
        "asia-southeast2-b", "asia-southeast2-c", "europe-north1-a",
        "europe-west1-c", "europe-west2-b", "europe-west4-a", "europe-west4-b",
        "europe-west4-c", "europe-west8-b", "us-central1-b", "us-central1-f",
        "us-east1-b", "us-east4-c", "us-east5-a", "us-east5-b", "us-east5-c",
        "us-south1-a", "us-south1-b", "us-west1-b", "us-west1-c",
        "us-west3-a", "us-west4-a"
    ],
    "G2 (L4)": [
        "asia-east1-a", "asia-east1-b", "asia-east1-c",
        "asia-northeast1-a", "asia-northeast1-b", "asia-northeast1-c",
        "asia-northeast3-a", "asia-northeast3-b",
        "asia-south1-a", "asia-south1-b", "asia-south1-c",
        "asia-southeast1-a", "asia-southeast1-b", "asia-southeast1-c",
        "europe-west1-b", "europe-west1-c",
        "europe-west2-a", "europe-west2-b",
        "europe-west3-a", "europe-west3-b",
        "europe-west4-a", "europe-west4-b", "europe-west4-c",
        "europe-west6-b", "europe-west6-c",
        "me-central2-a", "me-central2-c",
        "northamerica-northeast2-a", "northamerica-northeast2-b",
        "us-central1-a", "us-central1-b", "us-central1-c", "us-central1-f",
        "us-east1-b", "us-east1-c",
        "us-east4-a", "us-east4-c",
        "us-west1-a", "us-west1-b", "us-west1-c",
        "us-west4-a", "us-west4-c"
    ],
    "N1 (T4)": [
        "asia-east1-a", "asia-east1-c",
        "asia-east2-a", "asia-east2-c",
        "asia-northeast1-a", "asia-northeast1-c",
        "asia-northeast3-b", "asia-northeast3-c",
        "asia-south1-a", "asia-south1-b",
        "asia-southeast1-a", "asia-southeast1-b", "asia-southeast1-c",
        "asia-southeast2-a", "asia-southeast2-b",
        "australia-southeast1-a", "australia-southeast1-c",
        "europe-central2-b", "europe-central2-c",
        "europe-west1-b", "europe-west1-c", "europe-west1-d",
        "europe-west2-a", "europe-west2-b",
        "europe-west3-b",
        "europe-west4-a", "europe-west4-b", "europe-west4-c",
        "me-west1-b", "me-west1-c",
        "northamerica-northeast1-c",
        "southamerica-east1-a", "southamerica-east1-b", "southamerica-east1-c",
        "us-central1-a", "us-central1-b", "us-central1-c", "us-central1-f",
        "us-east1-b", "us-east1-c", "us-east1-d",
        "us-east4-a", "us-east4-b", "us-east4-c",
        "us-west1-a", "us-west1-b",
        "us-west2-b", "us-west2-c",
        "us-west3-b",
        "us-west4-a", "us-west4-b"
    ],
    "N1 (V100)": [
        "asia-east1-c", "europe-west4-a", "europe-west4-b", "europe-west4-c",
        "us-central1-a", "us-central1-b", "us-central1-c", "us-central1-f",
        "us-east1-c", "us-west1-a", "us-west1-b",
    ],
    "CPU (Global)": COMMON_CPU_ZONES,
}

# Map machine type to its family for zone lookup
MACHINE_TO_FAMILY = {mt: info["family"] for mt, info in MACHINE_TYPES.items()}

# Which families map to which GPU_ZONES key
FAMILY_TO_GPU_ZONE_KEY = {
    "A4X Max": "A4X Max (GB300)",
    "A4X": "A4X (GB200)",
    "A4": "A4 (B200)",
    "A3 Ultra": "A3 Ultra (H200)",
    "A3 Edge": "A3 Edge (H100)",
    "A3 Mega": "A3 Mega (H100)",
    "A3 High": "A3 High (H100)",
    "A2 Ultra": "A2 Ultra (A100 80GB)",
    "A2 Standard": "A2 Standard (A100 40GB)",
    "A2 Mega": "A2 Standard (A100 40GB)",
    "G4": "G4 (RTX PRO 6000)",
    "G2": "G2 (L4)",
    "N1 (T4)": "N1 (T4)",
    "N1 (V100)": "N1 (V100)",
}
for _chip, _family, *_ in _CPU_SERIES_SPECS:
    FAMILY_TO_GPU_ZONE_KEY[_family] = "CPU (Global)"

# Consumption model support matrix
CONSUMPTION_SUPPORT = {
    "on_demand": {
        "A4X Max": False, "A4X": True, "A4": False,
        "A3 Ultra": False, "A3 Edge": True, "A3 Mega": True, "A3 High": True,
        "A2 Ultra": True, "A2 Standard": True, "A2 Mega": True,
        "G4": True, "G2": True, "N1 (T4)": True, "N1 (V100)": True,
    },
    "spot": {
        "A4X Max": True, "A4X": True, "A4": True,
        "A3 Ultra": True, "A3 Edge": True, "A3 Mega": True, "A3 High": True,
        "A2 Ultra": True, "A2 Standard": True, "A2 Mega": True,
        "G4": True, "G2": True, "N1 (T4)": True, "N1 (V100)": True,
    },
    "dws_calendar": {
        "A4X Max": False, "A4X": False, "A4": True,
        "A3 Ultra": True, "A3 Edge": True, "A3 Mega": True, "A3 High": True,
        "A2 Ultra": False, "A2 Standard": False, "A2 Mega": False,
        "G4": False, "G2": False, "N1 (T4)": False, "N1 (V100)": False,
    },
    "dws_flex": {
        "A4X Max": True, "A4X": True, "A4": True,
        "A3 Ultra": True, "A3 Edge": True, "A3 Mega": True, "A3 High": True,
        "A2 Ultra": False, "A2 Standard": False, "A2 Mega": False,
        "G4": True, "G2": True, "N1 (T4)": True, "N1 (V100)": True,
    },
}
# Enable all consumption models for all CPU families so users can query any advisory or scan mode
for _chip, _family, *_ in _CPU_SERIES_SPECS:
    for _mode in ("on_demand", "spot", "dws_calendar", "dws_flex"):
        CONSUMPTION_SUPPORT[_mode][_family] = True

# TPU types, zones, machine types, and consumption model support
TPU_TYPES = {
    "v6e": {
        "gpu": "Cloud TPU v6e (Trillium)",
        "accelerator_prefix": "v6e",
        "zones": ["asia-northeast1-b", "europe-west4-a", "southamerica-west1-a",
                   "us-central1-b", "us-east1-d", "us-east5-a", "us-east5-b"],
        "machine_types": {
            "ct6e-standard-1t": {"chips": 1, "vcpus": 44, "memory_gb": 176, "hbm_gb": 32},
            "ct6e-standard-4t": {"chips": 4, "vcpus": 180, "memory_gb": 720, "hbm_gb": 128},
            "ct6e-standard-8t": {"chips": 8, "vcpus": 180, "memory_gb": 1440, "hbm_gb": 256},
        },
        "topologies": ["1x1", "2x2", "2x4", "4x4", "4x8", "8x8", "8x16", "16x16"],
        "supported": {"on_demand": True, "spot": True, "dws_calendar": True, "dws_flex": True},
    },
    "v5p": {
        "gpu": "Cloud TPU v5p (Viperfish)",
        "accelerator_prefix": "v5p",
        "zones": ["europe-west4-b", "us-central1-a", "us-east5-a"],
        "machine_types": {
            "ct5p-hightpu-1t": {"chips": 1, "vcpus": 52, "memory_gb": 112, "hbm_gb": 95},
            "ct5p-hightpu-2t": {"chips": 2, "vcpus": 104, "memory_gb": 224, "hbm_gb": 190},
            "ct5p-hightpu-4t": {"chips": 4, "vcpus": 208, "memory_gb": 448, "hbm_gb": 380},
        },
        "topologies": ["2x2x1", "2x2x2", "2x2x4", "2x4x4", "4x4x4"],
        "supported": {"on_demand": True, "spot": True, "dws_calendar": True, "dws_flex": True},
    },
    "v5e": {
        "gpu": "Cloud TPU v5e (Viperlite)",
        "accelerator_prefix": "v5litepod",
        "zones": ["europe-west4-b", "us-central1-a", "us-south1-a",
                   "us-west1-c", "us-west4-a"],
        "machine_types": {
            "ct5e-hightpu-1t": {"chips": 1, "vcpus": 24, "memory_gb": 48, "hbm_gb": 16},
            "ct5e-hightpu-4t": {"chips": 4, "vcpus": 112, "memory_gb": 192, "hbm_gb": 64},
            "ct5e-hightpu-8t": {"chips": 8, "vcpus": 224, "memory_gb": 384, "hbm_gb": 128},
        },
        "topologies": ["1x1", "2x2", "2x4", "4x4", "4x8", "8x8", "8x16", "16x16"],
        "supported": {"on_demand": True, "spot": True, "dws_calendar": True, "dws_flex": True},
    },
    "v4": {
        "gpu": "Cloud TPU v4 (Pufferfish)",
        "accelerator_prefix": "v4",
        "zones": ["us-central2-b"],
        "machine_types": {
            "ct4p-hightpu-4t": {"chips": 4, "vcpus": 240, "memory_gb": 408, "hbm_gb": 128},
        },
        "topologies": ["2x2x1", "2x2x2", "2x2x4", "2x4x4", "4x4x4"],
        "supported": {"on_demand": True, "spot": True, "dws_calendar": False, "dws_flex": True},
    },
    "v3": {
        "gpu": "Cloud TPU v3 (Dragonfish)",
        "accelerator_prefix": "v3",
        "zones": ["europe-west4-a", "us-central1-a", "us-central1-b"],
        "machine_types": {
            "v3-8": {"chips": 4, "vcpus": 96, "memory_gb": 340, "hbm_gb": 64},
        },
        "topologies": ["2x2", "4x4", "4x8", "8x8"],
        "supported": {"on_demand": True, "spot": True, "dws_calendar": False, "dws_flex": False},
    },
    "v2": {
        "gpu": "Cloud TPU v2 (Jellyfish)",
        "accelerator_prefix": "v2",
        "zones": ["asia-east1-c", "europe-west4-a", "us-central1-a",
                   "us-central1-b", "us-central1-c"],
        "machine_types": {
            "v2-8": {"chips": 4, "vcpus": 96, "memory_gb": 340, "hbm_gb": 32},
        },
        "topologies": ["2x2", "4x4", "4x8", "8x8"],
        "supported": {"on_demand": True, "spot": True, "dws_calendar": False, "dws_flex": False},
    },
}


def get_gce_machine_type(machine_type: str) -> str:
    """Return the underlying GCE machineType string (e.g. 'n1-standard-4-t4' -> 'n1-standard-4')."""
    info = MACHINE_TYPES.get(machine_type)
    if info and info.get("gce_machine_type"):
        return info["gce_machine_type"]
    return machine_type


def is_valid_machine_type(machine_type: str) -> bool:
    """Return True if machine_type is in our catalog OR matches a valid GCE machine type pattern."""
    if not machine_type:
        return False
    if machine_type in MACHINE_TYPES:
        return True
    if any(machine_type in t.get("machine_types", {}) for t in TPU_TYPES.values()):
        return True
    return bool(re.match(r"^[a-z][a-z0-9-]{1,62}$", machine_type))


def infer_family_from_machine_type(machine_type: str) -> str:
    """Infer the machine family from a machine type string, even for custom/unlisted types."""
    if machine_type in MACHINE_TO_FAMILY:
        return MACHINE_TO_FAMILY[machine_type]
    prefix = machine_type.split("-", 1)[0].upper()
    if prefix in FAMILY_TO_GPU_ZONE_KEY:
        return prefix
    return prefix or "Custom"


def get_zones_for_machine_type(machine_type: str) -> list[str]:
    """Get supported zones for a given machine type (GPU, TPU, CPU, or Custom)."""
    # Check TPU machine types (ct6e-standard-1t, ct5p-hightpu-4t, v3-8, etc.)
    for tpu_type, tpu_info in TPU_TYPES.items():
        if machine_type in tpu_info.get("machine_types", {}):
            return tpu_info["zones"]
    # Known GPU or CPU machine types
    family = MACHINE_TO_FAMILY.get(machine_type)
    if not family:
        family = infer_family_from_machine_type(machine_type)
    gpu_zone_key = FAMILY_TO_GPU_ZONE_KEY.get(family)
    if gpu_zone_key and gpu_zone_key in GPU_ZONES:
        return GPU_ZONES[gpu_zone_key]
    # Fallback for any custom or newly released GCE machine type
    if is_valid_machine_type(machine_type):
        return COMMON_CPU_ZONES
    return []


def is_consumption_supported(machine_type: str, consumption_model: str) -> bool:
    """Check if a consumption model is supported for a given machine type."""
    # Check TPU types first
    for tpu_type, tpu_info in TPU_TYPES.items():
        if machine_type in tpu_info.get("machine_types", {}):
            return tpu_info.get("supported", {}).get(consumption_model, False)
    # Known GPU / CPU types
    family = MACHINE_TO_FAMILY.get(machine_type)
    if not family:
        family = infer_family_from_machine_type(machine_type)
    model_support = CONSUMPTION_SUPPORT.get(consumption_model, {})
    if family in model_support:
        return model_support[family]
    # Default to True for custom GCE machine types so users are not blocked
    return is_valid_machine_type(machine_type)


def get_all_machine_types_info() -> list[dict]:
    """Return all machine types with their info for the frontend."""
    result = []
    for mt, info in MACHINE_TYPES.items():
        family = info["family"]
        gpu_zone_key = FAMILY_TO_GPU_ZONE_KEY.get(family, "CPU (Global)")
        zones = GPU_ZONES.get(gpu_zone_key, COMMON_CPU_ZONES)
        regions = sorted(set(z.rsplit("-", 1)[0] for z in zones))
        entry = {
            "machineType": mt,
            "gpu": info["gpu"],
            "chip": info.get("chip", ""),
            "gpuCount": info["gpu_count"],
            "family": family,
            "category": info.get("category", "GPU"),
            "zones": zones,
            "regions": regions,
            "supported": {
                "on_demand": is_consumption_supported(mt, "on_demand"),
                "spot": is_consumption_supported(mt, "spot"),
                "dws_calendar": is_consumption_supported(mt, "dws_calendar"),
                "dws_flex": is_consumption_supported(mt, "dws_flex"),
            },
        }
        if info.get("vcpus") is not None:
            entry["vcpus"] = info["vcpus"]
        if info.get("memory_gb") is not None:
            entry["memoryGb"] = info["memory_gb"]
        result.append(entry)
    # Add TPU entries from machine_types
    for tpu_type, tpu_info in TPU_TYPES.items():
        supported = tpu_info.get("supported", {})
        for mt_name, mt_spec in tpu_info.get("machine_types", {}).items():
            result.append({
                "machineType": mt_name,
                "gpu": tpu_info.get("gpu", f"Cloud TPU {tpu_type}"),
                "chip": tpu_type,
                "gpuCount": mt_spec["chips"],
                "family": f"TPU {tpu_type}",
                "category": "TPU",
                "zones": tpu_info["zones"],
                "regions": sorted(set(z.rsplit("-", 1)[0] for z in tpu_info["zones"])),
                "vcpus": mt_spec.get("vcpus"),
                "memoryGb": mt_spec.get("memory_gb"),
                "hbmGb": mt_spec.get("hbm_gb"),
                "topologies": tpu_info.get("topologies", []),
                "supported": supported,
            })
    return result


def get_chip_groups() -> dict:
    """Return machine types grouped by chip/series across all compute categories."""
    gpu_chips = {}
    cpu_series = {}
    for mt, info in MACHINE_TYPES.items():
        chip = info.get("chip", info["gpu"])
        category = info.get("category", "GPU")
        family = info["family"]
        gpu_zone_key = FAMILY_TO_GPU_ZONE_KEY.get(family, "CPU (Global)")
        zones = GPU_ZONES.get(gpu_zone_key, COMMON_CPU_ZONES)
        regions = sorted(set(z.rsplit("-", 1)[0] for z in zones))
        target = gpu_chips if category == "GPU" else cpu_series
        if chip not in target:
            target[chip] = {
                "chip": chip,
                "gpu": info["gpu"],
                "category": category,
                "machineTypes": [],
            }
        mt_item = {
            "machineType": mt,
            "gpuCount": info["gpu_count"],
            "family": family,
            "zones": zones,
            "regions": regions,
        }
        if info.get("vcpus") is not None:
            mt_item["vcpus"] = info["vcpus"]
        if info.get("memory_gb") is not None:
            mt_item["memoryGb"] = info["memory_gb"]
        target[chip]["machineTypes"].append(mt_item)

    tpu_chips = {}
    for tpu_type, tpu_info in TPU_TYPES.items():
        tpu_chips[tpu_type] = {
            "chip": tpu_type,
            "gpu": f"Cloud TPU {tpu_type}",
            "category": "TPU",
            "zones": tpu_info["zones"],
            "regions": sorted(set(z.rsplit("-", 1)[0] for z in tpu_info["zones"])),
        }

    return {
        "gpuChips": list(gpu_chips.values()),
        "tpuChips": list(tpu_chips.values()),
        "cpuSeries": list(cpu_series.values()),
    }
