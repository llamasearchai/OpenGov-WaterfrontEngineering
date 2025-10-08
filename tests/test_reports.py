"""
Tests for report template generation.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from open_gov_waterfront.reports import write_report_template


def test_write_report_template(tmp_path: Path) -> None:
    """Test report template creation."""
    output_file = tmp_path / "test_report.csv"
    write_report_template(output_file)

    assert output_file.exists()
    df = pd.read_csv(output_file)
    assert len(df.columns) == 20
    assert "project" in df.columns
    assert "location" in df.columns
    assert "jurisdiction" in df.columns
    assert "waterbody" in df.columns
    assert "design_wave_Hs_m" in df.columns
    assert "pile_D_m" in df.columns
    assert "notes" in df.columns
    assert len(df) == 0


def test_write_report_template_columns(tmp_path: Path) -> None:
    """Test that report template has all required columns."""
    output_file = tmp_path / "columns_test.csv"
    write_report_template(output_file)

    df = pd.read_csv(output_file)
    expected_columns = [
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
    assert list(df.columns) == expected_columns


def test_write_report_template_overwrites(tmp_path: Path) -> None:
    """Test that report template can overwrite existing file."""
    output_file = tmp_path / "overwrite_test.csv"
    write_report_template(output_file)
    write_report_template(output_file)
    assert output_file.exists()
