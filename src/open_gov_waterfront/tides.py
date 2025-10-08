"""
Tide harmonic synthesis (simple constituent sum).

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Constituent:
    amp_m: float
    omega_rad_s: float
    phase_rad: float


def tide_series(
    start_s: float, duration_s: float, dt_s: float, constituents: list[Constituent]
) -> tuple[np.ndarray, np.ndarray]:
    """
    Return (t_seconds, eta_m): sum of A cos(omega t + phase) from t=0.
    """
    if duration_s <= 0 or dt_s <= 0:
        raise ValueError("duration and dt must be > 0")
    t = np.arange(0.0, duration_s + 1e-9, dt_s, dtype=float)
    eta = np.zeros_like(t)
    for c in constituents:
        eta += c.amp_m * np.cos(c.omega_rad_s * t + c.phase_rad)
    return t, eta
