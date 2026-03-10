# Timeloop Bus - Implementation Plan

## Project Overview

A text-adventure game with 8-bit pixel art visuals set on a greyhound bus trapped in a timeloop. Players interact via free-form text, an LLM generates live responses to any action. The goal is to uncover the mystery and escape via one of three endings.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Game Engine | Python + Pygame |
| Web Export | Pygbag (WebAssembly) |
| LLM Primary | Ollama (local, via Docker) |
| LLM Backup | Groq API |
| Lore Storage | JSON data files |
| Resolution | 320x240 (classic 8-bit) |
| Controls | Keyboard only |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        MAIN LOOP                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   INPUT     │→ │    GAME     │→ │      RENDERER      │  │
│  │  Handler    │  │    STATE    │  │   (Pygame draw)    │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│         │                │                     │             │
│         ↓                ↓                     ↓             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   LLM INTEGRATION                       ││
│  │  ┌────────────┐    ┌────────────┐    ┌──────────────┐  ││
│  │  │   OLLAMA  │    │    GROQ    │    │   FALLBACK   │  ││
│  │  │  (local)  │    │   (API)    │    │   HANDLER    │  ││
│  │  └────────────┘    └────────────┘    └──────────────┘  ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## Core Game Mechanics

### Time Loop System
- **Clock**: Visible in-game, shows current "minute"
- **Progression**: Each text action advances time by 1 minute
- **Loop Trigger**: After 10 minutes (10 actions), timeloop resets
- **Reset**: Full reset of all passengers, world state; player (human) retains memory

### Action System
- Free-form text input
- LLM interprets action and generates result
- Actions stored for consistency within loop (same action → same result)
- All action types allowed: dialogue, violence, investigation, destruction

### Endings (3 Total)

| Ending | Trigger | Result |
|--------|---------|--------|
| #1 - Coma Wake | Examine driver's lamp closely | Player wakes up from coma |
| #2 - Dark City | Smash the lamp | Bus arrives in dark city, loop breaks |
| #3 - Give Up | Kill yourself (emo boy tells how) | Loop ends, no restart |

## LLM Integration

### System Prompt Structure
```json
{
  "setting": "2 AM greyhound bus, night, silent driver, sleeping passengers",
  "rules": ["any action allowed", "death is temporary", "loop resets everything"],
  "npcs": [...],
  "loop_state": {...},
  "world_changes": [...]
}
```

### Fallback System
1. Try Ollama first
2. If fails, try Groq
3. If both fail: trigger "lightning" effect + instant loop reset

### Consistency System
- Store action hashes → results mapping within each loop
- Same action text produces same result

## File Structure

```
timeloop-bus/
├── main.py                      # Entry point, main game loop
├── config.py                    # Settings (timer, resolution, LLM endpoints)
├── requirements.txt            # Python dependencies
│
├── game/
│   ├── __init__.py
│   ├── state.py                 # GameState class (loop count, minute, actions)
│   ├── renderer.py              # Pygame rendering (bus, NPCs, UI)
│   ├── input_handler.py         # Text input, keyboard controls
│   ├── loop_manager.py         # Timer, reset logic, endings
│   └── action_tracker.py       # Stores action→result for consistency
│
├── lore/
│   ├── npcs.json                # NPC definitions, personalities, secrets
│   ├── setting.json            # Bus description, atmosphere, rules
│   └── endings.json            # Ending triggers and responses
│
├── llm/
│   ├── __init__.py
│   ├── base.py                  # Abstract LLM interface
│   ├── ollama.py               # Ollama client (local)
│   ├── groq.py                 # Groq API client (cloud)
│   ├── failover.py             # Handles fallback between LLMs
│   └── prompt_builder.py       # Constructs system prompts from lore
│
├── assets/
│   ├── sprites/                # Pixel art sprites (placeholder/generated)
│   │   ├── bus_interior.png
│   │   ├── driver.png
│   │   ├── passengers/
│   │   └── ui/
│   └── fonts/                  # 8-bit font for text
│
└── web/
    └── index.html              # Pygbag entry point for web
```

## Game Visuals (8-bit Style)

### Scene Layout (320x240)
```
┌────────────────────────────────────────┐
│  [CLOCK: 02:XX]            [LOOP: #1]  │
├────────────────────────────────────────┤
│                                        │
│     [Window]  [Driver]  [Window]      │
│         ■        ■■■■        ■        │
│                                        │
│  [Pass 1]  [Pass 2]  [Pass 3] [Pass 4] │
│     ■■       ■■       ■■       ■■     │
│                                        │
│              [AISLE]                   │
│            ◄────────►                  │
│                                        │
├────────────────────────────────────────┤
│ > [Text input area...                 ]│
│ [Dialogue/action result appears here]  │
└────────────────────────────────────────┘
```

### Visual Elements
- **Bus Interior**: Top-down or slight angle view
- **Driver**: Silhouette at front, has "lamp" object
- **Passengers**: 4 colored rectangles with simple sprite details
- **Windows**: Can show broken state (pixel changes)
- **Clock**: Top corner, shows in-game time
- **Loop Counter**: Top corner

### Pixel Art Sources (To Test)
1. Code-drawn rectangles/shapes (instant, placeholder)
2. OpenGameArt free packs
3. Generate with Pygame primitives

## Lore Data (JSON Structure)

### npcs.json
```json
{
  "driver": {
    "name": "The Driver",
    "description": "Middle-aged, silent, never takes eyes off road",
    "attributes": ["stoic", "aware", "protective"],
    "secret": "Has a strange lamp, is aware of the loop",
    "location": "front"
  },
  "alex": {
    "name": "Alex",
    "description": "Young gamer, earbuds in, gaming on phone",
    "attributes": ["gruff", "helpful", "distracted"],
    "secret": "Knows about the lamp",
    "location": "seat_1"
  },
  "maria": {
    "name": "Maria",
    "description": "Anxious, keeps checking watch",
    "attributes": ["nervous", "observant", "scared"],
    "secret": "Has seen loops before, remembers fragments",
    "location": "seat_2"
  },
  "emo_boy": {
    "name": "The Kid",
    "description": "Young, quiet, emo aesthetic",
    "attributes": ["silent", "melancholic", "knowing"],
    "secret": "Knows how to end it all",
    "location": "seat_3"
  }
}
```

### setting.json
```json
{
  "title": "Timeloop Bus",
  "time_of_day": "2:00 AM",
  "atmosphere": "Eerie silence, hum of engine, darkness outside",
  "bus_description": "Greyhound bus, about 20 seats,wc in back",
  "rules": [
    "Player can do ANY action",
    "All actions have consequences (until reset)",
    "Passengers reset each loop",
    "Player human memory persists"
  ],
  "lamp_description": "Strange brass lamp driver keeps. Flickers oddly."
}
```

## Dependencies

```
pygame>=2.5.0
requests>=2.31.0
pillow>=10.0.0  # For image handling
```

## Configuration (config.py)

```python
# Resolution
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
SCALE = 3  # Scale up for visibility

# Timing
MINUTES_PER_ACTION = 1
MAX_MINUTES = 10

# LLM Settings
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:7b"
GROQ_API_KEY = None  # Set via env var
PREFERRED_LLM = "ollama"  # or "groq"

# Debug
DEBUG_MODE = True
LOG_PROMPTS = True

# Audio
ENABLE_SOUND = True
```

## Testing Strategy

1. **Unit Tests**: LLM clients, state management
2. **Integration Tests**: Full action → response flow
3. **Playtest**: Manual testing of all three endings
4. **Edge Cases**: LLM failure, empty input, rapid actions

## Future Considerations (Post-MVP)

- More NPCs and lore depth
- Multiple routes to endings
- Achievement system
- Extended sound design
- Mobile touch controls
- Save/load between sessions
