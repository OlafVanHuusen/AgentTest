# Phase 2: Visuals

**Duration**: 2 hours  
**Goal**: Complete pixel art visuals for bus interior, NPCs, and UI

## Tasks

### 2.1 Bus Interior
- [ ] Draw detailed 8-bit bus interior (top-down view):
  - Aisle running center
  - Seat rows (2 on each side)
  - Windows along sides (4 windows total)
  - Driver cockpit at front
  - Bathroom door at back
- [ ] Use placeholder colored rectangles initially
- [ ] Test scaling (3x) for visibility

### 2.2 NPCs
- [ ] Create 4 passenger sprites:
  - **Driver**: Gray/dark silhouette at front, has lamp nearby
  - **Alex**: Blue, gaming on phone (glowing screen)
  - **Maria**: Purple, anxious, checking watch
  - **Emo Boy**: Black, headphones, slumped
- [ ] NPCs should have distinct colors for identification
- [ ] Add simple idle animations (optional): blinking, slight movement

### 2.3 UI Elements
- [ ] Clock display (top-left): "02:XX"
- [ ] Loop counter (top-right): "LOOP #X"
- [ ] Action counter (top): "Actions: X/10"
- [ ] Text input box (bottom):
  - Dark background
  - Blinking cursor
  - Monospace font
- [ ] Dialogue/result box (above input):
  - Shows LLM response
  - Auto-scroll if long

### 2.4 Visual States
- [ ] Create state system for world changes:
  - Window broken (show cracks/empty)
  - Blood stains (if violence)
  - Items moved/changed
- [ ] These states should be drawable based on `GameState.world_changes`

### 2.5 Font
- [ ] Find or generate 8-bit font
- [ ] Load in `game/renderer.py`
- [ ] Use for all text (clock, dialogue, input)

## Expected Output
- `python main.py` shows full bus interior with all NPCs
- Clock and loop counter visible
- Text input area at bottom works (typing shows on screen)

## Visual Reference
```
┌────────────────────────────────────────┐
│  CLOCK: 02:00          LOOP: #1        │
├────────────────────────────────────────┤
│                                        │
│   ■ ■ ■ ■    [Driver]    ■ ■ ■ ■      │
│  (windows)     ████        (windows)  │
│                                        │
│   ████ ████   ███████   ████ ████     │
│  (seats)      (aisle)    (seats)      │
│                                        │
│   [Alex]  [Maria]  [Emo]   [Empty]    │
│                                        │
│                         [Bathroom]    │
└────────────────────────────────────────┘
```

## Questions
- Should the bus be top-down or side-view?
- Do you want animated sprites or static?
