# Phase 6: Web Export

**Duration**: 1 hour  
**Goal**: Build game for web browser using Pygbag

## Tasks

### 6.1 Pygbag Setup
- [ ] Install Pygbag: `pip install pygbag`
- [ ] Create `web/index.html`:
  ```html
  <!DOCTYPE html>
  <html>
  <head>
      <title>Timeloop Bus</title>
      <style>
          body { background: #111; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
          canvas { image-rendering: pixelated; }
      </style>
  </head>
  <body>
      <script src="https://pygame-web.github.io/pygbag/pygbag.js"></script>
      <script>
          pyag = window.pygameweb
          pyag.init('main.py', { 
              focus: true,
              async: true,
              canvas: document.getElementById('canvas')
          })
      </script>
      <canvas id="canvas" width="960" height="720"></canvas>
  </body>
  </html>
  ```
- [ ] Configure `config.py` for web:
  - Set `SCALE = 3` (320x240 × 3 = 960x720)
  - Disable sound by default (browser requires user interaction)

### 6.2 Web Build
- [ ] Run: `pygbag main.py`
- [ ] This generates `web/build/` with:
  - `index.html` (modified)
  - `main.py` (WASM compiled)
  - Various .data, .wasm files

### 6.3 Testing
- [ ] Test in local browser (requires local server):
  - Python: `python -m http.server 8000`
  - Open: `http://localhost:8000/web/build/`
- [ ] Verify:
  - Game loads in browser
  - Text input works
  - LLM calls work (may need CORS handling)

### 6.4 Web-Specific Considerations
- [ ] **Ollama**: Won't work in browser (requires local server)
  - Option A: Require Groq API for web version
  - Option B: Show message "Local LLM not available in web version"
- [ ] **File access**: No local file system access
  - Embed lore JSON in Python code or load from network
- [   ] **Performance**: May be slower, test on actual device
- [ ] **Touch**: Optional: add touch controls for mobile

### 6.5 Deployment (Optional)
- [ ] Upload `web/build/` folder to:
  - itch.io (Static hosting)
  - GitHub Pages
  - Netlify/Vercel

## Expected Output
- Game playable in modern browsers
- Responsive canvas (scales to fit)
- Web-optimized build

## Troubleshooting
- **CORS errors**: May need proxy for API calls
- **Performance**: Reduce effects if slow
- **Sound**: Browser requires user click first

## Questions
- Do you want to deploy to a specific platform (itch.io, etc.)?
- Should we prioritize web or desktop first?
