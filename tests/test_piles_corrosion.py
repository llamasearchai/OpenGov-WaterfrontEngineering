"""
Tests for pile capacity and corrosion calculations.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from open_gov_waterfront.corrosion import CorrosionInputs, remaining_thickness_mm
from open_gov_waterfront.piles import PileAxialInputs, pile_axial_capacity_kN


def test_pile_capacity_and_corrosion() -> None:
    Q = pile_axial_capacity_kN(
        PileAxialInputs(
            shaft_length_m=20.0,
            perimeter_m=3.14,
            area_tip_m2=0.2,
            unit_skin_kPa=50.0,
            unit_end_bearing_kPa=1000.0,
        )
    )
    assert Q > 0.0
    t = remaining_thickness_mm(
        CorrosionInputs(t0_mm=16.0, rate_mm_per_year=0.1, years=50.0)
    )
    assert 0.0 <= t < 16.0


def test_pile_capacity_components() -> None:
    """Test that pile capacity includes both skin and end bearing."""
    Q1 = pile_axial_capacity_kN(
        PileAxialInputs(
            shaft_length_m=20.0,
            perimeter_m=3.0,
            area_tip_m2=0.2,
            unit_skin_kPa=50.0,
            unit_end_bearing_kPa=0.0,
        )
    )
    Q2 = pile_axial_capacity_kN(
        PileAxialInputs(
            shaft_length_m=20.0,
            perimeter_m=3.0,
            area_tip_m2=0.2,
            unit_skin_kPa=0.0,
            unit_end_bearing_kPa=1000.0,
        )
    )
    Q_total = pile_axial_capacity_kN(
        PileAxialInputs(
            shaft_length_m=20.0,
            perimeter_m=3.0,
            area_tip_m2=0.2,
            unit_skin_kPa=50.0,
            unit_end_bearing_kPa=1000.0,
        )
    )
    assert abs(Q_total - (Q1 + Q2)) < 0.1


def test_corrosion_total_loss() -> None:
    """Test corrosion with complete thickness loss."""
    t = remaining_thickness_mm(
        CorrosionInputs(t0_mm=10.0, rate_mm_per_year=0.5, years=30.0)
    )
    assert t == 0.0


def test_corrosion_partial_loss() -> None:
    """Test corrosion with partial thickness loss."""
    t = remaining_thickness_mm(
        CorrosionInputs(t0_mm=20.0, rate_mm_per_year=0.2, years=25.0)
    )
    assert t == 15.0
