"""
Simple Backend Server for Testing (without ML model loading)
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
import os
import io
from PIL import Image
from typing import List
import logging
import numpy as np

import config
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Quantum Image Retrieval API",
    description="Quantum-enhanced image similarity search",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize retrieval system
try:
    logger.info("Initializing Appwrite retrieval system...")
    retrieval_system = AppwriteQuantumRetrieval()
    logger.info("Appwrite retrieval system initialized")
except Exception as e:
    logger.error(f"Initialization failed: {e}")
    raise

# Create uploads directory
os.makedirs('uploads', exist_ok=True)


def extract_dummy_features(image):
    """Extract dummy features for testing (replace with real model later)"""
    # Convert image to numpy array
    img_array = np.array(image.resize((224, 224)))
    # Generate 8D feature vector from image statistics
    features = [
        float(np.mean(img_array[:, :, 0])),  # Red channel mean
        float(np.mean(img_array[:, :, 1])),  # Green channel mean
        float(np.mean(img_array[:, :, 2])),  # Blue channel mean
        float(np.std(img_array[:, :, 0])),   # Red channel std
        float(np.std(img_array[:, :, 1])),   # Green channel std
        float(np.std(img_array[:, :, 2])),   # Blue channel std
        float(np.mean(img_array)),           # Overall mean
        float(np.std(img_array)),            # Overall std
    ]
    return features


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Quantum Image Retrieval API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image and find similar images"""
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        logger.info(f"📸 Processing: {file.filename}")
        
        # Extract features (dummy for now)
        features_list = extract_dummy_features(image)
    logger.info(f"Features extracted: {features_list[:3]}...")
        
        # Search similar images
    logger.info("Searching database...")
        similar_images = retrieval_system.search_similar_images(
            query_features=features_list,
            top_k=10,
            confidence_threshold=config.GOOD_CONFIDENCE_THRESHOLD
        )
        
    logger.info(f"Found {len(similar_images)} similar images")
        
        high_confidence = [
            img for img in similar_images 
            if img['similarity'] >= config.HIGH_CONFIDENCE_THRESHOLD
        ]
        
        return JSONResponse(content={
            "success": True,
            "query_image": file.filename,
            "total_results": len(similar_images),
            "high_confidence_results": len(high_confidence),
            "results": similar_images
        })
        
    except Exception as e:
    logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/image/{image_id}")
async def get_image(image_id: str):
    """Get image by ID"""
    try:
        image_data = retrieval_system.get_image(image_id)
        
        if not image_data:
            raise HTTPException(status_code=404, detail="Image not found")
        
        return StreamingResponse(
            io.BytesIO(image_data),
            media_type="image/jpeg"
        )
    except HTTPException:
        raise
    except Exception as e:
    logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_statistics():
    """Get database statistics"""
    try:
        stats = retrieval_system.get_statistics()
        return JSONResponse(content={
            "success": True,
            "statistics": stats
        })
    except Exception as e:
    logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "feature_extractor": "dummy (for testing)",
        "retrieval_system": "ready",
        "appwrite": "connected"
    }


@app.on_event("startup")
async def startup_event():
    """Startup tasks"""
    logger.info("Starting Quantum Image Retrieval API...")
    logger.info(f"📍 Appwrite: {config.APPWRITE_ENDPOINT}")
    logger.info(f"Mode: Quantum-Inspired")
    logger.info("Using dummy feature extractor for testing")


if __name__ == "__main__":
    try:
        config.validate()
    except ValueError as e:
    logger.error(f"Config error: {e}")
        exit(1)
    
    logger.info(f"🌐 Starting server on {config.HOST}:{config.PORT}")
    uvicorn.run(
        "backend_simple:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info"
    )
