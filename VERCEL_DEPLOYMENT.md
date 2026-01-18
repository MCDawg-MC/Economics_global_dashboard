# Deploying to Vercel - Step by Step Guide

## Problem: 404 Error on Vercel

The 404 error occurs because:
1. Vercel doesn't know the app is in the `frontend/` subdirectory
2. React Router needs proper configuration for client-side routing
3. Environment variables aren't set

## Solution: Follow These Steps

### Option 1: Deploy Only Frontend (Recommended for Quick Deploy)

#### Step 1: Configure Vercel Project Settings

When importing from GitHub:

1. **Framework Preset**: Select "Create React App"
2. **Root Directory**: Click "Edit" and set to `frontend`
3. **Build Command**: `npm run build` (default is fine)
4. **Output Directory**: `build` (default is fine)
5. **Install Command**: `npm install` (default is fine)

#### Step 2: Add Environment Variables

In Vercel dashboard → Project Settings → Environment Variables:

Add these variables:
```
REACT_APP_MAPBOX_TOKEN=your_mapbox_token_here
REACT_APP_API_URL=https://your-backend-url.com/api/v1
```

**Get Mapbox Token:**
1. Go to https://www.mapbox.com/
2. Sign up (free)
3. Go to Account → Tokens
4. Copy your default public token

#### Step 3: Deploy

Click "Deploy" and wait for build to complete.

---

### Option 2: Manual Vercel CLI Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name? country-momentum-index
# - Directory? ./
# - Override settings? No
```

---

### Option 3: Using Root-Level vercel.json (Already Created)

The repository now has a `vercel.json` file that tells Vercel:
- Build command: `cd frontend && npm install && npm run build`
- Output directory: `frontend/build`
- Rewrites: All routes go to index.html (for React Router)

Just deploy from the root, and it should work!

---

## Troubleshooting

### Still Getting 404?

**Check Build Logs:**
1. Go to Vercel Dashboard
2. Click on your deployment
3. Check "Building" logs for errors

**Common Issues:**

1. **Build Failed?**
   - Check if all dependencies are in `package.json`
   - Make sure `react-scripts` is installed

2. **Map Not Showing?**
   - Add `REACT_APP_MAPBOX_TOKEN` environment variable
   - Redeploy after adding env vars

3. **API Errors?**
   - Update `REACT_APP_API_URL` to point to your backend
   - For testing, you can use mock data (no backend needed)

4. **Root Directory Wrong?**
   - In Vercel settings, set Root Directory to `frontend`
   - Or use the vercel.json in the root

---

## Environment Variables Explained

### Required for Frontend:

```bash
# Mapbox API Token (for map display)
REACT_APP_MAPBOX_TOKEN=pk.eyJ1Ijoi...

# Backend API URL (where your FastAPI backend is hosted)
REACT_APP_API_URL=https://your-backend.herokuapp.com/api/v1

# Or for testing without backend (will show errors but UI works)
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### How to Add in Vercel:

1. Go to Vercel Dashboard
2. Select your project
3. Settings → Environment Variables
4. Add each variable
5. Deploy again (or trigger redeploy)

---

## Backend Deployment (Separate)

The backend (FastAPI) should be deployed separately to:
- **Heroku**: https://www.heroku.com/
- **Railway**: https://railway.app/
- **Render**: https://render.com/
- **AWS/GCP/Azure**: For production scale

Then update `REACT_APP_API_URL` to point to your deployed backend.

---

## Quick Fix Checklist

If deployment fails:

- [ ] Root Directory set to `frontend` in Vercel settings?
- [ ] `REACT_APP_MAPBOX_TOKEN` environment variable added?
- [ ] Build logs show successful build?
- [ ] `vercel.json` exists in root directory?
- [ ] All files committed and pushed to GitHub?

---

## Expected Deployment Flow

```
GitHub Push → Vercel Detects Change → Install Dependencies →
Build React App → Deploy to CDN → Live at your-project.vercel.app
```

---

## Test Your Deployment

Once deployed, visit your Vercel URL and check:

1. ✅ Page loads (no 404)
2. ✅ Map appears (may need Mapbox token)
3. ✅ Navigation works (Dashboard, click country)
4. ⚠️ API calls may fail (need backend deployed)

---

## Complete Production Setup

For full production deployment:

1. **Frontend (Vercel)**:
   - Deploy from `frontend/` directory
   - Add Mapbox token
   - Configure custom domain (optional)

2. **Backend (Heroku/Railway)**:
   - Deploy FastAPI app
   - Set up PostgreSQL database
   - Configure environment variables

3. **Database (Managed PostgreSQL)**:
   - AWS RDS, Heroku Postgres, or Supabase
   - Run migrations
   - Seed data

4. **Connect Frontend to Backend**:
   - Update `REACT_APP_API_URL` in Vercel
   - Redeploy frontend

---

## Alternative: Deploy Without Backend

The frontend can work in "demo mode" without the backend:

1. Deploy frontend to Vercel
2. API calls will fail, but you can:
   - Mock the API responses in `src/services/api.js`
   - Use static JSON data
   - Show "Demo Mode" message

---

## Need Help?

- Vercel Docs: https://vercel.com/docs
- GitHub Issues: https://github.com/MCDawg-MC/Economics_global_dashboard/issues
- Check build logs in Vercel dashboard for specific errors
