/**
 * Image Upload Component with Drag & Drop
 * Uploads images via backend API (Cloudinary + Pinecone)
 */

import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import {
  Box,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  LinearProgress,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { uploadImage } from "../services/api";
import type { UploadResponse } from "../types";

interface ImageUploadProps {
  onUploadSuccess: (response: UploadResponse) => void;
}

export const ImageUpload: React.FC<ImageUploadProps> = ({
  onUploadSuccess,
}) => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState<string>("");

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) return;

      setUploading(true);
      setError(null);
      setUploadProgress(`Starting upload of ${acceptedFiles.length} image(s)...`);

      try {
        // Process all files
        for (let i = 0; i < acceptedFiles.length; i++) {
          const file = acceptedFiles[i];
          setUploadProgress(`Processing image ${i + 1} of ${acceptedFiles.length}...`);

          // Upload via backend API (includes feature extraction and similarity search)
          setUploadProgress(`Uploading image ${i + 1} to backend...`);
          const response = await uploadImage(file, (progress) => {
            setUploadProgress(`Image ${i + 1}: Processing ${progress}%`);
          });

          // Only show results for the last image
          if (i === acceptedFiles.length - 1) {
            setUploadProgress("All uploads complete!");
            onUploadSuccess(response);
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Upload failed");
        setUploadProgress("");
      } finally {
        setUploading(false);
        setTimeout(() => setUploadProgress(""), 2000);
      }
    },
    [onUploadSuccess]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
    },
    multiple: true,
    disabled: uploading,
  });

  return (
    <Box sx={{ width: "100%", maxWidth: 800, mx: "auto", mb: 4 }}>
      <Paper
        {...getRootProps()}
        sx={{
          p: 6,
          textAlign: "center",
          cursor: uploading ? "wait" : "pointer",
          border: "2px dashed",
          borderColor: isDragActive ? "primary.main" : "grey.400",
          bgcolor: isDragActive ? "action.hover" : "background.paper",
          transition: "all 0.3s",
          "&:hover": {
            borderColor: "primary.main",
            bgcolor: "action.hover",
          },
        }}
      >
        <input {...getInputProps()} />

        {uploading ? (
          <Box>
            <CircularProgress size={60} />
            <Typography variant="h6" sx={{ mt: 2 }}>
              {uploadProgress || "Processing image..."}
            </Typography>
            <LinearProgress sx={{ mt: 2, maxWidth: 400, mx: "auto" }} />
          </Box>
        ) : (
          <Box>
            <CloudUploadIcon
              sx={{ fontSize: 60, color: "primary.main", mb: 2 }}
            />
            <Typography variant="h5" gutterBottom>
              {isDragActive ? "Drop images here" : "Upload Images"}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Drag & drop images here, or click to select multiple images
            </Typography>
            <Typography
              variant="caption"
              color="text.secondary"
              display="block"
              sx={{ mt: 1 }}
            >
              Supports: PNG, JPG, JPEG, GIF, WebP
            </Typography>
          </Box>
        )}
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};
