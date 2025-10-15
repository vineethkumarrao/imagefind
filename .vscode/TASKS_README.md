# VS Code Tasks Guide

This project includes VS Code tasks for easy development workflow.

## 🚀 Quick Start Tasks

### Access Tasks
Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) and type "Tasks: Run Task"

---

## 📋 Available Tasks

### 🌐 Server Tasks

#### 1. **Start All Servers** ⭐ RECOMMENDED
Starts both backend and frontend servers simultaneously.
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

#### 2. **Start Backend Server**
Runs the FastAPI backend with:
- ResNet-50 feature extractor (512D embeddings)
- Appwrite integration
- Quantum similarity algorithm
- Lazy-loaded ML model (faster startup)

#### 3. **Start Frontend Server**
Runs the React TypeScript frontend with:
- Vite dev server
- Hot module replacement
- Material-UI components

---

### 📤 Upload Tasks

#### 4. **Upload All Images** ⭐ RECOMMENDED
Uploads all testing images from all categories:
- Healthcare (X-ray images): 24 images
- Satellite images: 30 images
- Surveillance images: 24 images
- Total: ~78 images with 512D embeddings

#### 5. **Upload Healthcare Images**
Uploads only healthcare/X-ray images to `healthcare-images` bucket

#### 6. **Upload Satellite Images**
Uploads only satellite images to `satellite-images` bucket

#### 7. **Upload Surveillance Images**
Uploads only surveillance/survey images to `surveillance-images` bucket

---

### 🔧 Setup Tasks

#### 8. **Setup Appwrite**
Creates Appwrite database, collections, and storage buckets:
- Database: `quantum-images-db`
- Collection: `feature-vectors` (512D support)
- Buckets: `healthcare-images`, `satellite-images`, `surveillance-images`

#### 9. **Update Collection (512D)**
Updates the Appwrite collection schema to support 512D feature vectors

---

## 🎯 Typical Workflow

### First Time Setup:
1. Run: **Setup Appwrite** (creates database structure)
2. Run: **Update Collection (512D)** (enables 512D vectors)
3. Run: **Start All Servers** (starts backend + frontend)
4. Run: **Upload All Images** (populates database)

### Daily Development:
1. Run: **Start All Servers**
2. Open: http://localhost:5173 (frontend)
3. Open: http://localhost:8000/docs (API docs)

### After Code Changes:
Tasks will auto-reload:
- Backend: Uvicorn auto-reloads on file changes
- Frontend: Vite HMR updates instantly

---

## 🐛 Debugging

### Use Debug Configurations
Press `F5` or go to Run & Debug panel:
- **Python: Backend Server** - Debug backend with breakpoints
- **Python: Upload All Images** - Debug upload process
- **Python: Upload Healthcare/Satellite/Surveillance** - Debug specific uploads

---

## 📁 Task Locations

Tasks are organized in panels:
- **Servers Group**: Both server tasks appear in same panel
- **Dedicated Panels**: Each upload task gets its own panel
- **Auto-restart**: Backend and frontend have instance limits (no duplicates)

---

## ⚙️ Configuration Files

- `.vscode/tasks.json` - Task definitions
- `.vscode/launch.json` - Debug configurations
- `.vscode/settings.json` - Python/TypeScript settings

---

## 🔑 Environment Variables

All tasks automatically load from `.env`:
```
APPWRITE_ENDPOINT=https://fra.cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=68eed0ee0033a7ceca80
APPWRITE_API_KEY=standard_fcf13ee4340fc48c1ed2ab7c13b04566e08ef58796b9eabfd2638d4d278bd40c83af8f0ee64440a6dd5acc9850d974d4f7d2547beb0506359d0d04160335c2476e8254bd44289c67c00090451a6929fc0cda1c27010c3214fc6af31bb3c64a2803bda88ff6d19756065b7b8ee633750687f970a026849246447b0cd9630e4ebd
DATABASE_ID=quantum-images-db
COLLECTION_ID=feature-vectors
```

---

## 📊 Expected Output

### Backend Server:
```
✅ Appwrite retrieval system initialized
⚡ Feature extractor will load on first request
🌐 Starting server on 0.0.0.0:8000
```

### Frontend Server:
```
VITE v5.4.20 ready in 767 ms
➜ Local: http://localhost:5173/
```

### Upload All Images:
```
🎉 MASTER UPLOAD COMPLETE!
HEALTHCARE      - ✅  24 | ❌   0
SATELLITE       - ✅  30 | ❌   0
SURVEILLANCE    - ✅  24 | ❌   0
TOTAL           - ✅  78 | ❌   0
```

---

## 🆘 Troubleshooting

### Backend won't start?
- Check Python environment: `python --version` (should be 3.13.7)
- Check dependencies: `pip list | grep -E "(torch|appwrite|fastapi)"`
- Port 8000 in use? Change PORT in `.env`

### Frontend won't start?
- Check Node version: `node --version` (should be v22.18.0)
- Reinstall deps: `cd frontend && npm install`
- Port 5173 in use? It will auto-select another port

### Upload fails?
- Check Appwrite connection: `python setup_appwrite.py`
- Verify images exist: `ls testingimages/xray/`
- Check API key in `.env`

---

## 📝 Notes

- **Model Loading**: Backend uses lazy loading - ResNet-50 loads on first image upload (takes ~10s)
- **Rate Limiting**: Uploads have 0.3s delay between images to avoid Appwrite rate limits
- **Feature Vectors**: All images use 512D ResNet-50 embeddings (consistent for search)
- **Quantum Algorithm**: AE-QIP mode "inspired" for fast similarity computation

---

## 🔗 Useful URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **Appwrite Console**: https://fra.cloud.appwrite.io/console
- **GitHub Copilot**: Available for code assistance

---

Enjoy developing! 🚀
