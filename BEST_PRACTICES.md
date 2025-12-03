# Boas Práticas e Convenções

## 🎨 Estilo de Código

### Naming Conventions

```python
# Classes: PascalCase
class PlayerEntity:
    pass

class ResourceManager:
    pass

# Funções/Métodos: snake_case
def calculate_damage(attacker, defender):
    pass

def load_game_state():
    pass

# Constantes: UPPER_SNAKE_CASE
MAX_HEALTH = 100
ATTACK_COOLDOWN = 600
DEFAULT_SPEED = 5

# Variáveis: snake_case
player_position = (100, 200)
is_alive = True
health_points = 100

# Privados: prefixo _
class Player:
    def __init__(self):
        self._internal_state = {}
        self.__very_private = None
```

### Type Hints

```python
from typing import List, Dict, Optional, Tuple

def create_entity(
    position: Tuple[int, int],
    health: int = 100,
    name: Optional[str] = None
) -> Entity:
    """Create a new entity."""
    pass

def get_nearby_enemies(
    position: Tuple[int, int],
    radius: float
) -> List[Enemy]:
    """Get all enemies within radius."""
    pass
```

### Docstrings

```python
def calculate_damage(attacker: Entity, defender: Entity) -> int:
    """
    Calculate damage from attacker to defender.
    
    Args:
        attacker: Entity attacking
        defender: Entity defending
        
    Returns:
        Final damage amount after calculations
        
    Example:
        >>> damage = calculate_damage(player, enemy)
        >>> print(damage)
        25
    """
    base_damage = attacker.stats.get('attack', 0)
    defense = defender.stats.get('defense', 0)
    return max(0, base_damage - defense)
```

## 🏗️ Padrões Arquiteturais

### 1. Component Pattern

```python
# ✅ BOM: Composição
class Player(Entity):
    def __init__(self):
        super().__init__()
        self.add_component(HealthComponent(self, 100))
        self.add_component(MovementComponent(self, speed=5))
        self.add_component(SpriteComponent(self, "player.png"))

# ❌ RUIM: Herança profunda
class MovableEntity(Entity):
    pass

class CombatEntity(MovableEntity):
    pass

class Player(CombatEntity):
    pass
```

### 2. Dependency Injection

```python
# ✅ BOM: Injeção de dependência
class CombatSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
    
    def deal_damage(self, target, amount):
        target.take_damage(amount)
        self.event_bus.publish(Events.DAMAGE_DEALT, amount=amount)

# ❌ RUIM: Dependência global
class CombatSystem:
    def deal_damage(self, target, amount):
        target.take_damage(amount)
        GLOBAL_EVENT_BUS.publish(...)  # Acoplado!
```

### 3. Factory Pattern

```python
# ✅ BOM: Factory para criação
class EntityFactory:
    @staticmethod
    def create_enemy(enemy_type: str, position: Tuple[int, int]) -> Enemy:
        """Create enemy by type."""
        config = MONSTER_DATA[enemy_type]
        enemy = Enemy(position)
        enemy.add_component(HealthComponent(enemy, config['health']))
        enemy.add_component(AIComponent(enemy, config['ai_type']))
        return enemy

# Uso
enemy = EntityFactory.create_enemy('goblin', (100, 100))

# ❌ RUIM: Criação manual repetida
enemy = Enemy((100, 100))
enemy.health = 50
enemy.speed = 3
enemy.ai_type = 'aggressive'
# ... repetido em vários lugares
```

### 4. Observer Pattern (Event Bus)

```python
# ✅ BOM: Desacoplado via eventos
class HealthSystem:
    def __init__(self):
        event_bus.subscribe(Events.DAMAGE_TAKEN, self.on_damage)
    
    def on_damage(self, entity, amount):
        entity.health -= amount

class UISystem:
    def __init__(self):
        event_bus.subscribe(Events.DAMAGE_TAKEN, self.update_health_bar)
    
    def update_health_bar(self, entity, amount):
        # Atualiza UI independentemente

# ❌ RUIM: Acoplado diretamente
class HealthSystem:
    def take_damage(self, entity, amount):
        entity.health -= amount
        UI_INSTANCE.update_health_bar(entity)  # Acoplado!
```

## 🔧 Otimizações

### 1. Cache e Memoization

```python
from functools import lru_cache

# ✅ BOM: Cache automático
@lru_cache(maxsize=128)
def calculate_path(start: Tuple[int, int], end: Tuple[int, int]) -> List:
    """Calculate path with automatic caching."""
    # Cálculo pesado
    return path

# ✅ BOM: Lazy loading
class AnimationLoader:
    def __init__(self):
        self._animations = {}
    
    def get_animation(self, name: str):
        if name not in self._animations:
            self._animations[name] = self._load_from_disk(name)
        return self._animations[name]
```

### 2. Spatial Partitioning

```python
# ✅ BOM: Spatial hash para colisões
spatial_hash = SpatialHash(cell_size=128)
spatial_hash.rebuild(all_sprites)
nearby = spatial_hash.query(player.rect)  # Apenas próximos!

# ❌ RUIM: Loop completo
for sprite in all_sprites:  # O(n²)
    if sprite.rect.colliderect(player.rect):
        # ...
```

### 3. Object Pooling

```python
# ✅ BOM: Pool de objetos
class ParticlePool:
    def __init__(self, size=100):
        self.pool = [Particle() for _ in range(size)]
        self.active = []
        self.inactive = self.pool.copy()
    
    def get(self):
        if self.inactive:
            particle = self.inactive.pop()
            self.active.append(particle)
            return particle
        return None
    
    def release(self, particle):
        self.active.remove(particle)
        self.inactive.append(particle)

# ❌ RUIM: Criar/destruir constantemente
for _ in range(100):
    particle = Particle()  # Alocação!
    # ... uso
    del particle  # Garbage collection!
```

### 4. Culling

```python
# ✅ BOM: Renderiza apenas visível
def render(self, camera):
    visible = [s for s in sprites if camera.is_visible(s.rect)]
    for sprite in visible:
        sprite.draw()

# ❌ RUIM: Renderiza tudo
def render(self):
    for sprite in sprites:  # Mesmo fora da tela!
        sprite.draw()
```

## 🧪 Testabilidade

### 1. Componentes Testáveis

```python
# ✅ BOM: Testável isoladamente
class HealthComponent:
    def take_damage(self, amount: int) -> bool:
        if self.vulnerable:
            self.current_health -= amount
            return True
        return False

# Teste
def test_health_damage():
    health = HealthComponent(None, max_health=100)
    assert health.take_damage(25) == True
    assert health.current_health == 75

# ❌ RUIM: Acoplado ao Pygame
class Player:
    def take_damage(self, amount):
        pygame.mixer.Sound('damage.wav').play()  # Não testável!
        self.health -= amount
```

### 2. Mocks e Injeção

```python
# ✅ BOM: Aceita mock
class AISystem:
    def __init__(self, pathfinder):
        self.pathfinder = pathfinder
    
    def find_path(self, start, end):
        return self.pathfinder.calculate(start, end)

# Teste com mock
def test_ai():
    mock_pathfinder = MockPathfinder()
    ai = AISystem(mock_pathfinder)
    path = ai.find_path((0, 0), (10, 10))
    assert len(path) > 0
```

## 📦 Organização de Código

### Estrutura de Arquivo

```python
"""
Module description here.

This module handles X, Y, and Z functionality.
"""

# Standard library
import sys
from typing import List, Dict

# Third-party
import pygame

# Local imports
from config import WIDTH, HEIGHT
from src.core import resource_manager

# Constants
MAX_ENTITIES = 1000
DEFAULT_SPEED = 5

# Classes
class MyClass:
    """Class description."""
    
    def __init__(self):
        """Initialize."""
        pass
    
    def public_method(self):
        """Public method."""
        pass
    
    def _private_method(self):
        """Private helper method."""
        pass

# Functions
def helper_function():
    """Helper function."""
    pass

# Main execution
if __name__ == '__main__':
    main()
```

### Imports

```python
# ✅ BOM: Imports organizados
# Standard library
import sys
from pathlib import Path
from typing import List, Optional

# Third-party
import pygame
import numpy as np

# Local - absolute imports
from config import WIDTH, HEIGHT
from src.core import resource_manager
from src.entities import Player, Enemy

# ❌ RUIM: Imports bagunçados
from config import *  # Import *
import pygame, sys, random  # Múltiplos em linha
from .. import something  # Import relativo confuso
```

## 🚀 Performance Tips

### 1. List Comprehension vs Loop

```python
# ✅ Rápido
visible = [s for s in sprites if camera.is_visible(s.rect)]

# ❌ Mais lento
visible = []
for s in sprites:
    if camera.is_visible(s.rect):
        visible.append(s)
```

### 2. Evite Criação Desnecessária

```python
# ✅ BOM: Reutiliza
temp_vector = pygame.math.Vector2()

def update(self):
    temp_vector.x = self.velocity.x
    temp_vector.y = self.velocity.y
    # usa temp_vector

# ❌ RUIM: Cria toda frame
def update(self):
    temp = pygame.math.Vector2(self.velocity.x, self.velocity.y)
```

### 3. Atualize Apenas Necessário

```python
# ✅ BOM: Dirty flag
class Sprite:
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.dirty = True
    
    def render(self):
        if self.dirty:
            self._update_surface()
            self.dirty = False

# ❌ RUIM: Atualiza sempre
class Sprite:
    def render(self):
        self._update_surface()  # Todo frame!
```

## 🎯 Checklist de Qualidade

Antes de commitar código, verifique:

- [ ] Nomes descritivos e consistentes
- [ ] Funções pequenas (< 50 linhas)
- [ ] Type hints em funções públicas
- [ ] Docstrings em classes e funções públicas
- [ ] Sem código duplicado (DRY)
- [ ] Sem números mágicos (use constantes)
- [ ] Imports organizados
- [ ] Componentes testáveis
- [ ] Performance considerada
- [ ] Tratamento de erros

## 📚 Referências

- [PEP 8 - Style Guide](https://pep8.org/)
- [PEP 257 - Docstrings](https://www.python.org/dev/peps/pep-0257/)
- [Clean Code by Robert Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)
