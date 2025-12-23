from dataclasses import dataclass
import numpy as np

@dataclass
class MusicIntent:
    """
    High-level musical forces derived from semantics.
    """
    duration_seconds: int

    # Time-varying
    intensity_curve: np.ndarray     # shape (T,) 0–1
    tension_curve: np.ndarray       # shape (T,) 0–1
    density_curve: np.ndarray       # shape (T,) 0–1

    # Global
    tempo_base: int
    harmonic_color: str             # "bright", "dark", "ambiguous"
    motion_profile: str             # "drift", "rise", "wave", "collapse"
    emotional_vector: np.ndarray    # [valence, arousal, tension]
