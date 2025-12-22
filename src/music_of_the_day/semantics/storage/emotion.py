from pathlib import Path
from datetime import date, datetime, timedelta
import json
from typing import Optional

from music_of_the_day.semantics.emotion import EmotionState

BASE_DIR = Path("data/processed/emotion")
BASE_DIR.mkdir(parents=True, exist_ok=True)


def _serialize(emotion: EmotionState) -> dict:
    return {
        "valence": float(emotion.valence),
        "arousal": float(emotion.arousal),
        "tension": float(emotion.tension),
    }


def _deserialize(data: dict) -> EmotionState:
    return EmotionState(
        valence=float(data["valence"]),
        arousal=float(data["arousal"]),
        tension=float(data["tension"]),
    )


def save_emotion(emotion: EmotionState, day: date | str | None = None) -> Path:
    """
    Save emotion for a given day (or today) and update latest.json.
    """
    if day is None:
        day = date.today()
    elif isinstance(day, str):
        day = datetime.fromisoformat(day).date()

    path = BASE_DIR / f"{day.isoformat()}.json"
    payload = _serialize(emotion)

    path.write_text(json.dumps(payload, indent=2))

    # Update latest.json
    latest_path = BASE_DIR / "latest.json"
    latest_path.write_text(json.dumps(payload, indent=2))

    return path


def load_emotion(day: date | str | None = None) -> Optional[EmotionState]:
    """
    Load emotion for a specific day. Defaults to today.
    """
    if day is None:
        day = date.today()
    elif isinstance(day, str):
        day = datetime.fromisoformat(day).date()

    path = BASE_DIR / f"{day.isoformat()}.json"
    if not path.exists():
        return None

    return _deserialize(json.loads(path.read_text()))


def load_yesterday_emotion() -> Optional[EmotionState]:
    """
    Load yesterday's emotion if available.
    """
    yesterday = date.today() - timedelta(days=1)
    return load_emotion(yesterday)


def load_latest_emotion() -> Optional[EmotionState]:
    """
    Load most recent emotion, fallback to yesterday.
    """
    latest_path = BASE_DIR / "latest.json"
    if latest_path.exists():
        return _deserialize(json.loads(latest_path.read_text()))
    return load_yesterday_emotion()
