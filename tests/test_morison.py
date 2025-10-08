"""
Tests for Morison equation calculations.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

import pytest

from open_gov_waterfront.morison import MorisonCoeffs, morison_inline_max_per_length_N


def test_morison_positive_force() -> None:
    F = morison_inline_max_per_length_N(D_m=1.0, u_amp_mps=1.0, a_amp_mps2=0.5)
    assert F > 0.0


def test_morison_custom_coefficients() -> None:
    """Test Morison with custom drag and inertia coefficients."""
    F1 = morison_inline_max_per_length_N(
        D_m=1.0, u_amp_mps=1.0, a_amp_mps2=0.5, coeffs=MorisonCoeffs(Cd=1.0, Cm=2.0)
    )
    F2 = morison_inline_max_per_length_N(
        D_m=1.0, u_amp_mps=1.0, a_amp_mps2=0.5, coeffs=MorisonCoeffs(Cd=1.2, Cm=2.5)
    )
    assert F2 > F1


def test_morison_zero_velocity() -> None:
    """Test Morison with zero velocity (inertia only)."""
    F = morison_inline_max_per_length_N(D_m=1.0, u_amp_mps=0.0, a_amp_mps2=1.0)
    assert F > 0.0


def test_morison_invalid_diameter() -> None:
    """Test error handling for invalid diameter."""
    with pytest.raises(ValueError):
        morison_inline_max_per_length_N(D_m=-1.0, u_amp_mps=1.0, a_amp_mps2=0.5)
