import json
import os
from datetime import datetime

class SaveSystem:
    def __init__(self, save_dir="saves"):
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
    def get_save_info(self, slot=1):
        """Get metadata for a specific save slot."""
        filename = os.path.join(self.save_dir, f"save_{slot}.json")
        if not os.path.exists(filename):
            return None
            
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                return {
                    "slot": slot,
                    "timestamp": data.get("timestamp", "Unknown"),
                    # Add usage info later like player level, area, etc.
                }
        except:
            return None

    def get_all_slots(self, max_slots=3):
        """Get info for all slots."""
        slots = []
        for i in range(1, max_slots + 1):
            info = self.get_save_info(i)
            if info:
                slots.append(info)
            else:
                slots.append({"slot": i, "empty": True})
        return slots
    
    def save_game(self, target, slot=1):
        """Save game state to a JSON file. Target can be Level or Player."""
        # Determine if target is Level (has player) or Player
        if hasattr(target, 'player'):
            player = target.player
        else:
            player = target

        data = {
            "timestamp": str(datetime.now()),
            "player": {
                "pos": (player.hitbox.centerx, player.hitbox.centery),
                "stats": player.stats,
                "health": player.health,
                "energy": player.energy,
                "coin": player.coin,
                "weapon_index": player.weapon_index,
                "magic_index": player.magic_index,
                # Simple inventory serialization if feasible, otherwise extract items
                "inventory_old": player.inventory_data, # Legacy support
            }
        }
        
        # Save InventorySystem data if available
        if hasattr(player, 'inventory') and hasattr(player.inventory, 'to_dict'):
            data["player"]["inventory"] = player.inventory.to_dict()
        
        filename = os.path.join(self.save_dir, f"save_{slot}.json")
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Game saved to {filename}")
            return True
        except Exception as e:
            print(f"Failed to save game: {e}")
            import traceback
            traceback.print_exc()
            return False

    def load_game(self, target, slot=1):
        """Load game state from a JSON file. Target can be Level or Player."""
        if hasattr(target, 'player'):
            player = target.player
        else:
            player = target
            
        filename = os.path.join(self.save_dir, f"save_{slot}.json")
        if not os.path.exists(filename):
            print(f"Save file {filename} not found.")
            return False
            
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            p_data = data["player"]
            
            # Restore position
            if "pos" in p_data:
                player.hitbox.center = p_data["pos"]
                player.rect.center = player.hitbox.center
                
            # Restore stats
            player.stats.update(p_data.get("stats", {}))
            player.health = p_data.get("health", player.stats['health'])
            player.energy = p_data.get("energy", player.stats['energy'])
            player.coin = p_data.get("coin", 0)
            player.weapon_index = p_data.get("weapon_index", 0)
            player.magic_index = p_data.get("magic_index", 0)
            
            # Update derived attributes
            player.weapon = list(player.weapon_data.keys())[player.weapon_index] if hasattr(player, 'weapon_data') else player.weapon
            player.magic = list(player.magic_data.keys())[player.magic_index] if hasattr(player, 'magic_data') else player.magic
            
            # Restore InventorySystem
            if "inventory" in p_data and hasattr(player, 'inventory') and hasattr(player.inventory, 'from_dict'):
                player.inventory.from_dict(p_data["inventory"])
            elif "inventory_old" in p_data:
                player.inventory_data = p_data["inventory_old"]
                
            print(f"Game loaded from {filename}")
            return True
        except Exception as e:
            print(f"Failed to load game: {e}")
            return False
