"""
Pinecone Vector Database Service
Handles vector storage, indexing, and similarity search
"""

import logging
from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
import numpy as np
from config import config

logger = logging.getLogger(__name__)


class PineconeVectorService:
    """Service for managing vectors with Pinecone"""
    
    def __init__(self):
        """Initialize Pinecone client and index"""
        try:
            # Initialize Pinecone
            self.pc = Pinecone(api_key=config.PINECONE_API_KEY)
            
            # Check if index exists, create if not
            index_name = config.PINECONE_INDEX_NAME
            
            if index_name not in self.pc.list_indexes().names():
                logger.info(f"📦 Creating Pinecone index: {index_name}")
                self.pc.create_index(
                    name=index_name,
                    dimension=config.FEATURE_DIMENSION,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                logger.info(f"✅ Index created: {index_name}")
            
            # Connect to index
            self.index = self.pc.Index(index_name)
            
            # Get index stats
            stats = self.index.describe_index_stats()
            logger.info("✅ Pinecone service initialized")
            logger.info(f"   Index: {index_name}")
            logger.info(f"   Dimension: {config.FEATURE_DIMENSION}")
            logger.info(f"   Vectors: {stats.total_vector_count}")
            
        except Exception as e:
            logger.error(f"❌ Pinecone initialization failed: {e}")
            raise
    
    def upsert_vector(
        self,
        vector_id: str,
        features: List[float],
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Insert or update a vector in Pinecone
        
        Args:
            vector_id: Unique vector ID
            features: Feature vector (2048D or 512D)
            metadata: Associated metadata (category, filename, url, etc.)
            
        Returns:
            True if successful
        """
        try:
            # Ensure features is a list
            if isinstance(features, np.ndarray):
                features = features.tolist()
            
            # Validate dimension
            if len(features) != config.FEATURE_DIMENSION:
                logger.warning(f"⚠️ Feature dimension mismatch: {len(features)} != {config.FEATURE_DIMENSION}")
                # Pad or truncate if needed
                if len(features) < config.FEATURE_DIMENSION:
                    features = features + [0.0] * (config.FEATURE_DIMENSION - len(features))
                else:
                    features = features[:config.FEATURE_DIMENSION]
            
            # Upsert to Pinecone
            self.index.upsert(
                vectors=[{
                    'id': vector_id,
                    'values': features,
                    'metadata': metadata
                }]
            )
            
            logger.info(f"✅ Vector indexed: {vector_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Upsert failed: {e}")
            return False
    
    def search(
        self,
        query_features: List[float],
        top_k: int = 10,
        category_filter: Optional[str] = None,
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors
        
        Args:
            query_features: Query feature vector
            top_k: Number of results to return
            category_filter: Optional category filter
            min_score: Minimum similarity score threshold
            
        Returns:
            List of similar vectors with metadata and scores
        """
        try:
            # Ensure features is a list
            if isinstance(query_features, np.ndarray):
                query_features = query_features.tolist()
            
            # Validate dimension
            if len(query_features) != config.FEATURE_DIMENSION:
                if len(query_features) < config.FEATURE_DIMENSION:
                    query_features = query_features + [0.0] * (config.FEATURE_DIMENSION - len(query_features))
                else:
                    query_features = query_features[:config.FEATURE_DIMENSION]
            
            # Build filter
            filter_dict = None
            if category_filter:
                filter_dict = {'category': {'$eq': category_filter}}
            
            logger.info(f"🔍 Searching Pinecone (top_k={top_k}, filter={category_filter})...")
            
            # Query Pinecone
            results = self.index.query(
                vector=query_features,
                top_k=top_k,
                filter=filter_dict,
                include_metadata=True
            )
            
            # Process results
            matches = []
            for match in results['matches']:
                score = match['score']
                
                # Apply minimum score threshold
                if score >= min_score:
                    matches.append({
                        'id': match['id'],
                        'score': float(score),
                        'metadata': match.get('metadata', {})
                    })
            
            logger.info(f"✅ Found {len(matches)} matches (threshold: {min_score})")
            
            return matches
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    def delete_vector(self, vector_id: str) -> bool:
        """
        Delete a vector from Pinecone
        
        Args:
            vector_id: Vector ID to delete
            
        Returns:
            True if successful
        """
        try:
            self.index.delete(ids=[vector_id])
            logger.info(f"🗑️ Deleted vector: {vector_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Delete failed: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get index statistics
        
        Returns:
            Dictionary with index stats
        """
        try:
            stats = self.index.describe_index_stats()
            
            return {
                'total_vector_count': int(stats.total_vector_count),
                'dimension': int(config.FEATURE_DIMENSION),
                'index_name': str(config.PINECONE_INDEX_NAME)
            }
            
        except Exception as e:
            logger.error(f"❌ Stats failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                'total_vector_count': 0,
                'dimension': int(config.FEATURE_DIMENSION),
                'index_name': str(config.PINECONE_INDEX_NAME),
                'error': str(e)
            }
    
    def delete_all_vectors(self) -> bool:
        """
        Delete all vectors from index (use with caution!)
        
        Returns:
            True if successful
        """
        try:
            self.index.delete(delete_all=True)
            logger.warning("🗑️ All vectors deleted from index!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Delete all failed: {e}")
            return False
