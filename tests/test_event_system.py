#!/usr/bin/env python3
"""
Test script for the ABM event system.

This script creates a simple ABM model with vital dynamics and death monitoring
components to demonstrate the event system functionality.
"""

import polars as pl
import numpy as np
from src.project.abm.model import ABMModel
from src.project.abm.params import ABMParams
from src.project.abm.components import (
    VitalDynamicsProcess, 
    VitalDynamicsParams,
    DeathMonitorTracker,
    DeathMonitorParams,
    DeathAwareComponent
)


def create_simple_scenario():
    """Create a simple scenario for testing."""
    return pl.DataFrame({
        'pop': [1000, 800, 1200],  # Population in each patch
        'lat': [40.7, 40.8, 40.9],  # Latitude
        'lon': [-74.0, -74.1, -74.2],  # Longitude
        'id': ['patch_1', 'patch_2', 'patch_3']  # Patch IDs
    })


def test_event_system():
    """Test the event system with a simple simulation."""
    print("Testing ABM Event System")
    print("=" * 50)
    
    # Create scenario and parameters
    
    scenario = create_simple_scenario()
    params = ABMParams(
        num_ticks=10,  # Short simulation
        verbose=True,
        show_progress=False,  # Disable progress bar for cleaner output
        seed=12345
    )
    
    print(f"Scenario: {len(scenario)} patches with {scenario['pop'].sum()} total population")
    print(f"Simulation: {params.num_ticks} ticks")
    print()
    
    # Create model
    model = ABMModel(scenario, params, name="event_test_model")
    
    # Setup components with vital dynamics and event monitoring
    # Override the default death rate to make sure we see some deaths
    vital_params = VitalDynamicsParams(
        crude_death_rate=200.0  # Very high death rate for testing (200 per 1000 per year)
    )
    
    death_monitor_params = DeathMonitorParams(
        track_death_locations=True,
        track_death_states=True,
        verbose_deaths=True
    )
    
    # Create component classes with parameters
    class ConfiguredVitalDynamics(VitalDynamicsProcess):
        def __init__(self, model, verbose=False):
            super().__init__(model, verbose=verbose, params=vital_params)
    
    class ConfiguredDeathMonitor(DeathMonitorTracker):
        def __init__(self, model, verbose=False):
            super().__init__(model, verbose=verbose, params=death_monitor_params)
    
    # Add components to model
    model.components = [
        ConfiguredVitalDynamics,
        ConfiguredDeathMonitor,
        DeathAwareComponent
    ]
    
    print("Components added:")
    for i, comp in enumerate(model.components, 1):
        print(f"  {i}. {comp.__name__}")
    print()
    
    # Run the simulation
    print("Running simulation...")
    print("-" * 30)
    model.run()
    print("-" * 30)
    print("Simulation completed!")
    print()
    
    # Check event system statistics
    stats = model.event_bus.get_stats()
    print("Event System Statistics:")
    print(f"  Events emitted: {stats['events_emitted']}")
    print(f"  Total subscribers: {stats['total_subscribers']}")
    print(f"  Active event types: {stats['active_event_types']}")
    print(f"  Dispatch errors: {stats['dispatch_errors']}")
    print()
    
    # Get death monitor results
    death_monitor = None
    death_aware = None
    
    for instance in model.instances:
        if isinstance(instance, DeathMonitorTracker):
            death_monitor = instance
        elif isinstance(instance, DeathAwareComponent):
            death_aware = instance
    
    if death_monitor:
        summary = death_monitor.get_death_summary()
        print("Death Monitor Summary:")
        print(f"  Total deaths: {summary['total_deaths']}")
        print(f"  Death events: {summary['num_death_events']}")
        if summary['deaths_by_patch']:
            print(f"  Deaths by patch: {summary['deaths_by_patch']}")
        if summary['deaths_by_state']:
            print(f"  Deaths by state: {summary['deaths_by_state']}")
        print(f"  Recent death indices: {len(death_monitor.get_recent_deaths())}")
        print(f"  All death indices: {len(death_monitor.get_all_deaths())}")
        print()
    
    if death_aware:
        print("Death Aware Component:")
        print(f"  Death reactions: {death_aware.get_reaction_count()}")
        print()
    
    # Verify the event system worked
    print("Event System Verification:")
    if stats['events_emitted'] > 0:
        print("  ✓ Events were emitted")
    else:
        print("  ✗ No events were emitted")
    
    if stats['total_subscribers'] > 0:
        print("  ✓ Components subscribed to events")
    else:
        print("  ✗ No components subscribed to events")
    
    if death_monitor and death_monitor.total_deaths > 0:
        print("  ✓ Death events were processed")
    else:
        print("  ✗ No death events were processed")
    
    if death_aware and death_aware.get_reaction_count() > 0:
        print("  ✓ Components reacted to events")
    else:
        print("  ✗ No components reacted to events")
    
    print()
    print("Test completed successfully!")
    
    # Cleanup
    model.cleanup()
    
    return model, death_monitor, death_aware


if __name__ == "__main__":
    # Run the test
    model, death_monitor, death_aware = test_event_system()
    
    # Optional: Interactive exploration
    print("\nComponents available for inspection:")
    print("  - model: ABMModel instance")
    print("  - death_monitor: DeathMonitorTracker instance")  
    print("  - death_aware: DeathAwareComponent instance")
    print("\nExample usage:")
    print("  death_monitor.get_death_summary()")
    print("  model.event_bus.get_stats()")