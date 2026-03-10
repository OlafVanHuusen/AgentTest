# Phase 4: Game Logic

**Duration**: 2 hours  
**Goal**: Implement time progression, loop mechanics, action tracking, and ending detection

## Tasks

### 4.1 Time System
- [ ] Modify `GameState` to track:
  - `current_minute` (starts at 0 or 120 for 2 AM)
  - `actions_this_loop` (count, max 10)
- [ ] Create `game/clock.py`:
  - `advance_minute()`: increments minute + action count
  - `get_formatted_time()`: returns "02:XX" string
- [ ] Each text action advances time by 1 minute

### 4.2 Loop Manager
- [ ] Create `game/loop_manager.py`:
  - Check if `actions_this_loop >= 10`
  - If yes, trigger loop reset
  - Visual effect: screen glitches, flashes, fades
- [ ] Reset function:
  - `current_minute = 0` (or back to 2 AM)
  - `actions_this_loop = 0`
  - `world_changes = {}` (full reset)
  - `loop_count += 1`
  - Keep `ending_triggered` and `game_over` flags

### 4.3 Action Tracker (Consistency)
- [ ] Create `game/action_tracker.py`:
  - Store `action_hash → result` mapping per loop
  - Hash function: simple hash of lowercase action text
  - Same action text within same loop → returns cached result
  - Clears on loop reset
- [ ] This ensures: if player types "kill driver" twice in one loop, same result both times

### 4.4 Ending Detection
- [ ] Modify prompt builder to check for ending triggers in player input:
  - **Ending 1**: Player examines lamp closely → check "look lamp", "examine lamp", "look at lamp"
  - **Ending 2**: Player smashes lamp → check "smash lamp", "break lamp", "destroy lamp"  
  - **Ending 3**: Player asks about death/ending → check "kill myself", "end it", "how to die"
- [ ] LLM should recognize these and return special response
- [ ] Or: parse LLM response for ending keywords
- [ ] On ending detected:
  - Set `ending_triggered = True`
  - Set `game_over = True`
  - Display ending text
  - Show "Press R to restart" or similar

### 4.5 Lightning Effect (LLM Failure)
- [ ] Create visual effect for when both LLMs fail:
  - Screen flashes white
  - "Lightning" crack sound (optional)
  - Instant loop reset
- [ ] Log failure for debugging

### 4.6 Input Handler Integration
- [ ] Update `game/input_handler.py`:
  - Capture text input (Enter to submit)
  - Send to LLM
  - Display response
  - Advance time
  - Check for loop reset or ending

## Expected Output
- Each action advances clock by 1 minute
- After 10 actions, loop resets with visual effect
- Same action twice in one loop = same result
- All three endings are reachable
- LLM failure triggers lightning + reset

## Edge Cases to Handle
- Empty input: ignore or show "Type something..."
- Very long input: truncate or allow (LLM handles)
- Rapid typing: queue actions or ignore until complete
- Non-English input: LLM may or may not handle

## Questions
- Should loop counter be visible to player?
- Exact wording for ending triggers?
