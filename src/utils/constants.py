"""
Global Constants for TRIGNUM-300M
"""

# Default thresholds
DEFAULT_CONFIDENCE_THRESHOLD = 0.5

# Standard Universal Illogics (Level 1)
LOGIC_CONTRADICTION = "Contradiction"
LOGIC_CIRCULAR = "Circular Reference"
LOGIC_FALSE_DICHOTOMY = "False Dichotomy"
LOGIC_NON_SEQUITUR = "Non-sequitur"
LOGIC_BEGGING_QUESTION = "Begging the Question"

# API & Dataset
HF_DATASETS_API_BASE = "https://datasets-server.huggingface.co/rows"
DEFAULT_DATASET_LIMIT = 100

# File Paths
DEFAULT_LOG_DIR = "logs/"
DEFAULT_METRICS_OUT = "benchmarks/results/"
