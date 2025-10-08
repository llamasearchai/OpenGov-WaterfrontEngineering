"""
Tests for mooring load calculations.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from open_gov_waterfront.mooring import EnvLoads, mooring_total_load_N


def test_mooring_load() -> None:
    env = EnvLoads(
        A_wind_m2=1000.0, A_current_m2=800.0, U_wind_mps=20.0, U_current_mps=1.0
    )
    F = mooring_total_load_N(env)
    assert F > 0.0


def test_mooring_wind_only() -> None:
    """Test mooring with wind load only."""
    env = EnvLoads(
        A_wind_m2=1000.0, A_current_m2=0.0, U_wind_mps=25.0, U_current_mps=0.0
    )
    F = mooring_total_load_N(env)
    assert F > 0.0


def test_mooring_current_only() -> None:
    """Test mooring with current load only."""
    env = EnvLoads(
        A_wind_m2=0.0, A_current_m2=500.0, U_wind_mps=0.0, U_current_mps=2.0
    )
    F = mooring_total_load_N(env)
    assert F > 0.0


def test_mooring_safety_factor() -> None:
    """Test that safety factor correctly scales the load."""
    env1 = EnvLoads(
        A_wind_m2=1000.0,
        A_current_m2=800.0,
        U_wind_mps=20.0,
        U_current_mps=1.0,
        safety_factor=1.0,
    )
    env2 = EnvLoads(
        A_wind_m2=1000.0,
        A_current_m2=800.0,
        U_wind_mps=20.0,
        U_current_mps=1.0,
        safety_factor=2.0,
    )
    F1 = mooring_total_load_N(env1)
    F2 = mooring_total_load_N(env2)
    assert abs(F2 - 2.0 * F1) < 1.0  # Should be approximately doubled
