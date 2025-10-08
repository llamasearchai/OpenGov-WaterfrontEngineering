"""
Command-line interface for OpenGov-WaterfrontEngineering.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme

from .berthing import berthing_energy_J, fender_reaction_kN
from .corrosion import CorrosionInputs, remaining_thickness_mm
from .mooring import EnvLoads, mooring_total_load_N
from .morison import MorisonCoeffs, morison_inline_max_per_length_N
from .piles import PileAxialInputs, pile_axial_capacity_kN
from .reports import write_report_template
from .scour import pile_scour_depth_m
from .seawall import sliding_fs
from .states import list_states
from .tides import Constituent, tide_series
from .waves import celerity_c, group_celerity_cg, shoaling_coefficient, wavelength_L

app = typer.Typer(
    help="OpenGov-WaterfrontEngineering: Marine/waterfront screening toolkit (CA/IN/OH)."
)
console = Console(theme=Theme({"info": "cyan", "error": "red", "success": "green"}))


@app.command("list-states")
def cmd_list_states() -> None:
    """List supported state profiles (CA, IN, OH)."""
    lines = [
        f"{p.code}: {p.name} - Waters: {p.waters}; Agencies: {', '.join(p.agencies)}. {p.notes}"
        for p in list_states()
    ]
    console.print(Panel("\n".join(lines), title="Supported States"))


@app.command("waves")
def cmd_waves(
    T_s: float = typer.Option(..., "--T", help="Wave period (s)"),
    h_m: float = typer.Option(..., "--h", help="Water depth (m)"),
) -> None:
    """Calculate linear wave properties: wavelength, celerity, group velocity, shoaling."""
    L = wavelength_L(T_s, h_m)
    c = celerity_c(T_s, h_m)
    cg = group_celerity_cg(T_s, h_m)
    Ks = shoaling_coefficient(None, T_s, h_m)
    console.print(
        Panel(
            f"L = {L:.2f} m\nc = {c:.2f} m/s\ncg = {cg:.2f} m/s\nKs = {Ks:.3f}",
            title="Linear Waves",
        )
    )


@app.command("morison-max")
def cmd_morison_max(
    D_m: float = typer.Option(..., "--D", help="Pile diameter (m)"),
    u_amp: float = typer.Option(..., "--u", help="Velocity amplitude (m/s)"),
    a_amp: float = typer.Option(..., "--a", help="Acceleration amplitude (m/s^2)"),
    Cd: float = typer.Option(1.0, "--Cd"),
    Cm: float = typer.Option(2.0, "--Cm"),
) -> None:
    """Calculate maximum Morison inline force per unit length on a pile."""
    FpL = morison_inline_max_per_length_N(D_m, u_amp, a_amp, coeffs=MorisonCoeffs(Cd=Cd, Cm=Cm))
    console.print(
        Panel(f"Max inline force per length = {FpL:.1f} N/m", title="Morison Inline Force")
    )


@app.command("berthing")
def cmd_berthing(
    mass_tonnes: float = typer.Option(..., "--mass", help="Vessel mass (tonnes)"),
    speed_knots: float = typer.Option(..., "--speed", help="Berthing speed (knots)"),
    Ce: float = typer.Option(1.0, "--Ce"),
    Cc: float = typer.Option(1.0, "--Cc"),
    Cs: float = typer.Option(1.0, "--Cs"),
    eff: float = typer.Option(0.7, "--eff", help="Fender efficiency"),
    defl_m: float = typer.Option(0.5, "--defl", help="Fender deflection (m)"),
) -> None:
    """Calculate berthing energy and fender reaction."""
    E = berthing_energy_J(mass_tonnes, speed_knots, Ce=Ce, Cc=Cc, Cs=Cs)
    RkN = fender_reaction_kN(E, efficiency=eff, deflection_m=defl_m)
    console.print(
        Panel(f"E = {E:,.0f} J\nR = {RkN:.1f} kN", title="Berthing Energy/Reaction")
    )


@app.command("mooring")
def cmd_mooring(
    A_wind: float = typer.Option(..., "--Aw", help="Projected wind area (m^2)"),
    A_curr: float = typer.Option(..., "--Ac", help="Projected current area (m^2)"),
    U_wind: float = typer.Option(..., "--Uw", help="Wind speed (m/s)"),
    U_curr: float = typer.Option(..., "--Uc", help="Current speed (m/s)"),
    Cd_wind: float = typer.Option(1.0, "--Cdw"),
    Cd_curr: float = typer.Option(1.0, "--Cdc"),
    SF: float = typer.Option(1.5, "--SF", help="Safety factor"),
) -> None:
    """Calculate total mooring load from wind and current."""
    env = EnvLoads(
        A_wind_m2=A_wind,
        A_current_m2=A_curr,
        U_wind_mps=U_wind,
        U_current_mps=U_curr,
        Cd_wind=Cd_wind,
        Cd_current=Cd_curr,
        safety_factor=SF,
    )
    F = mooring_total_load_N(env)
    console.print(Panel(f"Total mooring load = {F/1000:.1f} kN", title="Mooring Load"))


@app.command("pile-axial")
def cmd_pile_axial(
    shaft_len: float = typer.Option(..., "--L", help="Shaft length (m)"),
    perimeter: float = typer.Option(..., "--perim", help="Perimeter (m)"),
    area_tip: float = typer.Option(..., "--Atip", help="Tip area (m^2)"),
    qs_kPa: float = typer.Option(..., "--qs"),
    qb_kPa: float = typer.Option(..., "--qb"),
) -> None:
    """Calculate pile axial capacity."""
    Q = pile_axial_capacity_kN(
        PileAxialInputs(
            shaft_length_m=shaft_len,
            perimeter_m=perimeter,
            area_tip_m2=area_tip,
            unit_skin_kPa=qs_kPa,
            unit_end_bearing_kPa=qb_kPa,
        )
    )
    console.print(Panel(f"Axial capacity = {Q:.0f} kN", title="Pile Axial Capacity"))


@app.command("corrosion")
def cmd_corrosion(
    t0_mm: float = typer.Option(..., "--t0", help="Initial thickness (mm)"),
    rate: float = typer.Option(..., "--rate", help="Corrosion rate (mm/yr)"),
    years: float = typer.Option(..., "--years"),
) -> None:
    """Calculate remaining thickness after corrosion."""
    t_rem = remaining_thickness_mm(
        CorrosionInputs(t0_mm=t0_mm, rate_mm_per_year=rate, years=years)
    )
    console.print(Panel(f"Remaining thickness = {t_rem:.2f} mm", title="Corrosion Allowance"))


@app.command("seawall-slide")
def cmd_seawall_slide(
    mu: float = typer.Option(..., "--mu", help="Base friction coefficient"),
    W_kN: float = typer.Option(..., "--W", help="Wall weight (kN)"),
    T_kN: float = typer.Option(..., "--T", help="Horizontal thrust (kN)"),
) -> None:
    """Calculate seawall sliding factor of safety."""
    FS = sliding_fs(mu, W_kN, T_kN)
    console.print(Panel(f"Sliding FS = {FS:.2f}", title="Seawall Sliding"))


@app.command("scour-pile")
def cmd_scour_pile(
    D_m: float = typer.Option(..., "--D", help="Pile diameter (m)"),
    U_mps: float = typer.Option(..., "--U", help="Depth-averaged current (m/s)"),
    K: float = typer.Option(2.0, "--K"),
    mexp: float = typer.Option(1.0, "--m"),
) -> None:
    """Calculate local scour depth at pile (screening)."""
    ys = pile_scour_depth_m(D_m, U_mps, K=K, m=mexp)
    console.print(Panel(f"Estimated local scour = {ys:.2f} m", title="Pile Scour (Screening)"))


@app.command("tides")
def cmd_tides(
    A1: float = typer.Option(..., "--A1", help="Constituent 1 amplitude (m)"),
    T1: float = typer.Option(..., "--T1", help="Constituent 1 period (s)"),
    P1: float = typer.Option(0.0, "--P1", help="Constituent 1 phase (rad)"),
    A2: float = typer.Option(0.0, "--A2"),
    T2: float = typer.Option(0.0, "--T2"),
    P2: float = typer.Option(0.0, "--P2"),
    dur: float = typer.Option(43200.0, "--dur", help="Duration (s)"),
    dt: float = typer.Option(600.0, "--dt", help="Time step (s)"),
) -> None:
    """Generate tide synthesis from constituents."""
    import math

    cons = [Constituent(amp_m=A1, omega_rad_s=2 * math.pi / T1, phase_rad=P1)]
    if A2 > 0 and T2 > 0:
        cons.append(Constituent(amp_m=A2, omega_rad_s=2 * math.pi / T2, phase_rad=P2))
    t, eta = tide_series(0.0, dur, dt, cons)
    console.print(
        Panel(
            f"Generated {len(t)} points. Max eta = {float(eta.max()):.2f} m, Min eta = {float(eta.min()):.2f} m",
            title="Tide Synthesis",
        )
    )


@app.command("report-template")
def cmd_report_template(
    out: Path = typer.Option(Path("waterfront_report_template.csv"), "--out")
) -> None:
    """Write a report template CSV."""
    write_report_template(out)
    console.print(Panel(f"Wrote report template to {out}", title="Report Template"))


if __name__ == "__main__":
    app()
