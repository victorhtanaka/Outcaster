# 🚀 Quick Reference - Outcaster

## 📚 Importações Comuns

```python
# Core
from src.core import resource_manager, event_bus, Events
from src.core import GameStateManager, GameState

# Entities
from src.entities import Entity
from src.entities.components import (
    HealthComponent, SpriteComponent, TransformComponent,
    StatsComponent, CollisionComponent, AIComponent
)

# Systems
from src.systems import Camera, YSortCameraGroup, SpatialHash
from src.systems.collision import CollisionSystem
from src.systems.combat import CombatSystem

# UI
from src.ui.components import Panel, Bar, Button, Text, Image

# Utils
from src.utils import import_csv_layout, import_folder

# Config
from config import WIDTH, HEIGHT, FPS
from config import WEAPON_DATA, MAGIC_DATA, MONSTER_DATA
from config import UI_FONT, UI_FONT_THIN
```

## 🎯 Snippets Úteis

### Carregar Recursos

```python
# Imagem (com cache automático)
image = resource_manager.load_image("path/to/image.png")

# Som
sound = resource_manager.load_sound("path/to/sound.wav", volume=0.5)

# Fonte
font = resource_manager.load_font("path/to/font.ttf", size=32)

# Animação
frames = resource_manager.load_animation("path/to/folder")
```

### Criar Entidade

```python
# Entidade básica
entity = Entity(sprite_groups)

# Com componentes
entity.add_component(TransformComponent(entity, pos=(100, 100)))
entity.add_component(HealthComponent(entity, max_health=100))
entity.add_component(SpriteComponent(entity, "sprite.png"))

# Usar componente
health = entity.get_component(HealthComponent)
if health:
    health.take_damage(10)
```

### Sistema de Eventos

```python
# Publicar evento
event_bus.publish(Events.PLAYER_DAMAGED, damage=10, source="enemy")

# Escutar evento
def on_damage(damage, source):
    print(f"Took {damage} from {source}")

event_bus.subscribe(Events.PLAYER_DAMAGED, on_damage)

# Remover listener
event_bus.unsubscribe(Events.PLAYER_DAMAGED, on_damage)
```

### UI Components

```python
# Painel
panel = Panel(x=100, y=100, width=300, height=200,
              bg_color=(50, 50, 50), border_color=(255, 255, 255))

# Barra de vida
health_bar = Bar(x=120, y=120, width=200, height=20,
                 fg_color=(255, 0, 0), bg_color=(100, 100, 100))
health_bar.set_value(current=75, maximum=100)

# Texto
text = Text(x=250, y=150, text="Hello World",
            color=(255, 255, 255), center=True)

# Botão
button = Button(x=150, y=200, width=200, height=50,
                text="Click Me", callback=on_click)

# Renderizar
panel.render(screen)
health_bar.render(screen)
text.render(screen)
button.render(screen)
```

### Camera e Renderização

```python
# Criar camera group
camera_group = YSortCameraGroup(
    floor_image_path="path/to/floor.png"
)

# Adicionar sprites
player = Entity(camera_group)
enemy = Entity(camera_group)

# Renderizar (com culling automático)
camera_group.custom_draw(player)

# Atualizar inimigos visíveis
camera_group.enemy_update(player)
```

### Colisões

```python
# Sistema de colisão
collision_system = CollisionSystem()

# Atualizar spatial hash
collision_system.update_spatial_hash(all_sprites)

# Verificar colisão
has_collision = collision_system.check_collision(
    entity, 'horizontal', obstacles
)

# Resolver colisão
collision_system.resolve_collision(
    entity, 'horizontal', obstacles
)

# Obter colisões
colliding = collision_system.get_collisions(
    player.rect, enemy_group
)
```

### Sistema de Combate

```python
# Criar sistema
combat_system = CombatSystem()

# Criar ataque
attack = combat_system.create_attack(
    attacker=player,
    attack_type='sword',
    damage=25,
    position=(100, 100),
    size=(64, 64)
)

# Processar ataques
combat_system.process_attacks(enemy_group)

# Limpar ataques
combat_system.clear_attacks()
```

## 🎮 Game Loop Básico

```python
import pygame
from config import WIDTH, HEIGHT, FPS
from src.core import resource_manager, event_bus

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.setup()
    
    def setup(self):
        """Setup game objects."""
        pass
    
    def handle_events(self):
        """Handle input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self, dt):
        """Update game logic."""
        pass
    
    def render(self):
        """Render game."""
        self.screen.fill((0, 0, 0))
        # Render here
        pygame.display.flip()
    
    def run(self):
        """Main loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
```

## 📋 Eventos Disponíveis

```python
# Player events
Events.PLAYER_DIED
Events.PLAYER_DAMAGED
Events.PLAYER_HEALED

# Enemy events
Events.ENEMY_DIED

# Item events
Events.COIN_COLLECTED

# Weapon/Magic events
Events.WEAPON_SWITCHED
Events.MAGIC_SWITCHED

# UI events
Events.INVENTORY_OPENED
Events.MENU_OPENED

# Game events
Events.GAME_PAUSED
Events.GAME_RESUMED
```

## 🔧 Configurações Importantes

```python
# Display
WIDTH = 1920
HEIGHT = 1080
FPS = 60
TILESIZE = 64

# Cores
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'

# Paths
from config.paths import (
    UI_FONT, UI_FONT_THIN,
    PLAYER_GRAPHICS, MONSTER_GRAPHICS,
    MAP_FLOOR, MAP_ENTITIES
)

# Game Data
from config.game_data import (
    WEAPON_DATA, MAGIC_DATA, MONSTER_DATA
)
```

## 💡 Dicas Rápidas

### Performance
```python
# ✅ Use cache
image = resource_manager.load_image(path)  # Cached!

# ✅ Use culling
camera_group.custom_draw(player)  # Only visible

# ✅ Use spatial hash
collision_system.update_spatial_hash(sprites)
```

### Organização
```python
# ✅ Imports no topo
from config import WIDTH
from src.core import resource_manager

# ✅ Constantes em UPPER_CASE
MAX_HEALTH = 100
DEFAULT_SPEED = 5

# ✅ Type hints
def calculate_damage(attacker: Entity, defender: Entity) -> int:
    pass
```

### Componentes
```python
# ✅ Pequenos e focados
class HealthComponent(Component):
    def update(self, dt: float = 0):
        # Apenas lógica de vida
        pass

# ✅ Composição > Herança
entity.add_component(HealthComponent(entity, 100))
entity.add_component(MovementComponent(entity, 5))
```

## 📖 Documentação Completa

- `README.md` - Visão geral
- `REFACTORING_GUIDE.md` - Guia detalhado
- `MIGRATION.md` - Como migrar
- `BEFORE_AFTER.md` - Comparações
- `BEST_PRACTICES.md` - Padrões
- `SUMMARY.md` - Resumo completo
- `examples.py` - Exemplos práticos

## 🆘 Troubleshooting

### Imagem não carrega
```python
# Verifique o caminho
print(Path("path/to/image.png").exists())

# Use resource manager (trata erros)
image = resource_manager.load_image("path/to/image.png")
```

### Evento não dispara
```python
# Verifique se está subscrito
event_bus.subscribe(Events.PLAYER_DAMAGED, handler)

# Verifique se está publicando corretamente
event_bus.publish(Events.PLAYER_DAMAGED, damage=10, source="test")
```

### Componente não funciona
```python
# Verifique se foi adicionado
health = entity.get_component(HealthComponent)
if health:
    health.take_damage(10)

# Verifique se update é chamado
entity.update_components(dt)
```

### Performance baixa
```python
# Use culling
camera_group.custom_draw(player)

# Use spatial hash
collision_system.update_spatial_hash(sprites)

# Cache recursos
resource_manager.load_image(path)  # Cached!
```

---

**Para mais detalhes, consulte a documentação completa! 📚**
