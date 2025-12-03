"""Event system for decoupled communication."""
from typing import Callable, Dict, List, Any
from collections import defaultdict


class EventBus:
    """Simple event bus for publish-subscribe pattern."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)
        self._initialized = True
    
    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to an event."""
        if callback not in self._listeners[event_type]:
            self._listeners[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """Unsubscribe from an event."""
        if callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)
    
    def publish(self, event_type: str, **kwargs):
        """Publish an event to all subscribers."""
        for callback in self._listeners[event_type]:
            try:
                callback(**kwargs)
            except Exception as e:
                print(f"Error in event handler for {event_type}: {e}")
    
    def clear(self):
        """Clear all event listeners."""
        self._listeners.clear()


# Event types constants
class Events:
    """Event type constants."""
    PLAYER_DIED = "player_died"
    PLAYER_DAMAGED = "player_damaged"
    PLAYER_HEALED = "player_healed"
    ENEMY_DIED = "enemy_died"
    COIN_COLLECTED = "coin_collected"
    WEAPON_SWITCHED = "weapon_switched"
    MAGIC_SWITCHED = "magic_switched"
    INVENTORY_OPENED = "inventory_opened"
    MENU_OPENED = "menu_opened"
    GAME_PAUSED = "game_paused"
    GAME_RESUMED = "game_resumed"


# Global instance
event_bus = EventBus()
