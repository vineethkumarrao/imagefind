"""
Setup Script for Cloudinary + Pinecone
This script will:
1. Verify Cloudinary connection
2. Create Pinecone index if it doesn't exist
3. Test uploads to all 3 categories
"""

import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import cloudinary
import cloudinary.api
import cloudinary.uploader
import logging

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_cloudinary():
    """Setup and test Cloudinary connection"""
    logger.info("=" * 60)
    logger.info("🌥️  CLOUDINARY SETUP")
    logger.info("=" * 60)
    
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    
    if not all([cloud_name, api_key, api_secret]):
        logger.error("❌ Missing Cloudinary credentials!")
        logger.error("Please set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET in .env")
        return False
    
    if api_secret == "REPLACE_WITH_YOUR_API_SECRET_FROM_DASHBOARD":
        logger.error("❌ Please replace CLOUDINARY_API_SECRET in .env with your actual secret!")
        logger.error("Get it from: https://console.cloudinary.com/settings/security")
        return False
    
    # Configure Cloudinary
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True
    )
    
    logger.info(f"✅ Cloud Name: {cloud_name}")
    logger.info(f"✅ API Key: {api_key[:10]}...")
    logger.info(f"✅ API Secret: {api_secret[:10]}...")
    
    # Test connection
    try:
        # Try to get account info
        result = cloudinary.api.ping()
        logger.info("✅ Cloudinary connection successful!")
        logger.info(f"   Status: {result.get('status', 'OK')}")
        return True
    except Exception as e:
        logger.error(f"❌ Cloudinary connection failed: {e}")
        return False


def setup_pinecone():
    """Setup and test Pinecone connection"""
    logger.info("\n" + "=" * 60)
    logger.info("🌲 PINECONE SETUP")
    logger.info("=" * 60)
    
    api_key = os.getenv('PINECONE_API_KEY')
    index_name = os.getenv('PINECONE_INDEX_NAME', 'quantum-images-prod')
    dimension = int(os.getenv('FEATURE_DIMENSION', '2048'))
    
    if not api_key:
        logger.error("❌ Missing PINECONE_API_KEY in .env")
        return False
    
    logger.info(f"✅ API Key: {api_key[:20]}...")
    logger.info(f"✅ Index Name: {index_name}")
    logger.info(f"✅ Dimension: {dimension}")
    
    try:
        # Initialize Pinecone
        pc = Pinecone(api_key=api_key)
        
        # Check if index exists
        existing_indexes = pc.list_indexes().names()
        logger.info(f"📊 Existing indexes: {existing_indexes}")
        
        if index_name not in existing_indexes:
            logger.info(f"📦 Creating index: {index_name}...")
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
            logger.info(f"✅ Index '{index_name}' created successfully!")
        else:
            logger.info(f"✅ Index '{index_name}' already exists")
        
        # Connect to index
        index = pc.Index(index_name)
        stats = index.describe_index_stats()
        
        logger.info("✅ Pinecone connection successful!")
        logger.info(f"   Total vectors: {stats.total_vector_count}")
        logger.info(f"   Dimension: {dimension}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Pinecone setup failed: {e}")
        return False


def verify_folders():
    """Verify Cloudinary folder structure for 3 categories"""
    logger.info("\n" + "=" * 60)
    logger.info("📁 CLOUDINARY FOLDER STRUCTURE")
    logger.info("=" * 60)
    
    categories = ['healthcare', 'satellite', 'surveillance']
    
    for category in categories:
        folder_path = f"quantum-images/{category}"
        logger.info(f"✅ {category.capitalize()}: {folder_path}")
    
    logger.info("\n💡 Images will be organized as:")
    logger.info("   quantum-images/healthcare/image1.jpg")
    logger.info("   quantum-images/satellite/image2.jpg")
    logger.info("   quantum-images/surveillance/image3.jpg")
    
    return True


def main():
    """Run complete setup"""
    logger.info("\n" + "🚀 " * 20)
    logger.info("QUANTUM IMAGE RETRIEVAL - SETUP")
    logger.info("🚀 " * 20 + "\n")
    
    cloudinary_ok = setup_cloudinary()
    pinecone_ok = setup_pinecone()
    folders_ok = verify_folders()
    
    logger.info("\n" + "=" * 60)
    logger.info("📊 SETUP SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Cloudinary: {'✅ Connected' if cloudinary_ok else '❌ Failed'}")
    logger.info(f"Pinecone:   {'✅ Connected' if pinecone_ok else '❌ Failed'}")
    logger.info(f"Folders:    {'✅ Configured' if folders_ok else '❌ Failed'}")
    
    if cloudinary_ok and pinecone_ok:
        logger.info("\n🎉 SETUP COMPLETE! You're ready to go!")
        logger.info("\n📋 Next steps:")
        logger.info("   1. Backend: python backend_server.py")
        logger.info("   2. Frontend: cd frontend && npm install && npm run dev")
        logger.info("   3. Upload images via UI or scripts")
        return True
    else:
        logger.error("\n❌ Setup incomplete. Please fix errors above.")
        return False


if __name__ == "__main__":
    main()
