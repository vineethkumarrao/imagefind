"""
Vision Transformer Feature Extractor
State-of-the-art transformer-based image feature extraction
"""

import torch
import torch.nn as nn
from transformers import ViTModel, ViTImageProcessor
from PIL import Image
import numpy as np
import logging

logger = logging.getLogger(__name__)


class ViTFeatureExtractor:
    """Extract features using Vision Transformer"""
    
    def __init__(self, model_name="google/vit-base-patch16-224", feature_dim=768):
        logger.info(f" Initializing Vision Transformer ({model_name})...")
        
        self.feature_dim = feature_dim
        self.processor = ViTImageProcessor.from_pretrained(model_name)
        self.model = ViTModel.from_pretrained(model_name)
        self.model.eval()
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
        
        logger.info(f" ViT extractor ready (Device: {self.device})")
        logger.info(f"   Output: {feature_dim}D feature vectors")
    
    def extract_features(self, image):
        """Extract features from single image"""
        if isinstance(image, str):
            image = Image.open(image).convert("RGB")
        elif not isinstance(image, Image.Image):
            raise ValueError("Image must be PIL Image or path string")
        
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        inputs = self.processor(images=image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        features = outputs.last_hidden_state[:, 0, :].squeeze()
        features = features.cpu().numpy()
        features = features / (np.linalg.norm(features) + 1e-8)
        
        return features.tolist()
    
    def extract_batch_features(self, images):
        """Extract features from multiple images"""
        pil_images = []
        for img in images:
            if isinstance(img, str):
                img = Image.open(img).convert("RGB")
            elif img.mode != "RGB":
                img = img.convert("RGB")
            pil_images.append(img)
        
        inputs = self.processor(images=pil_images, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        features = outputs.last_hidden_state[:, 0, :].cpu().numpy()
        features = features / (np.linalg.norm(features, axis=1, keepdims=True) + 1e-8)
        
        return features.tolist()
