"""
Tests for CLI and state profiles.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from open_gov_waterfront.cli import app
from open_gov_waterfront.states import get_state, list_states

runner = CliRunner()


def test_cli_list_states() -> None:
    result = runner.invoke(app, ["list-states"])
    assert result.exit_code == 0
    assert "California" in result.stdout
    assert "Ohio" in result.stdout
    assert "Indiana" in result.stdout


def test_cli_waves() -> None:
    """Test waves CLI command."""
    result = runner.invoke(app, ["waves", "--T", "10", "--h", "50"])
    assert result.exit_code == 0
    assert "Linear Waves" in result.stdout


def test_cli_morison() -> None:
    """Test morison-max CLI command."""
    result = runner.invoke(app, ["morison-max", "--D", "1.5", "--u", "1.0", "--a", "0.5"])
    assert result.exit_code == 0


def test_cli_berthing() -> None:
    """Test berthing CLI command."""
    result = runner.invoke(app, ["berthing", "--mass", "8000", "--speed", "0.5"])
    assert result.exit_code == 0


def test_cli_seawall() -> None:
    """Test seawall-slide CLI command."""
    result = runner.invoke(app, ["seawall-slide", "--mu", "0.6", "--W", "1000", "--T", "400"])
    assert result.exit_code == 0


def test_state_profiles() -> None:
    """Test state profile retrieval."""
    states = list_states()
    assert len(states) == 3
    ca = get_state("CA")
    assert ca.code == "CA"
    assert ca.name == "California"


def test_state_agencies() -> None:
    """Test state agency lists."""
    ca = get_state("CA")
    assert "USACE" in ca.agencies
    assert "CA Coastal Commission" in ca.agencies


def test_cli_mooring() -> None:
    """Test mooring CLI command."""
    result = runner.invoke(app, ["mooring", "--Aw", "1200", "--Ac", "800", "--Uw", "22", "--Uc", "1.2"])
    assert result.exit_code == 0


def test_cli_pile_axial() -> None:
    """Test pile-axial CLI command."""
    result = runner.invoke(
        app, ["pile-axial", "--L", "25", "--perim", "3.6", "--Atip", "0.25", "--qs", "60", "--qb", "1200"]
    )
    assert result.exit_code == 0


def test_cli_corrosion() -> None:
    """Test corrosion CLI command."""
    result = runner.invoke(app, ["corrosion", "--t0", "16", "--rate", "0.12", "--years", "50"])
    assert result.exit_code == 0


def test_cli_scour_pile() -> None:
    """Test scour-pile CLI command."""
    result = runner.invoke(app, ["scour-pile", "--D", "1.2", "--U", "1.5"])
    assert result.exit_code == 0


def test_cli_tides() -> None:
    """Test tides CLI command."""
    result = runner.invoke(
        app, ["tides", "--A1", "0.5", "--T1", "44714", "--P1", "0", "--dur", "43200", "--dt", "600"]
    )
    assert result.exit_code == 0


def test_cli_tides_two_constituents() -> None:
    """Test tides CLI command with two constituents."""
    result = runner.invoke(
        app,
        [
            "tides",
            "--A1",
            "0.5",
            "--T1",
            "44714",
            "--P1",
            "0",
            "--A2",
            "0.2",
            "--T2",
            "43200",
            "--P2",
            "1.0",
            "--dur",
            "172800",
            "--dt",
            "600",
        ],
    )
    assert result.exit_code == 0


def test_cli_report_template(tmp_path) -> None:
    """Test report-template CLI command."""

    output_file = tmp_path / "test_template.csv"
    result = runner.invoke(app, ["report-template", "--out", str(output_file)])
    assert result.exit_code == 0
    assert output_file.exists()


def test_get_state_invalid() -> None:
    """Test error handling for invalid state code."""
    from open_gov_waterfront.states import get_state

    with pytest.raises(KeyError, match="Unsupported state"):
        get_state("XX")
