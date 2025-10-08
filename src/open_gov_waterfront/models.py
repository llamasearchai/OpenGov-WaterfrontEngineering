"""
Pydantic models for API requests and responses.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class WaveRequest(BaseModel):
    T_s: float = Field(..., gt=0, description="Wave period (s)")
    h_m: float = Field(..., gt=0, description="Water depth (m)")


class WaveResponse(BaseModel):
    wavelength_m: float
    celerity_mps: float
    group_celerity_mps: float
    shoaling_coefficient: float


class MorisonRequest(BaseModel):
    D_m: float = Field(..., gt=0, description="Pile diameter (m)")
    u_amp_mps: float = Field(..., ge=0, description="Velocity amplitude (m/s)")
    a_amp_mps2: float = Field(..., description="Acceleration amplitude (m/s^2)")
    Cd: float = Field(1.0, description="Drag coefficient")
    Cm: float = Field(2.0, description="Inertia coefficient")


class MorisonResponse(BaseModel):
    force_per_length_Npm: float


class BerthingRequest(BaseModel):
    mass_tonnes: float = Field(..., gt=0, description="Vessel mass (tonnes)")
    speed_knots: float = Field(..., gt=0, description="Berthing speed (knots)")
    Ce: float = Field(1.0, description="Eccentricity coefficient")
    Cc: float = Field(1.0, description="Configuration coefficient")
    Cs: float = Field(1.0, description="Softness coefficient")
    efficiency: float = Field(0.7, gt=0, description="Fender efficiency")
    deflection_m: float = Field(0.5, gt=0, description="Fender deflection (m)")


class BerthingResponse(BaseModel):
    energy_J: float
    fender_reaction_kN: float


class MooringRequest(BaseModel):
    A_wind_m2: float = Field(..., ge=0, description="Projected wind area (m^2)")
    A_current_m2: float = Field(..., ge=0, description="Projected current area (m^2)")
    U_wind_mps: float = Field(..., ge=0, description="Wind speed (m/s)")
    U_current_mps: float = Field(..., ge=0, description="Current speed (m/s)")
    Cd_wind: float = Field(1.0, description="Wind drag coefficient")
    Cd_current: float = Field(1.0, description="Current drag coefficient")
    safety_factor: float = Field(1.5, gt=0, description="Safety factor")


class MooringResponse(BaseModel):
    total_load_N: float


class PileAxialRequest(BaseModel):
    shaft_length_m: float = Field(..., gt=0, description="Shaft length (m)")
    perimeter_m: float = Field(..., gt=0, description="Perimeter (m)")
    area_tip_m2: float = Field(..., gt=0, description="Tip area (m^2)")
    unit_skin_kPa: float = Field(..., ge=0, description="Unit skin friction (kPa)")
    unit_end_bearing_kPa: float = Field(..., ge=0, description="Unit end bearing (kPa)")


class PileAxialResponse(BaseModel):
    capacity_kN: float


class CorrosionRequest(BaseModel):
    t0_mm: float = Field(..., gt=0, description="Initial thickness (mm)")
    rate_mm_per_year: float = Field(..., ge=0, description="Corrosion rate (mm/yr)")
    years: float = Field(..., ge=0, description="Service life (years)")


class CorrosionResponse(BaseModel):
    remaining_thickness_mm: float


class SeawallRequest(BaseModel):
    mu: float = Field(..., gt=0, description="Base friction coefficient")
    W_kN: float = Field(..., gt=0, description="Wall weight (kN)")
    T_kN: float = Field(..., gt=0, description="Horizontal thrust (kN)")


class SeawallResponse(BaseModel):
    sliding_fs: float


class ScourRequest(BaseModel):
    D_m: float = Field(..., gt=0, description="Pile diameter (m)")
    U_mps: float = Field(..., ge=0, description="Current speed (m/s)")
    K: float = Field(2.0, gt=0, description="Scour coefficient")
    m: float = Field(1.0, gt=0, description="Scour exponent")


class ScourResponse(BaseModel):
    scour_depth_m: float


class HealthResponse(BaseModel):
    status: str
    version: str
