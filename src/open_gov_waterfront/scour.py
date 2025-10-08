"""
Local scour estimate at piles (screening).

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from .utils import g


def pile_scour_depth_m(D_m: float, U_mps: float, K: float = 2.0, m: float = 1.0) -> float:
    """
    Screening scour at a cylindrical pile in steady current:
    y_s = K * D * (U / sqrt(g*D))^m
    """
    if D_m <= 0 or U_mps < 0 or K <= 0 or m <= 0:
        raise ValueError("Invalid inputs.")
    FrD = U_mps / ((g * D_m) ** 0.5)
    return float(K * D_m * (FrD**m))
