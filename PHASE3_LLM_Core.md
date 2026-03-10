# Phase 3: LLM Core

**Duration**: 3 hours  
**Goal**: Implement LLM integration (Ollama, Groq) with fallback handling and prompt building

## Tasks

### 3.1 LLM Base Interface
- [ ] Create `llm/base.py` with abstract `LLMClient` class:
  ```python
  class LLMClient(ABC):
      @abstractmethod
      def generate(self, prompt: str) -> str:
          pass
      
      @abstractmethod
      def is_available(self) -> bool:
          pass
  ```

### 3.2 Ollama Client
- [ ] Create `llm/ollama.py`:
  - Connect to `http://localhost:11434`
  - Use model from config (llama3.2:7b or similar)
  - Implement `generate(prompt)` → returns response string
  - Implement `is_available()` → health check
- [ ] Test Docker/Ollama connection

### 3.3 Groq API Client
- [ ] Create `llm/groq.py`:
  - Use `requests` to call Groq API
  - API key from environment variable `GROQ_API_KEY`
  - Implement `generate(prompt)` → returns response
  - Implement `is_available()` → checks API key + connectivity
- [ ] Handle API errors gracefully

### 3.4 Failover Handler
- [ ] Create `llm/failover.py`:
  - Try Ollama first (if `config.PREFERRED_LLM == "ollama"`)
  - If fails, try Groq
  - If both fail: trigger `lightning_effect()` + instant loop reset
  - Log failures for debugging

### 3.5 Prompt Builder
- [ ] Create `llm/prompt_builder.py`:
  - Load lore from JSON files
  - Build system prompt from `setting.json`
  - Inject current NPC states from game state
  - Inject world changes (broken windows, etc.)
  - Include loop count and minute
- [ ] System prompt should include:
  - Game setting and atmosphere
  - NPC descriptions and secrets
  - Rules (any action allowed, loop resets)
  - Current world state
  - Player's goal

### 3.6 Full Integration
- [ ] Connect input handler to LLM
- [ ] Player types action → sent to LLM
- [ ] Response displayed in dialogue box
- [ ] Response stored in action tracker

### 3.7 Testing
- [ ] Test: "talk to driver"
- [ ] Test: "smash window"
- [ ] Test: "kill driver"
- [ ] Verify responses are atmospheric and follow game rules

## Expected Output
- Type any action → get LLM response
- LLM respects game setting (2AM bus, silent driver)
- LLM allows any action type
- Fallback works if primary LLM is down

## Example Prompt Structure
```
You are the game master for "Timeloop Bus", an 8-bit adventure game.

SETTING: 2 AM. Greyhound bus driving through night.
The player just woke up. The driver is silent.
Other passengers are sleeping or on phones.

ATMOSPHERE: Eerie silence, hum of engine, darkness outside.
Bus has 20 seats, aisle down middle, bathroom in back.

NPCS:
- DRIVER: Middle-aged, silent, never talks. Has strange brass lamp.
- ALEX: Young gamer, earbuds in. Gruff but knows things.
- MARIA: Anxious, checks watch. Has seen loops before.
- THE KID: Quiet, emo. Knows how to end everything.

RULES:
- Player can do ANY action
- Deaths are temporary (loop resets)
- Be descriptive and atmospheric

CURRENT STATE:
- Loop: #1, Minute: 2
- Actions taken: ["woke up", "looked around"]
- World changes: None yet

What happens when the player types an action?
```

## Questions
- Which LLM model specifically for Ollama? (llama3.2:1b, 3b, 7b?)
- Max tokens for responses?
