from typing import List, Dict, Any
from .real_historical_data import REAL_HISTORICAL_TRAGEDIES_DATASET
from .kaggle_dataset import KAGGLE_STEFANINI_DATASET

DATASET_REGISTRY = {
    "real_historical": {
        "key": "real_historical",
        "title": "Real Indian O&G Historical Tragedies (Precursor Analysis)",
        "description": "Real historical precursor observations from Baghjan, BHN, HPCL, and GAIL disasters.",
        "records": REAL_HISTORICAL_TRAGEDIES_DATASET
    },
    "kaggle_stefanini": {
        "key": "kaggle_stefanini",
        "title": "Kaggle IHM Stefanini Industrial Safety (Top 20 Samples)",
        "description": "Open source global mining/metals safety database mapped to SIF-Sentinel NLP.",
        "records": KAGGLE_STEFANINI_DATASET
    }
}

def get_demo_batch() -> List[Dict[str, Any]]:
    return [dict(item) for item in REAL_HISTORICAL_TRAGEDIES_DATASET]

def get_dataset_by_key(dataset_key: str) -> List[Dict[str, Any]]:
    ds = DATASET_REGISTRY.get(dataset_key, DATASET_REGISTRY["real_historical"])
    return [dict(item) for item in ds["records"]]

def list_available_datasets() -> List[Dict[str, Any]]:
    return [
        {
            "key": k,
            "title": v["title"],
            "description": v["description"],
            "count": len(v["records"])
        }
        for k, v in DATASET_REGISTRY.items()
    ]
