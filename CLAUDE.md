# CLAUDE.md — Moodboard Project Context

> This file provides context for AI assistants (Claude, Cursor, Copilot) working on this codebase.

---

## Project Overview

**Name:** Moodboard

**One-liner:** Turn inspo into a shopping cart.

**What it does:** Users upload 1-5 inspiration images (Pinterest screenshots, outfit photos, movie stills) plus an optional text prompt. The app uses AI to extract the aesthetic "mood" from the images, then returns shoppable products that match that vibe — not identical items, but pieces that capture the same feeling.

**Key differentiator:** Unlike Google Lens or visual search (which finds the exact item), Moodboard understands aesthetic *energy* and returns products that feel right even if they look nothing like the original image.

---

## Tech Stack

### Frontend (`/frontend`)
- **Framework:** React 19 + Vite 7
- **Styling:** Tailwind CSS v4 (config via `@theme` in CSS)
- **State:** React useState + Context API for theming
- **Icons:** lucide-react

### Backend (`/backend`)
- **Framework:** Flask (Python 3.11+)
- **Vision AI:** OpenAI GPT-4V (gpt-4o)
- **Shopping API:** ShopStyle Collective
- **Deployment:** Render or Railway (Gunicorn)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│                    (React + Tailwind)                        │
│                                                              │
│  Upload Images → Add Prompt → Submit → Display Results       │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              │ POST /api/moodcheck
                              │ { images: [base64...], prompt: string }
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         BACKEND                              │
│                        (Flask)                               │
│                                                              │
│  1. Validate request                                         │
│  2. Send images to GPT-4V → Extract mood profile             │
│  3. Use search queries to call ShopStyle → Get products      │
│  4. Return { vibe, products }                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

```
moodboard/
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── App.jsx             # Main component, state management
│   │   ├── main.jsx            # Entry point
│   │   ├── index.css           # Tailwind v4 + theme variables + animations
│   │   ├── context/
│   │   │   └── ThemeContext.jsx
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── ImageUploader.jsx
│   │   │   ├── PromptInput.jsx
│   │   │   ├── SubmitButton.jsx
│   │   │   ├── MoodSummary.jsx
│   │   │   ├── ProductCard.jsx
│   │   │   ├── ProductGrid.jsx
│   │   │   ├── LoadingOverlay.jsx
│   │   │   ├── ErrorMessage.jsx
│   │   │   ├── ThemeToggle.jsx
│   │   │   └── Clock.jsx
│   │   └── utils/
│   │       └── api.js          # API call helper
│   ├── index.html
│   ├── vite.config.js
│   ├── eslint.config.js
│   └── package.json
│
├── backend/                    # Flask backend
│   ├── app.py                  # Main Flask app
│   ├── config.py               # Environment config
│   ├── requirements.txt
│   ├── Procfile                # Gunicorn for production
│   ├── .env.example
│   ├── services/
│   │   ├── vision.py           # GPT-4V integration
│   │   └── shopping.py         # ShopStyle API
│   ├── utils/
│   │   ├── validation.py       # Request validation
│   │   └── logger.py           # Logging utility
│   └── tests/
│       ├── test_validation.py
│       ├── test_vision.py
│       ├── test_shopping.py
│       └── test_integration.py
│
├── docs/                       # Project documentation
│   ├── BACKEND_PRD.md
│   └── FRONTEND_PRD.md
│
├── CLAUDE.md                   # This file
├── GITHUB_AI_INSTRUCTIONS.md   # Git workflow rules
└── README.md
```

---

## Development Commands

### Frontend
```bash
cd frontend
npm install
npm run dev      # Start dev server (http://localhost:5173)
npm run build    # Production build
npm run lint     # ESLint check
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py    # Start dev server (http://localhost:5001)

# Tests
pytest -v                        # Run all tests
pytest -m "not slow" -v          # Skip API tests
pytest --cov=. --cov-report=html # With coverage
```

---

## Environment Variables

### Frontend (`frontend/.env`)
```
VITE_API_URL=http://localhost:5001
```

### Backend (`backend/.env`)
```
OPENAI_API_KEY=sk-...
SHOPSTYLE_PID=uid1234-...
FLASK_ENV=development
PORT=5001
```

---

## API Schema

### Endpoint: `POST /api/moodcheck`

#### Request
```json
{
  "images": ["data:image/jpeg;base64,..."],
  "prompt": "casual summer affordable"
}
```

**Validation:**
- `images`: Required, 1-5 items, base64 data URIs, JPEG/PNG/WEBP, max 5MB each
- `prompt`: Optional, max 200 characters

#### Response (Success)
```json
{
  "success": true,
  "vibe": {
    "name": "Coastal Grandmother",
    "mood": "Effortless, relaxed, polished",
    "color_palette": [{"name": "Cream", "hex": "#F5F5DC"}],
    "textures": ["linen", "cotton"],
    "key_pieces": ["oversized blazer", "white tee"],
    "avoid": ["loud logos"],
    "search_queries": ["oversized linen blazer women"]
  },
  "products": [{
    "id": "ss_12345",
    "name": "Oversized Linen Blazer",
    "brand": "Vince",
    "price": 89.99,
    "image_url": "https://...",
    "product_url": "https://...",
    "retailer": "Nordstrom"
  }]
}
```

---

## Theme System

Dark (default) and light themes via CSS variables and React Context.

### Usage
```jsx
import { useTheme } from './context/ThemeContext'
const { theme, toggleTheme } = useTheme()
```

### CSS Classes
- `theme-text-primary`, `theme-text-secondary`, `theme-text-tertiary`
- `.glass`, `.glass-hover`, `.glass-card` (glassmorphism)
- `.animate-fade-in`, `.animate-slide-up`, `.animate-scale-in`

---

## Git Workflow

### Branch Naming
`feat/`, `fix/`, `docs/`, `chore/` + short description

### Commit Messages
Format: `<type>: <short present-tense summary>`

- Under 60 characters, no emojis
- Present tense, specific, casual tone
- Example: `feat: add dark mode toggle`

### Rules
- Never commit secrets (.env files)
- Work on branches, not main
- Keep commits small (1 purpose each)
- Pull before push, rebase if needed

---

## Gotchas

### Frontend
- Images convert to base64 before sending
- Theme persists to localStorage (`moodboard-theme`)
- ESLint allows unused vars prefixed with uppercase/underscore

### Backend
- GPT-4V takes 5-15 seconds per request
- ShopStyle `clickUrl` is the affiliate link (not `url`)
- Backend strips markdown code blocks from GPT responses
- Rate limiting: 10 req/min on moodcheck, 100/day default
- Port 5001 locally (macOS uses 5000 for AirPlay)

### CORS
- Backend has `flask-cors` enabled
- Frontend `VITE_API_URL` must match backend URL

---

## Deployment

### Backend (Render)
1. Connect GitHub repo to Render
2. Set environment variables in Render dashboard
3. Deploy from `backend/` directory
4. Uses Gunicorn via Procfile

### Frontend (Vercel/Netlify)
1. Connect GitHub repo
2. Set `VITE_API_URL` to production backend URL
3. Build command: `npm run build`
4. Output directory: `dist`

### Environment Variables (Production)
```
OPENAI_API_KEY=sk-...        # Real OpenAI key
SHOPSTYLE_PID=uid...         # Real ShopStyle PID
FLASK_ENV=production
PORT=10000                   # Render assigns this
```
