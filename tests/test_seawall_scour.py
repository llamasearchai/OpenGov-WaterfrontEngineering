"""
Tests for seawall and scour calculations.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

import pytest

from open_gov_waterfront.scour import pile_scour_depth_m
from open_gov_waterfront.seawall import sliding_fs


def test_seawall_fs_and_scour() -> None:
    FS = sliding_fs(mu=0.6, W_kN=1000.0, T_kN=400.0)
    ys = pile_scour_depth_m(D_m=1.2, U_mps=1.5)
    assert FS > 1.0
    assert ys > 0.0


def test_seawall_fs_values() -> None:
    """Test seawall factor of safety calculation."""
    FS1 = sliding_fs(mu=0.5, W_kN=1000.0, T_kN=500.0)
    assert abs(FS1 - 1.0) < 0.01
    FS2 = sliding_fs(mu=0.6, W_kN=1000.0, T_kN=400.0)
    assert FS2 == 1.5


def test_scour_zero_velocity() -> None:
    """Test scour with zero current velocity."""
    ys = pile_scour_depth_m(D_m=1.0, U_mps=0.0)
    assert ys == 0.0


def test_scour_varies_with_velocity() -> None:
    """Test that scour increases with velocity."""
    ys1 = pile_scour_depth_m(D_m=1.0, U_mps=1.0)
    ys2 = pile_scour_depth_m(D_m=1.0, U_mps=2.0)
    assert ys2 > ys1


def test_seawall_invalid_inputs() -> None:
    """Test error handling for invalid seawall inputs."""
    with pytest.raises(ValueError):
        sliding_fs(mu=0.0, W_kN=1000.0, T_kN=400.0)
    with pytest.raises(ValueError):
        sliding_fs(mu=0.6, W_kN=-100.0, T_kN=400.0)


def test_scour_invalid_diameter() -> None:
    """Test error handling for invalid pile diameter in scour."""
    with pytest.raises(ValueError):
        pile_scour_depth_m(D_m=-1.0, U_mps=1.5)


def test_scour_invalid_K() -> None:
    """Test error handling for invalid scour coefficient."""
    with pytest.raises(ValueError):
        pile_scour_depth_m(D_m=1.0, U_mps=1.5, K=-1.0)


def test_scour_invalid_m() -> None:
    """Test error handling for invalid scour exponent."""
    with pytest.raises(ValueError):
        pile_scour_depth_m(D_m=1.0, U_mps=1.5, m=-0.5)
