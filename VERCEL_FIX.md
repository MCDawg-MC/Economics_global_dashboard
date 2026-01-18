# VERCEL 404 FIX - EXACT STEPS

## ✅ GitHub is Updated

All code is pushed. The issue is **Vercel Project Settings**.

---

## 🚨 THE PROBLEM

Vercel is trying to deploy from the **root directory**, but your React app is in the **frontend/** subdirectory.

---

## ✅ THE SOLUTION - Do This EXACTLY:

### Step 1: Delete Current Vercel Project

1. Go to Vercel Dashboard: https://vercel.com/dashboard
2. Find your project
3. Click on it
4. Go to **Settings** (top navigation)
5. Scroll to bottom
6. Click **"Delete Project"**
7. Confirm deletion

### Step 2: Re-Import with Correct Settings

1. Go to https://vercel.com/new
2. Click **"Import Git Repository"**
3. Select your GitHub repo: **Economics_global_dashboard**
4. **WAIT!** Don't click Deploy yet!

### Step 3: Configure Project Settings ⚠️ CRITICAL

In the "Configure Project" screen:

```
Framework Preset: Create React App

Root Directory: [Click "Edit"] → Type: frontend
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                 THIS IS THE KEY SETTING!

Build Command: npm run build (leave as default)

Output Directory: build (leave as default)

Install Command: npm install (leave as default)
```

### Step 4: Add Environment Variables

Still on the same screen, click **"Environment Variables"**:

Add this variable:
```
Name: REACT_APP_MAPBOX_TOKEN
Value: [Your Mapbox token from https://mapbox.com]
```

Add this variable (for now):
```
Name: REACT_APP_API_URL
Value: http://localhost:8000/api/v1
```

### Step 5: Deploy

NOW click **"Deploy"**

---

## 🎯 What This Does

Setting **Root Directory to `frontend`** tells Vercel:
- Look in the `frontend/` folder for package.json
- Run npm install there
- Build the React app from there
- Deploy the build output

---

## 📸 Visual Guide

**What you should see in Vercel settings:**

```
┌─────────────────────────────────────────┐
│ Configure Project                        │
├─────────────────────────────────────────┤
│ Framework Preset: Create React App      │
│                                          │
│ Root Directory: frontend  [Edit]        │
│                 ^^^^^^^^                 │
│                 MUST BE SET!             │
│                                          │
│ Build Command: npm run build            │
│ Output Directory: build                 │
│ Install Command: npm install            │
└─────────────────────────────────────────┘
```

---

## 🔍 Alternative: Use Vercel CLI (If Dashboard Doesn't Work)

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd "C:\Users\mitch\Documents\Coding Projects\COLLEGE TRACKER\Economics_global_dashboard\frontend"

# Login
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? [Your account]
# - Link to existing project? No
# - What's your project's name? country-momentum-index
# - In which directory is your code located? ./ (current directory)
# - Want to modify settings? No

# Production deploy
vercel --prod
```

---

## ✅ Expected Result

After deploying with correct settings:

1. ✅ Build succeeds (check logs)
2. ✅ Site loads at your-project.vercel.app
3. ✅ No 404 error
4. ✅ React app displays
5. ⚠️ Map may not show (need Mapbox token)
6. ⚠️ API calls fail (backend not deployed yet)

---

## 🐛 Still Getting 404?

### Check These:

1. **Vercel Build Logs**:
   - Go to deployment
   - Click "Building"
   - Look for errors

2. **Verify Root Directory**:
   - Settings → General
   - Scroll to "Root Directory"
   - Should show: `frontend`

3. **Check Framework**:
   - Settings → General
   - Framework Preset: Create React App

4. **File Structure on Vercel**:
   Build logs should show:
   ```
   Installing dependencies...
   Running "npm install" in frontend...
   ```

---

## 🚀 Quick Test

After deployment, visit:
```
https://your-project.vercel.app/
```

You should see:
- ✅ "Country Momentum Index" header
- ✅ Dashboard layout
- ⚠️ Empty map (without Mapbox token)
- ⚠️ Empty leaderboards (without backend)

---

## 💡 Pro Tip: Deploy from Vercel CLI

The CLI is often more reliable:

```bash
cd frontend
vercel --prod
```

This automatically detects it's a Create React App and configures everything correctly.

---

## 📞 Need More Help?

If still failing:
1. Share the **build logs** from Vercel
2. Share a screenshot of your **Project Settings**
3. Check if `frontend/package.json` exists in your GitHub repo

---

## ✅ GitHub is Ready

Your code is already on GitHub with all fixes:
https://github.com/MCDawg-MC/Economics_global_dashboard

The issue is purely **Vercel configuration**, not the code!
