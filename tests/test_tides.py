"""
Tests for tide harmonic synthesis.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

import numpy as np
import pytest

from open_gov_waterfront.tides import Constituent, tide_series


def test_tide_series_single_constituent() -> None:
    """Test tide series with single constituent."""
    const = Constituent(amp_m=1.0, omega_rad_s=0.0001, phase_rad=0.0)
    t, eta = tide_series(0.0, 3600.0, 600.0, [const])
    assert len(t) == 7
    assert len(eta) == 7
    assert isinstance(t, np.ndarray)
    assert isinstance(eta, np.ndarray)


def test_tide_series_multiple_constituents() -> None:
    """Test tide series with multiple constituents."""
    const1 = Constituent(amp_m=1.0, omega_rad_s=0.0001, phase_rad=0.0)
    const2 = Constituent(amp_m=0.5, omega_rad_s=0.0002, phase_rad=1.57)
    t, eta = tide_series(0.0, 7200.0, 1200.0, [const1, const2])
    assert len(t) == 7
    assert len(eta) == 7
    assert np.max(eta) <= 1.5
    assert np.min(eta) >= -1.5


def test_tide_series_zero_amplitude() -> None:
    """Test tide series with zero amplitude constituent."""
    const = Constituent(amp_m=0.0, omega_rad_s=0.0001, phase_rad=0.0)
    t, eta = tide_series(0.0, 1000.0, 100.0, [const])
    assert np.all(eta == 0.0)


def test_tide_series_phase_shift() -> None:
    """Test that phase shift affects the tide series."""
    const1 = Constituent(amp_m=1.0, omega_rad_s=0.001, phase_rad=0.0)
    const2 = Constituent(amp_m=1.0, omega_rad_s=0.001, phase_rad=np.pi)
    t, eta1 = tide_series(0.0, 1000.0, 100.0, [const1])
    t, eta2 = tide_series(0.0, 1000.0, 100.0, [const2])
    assert not np.allclose(eta1, eta2)


def test_tide_series_invalid_duration() -> None:
    """Test error handling for invalid duration."""
    const = Constituent(amp_m=1.0, omega_rad_s=0.0001, phase_rad=0.0)
    with pytest.raises(ValueError, match="duration and dt must be > 0"):
        tide_series(0.0, -100.0, 10.0, [const])


def test_tide_series_invalid_dt() -> None:
    """Test error handling for invalid time step."""
    const = Constituent(amp_m=1.0, omega_rad_s=0.0001, phase_rad=0.0)
    with pytest.raises(ValueError, match="duration and dt must be > 0"):
        tide_series(0.0, 1000.0, 0.0, [const])


def test_tide_series_empty_constituents() -> None:
    """Test tide series with no constituents."""
    t, eta = tide_series(0.0, 1000.0, 100.0, [])
    assert len(t) == 11
    assert np.all(eta == 0.0)
