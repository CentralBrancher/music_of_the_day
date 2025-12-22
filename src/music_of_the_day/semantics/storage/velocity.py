from pathlib import Path
from datetime import date, timedelta

BASE_DIR = Path("data/processed/velocities")
BASE_DIR.mkdir(parents=True, exist_ok=True)


def save_velocity(velocity: float, day: date = None) -> Path:
    """
    Save today's velocity as a float to a .txt file.
    Also updates 'latest.txt' for convenience.
    """
    day = day or date.today()
    path = BASE_DIR / f"{day.isoformat()}.txt"
    path.write_text(f"{velocity:.6f}")  # save float with precision

    # Update latest.txt
    latest_path = BASE_DIR / "latest.txt"
    latest_path.write_text(f"{velocity:.6f}")

    return path


def load_velocity(day: date = None) -> float | None:
    """
    Load velocity for a specific day (float). Defaults to today.
    Returns None if file not found.
    """
    day = day or date.today()
    path = BASE_DIR / f"{day.isoformat()}.txt"
    if path.exists():
        return float(path.read_text().strip())
    return None


def load_yesterday_velocity() -> float | None:
    """
    Load yesterday's velocity, or None if not found.
    """
    yesterday = date.today() - timedelta(days=1)
    return load_velocity(yesterday)


def load_latest_velocity() -> float | None:
    """
    Load latest velocity (most recent day). Falls back to yesterday if missing.
    """
    latest_path = BASE_DIR / "latest.txt"
    if latest_path.exists():
        return float(latest_path.read_text().strip())
    return load_yesterday_velocity()
