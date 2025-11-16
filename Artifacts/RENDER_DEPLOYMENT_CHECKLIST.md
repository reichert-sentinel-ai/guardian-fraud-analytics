# Guardian API Render Deployment Checklist

## Current Status
❌ Backend API needs to be deployed on Render

## Steps to Deploy on Render

### 1. Check if Service Exists
- Go to https://dashboard.render.com
- Look for a service named `guardian-api` or similar
- If it doesn't exist, proceed to step 2
- If it exists, check its status (should be "Live")

### 2. Create New Service
1. Click **"New"** → **"Web Service"**
2. Connect GitHub repository: `reichert-sentinel-ai/guardian-fraud-detection` (or your repo name)
3. Render should auto-detect `render.yaml` in the `Artifacts` folder
4. If not auto-detected, configure manually:
   - **Name**: `guardian-api`
   - **Environment**: `Docker`
   - **Root Directory**: `Artifacts` (important!)
   - **Dockerfile Path**: `Dockerfile` (relative to root directory)
   - **Health Check Path**: `/health`
   - **Auto-Deploy**: `Yes`

### 3. Verify Service Configuration
Check these settings in the Render dashboard:

**Settings Tab:**
- ✅ **Root Directory**: `Artifacts`
- ✅ **Environment**: `Docker`
- ✅ **Dockerfile Path**: `Dockerfile`
- ✅ **Health Check Path**: `/health`

**Environment Tab:**
- ✅ **PORT**: `8000` (or Render's auto-assigned port)
- ⚠️ **Database**: Guardian uses PostgreSQL - you may need to add a PostgreSQL database service
- ⚠️ **Redis**: Guardian uses Redis for caching - optional but recommended

### 4. Optional: Add PostgreSQL Database
Guardian uses PostgreSQL. You can:
- Add a PostgreSQL database service on Render
- Or use environment variables to point to an external database
- Or the app will work without DB (some features may be limited)

To add PostgreSQL:
1. Click **"New"** → **"PostgreSQL"**
2. Name it `guardian-db`
3. Copy the connection string
4. Add to Guardian API service environment variables:
   - `DB_HOST`: (from connection string)
   - `DB_PORT`: `5432`
   - `DB_USER`: (from connection string)
   - `DB_PASSWORD`: (from connection string)
   - `DB_NAME`: (from connection string)

### 5. Optional: Add Redis (for caching)
1. Click **"New"** → **"Redis"**
2. Name it `guardian-redis`
3. Add to Guardian API service environment variables:
   - `REDIS_HOST`: (from Redis service)
   - `REDIS_PORT`: `6379`
   - `REDIS_PASSWORD`: (if set)

### 6. Check Deployment Logs
1. Go to **"Logs"** tab
2. Look for:
   - ✅ "Building Docker image..."
   - ✅ "Starting container..."
   - ✅ "Uvicorn running on..."
   - ✅ "✅ API Ready!"
   - ❌ Any error messages

### 7. Test After Deployment
Once deployed, test these URLs:
- ✅ `https://guardian-api.onrender.com/` → Should return API info
- ✅ `https://guardian-api.onrender.com/health` → Should return `{"status": "healthy"}`
- ✅ `https://guardian-api.onrender.com/docs` → API documentation (if debug enabled)

### 8. Verify CORS is Working
After deployment, check browser console on frontend:
- ❌ Should NOT see CORS errors
- ✅ API calls should return 200 status
- ✅ Data should load in the UI

## Quick Deploy Command (if using Render CLI)
```bash
render deploy
```

## Manual Deploy Trigger
1. Go to service dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**
3. Wait 3-5 minutes for build to complete

## Expected Deployment Time
- First deployment: 5-10 minutes
- Subsequent deployments: 3-5 minutes

## After Successful Deployment
The frontend at `https://guardian-fraud-detection.vercel.app` should:
- ✅ Load without CORS errors
- ✅ Display data from the API
- ✅ All endpoints should work

