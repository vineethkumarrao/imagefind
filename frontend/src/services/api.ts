/**
 * API Client for backend communication
 */

import axios from "axios";
import { storage } from "./appwrite";
import { ID } from "appwrite";
import type {
  UploadResponse,
  SearchResponse,
  StatsResponse,
  HealthResponse,
} from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const APPWRITE_BUCKET_ID =
  import.meta.env.VITE_APPWRITE_BUCKET_ID || "68eed0f200256bafa59e";

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
 * Upload an image directly to Appwrite storage (no backend processing)
 * Useful for faster uploads when you don't need immediate similarity search
 */
export const uploadToAppwriteDirect = async (
  file: File,
  category: string,
  onProgress?: (progress: number) => void
): Promise<UploadResponse> => {
  try {
    // Map category to bucket ID
    const bucketMap: Record<string, string> = {
      healthcare: APPWRITE_BUCKET_ID,
      satellite:
        import.meta.env.VITE_APPWRITE_BUCKET_SATELLITE ||
        "68eed0f500197ae0eaa5",
      surveillance:
        import.meta.env.VITE_APPWRITE_BUCKET_SURVEILLANCE ||
        "68eed0fa00280d73f8c2",
    };

    const bucketId = bucketMap[category] || APPWRITE_BUCKET_ID;

    // Generate unique file ID
    const fileId = ID.unique();

    // Upload to Appwrite storage
    const uploadedFile = await storage.createFile(
      bucketId,
      fileId,
      file,
      undefined,
      (progress) => {
        if (onProgress) {
          const percentCompleted = Math.round(
            (progress.chunksUploaded / progress.chunksTotal) * 100
          );
          onProgress(percentCompleted);
        }
      }
    );

    // Return a response similar to backend upload
    return {
      success: true,
      status: "uploaded",
      message: `Image uploaded successfully to ${category} category`,
      query_image: file.name,
      file_id: uploadedFile.$id,
      total_results: 0,
      high_confidence_results: 0,
      exact_match: null,
      results: [],
    };
  } catch (error) {
    console.error("Direct upload error:", error);
    throw new Error("Failed to upload image to Appwrite");
  }
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
