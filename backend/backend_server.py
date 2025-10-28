
import os
import sys
import io
import logging
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from PIL import Image
import uvicorn
from config import config
from services.cloudinary_service import CloudinaryImageService
from services.pinecone_service import PineconeVectorService


# Load .env before importing config
load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

feature_extractor = None
cloudinary_service = None
pinecone_service = None
cache_service = None


def get_feature_extractor():
    global feature_extractor
    if feature_extractor is None:
        extractor_type = os.getenv('FEATURE_EXTRACTOR_TYPE', 'resnet')

        if extractor_type == 'vit':
            try:
                from ml.feature_extractors.vit_extractor import ViTFeatureExtractor
                feature_extractor = ViTFeatureExtractor()
                logger.info("Using ViT feature extractor")
            except Exception as e:
                logger.warning(f"ViT not available: {e}. Using ResNet.")
                from ml.unified_feature_extractor import UnifiedFeatureExtractor
                feature_extractor = UnifiedFeatureExtractor(
                    feature_dim=config.FEATURE_DIMENSION,
                    use_amp=True
                )
        elif extractor_type == 'ensemble':
            try:
                from ml.feature_extractors.ensemble_extractor import EnsembleFeatureExtractor
                feature_extractor = EnsembleFeatureExtractor(
                    feature_dim=config.FEATURE_DIMENSION
                )
                logger.info("Using Ensemble feature extractor")
            except Exception as e:
                logger.warning(f"Ensemble not available: {e}. Using ResNet.")
                from ml.unified_feature_extractor import UnifiedFeatureExtractor
                feature_extractor = UnifiedFeatureExtractor(
                    feature_dim=config.FEATURE_DIMENSION,
                    use_amp=True
                )
        else:
            from ml.unified_feature_extractor import UnifiedFeatureExtractor
            feature_extractor = UnifiedFeatureExtractor(
                feature_dim=config.FEATURE_DIMENSION,
                use_amp=True
            )
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


def get_cache_service():
    global cache_service
    if cache_service is None:
        try:
            from services.cache_service import get_cache
            cache_service = get_cache()
            logger.info("Cache service enabled")
        except Exception as e:
            logger.warning(f"Cache not available: {e}")
            cache_service = None
    return cache_service


app = FastAPI(title='Quantum Image API', version='3.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get('/')
async def root():
    cache_stats = {}
    cache = get_cache_service()
    if cache:
        cache_stats = cache.get_stats()
    return {
        'message': 'Quantum Image API v3.0',
        'storage': 'Cloudinary',
        'vectors': 'Pinecone',
        'cache': cache_stats,
        'features': ['caching', 'rate-limiting', 'multi-model']
    }


@app.post('/api/upload')
@limiter.limit("20/minute")
async def upload_image(request: Request, file: UploadFile = File(...)):
    try:
        start_time = time.time()
        contents = await file.read()

        # Try cache first
        cache = get_cache_service()
        features = None
        if cache:
            features = cache.get_features(contents)

        # Extract features if not cached
        if features is None:
            image = Image.open(io.BytesIO(contents)).convert('RGB')
            features = get_feature_extractor().extract_features(image)

            # Cache for future use
            if cache:
                cache.set_features(contents, features)

        # Search similar images
        matches = get_pinecone_service().search(
            features,
            top_k=10,
            min_score=config.GOOD_CONFIDENCE_THRESHOLD
        )

        results = [{
            'id': m['id'],
            'filename': m['metadata'].get('filename'),
            'category': m['metadata'].get('category'),
            'similarity': m['score'],
            'image_url': m['metadata'].get('cloudinary_url')
        } for m in matches]

        elapsed = time.time() - start_time

        return {
            'success': True,
            'similar_images': results,
            'processing_time': f"{elapsed:.3f}s",
            'cached': features is not None and cache is not None
        }
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(500, str(e))


@app.post('/api/upload-and-store')
@limiter.limit("10/minute")
async def upload_and_store(
    request: Request,
    file: UploadFile = File(...),
    category: str = 'healthcare'
):
    try:
        start_time = time.time()
        contents = await file.read()

        # Extract features with caching
        cache = get_cache_service()
        features = None
        if cache:
            features = cache.get_features(contents)

        if features is None:
            image = Image.open(io.BytesIO(contents)).convert('RGB')
            features = get_feature_extractor().extract_features(image)
            if cache:
                cache.set_features(contents, features)

        # Upload to Cloudinary
        result = get_cloudinary_service().upload_image(
            contents,
            file.filename,
            category
        )

        # Store in Pinecone
        vector_id = result['public_id'].replace('/', '_')
        metadata = {
            'filename': file.filename,
            'category': category,
            'cloudinary_url': result['secure_url'],
            'uploaded_at': datetime.utcnow().isoformat()
        }
        get_pinecone_service().upsert_vector(vector_id, features, metadata)

        # Search similar
        matches = get_pinecone_service().search(
            features,
            top_k=10,
            category_filter=category,
            min_score=config.GOOD_CONFIDENCE_THRESHOLD
        )

        results = [{
            'id': m['id'],
            'filename': m['metadata'].get('filename'),
            'similarity': m['score'],
            'image_url': m['metadata'].get('cloudinary_url')
        } for m in matches if m['id'] != vector_id]

        elapsed = time.time() - start_time

        return {
            'success': True,
            'uploaded_image': {
                'filename': file.filename,
                'cloudinary_url': result['secure_url']
            },
            'similar_images': results,
            'processing_time': f"{elapsed:.3f}s"
        }
    except Exception as e:
        logger.error(f"Upload and store error: {e}")
        raise HTTPException(500, str(e))


@app.get('/api/stats')
async def get_stats():
    stats = get_pinecone_service().get_statistics()
    return {
        'success': True,
        'statistics': stats
    }


@app.get('/health')
async def health():
    return {'status': 'healthy'}


if __name__ == '__main__':
    uvicorn.run(app, host=config.HOST, port=config.PORT)
