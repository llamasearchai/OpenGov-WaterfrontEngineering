"""
Tests for berthing energy and fender calculations.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

import pytest

from open_gov_waterfront.berthing import berthing_energy_J, fender_reaction_kN


def test_berthing_energy() -> None:
    E = berthing_energy_J(10000.0, 0.5)  # 10,000 t at 0.5 kn
    R = fender_reaction_kN(E, efficiency=0.7, deflection_m=0.5)
    assert E > 0.0 and R > 0.0


def test_berthing_with_coefficients() -> None:
    """Test berthing energy with modification coefficients."""
    E = berthing_energy_J(5000.0, 0.8, Ce=0.9, Cc=0.8, Cs=1.0)
    assert E > 0.0


def test_fender_reaction_varies_with_efficiency() -> None:
    """Test that fender reaction varies with efficiency."""
    E = 1000000.0
    R1 = fender_reaction_kN(E, efficiency=0.5, deflection_m=0.5)
    R2 = fender_reaction_kN(E, efficiency=0.8, deflection_m=0.5)
    assert R1 > R2  # Lower efficiency means higher reaction


def test_berthing_invalid_mass() -> None:
    """Test error handling for invalid mass."""
    with pytest.raises(ValueError):
        berthing_energy_J(-100.0, 0.5)


def test_berthing_invalid_speed() -> None:
    """Test error handling for invalid speed."""
    with pytest.raises(ValueError):
        berthing_energy_J(1000.0, -0.5)


def test_fender_invalid_efficiency() -> None:
    """Test error handling for invalid efficiency."""
    with pytest.raises(ValueError):
        fender_reaction_kN(1000.0, efficiency=0.0, deflection_m=0.5)
