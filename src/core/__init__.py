"""Core module."""
from .resource_manager import ResourceManager, resource_manager
from .event_bus import EventBus, event_bus, Events
from .game_state import GameStateManager, GameState

__all__ = [
    'ResourceManager', 'resource_manager',
    'EventBus', 'event_bus', 'Events',
    'GameStateManager', 'GameState'
]
