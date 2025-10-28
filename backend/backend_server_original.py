from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv
import io
from PIL import Image
from typing import Optional
import logging
from datetime import datetime

# Load .env before importing config
load_dotenv()

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config
from services.cloudinary_service import CloudinaryImageService
from services.pinecone_service import PineconeVectorService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

feature_extractor = None
cloudinary_service = None
pinecone_service = None

def get_feature_extractor():
    global feature_extractor
    if feature_extractor is None:
        from ml.unified_feature_extractor import UnifiedFeatureExtractor
        feature_extractor = UnifiedFeatureExtractor(feature_dim=config.FEATURE_DIMENSION)
    return feature_extractor

def get_cloudinary_service():
    global cloudinary_service
    if cloudinary_service is None:
        cloudinary_service = CloudinaryImageService()
    return cloudinary_service

def get_pinecone_service():
    global pinecone_service
    if pinecone_service is None:
        pinecone_service = PineconeVectorService()
    return pinecone_service

app = FastAPI(title='Quantum Image API', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.get('/')
async def root():
    return {'message': 'Quantum Image API v2.0', 'storage': 'Cloudinary', 'vectors': 'Pinecone'}

@app.post('/api/upload')
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        features = get_feature_extractor().extract_features(image)
        matches = get_pinecone_service().search(features, top_k=10, min_score=config.GOOD_CONFIDENCE_THRESHOLD)
        results = [{'id': m['id'], 'filename': m['metadata'].get('filename'), 'category': m['metadata'].get('category'), 'similarity': m['score'], 'image_url': m['metadata'].get('cloudinary_url')} for m in matches]
        return {'success': True, 'similar_images': results}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post('/api/upload-and-store')
async def upload_and_store(file: UploadFile = File(...), category: str = 'healthcare'):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        features = get_feature_extractor().extract_features(image)
        result = get_cloudinary_service().upload_image(contents, file.filename, category)
        vector_id = result['public_id'].replace('/', '_')
        metadata = {'filename': file.filename, 'category': category, 'cloudinary_url': result['secure_url'], 'uploaded_at': datetime.utcnow().isoformat()}
        get_pinecone_service().upsert_vector(vector_id, features, metadata)
        matches = get_pinecone_service().search(features, top_k=10, category_filter=category, min_score=config.GOOD_CONFIDENCE_THRESHOLD)
        results = [{'id': m['id'], 'filename': m['metadata'].get('filename'), 'similarity': m['score'], 'image_url': m['metadata'].get('cloudinary_url')} for m in matches if m['id'] != vector_id]
        return {'success': True, 'uploaded_image': {'filename': file.filename, 'cloudinary_url': result['secure_url']}, 'similar_images': results}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get('/api/stats')
async def get_stats():
    return {'success': True, 'statistics': get_pinecone_service().get_statistics()}

@app.get('/health')
async def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    uvicorn.run(app, host=config.HOST, port=config.PORT)
