# project

## Project Structure
- `laser-measles/` - Git submodule containing the core laser-measles framework
- `src/project/` - Project-specific extensions and customizations
- `tests/` - Project-specific test files

## Setup

### Initializing the Submodule

After cloning this repository, you need to initialize and update the submodule:

```bash
git submodule update --init --recursive
```

### Using a Specific Tag

To configure the submodule to use a specific tag (e.g., v0.7.2-dev3):

1. Navigate to the submodule directory:
   ```bash
   cd laser-measles
   ```

2. Checkout the desired tag:
   ```bash
   git checkout v0.7.2-dev3
   ```

3. Return to the project root and commit the submodule reference:
   ```bash
   cd ..
   git add laser-measles
   git commit -m "Update submodule to v0.7.2-dev3"
   ```

### Updating the Submodule

To update the submodule to the latest commit on its default branch:

```bash
git submodule update --remote laser-measles
```

## Project Initialization

### Prerequisites

- Python 3.11+ (recommended)
- Git

### Installation Steps

1. **Clone the repository with submodules:**
   ```bash
   git clone --recurse-submodules <repository-url>
   cd laser_measles_project_template
   ```

2. **Install UV (Python package manager):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install project and dependencies:**
   ```bash
   # This creates a virtual environment and installs all dependencies
   uv sync
   
   # Install laser-measles submodule
   cd laser-measles
   uv pip install -e ".[dev]"
   cd ..
   ```

4. **Verify installation:**
   ```bash
   # Activate the environment
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Run tests to ensure everything is working
   cd laser-measles
   pytest tests/unit/ -v
   cd ..
   ```

### Development Setup

For full development including examples and documentation for laser-measles:

```bash
cd laser-measles
uv pip install -e ".[full]"
cd ..
```

### Quick Start

After installation, you can run a basic model:

```python
from laser_measles.abm import ABMModel, ABMParams
from laser_measles.scenarios.synthetic import SyntheticScenario

# Create a simple scenario and model
scenario = SyntheticScenario(num_patches=10, population_size=10000)
params = ABMParams(num_ticks=365, use_numba=False)
model = ABMModel(scenario, params, name="test_model")

# Add basic components and run
from laser_measles.abm.components import *
model.components = [
    ProcessVitalDynamics,
    ProcessInfection,
    ProcessTransmission,
    TrackerState
]

model.run()
```