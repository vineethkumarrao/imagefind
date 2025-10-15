# 🚀 Quick Reference Card

## 📋 Installation (One-Time Setup)

```powershell
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Setup Appwrite (creates database, collection, buckets)
python setup_appwrite.py

# 3. Install frontend dependencies
cd frontend
npm install
cd ..
```

## ▶️ Running the Application

### Start Backend (Terminal 1)
```powershell
python backend_server.py
```
✅ http://localhost:8000
✅ http://localhost:8000/docs (Swagger API)

### Start Frontend (Terminal 2)
```powershell
cd frontend
npm run dev
```
✅ http://localhost:5173

## 📤 Upload Sample Images

```powershell
# Place images in these directories first:
# - data/professional_images/healthcare/
# - data/professional_images/satellite/
# - data/professional_images/surveillance/

# Then run uploaders:
python healthcare_uploader.py
python satellite_uploader.py
python surveillance_uploader.py
```

## 🔍 Quick Tests

```powershell
# Test backend health
curl http://localhost:8000/api/health

# Get statistics
curl http://localhost:8000/api/stats

# Or use PowerShell
Invoke-RestMethod -Uri http://localhost:8000/api/health
Invoke-RestMethod -Uri http://localhost:8000/api/stats
```

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | React UI |
| Backend API | http://localhost:8000 | FastAPI |
| API Docs | http://localhost:8000/docs | Swagger |
| Appwrite Console | https://fra.cloud.appwrite.io/console | Cloud Dashboard |

## 🔑 Your Credentials

**Endpoint:** https://fra.cloud.appwrite.io/v1
**Project ID:** 68eed0ee0033a7ceca80
**Database:** quantum-images-db
**Collection:** feature-vectors

## 📁 Key Files

| File | Purpose |
|------|---------|
| `.env` | Backend configuration |
| `frontend/.env` | Frontend configuration |
| `backend_server.py` | FastAPI server |
| `setup_appwrite.py` | Appwrite setup |
| `config.py` | Configuration manager |
| `src/cloud/appwrite_retrieval.py` | Appwrite integration |

## 🛠️ Development Commands

```powershell
# Backend
python backend_server.py        # Run server
pip install package_name        # Install package

# Frontend
cd frontend
npm run dev                     # Development server
npm run build                   # Production build
npm run preview                 # Preview build
npm install package_name        # Install package
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | `pip install -r requirements.txt` |
| Cannot find module (frontend) | `cd frontend && npm install` |
| Port already in use | Close other processes |
| Model weights not found | Ensure `consistent_resnet50_8d.pth` exists |
| Appwrite error | Check `.env` credentials |

## 📊 Project Structure

```
image-Quantum/
├── backend_server.py          ← FastAPI server
├── config.py                  ← Configuration
├── setup_appwrite.py          ← Setup script
├── .env                       ← Backend env (configured)
├── src/cloud/                 ← Appwrite integration
├── *_uploader.py              ← Image uploaders (3 files)
├── requirements.txt           ← Python deps
└── frontend/
    ├── src/                   ← React source
    ├── package.json           ← Node deps
    └── .env                   ← Frontend env (configured)
```

## ⚡ Quick Deploy Checklist

- [ ] Run `pip install -r requirements.txt`
- [ ] Run `python setup_appwrite.py`
- [ ] Run `cd frontend && npm install`
- [ ] Start backend: `python backend_server.py`
- [ ] Start frontend: `cd frontend && npm run dev`
- [ ] Open http://localhost:5173
- [ ] Upload test image
- [ ] Verify results

## 💡 Tips

- Model weights file: `consistent_resnet50_8d.pth` (must exist)
- Both servers support hot reload
- Frontend proxies `/api` to backend automatically
- Use Appwrite console to monitor database/storage
- Check `PROJECT_COMPLETE.md` for full documentation

---

**Ready? Start with: `pip install -r requirements.txt`** 🚀
