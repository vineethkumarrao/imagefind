"""
Appwrite Quantum Retrieval System
Handles database operations and image storage with Appwrite
"""

from typing import List, Dict, Any, Optional
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.query import Query
from appwrite.id import ID
from appwrite.permission import Permission
from appwrite.role import Role
from appwrite.input_file import InputFile
import logging

from config import config

# Import quantum algorithm
try:
    from src.quantum.ae_qip_algorithm import AEQIPAlgorithm
    QUANTUM_AVAILABLE = True
except ImportError:
    QUANTUM_AVAILABLE = False
    logging.warning("⚠️  Quantum algorithm not available")

logger = logging.getLogger(__name__)


class AppwriteQuantumRetrieval:
    """Appwrite-based quantum image retrieval system"""
    
    def __init__(self):
        """Initialize Appwrite client and services"""
        
        # Initialize Appwrite client
        self.client = Client()
        self.client.set_endpoint(config.APPWRITE_ENDPOINT)
        self.client.set_project(config.APPWRITE_PROJECT_ID)
        self.client.set_key(config.APPWRITE_API_KEY)
        
        # Initialize services
        self.databases = Databases(self.client)
        self.storage = Storage(self.client)
        
        # Initialize quantum algorithm if available
        if QUANTUM_AVAILABLE:
            self.quantum_algo = AEQIPAlgorithm()
            logger.info("✅ Quantum algorithm initialized")
        else:
            self.quantum_algo = None
            logger.warning("⚠️  Running without quantum enhancement")
        
        logger.info("✅ Appwrite services initialized")
    
    def upload_image(
        self,
        image_data: bytes,
        filename: str,
        category: str,
        features: List[float]
    ) -> Dict[str, Any]:
        """
        Upload image to Appwrite storage and save features to database
        
        Args:
            image_data: Image binary data
            filename: Image filename
            category: Image category (healthcare, satellite, surveillance)
            features: Feature vector
            
        Returns:
            Dict with upload information
        """
        try:
            # Get bucket ID for category
            bucket_id = config.CATEGORY_BUCKET_MAP.get(category)
            if not bucket_id:
                raise ValueError(f"Unknown category: {category}")
            
            # Generate unique ID
            file_id = ID.unique()
            
            # Upload to storage
            logger.info(f"📤 Uploading {filename} to bucket {bucket_id}...")
            file_result = self.storage.create_file(
                bucket_id=bucket_id,
                file_id=file_id,
                file=InputFile.from_bytes(image_data, filename=filename),
                permissions=[
                    Permission.read(Role.any())
                ]
            )
            
            # Save metadata to database
            logger.info(f"💾 Saving metadata to database...")
            document = self.databases.create_document(
                database_id=config.APPWRITE_DATABASE_ID,
                collection_id=config.APPWRITE_COLLECTION_ID,
                document_id=ID.unique(),
                data={
                    'image_id': file_id,
                    'category': category,
                    'features': features,  # Pass array directly, not JSON string
                    'filename': filename,
                    'storage_path': file_result['$id'],
                    'bucket_id': bucket_id
                },
                permissions=[
                    Permission.read(Role.any())
                ]
            )
            
            logger.info(f"✅ Upload successful: {file_id}")
            
            return {
                'success': True,
                'image_id': file_id,
                'document_id': document['$id'],
                'filename': filename,
                'category': category,
                'bucket_id': bucket_id
            }
            
        except Exception as e:
            logger.error(f"❌ Upload failed: {e}")
            raise
    
    def search_similar_images(
        self,
        query_features: List[float],
        top_k: int = 10,
        confidence_threshold: float = 0.84,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar images using quantum-enhanced similarity
        
        Args:
            query_features: Query feature vector
            top_k: Number of results to return
            confidence_threshold: Minimum similarity threshold
            category: Optional category filter
            
        Returns:
            List of similar images with similarity scores
        """
        try:
            logger.info(f"🔍 Searching for similar images (top_k={top_k})...")
            
            # Build query with high limit to fetch all documents
            queries = [Query.limit(5000)]  # Fetch up to 5000 documents
            if category:
                queries.append(Query.equal('category', category))
            
            # Fetch documents
            result = self.databases.list_documents(
                database_id=config.APPWRITE_DATABASE_ID,
                collection_id=config.APPWRITE_COLLECTION_ID,
                queries=queries
            )
            
            documents = result['documents']
            logger.info(f"📊 Processing {len(documents)} documents...")
            logger.info(f"🎯 Confidence threshold: {confidence_threshold:.4f}")
            
            # Calculate similarities
            similarities = []
            all_similarities = []  # Track all for debugging
            
            for doc in documents:
                try:
                    # Get features (already a list, no need to parse JSON)
                    doc_features = doc['features']
                    
                    # Calculate similarity
                    if self.quantum_algo and config.USE_QUANTUM_INSPIRED:
                        similarity = self.quantum_algo.calculate_similarity(
                            query_features,
                            doc_features
                        )
                    else:
                        # Fallback to classical cosine similarity
                        similarity = self._cosine_similarity(
                            query_features,
                            doc_features
                        )
                    
                    # Track all similarities for debugging
                    all_similarities.append({
                        'filename': doc['filename'],
                        'similarity': similarity
                    })
                    
                    if similarity >= confidence_threshold:
                        similarities.append({
                            'image_id': doc['image_id'],
                            'document_id': doc['$id'],
                            'filename': doc['filename'],
                            'category': doc['category'],
                            'similarity': float(similarity),
                            'bucket_id': doc['bucket_id'],
                            'storage_path': doc['storage_path']
                        })
                        
                except Exception as e:
                    logger.warning(f"⚠️  Error processing document {doc['$id']}: {e}")
                    continue
            
            # Log all similarities for debugging (top 10)
            all_similarities.sort(key=lambda x: x['similarity'], reverse=True)
            logger.info(f"📊 Top 10 ALL similarities (before threshold filter):")
            for i, sim in enumerate(all_similarities[:10]):
                logger.info(f"   {i+1}. {sim['filename']}: {sim['similarity']:.6f}")
            
            # Sort by similarity
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Log top similarities for debugging
            if similarities:
                logger.info(f"📊 Top 5 similarities (after threshold {confidence_threshold:.4f}):")
                for i, sim in enumerate(similarities[:5]):
                    logger.info(f"   {i+1}. {sim['filename']}: {sim['similarity']:.4f}")
            else:
                logger.warning(f"⚠️  No images met threshold {confidence_threshold:.4f}")
            
            # Return top K
            results = similarities[:top_k]
            logger.info(f"✅ Found {len(results)} similar images")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            raise
    
    def get_image(self, image_id: str) -> Optional[bytes]:
        """
        Get image from Appwrite storage
        
        Args:
            image_id: Image ID
            
        Returns:
            Image binary data or None
        """
        try:
            # Find document
            result = self.databases.list_documents(
                database_id=config.APPWRITE_DATABASE_ID,
                collection_id=config.APPWRITE_COLLECTION_ID,
                queries=[
                    Query.equal('image_id', image_id),
                    Query.limit(1)
                ]
            )
            
            if not result['documents']:
                logger.warning(f"⚠️  Image not found: {image_id}")
                return None
            
            doc = result['documents'][0]
            bucket_id = doc['bucket_id']
            file_id = doc['image_id']
            
            # Get file from storage
            file_data = self.storage.get_file_download(
                bucket_id=bucket_id,
                file_id=file_id
            )
            
            return file_data
            
        except Exception as e:
            logger.error(f"❌ Image retrieval failed: {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database and storage statistics
        
        Returns:
            Dict with statistics
        """
        try:
            # Get document counts by category
            stats = {
                'total_images': 0,
                'categories': {}
            }
            
            for category in ['healthcare', 'satellite', 'surveillance']:
                result = self.databases.list_documents(
                    database_id=config.APPWRITE_DATABASE_ID,
                    collection_id=config.APPWRITE_COLLECTION_ID,
                    queries=[
                        Query.equal('category', category),
                        Query.limit(1)
                    ]
                )
                count = result['total']
                stats['categories'][category] = count
                stats['total_images'] += count
            
            # Get bucket information
            stats['buckets'] = {
                'healthcare': config.APPWRITE_BUCKET_HEALTHCARE,
                'satellite': config.APPWRITE_BUCKET_SATELLITE,
                'surveillance': config.APPWRITE_BUCKET_SURVEILLANCE
            }
            
            stats['quantum_mode'] = 'inspired' if config.USE_QUANTUM_INSPIRED else 'true'
            stats['feature_dimension'] = config.FEATURE_DIMENSION
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Statistics retrieval failed: {e}")
            return {
                'error': str(e),
                'total_images': 0,
                'categories': {}
            }
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Similarity score (0-1)
        """
        import numpy as np
        
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        dot_product = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        
        # Normalize to 0-1 range
        similarity = (similarity + 1) / 2
        
        return float(similarity)
