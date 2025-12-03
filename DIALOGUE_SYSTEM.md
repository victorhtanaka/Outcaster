# Sistema de Diálogo com NPCs - Outcaster

## 📋 Visão Geral

Sistema completo de diálogo interativo para NPCs implementado no jogo Outcaster. O sistema permite que o jogador interaja com NPCs através de prompts visuais e navegue por sequências de diálogo.

## ✨ Funcionalidades

### 1. **Detecção de Proximidade**
- O sistema detecta automaticamente quando o jogador está perto de um NPC
- Mostra um prompt visual acima do NPC: "Pressione [G] para falar"
- Distância configurável através de `INTERACTION_DISTANCE` em `settings.py`

### 2. **Sistema de Diálogo**
- Sequências de múltiplas mensagens por NPC
- Nome do NPC exibido no diálogo
- Navegação entre mensagens com tecla ESPAÇO
- Botão visual de "Continuar" na interface
- Overlay semi-transparente para destacar o diálogo

### 3. **Interface Intuitiva**
- Caixa de diálogo estilizada com borda
- Texto com word-wrap automático
- Nome do NPC em destaque (cor dourada)
- Botão de continuar visível na UI

## 🎮 Como Usar

### Para Jogadores:

1. **Aproxime-se de um NPC** (quadrado azul no mapa)
2. **Quando ver o prompt "Pressione [G] para falar"**, pressione a tecla **G**
3. **Leia a mensagem** do NPC
4. **Pressione ESPAÇO** para avançar para a próxima mensagem
5. O diálogo termina automaticamente após a última mensagem

### Para Desenvolvedores:

#### Criar um Novo NPC com Diálogo:

```python
# 1. No Level.__init__ ou _setup_npcs(), registre o diálogo:
self.dialogue_system.register_dialogue(
    'npc_id',  # ID único do NPC
    [
        "Primeira mensagem do NPC",
        "Segunda mensagem...",
        "Terceira mensagem..."
    ],
    "Nome do NPC"  # Nome exibido na UI
)

# 2. Crie o NPC no mapa:
npc = NPC(
    (x, y),  # Posição no mapa
    [self.visible_sprites, self.npc_sprites],  # Grupos de sprites
    self.obstacle_sprites,  # Sprites de obstáculos
    'npc_id'  # Mesmo ID usado no registro do diálogo
)
```

#### Adicionar NPC via Tilemap (CSV):

```python
# No método create_map(), adicione casos para códigos de NPC:
if col == '395':  # Código para Village Elder
    npc = NPC(
        (x, y),
        [self.visible_sprites, self.npc_sprites],
        self.obstacle_sprites,
        'village_elder'
    )
elif col == '396':  # Código para Merchant
    npc = NPC(
        (x, y),
        [self.visible_sprites, self.npc_sprites],
        self.obstacle_sprites,
        'merchant'
    )
```

## 🏗️ Arquitetura do Sistema

### Componentes Principais:

#### 1. **DialogueSystem** (`src/systems/dialogue_system.py`)
Gerencia o estado global dos diálogos:
- `register_dialogue()`: Registra diálogos para NPCs
- `start_dialogue()`: Inicia um diálogo
- `advance_dialogue()`: Avança para próxima mensagem
- `is_active()`: Verifica se há diálogo ativo

#### 2. **DialogueBox** (`src/ui/dialogue_box.py`)
Renderiza a interface do diálogo:
- `draw_dialogue()`: Desenha caixa de diálogo completa
- `draw_interaction_prompt()`: Mostra prompt de interação
- Word-wrap automático para textos longos
- Botão de continuar integrado

#### 3. **NPC** (`src/entities/npc.py`)
Entidade NPC interativa:
- `check_player_proximity()`: Verifica proximidade do jogador
- `dialogues`: Lista de mensagens do NPC
- `npc_id`: Identificador único
- Suporte para animações (idle, talk, etc.)

#### 4. **Player** (`src/entities/player.py`)
Sistema de interação no jogador:
- `nearby_npc`: Referência ao NPC próximo
- `try_interact()`: Tenta iniciar interação
- `talking`: Flag de estado de diálogo
- Callback para sistema de diálogo

## 📁 Estrutura de Arquivos

```
src/
├── systems/
│   └── dialogue_system.py    # Sistema de gerenciamento de diálogos
├── ui/
│   └── dialogue_box.py        # Interface do diálogo
├── entities/
│   ├── npc.py                 # Entidade NPC
│   └── player.py              # Interação do jogador
└── core/
    └── level.py               # Integração no Level
```

## ⚙️ Configurações

Em `config/settings.py`:

```python
INTERACTION_DISTANCE = 600  # Distância para interação com NPCs
```

Em `src/ui/dialogue_box.py`:

```python
BOX_WIDTH = 1400           # Largura da caixa de diálogo
BOX_HEIGHT = 250           # Altura da caixa de diálogo
TEXT_PADDING = 40          # Padding do texto
BUTTON_WIDTH = 200         # Largura do botão continuar
```

## 🎨 Customização

### Personalizar Aparência do Diálogo:

```python
# Em dialogue_box.py, altere as cores:
overlay.fill((0, 0, 0))  # Cor do overlay (R, G, B)
overlay.set_alpha(100)    # Transparência do overlay (0-255)

# Cores do texto:
speaker_surface = self.font_medium.render(speaker, True, 'gold')  # Nome do NPC
text_rect = self.font_small.render(text, True, TEXT_COLOR)       # Texto do diálogo
```

### Personalizar Sprites dos NPCs:

```python
# Criar NPC com sprite customizado:
npc = NPC(
    pos=(x, y),
    groups=[self.visible_sprites, self.npc_sprites],
    obstacle_sprites=self.obstacle_sprites,
    npc_id='custom_npc',
    sprite_path='gameinfo/graphics/npcs/my_npc.png'  # Sprite customizado
)

# Ou usar animações:
npc.import_npc_assets('gameinfo/graphics/npcs/merchant')
```

## 🐛 Troubleshooting

### NPCs não aparecem no mapa:
- Verifique se os NPCs estão sendo criados em `_create_example_npcs()`
- Confirme que estão nos grupos corretos: `visible_sprites` e `npc_sprites`

### Prompt de interação não aparece:
- Verifique `INTERACTION_DISTANCE` em settings.py
- Confirme que `check_npc_proximity()` está sendo chamado no `Level.run()`

### Diálogo não avança:
- Certifique-se de pressionar ESPAÇO (não ENTER)
- Verifique se há `pygame.time.wait(200)` para debounce

### NPCs são obstáculos:
- Remova `obstacle_sprites` dos grupos do NPC se quiser que o jogador passe por eles

## 📝 NPCs de Exemplo

O jogo inclui 2 NPCs de exemplo:

### 1. Ancião da Vila (`village_elder`)
- **Posição**: (2500, 2500)
- **Mensagens**: 4 falas sobre o mundo e perigos

### 2. Mercador (`merchant`)
- **Posição**: (3000, 2500)
- **Mensagens**: 3 falas sobre itens e comércio

## 🚀 Próximos Passos

Sugestões para expandir o sistema:

1. **Escolhas de Diálogo**: Adicionar opções de resposta do jogador
2. **Quests**: Integrar sistema de missões com NPCs
3. **Condições**: Diálogos diferentes baseados em progresso do jogo
4. **Animações**: Adicionar animações de "falando" aos NPCs
5. **Som**: Adicionar efeitos sonoros e vozes
6. **Portraits**: Adicionar retratos dos NPCs na UI
7. **Rich Text**: Suporte para cores e formatação no texto

## 📚 Referências

- **Pygame Documentation**: https://www.pygame.org/docs/
- **Game UI Best Practices**: Feedback visual claro, controles intuitivos
- **Dialogue Systems**: Estado, sequências, navegação

---

**Desenvolvido para Outcaster** 🎮
Sistema modular e extensível para criar experiências narrativas ricas!
