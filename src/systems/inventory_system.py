"""Inventory system for managing player items."""
from typing import Optional, Dict, List
from config.game_data import ITEM_DATA


class InventorySlot:
    """Represents a single slot in the inventory."""
    
    def __init__(self):
        self.item_id: Optional[str] = None
        self.quantity: int = 0
    
    def is_empty(self) -> bool:
        """Check if slot is empty."""
        return self.item_id is None or self.quantity <= 0
    
    def add_quantity(self, amount: int) -> int:
        """Add quantity to slot. Returns overflow if any."""
        if not self.item_id:
            return amount
        
        item_data = ITEM_DATA.get(self.item_id, {})
        max_stack = item_data.get('max_stack', 1)
        
        new_quantity = self.quantity + amount
        if new_quantity <= max_stack:
            self.quantity = new_quantity
            return 0
        else:
            self.quantity = max_stack
            return new_quantity - max_stack
    
    def remove_quantity(self, amount: int) -> int:
        """Remove quantity from slot. Returns actual amount removed."""
        if self.quantity >= amount:
            self.quantity -= amount
            removed = amount
            if self.quantity <= 0:
                self.clear()
            return removed
        else:
            removed = self.quantity
            self.clear()
            return removed
    
    def set_item(self, item_id: str, quantity: int = 1):
        """Set item in slot."""
        self.item_id = item_id
        self.quantity = quantity
    
    def clear(self):
        """Clear the slot."""
        self.item_id = None
        self.quantity = 0
    
    def get_item_data(self) -> Dict:
        """Get item data from game data."""
        if self.item_id:
            return ITEM_DATA.get(self.item_id, {})
        return {}

    def to_dict(self):
        return {"item_id": self.item_id, "quantity": self.quantity}
    
    def from_dict(self, data):
        self.item_id = data.get("item_id")
        self.quantity = data.get("quantity", 0)


class InventorySystem:
    """Manages player inventory with 20 slots."""
    
    MAX_SLOTS = 20
    
    def __init__(self):
        self.slots: List[InventorySlot] = [InventorySlot() for _ in range(self.MAX_SLOTS)]
        self.selected_index = 0

    def to_dict(self):
        return {
            "slots": [slot.to_dict() for slot in self.slots],
            "selected_index": self.selected_index
        }

    def from_dict(self, data):
        slot_data = data.get("slots", [])
        for i, s_data in enumerate(slot_data):
            if i < len(self.slots):
                self.slots[i].from_dict(s_data)
        self.selected_index = data.get("selected_index", 0)
    
    def add_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Add item to inventory.
        
        Args:
            item_id: ID of item to add
            quantity: Amount to add
            
        Returns:
            True if successfully added, False if inventory full
        """
        if item_id not in ITEM_DATA:
            print(f"Warning: Item '{item_id}' not found in ITEM_DATA")
            return False
        
        item_data = ITEM_DATA[item_id]
        is_stackable = item_data.get('stackable', False)
        
        remaining = quantity
        
        # If stackable, try to add to existing stacks first
        if is_stackable:
            for slot in self.slots:
                if slot.item_id == item_id and not slot.is_empty():
                    overflow = slot.add_quantity(remaining)
                    remaining = overflow
                    if remaining <= 0:
                        return True
        
        # Find empty slots for remaining items
        while remaining > 0:
            empty_slot = self._find_empty_slot()
            if empty_slot is None:
                print(f"Inventory full! Could not add {remaining} of {item_id}")
                return False
            
            # Add to empty slot
            if is_stackable:
                max_stack = item_data.get('max_stack', 1)
                add_amount = min(remaining, max_stack)
                empty_slot.set_item(item_id, add_amount)
                remaining -= add_amount
            else:
                empty_slot.set_item(item_id, 1)
                remaining -= 1
        
        return True
    
    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Remove item from inventory.
        
        Args:
            item_id: ID of item to remove
            quantity: Amount to remove
            
        Returns:
            True if successfully removed, False if not enough items
        """
        # Check if we have enough
        total = self.count_item(item_id)
        if total < quantity:
            return False
        
        remaining = quantity
        for slot in self.slots:
            if slot.item_id == item_id and remaining > 0:
                removed = slot.remove_quantity(remaining)
                remaining -= removed
        
        return remaining <= 0
    
    def remove_item_at_slot(self, slot_index: int, quantity: int = 1) -> bool:
        """Remove item from specific slot."""
        if 0 <= slot_index < self.MAX_SLOTS:
            slot = self.slots[slot_index]
            if not slot.is_empty():
                slot.remove_quantity(quantity)
                return True
        return False
    
    def get_item(self, item_id: str) -> Optional[InventorySlot]:
        """Get first slot containing item."""
        for slot in self.slots:
            if slot.item_id == item_id:
                return slot
        return None
    
    def get_slot(self, index: int) -> Optional[InventorySlot]:
        """Get slot at index."""
        if 0 <= index < self.MAX_SLOTS:
            return self.slots[index]
        return None
    
    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """Check if inventory has item."""
        return self.count_item(item_id) >= quantity
    
    def count_item(self, item_id: str) -> int:
        """Count total quantity of item in inventory."""
        total = 0
        for slot in self.slots:
            if slot.item_id == item_id:
                total += slot.quantity
        return total
    
    def has_space(self) -> bool:
        """Check if inventory has any empty slots."""
        return self._find_empty_slot() is not None
    
    def get_empty_slots_count(self) -> int:
        """Get number of empty slots."""
        return sum(1 for slot in self.slots if slot.is_empty())
    
    def clear(self):
        """Clear entire inventory."""
        for slot in self.slots:
            slot.clear()
        self.selected_index = 0
    
    def _find_empty_slot(self) -> Optional[InventorySlot]:
        """Find first empty slot."""
        for slot in self.slots:
            if slot.is_empty():
                return slot
        return None
    
    def move_selection(self, direction: str):
        """
        Move selected slot index.
        
        Args:
            direction: 'up', 'down', 'left', 'right'
        """
        cols = 5  # 5 columns
        rows = 4  # 4 rows (20 slots total)
        
        current_row = self.selected_index // cols
        current_col = self.selected_index % cols
        
        if direction == 'up':
            current_row = max(0, current_row - 1)
        elif direction == 'down':
            current_row = min(rows - 1, current_row + 1)
        elif direction == 'left':
            current_col = max(0, current_col - 1)
        elif direction == 'right':
            current_col = min(cols - 1, current_col + 1)
        
        self.selected_index = current_row * cols + current_col
    
    def get_selected_slot(self) -> InventorySlot:
        """Get currently selected slot."""
        return self.slots[self.selected_index]
    
    def use_selected_item(self) -> Optional[Dict]:
        """Use/activate selected item. Returns item data if used."""
        slot = self.get_selected_slot()
        if slot.is_empty():
            return None
        
        item_data = slot.get_item_data()
        item_type = item_data.get('type')
        
        # For consumables, remove one from inventory
        if item_type == 'normal' and item_data.get('stackable', False):
            # Check if it's a consumable (has heal_amount or mana_amount)
            if 'heal_amount' in item_data or 'mana_amount' in item_data:
                slot.remove_quantity(1)
        
        return item_data
    
    def get_all_items(self) -> List[Dict]:
        """Get list of all items with their quantities."""
        items = []
        for i, slot in enumerate(self.slots):
            if not slot.is_empty():
                items.append({
                    'slot_index': i,
                    'item_id': slot.item_id,
                    'quantity': slot.quantity,
                    'data': slot.get_item_data()
                })
        return items
    
    def debug_print(self):
        """Print inventory contents for debugging."""
        print("\n=== INVENTORY ===")
        for i, slot in enumerate(self.slots):
            if not slot.is_empty():
                item_data = slot.get_item_data()
                print(f"Slot {i}: {item_data.get('name', 'Unknown')} x{slot.quantity}")
        print(f"Empty slots: {self.get_empty_slots_count()}")
        print("================\n")
