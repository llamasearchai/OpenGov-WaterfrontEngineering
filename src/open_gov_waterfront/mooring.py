"""
Mooring environmental loads (wind and current).

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from dataclasses import dataclass

from .utils import rho_air, rho_water


@dataclass(frozen=True)
class EnvLoads:
    A_wind_m2: float
    A_current_m2: float
    U_wind_mps: float
    U_current_mps: float
    Cd_wind: float = 1.0
    Cd_current: float = 1.0
    safety_factor: float = 1.5


def mooring_total_load_N(env: EnvLoads) -> float:
    Fw = 0.5 * rho_air * env.Cd_wind * env.A_wind_m2 * (env.U_wind_mps**2)
    Fc = 0.5 * rho_water * env.Cd_current * env.A_current_m2 * (env.U_current_mps**2)
    return float((Fw + Fc) * env.safety_factor)
