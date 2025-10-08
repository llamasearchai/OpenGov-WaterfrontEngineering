# OpenGov-WaterfrontEngineering

A comprehensive terminal-first toolkit for marine and waterfront screening analyses used in public-sector projects. Focus: California (coastal), Ohio (Great Lakes/rivers), and Indiana (inland waterways).

**Author:** Nik Jois <nikjois@llamasearch.ai>

## Features

### Engineering Calculations
- **Linear wave theory:** dispersion, wavelength, celerity, group velocity, shoaling
- **Morison inline force** on piles (wave-structure interaction)
- **Berthing energy** and simple fender reaction estimates
- **Mooring environmental loads** (wind + current forces)
- **Pile axial capacity** (static skin friction + end bearing)
- **Corrosion allowance** for steel structures
- **Seawall sliding factor of safety** (screening)
- **Local scour at piles** (screening-level estimates)
- **Tide harmonic synthesis** from constituents
- **Report template** generation

### Technology Stack
- **Command-line interface (CLI)** using Typer with Rich terminal output
- **FastAPI REST API** with full OpenAPI documentation
- **OpenAI Agents SDK integration** for AI-powered engineering assistance
- **Docker containerization** for easy deployment
- **Comprehensive test suite** with **100% code coverage** (90 tests, 443 statements)
- **Type-safe Python 3.11+** with full mypy type checking

## Safety and Compliance

**IMPORTANT:** These are screening-level tools only. All calculations must be validated against governing standards including:
- ASCE MOP 130 (Waterfront Facilities)
- ASCE 61 (Seismic Design of Piers and Wharves)
- PIANC guidelines
- USACE Engineering Manuals (EM) and Technical Letters (ETL)
- CA Coastal Commission requirements
- NOAA/USACE design data
- Local AHJ and permit requirements

Always obtain professional engineering review and agency approvals for production work.

## Installation

### Using uv (recommended)

```bash
# Install uv: https://docs.astral.sh/uv/
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create environment and sync
uv venv -p 3.11
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Using pip

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Using Docker

```bash
# Build and run with docker-compose
docker-compose up -d

# Or build manually
docker build -t opengov-waterfront:latest .
docker run -p 8000:8000 opengov-waterfront:latest
```

## Quick Start

### Run Tests

```bash
# Using pytest directly
pytest -v

# Using make
make test

# With coverage report
make test-cov

# Using tox
tox
```

### CLI Usage

List supported states:
```bash
opengov-waterfront list-states
```

Calculate wave properties (T=10s, h=50m):
```bash
opengov-waterfront waves --T 10 --h 50
```

Morison inline force:
```bash
opengov-waterfront morison-max --D 1.5 --u 1.0 --a 0.5 --Cd 1.0 --Cm 2.0
```

Berthing energy and fender reaction:
```bash
opengov-waterfront berthing --mass 8000 --speed 0.5 --Ce 1.0 --Cc 1.0 --Cs 1.0 --eff 0.7 --defl 0.4
```

Mooring environmental load:
```bash
opengov-waterfront mooring --Aw 1200 --Ac 800 --Uw 22 --Uc 1.2
```

Pile axial capacity:
```bash
opengov-waterfront pile-axial --L 25 --perim 3.6 --Atip 0.25 --qs 60 --qb 1200
```

Corrosion allowance:
```bash
opengov-waterfront corrosion --t0 16 --rate 0.12 --years 50
```

Seawall sliding factor of safety:
```bash
opengov-waterfront seawall-slide --mu 0.6 --W 1200 --T 400
```

Pile scour estimate:
```bash
opengov-waterfront scour-pile --D 1.2 --U 1.5 --K 2 --m 1
```

Tide synthesis:
```bash
opengov-waterfront tides --A1 0.5 --T1 44714 --P1 0 --A2 0.2 --T2 43200 --P2 1.0 --dur 172800 --dt 600
```

Generate report template:
```bash
opengov-waterfront report-template --out waterfront_report_template.csv
```

### API Server

Start the FastAPI server:
```bash
opengov-waterfront-server
```

Or using uvicorn directly:
```bash
uvicorn open_gov_waterfront.server:app --host 0.0.0.0 --port 8000
```

Access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Example API requests:

```bash
# Health check
curl http://localhost:8000/health

# Calculate wave properties
curl -X POST http://localhost:8000/waves \
  -H "Content-Type: application/json" \
  -d '{"T_s": 10.0, "h_m": 50.0}'

# Calculate Morison force
curl -X POST http://localhost:8000/morison \
  -H "Content-Type: application/json" \
  -d '{"D_m": 1.5, "u_amp_mps": 1.0, "a_amp_mps2": 0.5, "Cd": 1.0, "Cm": 2.0}'
```

### OpenAI Agents SDK Integration

For AI-powered engineering assistance, set your OpenAI API key:

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

Then use the agent in your Python code:

```python
from open_gov_waterfront.agent import WaterfrontAgent

agent = WaterfrontAgent()

# Get engineering guidance
response = agent.query(
    "What wave conditions should I use for a ferry terminal in San Francisco Bay?"
)
print(response)

# Get calculation suggestions
suggestions = agent.suggest_calculation(
    "Designing a new pile-supported wharf for container vessels in Long Beach"
)
print(suggestions)

# Interpret results
interpretation = agent.interpret_results(
    "berthing",
    {"mass_tonnes": 8000, "speed_knots": 0.5},
    {"energy_J": 330000, "fender_reaction_kN": 943}
)
print(interpretation)
```

## Development

### Code Quality

```bash
# Format code
make format

# Run linter
make lint

# Type checking
make typecheck

# Run all checks and tests
make all
```

### Project Structure

```
OpenGov-WaterfrontEngineering/
├── pyproject.toml          # Project configuration
├── tox.ini                 # Tox configuration
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── Makefile                # Development automation
├── README.md               # This file
├── LICENSE                 # MIT License
├── src/
│   └── open_gov_waterfront/
│       ├── __init__.py     # Package initialization
│       ├── cli.py          # Command-line interface
│       ├── server.py       # FastAPI server
│       ├── agent.py        # OpenAI agent integration
│       ├── models.py       # Pydantic models for API
│       ├── utils.py        # Constants and utilities
│       ├── states.py       # State profiles (CA/IN/OH)
│       ├── waves.py        # Linear wave theory
│       ├── morison.py      # Morison equation
│       ├── berthing.py     # Berthing energy
│       ├── mooring.py      # Mooring loads
│       ├── piles.py        # Pile capacity
│       ├── corrosion.py    # Corrosion allowance
│       ├── seawall.py      # Seawall stability
│       ├── scour.py        # Scour estimates
│       ├── tides.py        # Tide synthesis
│       └── reports.py      # Report generation
└── tests/
    ├── test_waves.py
    ├── test_morison.py
    ├── test_berthing.py
    ├── test_mooring.py
    ├── test_piles_corrosion.py
    ├── test_seawall_scour.py
    ├── test_cli_states.py
    └── test_server.py
```

## State-Specific Notes

### California (CA)
- Consider sea level rise per CA Coastal Commission guidance
- Coastal wave transformation and seismic demands per ASCE 61
- CEQA environmental review and Coastal Development Permits
- Coordinate with CA Coastal Commission, USACE, NOAA, and Port authorities

### Ohio (OH)
- Great Lakes (Lake Erie) seiche effects and ice loads
- Variable water levels and storm surge
- Coordinate with ODNR, OEPA, USACE Buffalo District, and Port authorities

### Indiana (IN)
- Riverine hydraulics on Ohio River and inland waterways
- Scour considerations in alluvial channels
- Debris loading and navigation clearances
- Freshwater properties (density, ice)
- Coordinate with USACE Louisville District, IDEM, DNR, and local ports

## Key Equations

### Linear Wave Dispersion
```
ω² = gk tanh(kh)
L = 2π/k
c = ω/k
```

Shoaling coefficient:
```
Ks = √(cg0/cg)
cg = (c/2)(1 + 2kh/sinh(2kh))
```

### Morison Inline Force (per unit length)
```
f(t) = ½ρ CD D |u(t)|u(t) + ρ CM (πD²/4) a(t)
```

### Berthing Energy (PIANC baseline)
```
E = ½ m v² Ce Cc Cs
```

### Mooring Wind/Current Forces
```
Fw = ½ρa CD,w Aw U²
Fc = ½ρ CD,c Ac Uc²
```

### Pile Axial Capacity
```
Q = qs As + qb Ab
```

### Corrosion Allowance
```
tremain = t0 - CR · Y
```

### Seawall Sliding FS (screening)
```
FS = μW/T
```

### Local Scour (screening form)
```
ys = K D (U/√(gD))^m
```

### Tide Synthesis
```
η(t) = Σ Ai cos(ωi t + φi)
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please ensure:
- No emojis in code or documentation
- Complete type annotations
- Comprehensive tests for new features
- Professional engineering standards
- No placeholders or stubs
- Format code with `make format`
- Pass all checks with `make all`

## Support

For issues, questions, or contributions, please contact:
- **Author:** Nik Jois
- **Email:** nikjois@llamasearch.ai

## Version

Current version: 0.1.0

## Test Coverage

**100% code coverage achieved**
- 90 comprehensive tests
- 443 statements covered
- All modules: 100% coverage
- Zero known defects

See [COVERAGE_REPORT.md](COVERAGE_REPORT.md) for detailed coverage analysis.

## Acknowledgments

Developed following industry best practices and standards from:
- ASCE (American Society of Civil Engineers)
- PIANC (World Association for Waterborne Transport Infrastructure)
- USACE (US Army Corps of Engineers)
- NOAA (National Oceanic and Atmospheric Administration)
