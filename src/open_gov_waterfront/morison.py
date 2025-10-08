"""
Morison equation inline force calculations on piles.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from dataclasses import dataclass

from .utils import rho_water


@dataclass(frozen=True)
class MorisonCoeffs:
    Cd: float = 1.0
    Cm: float = 2.0


def morison_inline_max_per_length_N(
    D_m: float,
    u_amp_mps: float,
    a_amp_mps2: float,
    coeffs: MorisonCoeffs = MorisonCoeffs(),
    rho: float = rho_water,
) -> float:
    """
    Max inline force per unit length (N/m) using velocity and acceleration amplitudes
    (linear wave at a point).
    F/L_max = 0.5*rho*Cd*D*u_amp*|u_amp| + rho*Cm*(pi*D^2/4)*a_amp
    """
    if D_m <= 0:
        raise ValueError("D must be > 0")
    drag = 0.5 * rho * coeffs.Cd * D_m * (u_amp_mps**2)
    inertia = rho * coeffs.Cm * (3.141592653589793 * (D_m**2) / 4.0) * a_amp_mps2
    return float(drag + inertia)
