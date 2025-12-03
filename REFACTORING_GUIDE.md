# Outcaster - Projeto Refatorado

## 📁 Nova Estrutura do Projeto

```
Outcaster/
├── main.py                 # Ponto de entrada refatorado
├── config/                 # Configurações centralizadas
│   ├── __init__.py
│   ├── settings.py        # Constantes e configurações
│   ├── game_data.py       # Dados de armas, inimigos, etc
│   └── paths.py           # Caminhos de recursos
├── src/                   # Código fonte organizado
│   ├── core/              # Sistemas core do jogo
│   │   ├── __init__.py
│   │   ├── resource_manager.py  # Gerenciamento de assets
│   │   ├── event_bus.py         # Sistema de eventos
│   │   └── game_state.py        # Gerenciamento de estados
│   ├── entities/          # Entidades do jogo
│   │   ├── __init__.py
│   │   ├── entity.py            # Classe base de entidade
│   │   ├── components.py        # Componentes reutilizáveis
│   │   ├── player.py            # Jogador
│   │   └── enemy.py             # Inimigos
│   ├── systems/           # Sistemas do jogo
│   │   ├── __init__.py
│   │   ├── camera.py            # Sistema de câmera otimizado
│   │   ├── collision.py         # Sistema de colisão
│   │   └── combat.py            # Sistema de combate
│   ├── ui/                # Interface do usuário
│   │   ├── __init__.py
│   │   ├── components.py        # Componentes UI reutilizáveis
│   │   └── hud.py               # HUD do jogo
│   ├── screens/           # Telas do jogo
│   │   ├── __init__.py
│   │   ├── menu.py              # Menus
│   │   └── game_screen.py       # Tela principal
│   └── utils/             # Utilitários
│       ├── __init__.py
│       └── helpers.py           # Funções auxiliares
├── code/                  # Código original (manter por compatibilidade)
└── gameinfo/              # Assets do jogo
    ├── graphics/
    ├── audio/
    └── map/
```

## 🎯 Melhorias Implementadas

### 1. **Arquitetura Baseada em Componentes**
- Sistema ECS (Entity Component System) simplificado
- Componentes reutilizáveis: Health, Transform, Sprite, AI, Stats
- Maior flexibilidade e manutenibilidade

### 2. **Gerenciamento de Recursos Otimizado**
- `ResourceManager` singleton com cache automático
- Lazy loading de assets
- Redução de I/O e uso de memória

### 3. **Sistema de Estados**
- `GameStateManager` para gerenciar fluxo do jogo
- Estados: Menu, Playing, Paused, Inventory, GameOver
- Transições limpas entre estados

### 4. **Sistema de Eventos**
- `EventBus` para comunicação desacoplada
- Publish-subscribe pattern
- Eventos tipados e documentados

### 5. **UI Componentizada**
- Componentes reutilizáveis: Button, Bar, Panel, Text
- Redução de código duplicado
- Fácil criação de novas interfaces

### 6. **Renderização Otimizada**
- Sistema de câmera com culling
- Apenas sprites visíveis são renderizados
- Spatial hashing para colisões eficientes
- Y-sorting otimizado

### 7. **Configuração Centralizada**
- Separação de settings, game data e paths
- Fácil ajuste de parâmetros
- Paths usando pathlib para compatibilidade

## 🚀 Padrões de Código Aplicados

### Clean Code
- Nomes descritivos e claros
- Funções pequenas e focadas
- Comentários apenas onde necessário
- DRY (Don't Repeat Yourself)

### Design Patterns
- **Singleton**: ResourceManager, EventBus
- **State Pattern**: GameStateManager
- **Observer Pattern**: Event system
- **Component Pattern**: Entity components
- **Factory Pattern**: Resource loading

### SOLID Principles
- **Single Responsibility**: Cada classe tem uma única responsabilidade
- **Open/Closed**: Extensível via componentes
- **Liskov Substitution**: Componentes intercambiáveis
- **Interface Segregation**: Interfaces específicas
- **Dependency Inversion**: Depende de abstrações

## 📊 Melhorias de Performance

1. **Cache de Recursos**: Assets carregados uma vez
2. **Culling**: Apenas sprites visíveis são processados
3. **Spatial Hash**: Colisões O(n) → O(1) em média
4. **Event System**: Desacoplamento reduz dependências
5. **Component System**: Update apenas componentes necessários

## 🔧 Como Usar a Nova Estrutura

### Criando uma Nova Entidade
```python
from src.entities import Entity
from src.entities.components import HealthComponent, SpriteComponent

entity = Entity(groups)
entity.add_component(HealthComponent(entity, max_health=100))
entity.add_component(SpriteComponent(entity, "path/to/sprite.png"))
```

### Usando o Resource Manager
```python
from src.core import resource_manager

# Carregar imagem (com cache automático)
image = resource_manager.load_image("path/to/image.png")

# Carregar som
sound = resource_manager.load_sound("path/to/sound.wav", volume=0.5)

# Carregar animação
frames = resource_manager.load_animation("path/to/animation/folder")
```

### Usando o Event Bus
```python
from src.core import event_bus, Events

# Publicar evento
event_bus.publish(Events.PLAYER_DAMAGED, damage=10, source="enemy")

# Escutar evento
def on_player_damaged(damage, source):
    print(f"Player took {damage} damage from {source}")

event_bus.subscribe(Events.PLAYER_DAMAGED, on_player_damaged)
```

### Criando UI
```python
from src.ui.components import Panel, Bar, Button

# Criar painel
panel = Panel(x=100, y=100, width=300, height=200)

# Criar barra de vida
health_bar = Bar(x=120, y=120, width=200, height=20, fg_color=(255, 0, 0))
health_bar.set_value(current=75, maximum=100)

# Criar botão
button = Button(x=150, y=200, width=100, height=40, 
                text="Click", callback=lambda: print("Clicked!"))
```

## 🎮 Próximos Passos

1. Migrar código existente para nova estrutura
2. Implementar estados de jogo completos
3. Refatorar Player e Enemy com componentes
4. Criar sistema de save/load
5. Adicionar testes unitários
6. Documentar API completa

## 📝 Notas de Migração

- O código original em `code/` foi mantido para referência
- A nova estrutura é retrocompatível
- Migração gradual é recomendada
- Testes após cada migração de módulo

## 🔍 Estrutura de Dados

### Componentes Disponíveis
- `TransformComponent`: Posição e movimento
- `SpriteComponent`: Renderização e animações
- `HealthComponent`: Vida e dano
- `StatsComponent`: Atributos do personagem
- `CollisionComponent`: Detecção de colisão
- `AIComponent`: Comportamento de IA

### Eventos Disponíveis
- `PLAYER_DIED`, `PLAYER_DAMAGED`, `PLAYER_HEALED`
- `ENEMY_DIED`, `COIN_COLLECTED`
- `WEAPON_SWITCHED`, `MAGIC_SWITCHED`
- `INVENTORY_OPENED`, `MENU_OPENED`
- `GAME_PAUSED`, `GAME_RESUMED`

## 💡 Dicas de Desenvolvimento

1. Use type hints para melhor IDE support
2. Documente funções públicas
3. Mantenha componentes pequenos e focados
4. Use eventos para comunicação entre sistemas
5. Aproveite o cache do ResourceManager
6. Teste performance com profiling

## 📚 Referências

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Clean Code by Robert Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)
- [Python Design Patterns](https://refactoring.guru/design-patterns/python)
