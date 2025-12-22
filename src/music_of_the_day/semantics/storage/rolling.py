import numpy as np
from pathlib import Path
from datetime import date, timedelta

BASE_DIR = Path("data/processed/embeddings/rolling")
BASE_DIR.mkdir(parents=True, exist_ok=True)

def save_embeddings(embeddings: np.ndarray, day: date = None):
    """
    Save today's embeddings to disk.
    """
    day = day or date.today()
    path = BASE_DIR / f"{day.isoformat()}.npy"
    np.save(path, embeddings)

    # Update 'latest.npy' for convenience
    latest_path = BASE_DIR / "latest.npy"
    np.save(latest_path, embeddings)
    return path

def load_embeddings(day: date = None):
    """
    Load embeddings for a specific day. Defaults to today.
    """
    day = day or date.today()
    path = BASE_DIR / f"{day.isoformat()}.npy"
    if path.exists():
        return np.load(path)
    return None

def load_yesterday_embeddings():
    """
    Load yesterday's embeddings, or None if not found.
    """
    yesterday = date.today() - timedelta(days=1)
    return load_embeddings(yesterday)

def load_latest_embeddings():
    """
    Load latest embeddings (most recent), fallback to yesterday if missing.
    """
    latest_path = BASE_DIR / "latest.npy"
    if latest_path.exists():
        return np.load(latest_path)
    return load_yesterday_embeddings()

def load_last_n_days(n: int = 14):
    """
    Returns an array of embeddings for the last n days (ignores missing days).
    """
    today = date.today()
    embeddings_list = []
    for delta in range(1, n+1):
        day = today - timedelta(days=delta)
        emb = load_embeddings(day)
        if emb is not None:
            embeddings_list.append(emb)
    if embeddings_list:
        return np.vstack(embeddings_list)
    return None

def compute_rolling_average(n: int = 14):
    last_embeddings = load_last_n_days(n)
    if last_embeddings is not None:
        return np.mean(last_embeddings, axis=0, keepdims=True)  # average vector
    return None