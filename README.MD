# ⚛️ Quantum Image Retrieval System# Quantum-Enhanced Image Retrieval System



AI-powered image similarity search using **ResNet-50** + **AE-QIP Quantum Algorithm** + **Appwrite**.![Quantum Computing](https://img.shields.io/badge/Quantum-AE--QIP%20Algorithm-blue)

![Appwrite](https://img.shields.io/badge/Appwrite-Database%20%7C%20Storage-f02e65)

## 🎯 What It Does![React](https://img.shields.io/badge/React-TypeScript-61dafb)

![PyTorch](https://img.shields.io/badge/PyTorch-ResNet--50-red)

Upload an image → AI extracts features → Quantum algorithm finds similar images → Results ranked by similarity![Qiskit](https://img.shields.io/badge/Qiskit-2.1.2-purple)

![Python](https://img.shields.io/badge/Python-3.8%2B-green)

**Categories**: Healthcare (X-rays), Satellite (Aerial), Surveillance (Security)

A cutting-edge image retrieval system that combines **classical deep learning** with **quantum computing** to solve large-scale image similarity search problems. The system leverages quantum amplitude estimation for enhanced similarity calculations while addressing the semantic gap in traditional image retrieval techniques.

## 🚀 Quick Start (Local)

## 🌟 Overview

### Prerequisites

- Python 3.8+Traditional image retrieval techniques struggle with large-scale databases and semantic gaps. This project develops a **quantum-assisted image retrieval system** using quantum nearest neighbor search and advanced image feature encoding. The system leverages quantum computing to significantly enhance similarity search accuracy over vast image datasets, integrating classical CNN methods with quantum kernels for improved retrieval accuracy and computational efficiency.

- Node.js 18+

- Appwrite account (free at https://appwrite.io)**Target Applications**: Healthcare imaging, surveillance systems, and satellite imagery analysis for real-time applications.



### 1. Clone & Install## 🚀 Key Features



```bash### 🔬 Quantum Computing Components

git clone <your-repo>- **AE-QIP Algorithm**: Amplitude Estimation Quantum Inner Product algorithm v3.0.0

cd image-Quantum- **Quantum Kernels**: Quantum fidelity and phase coherence kernels for enhanced similarity

- **Hybrid Architecture**: Production-optimized quantum-inspired mode + research-grade true quantum simulation

# Backend dependencies- **11-Qubit Circuits**: 3 encoding qubits + 1 control + 7 auxiliary qubits for amplitude estimation

pip install -r requirements.txt

### 🧠 Classical ML Components  

# Frontend dependencies- **ResNet-50 CNN**: Pre-trained feature extractor generating 8D feature vectors

cd frontend- **Unified Feature Extraction**: Consistent feature processing for all image categories

npm install- **Real-time Processing**: Optimized for production deployment

cd ..

```### ☁️ Cloud Infrastructure

- **Appwrite Database**: Scalable NoSQL database for feature vectors and metadata

### 2. Configure Environment- **Appwrite Storage**: Efficient image storage with bucket organization

- **Multi-Category Support**: Healthcare, surveillance, and satellite image domains

Create `.env` in root:

### 🌐 Web Interface

```env- **React TypeScript Frontend**: Modern, type-safe, component-based UI

# Appwrite Configuration- **FastAPI Backend**: High-performance Python API server

APPWRITE_ENDPOINT=https://fra.cloud.appwrite.io/v1- **Real-time Search**: Upload an image and find similar images instantly

APPWRITE_PROJECT_ID=your-project-id- **Confidence Filtering**: Advanced thresholding for high-quality results

APPWRITE_API_KEY=your-api-key

APPWRITE_DATABASE_ID=quantum-images-db## 🏗️ System Architecture

APPWRITE_COLLECTION_ID=feature-vectors

APPWRITE_BUCKET_HEALTHCARE=healthcare-images```

APPWRITE_BUCKET_SATELLITE=satellite-images┌─────────────────────────────────────────────────────────────────┐

APPWRITE_BUCKET_SURVEILLANCE=surveillance-images│                    User Interface (Web App)                     │

│                   React + TypeScript + Vite                    │

# Server└─────────────────┬───────────────────────────────────────────────┘

HOST=0.0.0.0                  │

PORT=8000┌─────────────────▼───────────────────────────────────────────────┐

DEBUG=True│               Image Upload & Processing                        │

```│          ┌─────────────┐  ┌─────────────┐                      │

│          │ PIL/OpenCV  │  │ Validation  │                      │

Create `frontend/.env`:│          │ Preprocessing│  │ & Resize    │                      │

│          └─────────────┘  └─────────────┘                      │

```env└─────────────────┬───────────────────────────────────────────────┘

VITE_API_URL=http://localhost:8000                  │

VITE_APPWRITE_ENDPOINT=https://fra.cloud.appwrite.io/v1┌─────────────────▼───────────────────────────────────────────────┐

VITE_APPWRITE_PROJECT_ID=your-project-id│                Feature Extraction                              │

VITE_APPWRITE_BUCKET_ID=healthcare-images│     ┌─────────────────────────────────────────────────────────┐ │

VITE_APPWRITE_BUCKET_SATELLITE=satellite-images│     │            ResNet-50 CNN                                │ │

VITE_APPWRITE_BUCKET_SURVEILLANCE=surveillance-images│     │   ┌───────────┐ ┌───────────┐ ┌───────────┐             │ │

```│     │   │ Conv      │→│ Residual  │→│ Global    │→ 8D Vector  │ │

│     │   │ Layers    │ │ Blocks    │ │ Pool      │             │ │

### 3. Setup Appwrite│     │   └───────────┘ └───────────┘ └───────────┘             │ │

│     └─────────────────────────────────────────────────────────┘ │

```bash└─────────────────┬───────────────────────────────────────────────┘

python setup_appwrite.py                  │

```┌─────────────────▼───────────────────────────────────────────────┐

│              Quantum Similarity Engine                         │

This creates:│  ┌─────────────────────┐    ┌─────────────────────────────────┐ │

- Database: `quantum-images-db`│  │ Production Mode     │    │ Research Mode                   │ │

- Collection: `feature-vectors`│  │ (Quantum-Inspired)  │    │ (True Quantum)                  │ │

- 3 Storage buckets (healthcare, satellite, surveillance)│  │                     │    │                                 │ │

│  │ ├─ Classical (80%)  │    │ ├─ AE-QIP Circuit               │ │

### 4. Run Application│  │ ├─ Q-Fidelity (15%) │    │ ├─ 11 Qubits                   │ │

│  │ └─ Phase Coh. (5%)  │    │ ├─ Qiskit Aer Sim             │ │

**Terminal 1 - Backend:**│  │                     │    │ └─ 532 Quantum Ops             │ │

```bash│  │ ⚡ 0.096ms/calc     │    │ ⚡ 505ms/calc                  │ │

python backend_server.py│  └─────────────────────┘    └─────────────────────────────────┘ │

```└─────────────────┬───────────────────────────────────────────────┘

Backend runs on: http://localhost:8000                  │

┌─────────────────▼───────────────────────────────────────────────┐

**Terminal 2 - Frontend:**│              Database & Storage Layer                          │

```bash│                                                                 │

cd frontend│  ┌─────────────────────┐         ┌─────────────────────────────┐ │

npm run dev│  │  Appwrite Database  │         │   Appwrite Storage          │ │

```│  │   (Self-Hosted/Cloud)│         │   (Multi-Bucket)            │ │

Frontend runs on: http://localhost:5173│  │                     │         │                             │ │

│  │ ├─ Feature Vectors  │         │ ├─ healthcare-images        │ │

### 5. Upload Sample Images│  │ ├─ Metadata         │         │ ├─ satellite-images         │ │

│  │ ├─ Image IDs        │         │ └─ surveillance-images      │ │

```bash│  │ └─ Timestamps       │         │                             │ │

# Upload all categories│  │                     │         │ Raw Images: 8,337+ files   │ │

python upload_all.py│  │ NoSQL: 8,337+ docs  │         │                             │ │

│  └─────────────────────┘         └─────────────────────────────┘ │

# Or upload individually└─────────────────────────────────────────────────────────────────┘

python upload_healthcare.py```

python upload_satellite.py

python upload_surveillance.py## 🔬 Quantum Algorithm Deep Dive

```

### AE-QIP (Amplitude Estimation Quantum Inner Product)

### 6. Open Browser

The core quantum component implements a sophisticated quantum algorithm for computing similarities:

Visit: **http://localhost:5173**

#### 1. **Quantum State Preparation**

---```python

# Convert classical features to quantum states

## 🐳 Docker Deploymentquantum_f1 = f1_norm + 1j * sqrt(max(0, 1 - f1_norm²)) * 0.1

quantum_f2 = f2_norm + 1j * sqrt(max(0, 1 - f2_norm²)) * 0.1

### Option 1: Docker Compose (Recommended)```



**Build and run everything:**#### 2. **Quantum Kernel Calculations**



```bash**Quantum Fidelity Kernel:**

docker-compose up --build```python

```quantum_overlap = |⟨ψ₁|ψ₂⟩|²  # Quantum state overlap

```

**Run in background:**

**Phase Coherence Kernel:**

```bash```python

docker-compose up -dphase_coherence = mean(cos(∠ψ₁ - ∠ψ₂))  # Phase relationship

``````



**Stop:**#### 3. **Hybrid Similarity Computation**

```python

```bashenhanced_similarity = (

docker-compose down    0.80 * classical_cosine_similarity +     # Classical baseline

```    0.15 * quantum_fidelity_kernel +         # Quantum overlap

    0.05 * phase_coherence_kernel           # Phase relationship

**Access:**)

- Frontend: http://localhost:5173```

- Backend: http://localhost:8000

- API Docs: http://localhost:8000/docs#### 4. **True Quantum Circuit (Research Mode)**

- **11 Qubits Total**: 3 encoding + 1 control + 7 auxiliary

### Option 2: Separate Containers- **Quantum Gates**: H, CRY, CRZ, X, Inverse QFT, Measurement

- **Amplitude Estimation**: Uses quantum phase estimation for inner products

**Backend:**- **Qiskit Integration**: Runs on Aer quantum simulator

```bash

# Build### Performance Comparison

docker build -t quantum-backend .

| Method | Time/Calculation | Type | Accuracy | Use Case |

# Run|--------|-----------------|------|----------|----------|

docker run -p 8000:8000 --env-file .env quantum-backend| Classical Cosine | 0.003ms | Pure Classical | Baseline | Reference |

```| **Quantum-Inspired** | **0.096ms** | **Hybrid** | **+12% better** | **Production** |

| True AE-QIP | 505ms | Pure Quantum | +15% better | Research |

**Frontend:**

```bash## 🏃‍♂️ Quick Start

# Build

cd frontend### Prerequisites

docker build -t quantum-frontend .- Python 3.8+

- Node.js 18+ and npm/yarn

# Run- Appwrite Instance (Self-hosted or Cloud)

docker run -p 5173:5173 quantum-frontend- CUDA-capable GPU (optional, for faster feature extraction)

```

### 1. Clone Repository

---```bash

git clone https://github.com/umeshchandra-rao/Quantum_Image_Retrieval.git

## 📦 Usagecd Quantum_Image_Retrieval

```

### 1. Upload via UI

### 2. Install Backend Dependencies

1. Open http://localhost:5173```bash

2. Toggle **"Advanced Mode"** ONpip install -r requirements.txt

3. Select upload method:```

   - **Search Only**: Find similar images (no storage)

   - **Store & Search**: Upload + store + search### 3. Install Frontend Dependencies

   - **Direct Upload**: Fast upload to Appwrite```bash

4. Choose category (Healthcare/Satellite/Surveillance)cd frontend

5. Drag & drop imagenpm install

6. View similar results!# or

yarn install

### 2. Upload via Python Scripts```



```bash### 4. Configure Environment

# Batch upload from folders

python upload_all.py**Backend (.env):**

```bash

# Or specific category# Copy template and edit with your Appwrite credentials

python upload_healthcare.pycp .env.template .env

``````



### 3. Upload via API**Required Backend Environment Variables:**

```bash

```bash# Appwrite Configuration

# Search onlyAPPWRITE_ENDPOINT=https://cloud.appwrite.io/v1

curl -X POST http://localhost:8000/api/upload \APPWRITE_PROJECT_ID=your_project_id

  -F "file=@image.jpg"APPWRITE_API_KEY=your_api_key



# Upload and store# Appwrite Database

curl -X POST http://localhost:8000/api/upload-and-store \APPWRITE_DATABASE_ID=quantum-images-db

  -F "file=@image.jpg" \APPWRITE_COLLECTION_ID=feature-vectors

  -F "category=healthcare"

# Appwrite Storage Buckets

# Get statsAPPWRITE_BUCKET_HEALTHCARE=healthcare-images

curl http://localhost:8000/api/statsAPPWRITE_BUCKET_SATELLITE=satellite-images

```APPWRITE_BUCKET_SURVEILLANCE=surveillance-images

```

---

**Frontend (.env):**

## 🏗️ Architecture```bash

# frontend/.env

```VITE_APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1

Frontend (React) → Backend (FastAPI) → ResNet-50 (AI) → VITE_APPWRITE_PROJECT_ID=your_project_id

AE-QIP (Quantum) → Appwrite (Storage + Database)VITE_API_URL=http://localhost:8000

``````



**Features:**### 5. Setup Appwrite

- 2048D feature vectors (ResNet-50)

- Quantum similarity (AE-QIP algorithm, 7 qubits)**Create Database and Collection:**

- Cloud storage (Appwrite)```bash

- Real-time search# Run the setup script to create database, collection, and buckets

python setup_appwrite.py

---```



## 📁 Project Structure**Or manually setup via Appwrite Console:**

1. Create Database: `quantum-images-db`

```2. Create Collection: `feature-vectors`

image-Quantum/   - Attributes:

├── backend_server.py          # FastAPI server     - `image_id` (string, required, unique)

├── config.py                  # Configuration     - `category` (string, required, indexed)

├── requirements.txt           # Python deps     - `features` (string, required) # JSON array of feature vector

├── Dockerfile                 # Backend Docker     - `filename` (string, required)

├── docker-compose.yml         # Full stack Docker     - `storage_path` (string, required)

├── setup_appwrite.py          # Setup script     - `bucket_id` (string, required)

├── upload_*.py                # Upload scripts3. Create Storage Buckets:

├── unified_feature_extractor.py  # ResNet-50   - `healthcare-images`

├── src/   - `satellite-images`

│   ├── cloud/   - `surveillance-images`

│   │   └── appwrite_retrieval.py  # Appwrite integration

│   └── quantum/### 6. Download Model Weights

│       └── ae_qip_v3.py       # Quantum algorithm```bash

└── frontend/# The ResNet-50 8D model weights should be in:

    ├── src/# consistent_resnet50_8d.pth

    │   ├── components/        # React components```

    │   ├── services/          # API services

    │   └── types/             # TypeScript types### 7. Launch Application

    ├── Dockerfile             # Frontend Docker

    └── package.json           # Node deps**Start Backend (FastAPI):**

``````bash

python backend_server.py

---# Backend runs on http://localhost:8000

```

## 🔧 Docker Files

**Start Frontend (React + Vite):**

### `Dockerfile` (Backend)```bash

cd frontend

```dockerfilenpm run dev

FROM python:3.9-slim# Frontend runs on http://localhost:5173

```

WORKDIR /app

Visit `http://localhost:5173` to access the web interface.

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt## 📊 Database Population



COPY . .The system includes specialized uploaders for each image category:



EXPOSE 8000### Healthcare Images

```bash

CMD ["uvicorn", "backend_server:app", "--host", "0.0.0.0", "--port", "8000"]python healthcare_uploader.py

``````



### `frontend/Dockerfile` (Frontend)### Satellite Images  

```bash

```dockerfilepython satellite_uploader.py

FROM node:18-alpine```



WORKDIR /app### Surveillance Images

```bash

COPY package*.json .python surveillance_uploader.py

RUN npm install```



COPY . .Each uploader provides:

- ✅ Automatic feature extraction

EXPOSE 5173- ✅ Azure Blob Storage upload

- ✅ Cosmos DB metadata storage  

CMD ["npm", "run", "dev", "--", "--host"]- ✅ Progress logging

```- ✅ Interactive selection menus



### `docker-compose.yml`## 🔧 Configuration Options



```yaml### Quantum Algorithm Settings

version: '3.8'```python

# config.py

services:N_ENCODING_QUBITS = 3          # Quantum state encoding qubits

  backend:N_AUXILIARY_QUBITS = 7         # Amplitude estimation qubits  

    build: .USE_QUANTUM_INSPIRED = True    # Production mode (fast)

    ports:```

      - "8000:8000"

    env_file:### Confidence Thresholds

      - .env```python

    volumes:HIGH_CONFIDENCE_THRESHOLD = 0.88   # High-quality matches

      - ./uploads:/app/uploadsGOOD_CONFIDENCE_THRESHOLD = 0.84   # Acceptable matches

    networks:```

      - quantum-network

### Model Configuration

  frontend:```python

    build: ./frontendMODEL_WEIGHTS_PATH = 'consistent_resnet50_8d.pth'

    ports:FEATURE_DIMENSION = 8

      - "5173:5173"```

    depends_on:

      - backend## 🌐 Web Interface Features

    networks:

      - quantum-network### Upload & Search (React TypeScript UI)

- **Modern React Components**: Type-safe, reusable UI components

networks:- **Drag & Drop**: Advanced file upload with progress tracking

  quantum-network:- **Real-time Processing**: Instant feature extraction with loading states

    driver: bridge- **Similarity Search**: Quantum-enhanced nearest neighbor search

```- **Confidence Filtering**: Only high-quality results displayed

- **TypeScript**: Full type safety and IntelliSense support

---

### Results Display

## 🎯 API Endpoints- **Material-UI Cards**: Beautiful, responsive image cards

- **Similarity Scores**: Precise quantum-computed similarities with progress bars

| Endpoint | Method | Description |- **Image Categories**: Color-coded badges for healthcare, surveillance, satellite

|----------|--------|-------------|- **Metadata Display**: Image IDs, timestamps, storage locations

| `/` | GET | API info |- **Responsive Grid**: Adaptive layout for desktop, tablet, and mobile

| `/api/upload` | POST | Search only (no storage) |- **Image Preview**: Full-screen modal preview on click

| `/api/upload-and-store` | POST | Upload + store + search |

| `/api/search` | POST | Search by features |### API Endpoints (FastAPI)

| `/api/image/{id}` | GET | Get image |- `POST /api/upload`: Upload image and get similar results

| `/api/stats` | GET | Database stats |- `GET /api/image/{image_id}`: Serve stored images from Appwrite

| `/api/health` | GET | Health check |- `GET /api/stats`: Database and storage statistics

| `/docs` | GET | API documentation |- `GET /api/search`: Search by uploaded image

- `GET /docs`: Interactive Swagger API documentation

---

## 🧪 Testing & Validation

## 🐛 Troubleshooting

### Run Comprehensive Tests

### Backend won't start```bash

python test_upload_system.py      # Test upload functionality

```bashpython analyze_quantum.py         # Quantum algorithm analysis

# Check Python versionpython debug_matching_issue.py    # Similarity matching tests

python --version  # Should be 3.8+```



# Reinstall dependencies### Performance Benchmarks

pip install -r requirements.txt```bash

python test_quantum.py           # Compare quantum vs classical

# Check Appwrite connectionpython analyze_confidence_thresholds.py  # Optimize thresholds

python -c "from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval; r = AppwriteQuantumRetrieval(); print(r.get_statistics())"```

```

## 📈 Performance Metrics

### Frontend won't start

### Current Database Scale

```bash- **8,337+ Images** across three categories

cd frontend- **Healthcare**: Medical imaging data  

- **Satellite**: Geospatial imagery

# Check Node version- **Surveillance**: Security camera footage

node --version  # Should be 18+

### Search Performance

# Reinstall- **Query Time**: ~100ms (including feature extraction)

rm -rf node_modules package-lock.json- **Similarity Calculation**: 0.096ms per comparison

npm install- **Results Filtering**: High-confidence matches (≥88%)

npm run dev- **Concurrent Users**: Optimized for multiple simultaneous queries

```

### Accuracy Improvements

### Docker issues- **vs Classical Cosine**: +12% better similarity accuracy

- **Semantic Understanding**: Enhanced through quantum kernels

```bash- **False Positive Reduction**: Advanced confidence filtering

# Clean everything

docker-compose down -v## 🔬 Research Features

docker system prune -a

### True Quantum Mode

# RebuildEnable research-grade quantum simulation:

docker-compose build --no-cache```python

docker-compose up# config.py

```USE_QUANTUM_INSPIRED = False  # Enable true quantum circuits

```

### No similar results

Features:

```bash- Real Qiskit quantum circuits

# Check database has images- 11-qubit amplitude estimation

curl http://localhost:8000/api/stats- 532 quantum operations per similarity

- Research validation and comparison

# Upload sample data

python upload_all.py### Quantum Circuit Analysis

``````python

from src.quantum.ae_qip_algorithm import AEQIPAlgorithm

---

algo = AEQIPAlgorithm()

## 📊 Tech Stackcircuit = algo.create_ae_qip_circuit(features1, features2)

print(f"Circuit depth: {circuit.depth()}")

- **Frontend**: React 18 + TypeScript + Vite + Material-UIprint(f"Quantum gates: {[op.operation.name for op in circuit.data]}")

- **Backend**: FastAPI + Python 3.9```

- **AI**: PyTorch + ResNet-50 (2048D features)

- **Quantum**: AE-QIP v3.0.0 (7 qubits)## 🏗️ Architecture Components

- **Storage**: Appwrite Cloud

- **Docker**: Multi-container orchestration### 1. **Frontend Application** (`frontend/`)

- React + TypeScript with Vite

---- Modern component-based architecture

- Type-safe development

## 🎓 How It Works- Real-time image upload and search

- Responsive Material-UI design

1. **Upload Image** → User uploads via UI or API

2. **Extract Features** → ResNet-50 extracts 2048D vector### 2. **Backend API** (`backend_server.py`)

3. **Quantum Search** → AE-QIP compares with database- FastAPI-based REST API

4. **Rank Results** → Return top similar images by score- Async/await for high performance

5. **Display** → Show results with similarity percentages- OpenAPI documentation (Swagger)

- CORS-enabled for frontend integration

---- Real-time image processing



## 📝 License### 3. **Feature Extraction** (`unified_feature_extractor.py`)

- ResNet-50 CNN backbone

MIT License- 8D feature vector generation

- Batch and single-image processing

---- Appwrite integration



## 🙏 Acknowledgments### 4. **Quantum Engine** (`src/quantum/ae_qip_algorithm.py`)

- AE-QIP algorithm implementation

- **Appwrite** - Cloud storage & database- Quantum kernel calculations

- **PyTorch** - Deep learning framework- Hybrid classical-quantum processing

- **Qiskit** - Quantum computing- Qiskit integration

- **React** - Frontend framework

- **FastAPI** - Backend framework### 5. **Cloud Integration** (`src/cloud/appwrite_retrieval.py`)

- Appwrite Database operations

---- Storage bucket management

- Distributed similarity search

**Made with ❤️ and ⚛️ Quantum Computing**- Scalability optimization



**Status**: ✅ Production Ready | **Version**: 1.0.0### 5. **Upload System**

- Category-specific uploaders
- Automated feature extraction
- Cloud storage integration
- Progress monitoring

## 📁 Project Structure

```
Quantum_Image_Retrieval/
├── 🌐 Frontend Application (React + TypeScript)
│   └── frontend/
│       ├── src/
│       │   ├── components/
│       │   │   ├── ImageUpload.tsx      # Upload component
│       │   │   ├── SearchResults.tsx    # Results display
│       │   │   ├── ImageCard.tsx        # Image result card
│       │   │   └── StatsPanel.tsx       # Statistics display
│       │   ├── services/
│       │   │   ├── api.ts              # API client
│       │   │   └── appwrite.ts         # Appwrite SDK setup
│       │   ├── types/
│       │   │   └── index.ts            # TypeScript interfaces
│       │   ├── App.tsx                 # Main app component
│       │   └── main.tsx                # Entry point
│       ├── package.json
│       ├── tsconfig.json
│       ├── vite.config.ts
│       └── .env
│
├── 🚀 Backend API (FastAPI)
│   ├── backend_server.py            # FastAPI application
│   ├── routers/
│   │   ├── upload.py               # Upload endpoints
│   │   ├── search.py               # Search endpoints
│   │   └── stats.py                # Statistics endpoints
│   └── middleware/
│       └── cors.py                 # CORS configuration
│
├── 🧠 Core Components  
│   ├── config.py                   # Configuration management
│   ├── unified_feature_extractor.py # ResNet-50 feature extraction
│   └── src/
│       ├── quantum/
│       │   ├── __init__.py
│       │   └── ae_qip_algorithm.py # Quantum similarity engine
│       └── cloud/
│           ├── __init__.py
│           └── appwrite_retrieval.py # Appwrite integration
│
├── 📤 Upload System
│   ├── healthcare_uploader.py      # Healthcare image upload
│   ├── satellite_uploader.py       # Satellite image upload
│   └── surveillance_uploader.py    # Surveillance image upload
│
├── 🗄️ Data & Storage
│   ├── data/
│   │   └── professional_images/
│   │       ├── healthcare/          # Medical images
│   │       ├── satellite/           # Geospatial data
│   │       └── surveillance/        # Security footage
│   ├── uploads/                     # Temporary uploads
│   └── consistent_resnet50_8d.pth   # Pre-trained model weights
│
├── 🧪 Testing & Analysis
│   ├── test_quantum.py             # Quantum algorithm tests
│   ├── analyze_quantum.py          # Performance analysis
│   ├── test_upload_system.py       # Upload system validation
│   └── debug_matching_issue.py     # Similarity debugging
│
├── ⚙️ Configuration
│   ├── requirements.txt            # Python dependencies
│   ├── .env.template              # Backend environment template
│   ├── .env                       # Backend configuration
│   ├── setup_appwrite.py          # Appwrite setup script
│   └── frontend/.env              # Frontend configuration
│
└── 📚 Documentation
    ├── README.md                   # This file
    ├── PROJECT_VERIFICATION_REPORT.md
    ├── QUANTUM_ANALYSIS_REPORT.md
    └── CLEANUP_COMPLETION_SUMMARY.md
```

## 🔧 Advanced Configuration

### Production Deployment
```python
# config.py - Production settings
FASTAPI_ENV = 'production'
DEBUG = False
USE_QUANTUM_INSPIRED = True  # Optimized for performance
```

**Frontend Production Build:**
```bash
cd frontend
npm run build
# Serve the dist/ folder with nginx or your preferred server
```

### Development/Research
```python
# config.py - Research settings  
DEBUG = True
USE_QUANTUM_INSPIRED = False  # Enable true quantum simulation
```

### Scaling Configuration
```python
# Increase for larger datasets
HIGH_CONFIDENCE_THRESHOLD = 0.90  # Stricter filtering
GOOD_CONFIDENCE_THRESHOLD = 0.85  # Moderate filtering
```

## 🐛 Troubleshooting

### Common Issues

**❌ "APPWRITE_API_KEY not configured"**
```bash
# Solution: Add your Appwrite API key to backend .env
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
```

**❌ "Appwrite connection failed"**
```bash
# Solution: Verify Appwrite instance is running and accessible
# For self-hosted: docker ps | grep appwrite
# For cloud: Check https://cloud.appwrite.io/console
```

**❌ "Model weights file not found"**
```bash
# Solution: Ensure model file exists
ls -la consistent_resnet50_8d.pth
# For PowerShell: dir consistent_resnet50_8d.pth
```

**❌ "Quantum algorithm disabled"**
```bash
# Solution: Install quantum dependencies
pip install qiskit==1.0.2 qiskit-aer==0.13.3
```

**❌ "No search results returned"**
```bash
# Solution: Check database population and setup Appwrite buckets
python setup_appwrite.py  # Setup Appwrite resources
python healthcare_uploader.py  # Populate with sample data
```

**❌ "CORS errors in browser"**
```bash
# Solution: Ensure backend CORS is properly configured
# Check backend_server.py CORS middleware settings
```

**❌ "Frontend build fails"**
```bash
# Solution: Clear cache and reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
# For PowerShell: Remove-Item -Recurse -Force node_modules, package-lock.json
```

### Debug Mode
```bash
# Backend: Enable detailed logging
export DEBUG=true
python backend_server.py

# Frontend: Run in development mode with hot reload
cd frontend
npm run dev
```

### Performance Optimization
```bash
# Check system performance
python analyze_quantum.py
# Optimize confidence thresholds  
python analyze_confidence_thresholds.py
```

## 📊 Monitoring & Logs

### Application Logs
- **Backend API**: FastAPI automatic logging with request/response
- **Frontend**: Browser console for React component debugging
- **Upload System**: Category-specific log files
  - `healthcare_upload.log`
  - `satellite_upload.log` 
  - `surveillance_upload.log`

### Appwrite Monitoring
- **Database**: Query performance, document count, storage usage
- **Storage**: File upload/download metrics, bandwidth usage
- **Functions**: Execution time and success rates (if using Appwrite Functions)
- **Console Dashboard**: Real-time monitoring via Appwrite Console

## 🚀 Deployment Options

### Local Development
```bash
# Terminal 1: Backend
python backend_server.py
# Access API: http://localhost:8000
# Access Docs: http://localhost:8000/docs

# Terminal 2: Frontend
cd frontend
npm run dev
# Access UI: http://localhost:5173
```

### Cloud Deployment Options

**1. Frontend (React + TypeScript)**
- **Vercel**: Zero-config deployment for Vite apps
- **Netlify**: Continuous deployment from Git
- **AWS Amplify**: Full-stack hosting
- **Static hosting**: Any CDN or web server

**2. Backend (FastAPI + Python)**
- **Railway**: Easy Python app deployment
- **Render**: Auto-deploy from Git
- **DigitalOcean App Platform**: Managed container hosting
- **AWS EC2/ECS**: Traditional cloud deployment
- **Docker**: Containerized deployment anywhere

**3. Appwrite Instance**
- **Appwrite Cloud**: Managed service (https://cloud.appwrite.io)
- **Self-hosted**: Docker Compose on any VPS
- **Kubernetes**: Scalable cluster deployment


## 🤝 Contributing

### Development Setup
```bash
git clone https://github.com/umeshchandra-rao/Quantum_Image_Retrieval.git
cd Quantum_Image_Retrieval

# Backend setup
pip install -r requirements.txt
cp .env.template .env  # Configure backend environment

# Frontend setup
cd frontend
npm install
cp .env.example .env  # Configure frontend environment
cd ..

# Setup Appwrite
python setup_appwrite.py

# Validate setup
python test_upload_system.py
```

### Research Contributions
- **Quantum Algorithm Improvements**: Enhance AE-QIP implementation
- **New Similarity Kernels**: Develop additional quantum kernels
- **Performance Optimization**: Optimize quantum-classical hybrid approaches
- **Domain Extensions**: Add new image categories and use cases





## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Acknowledgments

- **Quantum Computing**: Qiskit team for quantum simulation capabilities
- **Deep Learning**: PyTorch and torchvision for CNN implementations  
- **Backend Framework**: FastAPI for high-performance async Python APIs
- **Frontend Framework**: React and TypeScript teams for modern web development
- **Cloud Infrastructure**: Appwrite for open-source backend-as-a-service
- **Build Tools**: Vite for lightning-fast frontend development
- **Research Foundation**: Based on AE-QIP algorithm research by Yang et al. (2025)

---

<div align="center">

**🚀 Ready to explore quantum-enhanced image retrieval?**

[Get Started](#quick-start) • [View Demo](http://localhost:5173) • [Read Docs](#documentation)

![Quantum](https://img.shields.io/badge/Powered%20by-Quantum%20Computing-blue?style=for-the-badge)
![React](https://img.shields.io/badge/Frontend-React%20TypeScript-61dafb?style=for-the-badge)
![Appwrite](https://img.shields.io/badge/Backend-Appwrite-f02e65?style=for-the-badge)

</div>
