import pygame
import json
import os

class InputConfig:
    # Default bindings
    DEFAULT_KEYBINDS = {
        'move_up': pygame.K_w,
        'move_down': pygame.K_s,
        'move_left': pygame.K_a,
        'move_right': pygame.K_d,
        'attack': pygame.K_SPACE,
        'magic': pygame.K_LCTRL,
        # note: 'magic_switch' was using 'e' in player input, but interact was also 'e'. 
        # I will separate them or keep them same. In player input logic, it checked keys[pygame.K_e].
        # I'll add 'switch_magic' as a separate action but default to E if that's desired, 
        # BUT 'interact' is usually important. 
        # In Player.input: if keys[pygame.K_e] and self.can_switch_magic: ...
        # In Level.update_playing: elif event.key == pygame.K_e: self.player.try_interact()
        # They share the key. I will define one 'interact' and use it for both for now, or define both.
        # Defining both allows user to separate them if they want.
        'switch_magic': pygame.K_e,
        'interact': pygame.K_e,
        'dash': pygame.K_LSHIFT,
        'inventory': pygame.K_i,
        'menu': pygame.K_ESCAPE,
        'journal': pygame.K_g, # Was using G for dialogue debug?
        'dialogue_advance': pygame.K_SPACE,
        # Menu navigation keys (often hardcoded or separate, but can be bound)
        # 'menu_up': pygame.K_UP,
        # 'menu_down': pygame.K_DOWN,
        # 'menu_confirm': pygame.K_RETURN,
        # 'menu_back': pygame.K_BACKSPACE
    }
    
    # Store current bindings
    keybinds = DEFAULT_KEYBINDS.copy()
    config_path = 'config/keybinds.json'

    @staticmethod
    def load_config():
        """Load keybinds from file or use defaults."""
        if os.path.exists(InputConfig.config_path):
            try:
                with open(InputConfig.config_path, 'r') as f:
                    saved_binds = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    for action, key in saved_binds.items():
                        # Determine if we should allow adding new keys not in default? probably yes for forward compat, 
                        # but usually we only want valid actions.
                        if action in InputConfig.DEFAULT_KEYBINDS:
                            InputConfig.keybinds[action] = key
                    print("Keybinds loaded.")
            except Exception as e:
                print(f"Error loading keybinds: {e}")
                InputConfig.keybinds = InputConfig.DEFAULT_KEYBINDS.copy()
        else:
            print("No keybinds found, using defaults.")

    @staticmethod
    def save_config():
        """Save current keybinds to file."""
        try:
            os.makedirs('config', exist_ok=True)
            with open(InputConfig.config_path, 'w') as f:
                json.dump(InputConfig.keybinds, f, indent=4)
            print("Keybinds saved.")
        except Exception as e:
            print(f"Error saving keybinds: {e}")

    @staticmethod
    def get_key(action):
        """Get key code for action."""
        return InputConfig.keybinds.get(action, InputConfig.DEFAULT_KEYBINDS.get(action))

    @staticmethod
    def get_key_name(action):
        """Get readable name of key for action."""
        key_code = InputConfig.get_key(action)
        if key_code is None: return "None"
        return pygame.key.name(key_code).upper()

    @staticmethod
    def set_key(action, key_code):
        """Set new key for action."""
        InputConfig.keybinds[action] = key_code
        InputConfig.save_config()
        
    @staticmethod
    def reset_to_defaults():
        InputConfig.keybinds = InputConfig.DEFAULT_KEYBINDS.copy()
        InputConfig.save_config()
