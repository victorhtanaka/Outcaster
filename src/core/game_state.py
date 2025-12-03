"""Game state management."""
from abc import ABC, abstractmethod
from enum import Enum, auto
import pygame


class GameState(Enum):
    """Game state enumeration."""
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    INVENTORY = auto()
    DIALOGUE = auto()
    GAME_OVER = auto()
    OBJECTIVE = auto()


class State(ABC):
    """Abstract base class for game states."""
    
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.screen = pygame.display.get_surface()
    
    @abstractmethod
    def handle_events(self, events):
        """Handle input events."""
        pass
    
    @abstractmethod
    def update(self, dt):
        """Update state logic."""
        pass
    
    @abstractmethod
    def render(self):
        """Render state."""
        pass
    
    def enter(self):
        """Called when entering this state."""
        pass
    
    def exit(self):
        """Called when exiting this state."""
        pass


class GameStateManager:
    """Manages game states and transitions."""
    
    def __init__(self):
        self._states = {}
        self._current_state = None
        self._state_stack = []
    
    def register_state(self, state_type: GameState, state: State):
        """Register a state."""
        self._states[state_type] = state
    
    def change_state(self, state_type: GameState):
        """Change to a different state."""
        if self._current_state:
            self._current_state.exit()
        
        self._current_state = self._states.get(state_type)
        
        if self._current_state:
            self._current_state.enter()
    
    def push_state(self, state_type: GameState):
        """Push a state onto the stack (for overlays)."""
        if self._current_state:
            self._state_stack.append(self._current_state)
        
        self._current_state = self._states.get(state_type)
        
        if self._current_state:
            self._current_state.enter()
    
    def pop_state(self):
        """Pop the current state and return to previous."""
        if self._current_state:
            self._current_state.exit()
        
        if self._state_stack:
            self._current_state = self._state_stack.pop()
            if self._current_state:
                self._current_state.enter()
    
    def handle_events(self, events):
        """Handle events for current state."""
        if self._current_state:
            self._current_state.handle_events(events)
    
    def update(self, dt):
        """Update current state."""
        if self._current_state:
            self._current_state.update(dt)
    
    def render(self):
        """Render current state."""
        if self._current_state:
            self._current_state.render()
    
    @property
    def current_state(self):
        """Get current state."""
        return self._current_state
