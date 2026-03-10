# Phase 5: Polish

**Duration**: 1 hour  
**Goal**: Final visual polish, debug mode, and sound effects

## Tasks

### 5.1 Pixel Art Sprites
- [ ] Evaluate sprite options:
  - Option A: Code-drawn shapes (already done in Phase 2)
  - Option B: Download free 8-bit packs from OpenGameArt
  - Option C: Simple Pygame primitives with detail
- [ ] Replace placeholder rectangles with actual sprites if desired
- [ ] Ensure all sprites fit 320x240 and scale properly

### 5.2 Visual Feedback for Actions
- [ ] Track world changes from LLM responses:
  - "smash window" → add "window_broken" to world_changes
  - "kill [person]" → add "[person]_dead" to world_changes
  - Parse LLM response for action keywords
- [ ] Draw these changes in renderer:
  - Broken window: show cracks, different color
  - Blood: red splatter sprite
  - Items: show broken items, moved objects
- [ ] Changes persist within loop, clear on reset

### 5.3 Debug Mode
- [ ] If `config.DEBUG_MODE = True`:
  - Print all prompts to console
  - Print all LLM responses to console
  - Show timing (how long LLM took)
  - Show which LLM was used (Ollama/Groq)
- [ ] Add debug key (F1 or ~) to toggle in-game debug overlay

### 5.4 Ambient Sound (Optional)
- [ ] Add `assets/sounds/` directory
- [ ] Find or generate simple ambient sounds:
  - Bus engine hum (looping)
  - Thunder/lightning (for failure)
  - Optional: small UI sounds
- [ ] Use `pygame.mixer` for playback
- [ ] Toggle via config `ENABLE_SOUND`

### 5.5 UI Polish
- [ ] Add typing animation (characters appear one by one)
- [ ] Add scroll for long responses
- [ ] Visual indicator when LLM is "thinking" (loading spinner or text)
- [ ] Make text box font more readable

### 5.6 Final Testing
- [ ] Test all three endings are reachable
- [ ] Test loop reset visual effect
- [ ] Test LLM failover
- [ ] Test action consistency (same action twice)

## Expected Output
- Game feels complete and polished
- Debug mode helpful for development
- Visual feedback for player actions
- Sound adds atmosphere (if enabled)

## Questions
- Which sprite option do you want to try first?
- Should we add more sound effects or keep it simple?
