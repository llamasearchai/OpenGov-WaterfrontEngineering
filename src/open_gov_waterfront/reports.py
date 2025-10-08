"""
Report template generation.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_report_template(path: Path) -> None:
    cols = [
        "project",
        "location",
        "jurisdiction",
        "waterbody",
        "design_wave_Hs_m",
        "design_Tp_s",
        "water_depth_m",
        "pile_D_m",
        "morison_Cd",
        "morison_Cm",
        "mooring_wind_area_m2",
        "mooring_current_area_m2",
        "mooring_wind_mps",
        "mooring_current_mps",
        "berthing_mass_tonnes",
        "berthing_speed_knots",
        "seawall_mu",
        "seawall_W_kN",
        "seawall_T_kN",
        "notes",
    ]
    pd.DataFrame(columns=cols).to_csv(path, index=False)
