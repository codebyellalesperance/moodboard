# Moodboard Deployment Guide

## Prerequisites

Before deploying, ensure you have:

- [ ] GitHub account with repo pushed (codebyellalesperance/moodboard)
- [ ] OpenAI API key (from platform.openai.com)
- [ ] ShopStyle Collective PID (from shopstylecollective.com)
- [ ] Render account (render.com) - free tier works
- [ ] Vercel account (vercel.com) - free tier works

---

## Part 1: Backend Deployment (Render)

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended for easy repo access)

### Step 2: Create Web Service
1. Click **New** → **Web Service**
2. Connect your GitHub account if not already connected
3. Select the `moodboard` repository

### Step 3: Configure Service
| Setting | Value |
|---------|-------|
| Name | `moodboard-api` (or `moodboard-api-dev` for dev) |
| Region | Oregon (US West) or closest to you |
| Branch | `main` |
| Root Directory | `backend` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app --workers 2 --timeout 120` |

### Step 4: Set Environment Variables
Click **Environment** and add:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | `sk-your-actual-openai-key` |
| `SHOPSTYLE_PID` | `uid1234-your-actual-shopstyle-pid` |
| `FLASK_ENV` | `production` |

> Note: `PORT` is automatically set by Render

### Step 5: Deploy
1. Click **Create Web Service**
2. Wait for build to complete (2-5 minutes)
3. Note your URL: `https://moodboard-api.onrender.com`

### Step 6: Verify Backend
```bash
# Test health endpoint
curl https://moodboard-api.onrender.com/health

# Expected response:
# {"service":"moodboard-api","status":"healthy"}
```

---

## Part 2: Frontend Deployment (Vercel)

### Step 1: Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub

### Step 2: Import Project
1. Click **Add New** → **Project**
2. Select the `moodboard` repository
3. Click **Import**

### Step 3: Configure Project
| Setting | Value |
|---------|-------|
| Framework Preset | Vite |
| Root Directory | `frontend` |
| Build Command | `npm run build` |
| Output Directory | `dist` |

### Step 4: Set Environment Variables
Add the following environment variable:

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://moodboard-api.onrender.com` |

> Replace with your actual Render backend URL

### Step 5: Deploy
1. Click **Deploy**
2. Wait for build to complete (1-2 minutes)
3. Note your URL: `https://moodboard-xyz.vercel.app`

---

## Part 3: Post-Deployment Verification

### Backend Checks
- [ ] Health endpoint returns 200: `curl https://your-backend.onrender.com/health`
- [ ] Check Render logs for startup message
- [ ] No errors in Render dashboard

### Frontend Checks
- [ ] Site loads at Vercel URL
- [ ] No console errors (F12 → Console)
- [ ] Theme toggle works

### Full E2E Test
- [ ] Upload 1 image
- [ ] Click "Shop This Mood"
- [ ] Loading overlay appears
- [ ] Results display (mood name, colors, products)
- [ ] Click a product → opens affiliate link
- [ ] "Start Over" returns to upload screen

---

## Environment-Specific Setup

### Development Environment
If you want a separate dev environment:

**Backend (Render):**
- Create second web service named `moodboard-api-dev`
- Use same settings but can use test API keys
- URL: `https://moodboard-api-dev.onrender.com`

**Frontend (Vercel):**
- Create Preview deployments (automatic on PRs)
- Or create separate project named `moodboard-dev`
- Set `VITE_API_URL` to dev backend URL

### Production Environment
- Use production API keys with higher rate limits
- Consider upgrading Render plan for always-on (free tier sleeps after 15min inactivity)
- Set up custom domain if desired

---

## Custom Domain Setup (Optional)

### Backend (Render)
1. Go to your service → **Settings** → **Custom Domains**
2. Add domain: `api.yourdomain.com`
3. Add DNS records as instructed

### Frontend (Vercel)
1. Go to your project → **Settings** → **Domains**
2. Add domain: `yourdomain.com`
3. Add DNS records as instructed

---

## Monitoring Setup

### UptimeRobot (Free)
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Create free account
3. Add new monitor:
   - Type: HTTP(s)
   - URL: `https://your-backend.onrender.com/health`
   - Interval: 5 minutes
4. Set up email alerts

### Cost Monitoring
- **OpenAI**: Check usage at [platform.openai.com/usage](https://platform.openai.com/usage)
- **Render**: Free tier includes 750 hours/month
- **Vercel**: Free tier includes 100GB bandwidth/month

---

## Troubleshooting

### Backend won't start
1. Check Render logs for errors
2. Verify all environment variables are set
3. Ensure `requirements.txt` has all dependencies

### Frontend can't connect to backend
1. Check `VITE_API_URL` is correct (no trailing slash)
2. Check browser console for CORS errors
3. Verify backend is running (health check)

### API returns 500 errors
1. Check Render logs for Python errors
2. Verify `OPENAI_API_KEY` is valid
3. Verify `SHOPSTYLE_PID` is valid

### Slow responses (>15 seconds)
1. Free Render tier sleeps after 15min - first request wakes it up
2. Consider upgrading to paid plan for always-on
3. OpenAI API can take 5-10 seconds for image analysis

### Rate limit errors (429)
1. Backend limits: 10 requests/minute per IP
2. Wait 1 minute and retry
3. For production, adjust limits in `app.py`

---

## Quick Reference

### URLs
| Environment | Backend | Frontend |
|-------------|---------|----------|
| Local | http://localhost:5001 | http://localhost:5173 |
| Dev | https://moodboard-api-dev.onrender.com | https://moodboard-dev.vercel.app |
| Prod | https://moodboard-api.onrender.com | https://moodboard.vercel.app |

### Environment Variables
```bash
# Backend (.env)
OPENAI_API_KEY=sk-...
SHOPSTYLE_PID=uid...
FLASK_ENV=production

# Frontend (.env)
VITE_API_URL=https://moodboard-api.onrender.com
```

### Useful Commands
```bash
# Check backend health
curl https://your-backend.onrender.com/health

# Test moodcheck endpoint
curl -X POST https://your-backend.onrender.com/api/moodcheck \
  -H "Content-Type: application/json" \
  -d '{"images": ["data:image/png;base64,..."], "prompt": "test"}'

# View Render logs
# Go to Render dashboard → Your service → Logs

# Redeploy
# Push to main branch - auto-deploys on both Render and Vercel
```

---

## Checklist Summary

### Before Deployment
- [ ] OpenAI API key ready
- [ ] ShopStyle PID ready
- [ ] Code pushed to GitHub

### Backend Deployment
- [ ] Render account created
- [ ] Web service created with correct settings
- [ ] Environment variables set
- [ ] Health check passes

### Frontend Deployment
- [ ] Vercel account created
- [ ] Project imported with correct settings
- [ ] `VITE_API_URL` set to backend URL
- [ ] Site loads correctly

### Final Verification
- [ ] Full E2E flow works (upload → results → product click)
- [ ] No console errors
- [ ] Monitoring set up (optional)
