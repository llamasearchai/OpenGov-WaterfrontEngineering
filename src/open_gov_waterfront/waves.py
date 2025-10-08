"""
Linear wave theory calculations: dispersion, wavelength, celerity, shoaling.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

import math

from .utils import g


def dispersion_k(T_s: float, h_m: float, tol: float = 1e-10, iters: int = 100) -> float:
    """
    Solve linear wave dispersion for wavenumber k (1/m): omega^2 = g k tanh(kh).
    """
    if T_s <= 0 or h_m <= 0:
        raise ValueError("T and h must be > 0")
    omega = 2.0 * math.pi / T_s
    # Deep-water initial guess
    k = (omega**2) / g
    for _ in range(iters):
        f = g * k * math.tanh(k * h_m) - omega**2
        df = g * math.tanh(k * h_m) + g * k * h_m * (1.0 / math.cosh(k * h_m)) ** 2
        step = f / df
        k -= step
        if abs(step) < tol:
            break
    if k <= 0:
        raise RuntimeError("Failed to solve dispersion.")
    return float(k)


def wavelength_L(T_s: float, h_m: float) -> float:
    k = dispersion_k(T_s, h_m)
    return float(2.0 * math.pi / k)


def celerity_c(T_s: float, h_m: float) -> float:
    k = dispersion_k(T_s, h_m)
    omega = 2.0 * math.pi / T_s
    return float(omega / k)


def group_celerity_cg(T_s: float, h_m: float) -> float:
    k = dispersion_k(T_s, h_m)
    c = celerity_c(T_s, h_m)
    n = 0.5 * (1.0 + (2.0 * k * h_m) / math.sinh(2.0 * k * h_m))
    return float(n * c)


def shoaling_coefficient(K0: float | None, T_s: float, h_m: float) -> float:
    """
    Shoaling coefficient Ks = sqrt(cg0/cg). If K0 (deep-water group velocity) not provided,
    approximate cg0 = g T / (4 pi).
    """
    cg = group_celerity_cg(T_s, h_m)
    if K0 is None:
        cg0 = (g * T_s) / (4.0 * math.pi)
    else:
        cg0 = K0
    return float(math.sqrt(cg0 / cg))
