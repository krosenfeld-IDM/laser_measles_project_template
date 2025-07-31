# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a project template built on the laser-measles framework - a spatial measles modeling toolkit that extends the LASER (Large-scale Agent-based Spatial Epidemiological Research) framework. The project provides a starting point for epidemiological modeling with both the laser-measles library (as a git submodule) and project-specific customizations.

## Project Structure

### Key Directories
- `laser-measles/` - Git submodule containing the core laser-measles framework
- `src/project/` - Project-specific extensions and customizations
- `src/project/abm/` - Agent-based model components and extensions
- `src/project/abm/components/` - Custom ABM components
- `tests/` - Project-specific test files
- `tests/test_event_system.py` - Integration tests for event system

### Architecture Overview

The project follows a component-based architecture where:
- **ABMModel** (in `src/project/abm/model.py`) extends the base laser-measles ABM with event system integration
- **Components** are modular units that handle specific aspects (vital dynamics, disease transmission, tracking)
- **EventBus** provides inter-component communication without tight coupling
- **Events** carry information between components (deaths, births, infections, etc.)

## Common Development Commands

### Environment Setup
```bash
# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment with all dependencies
uv sync

# Install laser-measles submodule in development mode
cd laser-measles
uv pip install -e ".[dev]"
cd ..

# For full development (includes examples and documentation)
cd laser-measles  
uv pip install -e ".[full]"
cd ..
```

### Submodule Management
```bash
# Initialize submodules after cloning
git submodule update --init --recursive

# Update submodule to specific tag
cd laser-measles
git checkout v0.7.2-dev3
cd ..
git add laser-measles
git commit -m "Update submodule to v0.7.2-dev3"

# Update submodule to latest
git submodule update --remote laser-measles
```

### Testing
```bash
# Activate virtual environment first
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run laser-measles tests
cd laser-measles
pytest tests/unit/ -v
pytest tests/scientific/ -v  # Scientific validation tests
pytest -m "not slow"  # Skip slow tests
cd ..

# Run project-specific tests
python tests/test_event_system.py
# Or run all project tests
pytest tests/ -v

# Run tests with coverage (in laser-measles directory)
pytest --cov --cov-report=term-missing --cov-report=xml -vv tests
```

### Code Quality
```bash
# Format and lint code (run from laser-measles directory)
ruff check src/ tests/
ruff format src/ tests/

# Type checking (if available)
mypy src/
pyright src/
```

### CLI Usage
```bash
# Test laser-measles CLI
laser-measles --help
```

## Project-Specific Architecture

### Enhanced ABM Model with Event System

The project extends the base laser-measles ABM with a comprehensive event system:

#### Event System Components (`src/project/abm/events.py`)
- **BaseEvent**: Abstract base for all events with timestamp, source, and data
- **VitalDynamicsEvent**: Deaths, births, aging events  
- **DiseaseEvent**: Infections, transmission, recovery events
- **ModelEvent**: Model lifecycle events (init, tick start/end, complete)
- **EventBus**: Central dispatcher managing subscriptions and event emission
- **EventMixin**: Mixin class to add event capabilities to components

#### Enhanced ABM Model (`src/project/abm/model.py`)
- Integrates EventBus into model initialization
- Emits model lifecycle events (init, tick_start, tick_end, complete)
- Automatically sets up event capabilities for components
- Maintains backward compatibility with existing components

#### Event-Enabled Components
- **ProcessVitalDynamics**: Emits death and birth events with agent details (no longer includes vaccination)
- **DeathMonitorTracker**: Tracks death statistics by listening to death events
- Custom components can inherit from EventMixin to gain event capabilities

### Event System Usage Patterns

#### Making a Component Event-Aware
```python
from laser_measles.abm.base import BaseComponent
from project.abm.events import EventMixin

class MyComponent(BaseComponent, EventMixin):
    def __init__(self, model, verbose=False):
        super().__init__(model, verbose)
        self.__init_event_mixin__()
    
    def set_event_bus(self, event_bus):
        """Called automatically by ABMModel"""
        self._event_bus = event_bus
        self.subscribe_to_events(['deaths', 'births'], self.handle_vital_events)
    
    def __call__(self, model, tick):
        # Emit events during processing
        self.emit_event('my_custom_event', 
                       data={'info': 'example'}, 
                       tick=tick)
    
    def handle_vital_events(self, event):
        # React to death/birth events
        if event.event_type == 'deaths':
            agent_indices = event.data['agent_indices']
            # Process death information
```

#### Event Data Structure
Events carry rich contextual information:
```python
# Death event example
{
    'event_type': 'deaths',
    'agent_indices': [1, 5, 8],           # Which agents died
    'patch_ids': [0, 1, 0],               # Where they died
    'disease_states': [2, 1, 3],          # Their disease states
    'num_deaths': 3,                      # Total count
    'tick': 15                            # When it happened
}

# Birth event example (vaccination_delay removed)
{
    'event_type': 'births',
    'agent_indices': [100, 101, 102],     # New agent indices
    'patch_births': [2, 1, 0],           # Births per patch
    'total_births': 3,                    # Total new births
    'birth_rate': 0.02,                   # Birth rate used
    'tick': 15                            # When births occurred
}
```

### Model Characteristics

#### Disease Dynamics Without Vaccination
This model focuses on **natural disease dynamics only**:
- **No MCV1 vaccination**: Routine immunization has been completely removed
- **No vaccination scheduling**: Newborns remain susceptible throughout the simulation  
- **Pure epidemiological modeling**: Disease spreads based on transmission, recovery, and vital dynamics only
- **Simplified vital dynamics**: Birth and death processes without vaccination complications

#### Scenario Data Requirements
The model requires scenario data with these fields:
- `pop`: Population count per patch (integer)
- `lat`: Latitude (float)
- `lon`: Longitude (float)  
- `id`: Patch identifiers (string or integer)
- **Note**: `mcv1` field has been removed - no vaccination coverage data needed

### Development Guidelines

#### Component Development
1. Inherit from appropriate base class (BaseComponent, BaseTracker, etc.)
2. Use Pydantic for parameter validation following existing patterns
3. Add EventMixin for inter-component communication needs
4. Implement `set_event_bus()` method if component needs event capabilities
5. Use `__call__(model, tick)` for per-tick execution
6. Follow Google docstring conventions

#### Event System Best Practices
1. **Emit Meaningful Events**: Include relevant data (agent indices, locations, states)
2. **Use Appropriate Event Types**: VitalDynamicsEvent for births/deaths, DiseaseEvent for infections
3. **Handle Events Gracefully**: Use try/catch in event handlers to prevent simulation crashes
4. **Minimal Performance Impact**: Event system adds ~1ms overhead per simulation

#### Model Integration
```python
from project.abm import ABMModel, ABMParams
from laser_measles.scenarios.synthetic import SyntheticScenario

# Create model with event system
scenario = SyntheticScenario(num_patches=10, population_size=10000)
params = ABMParams(num_ticks=365, use_numba=False)
model = ABMModel(scenario, params, name="test_model")

# Add components (event capabilities set up automatically)
model.components = [
    ProcessVitalDynamics,
    ProcessInfection, 
    DeathMonitorTracker  # This component will listen to death events
]

model.run()

# Access event statistics
stats = model.event_bus.get_stats()
print(f"Events emitted: {stats['events_emitted']}")
```

## Dependencies and Requirements

### Core Dependencies (from pyproject.toml)
- Python 3.11+
- laser-core>=0.5.1 - Core LASER framework
- pydantic>=2.11.5 - Parameter validation
- polars>=1.30.0 - DataFrame operations  
- alive-progress>=3.2.0 - Progress bars
- typer>=0.12.0 - CLI framework
- numpy, numba - Numerical computing

### Laser-Measles Dependencies
- All dependencies from laser-measles submodule
- Additional dev dependencies available via `[dev]` and `[full]` extras

## File Organization

### Naming Conventions
- Components: `process_*.py` for processes, `tracker_*.py` for trackers
- Tests: `test_*.py` pattern
- Use snake_case for Python files, PascalCase for class names
- Event types: lowercase strings ('deaths', 'births', 'infections')

### Component Categories
- **Process Components**: Modify model state (births, deaths, infection, transmission)
- **Tracker Components**: Record metrics and state over time  
- **Initialization Components**: Set up initial conditions

## Testing Strategy

### Test Types
- **Unit Tests**: In `laser-measles/tests/unit/` for framework components
- **Scientific Tests**: In `laser-measles/tests/scientific/` for model validation
- **Integration Tests**: Project-level tests in `tests/` directory

### Event System Testing
The `tests/test_event_system.py` demonstrates:
- Full model execution with event system
- Event emission and subscription verification
- Component interaction through events
- Performance impact measurement

## Legacy Compatibility

The project maintains full backward compatibility:
- Existing components work unchanged
- Event system is optional - components can opt-in
- No breaking changes to existing laser-measles functionality
- Performance impact is minimal (< 1ms per simulation)

## Common Issues and Solutions

1. **Submodule Not Initialized**: Run `git submodule update --init --recursive`
2. **Import Errors**: Ensure virtual environment is activated and both project and laser-measles are installed
3. **Event System Not Working**: Check that components inherit from EventMixin and implement `set_event_bus()`
4. **Performance Issues**: Use `use_numba=True` in model parameters for large simulations
5. **MCV1/Vaccination Errors**: This model has vaccination completely removed. Do not include `mcv1` fields in scenario data or vaccination parameters in components