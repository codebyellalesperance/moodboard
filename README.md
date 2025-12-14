# Moodboard

**Turn inspo into a shopping cart.**

Upload inspiration images, get shoppable products that match the vibe.

## What It Does

1. Upload 1-5 images (Pinterest screenshots, outfit photos, movie stills)
2. Optionally add a prompt ("casual summer affordable")
3. AI extracts the aesthetic mood from your images
4. Get curated products that capture the same feeling

Unlike visual search that finds exact items, Moodboard understands aesthetic *energy*.

## Quick Start

### 1. Clone and setup
```bash
git clone https://github.com/codebyellalesperance/moodboard.git
cd moodboard
cp .env.example .env
```

### 2. Add your API keys to `.env`
```
OPENAI_API_KEY=sk-your-key
SHOPSTYLE_PID=uid-your-pid
```

### 3. Start backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### 4. Start frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```

### 5. Open http://localhost:5173

## Tech Stack

- **Frontend:** React + Vite + Tailwind CSS
- **Backend:** Flask + Python
- **AI:** OpenAI GPT-4V
- **Products:** ShopStyle Collective API

## Project Structure

```
moodboard/
├── .env              # Your API keys (create from .env.example)
├── frontend/         # React app
└── backend/          # Flask API
```

## API Keys

- **OpenAI:** Get from [platform.openai.com](https://platform.openai.com)
- **ShopStyle:** Apply at [shopstylecollective.com](https://www.shopstylecollective.com)

## License

MIT
