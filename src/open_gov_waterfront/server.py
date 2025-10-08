"""
FastAPI server for OpenGov-WaterfrontEngineering calculations.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import __version__
from .berthing import berthing_energy_J, fender_reaction_kN
from .corrosion import CorrosionInputs, remaining_thickness_mm
from .models import (
    BerthingRequest,
    BerthingResponse,
    CorrosionRequest,
    CorrosionResponse,
    HealthResponse,
    MooringRequest,
    MooringResponse,
    MorisonRequest,
    MorisonResponse,
    PileAxialRequest,
    PileAxialResponse,
    ScourRequest,
    ScourResponse,
    SeawallRequest,
    SeawallResponse,
    WaveRequest,
    WaveResponse,
)
from .mooring import EnvLoads, mooring_total_load_N
from .morison import MorisonCoeffs, morison_inline_max_per_length_N
from .piles import PileAxialInputs, pile_axial_capacity_kN
from .scour import pile_scour_depth_m
from .seawall import sliding_fs
from .states import list_states
from .waves import celerity_c, group_celerity_cg, shoaling_coefficient, wavelength_L

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting OpenGov-WaterfrontEngineering API server v%s", __version__)
    yield
    logger.info("Shutting down OpenGov-WaterfrontEngineering API server")


app = FastAPI(
    title="OpenGov-WaterfrontEngineering",
    description="Marine/waterfront screening toolkit API (CA/IN/OH)",
    version=__version__,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="healthy", version=__version__)


@app.get("/states")
async def get_states() -> JSONResponse:
    """List supported state profiles."""
    states = [
        {
            "code": p.code,
            "name": p.name,
            "waters": p.waters,
            "agencies": p.agencies,
            "notes": p.notes,
        }
        for p in list_states()
    ]
    return JSONResponse(content={"states": states})


@app.post("/waves", response_model=WaveResponse)
async def calculate_waves(req: WaveRequest) -> WaveResponse:
    """Calculate linear wave properties."""
    try:
        L = wavelength_L(req.T_s, req.h_m)
        c = celerity_c(req.T_s, req.h_m)
        cg = group_celerity_cg(req.T_s, req.h_m)
        Ks = shoaling_coefficient(None, req.T_s, req.h_m)
        return WaveResponse(
            wavelength_m=L, celerity_mps=c, group_celerity_mps=cg, shoaling_coefficient=Ks
        )
    except Exception as e:
        logger.error("Error calculating waves: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/morison", response_model=MorisonResponse)
async def calculate_morison(req: MorisonRequest) -> MorisonResponse:
    """Calculate Morison inline force."""
    try:
        FpL = morison_inline_max_per_length_N(
            req.D_m, req.u_amp_mps, req.a_amp_mps2, coeffs=MorisonCoeffs(Cd=req.Cd, Cm=req.Cm)
        )
        return MorisonResponse(force_per_length_Npm=FpL)
    except Exception as e:
        logger.error("Error calculating Morison force: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/berthing", response_model=BerthingResponse)
async def calculate_berthing(req: BerthingRequest) -> BerthingResponse:
    """Calculate berthing energy and fender reaction."""
    try:
        E = berthing_energy_J(req.mass_tonnes, req.speed_knots, Ce=req.Ce, Cc=req.Cc, Cs=req.Cs)
        RkN = fender_reaction_kN(E, efficiency=req.efficiency, deflection_m=req.deflection_m)
        return BerthingResponse(energy_J=E, fender_reaction_kN=RkN)
    except Exception as e:
        logger.error("Error calculating berthing: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/mooring", response_model=MooringResponse)
async def calculate_mooring(req: MooringRequest) -> MooringResponse:
    """Calculate mooring environmental load."""
    try:
        env = EnvLoads(
            A_wind_m2=req.A_wind_m2,
            A_current_m2=req.A_current_m2,
            U_wind_mps=req.U_wind_mps,
            U_current_mps=req.U_current_mps,
            Cd_wind=req.Cd_wind,
            Cd_current=req.Cd_current,
            safety_factor=req.safety_factor,
        )
        F = mooring_total_load_N(env)
        return MooringResponse(total_load_N=F)
    except Exception as e:
        logger.error("Error calculating mooring load: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/pile-axial", response_model=PileAxialResponse)
async def calculate_pile_axial(req: PileAxialRequest) -> PileAxialResponse:
    """Calculate pile axial capacity."""
    try:
        Q = pile_axial_capacity_kN(
            PileAxialInputs(
                shaft_length_m=req.shaft_length_m,
                perimeter_m=req.perimeter_m,
                area_tip_m2=req.area_tip_m2,
                unit_skin_kPa=req.unit_skin_kPa,
                unit_end_bearing_kPa=req.unit_end_bearing_kPa,
            )
        )
        return PileAxialResponse(capacity_kN=Q)
    except Exception as e:
        logger.error("Error calculating pile capacity: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/corrosion", response_model=CorrosionResponse)
async def calculate_corrosion(req: CorrosionRequest) -> CorrosionResponse:
    """Calculate remaining thickness after corrosion."""
    try:
        t = remaining_thickness_mm(
            CorrosionInputs(t0_mm=req.t0_mm, rate_mm_per_year=req.rate_mm_per_year, years=req.years)
        )
        return CorrosionResponse(remaining_thickness_mm=t)
    except Exception as e:
        logger.error("Error calculating corrosion: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/seawall", response_model=SeawallResponse)
async def calculate_seawall(req: SeawallRequest) -> SeawallResponse:
    """Calculate seawall sliding factor of safety."""
    try:
        FS = sliding_fs(req.mu, req.W_kN, req.T_kN)
        return SeawallResponse(sliding_fs=FS)
    except Exception as e:
        logger.error("Error calculating seawall FS: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/scour", response_model=ScourResponse)
async def calculate_scour(req: ScourRequest) -> ScourResponse:
    """Calculate local scour at pile."""
    try:
        ys = pile_scour_depth_m(req.D_m, req.U_mps, K=req.K, m=req.m)
        return ScourResponse(scour_depth_m=ys)
    except Exception as e:
        logger.error("Error calculating scour: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))


def main() -> None:
    """Run the FastAPI server."""
    import uvicorn

    uvicorn.run(
        "open_gov_waterfront.server:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False,
    )


if __name__ == "__main__":
    main()
