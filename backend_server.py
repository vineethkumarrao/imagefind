"""
FastAPI Backend Server for Quantum Image Retrieval System
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

from config import config
from src.cloud.appwrite_retrieval import AppwriteQuantumRetrieval
# Lazy import to avoid slow startup
# from unified_feature_extractor import UnifiedFeatureExtractor
# from src.quantum.ae_qip_v3 import AEQIPAlgorithm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for lazy loading
feature_extractor = None
quantum_algorithm = None

def get_feature_extractor():
    """Lazy load feature extractor"""
    global feature_extractor
    if feature_extractor is None:
        logger.info("Loading ResNet-50 feature extractor (2048D native)...")
        from unified_feature_extractor import UnifiedFeatureExtractor
        feature_extractor = UnifiedFeatureExtractor(feature_dim=2048)
        logger.info("Feature extractor loaded")
    return feature_extractor

def get_quantum_algorithm():
    """Lazy load quantum algorithm"""
    global quantum_algorithm
    if quantum_algorithm is None:
        logger.info("Loading AE-QIP v3.0.0 quantum algorithm...")
        from src.quantum.ae_qip_v3 import AEQIPAlgorithm
        quantum_algorithm = AEQIPAlgorithm(
            use_quantum_inspired=True,
            n_precision_qubits=7,
            enable_entanglement=False
        )
        logger.info("Quantum algorithm loaded")
        circuit_info = quantum_algorithm.get_circuit_info()
        logger.info(f"   Qubits: {circuit_info['total_qubits']} "
                   f"({circuit_info['encoding_qubits']}+"
                   f"{circuit_info['control_qubits']}+"
                   f"{circuit_info['auxiliary_qubits']})")
    return quantum_algorithm

# Initialize FastAPI app
logger.info("Initializing Quantum Image Retrieval API with 2048D features...")
app = FastAPI(
    title="Quantum Image Retrieval API",
    description="Quantum-enhanced image similarity search with Appwrite backend",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
try:
    # Don't load feature extractor yet - lazy load on first use
    logger.info("Initializing Appwrite retrieval system...")
    retrieval_system = AppwriteQuantumRetrieval()
    logger.info("Appwrite retrieval system initialized")
    logger.info("Feature extractor will load on first request")
    
except Exception as e:
    logger.error(f"Initialization failed: {e}")
    raise

# Create uploads directory
os.makedirs('uploads', exist_ok=True)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Quantum Image Retrieval API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "upload": "/api/upload",
            "search": "/api/search",
            "stats": "/api/stats",
            "image": "/api/image/{image_id}"
        }
    }

@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image and find similar images
    
    Args:
        file: Image file to upload
        
    Returns:
        JSON with similar images and their similarity scores
    """
    try:
        # Validate file type
        if file.content_type and not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        logger.info(f"Processing uploaded image: {file.filename}")
        
        # Extract features (lazy load model on first use)
        logger.info("Extracting features...")
        extractor = get_feature_extractor()
        features_list = extractor.extract_features(image)
        
        logger.info(f"Features extracted: {len(features_list)} dimensions")
        
        # Search for similar images
        logger.info("Searching for similar images...")
        similar_images = retrieval_system.search_similar_images(
            query_features=features_list,
            top_k=10,
            confidence_threshold=config.GOOD_CONFIDENCE_THRESHOLD
        )
        
        logger.info(f"Found {len(similar_images)} similar images")
        
        # Check if we found any very high confidence match (>95% = likely exact match)
        exact_match = None
        high_confidence_results = []
        
        for img in similar_images:
            if img['similarity'] >= config.HIGH_CONFIDENCE_THRESHOLD:
                high_confidence_results.append(img)
                if img['similarity'] >= 0.98:  # Very high similarity = likely exact image
                    exact_match = img
        
        # Determine status
        if not similar_images:
            status = "not_found"
            message = "No similar images found in database"
        elif exact_match:
            status = "exact_match"
            message = f"Found exact match: {exact_match['filename']}"
        elif high_confidence_results:
            status = "high_confidence"
            message = f"Found {len(high_confidence_results)} high confidence matches"
        else:
            status = "low_confidence"
            message = "Found some matches but with low confidence"
        
        return JSONResponse(content={
            "success": True,
            "status": status,
            "message": message,
            "query_image": file.filename,
            "total_results": len(similar_images),
            "high_confidence_results": len(high_confidence_results),
            "exact_match": exact_match,
            "results": similar_images
        })
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-and-store")
async def upload_and_store(
    file: UploadFile = File(...),
    category: str = 'healthcare'
):
    """
    Upload an image, extract features, store in Appwrite, and find similar images
    
    Args:
        file: Image file to upload
        category: Category of the image (healthcare, satellite, surveillance)
        
    Returns:
        JSON with upload info and similar images
    """
    try:
        # Validate category
        if category not in ['healthcare', 'satellite', 'surveillance']:
            raise HTTPException(status_code=400, detail="Invalid category")
        
        # Validate file type
        if file.content_type and not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        logger.info(f"Uploading and storing image: {file.filename} (category: {category})")
        
        # Extract features
        logger.info("Extracting features...")
        extractor = get_feature_extractor()
        features_list = extractor.extract_features(image)
        
        # Store in Appwrite (this will handle upload to storage + database)
        logger.info("Storing in Appwrite...")
        from appwrite import ID
        
        # Convert PIL image to bytes for storage
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr.seek(0)
        
        # Upload to Appwrite storage
        bucket_id = config.CATEGORY_BUCKET_MAP.get(category)
        file_id = ID.unique()
        
        storage_file = retrieval_system.storage.create_file(
            bucket_id=bucket_id,
            file_id=file_id,
            file=img_byte_arr.getvalue()
        )
        
        logger.info(f"File uploaded to storage: {storage_file['$id']}")
        
        # Store metadata in database
        document = retrieval_system.databases.create_document(
            database_id=config.DATABASE_ID,
            collection_id=config.COLLECTION_ID,
            document_id=ID.unique(),
            data={
                'image_id': storage_file['$id'],
                'filename': file.filename,
                'category': category,
                'bucket_id': bucket_id,
                'storage_path': f"{bucket_id}/{storage_file['$id']}",
                'features': features_list,
                'feature_dim': len(features_list)
            }
        )
        
        logger.info(f"Metadata stored in database: {document['$id']}")
        
        # Search for similar images
        logger.info("Searching for similar images...")
        similar_images = retrieval_system.search_similar_images(
            query_features=features_list,
            top_k=10,
            confidence_threshold=config.GOOD_CONFIDENCE_THRESHOLD
        )
        
        return JSONResponse(content={
            "success": True,
            "status": "stored",
            "message": f"Image uploaded and stored in {category} category",
            "query_image": file.filename,
            "file_id": storage_file['$id'],
            "document_id": document['$id'],
            "category": category,
            "total_results": len(similar_images),
            "results": similar_images
        })
        
    except Exception as e:
        logger.error(f"Upload and store error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
async def search_by_features(features: List[float]):
    """
    Search for similar images using feature vector
    
    Args:
        features: Feature vector (2048D)
        
    Returns:
        JSON with similar images
    """
    try:
        if len(features) != config.FEATURE_DIMENSION:
            raise HTTPException(
                status_code=400, 
                detail=f"Feature vector must have {config.FEATURE_DIMENSION} dimensions"
            )
        
        similar_images = retrieval_system.search_similar_images(
            query_features=features,
            top_k=10,
            confidence_threshold=config.GOOD_CONFIDENCE_THRESHOLD
        )
        
        return JSONResponse(content={
            "success": True,
            "total_results": len(similar_images),
            "results": similar_images
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/image/{image_id}")
async def get_image(image_id: str):
    """
    Get image by ID from Appwrite storage
    
    Args:
        image_id: Image document ID
        
    Returns:
        Image file stream
    """
    try:
        # Get image from Appwrite
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
        logger.error(f"Image retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_statistics():
    """
    Get database and storage statistics
    
    Returns:
        JSON with statistics
    """
    try:
        stats = retrieval_system.get_statistics()
        
        return JSONResponse(content={
            "success": True,
            "statistics": stats
        })
        
    except Exception as e:
        logger.error(f"Statistics error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/categories")
async def get_categories():
    """Get list of image categories"""
    return JSONResponse(content={
        "success": True,
        "categories": ["healthcare", "satellite", "surveillance"]
    })

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "feature_extractor": "ready",
        "retrieval_system": "ready",
        "appwrite": "connected"
    }

@app.on_event("startup")
async def startup_event():
    """Startup tasks"""
    logger.info("Starting Quantum Image Retrieval API...")
    logger.info(f"Appwrite Endpoint: {config.APPWRITE_ENDPOINT}")
    logger.info(f"Project ID: {config.APPWRITE_PROJECT_ID}")
    logger.info(f"Model: {config.MODEL_WEIGHTS_PATH}")
    logger.info(f"Quantum Mode: {'Inspired' if config.USE_QUANTUM_INSPIRED else 'True Quantum'}")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown tasks"""
    logger.info("Shutting down Quantum Image Retrieval API...")

if __name__ == "__main__":
    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        exit(1)
    
    # Run server
    logger.info(f"Starting server on {config.HOST}:{config.PORT}")
    uvicorn.run(
        "backend_server:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info"
    )
