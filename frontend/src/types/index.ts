/**
 * TypeScript interfaces for Quantum Image Retrieval System
 */

export interface SimilarImage {
  id: string;
  filename: string;
  category: string;
  similarity: number;
  image_url: string;
}

export interface UploadedImage {
  filename: string;
  cloudinary_url: string;
}

export interface UploadResponse {
  success: boolean;
  similar_images: SimilarImage[];
  uploaded_image?: UploadedImage;
}

export interface SearchResponse {
  success: boolean;
  similar_images: SimilarImage[];
}

export interface Statistics {
  total_vector_count: number;
  dimension: number;
  index_name: string;
}

export interface StatsResponse {
  success: boolean;
  statistics: Statistics;
}

export interface HealthResponse {
  status: string;
  feature_extractor: string;
  retrieval_system: string;
  appwrite: string;
}

export interface CategoryInfo {
  name: string;
  color: string;
  icon: string;
}

export const CATEGORY_COLORS: Record<string, CategoryInfo> = {
  healthcare: {
    name: "Healthcare",
    color: "#1976d2",
    icon: "🏥",
  },
  satellite: {
    name: "Satellite",
    color: "#2e7d32",
    icon: "🛰️",
  },
  surveillance: {
    name: "Surveillance",
    color: "#ed6c02",
    icon: "📹",
  },
};
