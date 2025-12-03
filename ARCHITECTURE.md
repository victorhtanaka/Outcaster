# 🏗️ Arquitetura do Sistema - Outcaster

## 📊 Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                         GAME LOOP                           │
│  ┌───────────┐  ┌──────────┐  ┌────────────┐  ┌─────────┐ │
│  │  Events   │→ │  Update  │→ │   Render   │→ │  Clock  │ │
│  └───────────┘  └──────────┘  └────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    STATE MANAGER                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   Menu   │  │ Playing  │  │  Paused  │  │   Death  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
         ↓                  ↓                  ↓
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   CORE SYSTEMS   │  │     ENTITIES     │  │   UI SYSTEMS     │
│ ┌──────────────┐ │  │ ┌──────────────┐ │  │ ┌──────────────┐ │
│ │   Resource   │ │  │ │    Player    │ │  │ │     HUD      │ │
│ │   Manager    │ │  │ │    Enemy     │ │  │ │    Menus     │ │
│ │   (Cache)    │ │  │ │     NPC      │ │  │ │  Inventory   │ │
│ └──────────────┘ │  │ └──────────────┘ │  │ └──────────────┘ │
│ ┌──────────────┐ │  │       ↓          │  └──────────────────┘
│ │  Event Bus   │ │  │  ┌──────────┐   │
│ │  (Pub/Sub)   │ │  │  │Components│   │
│ └──────────────┘ │  │  └──────────┘   │
└──────────────────┘  └──────────────────┘
         ↓                     ↓
┌──────────────────────────────────────────────────┐
│              GAME SYSTEMS                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Camera  │  │Collision │  │  Combat  │      │
│  │ (Culling)│  │  (Hash)  │  │ (Damage) │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└──────────────────────────────────────────────────┘
```

## 🔄 Fluxo de Dados

### 1. Inicialização

```
Start Game
    ↓
Initialize Pygame
    ↓
Create ResourceManager (Singleton)
    ↓
Create EventBus (Singleton)
    ↓
Setup GameStateManager
    ↓
Load Initial State (Menu)
    ↓
Enter Game Loop
```

### 2. Game Loop

```
┌─→ Handle Events
│       ↓
│   Update Current State
│       ↓
│   Update Systems
│   ├─→ Camera System
│   ├─→ Collision System  
│   ├─→ Combat System
│   └─→ AI System
│       ↓
│   Update Entities
│   └─→ Update Components
│       ↓
│   Render
│   ├─→ Camera (Culling)
│   ├─→ Sprites (Y-sorted)
│   └─→ UI Components
│       ↓
│   Clock Tick (FPS)
└───────┘
```

### 3. Event Flow

```
Game Event Occurs
    ↓
EventBus.publish(event_type, **data)
    ↓
EventBus finds subscribers
    ↓
Call each subscriber with data
    ↓
Subscribers react
    ├─→ Update UI
    ├─→ Update Stats
    ├─→ Play Sound
    └─→ Trigger Effects
```

### 4. Resource Loading

```
Request Resource
    ↓
Check Cache
    ├─→ Found? Return cached
    │
    └─→ Not Found?
        ↓
    Load from disk
        ↓
    Process (convert_alpha, etc)
        ↓
    Store in cache
        ↓
    Return resource
```

### 5. Entity Update

```
Entity.update()
    ↓
Update each component:
    ├─→ TransformComponent (movement)
    ├─→ HealthComponent (invulnerability)
    ├─→ SpriteComponent (animation)
    ├─→ AIComponent (behavior)
    └─→ CollisionComponent (hitbox)
        ↓
Render entity
```

## 🎯 Component System

```
┌──────────────────────────────────────────────────┐
│                    ENTITY                        │
│  ┌────────────────────────────────────────────┐ │
│  │         Component Dictionary                │ │
│  │  {                                          │ │
│  │    HealthComponent: instance,              │ │
│  │    TransformComponent: instance,           │ │
│  │    SpriteComponent: instance,              │ │
│  │    ...                                      │ │
│  │  }                                          │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  Methods:                                        │
│  ├─ add_component(component)                    │
│  ├─ get_component(ComponentType)                │
│  ├─ has_component(ComponentType)                │
│  └─ update_components(dt)                       │
└──────────────────────────────────────────────────┘
                      ↓
    ┌─────────────────┼─────────────────┐
    ↓                 ↓                 ↓
┌─────────┐    ┌──────────┐    ┌──────────┐
│ Health  │    │Transform │    │  Sprite  │
│Component│    │Component │    │Component │
└─────────┘    └──────────┘    └──────────┘
```

## 🔌 System Integration

### Camera System

```
┌────────────────────────────────────────┐
│         YSortCameraGroup               │
│  ┌──────────────────────────────────┐ │
│  │         Camera                   │ │
│  │  - offset (x, y)                 │ │
│  │  - is_visible(rect) → bool       │ │
│  └──────────────────────────────────┘ │
│                                        │
│  custom_draw(player):                 │
│    1. Center camera on player         │
│    2. Get visible sprites (culling)   │
│    3. Sort by Y position              │
│    4. Draw in order                   │
└────────────────────────────────────────┘
```

### Collision System

```
┌────────────────────────────────────────┐
│       CollisionSystem                  │
│  ┌──────────────────────────────────┐ │
│  │     Spatial Hash                 │ │
│  │  Grid[cell] = [sprites]          │ │
│  │                                  │ │
│  │  query(rect) → nearby sprites    │ │
│  │  (O(1) complexity)               │ │
│  └──────────────────────────────────┘ │
│                                        │
│  check_collision(entity, obstacles):  │
│    1. Get nearby from hash            │
│    2. Check only nearby               │
│    3. Return collision                │
└────────────────────────────────────────┘
```

### Combat System

```
┌────────────────────────────────────────┐
│         CombatSystem                   │
│                                        │
│  create_attack():                     │
│    1. Create attack sprite            │
│    2. Set damage, type, owner         │
│    3. Add to attack group             │
│                                        │
│  process_attacks(targets):            │
│    1. Check collisions                │
│    2. Apply damage                    │
│    3. Publish events                  │
│    4. Remove expired attacks          │
└────────────────────────────────────────┘
```

## 🎨 UI Architecture

```
┌────────────────────────────────────────┐
│          UIComponent (ABC)             │
│  - rect                                │
│  - visible, enabled                    │
│  - render(surface)                     │
│  - handle_event(event)                 │
│  - update(dt)                          │
└────────────────────────────────────────┘
              ↓
    ┌─────────┼─────────┬─────────┬──────────┐
    ↓         ↓         ↓         ↓          ↓
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│Panel │  │ Bar  │  │ Text │  │Button│  │Image │
└──────┘  └──────┘  └──────┘  └──────┘  └──────┘
```

## 📦 Dependency Graph

```
main.py
  ↓
├─→ config/
│   ├─→ settings
│   ├─→ game_data
│   └─→ paths
│
├─→ src/core/
│   ├─→ resource_manager (no deps)
│   ├─→ event_bus (no deps)
│   └─→ game_state (no deps)
│
├─→ src/entities/
│   ├─→ components → entity
│   └─→ entity → core
│
├─→ src/systems/
│   ├─→ camera → entity
│   ├─→ collision → camera
│   └─→ combat → core, entity
│
└─→ src/ui/
    └─→ components → core
```

## 🔄 State Machine

```
┌─────────────────────────────────────────┐
│         GameStateManager                │
│                                         │
│  States Stack:                          │
│  [CurrentState] ← [PreviousState]      │
│                                         │
│  Operations:                            │
│  ├─ change_state()  - Switch           │
│  ├─ push_state()    - Stack            │
│  └─ pop_state()     - Return           │
└─────────────────────────────────────────┘
                ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
┌─────────┐ ┌────────┐ ┌─────────┐
│  Menu   │ │Playing │ │ Paused  │
│  State  │ │ State  │ │  State  │
└─────────┘ └────────┘ └─────────┘
```

## 🎯 Performance Optimizations

### 1. Resource Caching

```
Request → Check Cache → Hit? Return : Load → Cache → Return
          ↓
       O(1) lookup
       No disk I/O
       Instant access
```

### 2. Spatial Hashing

```
World divided into grid cells
Sprite position → Cell coordinates
Check collision only in same/adjacent cells

Before: O(n²) - check all pairs
After:  O(1) - check only nearby
```

### 3. View Culling

```
Camera view bounds
  ↓
Check if sprite.rect in bounds
  ↓
Render: Only visible sprites
  ↓
Performance: 1000+ sprites @ 60 FPS
```

### 4. Component Updates

```
Entity.update_components():
  for component in active_components:
    component.update()

Only update what changes
Skip inactive/disabled components
Minimal processing per frame
```

## 📊 Memory Layout

```
┌──────────────────────────────────────┐
│      Resource Manager (Singleton)    │
│  ┌────────────────────────────────┐ │
│  │  Images Cache                  │ │ ← Shared
│  │  {path: Surface}               │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │  Sounds Cache                  │ │ ← Shared
│  │  {path: Sound}                 │ │
│  └────────────────────────────────┘ │
└──────────────────────────────────────┘
              ↓
   All entities reference same cached resources
              ↓
   Memory efficient: 1 copy for all
```

## 🎮 Game Flow Example

```
User presses SPACE (attack)
    ↓
Input Handler captures
    ↓
Player.attack() called
    ↓
CombatSystem.create_attack()
    ↓
Attack sprite created
    ↓
Next frame: process_attacks()
    ↓
Check collision with enemies
    ↓
Hit detected!
    ↓
EventBus.publish(ENEMY_DAMAGED)
    ↓
Multiple listeners react:
    ├─→ Enemy: health -= damage
    ├─→ UI: update health bar
    ├─→ Audio: play hit sound
    └─→ Particles: spawn effect
```

---

**Esta arquitetura garante:**
- ✅ Baixo acoplamento
- ✅ Alta coesão
- ✅ Fácil manutenção
- ✅ Performance otimizada
- ✅ Escalabilidade
