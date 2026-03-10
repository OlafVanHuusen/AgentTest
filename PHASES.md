# Timeloop Bus - Phase Overview

Quick reference for implementation. Each phase is in its own `.md` file.

## Phase Order

| Phase | File | Duration | Description |
|-------|------|----------|-------------|
| 1 | `PHASE1_Foundation.md` | 2h | Project setup, Pygame window, game loop, lore loading |
| 2 | `PHASE2_Visuals.md` | 2h | 8-bit bus interior, NPCs, UI elements |
| 3 | `PHASE3_LLM_Core.md` | 3h | Ollama + Groq integration, prompt builder, failover |
| 4 | `PHASE4_Game_Logic.md` | 2h | Time progression, loop reset, endings, action tracking |
| 5 | `PHASE5_Polish.md` | 1h | Debug mode, visual feedback, sounds, polish |
| 6 | `PHASE6_Web_Export.md` | 1h | Pygbag web export, browser testing |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Web export
pygbag main.py
```

## Key Files

```
├── main.py              # Entry point
├── config.py            # Settings
├── game/                # Game logic
│   ├── state.py
│   ├── renderer.py
│   ├── input_handler.py
│   ├── loop_manager.py
│   └── action_tracker.py
├── llm/                 # LLM integration
│   ├── base.py
│   ├── ollama.py
│   ├── groq.py
│   ├── failover.py
│   └── prompt_builder.py
├── lore/                # Game data (JSON)
│   ├── npcs.json
│   ├── setting.json
│   └── endings.json
└── assets/              # Sprites, sounds, fonts
```

## Dependencies

- pygame>=2.5.0
- requests>=2.31.0
- pillow>=10.0.0
- pygbag (for web export)

## Configuration

Edit `config.py` to change:
- Resolution (320x240 default)
- LLM preferences (Ollama/Groq)
- Debug mode
- Sound settings
