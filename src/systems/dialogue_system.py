"""Dialogue system for NPC interactions."""
import pygame
from typing import List, Optional, Dict


class DialogueMessage:
    """Represents a single dialogue message."""
    
    def __init__(self, text: str, speaker: str = "NPC"):
        self.text = text
        self.speaker = speaker


class DialogueSequence:
    """A sequence of dialogue messages."""
    
    def __init__(self, messages: List[str], speaker: str = "NPC"):
        self.messages = [DialogueMessage(msg, speaker) for msg in messages]
        self.current_index = 0
    
    def get_current_message(self) -> Optional[DialogueMessage]:
        """Get current dialogue message."""
        if self.current_index < len(self.messages):
            return self.messages[self.current_index]
        return None
    
    def advance(self) -> bool:
        """Move to next message. Returns True if there are more messages."""
        self.current_index += 1
        return self.current_index < len(self.messages)
    
    def reset(self):
        """Reset to first message."""
        self.current_index = 0
    
    def is_finished(self) -> bool:
        """Check if all messages have been shown."""
        return self.current_index >= len(self.messages)


class DialogueSystem:
    """Manages dialogue state and interactions."""
    
    def __init__(self):
        self.active = False
        self.current_sequence: Optional[DialogueSequence] = None
        self.current_npc = None
        self.dialogue_data: Dict[str, DialogueSequence] = {}
    
    def register_dialogue(self, npc_id: str, messages: List[str], speaker: str = None):
        """Register dialogue for an NPC."""
        speaker_name = speaker or npc_id
        self.dialogue_data[npc_id] = DialogueSequence(messages, speaker_name)
    
    def start_dialogue(self, npc_id: str, npc_obj=None):
        """Start dialogue with an NPC."""
        if npc_id in self.dialogue_data:
            self.current_sequence = self.dialogue_data[npc_id]
            self.current_sequence.reset()
            self.current_npc = npc_obj
            self.active = True
            return True
        return False
    
    def advance_dialogue(self) -> bool:
        """Advance to next dialogue message. Returns False if dialogue ended."""
        if not self.active or not self.current_sequence:
            return False
        
        if not self.current_sequence.advance():
            self.end_dialogue()
            return False
        return True
    
    def end_dialogue(self):
        """End current dialogue."""
        self.active = False
        self.current_sequence = None
        self.current_npc = None
    
    def get_current_message(self) -> Optional[DialogueMessage]:
        """Get current dialogue message."""
        if self.active and self.current_sequence:
            return self.current_sequence.get_current_message()
        return None
    
    def is_active(self) -> bool:
        """Check if dialogue is active."""
        return self.active
