"""
Seawall sliding factor of safety (screening).

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations


def sliding_fs(mu: float, W_kN: float, T_kN: float) -> float:
    """
    Factor of safety against sliding: FS = (mu * W) / T
    """
    if mu <= 0 or W_kN <= 0 or T_kN <= 0:
        raise ValueError("mu, W, T must be > 0")
    return float((mu * W_kN) / T_kN)
