"""
Ensemble Feature Extractor
Combines ResNet-50, ViT, and optionally CLIP for robust features
"""

import torch
import numpy as np
from PIL import Image
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class EnsembleFeatureExtractor:
    """Multi-model ensemble for robust feature extraction"""
    
    def __init__(self, feature_dim=512, use_vit=True, use_clip=False):
        logger.info(" Initializing Ensemble Feature Extractor...")
        
        self.feature_dim = feature_dim
        self.models = {}
        
        from ml.unified_feature_extractor import UnifiedFeatureExtractor
        self.models["resnet"] = UnifiedFeatureExtractor(feature_dim=2048)
        logger.info("    ResNet-50 loaded")
        
        if use_vit:
            try:
                from ml.feature_extractors.vit_extractor import ViTFeatureExtractor
                self.models["vit"] = ViTFeatureExtractor()
                logger.info("    ViT loaded")
            except Exception as e:
                logger.warning(f"    ViT not available: {e}")
        
        if use_clip:
            try:
                import clip
                self.models["clip"], _ = clip.load("ViT-B/32", device="cuda" if torch.cuda.is_available() else "cpu")
                logger.info("    CLIP loaded")
            except Exception as e:
                logger.warning(f"    CLIP not available: {e}")
        
        logger.info(f" Ensemble ready with {len(self.models)} models")
    
    def extract_features(self, image):
        """Extract and fuse features from all models"""
        if isinstance(image, str):
            image = Image.open(image).convert("RGB")
        
        all_features = []
        
        if "resnet" in self.models:
            f_resnet = self.models["resnet"].extract_features(image)
            all_features.append(np.array(f_resnet[:512]) * 0.5)
        
        if "vit" in self.models:
            f_vit = self.models["vit"].extract_features(image)
            all_features.append(np.array(f_vit[:512]) * 0.4)
        
        if "clip" in self.models:
            f_clip = self._extract_clip_features(image)
            all_features.append(np.array(f_clip[:512]) * 0.1)
        
        combined = np.concatenate(all_features)[:self.feature_dim]
        
        if len(combined) < self.feature_dim:
            combined = np.pad(combined, (0, self.feature_dim - len(combined)))
        
        combined = combined / (np.linalg.norm(combined) + 1e-8)
        
        return combined.tolist()
    
    def _extract_clip_features(self, image):
        """Extract CLIP features"""
        import clip
        device = "cuda" if torch.cuda.is_available() else "cpu"
        preprocess = clip.load("ViT-B/32", device=device)[1]
        
        image_input = preprocess(image).unsqueeze(0).to(device)
        with torch.no_grad():
            features = self.models["clip"].encode_image(image_input)
        
        return features.cpu().numpy().squeeze()
