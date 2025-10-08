"""
State profiles for CA, IN, OH waterfront jurisdictions.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

StateCode = Literal["CA", "IN", "OH"]


@dataclass(frozen=True)
class StateProfile:
    code: StateCode
    name: str
    waters: str
    agencies: list[str]
    notes: str


def _ca() -> StateProfile:
    return StateProfile(
        code="CA",
        name="California",
        waters="Pacific coast, bays, tidal channels",
        agencies=["USACE", "NOAA", "CA Coastal Commission", "Regional Boards", "Ports"],
        notes="Coastal processes, sea level rise, seismic considerations; CEQA/Coastal permits.",
    )


def _oh() -> StateProfile:
    return StateProfile(
        code="OH",
        name="Ohio",
        waters="Great Lakes (Lake Erie), Ohio River, inland waterways",
        agencies=["USACE", "ODNR", "OEPA", "Port Authorities"],
        notes="Ice, seiches on Lake Erie, riverine hydraulics; USACE/port coordination.",
    )


def _in_() -> StateProfile:
    return StateProfile(
        code="IN",
        name="Indiana",
        waters="Inland rivers/canals and Ohio River reaches",
        agencies=["USACE", "IDEM", "DNR", "Local Ports"],
        notes="Riverine navigation, scour, debris; inland vessel loads and freshwater properties.",
    )


_REGISTRY: dict[StateCode, StateProfile] = {"CA": _ca(), "OH": _oh(), "IN": _in_()}


def list_states() -> list[StateProfile]:
    return [p for _, p in sorted(_REGISTRY.items(), key=lambda kv: kv[0])]


def get_state(code: StateCode) -> StateProfile:
    if code not in _REGISTRY:
        raise KeyError(
            f"Unsupported state '{code}'. Supported: {', '.join(_REGISTRY.keys())}"
        )
    return _REGISTRY[code]
