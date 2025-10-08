"""
Pile axial capacity calculations (static skin + end bearing).

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PileAxialInputs:
    shaft_length_m: float
    perimeter_m: float
    area_tip_m2: float
    unit_skin_kPa: float
    unit_end_bearing_kPa: float


def pile_axial_capacity_kN(inp: PileAxialInputs) -> float:
    """
    Q = qs * As + qb * Ab, return in kN.
    """
    As = inp.perimeter_m * inp.shaft_length_m
    qb = inp.unit_end_bearing_kPa * inp.area_tip_m2
    qs = inp.unit_skin_kPa * As
    Q_kN = qs + qb  # since kPa * m^2 = kN
    return float(Q_kN)
