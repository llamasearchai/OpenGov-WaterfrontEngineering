"""
Berthing energy and fender reaction calculations.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations


def berthing_energy_J(
    mass_tonnes: float, speed_knots: float, Ce: float = 1.0, Cc: float = 1.0, Cs: float = 1.0
) -> float:
    """
    E = 0.5 * m * v^2 * Ce * Cc * Cs
    mass in metric tonnes, speed in knots.
    """
    if mass_tonnes <= 0 or speed_knots <= 0:
        raise ValueError("mass and speed must be > 0")
    m_kg = mass_tonnes * 1000.0
    v_mps = speed_knots * 0.514444
    E = 0.5 * m_kg * (v_mps**2) * Ce * Cc * Cs
    return float(E)


def fender_reaction_kN(energy_J: float, efficiency: float = 0.7, deflection_m: float = 0.5) -> float:
    """
    Simple reaction estimate: R = (E / (eff * deflection)) in N; return kN.
    """
    if efficiency <= 0 or deflection_m <= 0:
        raise ValueError("efficiency and deflection must be > 0")
    R = energy_J / (efficiency * deflection_m)
    return float(R / 1000.0)
