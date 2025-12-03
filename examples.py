"""
Example: How to use the new refactored structure.

This file demonstrates the usage of the new systems.
"""
import pygame
from src.core import resource_manager, event_bus, Events
from src.entities import Entity
from src.entities.components import (
    HealthComponent, SpriteComponent, TransformComponent
)
from src.ui.components import Panel, Bar, Button, Text
from src.systems.camera import YSortCameraGroup
from config import WIDTH, HEIGHT


# ========== Example 1: Resource Manager ==========
def example_resource_manager():
    """Demonstrate resource manager usage."""
    
    # Load image (automatically cached)
    player_image = resource_manager.load_image(
        'gameinfo/graphics/player/down/down_0.png'
    )
    
    # Load the same image again - returns cached version
    player_image_cached = resource_manager.load_image(
        'gameinfo/graphics/player/down/down_0.png'
    )
    
    # Load sound with volume
    attack_sound = resource_manager.load_sound(
        'gameinfo/audio/sword.wav',
        volume=0.3
    )
    
    # Load animation frames
    idle_frames = resource_manager.load_animation(
        'gameinfo/graphics/player/down_idle'
    )
    
    # Check cache status
    cache_info = resource_manager.get_cache_size()
    print(f"Cached items: {cache_info}")


# ========== Example 2: Event System ==========
def example_event_system():
    """Demonstrate event bus usage."""
    
    # Define event handler
    def on_player_damaged(damage, source):
        print(f"Player took {damage} damage from {source}!")
    
    def on_enemy_died(enemy_type, position):
        print(f"{enemy_type} died at {position}")
    
    # Subscribe to events
    event_bus.subscribe(Events.PLAYER_DAMAGED, on_player_damaged)
    event_bus.subscribe(Events.ENEMY_DIED, on_enemy_died)
    
    # Publish events
    event_bus.publish(Events.PLAYER_DAMAGED, damage=10, source="enemy")
    event_bus.publish(Events.ENEMY_DIED, enemy_type="squid", position=(100, 100))
    
    # Unsubscribe
    event_bus.unsubscribe(Events.PLAYER_DAMAGED, on_player_damaged)


# ========== Example 3: Component-Based Entity ==========
def example_entity_components():
    """Demonstrate component-based entity."""
    
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    
    # Create entity
    entity = Entity(all_sprites)
    
    # Add components
    transform = TransformComponent(entity, pos=(100, 100))
    entity.add_component(transform)
    
    health = HealthComponent(entity, max_health=100)
    entity.add_component(health)
    
    sprite = SpriteComponent(entity, 'gameinfo/graphics/player/down/down_0.png')
    entity.add_component(sprite)
    
    # Use components
    health.take_damage(25)
    print(f"Health: {health.current_health}/{health.max_health}")
    
    health.heal(10)
    print(f"Health after heal: {health.current_health}/{health.max_health}")
    
    # Update all components
    entity.update_components(dt=0.016)


# ========== Example 4: UI Components ==========
def example_ui_components(screen):
    """Demonstrate UI components."""
    
    # Create panel
    panel = Panel(
        x=100, y=100,
        width=300, height=200,
        bg_color=(50, 50, 50),
        border_color=(255, 255, 255)
    )
    
    # Create health bar
    health_bar = Bar(
        x=120, y=120,
        width=260, height=20,
        fg_color=(255, 0, 0),
        bg_color=(100, 100, 100)
    )
    health_bar.set_value(current=75, maximum=100)
    
    # Create text
    text = Text(
        x=250, y=160,
        text="Health: 75/100",
        color=(255, 255, 255)
    )
    
    # Create button
    def on_click():
        print("Button clicked!")
    
    button = Button(
        x=150, y=250,
        width=200, height=50,
        text="Click Me!",
        callback=on_click
    )
    
    # Render UI
    panel.render(screen)
    health_bar.render(screen)
    text.render(screen)
    button.render(screen)


# ========== Example 5: Camera System ==========
def example_camera_system():
    """Demonstrate optimized camera system."""
    
    # Create camera group
    camera_group = YSortCameraGroup(
        floor_image_path='gameinfo/graphics/tilemap/ground.png'
    )
    
    # Add sprites to group
    player = Entity(camera_group)
    player.rect = pygame.Rect(400, 300, 64, 64)
    
    # Create many sprites
    for i in range(100):
        sprite = Entity(camera_group)
        sprite.rect = pygame.Rect(i * 100, i * 50, 64, 64)
    
    # Draw only visible sprites (culling applied automatically)
    # camera_group.custom_draw(player)
    
    print(f"Total sprites: {len(camera_group.sprites())}")
    # Only visible sprites are rendered!


# ========== Example 6: Complete Game Loop Pattern ==========
class ExampleGameState:
    """Example of how to structure a game state."""
    
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        
        # Setup systems
        self.camera_group = YSortCameraGroup()
        
        # Create player with components
        self.player = self.create_player()
        
        # Setup UI
        self.health_bar = Bar(
            x=300, y=180,
            width=200, height=20,
            fg_color=(255, 0, 0)
        )
        
        # Subscribe to events
        event_bus.subscribe(Events.PLAYER_DAMAGED, self.on_player_damaged)
    
    def create_player(self):
        """Create player with components."""
        player = Entity(self.camera_group)
        
        # Add components
        player.add_component(TransformComponent(player, pos=(400, 300)))
        player.add_component(HealthComponent(player, max_health=100))
        player.add_component(SpriteComponent(
            player,
            'gameinfo/graphics/player/down/down_0.png'
        ))
        
        return player
    
    def on_player_damaged(self, damage, source):
        """Handle player damage event."""
        health = self.player.get_component(HealthComponent)
        if health:
            self.health_bar.set_value(
                health.current_health,
                health.max_health
            )
    
    def handle_events(self, events):
        """Handle input events."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Simulate damage
                    event_bus.publish(
                        Events.PLAYER_DAMAGED,
                        damage=10,
                        source="test"
                    )
    
    def update(self, dt):
        """Update game state."""
        # Update all sprites
        self.camera_group.update()
        
        # Update player components
        self.player.update_components(dt)
    
    def render(self):
        """Render game state."""
        # Clear screen
        self.screen.fill((113, 221, 238))
        
        # Draw sprites with camera
        self.camera_group.custom_draw(self.player)
        
        # Draw UI
        self.health_bar.render(self.screen)


# ========== Main Example ==========
def run_examples():
    """Run all examples."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    print("=" * 50)
    print("OUTCASTER - Refactored Structure Examples")
    print("=" * 50)
    
    print("\n1. Resource Manager Example:")
    example_resource_manager()
    
    print("\n2. Event System Example:")
    example_event_system()
    
    print("\n3. Component System Example:")
    example_entity_components()
    
    print("\n4. UI Components Example:")
    example_ui_components(screen)
    
    print("\n5. Camera System Example:")
    example_camera_system()
    
    print("\n" + "=" * 50)
    print("Examples completed! Check the code for details.")
    print("=" * 50)


if __name__ == '__main__':
    run_examples()
