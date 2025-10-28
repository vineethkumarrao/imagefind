/**
 * API Client for backend communication
 * Updated for Cloudinary + Pinecone backend
 */

import axios from "axios";
import type {
  UploadResponse,
  SearchResponse,
  StatsResponse,
  HealthResponse,
} from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Upload an image via backend API (includes feature extraction and similarity search)
 */
export const uploadImage = async (
  file: File,
  onProgress?: (progress: number) => void
): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post<UploadResponse>("/api/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress && progressEvent.total) {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        onProgress(percentCompleted);
      }
    },
  });

  return response.data;
};

/**
 * Upload and store image via backend API (includes feature extraction and storage)
 */
export const uploadAndStore = async (
  file: File,
  category: string,
  onProgress?: (progress: number) => void
): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("category", category);

  const response = await api.post<UploadResponse>(
    "/api/upload-and-store",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted);
        }
      },
    }
  );

  return response.data;
};

/**
 * Search by feature vector
 */
export const searchByFeatures = async (
  features: number[]
): Promise<SearchResponse> => {
  const response = await api.post<SearchResponse>("/api/search", features);
  return response.data;
};

/**
 * Get image URL by image ID
 */
export const getImageUrl = (imageId: string): string => {
  return `${API_BASE_URL}/api/image/${imageId}`;
};

/**
 * Get database statistics
 */
export const getStatistics = async (): Promise<StatsResponse> => {
  const response = await api.get<StatsResponse>("/api/stats");
  return response.data;
};

/**
 * Health check
 */
export const healthCheck = async (): Promise<HealthResponse> => {
  const response = await api.get<HealthResponse>("/api/health");
  return response.data;
};

/**
 * Get categories
 */
export const getCategories = async (): Promise<string[]> => {
  const response = await api.get<{ success: boolean; categories: string[] }>(
    "/api/categories"
  );
  return response.data.categories;
};

export default api;
