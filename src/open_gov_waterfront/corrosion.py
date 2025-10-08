"""
Corrosion allowance calculations.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CorrosionInputs:
    t0_mm: float
    rate_mm_per_year: float
    years: float


def remaining_thickness_mm(inp: CorrosionInputs) -> float:
    t = inp.t0_mm - inp.rate_mm_per_year * inp.years
    return float(max(0.0, t))
