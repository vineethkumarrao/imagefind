"""
Update Appwrite Collection for 512D Feature Vectors
"""

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
from config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def update_collection():
    """Update collection to support 512D feature vectors"""
    try:
        # Initialize Appwrite client
        client = Client()
        client.set_endpoint(config.APPWRITE_ENDPOINT)
        client.set_project(config.APPWRITE_PROJECT_ID)
        client.set_key(config.APPWRITE_API_KEY)
        
        databases = Databases(client)
        
        logger.info("🔄 Updating collection for 512D features...")
        
        # Delete old features attribute
        try:
            databases.delete_attribute(
                database_id=config.DATABASE_ID,
                collection_id=config.COLLECTION_ID,
                key='features'
            )
            logger.info("✅ Deleted old features attribute")
            import time
            time.sleep(2)  # Wait for deletion to complete
        except AppwriteException as e:
            logger.warning(f"⚠️  Could not delete old attribute: {e}")
        
        # Create new features attribute (512D array)
        try:
            databases.create_float_attribute(
                database_id=config.DATABASE_ID,
                collection_id=config.COLLECTION_ID,
                key='features',
                required=True,
                array=True
            )
            logger.info("✅ Created new features attribute (float array for 512D)")
        except AppwriteException as e:
            logger.error(f"❌ Error creating attribute: {e}")
            return False
        
        logger.info("🎉 Collection updated successfully!")
        logger.info("   Feature dimension: 512D")
        logger.info("   Ready for high-quality embeddings")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    config.validate()
    update_collection()
