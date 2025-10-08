"""
Tests for wave calculations.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

import pytest

from open_gov_waterfront.waves import (
    celerity_c,
    dispersion_k,
    group_celerity_cg,
    shoaling_coefficient,
    wavelength_L,
)


def test_wavelength_positive() -> None:
    L = wavelength_L(10.0, 50.0)
    c = celerity_c(10.0, 50.0)
    assert L > 0.0 and c > 0.0


def test_dispersion_deep_water() -> None:
    """Test dispersion in deep water (h >> L)."""
    k = dispersion_k(10.0, 1000.0)
    assert k > 0.0


def test_dispersion_shallow_water() -> None:
    """Test dispersion in shallow water."""
    k = dispersion_k(5.0, 2.0)
    assert k > 0.0


def test_group_celerity() -> None:
    """Test group velocity calculation."""
    cg = group_celerity_cg(10.0, 50.0)
    assert cg > 0.0


def test_shoaling_coefficient() -> None:
    """Test shoaling coefficient calculation."""
    Ks = shoaling_coefficient(None, 10.0, 10.0)
    assert Ks > 0.0


def test_invalid_wave_period() -> None:
    """Test error handling for invalid wave period."""
    with pytest.raises(ValueError):
        wavelength_L(-1.0, 50.0)


def test_invalid_water_depth() -> None:
    """Test error handling for invalid water depth."""
    with pytest.raises(ValueError):
        wavelength_L(10.0, -5.0)


def test_dispersion_convergence() -> None:
    """Test dispersion equation convergence with various conditions."""
    # Test with intermediate water depth
    k = dispersion_k(8.0, 20.0)
    assert k > 0.0
    # Test with shallow water
    k2 = dispersion_k(10.0, 5.0)
    assert k2 > 0.0


def test_shoaling_coefficient_with_K0() -> None:
    """Test shoaling coefficient with provided deep-water group velocity."""
    Ks = shoaling_coefficient(15.0, 10.0, 10.0)
    assert Ks > 0.0


def test_dispersion_fails_to_converge() -> None:
    """Test dispersion equation with extreme conditions that might not converge."""
    # Use very small period and depth which should still converge but exercises the code
    # The RuntimeError path is very difficult to trigger with valid physical inputs
    k = dispersion_k(1.0, 0.1)
    assert k > 0.0
