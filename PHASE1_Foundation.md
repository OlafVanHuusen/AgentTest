# Phase 1: Foundation

**Duration**: 2 hours  
**Goal**: Set up project structure, Pygame window, basic game loop, and lore loading

## Tasks

### 1.1 Project Setup
- [ ] Create directory structure: `game/`, `llm/`, `lore/`, `assets/sprites/`, `assets/fonts/`
- [ ] Create `requirements.txt` with dependencies:
  ```
  pygame>=2.5.0
  requests>=2.31.0
  pillow>=10.0.0
  ```
- [ ] Create `config.py` with all settings (resolution, timing, LLM configs, debug)

### 1.2 Main Entry Point
- [ ] Create `main.py` with:
  - Pygame initialization
  - Basic game loop (while running)
  - Event handling (quit, key presses)
  - Clock tick (60 FPS)

### 1.3 Game State
- [ ] Create `game/state.py` with `GameState` class:
  ```python
  class GameState:
      loop_count: int = 1
      current_minute: int = 0
      actions_taken: list[str]  # Action history this loop
      world_changes: dict        # Visual changes (broken windows, etc.)
      ending_triggered: bool = False
      game_over: bool = False
  ```

### 1.4 Lore Loading
- [ ] Create `lore/npcs.json` with NPC definitions (driver, alex, maria, emo boy)
- [ ] Create `lore/setting.json` with atmosphere, bus description, rules
- [ ] Create `lore/endings.json` with 3 endings (coma, dark city, give up)
- [ ] Create `game/lore_loader.py` to load JSON files into game state

### 1.5 Basic Renderer (Placeholder)
- [ ] Create `game/renderer.py` with basic `Renderer` class
- [ ] Draw solid color background (bus floor color)
- [ ] Draw placeholder rectangles for bus layout

## Expected Output
- Run `python main.py` → 320x240 window opens
- Window shows basic bus layout (rectangles)
- No interaction yet, just visual

## Questions
- None so far
