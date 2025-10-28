"""
Cloudinary Image Service
Handles image upload, optimization, and delivery via CDN
"""

import os
import logging
from typing import Optional, Dict, Any
import cloudinary
import cloudinary.uploader
from cloudinary import CloudinaryImage
from config import config

logger = logging.getLogger(__name__)


class CloudinaryImageService:
    """Service for managing images with Cloudinary"""
    
    def __init__(self):
        """Initialize Cloudinary with credentials from config"""
        cloudinary.config(
            cloud_name=config.CLOUDINARY_CLOUD_NAME,
            api_key=config.CLOUDINARY_API_KEY,
            api_secret=config.CLOUDINARY_API_SECRET,
            secure=True
        )
        logger.info("✅ Cloudinary service initialized")
        logger.info(f"   Cloud: {config.CLOUDINARY_CLOUD_NAME}")
    
    def upload_image(
        self,
        file_data: bytes,
        filename: str,
        category: str
    ) -> Dict[str, Any]:
        """
        Upload image to Cloudinary with optimizations
        
        Args:
            file_data: Image binary data
            filename: Original filename
            category: Image category (healthcare, satellite, surveillance)
            
        Returns:
            Dict with Cloudinary upload result
        """
        try:
            logger.info(f"📤 Uploading {filename} to Cloudinary ({category})...")
            
            # Upload with automatic optimizations
            result = cloudinary.uploader.upload(
                file_data,
                folder=f"quantum-images/{category}",
                public_id=os.path.splitext(filename)[0],
                resource_type="auto",
                quality="auto:good",  # Automatic quality optimization
                fetch_format="auto",  # Auto WebP/AVIF conversion
                overwrite=True,
                unique_filename=True,
                use_filename=True
            )
            
            logger.info(f"✅ Upload successful: {result['public_id']}")
            logger.info(f"   URL: {result['secure_url']}")
            logger.info(f"   Format: {result['format']}")
            logger.info(f"   Size: {result['bytes'] / 1024:.2f} KB")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Cloudinary upload failed: {e}")
            raise
    
    def get_optimized_url(
        self,
        public_id: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        crop: str = "fill"
    ) -> str:
        """
        Get optimized image URL with transformations
        
        Args:
            public_id: Cloudinary public ID
            width: Target width
            height: Target height
            crop: Crop mode (fill, fit, scale, etc.)
            
        Returns:
            Optimized image URL
        """
        transformation = {
            'quality': 'auto:good',
            'fetch_format': 'auto'
        }
        
        if width:
            transformation['width'] = width
        if height:
            transformation['height'] = height
        if width or height:
            transformation['crop'] = crop
        
        url = CloudinaryImage(public_id).build_url(**transformation)
        return url
    
    def delete_image(self, public_id: str) -> bool:
        """
        Delete image from Cloudinary
        
        Args:
            public_id: Cloudinary public ID
            
        Returns:
            True if successful
        """
        try:
            result = cloudinary.uploader.destroy(public_id)
            success = result.get('result') == 'ok'
            
            if success:
                logger.info(f"🗑️ Deleted image: {public_id}")
            else:
                logger.warning(f"⚠️ Delete failed: {public_id}")
                
            return success
            
        except Exception as e:
            logger.error(f"❌ Delete error: {e}")
            return False
    
    def get_image_info(self, public_id: str) -> Optional[Dict[str, Any]]:
        """
        Get image metadata from Cloudinary
        
        Args:
            public_id: Cloudinary public ID
            
        Returns:
            Image metadata or None
        """
        try:
            result = cloudinary.api.resource(public_id)
            return result
        except Exception as e:
            logger.error(f"❌ Failed to get image info: {e}")
            return None
