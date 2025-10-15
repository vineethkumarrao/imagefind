/**
 * TypeScript interfaces for Quantum Image Retrieval System
 */

export interface ImageResult {
  image_id: string;
  document_id: string;
  filename: string;
  category: "healthcare" | "satellite" | "surveillance";
  similarity: number;
  bucket_id: string;
  storage_path: string;
}

export interface UploadResponse {
  success: boolean;
  query_image: string;
  total_results: number;
  high_confidence_results: number;
  results: ImageResult[];
  // Optional fields for different upload modes
  status?: string;
  message?: string;
  file_id?: string;
  exact_match?: ImageResult | null;
}

export interface SearchResponse {
  success: boolean;
  total_results: number;
  results: ImageResult[];
}

export interface Statistics {
  total_images: number;
  categories: {
    healthcare: number;
    satellite: number;
    surveillance: number;
  };
  buckets: {
    healthcare: string;
    satellite: string;
    surveillance: string;
  };
  quantum_mode: string;
  feature_dimension: number;
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
