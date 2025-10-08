"""
Additional tests for server.py to achieve 100% coverage.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from open_gov_waterfront.server import app

client = TestClient(app)


def test_waves_error_handling() -> None:
    """Test waves endpoint error handling."""
    with patch("open_gov_waterfront.server.wavelength_L", side_effect=Exception("Test error")):
        response = client.post("/waves", json={"T_s": 10.0, "h_m": 50.0})
        assert response.status_code == 400
        assert "Test error" in response.json()["detail"]


def test_morison_error_handling() -> None:
    """Test morison endpoint error handling."""
    with patch(
        "open_gov_waterfront.server.morison_inline_max_per_length_N",
        side_effect=Exception("Test error"),
    ):
        response = client.post(
            "/morison", json={"D_m": 1.5, "u_amp_mps": 1.0, "a_amp_mps2": 0.5, "Cd": 1.0, "Cm": 2.0}
        )
        assert response.status_code == 400


def test_berthing_error_handling() -> None:
    """Test berthing endpoint error handling."""
    with patch("open_gov_waterfront.server.berthing_energy_J", side_effect=Exception("Test error")):
        response = client.post(
            "/berthing",
            json={
                "mass_tonnes": 8000.0,
                "speed_knots": 0.5,
                "Ce": 1.0,
                "Cc": 1.0,
                "Cs": 1.0,
                "efficiency": 0.7,
                "deflection_m": 0.5,
            },
        )
        assert response.status_code == 400


def test_mooring_error_handling() -> None:
    """Test mooring endpoint error handling."""
    with patch(
        "open_gov_waterfront.server.mooring_total_load_N", side_effect=Exception("Test error")
    ):
        response = client.post(
            "/mooring",
            json={
                "A_wind_m2": 1000.0,
                "A_current_m2": 800.0,
                "U_wind_mps": 20.0,
                "U_current_mps": 1.0,
                "Cd_wind": 1.0,
                "Cd_current": 1.0,
                "safety_factor": 1.5,
            },
        )
        assert response.status_code == 400


def test_pile_axial_error_handling() -> None:
    """Test pile axial endpoint error handling."""
    with patch(
        "open_gov_waterfront.server.pile_axial_capacity_kN", side_effect=Exception("Test error")
    ):
        response = client.post(
            "/pile-axial",
            json={
                "shaft_length_m": 20.0,
                "perimeter_m": 3.14,
                "area_tip_m2": 0.2,
                "unit_skin_kPa": 50.0,
                "unit_end_bearing_kPa": 1000.0,
            },
        )
        assert response.status_code == 400


def test_corrosion_error_handling() -> None:
    """Test corrosion endpoint error handling."""
    with patch(
        "open_gov_waterfront.server.remaining_thickness_mm", side_effect=Exception("Test error")
    ):
        response = client.post(
            "/corrosion", json={"t0_mm": 16.0, "rate_mm_per_year": 0.1, "years": 50.0}
        )
        assert response.status_code == 400


def test_seawall_error_handling() -> None:
    """Test seawall endpoint error handling."""
    with patch("open_gov_waterfront.server.sliding_fs", side_effect=Exception("Test error")):
        response = client.post("/seawall", json={"mu": 0.6, "W_kN": 1000.0, "T_kN": 400.0})
        assert response.status_code == 400


def test_scour_error_handling() -> None:
    """Test scour endpoint error handling."""
    with patch("open_gov_waterfront.server.pile_scour_depth_m", side_effect=Exception("Test error")):
        response = client.post("/scour", json={"D_m": 1.2, "U_mps": 1.5, "K": 2.0, "m": 1.0})
        assert response.status_code == 400


def test_server_main() -> None:
    """Test server main function."""
    with patch("uvicorn.run") as mock_run:
        from open_gov_waterfront.server import main

        main()
        mock_run.assert_called_once_with(
            "open_gov_waterfront.server:app",
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=False,
        )


async def test_server_startup_logging() -> None:
    """Test server startup and shutdown logging."""

    from open_gov_waterfront.server import lifespan

    # Mock app object
    class MockApp:
        pass

    app = MockApp()
    # Trigger lifespan context
    async with lifespan(app):
        pass  # This exercises the startup/shutdown logging
