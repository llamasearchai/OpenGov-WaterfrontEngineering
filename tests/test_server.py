"""
Tests for FastAPI server endpoints.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from open_gov_waterfront.server import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_states_endpoint() -> None:
    """Test states listing endpoint."""
    response = client.get("/states")
    assert response.status_code == 200
    data = response.json()
    assert "states" in data
    assert len(data["states"]) == 3


def test_waves_endpoint() -> None:
    """Test waves calculation endpoint."""
    payload = {"T_s": 10.0, "h_m": 50.0}
    response = client.post("/waves", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "wavelength_m" in data
    assert "celerity_mps" in data
    assert data["wavelength_m"] > 0


def test_morison_endpoint() -> None:
    """Test Morison force calculation endpoint."""
    payload = {"D_m": 1.5, "u_amp_mps": 1.0, "a_amp_mps2": 0.5, "Cd": 1.0, "Cm": 2.0}
    response = client.post("/morison", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "force_per_length_Npm" in data
    assert data["force_per_length_Npm"] > 0


def test_berthing_endpoint() -> None:
    """Test berthing calculation endpoint."""
    payload = {
        "mass_tonnes": 8000.0,
        "speed_knots": 0.5,
        "Ce": 1.0,
        "Cc": 1.0,
        "Cs": 1.0,
        "efficiency": 0.7,
        "deflection_m": 0.5,
    }
    response = client.post("/berthing", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "energy_J" in data
    assert "fender_reaction_kN" in data


def test_mooring_endpoint() -> None:
    """Test mooring load calculation endpoint."""
    payload = {
        "A_wind_m2": 1000.0,
        "A_current_m2": 800.0,
        "U_wind_mps": 20.0,
        "U_current_mps": 1.0,
        "Cd_wind": 1.0,
        "Cd_current": 1.0,
        "safety_factor": 1.5,
    }
    response = client.post("/mooring", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "total_load_N" in data


def test_pile_axial_endpoint() -> None:
    """Test pile axial capacity endpoint."""
    payload = {
        "shaft_length_m": 20.0,
        "perimeter_m": 3.14,
        "area_tip_m2": 0.2,
        "unit_skin_kPa": 50.0,
        "unit_end_bearing_kPa": 1000.0,
    }
    response = client.post("/pile-axial", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "capacity_kN" in data


def test_corrosion_endpoint() -> None:
    """Test corrosion calculation endpoint."""
    payload = {"t0_mm": 16.0, "rate_mm_per_year": 0.1, "years": 50.0}
    response = client.post("/corrosion", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "remaining_thickness_mm" in data


def test_seawall_endpoint() -> None:
    """Test seawall sliding FS endpoint."""
    payload = {"mu": 0.6, "W_kN": 1000.0, "T_kN": 400.0}
    response = client.post("/seawall", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "sliding_fs" in data


def test_scour_endpoint() -> None:
    """Test scour calculation endpoint."""
    payload = {"D_m": 1.2, "U_mps": 1.5, "K": 2.0, "m": 1.0}
    response = client.post("/scour", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "scour_depth_m" in data


def test_waves_invalid_input() -> None:
    """Test error handling for invalid wave inputs."""
    payload = {"T_s": -10.0, "h_m": 50.0}
    response = client.post("/waves", json=payload)
    assert response.status_code == 422  # FastAPI returns 422 for validation errors
